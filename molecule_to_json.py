#!/usr/bin/env python
"""
Converts any chemical datatype supported by openbabel to json.

Written by Patrick Fuller, patrickfuller@gmail.com, 28 Nov 12
"""

import pybel
from openbabel import OBMolBondIter
import re
import json_formatter


def molecule_to_json(molecule):
    """ Converts an OpenBabel molecule to json for use in Blender """

    # Get centroid to center molecule at (0, 0, 0)
    centroid = [0, 0, 0]
    for atom in molecule.atoms:
        centroid = [c + a for c, a in zip(centroid, atom.coords)]
    centroid = [c / float(len(molecule.atoms)) for c in centroid]

    # Openbabel atom types have valence ints. Remove those.
    # There are other flags on common atoms (aromatic, .co, am, etc.)
    parse_type = lambda t: t[0] if len(t) > 2 else re.sub("(\d|\W)", "", t)

    # Save atom element type and 3D location.
    atoms = [{"element": parse_type(atom.type),
              "location": [a - c for a, c in zip(atom.coords, centroid)]}
             for atom in molecule.atoms]

    # Save number of bonds and indices of endpoint atoms
    # Switch from 1-index to 0-index counting
    bonds = [{"source": b.GetBeginAtom().GetIndex(),
              "target": b.GetEndAtom().GetIndex(),
              "order": b.GetBondOrder()}
             for b in OBMolBondIter(molecule.OBMol)]

    return {"atoms": atoms, "bonds": bonds}


if __name__ == "__main__":
    from sys import argv, exit

    # Print help if needed
    if len(argv) < 3 or "--help" in argv:
        print ("USAGE: python molecule_to_json.py *type* *data* (--addh)\n"
               "    type: Type of input: smi, mol, cif, etc.\n"
               "    data: Chemical file or string\n"
               "    --addh:  add hydrogen atoms")
        exit()

    # "smi", "mol", "cif", etc.
    molecule_type = argv[1]

    # Support both files and strings.
    try:
        with open(argv[2]) as in_file:
            in_data = in_file.read()
    except:
        in_data = argv[2]

    # Load openbabel molecule
    molecule = pybel.readstring(molecule_type, in_data)
    molecule.addh()

    # User specified args to generate coordinates and keep hydrogen atoms
    if molecule_type == "smi":
        molecule.make3D(steps=500)
    if "--addh" not in argv:
        molecule.removeh()

    # Print result to stdout for piping and what not
    print json_formatter.dumps(molecule_to_json(molecule))
