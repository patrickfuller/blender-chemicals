Chemicals in Blender
====================

Draws chemicals in Blender using common input formats (smiles, molfiles, cif files,
etc.). For details, read my [blog post](http://www.patrick-fuller.com/molecules-from-smiles-molfiles-in-blender/).

Samples
-------

####Caffeine, ball and stick

![](http://www.patrick-fuller.com/img/caffeine_step_five_960.png)

####Penicillin, ball and stick, Cycles render

![](http://www.patrick-fuller.com/img/penicillin_in_marble_960.png)

####NU-100, ball and stick

![](http://www.patrick-fuller.com/img/nu_100_blender_960.png)

####NU-100, 3D printed from Blender output

![](http://www.patrick-fuller.com/img/nu_100_3d_print.png)

Usage
-----

In order to locally convert files to the required format, you will need the
[Open Babel](http://openbabel.org/wiki/Main_Page) library and Python bindings
for chemical file format parsing, which is best installed from source.
For more, read through the [Open Babel installation instructions](http://openbabel.org/docs/dev/Installation/install.html).

```
git clone https://github.com/openbabel/openbabel
mkdir build && cd build
cmake ../openbabel -DPYTHON_BINDINGS=ON
make && make install
```

From here, you can convert files to Javascript Object Notation with something like

```
python format_converter *data* *in_format* json > molecule.json
```

*format* is any format in [this list](http://openbabel.org/docs/2.3.0/FileFormats/Overview.html),
and *data* is either a string or a file containing the data specified by *format*.
From here, use `blender -P molecule_to_blender.py` to load the molecule.

The shell script is a light wrapper around these two commands. For example,

```bash
sh draw_molecule.sh "CC(C)(C)C1=CC2(C=C(C(C)(C)C)C1=O)CC2(c1ccccc1)c1ccccc1" smi
```

will convert the input data (string or file path) and load into Blender.
