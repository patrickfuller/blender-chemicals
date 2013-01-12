#!/usr/bin/env python
"""
Some small edits to json output.
 * Float decimals are truncated to three digits
 * [x, y, z] vectors are displayed on one line
"""

import json
from json import encoder
encoder.FLOAT_REPR = lambda o: format(o, '.3f')


def dumps(object):
    """Outputs json with small formatting edits."""
    # Pretty print json string with truncated floats
    json_string = json.dumps(object, indent=4, sort_keys=True)
    # Make all lists of floats one line and return
    return make_one_line_lists(json_string)


def make_one_line_lists(json_string):
    """Display float lists as one line in json. Useful for vectors."""
    json_string = json_string.split("\n")
    for i, row in enumerate(json_string):

        # Iterate through all rows that start a list
        if row[-1] != "[" or not has_next_float(json_string, i):
            continue

        # Move down rows until the list ends, deleting and appending.
        while has_next_float(json_string, i):
            row += " " + json_string[i + 1].strip()
            del json_string[i + 1]

        # Finish off with the closing bracket
        json_string[i] = row + " " + json_string[i + 1].strip()
        del json_string[i + 1]

    # Recombine the list into a string and return
    return "\n".join(json_string)


def has_next_float(json_string, i):
    """Tests if the next row in a split json string is a float."""
    try:
        float(json_string[i + 1].strip().replace(",", ""))
        return True
    except:
        return False
