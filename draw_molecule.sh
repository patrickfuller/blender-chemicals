# Generate molecule json
# $1 - either a string or a file correlated to the type specified in $2
# $2 - any input format supported by openbabel
python format_converter.py $1 $2 json > molecule.json

# Run in blender
if [[ $(uname -s) == "Darwin" ]]; then
    # Mac version, assumes no blender link
    /Applications/blender.app/Contents/MacOS/./blender molecule.blend -P molecule_to_blender.py
else
    blender molecule.blend -P molecule_to_blender.py
fi
