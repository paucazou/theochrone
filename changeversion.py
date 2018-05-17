#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende
"""Change version of the soft in different places"""
TODO change versions of download packages directly

import argparse
import collections
import re

FileData = collections.namedtuple('FileData',('path','line','line_clue'))

def change_version(new_version: str,path: str,line: str,line_clue: str) -> None:
    """Put new version into line where line_clue is
    in the file path"""
    with open(path) as f:
        file = f.read().split('\n')
    new_file = []
    for line_ in file:
        if line_clue in line_:
            line_ = line.format(new_version)
        new_file.append(line_)
    with open(path,'w') as f:
        f.write('\n'.join(new_file))
    return None

def main(new_version: str) -> None:
    if not re.match("^\d+\.\d+\.\d+$",new_version):
        raise ValueError("The new version doesn't seem to follow the correct syntax for a new version.\nPlease enter a version like X.X.X where X is a number")

    for file_item in files_data:
        change_version(new_version,file_item.path,file_item.line,file_item.line_clue)

    print('Please do not forget to apply following commands: `./manage.py makemigrations && ./manage.py migrate`')
    
    return None

files_data = (
    FileData('programme/command_line.py',4*' '+"""system.add_argument('--version', action='version',version='%(prog)s {}')""","""'--version', action='version',version='"""),
    FileData('README.md','Latest version is {}','Latest version is'),
    FileData('README.md','## New features available in {}','## New features available in'),
    FileData('programme/web/help/models.py','VERSION = "{}"','VERSION = '),
    FileData('programme/web/kalendarium/views.py',4*' '+'VERSION = "{}"','VERSION = '),
    )

parser = argparse.ArgumentParser(description="Change version of the soft in different places")
parser.add_argument("version",help="Change version number.")

if __name__ == '__main__':
    args=parser.parse_args()
    main(args.version)
    

    
