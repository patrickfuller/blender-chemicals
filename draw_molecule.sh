# Generate molecule json
# $1 - any format supported my openbabel. Tested on "smi", "mol", and "cif"
# $2 - either a string or a file correlated to the type specified in $1
python molecule_to_json.py $1 $2 > molecule.json

# Run in blender
if [[ $(uname -s) == "Darwin" ]]; then
    # Mac version, assumes no blender link
    /Applications/blender.app/Contents/MacOS/./blender molecule.blend -P json_molecule_to_blender.py
else
    blender molecule.blend -P json_molecule_to_blender.py
fi
