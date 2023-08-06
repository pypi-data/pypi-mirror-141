import os
import re
import click

def get_abs_path(path: str) -> str:
    if os.path.isabs(path):
        return path
    else:
        return os.path.realpath(path)

def rename_in_dirs(dir_path: str):
    # rename recursively in folders
    for dir in os.listdir(dir_path):
        full_dir = os.path.join(dir_path, dir)

        if os.path.isfile(full_dir):
            file_ext = re.search('(?<=index).*[\w+]', dir)
            parent_dir = dir_path.split('\\')[-1]

            if (file_ext):
                # rename index to folder name
                new_filename = f'{parent_dir}{file_ext[0]}'
                print(f'Renaming {dir} to {new_filename}')
                os.rename(full_dir, os.path.join(dir_path, new_filename))
        else:
            rename_in_dirs(full_dir)

@click.command()
@click.option('--dir', default=os.path.join(__file__), help='Which directory to recursively rename files named index')
def main(dir):
    rename_in_dirs(dir)
    print('DONE')

if (__name__ == '__main__'):
    main()