Chemicals in Blender
====================

Draws chemicals in Blender ≥2.8 using common input formats (smiles, molfiles, cif files,
etc.). For details, read my [blog post](https://patrickfuller.github.io/molecules-from-smiles-molfiles-in-blender/).

Samples
-------

### Caffeine, ball and stick

![](http://patrickfuller.github.io/img/caffeine_step_five_960.png)

### Penicillin, ball and stick, Cycles render

![](http://patrickfuller.github.io/img/penicillin_in_marble_960.png)

### NU-100, ball and stick

![](http://patrickfuller.github.io/img/nu_100_blender_960.png)

### NU-100, 3D printed from Blender output

![](http://patrickfuller.github.io/img/nu_100_3d_print.png)

Installation
------------

### With Conda

```
conda install -c openbabel openbabel
pip install blender-chemicals
```

This library uses [Open Babel](http://openbabel.org/wiki/Main_Page) to read
multiple chemical file formats. The easiest way to install is through [conda](https://conda.io/docs/).
If you're a scientist that doesn't currently use conda, I recommend
taking the time to learn it before continuing.

### Without Conda

If you prefer to build from source, read through the [Open Babel installation instructions](http://openbabel.org/docs/dev/Installation/install.html).
The commands usually boil down to something like:

```
git clone https://github.com/openbabel/openbabel --depth 1 && cd openbabel
mkdir build && cd build
cmake ../openbabel -DPYTHON_BINDINGS=ON
make && make install
```

Then, install this library with `pip install blender-chemicals`. Alternately,
you can `git clone` and run with `python -m blender_chemicals.run c1ccccc1`.

Usage
-----

### Command Line

This library installs a command-line tool that handles common use cases. To test, run:

```
blender-chemicals c1ccccc1
```

If this works, the command will load benzene into a Blender window.
You can replace `c1ccccc1` with another string or file path, and the program will
do its best to determine input format.

Beyond this, there are a number of configuration options. Type
`blender-chemicals --help` to learn more.

### In Blender

The command line simplifies the majority of usage, but it can't do everything. If you
want to customize, you'll likely want to import or edit the scripts directly.
I'd recommend copy-pasting the drawing code into Blender. For details, read my
[blog post](https://patrickfuller.github.io/molecules-from-smiles-molfiles-in-blender/).

With the current library organization, you would copy the contents of `draw.py`
into a Blender window. You can then hardcode the path of `atoms.json` (top of file)
and your JSON-formatted molecule (bottom of file).

### Generating JSON

If you're going the custom route, you'll still need to generate the proper JSON
format. To generate from the command line, run:

```
blender-chemicals c1ccccc1 --convert-only > molecule.json
```

If you're looking to draw hundred of chemicals, you can access the python function
directly.

```python
import pybel
from blender_chemicals.parse import process

output = []
for molecule in my_molecules:
    mol = pybel.readstring('format', molecule)
    output.append(process(mol))
```

From here, hardcode the paths in your blender script and adjust as needed.
