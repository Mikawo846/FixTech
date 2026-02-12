#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import glob

def has_meta_charset(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            return '<meta charset="utf-8">' in content.lower()
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return False

def find_html_without_meta():
    html_files = glob.glob('**/*.html', recursive=True)
    missing_meta = []
    for filepath in html_files:
        if not has_meta_charset(filepath):
            missing_meta.append(filepath)
    return missing_meta

if __name__ == "__main__":
    missing = find_html_without_meta()
    if missing:
        print("HTML files missing <meta charset=\"utf-8\">:")
        for f in missing:
            print(f)
    else:
        print("All HTML files have <meta charset=\"utf-8\">")
