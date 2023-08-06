from ..pipeline import FileTree
import pkg_resources
import os
from file_tree.parse_tree import available_subtrees


def load():
    directory = pkg_resources.resource_filename(__name__, "trees")
    for filename in os.listdir(directory):
        available_subtrees['mcot_pipe_' + filename] = FileTree.read(os.path.join(directory, filename)).to_string()