from jinja2 import Template
from typing import Dict, List, Any
from viztree.argments import create_base_parser
import json
import os


def make_dir_info(dir_name: str, sub_dirs: List[str] = [], parent_dir_path: str = '', current_path: str = '') -> Dict[str, Any]:
    """
    Make directory object to parse by fancytree.

    Args:
        dir_name (str): The directory name.
        sub_dirs (list): Sub directories of dir_name.
        parent_dir_path (str): Parent directory absolute path of the subdirectory.
        current_path (str): Current path of the subdirectory.

    Returns:
        dict: The made directory object.
    """
    dir_info = {
        "title": dir_name,
        "expanded": True,
        "folder": True,
        "children": [],
    }
    if sub_dirs:
        dir_info['sub_dirs'] = sub_dirs

    if parent_dir_path:
        dir_info['parent_dir_path'] = parent_dir_path

    if current_path:
        dir_info['current_path'] = current_path

    return dir_info


def make_file_info(files: List[Any]) -> List[Any]:
    """
    Make file object to parse by fancytree.

    Args:
        files (list): The files that the directory has.

    Returns:
        list: The made file object.
    """
    file_info_array: List[Dict[str, Any]] = []
    for file_name in files:
        file_info_array.append({
            "title": file_name,
            "file": True
        })

    return file_info_array


def merge_directory_path(path_dict: Dict[int, Any]) -> Dict[str, Any]:
    """
    Merge the directory path to make the the hierarchization of the directory path.

    Args:
        path_dict (dict): The path_dict has the directory information for level 1 or less in the flat state.

    Returns:
        list: The merged directory path.
    """
    _value = None
    # print(json.dumps(path_dict, indent=2))
    for key, value in sorted(path_dict.items(), reverse=True):
        if _value is None:
            _value = value
        else:
            for dir_info in path_dict[key]:
                for dir_one_level_below in _value:
                    if 'sub_dirs' in dir_info and \
                            dir_one_level_below['title'] in dir_info['sub_dirs'] and \
                            dir_one_level_below['parent_dir_path'] == dir_info['current_path']:
                        dir_info['children'] += [dir_one_level_below]

                        # delete unnecessary keys in visualizing the directory tree
                        if 'sub_dirs' in dir_one_level_below:
                            del dir_one_level_below['sub_dirs']
                        if 'current_path' in dir_one_level_below:
                            del dir_one_level_below['current_path']

                # delete unnecessary keys in visualizing the directory tree
                if 'sub_dirs' in dir_info:
                    del dir_info['sub_dirs']

            # delete unnecessary keys in visualizing the directory tree
            for dir_one_level_belowi in _value:
                if 'parent_dir_path' in dir_one_level_belowi:
                    del dir_one_level_belowi['parent_dir_path']

            _value = value

    # delete unnecessary keys in visualizing the directory tree
    if 'parent_dir_path' in path_dict[key][0]:
        del path_dict[key][0]['parent_dir_path']
    if 'current_path' in path_dict[key][0]:
        del path_dict[key][0]['current_path']

    return path_dict[key][0]


def make_tree(startpath: str) -> Dict[str, Any]:
    """
    Make a directory tree based on the specified directory path.

    Args:
        startpath (str): The path to start for getting recursively the directory path.

    Returns:
        dict: The parsed directory tree object.
    """
    top_dir_info: Dict[str, Any] = {}
    path_dict: Dict[int, Any] = {}
    parsed_dict_info_array: List[Any] = []
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        dir_name = os.path.basename(root)

        if level == 0:
            top_dir_info = make_dir_info(dir_name)
            top_dir_info['children'] += make_file_info(files)

        else:
            if level not in path_dict:
                path_dict[level] = []

            parent_dir_path = '/'.join((root.split('/')[:-1]))

            if len(root.split('/')) == 2:
                if path_dict[level]:
                    parsed_dict_info_array.append(merge_directory_path(path_dict))
                    parent_dir_path = ''

                # reset the variables to set new directory information for level 1 or less
                path_dict = {}
                path_dict[level] = []

            dir_info = make_dir_info(dir_name, dirs, parent_dir_path, root)
            dir_info['children'] += make_file_info(files)
            path_dict[level].append(dir_info)

    if path_dict:
        parsed_dict_info_array.append(merge_directory_path(path_dict))

    # merge top_dir_info and parsed_dict_info
    for parsed_dict_info in parsed_dict_info_array:
        top_dir_info['children'].append(parsed_dict_info)

    return top_dir_info


def main():
    args = create_base_parser()
    parsed_dir_info = make_tree(args.path)

    # read template
    with open('/'.join(__file__.split('/')[:-1]) + '/templates/dir_tree_html.j2', 'r') as f:
        template = f.read()

    # generate directory tree html file
    with open('./' + args.save, 'w') as f:
        f.write(Template(template).render(
            tree=json.dumps([parsed_dir_info], indent=2),
            skin=args.skin
        ))


if __name__ == "__main__":
    main()
