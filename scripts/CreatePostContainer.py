#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import os, sys
import shutil
import argparse

def main():
    try:
        parser = argparse.ArgumentParser(epilog='v{}')
        parser.add_argument('-dir', required=True, help='help text for default')
        args = parser.parse_args()

    except Exception as e:
        print(e)

    out_dir = f"./{args.dir}"
    print(f"Creating Directory {out_dir}!")
    if os.path.isdir(out_dir):
        shutil.rmtree(out_dir)
    os.makedirs(out_dir)
    os.chdir(out_dir)   

    title = {args.dir}
    side_bar_name = (args.dir).replace("-", " ")
    side_bar_url = (args.dir).lower()
    f= open("./_index.md","w+")
    f.write (f"---\ntitle: {args.dir} \nmenu:\n  sidebar:\n    name: {side_bar_name}\n    identifier: {side_bar_url}\n    weight: 300\n---")
    f.close()

if __name__ == '__main__':
    main()