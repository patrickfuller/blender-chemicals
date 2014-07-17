"""
Methods to interconvert between json and other (cif, mol, smi, etc.) files
"""

import os
import sys

import numpy as np
from numpy.linalg import norm
import pybel
ob = pybel.ob

import json_formatter as json

ROOT = os.path.normpath(os.path.dirname(__file__))
IS_PY3 = sys.version > "3"

with open(os.path.join(ROOT, "atoms.json")) as in_file:
    atom_map = json.load(in_file)


def convert(data, in_format, out_format, pretty=True, add_h=False):
    """Converts between two inputted chemical formats."""
    # Decide on a json formatter depending on desired prettiness
    dumps = json.dumps if pretty else json.compress

    # Not doing this can cause segfaults in the underlying openbabel C++
    if not IS_PY3:
        in_format.encode("ascii")
        out_format.encode("ascii")
        data.encode("ascii", "replace")

    # If it's a json string, load it. NOTE: This is a custom chemical format
    if in_format == "json" and isinstance(data, str if IS_PY3 else basestring):
        data = json.loads(data)

    # These use the open babel library to interconvert, with additions for json
    mol = (json_to_pybel(data) if in_format == "json" else
           pybel.readstring(in_format, data))

    # Infer structure in cases where the input format has no specification
    # or the specified structure is small
    if not mol.OBMol.HasNonZeroCoords() or len(mol.atoms) < 50:
        mol.make3D(steps=500)
    mol.OBMol.Center()

    if add_h:
        mol.addh()

    return (dumps(pybel_to_json(mol)) if out_format == "json"
            else mol.write(out_format))


def json_to_pybel(data):
    """Converts python data structure to pybel.Molecule."""
    obmol = ob.OBMol()
    obmol.BeginModify()
    for atom in data["atoms"]:
        obatom = obmol.NewAtom()
        obatom.SetAtomicNum(atom_map.index(atom["element"]) + 1)
        obatom.SetVector(*atom["location"])
    # If there is no bond data, try to infer them
    if "bonds" not in data or not data["bonds"]:
        obmol.ConnectTheDots()
        obmol.PerceiveBondOrders()
    # Otherwise, use the bonds in the data set
    else:
        for bond in data["bonds"]:
            if "atoms" not in bond:
                continue
            obmol.AddBond(bond["atoms"][0] + 1, bond["atoms"][1] + 1,
                          bond["order"])
    obmol.EndModify()
    return pybel.Molecule(obmol)


def pybel_to_json(molecule):
    """Converts a pybel molecule to json."""
    # Save atom element type and 3D location.
    atoms = [{"element": atom_map[atom.atomicnum - 1], "location": atom.coords}
             for atom in molecule.atoms]
    # Save number of bonds and indices of endpoint atoms
    bonds = [{"atoms": [b.GetBeginAtom().GetIndex(),
                        b.GetEndAtom().GetIndex()],
              "order": b.GetBondOrder()}
             for b in ob.OBMolBondIter(molecule.OBMol)]
    return {"atoms": atoms, "bonds": bonds}


if __name__ == "__main__":
    # Lazy converter to test this out
    import sys

    if "-h" in sys.argv or "--help" in sys.argv:
        print("\nUSAGE: python format_converter.py `in_data` `in_format` "
              "`out_format`\n"
              "ex. python format_converter.py data.mol mol json\n\n"
              "Interconverts between json and other chemical file formats.\n"
              "Notes: `in_data` can be a file or a string, and the script "
              "prints to stdout.\n")
        sys.exit()

    in_data, in_format, out_format = sys.argv[1:]
    try:
        with open(in_data) as in_file:
            data = in_file.read()
    except IOError:
        data = in_data
    print(convert(data, in_format, out_format))
