"""
Defines the pipeline before a FileTree is provided

At the first level it is simply a collection of functions with mapping from the function parameters to input/output/reference basenames
"""
from fsl.utils.fslsub import SubmitParams
from typing import List, Optional, Set, Tuple, Dict, Collection, Callable, Union, Any
import argparse
from dataclasses import dataclass
from file_tree import FileTree
import numpy as np
import os
from .datalad import get_tree
from itertools import chain
from copy import copy
import inspect

class Pipeline:
    """Collection of python functions forming a pipeline

    You can either create a new pipeline (`from mcot.pipe import Pipeline; pipe = Pipeline()`) or use a pre-existing one (`from mcot.pipe import pipe`)

    Scripts are added to a pipeline by using the pipeline as a decorator (see :meth:`__call__`).

    To run the pipeline based on instructions from the command line run `pipe.cli(tree)`, 
    where tree is a FileTree defining the directory structure of the pipeline input & output files.

    :ivar scripts: list of :class:`PipedFunction`, which define the python functions forming the pipeline and their input/output templates
    """
    def __init__(self, scripts=None, default_output=None, default_submit={}):
        """Create a new empty pipeline
        """
        if scripts is None:
            scripts = []
        if default_output is None:
            default_output = []
        self.scripts: List[PipedFunction] = list(scripts)
        self.default_output: List[str] = list(default_output)
        self.default_submit = default_submit

    def __call__(self, function=None, kwargs=None, no_iter=None, override=None, as_path=False, **submit_params):
        """Adds a python function as a :class:`PipedFunction` to the pipeline

        .. code-block:: python

            from mcot.pipe import pipe, In, Out, Ref, Var

            @pipe(logdir='log', minutes=41)
            def func(in_path: In, out_path: Out, ref_path: Ref, placeholder_key: Var):
                pass

        :param function: Optionally provide the function directly
        :param kwargs: maps function keyword arguments to templates, variables, or actual values.
        :param no_iter: optional set of parameters not to iterate over
        :param as_path: Provides function with `pathlib.Path` objects instead of strings (default: False)
        :param override: dictionary overriding the placeholders set in the filetree
        :param submit_params: arguments to use when submitting this job to the cluster
        """
        submit_params = SubmitParams(**self.default_submit, **submit_params)
        def wrapper(func):
            self.scripts.append(PipedFunction(func, submit_params=submit_params, kwargs=kwargs, no_iter=no_iter, override=override, as_path=as_path))
            return func
        if function is None:
            return wrapper
        wrapper(function)

    def make_concrete(self, tree: FileTree):
        """
        Splits the pipeline into individual jobs

        :param tree: set of templates for the input/output/reference files with all possible placeholder values
        """
        from .job import ConcretePipeline, FileTarget
        all_targets: Dict[str, FileTarget] = {}
        jobs = {}
        for script in self.scripts:
            jobs[script] = script.get_jobs(tree, all_targets)
        return ConcretePipeline(tree, jobs, all_targets)

    def cli(self, tree: Optional[FileTree]=None, description="Runs the pipeline", include_vars=None, exclude_vars=(), cli_arguments=None):
        """
        Runs the pipeline from the command line

        :param tree: `file_tree.FileTree` object describing the directory structure for the input/output files (defaults to datalad tree).
        :param description: Description to give of the script in the help message.
        :param include_vars: if provided, only include expose variables in this list to the command line
        :param exclude_vars: exclude variables in this list from the command line
        """
        from .job import RunMethod
        if len(self.scripts) == 0:
            raise ValueError("The pipeline does not contain any scripts...")
        if tree is None:
            tree = get_tree()
            if tree is None:
                raise ValueError("No reference filetree for pipeline found")
        parser = argparse.ArgumentParser(description)
        templates = set.union(*[script.filter_templates(output=True) for script in self.scripts])

        parser.add_argument("templates", nargs="*", default=self.default_output,
                            help=f"For which templates to produce the files (default: {', '.join(self.default_output)})")
        parser.add_argument("-m", '--pipeline_method', default=RunMethod.default().name,
                            choices=[m.name for m in RunMethod],
                            help=f"method used to run the jobs (default: {RunMethod.default().name})")
        parser.add_argument("-o", '--overwrite', action='store_true', help="If set overwrite any requested files")
        parser.add_argument("-d", '--overwrite_dependencies', action='store_true',
                            help="If set also overwrites dependencies of requested files")
        parser.add_argument("-r", '--raise_errors', action='store_true',
                            help="If set raise errors rather than catching them")
        parser.add_argument("-j", '--job-hold', default='',
                            help='Place a hold on this pipeline until job has completed')
        parser.add_argument("--datalad", action='store_true',
                            help="run datalad get on all input data before running/submitting the jobs")
        for var, values in tree.placeholders.items():
            if not isinstance(var, str):
                continue
            if '/' in var:
                continue
            if var in exclude_vars:
                continue
            if include_vars is not None and var not in include_vars:
                continue
            if np.asarray(values).ndim == 1:
                default = ','.join([str(v) for v in values])
            else:
                default = str(values)
            parser.add_argument(f"--{var}", nargs='+', help=f"Use to set the possible values of {var} to the selected values (default: {default})")
        
        args = parser.parse_args(cli_arguments)
        not_in_tree = [template for template in args.templates if template not in tree.template_keys()]
        if len(not_in_tree) > 0:
            raise ValueError(f"Requested templates {not_in_tree} are not defined in the FileTree")
        unrecognised_templates = set(args.templates).difference(templates)
        if len(unrecognised_templates) > 0:
            raise ValueError(f"Requested templates {unrecognised_templates} cannot be produced by this pipeline")
        for var in tree.placeholders:
            if isinstance(var, str) and getattr(args, var, None) is not None:
                tree.placeholders[var] = getattr(args, var)
        concrete = self.make_concrete(tree)
        torun = concrete.filter(args.templates, overwrite=args.overwrite, overwrite_dependencies=args.overwrite_dependencies)
        torun.report(args.templates)
        torun.run(RunMethod[args.pipeline_method], raise_errors=args.raise_errors, wait_for=() if args.job_hold == '' else args.job_hold.split(','), datalad=args.datalad)

    def move_to_subtree(self, sub_tree=None, other_mappings=None):
        """
        Creates a new pipeline that runs in a sub-tree of a larger tree rather than at the top level

        :param sub_tree: name of the sub-tree in the FileTree
        :param other_mappings: other mappings between templates or placeholder names and their new values
        """
        def update_key(key):
            if key in other_mappings:
                return other_mappings[key]
            elif sub_tree is not None:
                return sub_tree + '/' + key
            else:
                return key

        if other_mappings is None:
            other_mappings = {}
        all_scripts = [script.move_to_subtree(sub_tree, other_mappings) for script in self.scripts]
        new_default_submit = copy(self.default_submit)
        if 'logdir' in new_default_submit:
            new_default_submit['logdir'] = update_key(new_default_submit['logdir'])
        return Pipeline(all_scripts, [update_key(key) for key in self.default_output], new_default_submit)

    @classmethod
    def merge(cls, pipelines: Collection["Pipeline"]):
        """
        Combines multiple pipelines into a single one

        :param pipelines: pipelines containing part of the jobs
        :return: parent pipeline containing all of the jobs in pipelines
        """
        new_pipeline = Pipeline()
        for pipeline in pipelines:
            new_pipeline.scripts.extend([s.copy() for s in pipeline.scripts])
            new_pipeline.default_output.extend(pipeline.default_output)
        return new_pipeline

    def find(self, function: Union[str, Callable]):
        """
        Iterate over any pipeline scripts that run the provided function

        Either the function itself or the name of the function can be given
        """
        for script in list(self.scripts):
            if script.function == function or getattr(script.function, '__name__', None) == function:
                yield script

    def remove(self, function: Union[str, Callable]):
        """
        Remove any pipeline scripts that run the provided function from the pipeline

        Either the function itself or the name of the function can be given
        """
        for script in self.find(function):
            self.scripts.remove(script)

    def configure(self, kwargs):
        """
        Overrides the values passed on to the keyword arguments of all the scripts

        Any keywords not expected by a script will be silently skipped for that script
        """
        for script in self.scripts:
            try:
                script.configure(kwargs, allow_new_keywords=False, check=False)
            except KeyError:
                pass

class PipedFunction:
    """
    Represents a function stored in a pipeline
    """
    def __init__(self, function, submit_params: SubmitParams, kwargs=None, no_iter=None, override=None, as_path=True):
        """
        Wraps a function with additional information to run it in a pipeline

        :param function: python function that will be run in pipeline
        :param submit_params: parameters to submit job running python function to cluster using `fsl_sub`
        :param kwargs: maps function keyword arguments to templates, variables, or actual values.
        :param templates: maps function keyword arguments to templates in the FileTree with additional information on whether the file is input/output/reference
        :param no_iter: which parameters to not iterate over (i.e., they are passed to the function in an array)
        :param override: dictionary overriding the placeholders set in the filetree
        :param as_path: whether to pass on pathlib.Path objects instead of strings to the functions (default: True)
        """
        self.function = function
        self.submit_params = submit_params
        if override is None:
            override = {}
        self.override = override
        self.as_path = as_path

        self.placeholders: Dict[str, PlaceHolder] = {}
        self.templates: Dict[str, Template] = {}
        self.kwargs: Dict[str, Any] = {}

        self.configure(function.__annotations__)

        if kwargs is not None:
            self.configure(kwargs)

        if no_iter is None:
            no_iter = set()
        self.explicit_no_iter = set(no_iter)

    def copy(self, ):
        """
        Creates a copy of this PipedFunction for pipeline merging
        """
        new_script = copy(self)
        new_script.override = dict(self.override)
        new_script.placeholders = dict(self.placeholders)
        new_script.templates = dict(self.templates)
        new_script.kwargs = dict(self.kwargs)
        self.explicit_no_iter = set(self.explicit_no_iter)
        return new_script

    @property
    def no_iter(self, ) -> Set[str]:
        """
        Sequence of placeholder names that should not be iterated over
        """
        res = {key if value.key is None else value.key for key, value in self.placeholders.items() if value.no_iter}
        res.update(self.explicit_no_iter)
        return res

    def configure(self, kwargs, allow_new_keywords=True, check=True):
        """
        Overrides the values passed on to the keyword arguments of the script

        :param kwargs: new placeholders/templates/values for keyword arguments
        :param allow_new_keywords: if set to False, don't allow new keywords
        """
        bad_keys = []
        signature = inspect.signature(self.function)
        has_kws = any(param.kind == param.VAR_KEYWORD for param in signature.parameters.values())

        if not allow_new_keywords:
            existing_kws = set(signature.parameters)
            if has_kws:
                for d in (self.placeholders, self.templates, self.kwargs):
                    existing_kws.update(d.keys())
            if check:
                bad_keys = {key for key in kwargs.keys() if key not in signature.parameters}
                raise KeyError(f"Tried to configure {self} with keys that are not expected by the function: {bad_keys}")
        for key, value in kwargs.items():
            if not allow_new_keywords and key not in existing_kws:
                continue
            for d in (self.placeholders, self.templates, self.kwargs):
                if key in d:
                    del d[key]
            if isinstance(value, PlaceHolder):
                self.placeholders[key] = value
            elif isinstance(value, Template):
                self.templates[key] = value
            else:
                self.kwargs[key] = value

    def filter_templates(self, output=False) -> Set[str]:
        """
        Find all input or output template keys

        :param output: if set to True select the input rather than output templates
        :return: set of input or output templates
        """
        res = set()
        for kwarg_key, template in self.templates.items():
            if ((template.input and not output) or
                (template.output and output)):
                res.add(kwarg_key if template.key is None else template.key)
        return res

    def iter_over(self, tree: FileTree) -> Tuple[str, ...]:
        """
        Finds all the placeholders that should be iterated over before calling the function

        These are all the placeholders that affect the input templates, but are not part of `self.no_iter`.

        :param tree: set of templates with placeholder values
        :return: placeholder names to be iterated over sorted by name
        """
        tree = tree.update(**self.override)
        in_vars = self.all_placeholders(tree, False)
        out_vars = self.all_placeholders(tree, True)

        updated_no_iter = {
            tree.placeholders.linkages.get(
                tree.placeholders.find_key(key),
                tree.placeholders.find_key(key),
            ) for key in self.no_iter
        }
        all_in = in_vars.union(updated_no_iter)
        if len(out_vars.difference(all_in)) > 0:
            raise ValueError(f"{self}: Output template depends on {out_vars.difference(all_in)}, which none of the input templates depend on")
        return tuple(sorted(
            in_vars.difference(updated_no_iter), 
            key=lambda a: a if isinstance(a, str) else ''.join(sorted(a))))
        
    def get_jobs(self, tree: FileTree, all_targets: Dict):
        """
        Get a list of all individual jobs defined by this function

        :param tree: set of templates with placeholder values
        :param all_targets: mapping from filenames to Target objects used to match input/output filenames between jobs
        :return: sequence of jobs
        """
        from .job import SingleJob
        tree = tree.update(**self.override)
        to_iter = self.iter_over(tree)
        jobs = [SingleJob(self, sub_tree, all_targets, to_iter) for sub_tree in tree.iter_vars(to_iter)]
        return jobs
        
    def all_placeholders(self, tree: FileTree, output=False) -> Set[str]:
        """
        Identify the multi-valued placeholders affecting the input/output templates of this function

        :param tree: set of templates with placeholder values
        :param output: if set to True returns the placeholders for the output than input templates
        :return: set of all placeholders that affect the input/output templates
        """
        res = set()
        for t in self.filter_templates(output):
            res.update(tree.get_template(t).placeholders())
        if not output:
            for key, variable in self.placeholders.items():
                res.add(key if variable.key is None else variable.key)

        bad_keys = {key for key in res if key not in tree.placeholders}
        if len(bad_keys) > 0:
            raise ValueError(f"No value set for placeholders: {bad_keys}")

        _, only_multi = tree.placeholders.split()
        multi_keys = {only_multi.find_key(key) for key in res if key in only_multi}
        return {only_multi.linkages.get(key, key) for key in multi_keys}


    def move_to_subtree(self, sub_tree=None, other_mappings=None):
        """
        Creates a new wrapped function that runs in a sub-tree of a larger tree rather than at the top level

        :param sub_tree: name of the sub-tree in the FileTree
        :param other_mappings: other mappings between templates or placeholder names and their new values
        """
        def update_key(key):
            if key in other_mappings:
                return other_mappings[key]
            elif sub_tree is not None:
                return sub_tree + '/' + key
            else:
                return key

        def update_kwargs(input_dict):
            kwargs = {}
            for key, value in input_dict.items():
                kwargs[key] = value
                if isinstance(value, PlaceHolder) or isinstance(value, Template):
                    use_key = value.key if value.key is not None else key
                    kwargs[key] = value(update_key(use_key))
            return kwargs

        if other_mappings is None:
            other_mappings = {}
        new_script = copy(self)
        new_script.templates = update_kwargs(self.templates)
        new_script.placeholders = update_kwargs(self.placeholders)
        new_script.override = {update_key(key): value for key, value in self.override.items()}
        new_script.submit_params = copy(self.submit_params)
        if new_script.submit_params.logdir is not None:
            new_script.submit_params.logdir = update_key(new_script.submit_params.logdir)
        return new_script

    def __repr__(self, ):
        return f"PipedFunction({self.function.__name__})"


@dataclass
class Template(object):
    key: Optional[str] = None
    input: bool = False
    output: bool = False

    def __call__(self, key=None):
        return Template(key, self.input, self.output)

@dataclass
class PlaceHolder(object):
    key: Optional[str] = None
    no_iter: bool = False
    enumerate: bool = False

    def __call__(self, key=None, no_iter=None, enumerate=None):
        if no_iter is None:
            no_iter = self.no_iter
        if enumerate is None:
            enumerate = self.enumerate
        return PlaceHolder(key, no_iter, enumerate)


In = Template(input=True)
Out = Template(output=True)
Ref = Template()
Var = PlaceHolder()


def to_templates_dict(input_files=(), output_files=(), reference_files=()):
    """Helper function to convert a sequence of input/output/reference files into a template dictionary

    Args:
        input_files (sequence, optional): Template keys representing input files. Defaults to ().
        output_files (sequence, optional): Template keys representing output files. Defaults to ().
        reference_files (sequence, optional): Template keys representing reference paths. Defaults to ().

    Raises:
        KeyError: If the same template key is used as more than one of the input/output/reference options

    Returns:
        dict: mapping of the keyword argument names to the Template objects
    """
    res = {}
    for files, cls in [
        (input_files, In),
        (output_files, Out),
        (reference_files, Ref),
    ]:
        for name in files:
            if isinstance(name, str):
                short_name = name.split('/')[-1]
            else:
                short_name, name = name
            if name in res:
                raise KeyError(f"Dual definition for template {name}")
            res[short_name] = cls(name)

    return res


pipe = Pipeline()
