#!/usr/bin/env python
"""
Some small edits to json output.
 * Float decimals are truncated to three digits
 * [x, y, z] vectors are displayed on one line
 * Converts numpy arrays to lists and defined objects to dictionaries
 * Atoms and bonds are on one line each (looks more like other chem formats)
"""

from itertools import takewhile
import re
import json
from json import encoder
encoder.FLOAT_REPR = lambda o: format(o, '.6f')

import numpy as np

load = json.load
loads = json.loads


def compress(obj):
    """Outputs json without whitespace."""
    return json.dumps(obj, sort_keys=True, separators=(",", ":"),
                      cls=CustomEncoder)


def dumps(obj):
    """Outputs json with formatting edits + object handling."""
    return json.dumps(obj, indent=4, sort_keys=True, cls=CustomEncoder)


class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        """Fired when an unserializable object is hit."""
        if hasattr(obj, '__dict__'):
            return obj.__dict__.copy()
        elif isinstance(obj, np.ndarray):
            return obj.copy().tolist()
        else:
            raise TypeError(("Object of type %s with value of %s is not JSON "
                            "serializable") % (type(obj), repr(obj)))

    def encode(self, obj):
        """Fired for every object."""
        s = super(CustomEncoder, self).encode(obj)
        # If uncompressed, postprocess for formatting
        if len(s.splitlines()) > 1:
            s = self.postprocess(s)
        return s

    def postprocess(self, json_string):
        """Displays each atom and bond entry on its own line."""
        is_compressing = False
        compressed = []
        spaces = 0
        for row in json_string.split("\n"):
            if is_compressing:
                if row.strip() == "{":
                    compressed.append(row.rstrip())
                elif (len(row) > spaces and row[:spaces] == " " * spaces and
                        row[spaces:].rstrip() in ["]", "],"]):
                    compressed.append(row.rstrip())
                    is_compressing = False
                else:
                    compressed[-1] += " " + row.strip()
            else:
                compressed.append(row.rstrip())
                if any(a in row for a in ["atoms", "bonds"]):
                    # Fix to handle issues that arise with empty lists
                    if "[]" in row:
                        continue
                    spaces = sum(1 for _ in takewhile(str.isspace, row))
                    is_compressing = True
        return "\n".join(compressed)
