"""
Processes DIPPI data
"""
from mcot.pipe.pipeline import In, Out, Var, Ref, Pipeline
from . import dmri
from fsl import wrappers
import numpy as np
import nibabel as nib
import os
from shutil import copyfile, move
from fsl.utils.run import run, runfsl
from fsl.data.image import Image
from pathlib import Path
from fsl.transform import flirt, affine
from collections import defaultdict
import pandas as pd
from mcot.utils._scripts import round_bvals
from scipy import special


preproc_pipe = Pipeline(default_submit={'logdir': 'log'})
preproc_pipe(dmri.topup, minutes=240, override={'echo': '1'})

postproc_pipe = Pipeline(default_submit={'logdir': 'log'})
postproc_pipe(dmri.bedpostx_preproc, override={'echo': '1'}, minutes=15, kwargs=dict(multi_shell=False, ncrossing=2, model='1'))
postproc_pipe(dmri.bedpostx_xfibres, override={'echo': '1'}, queue='cuda.q')
postproc_pipe(dmri.bedpostx_postproc, override={'echo': '1'}, queue='cuda.q', kwargs=dict(multi_shell=False, ncrossing=2, keep_merged=False, model='1'))

merge_pipe = Pipeline(default_submit={'logdir': 'log'})

def get_max_b0(bvals_fn):
    b0, bfirst = sorted(np.unique(round_bvals(np.genfromtxt(bvals_fn, dtype=int))))[:2]
    return (b0 + bfirst) / 2


def pipeline(
    pe_mapping, field_strength, tphase_value, pevar='pedir', 
    output_tree='mcot_pipe_dippi', dmri_tree='mcot_pipe_dmri', 
    merge_tree=None, merge_var='part',
    data_in='data_in', bval_in='bval', bvec_in='bvec',
    topup_nb0=3, total_readout_time=0.05, eddy_peas='b0s',
):
    """
    Creates a pipeline to process DIffusion-Prepared Phase Imaging (DIPPI) data

    :param pe_mapping: maps phase encode directions in filename to actual orientations (e.g., "j+", "i-"). Required if not skipping preprocessing.
    :param field_strength: magnetic field strength of the scanner in Tesla used in DIPPI g-ratio estimation
    :param tphase_value: phase accumulation time in ms
    :param pevar: placeholder in filetree that encodes the phase encode direction in the input data, defaults to 'pedir'
    :param output_tree: sub-tree name where the DIPPI pipeline output will be stored. The sub-tree should match 'mcot_pipe_dippi'
    :param dmri_tree: sub-tree name where the diffusion MRI pipeline output has been or will be stored. The sub-tree should match 'mcot_pipe_dmri'
    :param merge_tree: sub-tree name where the DIPPI merged output should be stored. The sub-tree should match 'mcot_pipe_dippi'. If not provided the DIPPI data will note be merged
    :param merge_var: placeholder in filetree that encodes the dimension along which the filetree should be merged.
    :param data_in: template in filetree where the raw DIPPI data is stored, defaults to 'data_in'
    :param bval_in: template in filetree where the DIPPI b-values are stored, defaults to 'bval'
    :param bvec_in: template in filetree where the gradient orientations are stored, defaults to 'bvec'
    :param topup_nb0: maximum number of b=0 volumes to use per phase encode direction in topup, defaults to 3
    :param total_readout_time: readout time used in topup in s, defaults to 0.05
    :param eddy_peas: how FSL eddy should register the diffusion-weighted data to the b0's; one of ('skip', 'b0s', 'register'), defaults to 'b0s', which uses minimizes the offset in motion parameters between all interspersed b0's and the surrounding diffusion-weighted volumes
    """
    dmri_mapping = dict(
        nodif_ref=dmri_tree + '/nodif',
        mask_ref=dmri_tree + '/nodif_brain_mask',
        **{f'xtract_in_{fn}': f'{dmri_tree}/native_xtract/{fn}' for fn in ['densityNorm', 'localdir', 'density_lengths']}
    )
    res = Pipeline.merge([preproc_pipe, postproc_pipe]).move_to_subtree(output_tree, dict(
        data_in=data_in, bval_in=bval_in,
        bvec_in=bvec_in, pevar=pevar, 
        **dmri_mapping
    ))
    if merge_tree is not None:
        to_merge = ['data', 'bvals', 'bvecs', 'field_orient', 'tphase', 'mask']
        process_merge = Pipeline.merge([
            postproc_pipe.move_to_subtree(merge_tree, dmri_mapping),
            merge_pipe.move_to_subtree(merge_tree, {
                'merge_var': merge_var,
                'affine_in': f"{output_tree}/dippi2dmri",
                'ref_img': f"{dmri_tree}/nodif",
                'dippi2merged': f"{output_tree}/dippi2merged",
                **{f"{name}_in": f"{output_tree}/{name}" for name in to_merge}
            })
        ])
        common_transform = ['R2', 'amplitude', 'width', 'dyads']
        unique_transform = {
            'phase': ['dphase'],
            'grat': ['g_ratio', 'non_myelin'],
        }
        for tree_transform in ['phase', 'grat']:
            for to_transform in common_transform + unique_transform[tree_transform]:
                process_merge(resample, minutes=1, kwargs=dict(
                    input=In(f"{output_tree}/{tree_transform}/{to_transform}"),
                    output=Out(f"{output_tree}/{tree_transform}_to_merged/{to_transform}"),
                    reference=In(f"{merge_tree}/mask"),
                    affine=In(f"{output_tree}/dippi2merged"),
                    dyad=to_transform == 'dyads'
                ))
        res = Pipeline.merge([res, process_merge])
    res.configure(dict(
        topup_nb0=topup_nb0, total_readout_time=total_readout_time, eddy_peas=eddy_peas,
        field_strength=field_strength, tphase_value=tphase_value, pe_mapping=pe_mapping,
    ))
    return res


@preproc_pipe(minutes=30)
def get_diffusion_mask(
    nodif: In, nodif_ref: In, mask_ref: In,
    dippi2dmri: Out, dippi_nodif_in_dmri: Out, dmri2dippi: Out,
    nodif_brain: Out, nodif_brain_mask: Out
):
    """Transform the diffusion mask to DIPPI space"""
    wrappers.flirt(nodif, nodif_ref, omat=dippi2dmri, out=dippi_nodif_in_dmri)
    wrappers.invxfm(dippi2dmri, dmri2dippi)
    wrappers.flirt(
        mask_ref, nodif, out=nodif_brain_mask,
        applyxfm=True,  init=dmri2dippi, interp='nearestneighbour',
    )
    wrappers.fslmaths(nodif).mul(nodif_brain_mask).run(nodif_brain)


def collect_data_for_eddy(data_in, bval_in, bvec_in=None):
    tokeep, _ = dmri.sort_pe_dir(bval_in)
    pename = data_in.dims[0]

    bval = []
    bvec = []
    data = []
    for pe in tokeep:
        data.append(np.asarray(nib.load(data_in.sel({pename: pe}).item()).dataobj))
        if bvec_in is not None:
            bval.append(np.genfromtxt(bval_in.sel({pename: pe}).item(), dtype=int))
            bvec_raw = np.genfromtxt(bvec_in.sel({pename: pe}).item())
            bvec.append(bvec_raw.T if bvec_raw.shape[0] == 3 else bvec_raw)
    if bvec_in is None:
        return np.concatenate(data, 3)
    return np.concatenate(data, 3), np.concatenate(bval, 0), np.concatenate(bvec, 0)


@preproc_pipe(queue='cuda.q')
def eddy(
    data_in: In, bval_in: In, bvec_in: In, acqparams: In, nodif_brain_mask: In, eddy_index: In,
    eddy_dwi_in: Ref, eddy_bval: Out, eddy_bvec_in: Out, base: Ref('mag_eddy/basename'),
    final_image: Ref('mag_eddy/image'), final_bvec: Out('mag_eddy/rotated_bvecs'), 
    final_params: Out('mag_eddy/parameters'), pevar: Var(no_iter=True), 
    topup_basename: Ref('topup/basename'), topup_field: In('topup/fieldcoef'), eddy_peas
    ):
    assert eddy_peas in ('skip', 'b0s', 'register')

    data, bval, bvec = collect_data_for_eddy(data_in, bval_in, bvec_in)
    affine = nib.load(data_in.data[0]).affine

    nib.Nifti1Image(abs(data), affine).to_filename(eddy_dwi_in)
    np.savetxt(eddy_bval, bval, fmt='%d')
    np.savetxt(eddy_bvec_in, bvec, fmt='%.4f')

    kwargs = {}
    if eddy_peas == 'skip':
        kwargs['dont_peas'] = True
    elif eddy_peas == 'b0s':
        kwargs['b0_peas'] = True

    wrappers.eddy_cuda(
        imain=eddy_dwi_in, mask=nodif_brain_mask,
        index=eddy_index, acqp=acqparams,
        bvecs=eddy_bvec_in, bvals=eddy_bval, topup=topup_basename,
        cnr_maps=True, data_is_shelled=True,
        out=base, **kwargs
    )
    os.remove(eddy_dwi_in)
    os.remove(final_image)


@preproc_pipe(minutes=10)
def compare_motion_parameters(
    params: In("mag_eddy/parameters"), echo: Var("echo", no_iter=True), 
    eddy_bval: In, motion_parameters_plot: Out, 
):
    bval = np.genfromtxt(eddy_bval.sel({echo[0]: '1'}).item())
    max_b0 = get_max_b0(bval)

    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(2, 3, figsize=(15, 5))
    for e in echo[1]:
        arr = np.genfromtxt(params.sel({echo[0]: e}).item())
        for idx, ax in enumerate(axes.flatten()): 
            ax.plot(arr[:, idx])
    for idx_b0 in np.where(bval < max_b0)[0]:
        for ax in axes.flatten():
            ax.axvline(idx_b0, ls='--', color='k')
    axes[0, 0].set_xlabel('translations')
    axes[1, 0].set_xlabel('rotations')
    for idx, dim in enumerate('xyz'):
        axes[0, idx].set_title(dim)
        axes[1, idx].set_title('around ' + dim)
    fig.tight_layout()
    fig.savefig(motion_parameters_plot)


@preproc_pipe(queue='cuda.q')
def apply_eddy(
    data_in: In, bval_in: In, eddy_bval: In, eddy_bvec_in: In, acqparams: In, nodif_brain_mask: In, eddy_index: In,
    apply_eddy_in: Ref, base: Ref('apply_eddy/basename'),
    applied_params: Out('apply_eddy/parameters'),
    applied_image: Ref('apply_eddy/image'), pevar: Var(no_iter=True), 
    complex: Var(no_iter=True), eddy_params: In("mag_eddy/parameters"),
    topup_basename: Ref('topup/basename'), topup_field: In('topup/fieldcoef'),
    final_image: Out("complex_eddy_out")
    ):
    complex_name, complex = complex

    affine = nib.load(data_in.data[0]).affine
    imag_skipped = False
    data = collect_data_for_eddy(data_in, bval_in)
    for func_name in complex:
        func = getattr(np, func_name)
        fdata = func(data)
        if func_name == 'imag':
            imag_skipped = np.all(fdata == 0.)
            if imag_skipped:
                print('skipping imaginary')
                with open(applied_params.sel({complex_name: func_name}).item(), 'w') as f:
                    f.write(f"skipping because input image has no imaginary part\n")
                continue
        fn_data = apply_eddy_in.sel({complex_name: func_name}).item()
        nib.Nifti1Image(fdata, affine).to_filename(fn_data)

        wrappers.eddy_cuda(
            imain=fn_data, mask=nodif_brain_mask,
            index=eddy_index, acqp=acqparams,
            bvecs=eddy_bvec_in, bvals=eddy_bval, topup=topup_basename,
            data_is_shelled=True, niter=0, init=eddy_params,
            out=base.sel({complex_name: func_name}).item()
        )
    real_data = np.asarray(nib.load(applied_image.sel({complex_name: 'real'}).item()).dataobj)
    if imag_skipped:
        data = real_data
    else:
        imag_data = np.asarray(nib.load(applied_image.sel({complex_name: 'imag'}).item()).dataobj)
        data = real_data + 1j * imag_data
    nib.Nifti1Image(data, affine).to_filename(final_image)

    for fn in list(apply_eddy_in.data) + list(applied_image.data):
        if os.path.exists(fn):
            os.remove(fn)


@preproc_pipe(queue='cuda.q', override={'echo': '1'})
def apply_eddy_field(
    data_in: In, bval_in: In, eddy_bval: In, acqparams: In, nodif_brain_mask: In, eddy_index: In,
    field_eddy_in: Out, base: Ref('field_eddy/basename'), field_eddy_image_in: Ref,
    field_out: Out('field_eddy/rotated_bvecs'),
    applied_image: Ref('field_eddy/image'), pevar: Var(no_iter=True), 
    eddy_params: In("mag_eddy/parameters"),
    topup_basename: Ref('topup/basename'), topup_field: In('topup/fieldcoef'),
    ):
    data = abs(collect_data_for_eddy(data_in, bval_in))
    affine = nib.load(data_in.data[0]).affine
    img = nib.Nifti1Image(data, affine)
    img.to_filename(field_eddy_image_in)

    field_in = Image(img).getAffine("world", "fsl")[:3, :3] @ np.array([0, 0, 1])
    np.savetxt(field_eddy_in, [field_in] * img.shape[-1], fmt='%.4f')

    wrappers.eddy_cuda(
        imain=field_eddy_image_in, mask=nodif_brain_mask,
        index=eddy_index, acqp=acqparams,
        bvecs=field_eddy_in, bvals=eddy_bval, topup=topup_basename,
        data_is_shelled=True, niter=0, init=eddy_params,
        out=base
    )
    os.remove(field_eddy_image_in)
    os.remove(applied_image)


@preproc_pipe(minutes=10, override={'echo': '1'})
def collect(
    eddy_bval: In, bvals: Out,
    eddy_bvec: In("mag_eddy/rotated_bvecs"), bvecs: Out,
    eddy_field_orient: In("field_eddy/rotated_bvecs"), field_orient: Out,
    nodif_brain_mask: In, complex_eddy_out: In, mask: Out,
    tphase_fn: Out('tphase'), tphase_value, group: Out,
):
    nvols = np.genfromtxt(eddy_bval).size
    np.savetxt(group, np.ones(nvols, dtype=int), fmt='%d')
    for target_fn in (bvals, bvecs, field_orient):
        if os.path.exists(target_fn):
            os.remove(target_fn)
    copyfile(eddy_bval, bvals)
    copyfile(eddy_bvec, bvecs)
    copyfile(eddy_field_orient, field_orient)
    img = nib.load(nodif_brain_mask)
    inside_fov = abs(np.asarray(nib.load(complex_eddy_out).dataobj)).min(-1) > 0
    keep_mask = inside_fov & (img.get_fdata() > 0)
    nib.Nifti1Image(keep_mask.astype(int), img.affine).to_filename(mask)
    np.savetxt(tphase_fn,
        np.full(np.genfromtxt(bvals).shape, int(tphase_value)), fmt='%d',
    )


@preproc_pipe(minutes=10)
def deconfound(
    complex_eddy_out: In, echo: Var(no_iter=True), data: Out,
    bvals: In, bvecs: In, field_orient: In,
    confounded_phase: Ref, deconfound_phase: Ref, deconfound_basename: Ref
):
    echo_name = complex_eddy_out.dims[0]
    img = nib.load(complex_eddy_out.data[0])
    arrs = [np.asarray(nib.load(complex_eddy_out.sel({echo_name: e}).item()).dataobj) for e in '12']
    Path(confounded_phase).parent.mkdir(parents=True, exist_ok=True)
    if np.iscomplexobj(arrs[0]):
        unweighted_phase = arrs[0] / arrs[1]
        phase = unweighted_phase / abs(unweighted_phase) * abs(arrs[1])
        nib.Nifti1Image(phase, img.affine).to_filename(confounded_phase)
        phase_fn = confounded_phase
        nib.Nifti1Image(abs(arrs[0]), img.affine).to_filename(data.sel({echo_name: '1'}).item())
    else:
        copyfile(
            complex_eddy_out.sel({echo_name: '1'}).item(),
            data.sel({echo_name: '1'}).item(),
        )
        phase_fn = complex_eddy_out.sel({echo_name: '2'}).item()

    ref_bval = sorted(np.unique(round_bvals(np.genfromtxt(bvals))))[1]

    run(
        "mcot", "dippi", "deconfound",
        "--in-phase", phase_fn,
        "--basename", deconfound_basename,
        "--bvals", bvals,
        "--bvecs", bvecs,
        "--field", field_orient,
        "--ref-bval", ref_bval,
        log={'tee': True}
    )
    move(deconfound_phase, data.sel({echo_name: '2'}).item())


@postproc_pipe(minutes=10)
def average_sinsq_theta(dyads: In('bpx/dyads1'), bpx_dir: Ref("bpx/"), average_sinsq_theta: Out):
    ref_img = nib.load(dyads)
    total_sinsq = np.zeros(ref_img.shape[:3])
    total_fraction = np.zeros(ref_img.shape[:3])
    for idx in range(1, 4):
        dyads_fn = os.path.join(bpx_dir, f'dyads{idx}.nii.gz')
        if not os.path.isfile(dyads_fn):
            if idx == 1:
                raise ValueError("No input dyads")
            break
        fraction = nib.load(os.path.join(bpx_dir, f'mean_f{idx}samples.nii.gz')).get_fdata()
        sinsq = 1 - nib.load(dyads_fn).dataobj[..., 2] ** 2
        total_sinsq += sinsq * fraction
        total_fraction += fraction
    nib.Nifti1Image(total_sinsq / total_fraction, affine=ref_img.affine).to_filename(average_sinsq_theta)


@postproc_pipe(minutes=24 * 60, kwargs={'partial_fit': Out('grat/partial_fit')})
@postproc_pipe(minutes=24 * 60, kwargs={'partial_fit': Out('phase/partial_fit'), 'only_phase': True})
def partial_fit(
    data: In, bvals: In, bvecs: In, echo: Var(no_iter=True), group: In,
    dyads_in: In('bpx/dyads1'), bpx_dir: Ref("bpx/"), field_orient: In,
    fibre: Var(no_iter=True), fit_job: Var,
    field_strength, tphase: In, partial_fit, only_phase=False
):
    echo_name = echo[0]
    if only_phase:
        args = ('-p', )
    else:
        args = ()
    run(
        "mcot", "dippi", "fit",
        "-1", data.sel({echo_name: '1'}).item(),
        "-2", data.sel({echo_name: '2'}).item(),
        "-o", partial_fit,
        "-b", bvals,
        "-r", bvecs,
        "-t", tphase,
        "-x", bpx_dir,
        "-g", group,
        "-B", str(field_strength),
        "-f", field_orient,
        "--part", str(fit_job), '10',
        *args, log={'tee': True}
    )


@postproc_pipe(minutes=30, kwargs={
    'basename': Ref('phase/basename'),
    'partial_fit': In('phase/partial_fit'),
    **{name + '_out': Out(f'phase/{name}') for name in ['fit', 'dphase', 'R2', 'amplitude', 'width', 'dyads']}
})
@postproc_pipe(minutes=30, kwargs={
    'basename': Ref('grat/basename'),
    'partial_fit': In('grat/partial_fit'),
    **{name + '_out': Out(f'grat/{name}') for name in ['fit', 'g_ratio', 'R2', 'amplitude', 'width', 'dyads', 'non_myelin' ]}
})
def create_maps(
    partial_fit: In, basename: Ref, fibre: Var(no_iter=True), fit_job: Var(no_iter=True), fit_out, mask: In, **output_maps
):
    run([
        "mcot", "dippi", "merge_fits", fit_out, 
    ] + list(partial_fit.data))
    run(
        "mcot", "dippi", "create_maps",
        '-f', fit_out,
        '-b', basename,
        '-r', mask,
    )


@merge_pipe(minutes=30)
def merge(
    data_in: In, data: Out,
    mask_in: In, mask: Out, 
    bvals_in: In, bvals: Out,
    bvecs_in: In, bvecs: Out,
    field_orient_in: In, field_orient: Out,
    tphase_in: In, tphase: Out,
    affine_in: In, ref_img: In,
    merge_var: Var(no_iter=True), echo: Var(no_iter=True),
    group: Out, dmri2dippi: Out, dippi2dmri: Out, dippi2merged: Out
):
    raw_group = [np.zeros(np.genfromtxt(fn).size, dtype=int) + idx for idx, fn in enumerate(bvals_in.data)]
    np.savetxt(group, np.concatenate(raw_group), fmt='%d')

    for fns_in, fn_out, fmt in [
        (bvals_in, bvals, '%d'),
        (tphase_in, tphase, '%d'),
    ]:
        arr = np.concatenate([np.genfromtxt(fn) for fn in fns_in.data])
        np.savetxt(fn_out, arr, fmt=fmt)

    ref_img = Image(ref_img)
    world_indices = []
    all_resolutions = []
    for fn_mask, fn_affine in zip(mask_in.data, affine_in.data):
        img = Image(fn_mask)
        flirt_affine = flirt.readFlirt(fn_affine)
        transform = flirt.fromFlirt(flirt_affine, img, ref_img)
        voxel_indices = np.stack(np.where(img.data > 0), -1)
        world_indices.append(affine.transform(voxel_indices, transform)) 
        all_resolutions.append(abs(affine.decompose(transform, angles=False)[0]))

    world_indices = np.concatenate(world_indices, 0)
    bounding_box = (np.amin(world_indices, 0), np.amax(world_indices, 0))
    print(f"{bounding_box=}")
    resolution = np.amin(all_resolutions, 0)
    print(f"{resolution=}")

    new_qform = affine.scaleOffsetXform(
        scales=[-resolution[0], resolution[1], resolution[2]],
        offsets=[
            bounding_box[1][0] + resolution[0],
            bounding_box[0][1] - resolution[1],
            bounding_box[0][2] - resolution[2],
        ]
    )
    new_shape = np.ceil((bounding_box[1] - bounding_box[0]) / resolution).astype(int) + 2
    print(f"{new_shape=}")
    print(f"{new_qform=}")

    new_ref_img = Image(np.zeros(new_shape), xform=new_qform)

    # update flirt transform
    for fn_img_in, fn_affine_in, fn_affine_out in zip(mask_in.data.flat, affine_in.data.flat, dippi2merged.data.flat):
        img = Image(fn_img_in)
        old_flirt = flirt.readFlirt(fn_affine_in)
        xform = flirt.fromFlirt(old_flirt, img, ref_img)
        new_flirt = flirt.toFlirt(xform, img, new_ref_img)
        flirt.writeFlirt(new_flirt, fn_affine_out)

    for fns_in, fn_out in [
        (bvecs_in, bvecs),
        (field_orient_in, field_orient),
    ]:
        all_vectors = []
        for fn_in, affine_in in zip(fns_in.data.flat, dippi2merged.data.flat):
            raw_vectors = np.genfromtxt(fn_in)
            if raw_vectors.shape[0] == 3:
                raw_vectors = raw_vectors.T
            new_vectors = affine.transform(raw_vectors, flirt.readFlirt(affine_in)[:3, :3], vector=True)
            new_vectors /= np.linalg.norm(new_vectors, axis=-1, keepdims=True)
            all_vectors.extend(new_vectors)
        np.savetxt(fn_out, all_vectors, fmt='%.9f')

    mask_data = []
    echo_1_data = []
    echo_2_data = []
    b0_norms = []

    for fns_in, list_out in [
        (data_in.sel({echo[0]: '1'}), echo_1_data),
        (data_in.sel({echo[0]: '2'}), echo_2_data),
        (mask_in, mask_data),
    ]:
        for fn_in, fn_affine, fn_bval in zip(fns_in.data.flat, dippi2merged.data, bvals_in.data):
            img = Image(fn_in)
            new_flirt = flirt.readFlirt(fn_affine)
            if img.iscomplex:
                real = wrappers.flirt(Image(np.real(img.data), header=img.header), new_ref_img, out=wrappers.LOAD, init=new_flirt, interp='nearestneighbour', applyxfm=True)['out'].data
                img = wrappers.flirt(Image(np.imag(img.data), header=img.header), new_ref_img, out=wrappers.LOAD, init=new_flirt, interp='nearestneighbour', applyxfm=True)['out'].data
                resampled = real + img * 1j
            else:
                resampled = wrappers.flirt(fn_in, new_ref_img, out=wrappers.LOAD, init=new_flirt, interp='nearestneighbour', applyxfm=True)['out'].data

            if list_out is echo_1_data:
                use_b0 = np.genfromtxt(fn_bval) < 500
                b0_norm = np.mean(abs(resampled[..., use_b0]), -1, keepdims=True)
                b0_norms.append(b0_norm)
            
            list_out.append(resampled)

    ref_b0 = np.sum(b0_norms, 0) / np.maximum(np.sum([b0 != 0 for b0 in b0_norms], 0), 1)
    arrs = [
        np.concatenate([a * ref_b0 / np.maximum(b0, 1e-20) for a, b0 in zip(d, b0_norms)], -1)
        for d in (echo_1_data, echo_2_data)
    ]

    Image(np.all(mask_data, 0).astype(int), xform=new_qform).save(mask)
    Image(arrs[0], xform=new_qform).save(data.sel({echo[0]: '1'}).item())
    Image(arrs[1], xform=new_qform).save(data.sel({echo[0]: '2'}).item())

    for fn_transform in (dippi2dmri, dmri2dippi):
        np.savetxt(fn_transform, np.eye(4), fmt='%d')


@postproc_pipe(minutes=20, kwargs={
    **{name: In(f'grat/{name}') for name in ('dyads', 'width', 'amplitude')},
    **{name: Out(f'grat/{name}') for name in ('total_signal', 'delta_sinsq', 'mean_sinsq')},
})
@postproc_pipe(minutes=20, kwargs={
    **{name: In(f'phase/{name}') for name in ('dyads', 'width', 'amplitude')},
    **{name: Out(f'phase/{name}') for name in ('total_signal', 'delta_sinsq', 'mean_sinsq')},
})
def proc_sinsq(
    dyads, width, amplitude,
    total_signal, delta_sinsq, mean_sinsq,
    fibre: Var(no_iter=True), group: In, field_orient: In
):
    ref_img = nib.load(amplitude.data[0])

    if isinstance(width, str):
        width = np.stack([nib.load(width).get_fdata()] * 2, -1)
    else:
        width = np.stack([nib.load(fn).get_fdata() for fn in width.data], -1)
    amplitude = np.stack([nib.load(fn).get_fdata() for fn in amplitude.data], -1)
    dyads = np.stack([nib.load(fn).get_fdata() for fn in dyads.data], -1)
    if width.ndim < amplitude.ndim:
        width = width[..., np.newaxis, :]

    fixel_signal = special.hyp1f1(0.5, 1.5, width) * amplitude
    for idx, fn in enumerate(total_signal.data):
        nib.Nifti1Image(fixel_signal[..., idx], ref_img.affine).to_filename(fn)

    field_orientations = np.genfromtxt(field_orient)
    if field_orientations.shape[0] == 3:
        field_orientations = field_orientations.T
    group_indices = np.genfromtxt(group)

    delta = []
    averaged = []
    for idx_img, idx_group in enumerate(sorted(np.unique(group_indices))):
        use = idx_group == group_indices
        average_field = np.mean(field_orientations[use], 0)
        average_field /= np.linalg.norm(average_field)
        align = 1 - np.sum(dyads * average_field[:, np.newaxis], -2) ** 2
        delta.append(align[..., 1] - align[..., 0])
        averaged.append(np.sum(align * fixel_signal[..., idx_img, :], -1) / np.sum(fixel_signal[..., idx_img, :], -1))
    nib.Nifti1Image(np.stack(averaged, -1), ref_img.affine).to_filename(mean_sinsq)
    nib.Nifti1Image(np.stack(delta, -1), ref_img.affine).to_filename(delta_sinsq)


@postproc_pipe(minutes=10)
def proc_dphase(
    dphase: In('phase/dphase'), total_signal: In('phase/total_signal'), 
    delta_dphase: Out, mean_dphase: Out,
    fibre: Var(no_iter=True)
    ):
    ref_img = nib.load(dphase.data[0])
    dphase_arr = np.stack([nib.load(fn).get_fdata() for fn in dphase.data], -1)
    delta = (((dphase_arr[..., 1] - dphase_arr[..., 0]) + np.pi) % (2 * np.pi)) - np.pi
    nib.Nifti1Image(delta, ref_img.affine).to_filename(delta_dphase)

    signal_arr = np.stack([nib.load(fn).get_fdata() for fn in total_signal.data], -1)
    averaged = np.sum(dphase_arr * signal_arr, -1) / np.sum(signal_arr, -1)
    nib.Nifti1Image(averaged, ref_img.affine).to_filename(mean_dphase)


def resample(
    input,
    output,
    reference: In('mask'),
    affine: In('dmri2dippi'),
    dyad=False,
    **no_iter_vars
):
    if isinstance(input, str):
        fns_in = [input]
        fns_out = [output]
    else:
        fns_in = input.data.flatten()
        fns_out = output.data.flatten()

    for fn_in, fn_out in zip(fns_in, fns_out):
        if dyad:
            runfsl([
                'vecreg', '-i', fn_in, '-r', reference,
                '-o', fn_out, '-t', affine
            ])
        else:
            runfsl([
                'flirt', '-in', fn_in, '-ref', reference,
                '-out', fn_out, '-applyxfm', '-usesqform', 
                '-init', affine
            ])

for fn_in, fn_out in [
    ('densityNorm', 'density'),
    ('localdir', 'orient'),
    ('density_lengths', 'length'),
]:
    postproc_pipe(resample, minutes=20, kwargs=dict(
        input=In(f'xtract_in_{fn_in}'),
        output=Out(f'tract_{fn_out}'),
        tract=Var(no_iter=True)
    ))


@postproc_pipe(minutes=10)
def assign_to_tract(
    tract_orient: In, tract_density: In, tract_length: In, 
    dyads_grat: In('grat/dyads'), g_ratio: In('grat/g_ratio'), 
    amplitude_grat: In('grat/amplitude'), width_grat: In('grat/width'),
    tract_table: Out, tract: Var(no_iter=True), fibre: Var(no_iter=True)
):
    ref_img = nib.load(dyads_grat.sel({fibre[0]: '1'}).item())
    dyads1 = ref_img.get_fdata()
    dyads2 = nib.load(dyads_grat.sel({fibre[0]: '2'}).item()).get_fdata()

    as_dict = defaultdict(list)
    print(f"{tract=}")
    print(f"{fibre=}")
    for selected_tract in tract[1]:
        ref_dyads = nib.load(tract_orient.sel({tract[0]: selected_tract}).item()).get_fdata()
        mask = (
            (nib.load(tract_density.sel({tract[0]: selected_tract}).item()).get_fdata() > 0) &
            np.any(dyads2 != 0, -1)
        )
        if mask.sum() <= 1:
            continue
        use_second = (
            abs(np.sum(dyads2[mask] * ref_dyads[mask], -1)) >
            abs(np.sum(dyads1[mask] * ref_dyads[mask], -1))
        )
        for idx, dim in enumerate('ijk'):
            as_dict[f'voxel_{dim}'].extend(np.where(mask)[idx])
        as_dict['fibre'].extend(use_second.astype(int))
        for fn_name, fn in [
            ('g_ratio', g_ratio),
            ('amplitude', amplitude_grat),
            ('width', width_grat),
            ('sinsq', dyads_grat),
        ]:
            arr1 = np.squeeze(nib.load(fn.sel({fibre[0]: '1'}).item()).get_fdata()[mask])
            arr2 = np.squeeze(nib.load(fn.sel({fibre[0]: '2'}).item()).get_fdata()[mask])
            if fn_name == 'sinsq':
                arr1 = 1 - arr1[..., 2] ** 2
                arr2 = 1 - arr2[..., 2] ** 2
            if arr1.ndim == 2:
                arr1 = arr1.mean(-1)
                arr2 = arr2.mean(-1)
            print(fn_name, mask.sum(), arr1.shape)
            as_dict[fn_name].extend(np.select([use_second, ~use_second], [arr2, arr1]))
            as_dict['other_' + fn_name].extend(np.select([use_second, ~use_second], [arr1, arr2]))
        assert(len(as_dict['amplitude']) == len(as_dict['g_ratio']))

        as_dict['tract'].extend([selected_tract] * mask.sum())
        for fn_name, fn in [
            ('length', tract_length),
            ('density', tract_density),
        ]:
            as_dict[fn_name].extend(nib.load(fn.sel({tract[0]: selected_tract}).item()).get_fdata()[mask])

    as_dataframe = pd.DataFrame.from_dict(as_dict)
    as_dataframe['fixel_index'] = (
        1e7 * as_dataframe['voxel_k'] + 
        1e4 * as_dataframe['voxel_j'] + 
        10 * as_dataframe['voxel_i'] + 
        as_dataframe['fibre']
    ).astype(int)
    as_dataframe.to_csv(tract_table, index=False)