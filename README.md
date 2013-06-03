Chemicals in Blender
====================

Draws chemicals in Blender using common input formats (smiles, molfiles, cif files, etc.). For details, read my [blog post](http://www.patrick-fuller.com/molecules-from-smiles-molfiles-in-blender/).

Usage
-----

###Without dependencies

Use [this online tool](http://www.patrick-fuller.com/imolecule.html) to convert a chemical file
from any input format to Javascript Object Notation (drag input file into window,
then click "save as"). Rename it to `molecule.json`, and place it in the same
directory as these scripts. Then, load the file into Blender with

```
blender -P molecule_to_blender.py
```

Without the command line, you can copy and paste the contents of `molecule_to_blender.py` into Blender, update paths to `atomic_diameters.json`, `atomic_colors.json`, and `molecule.json`, and run.

The drawing function has the option to set a scale limit on molecules via
`max_molecule_size`. It can also generate space-filling models by setting
`show_bonds=False`.

It's a short script - don't be afraid to open it up and hack it to suit your needs.

###With dependencies

In order to locally convert files to the required format, you will need the
[Open Babel](http://openbabel.org/wiki/Main_Page) library and Python bindings
for chemical file format parsing, which can be installed via apt-get/macports
(the pip repository doesn't work).

```bash
apt-get/port install openbabel-python
```

In the case of OSX + homebrew, the default installer doesn't include python
bindings. Instead, use

```bash
brew install https://raw.github.com/rwest/homebrew/open-babel-new/Library/Formula/eigen2.rb
brew install https://raw.github.com/rwest/homebrew/open-babel-new/Library/Formula/open-babel.rb
```

If you have problems, refer to the Open Babel website.

From here, you can convert files to Javascript Object Notation with something like

```
python format_converter *data* *in_format* json > molecule.json
```

*format* is any format in [this list](http://openbabel.org/docs/2.3.0/FileFormats/Overview.html), and *data* is either a string or a file containing the data specified by *format*. From here, use `blender -P molecule_to_blender.py` to load
the molecule.

The shell script is a light wrapper around these two commands. For example,

```bash
sh draw_molecule.sh "CC(C)(C)C1=CC2(C=C(C(C)(C)C)C1=O)CC2(c1ccccc1)c1ccccc1" smi
sh draw_molecule.sh my_mol_file.mol mol
```

will convert the input data and load into Blender.

Samples
-------

####Caffeine, ball and stick

![](http://www.patrick-fuller.com/wp-content/uploads/2012/06/caffeine_occlusion.png)

####Penicillin, ball and stick, Cycles render

![](http://www.patrick-fuller.com/wp-content/uploads/2012/11/penicillin_in_marble.png)

####NU-100, ball and stick

![](http://www.patrick-fuller.com/wp-content/uploads/2013/02/nu_100_blender.png)

####Rb CD-MOF, space filling

![](http://www.patrick-fuller.com/wp-content/uploads/2012/11/mof_space_filling.png)
