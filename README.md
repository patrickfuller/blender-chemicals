Chemicals in Blender
====================

Draws chemicals in Blender using common input formats (smiles, molfiles, cif files, etc.)

This depends on openbabel / pybel for file parsing
```bash
apt-get install openbabel
pip install openbabel-python
```

Usage
-----

```bash
python molecule_to_json.py smi "CCC" > molecule.json
blender molecule.blend -P json_molecule_to_blender.py
```

Without the command line, you can copy and paste the contents of `json_molecule_to_blender.py` into Blender, update paths to `atomic_diameters.json`, `atomic_colors.json`, and `molecule.json`, and run.

The drawing function has the option to set a scale limit on molecules via `max_molecule_size`. It can also generate space-filling models by setting `show_bonds=False`

Samples
-------

####Caffeine, ball and stick

![](http://www.patrick-fuller.com/wp-content/uploads/2012/06/caffeine_occlusion.png)

####Penicillin, ball and stick, Cycles render

![](http://www.patrick-fuller.com/wp-content/uploads/2012/11/penicillin_in_marble.png)

####Rb CD-MOF, ball and stick

![](http://www.patrick-fuller.com/wp-content/uploads/2012/11/mof_ball_and_stick.png)

####Rb CD-MOF, space filling

![](http://www.patrick-fuller.com/wp-content/uploads/2012/11/mof_space_filling.png)
