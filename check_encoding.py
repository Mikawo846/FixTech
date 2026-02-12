#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import chardet
import glob

def detect_encoding(filepath):
    try:
        with open(filepath, 'rb') as f:
            raw_data = f.read()
            result = chardet.detect(raw_data)
            return result['encoding'], result['confidence']
    except Exception as e:
        return None, 0

def scan_files():
    extensions = ['*.html', '*.css', '*.js', '*.py', '*.md', '*.txt']
    non_utf8_files = []

    for ext in extensions:
        for filepath in glob.glob(ext, recursive=True):
            if os.path.isfile(filepath):
                encoding, confidence = detect_encoding(filepath)
                if encoding and encoding.lower() not in ['utf-8', 'utf8']:
                    if confidence > 0.7:  # Only consider high confidence detections
                        non_utf8_files.append((filepath, encoding, confidence))

    return non_utf8_files

if __name__ == "__main__":
    non_utf8 = scan_files()
    if non_utf8:
        print("Files not in UTF-8:")
        for filepath, encoding, confidence in non_utf8:
            print(f"{filepath}: {encoding} (confidence: {confidence:.2f})")
    else:
        print("All scanned files are in UTF-8 or detection failed.")
