#! /usr/bin/env python3

from pathlib import Path
import argparse
import logging
import os
import sys


def main():
    # Piping in PowerShell sets an encoding that can't handle some of Window's
    # own filenames.
    sys.stdout.reconfigure(errors='replace')

    parser = argparse.ArgumentParser(
        description='Compare "old" and "new" directories. Delete files from '
                    '"old" which are identical in "new".')

    parser.add_argument('-d',
        help='Delete files',
        action='store_true')
    parser.add_argument('old', type=Path)
    parser.add_argument('new', type=Path)

    args = parser.parse_args()

    log_format = logging.Formatter(
        '%(asctime)s %(name)s: %(levelname).4s  %(message)s',
        datefmt='%b %d %H:%M:%S')

    log_console = logging.StreamHandler()
    log_console.setFormatter(log_format)

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(log_console)

    logger.info(f"Comparing '{args.old}' and '{args.new}'.")

    if not args.d:
        logger.info('Will not delete any files without the -d flag.')

    recurse(args.old, args.new, deleting=args.d)


def recurse(old_path, new_path, indent=0, deleting=False):
    d_indent = '  ' * indent
    f_indent = '  ' * (indent + 1)

    old_files = list(os.scandir(old_path))
    old_files_f = sorted([i for i in old_files if i.is_file()], key=lambda d: d.name)
    old_files_d = sorted([i for i in old_files if i.is_dir()], key=lambda d: d.name)

    print(f"{d_indent}{old_path}: {len(old_files_f)} files:")
    for old_f in old_files_f:
        old_f_path = Path(old_f)
        old_f_rel = old_f_path.relative_to(old_path)

        new_f_path = new_path / old_f_rel

        if not new_f_path.is_file():
            print(f"{f_indent}Missing: {old_f_rel}")

        elif not old_f.stat().st_size == new_f_path.stat().st_size:
            print(f"{f_indent}Changed: {old_f_rel}")

        elif not bytewise_match(old_f_path, new_f_path):
            print(f"{f_indent}Changed: {old_f_rel}")

        else:
            print(f"{f_indent}Matched: {old_f_rel}")

            if deleting:
                print(f"{f_indent}DELETING: {old_f_rel}")
                try:
                    old_f_path.unlink()
                except PermissionError:
                    print(f"{f_indent}Failed to delete: {old_f_rel}")

    for old_d in old_files_d:
        old_d_path = Path(old_d)
        old_d_rel = old_d_path.relative_to(old_path)

        #print(f"{indent}{old_d_path}, {new_path / old_d_rel}")
        recurse(old_d_path, new_path / old_d_rel, indent=indent+1, deleting=deleting)

    if len(list(os.listdir(old_path))) == 0:
        print(f"{d_indent}Empty: {old_path}")

        if deleting:
            print(f"{d_indent}REMOVING: {old_path}")
            try:
                old_path.rmdir()
            except PermissionError:
                print(f"{d_indent}Failed to remove: {old_path}")


def bytewise_match(a, b, chunk=4096):
    a_f = open(a, 'rb')
    b_f = open(b, 'rb')

    while True:
        a_chunk = a_f.read(chunk)
        b_chunk = b_f.read(chunk)

        if a_chunk != b_chunk:
            return False

        if (len(a_chunk) < chunk):
            break

    return True


if __name__ == '__main__':
    main()
