import fire
import subprocess
import logging
from git import Repo


def add(url, name):
    command = [
        "git",
        "submodule",
        "add",
        url,
        name,
    ]
    try:
        result = subprocess.check_output(command)
        print("success")
    except subprocess.CalledProcessError as e:
        logging.error("Failed to add submodule!")


def delete(name):
    # get root_dir
    root_dir = get_git_root()

    # get path from git root
    path_from_root = get_path_from_git_root()

    # deinit submodule
    command = [
        "git",
        "submodule",
        "deinit",
        "-f",
        name,
    ]
    try:
        subprocess.check_output(command)
    except subprocess.CalledProcessError as e:
        logging.error("Delete Error!")

    # remove submodule file
    command = [
        "git",
        "rm",
        "-f",
        name,
    ]
    try:
        result = subprocess.check_output(command)
    except subprocess.CalledProcessError as e:
        logging.error("Delete Error!", exc_info=True)

    # remove submodule file
    command = [
        "rm",
        "-rf",
        f"{root_dir}/.git/modules/{path_from_root}/{name}",
    ]
    try:
        result = subprocess.check_output(command)
    except subprocess.CalledProcessError as e:
        logging.error("Delete Error!", exc_info=True)
    print("success")


def process(
    mode:str,
    *args,
):
    """sbmodder
    
    Add: sbmodder add https://url/to/repo mod_name
    Delete: sbmodder delete mod_name
    
    Args:
        mode (str): add, delete or move
    """
    # validation

    if mode == "add":
        print("add submodule")
        url = args[0]
        name = args[1]

        print(f"url: {url}")
        print(f"name: {name}")
        add(url, name)

    if mode == "delete":
        print("delete submodule")
        name = args[0]
        delete(name)


def get_git_root():
    command = [
        "git",
        "rev-parse",
        "--show-toplevel"
    ]
    try:
        result = subprocess.check_output(command)
    except subprocess.CalledProcessError as e:
        logging.error("Failed to get root dir", exc_info=True)
        return None
    root_dir = result.decode().replace("\n", "")
    return root_dir


def get_path_from_git_root():
    command = [
        "git",
        "rev-parse",
        "--show-prefix"
    ]
    try:
        result = subprocess.check_output(command)
    except subprocess.CalledProcessError as e:
        logging.error("Delete Error!", exc_info=True)
        return None
    path_from_root = result.decode().replace("\n", "")
    return path_from_root

        

def main():
    fire.Fire(process)

if __name__ == "__main__":
    main()
