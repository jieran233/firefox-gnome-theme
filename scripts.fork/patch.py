#!/usr/bin/env python3

from pathlib import Path
import re
import os
import requests
from tqdm import tqdm

def traverse_and_filter_pathlib(root_dir, max_depth, pattern, search_type='f'):
    """
    遍历指定的目录层数，并筛选出符合正则表达式的文件或目录
    
    :param root_dir: 要遍历的根目录
    :param max_depth: 最大的层级深度
    :param pattern: 正则表达式
    :param search_type: 搜索类型，可以是 'f' 或 'd'
    :return: 符合条件的项目列表
    """
    root_path = Path(root_dir)
    regex = re.compile(pattern)
    matches = []

    # Traverse the directory with a generator
    for path in root_path.rglob('*'):
        # Calculate current depth
        current_depth = len(path.relative_to(root_path).parts)

        if current_depth > max_depth:
            continue

        # Match based on the search type
        if search_type == 'f' and path.is_file() and regex.match(path.name):
            matches.append(path)
        elif search_type == 'd' and path.is_dir() and regex.match(path.name):
            matches.append(path)

    return matches


def search_patches_dir(root_dir):
    max_depth = 1
    regex_pattern = r".*\.patches$"
    search_type = 'd'

    result_list = traverse_and_filter_pathlib(root_dir, max_depth, regex_pattern, search_type)
    # change to relative path
    for i in range(0, len(result_list)):
        result_list[i] = os.path.relpath(result_list[i], root_dir)
    return result_list

        
class PatchManager:
    root_dir = ""
    
    def __init__(self, root_dir):
        self.root_dir = root_dir
        
    def __request_file(self, file_or_url):
        r = requests.get(file_or_url, stream=True)
        if r.status_code != 200:
            raise ValueError(f"Failed to fetch file: {file_or_url}")

        # add tqdm progress bar for requests.get
        with tqdm(total=int(r.headers.get('content-length', 0)),
                  desc=f"Fetching file: {file_or_url}",
                  unit='B',
                  unit_scale=True) as pbar:
            patch = ''
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    patch += chunk.decode('utf-8')
                    pbar.update(len(chunk))

        return patch

    
    def patch_add(self, origin_file_or_url, patch_file_or_url_list, position, line_break=2):
        """
        修补操作：添加

        :param origin_file_or_url: 原始文件或其 URL
        :param patch_file_or_url_list: 补丁文件或其 URL 列表
        :param position: 要添加的位置，可以是 'top' 或 'bottom'
        :param line_break: 在原内容和修补内容之间添加的换行符数量
        :return: 修补后的内容
        """ 
        if origin_file_or_url is None:
            origin = ""
        else:
            if origin_file_or_url.startswith('https://') or origin_file_or_url.startswith('http://'):
                origin = self.__request_file(origin_file_or_url)
            else:
                origin_file_or_url = os.path.join(self.root_dir, origin_file_or_url)
                with open(origin_file_or_url, 'r') as f:
                    origin = f.read()

        # 初始化补丁内容
        patches = []

        for patch_file_or_url in patch_file_or_url_list:
            if patch_file_or_url.startswith('https://') or patch_file_or_url.startswith('http://'):
                patch = self.__request_file(patch_file_or_url)
            else:
                patch_file_or_url = os.path.join(self.root_dir, patch_file_or_url)
                with open(patch_file_or_url, 'r') as f:
                    patch = f.read()
        
            patches.append(patch)

        # 根据位置插入补丁内容
        if position == 'top':
            return '\n' * line_break + '\n'.join(reversed(patches)) + '\n' * line_break + origin
        elif position == 'bottom':
            return origin + '\n' * line_break + '\n'.join(patches) + '\n' * line_break
        else:
            raise ValueError(f"Invalid position: {position}. Use 'top' or 'bottom'.")

    def patch_add_match(self, origin_file_or_url, patch_file_or_url_list, match, position, line_break=2):
        """
        修补操作：在指定内容之前/之后添加

        :param origin_file_or_url: 原始文件或其 URL
        :param patch_file_or_url_list: 补丁文件或其 URL 列表
        :param match: 要查找的指定内容
        :param position: 在指定内容之前/之后添加，'before' 或 'after'
        :param line_break: 在原内容和修补内容之间添加的换行符数量
        :return: 修补后的内容
        """
        if origin_file_or_url is None:
            origin = ""
        else:
            if origin_file_or_url.startswith('https://') or origin_file_or_url.startswith('http://'):
                origin = self.__request_file(origin_file_or_url)
            else:
                origin_file_or_url = os.path.join(self.root_dir, origin_file_or_url)
                with open(origin_file_or_url, 'r') as f:
                    origin = f.read()

        # 初始化补丁内容
        patches = []

        for patch_file_or_url in patch_file_or_url_list:
            if patch_file_or_url.startswith('https://') or patch_file_or_url.startswith('http://'):
                patch = self.__request_file(patch_file_or_url)
            else:
                patch_file_or_url = os.path.join(self.root_dir, patch_file_or_url)
                with open(patch_file_or_url, 'r') as f:
                    patch = f.read()

            patches.append(patch)

        if match not in origin:
            raise ValueError(f"Match not found: {match}")

        combined_patch = '\n' * line_break + '\n'.join(patches)

        if position == 'before':
            return origin.replace(match, combined_patch + '\n' * line_break + match)
        elif position == 'after':
            return origin.replace(match, match + '\n' * line_break + combined_patch)
        else:
            raise ValueError(f"Invalid position: {position}. Use 'before' or 'after'.")
    
    def patch_cp_file(self, source_path_or_url, target_dir):
        """
        修补操作：复制文件

        :param source_path_or_url: 源文件或其 URL
        :param target_dir: 目标目录
        :return: 无
        """
        if source_path_or_url.startswith('https://') or source_path_or_url.startswith('http://'):
            content = self.__request_file(source_path_or_url)
        else:
            source_path_or_url = os.path.join(self.root_dir, source_path_or_url)
            with open(source_path_or_url, 'r') as f:
                content = f.read()

        target_dir = os.path.join(self.root_dir, target_dir)
        if not os.path.exists(target_dir): 
            os.makedirs(target_dir)

        with open(os.path.join(target_dir, os.path.basename(source_path_or_url)), 'w') as f:
            f.write(content)
            
    def patch_rm_file(self, file_path):
        """
        修补操作：删除文件

        :param file_path: 文件路径
        :return: 无
        """
        file_path = os.path.join(self.root_dir, file_path)
        if os.path.exists(file_path):
            os.remove(file_path)
    
    def apply_patches(self, patches_data_for_item):
        """
        应用所有修补
        :param patches_data_for_item: 修补数据
        :return: 无
        """
        data = patches_data_for_item
        for patch_file, patch_functions in data['patches_lists'].items():
            print(f"Applying patches to {patch_file}...")
            for func in patch_functions:
                func_name = func.__code__.co_names[0]
                if func_name in ['patch_add', 'patch_add_match']:
                    patched_content = func()
                    with open(os.path.join(self.root_dir, patch_file), 'w') as f:
                        f.write(patched_content)
                elif func_name in ['patch_cp_file', 'patch_rm_file']:
                    func()


def main():
    
    cd = os.path.split(os.path.realpath(__file__))[0]
    root_dir = os.path.realpath(os.path.join(cd, '..'))
    
    patch_manager = PatchManager(root_dir=root_dir)
    
    patches_data = {
        "theme.patches": {
                "original_files": ["theme/gnome-theme.css", "theme.patches/fork/center.css"],
                "patches_lists": {
                    "theme/gnome-theme.css": [lambda: patch_manager.patch_add_match(origin_file_or_url="theme/gnome-theme.css",
                                                                patch_file_or_url_list=["theme.patches/gnome-theme.css.patch.css"],
                                                                match="/* Extensions support */",
                                                                position='before')],
                    "theme/variables.css": [lambda: patch_manager.patch_add_match(origin_file_or_url="theme/variables.css",
                                                                patch_file_or_url_list=["theme.patches/variables.css.patch.css"],
                                                                match="\t/* Animations */",
                                                                position='before')],
                    "theme/parts/csd.css": [lambda: patch_manager.patch_add_match(origin_file_or_url="theme/parts/csd.css",
                                                                patch_file_or_url_list=["theme.patches/parts/csd.css.patch.css"],
                                                                match="\t\t\tbackground: var(--gnome-button-background) !important;",
                                                                position='after')],
                    "theme.patches/fork/center.css": [lambda: patch_manager.patch_cp_file(source_path_or_url="theme.patches/fork/center.css",
                                                                target_dir="theme/fork")],
                    "theme.patches/fork/hide-tabs-toolbar.css": [lambda: patch_manager.patch_cp_file(source_path_or_url="theme.patches/fork/hide-tabs-toolbar.css",
                                                                target_dir="theme/fork")],
                    "theme.patches/fork/sidebar-tweaks.css": [lambda: patch_manager.patch_cp_file(source_path_or_url="theme.patches/fork/sidebar-tweaks.css",
                                                                target_dir="theme/fork")],
                    "theme.patches/colors/cosmic-dark.css": [lambda: patch_manager.patch_cp_file(source_path_or_url="theme.patches/colors/cosmic-dark.css",
                                                                target_dir="theme/colors")],
                    "theme.patches/icons/icons.css": [lambda: patch_manager.patch_cp_file(source_path_or_url="theme.patches/icons/icons.css",
                                                                target_dir="theme/icons")],
                }
            },
        "configuration.patches": {
                "original_files": ["configuration/user.js"],
                "patches_lists": {
                    "configuration/user.js": [lambda: patch_manager.patch_add(origin_file_or_url="configuration/user.js",
                                                                patch_file_or_url_list=reversed([
                                                                    "https://raw.githubusercontent.com/yokoffing/Betterfox/refs/heads/main/user.js",
                                                                    "configuration.patches/user.js.betterfox.override.js",
                                                                    "configuration.patches/user.js.fast-firefox.js",
                                                                    "configuration.patches/user.js.fast-firefox.override.js",
                                                                    "configuration.patches/user.js.ra1ahq.js",
                                                                    "configuration.patches/user.js.ra1ahq.override.js",
                                                                    "configuration.patches/user.js.custom.js"]),
                                                                position='top')]
                }
            }
        }

    results = search_patches_dir(root_dir)
    for item in results:
        if item in patches_data:
            print(f"Found patch: {item}")
            patch_manager.apply_patches(patches_data[item])
    

if __name__ == '__main__':
    main()