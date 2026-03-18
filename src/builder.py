import os
import shutil

from .systems import markdown_to_html_node

STATIC_DIR = "static"
PUBLIC_DIR = "public"

def _del_recursive(path: str, del_root_dir = True):
    for item in os.listdir(path):
        item = os.path.join(path, item)
        if os.path.isdir(item):
            _del_recursive(item)
        else:
            os.remove(item)
    if del_root_dir:
        os.rmdir(path)

def _cpy_recursive(from_path: str, to_path: str):
    for item in os.listdir(from_path):
        new_from_path = os.path.join(from_path, item)
        if os.path.isdir(new_from_path):
            new_to_path = os.path.join(to_path, item)
            os.mkdir(new_to_path)
            _cpy_recursive(new_from_path, new_to_path)
        else:
            shutil.copy2(new_from_path, to_path)



def build_public():
    from_path = STATIC_DIR
    to_path = PUBLIC_DIR
    if not os.path.exists(from_path):
        raise NotADirectoryError(f"could not find a directory at {from_path}: should be {STATIC_DIR}")
    public_dir_exists = os.path.exists(to_path) and os.path.isdir(to_path)
    if public_dir_exists:
        _del_recursive(to_path, del_root_dir=False)
    else:
        os.mkdir(to_path)
    _cpy_recursive(from_path, to_path)

def extract_title(md: str) -> str:
    for line in md.split('\n'):
        if line.startswith("# ") and line[2:].strip():
            return line[2:].strip()
    raise ValueError("No h1 header found in markdown text")

def generate_page(from_path: str, template_path: str, dest_path: str):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, 'r', encoding="utf-8") as f:
        md = f.read()
    with open(template_path, 'r', encoding="utf-8") as f:
        origin = f.read()
    html = markdown_to_html_node(md).to_html()
    title = extract_title(md)
    origin = origin.replace("{{ Title }}", title)
    origin = origin.replace("{{ Content }}", html)
    dest_folder = os.path.dirname(dest_path)
    os.makedirs(dest_folder, exist_ok = True)
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(origin)

def generate_pages_recursive(dir_path_content: str, template_path: str, dest_dir_path: str):
    for item in os.listdir(dir_path_content):
        new_path = os.path.join(dir_path_content, item)
        if os.path.isdir(new_path):
            new_dest_path = os.path.join(dest_dir_path, item)
            generate_pages_recursive(new_path, template_path, new_dest_path)
        elif new_path.endswith(".md"):
            root, _ = os.path.splitext(item)
            new_dest_path = os.path.join(dest_dir_path, f"{root}.html")
            generate_page(new_path, template_path, new_dest_path)

    
    
