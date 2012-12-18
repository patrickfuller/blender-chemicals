#!/usr/bin/env python
"""
Converts any chemical datatype supported by openbabel to json.

Written by Patrick Fuller, patrickfuller@gmail.com, 28 Nov 12
"""

import pybel
from openbabel import OBMolBondIter
import re
import json

def molecule_to_json(molecule):
    """ Converts an OpenBabel molecule to json for use in Blender """
    
    # Get centroid to center molecule at (0, 0, 0)
    centroid = [0, 0, 0]
    for atom in molecule.atoms:
        centroid = [c+a for c, a in zip(centroid, atom.coords)]
    centroid = [c/float(len(molecule.atoms)) for c in centroid]
    
    # Openbabel atom types have valence ints. Remove those.
    # There are other flags on common atoms (aromatic, .co, am, etc.)
    parse_type = lambda t: t[0] if len(t) > 2 else re.sub("(\d|\W)", "", t)
    
    # Save atom element type and 3D location.
    atoms = [{"element": parse_type(atom.type), 
              "location": [round(a-c, 3) for a,c in zip(atom.coords, centroid)]} 
             for atom in molecule.atoms]
    
    # Save number of bonds and indices of endpoint atoms
    # Switch from 1-index to 0-index counting
    bonds = [{"source": b.GetBeginAtom().GetIndex(), 
              "target": b.GetEndAtom().GetIndex(),
              "order": b.GetBondOrder()} for b in OBMolBondIter(molecule.OBMol)]
              
    json_string = json.dumps({"atoms": atoms, "bonds": bonds}, 
                              sort_keys=True, indent=4)
    
    # An obsessive-compulsive hack to display float lists as one line in json
    json_string = json_string.split('\n')
    for i, row in enumerate(json_string):
        # Iterate through all rows that start a list
        if row[-1] != "[" or not _has_next_float(json_string, i):
            continue
        # Move down rows until the list ends, deleting and appending.
        while _has_next_float(json_string, i):
            row += " " + json_string[i+1].strip()
            del json_string[i+1]
        # Finish off with the closing bracket
        json_string[i] = row + " ]"
        del json_string[i+1]
    # Recombine the list into a string and return
    return "\n".join(json_string)

def _has_next_float(json_string, i):
    """ Tests if the next row in a split json string is a float """
    try:
        float(json_string[i+1].strip().replace(",",""))
        return True
    except:
        return False 
    
if __name__ == "__main__":
    from sys import argv, exit
    
    # Print help if needed
    if len(argv) < 3 or "--help" in argv:
        print "USAGE: python molecule_to_json.py *type* *data* (--addh)"
        print "    type: Type of input: smi, mol, cif, etc."
        print "    data: Chemical file or string"
        print "    --addh:  add hydrogen atoms"
        exit()
    
    # "smi", "mol", "cif", etc.
    type = argv[1]
    
    # Support both files and strings.
    try:
       with open(argv[2]) as in_file:
           in_data = in_file.read()
    except:
        in_data = argv[2]
    
    # Load openbabel molecule
    molecule = pybel.readstring(type, in_data)
    molecule.addh()
    
    # User specified args to generate coordinates and keep hydrogen atoms
    if type == "smi":
        molecule.make3D(steps=500)
    if "--addh" not in argv:
        molecule.removeh()
    
    # Print result to stdout for piping and what not
    print molecule_to_json(molecule)
