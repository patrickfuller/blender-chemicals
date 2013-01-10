#!/usr/bin/env python
"""
Loads a json molecule and draws atoms in Blender.

Blender scripts are weird. Either run this inside of Blender or in a shell with
    blender foo.blend -P molecule_to_blender.py

The script expects an input file named "molecule.json" and should be in the
same directory as "atom_diameters.json" and "atom_colors.json"

Written by Patrick Fuller, patrickfuller@gmail.com, 28 Nov 12
"""

import bpy
from math import acos
from mathutils import Vector
import json

# Atomic radii from wikipedia, scaled to Blender diameters (C = 0.8 units)
# http://en.wikipedia.org/wiki/Atomic_radii_of_the_elements_(data_page)
with open("atom_diameters.json") as atom_diameters:
    diameters = json.load(atom_diameters)

# Atomic colors from cpk
# http://jmol.sourceforge.net/jscolors/
with open("atom_colors.json") as atom_colors:
    colors = json.load(atom_colors)

# Atoms that exist in both dictionaries. Only use these.
available_atoms = set(diameters.keys()) & set(colors.keys())

# Add atom materials to blender
for key in available_atoms:
    bpy.data.materials.new(name=key)
    bpy.data.materials[key].diffuse_color = colors[key]
    bpy.data.materials[key].specular_intensity = 0.2


def draw_molecule(molecule, center=(0, 0, 0), max_molecule_size=5,
                  show_bonds=True):
    """ Draw a molecule to blender. Uses loaded json molecule data. """

    # Get scale factor - only scales large molecules down
    max_coord = 1E-6
    for atom in molecule["atoms"]:
        max_coord = max(max_coord, *[abs(a) for a in atom["location"]])
    scale = min(max_molecule_size / max_coord, 1)

    # Scale location coordinates and add specified center
    for atom in molecule["atoms"]:
        atom["location"] = [c + x * scale for c, x in zip(center,
                                                          atom["location"])]

    # Add some mesh primitives
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.mesh.primitive_uv_sphere_add()
    sphere = bpy.context.object
    bpy.ops.mesh.primitive_cylinder_add()
    cylinder = bpy.context.object
    cylinder.active_material = bpy.data.materials["bond"]

    # Keep references to all atoms and bonds
    shapes = []

    # If using space_filling model, scale up atom size and remove bonds
    if not show_bonds:
        scale *= 2.5
        molecule["bonds"] = []

    # Draw atoms
    for atom in molecule["atoms"]:

        # If element is not in dictionary, use undefined values
        if atom["element"] not in available_atoms:
            atom["element"] = "undefined"

        # Copy mesh primitive and edit to make atom
        atom_sphere = sphere.copy()
        atom_sphere.data = sphere.data.copy()
        atom_sphere.location = atom["location"]
        atom_sphere.dimensions = [diameters[atom["element"]] * scale] * 3
        atom_sphere.active_material = bpy.data.materials[atom["element"]]
        bpy.context.scene.objects.link(atom_sphere)
        shapes.append(atom_sphere)

    # Draw bonds
    for bond in molecule["bonds"]:

        # Extracting locations
        first_loc = molecule["atoms"][bond["source"]]["location"]
        second_loc = molecule["atoms"][bond["target"]]["location"]
        diff = [c2 - c1 for c2, c1 in zip(first_loc, second_loc)]
        cent = [(c2 + c1) / 2 for c2, c1 in zip(first_loc, second_loc)]
        mag = sum(
            [(c2 - c1) ** 2 for c1, c2 in zip(first_loc, second_loc)]) ** 0.5

        # Euler rotation calculation
        v_axis = Vector(diff).normalized()
        v_obj = Vector((0, 0, 1))
        v_rot = v_obj.cross(v_axis)
        angle = acos(v_obj.dot(v_axis))

        # Check that the number of bonds is logical
        if bond["order"] not in range(1, 4):
            print("Improper number of bonds! Defaulting to 1.")
            bond["order"] = 1

        # Specify locations of each bond in every scenario
        if bond["order"] == 1:
            trans = [[0] * 3]
        elif bond["order"] == 2:
            trans = [[0.7 * diameters["bond"] * x for x in v_obj],
                    [-0.7 * diameters["bond"] * x for x in v_obj]]
        elif bond["order"] == 3:
            trans = [[0] * 3, [1.1 * diameters["bond"] * x for x in v_obj],
                    [-1.1 * diameters["bond"] * x for x in v_obj]]
        # Draw bonds
        for i in range(bond["order"]):
            bond_cylinder = cylinder.copy()
            bond_cylinder.data = cylinder.data.copy()
            bond_cylinder.dimensions = [diameters["bond"] * scale] * 2 + [mag]
            bond_cylinder.location = [c + scale * v for c,
                                      v in zip(cent, trans[i])]
            bond_cylinder.rotation_mode = "AXIS_ANGLE"
            bond_cylinder.rotation_axis_angle = [angle] + list(v_rot)
            bpy.context.scene.objects.link(bond_cylinder)
            shapes.append(bond_cylinder)

    # Remove primitive meshes
    bpy.ops.object.select_all(action='DESELECT')
    sphere.select = True
    cylinder.select = True
    # If the starting cube is there, remove it
    if "Cube" in bpy.data.objects.keys():
        bpy.data.objects.get("Cube").select = True
    bpy.ops.object.delete()

    # Smooth and join molecule shapes
    for shape in shapes:
        shape.select = True
    bpy.context.scene.objects.active = shapes[0]
    bpy.ops.object.shade_smooth()
    bpy.ops.object.join()

    # Center object origin to geometry
    bpy.ops.object.origin_set(type="ORIGIN_GEOMETRY", center="MEDIAN")

    # Refresh scene
    bpy.context.scene.update()

# Runs the method
if __name__ == "__main__":
    with open("molecule.json") as molecule_file:
        molecule = json.load(molecule_file)
    draw_molecule(molecule, show_bonds=True)
