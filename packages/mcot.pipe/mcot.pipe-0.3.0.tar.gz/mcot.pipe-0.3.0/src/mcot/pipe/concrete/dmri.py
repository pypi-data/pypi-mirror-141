"""
Processes dMRI data
"""
from mcot.pipe.pipeline import In, Out, Var, Ref, Pipeline
import nibabel as nib
import numpy as np
from fsl import wrappers
from fsl.utils.run import run, runfsl
from fsl.utils.platform import platform
from shutil import copyfile
from pathlib import Path
import os
from mcot.utils._scripts import round_bvals


_kwargs = {'default_submit': {'logdir': 'log'}}
pipe_preproc = Pipeline(**_kwargs)
pipe_postproc = Pipeline(**_kwargs)
pipe_single_shell = Pipeline(**_kwargs)
pipe_multi_shell = Pipeline(**_kwargs)


def sort_pe_dir(bvals, max_b0=None):
    tokeep = []
    todiscard = []
    pe_name = bvals.dims[0]
    if max_b0 is None:
        all_bvals = round_bvals(np.concatenate(np.genfromtxt(fn) for fn in bvals.data.flatten()))
        b0, bfirst = sorted(np.unique(all_bvals))[:2]
        max_b0 = (b0 + bfirst) / 2 
    for fn in bvals:
        if fn.item() is not None:
            bval = np.genfromtxt(fn.item())
            if not (bval < max_b0).any():
                raise ValueError(f"No b=0 volumes in {fn}")
            if (bval > max_b0).any():
                tokeep.append(fn[pe_name].item())
                continue
        todiscard.append(fn[pe_name].item())
    return tokeep, todiscard


def pipeline(
    multi_shell, skip_preproc=False, pe_mapping=None,
    output_tree=None, data_in="data_in", bval_in="bval_in", 
    bvec_in="bvec_in", mask_in="mask_in", pevar="pevar",
    topup_nb0=3, total_readout_time=0.05,
    ncrossing=3, model=None, bet_f=0.2, bet_g=0.5
    ):
    """
    Creates a diffusion MRI pipeline that can be embedded in a larger pipeline

    :param multi_shell: Set to True for multi-shell data and to False for single-shell data
    :param skip_preproc: skips preprocessing steps (i.e., assume the input data is already preprocessed)
    :param pe_mapping: maps phase encode directions in filename to actual orientations (e.g., "j+", "i-"). Required if not skipping preprocessing.
    :param output_tree: name of the sub-tree containing the "mcot_pipe_dmri" tree. All pipeline output will be written to this sub-tree.
    :param data_in: template name of the input diffusion data (preprocessed if skip_preproc is true, otherwise it should be raw NIFTI data)
    :param bval_in: template name of the input b-values
    :param bvec_in: template name of the input gradient orientations
    :param mask_in: template name of the input mask (ignored unless skip_preproc is set to true)
    :param pevar: name of the placeholder encoding the phase encode direction in the "data_in" template
    :param topup_nb0: maximum number of b0's to use per phase encode direction for FSL's topup
    :param total_readout_time: total readout time in ms
    :param ncrossing: maximum number of crossing fibres per voxel for FSL's bedpostX
    :param model: which model to fit in FSL's bedpostX (default: 1 for single-shell data, 2 for multi-shell data)
    :param bet_f: fractional intensity threshold used in FSL's bet to brain extract the mean b=0 image
    :param bet_g: vertical gradient in fractional intensity threshold used in FSL's bet to brain extract the mean b=0 image
    """
    if not skip_preproc and pe_mapping is None:
        raise ValueError("Setting `pe_mapping` is required when running diffusion MRI preprocessing.")
    pipe = combine_pipe(multi_shell, skip_preproc).move_to_subtree(output_tree, dict(
        data_in=data_in, bval_in=bval_in, bvec_in=bvec_in, mask_in=mask_in, pevar=pevar
    ))
    pipe.configure(dict(
        topup_nb0=topup_nb0, total_readout_time=total_readout_time,
        ncrossing=ncrossing, model=model, bet_f=bet_f, bet_g=bet_g, pe_mapping=pe_mapping,
    ))
    return pipe


def combine_pipe(multi_shell, skip_preproc=False):
    """
    Creates a basic pipeline to process diffusion MRI data

    :param multi_shell: Set to True for multi-shell data and to False for single-shell data
    :param skip_preproc: skips preprocessing steps (i.e., assume the input data is already preprocessed)
    """
    parts = [pipe_postproc]
    parts.append(pipe_multi_shell if multi_shell else pipe_single_shell)
    if skip_preproc:
        return Pipeline.merge(parts).move_to_subtree(other_mappings=dict(
            data='data_in', bvals='bval_in', bvecs='bvec_in', mask='mask_in'
        ))
    else:
        parts.append(pipe_preproc)
        return Pipeline.merge(parts)


@pipe_preproc(minutes=120)
def topup(
    data_in: In, bval_in: In, merged_b0: Out, acqparams: Out, eddy_index: Out,
    topup_basename: Ref('topup/basename'), topup_field: Out('topup/fieldcoef'),
    topup_movement: Out('topup/movement'), unwarped_b0: Out, nodif: Out, 
    pevar: Var(no_iter=True), pe_mapping, topup_nb0, total_readout_time
    ):
    """
    Extracts b0 data and runs topup
    """
    data = []
    acqparams_lines = []
    index = []
    index_count = 1

    ref_img = nib.load(data_in.values.flatten()[0])
    tokeep, todiscard = sort_pe_dir(bval_in)
    pename = data_in.dims[0]

    for pe in tokeep + todiscard:
        img = nib.load(data_in.sel({pename: pe}).item())

        fn_bval = bval_in.sel({pename: pe}).item()
        if fn_bval is None:
            bval = np.zeros(1 if img.ndim <= 3 else img.shape[3])
        else:
            bval = np.genfromtxt(fn_bval)

        indices = np.where(bval < max_b0)[0][:int(topup_nb0)]

        if (img.shape[:3] != ref_img.shape[:3]) or not np.allclose(img.affine, ref_img.affine):
            raise ValueError("Input images to topup should all be in the same space")

        if img.ndim == 4 and bval.shape != (img.shape[3], ):
            raise ValueError(f"b-value shape ({bval.shape}) does not match data shape ({img.shape}) for {fn_bval}")
        
        line = get_acqparams_row(pe_mapping[pe], float(total_readout_time))

        if img.ndim == 3:
            data.append(np.asarray(img.dataobj))
            acqparams_lines.append(line)
            if pe in tokeep:
                index.append(index_count)
                index_count += 1
            continue

        for idx in indices:
            volume = img.dataobj[..., idx]
            assert volume.ndim == 3
            if np.iscomplexobj(volume):
                volume = abs(volume)  # ignore any phase information
            data.append(volume)
            acqparams_lines.append(line)

        if pe in tokeep:
            idx_closest = np.argmin(abs(np.arange(img.shape[-1])[:, np.newaxis] - indices), -1)
            index.extend(idx_closest + index_count)
            index_count += len(indices)

    with open(acqparams, 'w') as f:
        f.writelines(acqparams_lines)

    with open(eddy_index, 'w') as f:
        f.write('\n'.join([str(idx) for idx in index]))
    nib.Nifti1Image(np.stack(data, -1), ref_img.affine).to_filename(merged_b0)

    wrappers.topup(
        imain=merged_b0, datain=acqparams,
        config='b02b0.cnf', out=topup_basename,
        iout=unwarped_b0,
    )
    wrappers.fslmaths(unwarped_b0).Tmean().run(nodif)


def get_acqparams_row(phase_encode, readout_time=0.05):
    """
    Creates a row for the acqparams file from topup based

    >>> get_acqparams_row("j-", 0.01)
    "0 -1 0 0.01\n"
    >>> get_acqparams_row("i")
    "1 0 0 0.05\n"

    :params phase_encode: phase encode direction (string with two elements, first one should be i, j, or k, second one should be + or -)
    :params readout_time: readout time, which will be written to the last column (defaults to 0.05)
    """
    dimensions = ('i', 'j', 'k')
    elements = ['0', '0', '0', str(readout_time)]
    if phase_encode in dimensions:
        elements[dimensions.index(phase_encode)] = '1'
    elif len(phase_encode) == 2:
        orient, sign = phase_encode
        if sign in dimensions:
            orient, sign = sign, orient
        if orient not in dimensions or sign not in '+-':
            raise ValueError(f"Unrecognised phase encode direction {phase_encode}; should by like i- or j+")
        elements[dimensions.index(orient)] = '1' if sign == '+' else '-1'
    else:
        raise ValueError(f"Unrecognised phase encode direction {phase_encode}")
    return ' '.join(elements) + '\n'


@pipe_preproc(minutes=5)
def topup_bet(nodif: In, nodif_brain: Out, nodif_brain_mask: Out, bet_f, bet_g):
    wrappers.bet(nodif, nodif_brain, mask=True, fracintensity=bet_f, g=bet_g)


@pipe_preproc(queue='cuda.q')
def eddy(
    data_in: In, bval_in: In, bvec_in: In, acqparams: In, nodif_brain_mask: In, eddy_index: In,
    eddy_dwi_in: Ref, eddy_bval: Out, eddy_bvec_in: Out, base: Ref('eddy/basename'),
    final_image: Out('eddy/image'), final_bvec: Out('eddy/rotated_bvecs'), 
    pevar: Var(no_iter=True), topup_basename: Ref('topup/basename'), topup_field: In('topup/fieldcoef'),
    ):
    tokeep, _ = sort_pe_dir(bval_in)
    pename = data_in.dims[0]
    if len(tokeep) > 1:
        runfsl(('fslmerge', '-t', eddy_dwi_in) + tuple(data_in.sel({pename: pe}) for pe in tokeep))
        bval = [np.genfromtxt(bval_in.sel({pename: pe}).item()) for pe in tokeep]
        bvec = [np.genfromtxt(bvec_in.sel({pename: pe}).item()) for pe in tokeep]
        bvec_rot = [a.T if a.shape[0] == 3 else a for a in bvec]
        np.savetxt(eddy_bval, np.concatenate(bval, 0))
        np.savetxt(eddy_bvec_in, np.concatenate(bvec_rot, 0))
    else:
        eddy_dwi_in = data_in.sel({pename: tokeep[0]}).item()
        copyfile(bval_in.sel({pename: tokeep[0]}).item(), eddy_bval)
        copyfile(bvec_in.sel({pename: tokeep[0]}).item(), eddy_bvec_in)

    wrappers.eddy_cuda(
        imain=eddy_dwi_in, mask=nodif_brain_mask,
        index=eddy_index, acqp=acqparams,
        bvecs=eddy_bvec_in, bvals=eddy_bval,
        out=base, topup=topup_basename,
        cnr_maps=True, data_is_shelled=True,
    )


@pipe_preproc(minutes=5)
def collect(
    final_image: In('eddy/image'), data: Out,
    final_bvec: In('eddy/rotated_bvecs'), bvecs: Out,
    eddy_bval: In, bvals: Out,
    nodif_brain_mask: In, mask: Out
):
    for source, target in [
        (final_image, data),
        (final_bvec, bvecs),
        (eddy_bval, bvals),
        (nodif_brain_mask, mask),
    ]:
        copyfile(source, target)


@pipe_multi_shell(minutes=20)
def extract_shell(
    data: In, bvals: In, bvecs: In, basename_shell: Ref, 
    data_shell: Out, bval_shell: Out, bvec_shell: Out, bvalue: Var,
):
    runfsl([
        'select_dwi_vols', data, bvals, basename_shell, str(bvalue), '-b', '0', '-obv', bvecs
    ])


@pipe_single_shell(minutes=30, kwargs=dict(
                data_shell=In('data'),
                bval_shell=In('bvals'),
                bvec_shell=In('bvecs'),
))
@pipe_multi_shell(minutes=30)
def dtifit(
    data_shell: In, bval_shell: In, bvec_shell: In, nodif_brain_mask: In,
    basename_dti: Ref("dti/basename"),
    fa: Out("dti/FA"), md: Out("dti/MD"), 
    v1: Out("dti/V1"), v2: Out("dti/V2"), v3: Out("dti/V3"),
    l1: Out("dti/L1"), l2: Out("dti/L2"), l3: Out("dti/L3"),
):
    runfsl([
        'dtifit', '-k', data_shell, '-b', bval_shell, '-r', bvec_shell, 
        '-m', nodif_brain_mask, '-o', basename_dti,
    ])


@pipe_multi_shell(minutes=30)
def dkifit(
    data: In, bvals: In, bvecs: In, mask: In,
    basename_dki: Ref("dki/basename"),
    fa: Out("dki/FA"), md: Out("dki/MD"), 
    v1: Out("dki/V1"), v2: Out("dki/V2"), v3: Out("dki/V3"),
    l1: Out("dki/L1"), l2: Out("dki/L2"), l3: Out("dki/L3"),
    k1: Out("dki/K1"), k2: Out("dki/K2"), k3: Out("dki/K3"), mk: Out('dki/MK'),
):
    runfsl([
        'dtifit', '-k', data, '-b', bvals, '-r', bvecs, 
        '-m', mask, '-o', basename_dki, '--kurdir'
    ])


@pipe_single_shell(minutes=30, kwargs={'multi_shell': False})
@pipe_multi_shell(minutes=30, kwargs={'multi_shell': True})
def bedpostx_preproc(
    data: In, bvals: In, bvecs: In, mask: In, 
    bval_bpx: Out("bpx/bvals"), bvec_bpx: Out("bpx/bvecs"), mask_bpx: Out("bpx/nodif_brain_mask"),
    bpx_split_data: Ref, bpx_working_dir: Ref, bpx_dir: Ref, bpx_job: Var(no_iter=True),
    commands: Out('bpx/commands'), bpx_split_log: Ref, model, ncrossing, multi_shell
):
    Path(bpx_working_dir).mkdir(exist_ok=True)
    copyfile(bvals, bval_bpx)
    copyfile(bvecs, bvec_bpx)
    copyfile(mask, mask_bpx)
    basename = bpx_dir[:bpx_dir.rfind('.bedpostX')]
    dim_name, bpx_job = bpx_job
    runfsl(
        'split_parts_gpu', data, mask_bpx, bval_bpx, bvec_bpx, 'NULL', '0', str(len(bpx_job)), bpx_dir, log={'tee': True}
    )
    nvox = np.sum(nib.load(mask).get_fdata() > 0)
    if model is None:
        model = '2' if multi_shell else '1'
    with open(commands, 'w') as f:
        for idx in bpx_job:
            f.write(
                f"xfibres_gpu --data={bpx_split_data.sel({dim_name: idx}).item()} --mask={mask} "
                f"-b {bvals} -r {bvecs} --forcedir --logdir={bpx_split_log.sel({dim_name: idx}).item()} "
                f"--nf={ncrossing} --fudge=1 --bi=1000 --nj=1250 --se=25 --model={model} --cnonlinear "
                f"{basename} {idx} {len(bpx_job)} {nvox}\n"
            )


@pipe_postproc(queue='cuda.q')
def bedpostx_xfibres(
    commands: In('bpx/commands'), bpx_job: Var, bpx_done: Out
):
    with open(commands, 'r') as f:
        all_commands = f.readlines()
    runfsl(all_commands[int(bpx_job)].strip(), log={'tee': True})
    run("touch", bpx_done)


@pipe_single_shell(minutes=30, kwargs={'multi_shell': False})
@pipe_multi_shell(minutes=30, kwargs={'multi_shell': True})
def bedpostx_postproc(
    data: In, bvals: In, bvecs: In, mask: In,
    dyads1: Out('bpx/dyads1'), bpx_working_dir: Ref, bpx_dir: Ref, 
    bpx_job: Var(no_iter=True), bpx_done: In, model, ncrossing, multi_shell,
    keep_merged=True,
):
    nvox = np.sum(nib.load(mask).get_fdata() > 0)
    model = model
    if model is None:
        model = '2' if multi_shell else '1'
    basename = bpx_dir[:bpx_dir.rfind('.bedpostX')]
    os.mkdir(os.path.join(bpx_dir, 'xfms'))
    run(
        f"bedpostx_postproc_gpu.sh --data={data} --mask={mask} "
        f"-b {bvals} -r {bvecs} --forcedir --logdir={bpx_working_dir} "
        f"--nf={ncrossing} --fudge=1 --bi=1000 --nj=1250 --se=25 --model={model} --cnonlinear "
        f"{nvox} {len(bpx_job[1])} {basename} {platform.fsldir}\n",
        log={'tee': True}
    )
    if not keep_merged:
        for fn in Path(bpx_dir).glob("merged_*samples.nii.gz"):
            os.remove(fn)


@pipe_postproc(minutes=120)
def dMRI_to_standard(
    dti_FA: In('dti/FA'), dMRI2std_aff: Out, dMRI2std_warp: Out
):
    fa_standard = os.path.join(platform.fsldir, 'data', 'standard', 'FSL_HCP1065_FA_1mm.nii.gz')
    wrappers.flirt(dti_FA, fa_standard, omat=dMRI2std_aff)
    wrappers.fnirt(dti_FA, ref=fa_standard, aff=dMRI2std_aff, cout=dMRI2std_warp)


@pipe_postproc(minutes=30)
def invert_dMRI_to_standard(
    dti_FA: In('dti/FA'), dMRI2std_warp: In, std2dMRI_warp: Out
):
    wrappers.invwarp(dMRI2std_warp, dti_FA, std2dMRI_warp)


@pipe_postproc(queue='cuda.q', kwargs=dict(
    ptx_options=Out('std_ptx_options'),
    densityNorm=Out('std_xtract/densityNorm'), 
    xtract=Ref('std_xtract/'),
    length=Out('std_xtract/density_lengths'), 
    orient=Out('std_xtract/localdir'),
    tract=Var('std_xtract/tract', no_iter=True),
    native=False,
))
@pipe_postproc(queue='cuda.q')
def xtract(
    dyad1: In('bpx/dyads1'), bpx_dir: Ref('bpx_dir'),
    dMRI2std_warp: In, std2dMRI_warp: In, ptx_options: Out('native_ptx_options'),
    densityNorm: Out('native_xtract/densityNorm'), xtract: Ref('native_xtract'),
    length: Out('native_xtract/density_lengths'), orient: Out('native_xtract/localdir'),
    tract: Var('native_xtract/tract', no_iter=True), native=True, use_gpu=True
):
    with open(ptx_options, 'w') as f:
        f.write('--opathdir\n')
    flags = []
    if native:
        flags.append('-native')
    if use_gpu:
        flags.append('-gpu')
    run([
        'xtract', '-bpx', bpx_dir, '-out', xtract,
        '-species', 'HUMAN',
        '-stdwarp', std2dMRI_warp, dMRI2std_warp,
        '-ptx_options', ptx_options,
    ] + flags)


pipe_multi_shell.default_output = ['dki/FA']
pipe_postproc.default_output = ['dti/FA']
pipe_preproc.default_output = ['data']