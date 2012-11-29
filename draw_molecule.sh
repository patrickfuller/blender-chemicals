# Generate molecule json
python molecule_to_json.py smi "CC(C)(C)C1=CC2(C=C(C(C)(C)C)C1=O)CC2(c1ccccc1)c1ccccc1" > molecule.json

# Can also do cif files or mol files
# python molecule_to_json cif my_file.cif > molecule.json
# python molecule_to_json mol my_file.mol > molecule.json

# Run in blender
blender molecule.blend -P json_molecule_to_blender.py

# Mac version, if no blender link
#/Applications/blender.app/Contents/MacOS/./blender molecule.blend -P molfile_to_blender.py