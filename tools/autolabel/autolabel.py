# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import os
import string

def lines_from_file(path):
    """
    Return every line from a file as list.
    """
    with open(path) as file:
        for line in file:
            yield line.strip('\n')
    
def between(string, start, end):
    """
    Return what's between start and end in a string.
    Not inclusive.
    """
    i = string.index(start)
    j = string[i:].index(end)
    
    return string[i+1: i+j]

def existing_labels(path):
    """
    Get all existing labels from a document.
    """
    labels = set()
    for line in lines_from_file(path):
        if 'label' not in line:
            continue
        label = between(line, '{', '}')
        label_type, label_value = label.split(':')
        labels.add((label_type.strip(), label_value.strip()))
        
    return labels

def sanitize(some_string):
    """
    Make it label-able.
    """
    some_string = some_string.replace(' ', '_')
    some_string = some_string.lower()
    return ''.join([c for c in some_string if c in string.ascii_letters + '_'])
  
def create_label_string(label_type, label_name):
    return r'\label{' + label_type + ':' + label_name + '}'
    

def label(path):
    """
    Creates labels,
    returns a list of string, one per line.
    """
    
    BEGIN_LABELS = {'definition':'def',
                'theorem': 'thm'}

    labels = existing_labels(path)
    lines = list(lines_from_file(path))


    i = 0
    while i < len(lines):
        
        if any((l in lines[i]) and ('begin' in lines[i]) for l in BEGIN_LABELS.keys()):
            if 'label' in lines[i+1]:
                i += 1
                continue
            try:
                label_type = BEGIN_LABELS[between(lines[i], '{', '}')]
                label_name = sanitize(between(lines[i], '[', ']'))
            except ValueError:
                # Could not find format \begin{}[], skip
                i += 1
                continue
            
            # This label exists in the document
            # Do not add it, continue instead
            if (label_type, label_name) in labels:
                i += 1
                continue
            
            label_str = create_label_string(label_type, label_name)
            
            print('Inserting:', label_str)
            
            lines.insert(i+1, label_str)
            labels.add((label_type, label_name))

        i += 1
    
    return lines
    
    
BEGIN_LABELS = {'definition':'def',
                'theorem': 'thm'}

path = 'test_doc_before.tex'
lines = label(path)
with open('test_doc_after.tex', 'w') as file:
    data = '\n'.join(lines)
    file.write(data)
