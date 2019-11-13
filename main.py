from pathlib import Path
import glob
import re
import os
import argparse
import filecmp
import shutil
import sys


parser = argparse.ArgumentParser(description='Copy latest files from windows history')

parser.add_argument('source',
                    help='path of source [e.g. F:\\FileHistory\\Username\\Computername\\Data\\C\\Users\\Username]')

parser.add_argument('destination',
                    help='path of destination [e.g. C:\\Users\\Username]')

parser.add_argument('-r', '--recursive', action='store_true',
                    help='recursive search')

parser.add_argument('-s', '--skip', action='store_true',
                    help='skip identical files')

parser.add_argument('-v', '--verbose', action='store_true',
                    help='print progress')

parser.add_argument('-e', '--exclude', nargs='+',
                    help='name of folder or dir to exclude')

args = parser.parse_args()


def search(current_path):
    current_path = os.path.abspath(current_path)
    source = os.path.abspath(args.source)
    destination = os.path.abspath(args.destination)
    
    try:
        for file_name in os.listdir(current_path):

            file_path = os.path.join(current_path, file_name)
            current_file = Path(file_path)

            if file_name in args.exclude:
                if args.verbose:
                    print(f"exclude {current_file}")
                continue

            new_path = re.sub(r' \(\d{4}_\d{2}_\d{2} \d{2}_\d{2}_\d{2} UTC\)', '', file_path)

            destination_path = new_path.replace(source, destination)
            new_file = Path(destination_path)  

            if new_file.exists():
                new_file.chmod(0o777)

            if current_file.is_dir():   
                if not new_file.exists():
                    if args.verbose:
                        print(f"make dir {new_file}")
                    new_file.mkdir()
                if args.recursive:
                    search(current_file)
                shutil.copystat(current_file, new_file)
            else: 
                copy(new_file, current_file)

    except Exception:
        tb = sys.exc_info()[2]
        print(tb) 


def copy(new_file, current_file):
    
    try:
        if not new_file.exists() or new_file.stat().st_mtime < current_file.stat().st_mtime:
            if new_file.exists() and args.skip and filecmp.cmp(current_file, new_file):
                if args.verbose:
                    print(f"skip {current_file}")
                return
            shutil.copyfile(current_file, new_file)
            shutil.copystat(current_file, new_file)
            if args.verbose:
                print(f"{'replace' if new_file.exists() else 'create'} {new_file}")
        #print(f"skip {new_file} because newer version exists")

    except Exception:
        tb = sys.exc_info()[2]
        print(tb) 


search(args.source)
