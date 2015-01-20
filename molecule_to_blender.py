#!/usr/bin/env python
"""
Loads a json molecule and draws atoms in Blender.

Blender scripts are weird. Either run this inside of Blender or in a shell with
    blender foo.blend -P molecule_to_blender.py

The script expects an input file named "molecule.json" and should be in the
same directory as "atoms.json"

Written by Patrick Fuller, patrickfuller@gmail.com, 28 Nov 12
"""

import bpy
from math import acos
from mathutils import Vector
import json
import os

# Get path of this file (useful when this script is imported)
PATH = os.path.dirname(os.path.realpath(__file__))

# Atomic radii from wikipedia, scaled to Blender radii (C = 0.4 units)
# http://en.wikipedia.org/wiki/Atomic_radii_of_the_elements_(data_page)
# Atomic colors from cpk
# http://jmol.sourceforge.net/jscolors/
with open(os.path.join(PATH, "atoms.json")) as in_file:
    atom_data = json.load(in_file)


def draw_molecule(molecule, center=(0, 0, 0), max_molecule_size=5,
                  show_bonds=True):
    """Draw a molecule to blender. Uses loaded json molecule data."""

    # Get scale factor - only scales large molecules down
    max_coord = 1E-6
    for atom in molecule["atoms"]:
        max_coord = max(max_coord, *[abs(a) for a in atom["location"]])
    scale = min(max_molecule_size / max_coord, 1)

    # Scale location coordinates and add specified center
    for atom in molecule["atoms"]:
        atom["location"] = [c + x * scale for c, x in zip(center,
                                                          atom["location"])]

    # Keep references to all atoms and bonds
    shapes = []

    # If using space-filling model, scale up atom size and remove bonds
    if not show_bonds:
        scale *= 2.5
        molecule["bonds"] = []

    # Add atom primitive
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.mesh.primitive_uv_sphere_add()
    sphere = bpy.context.object

    # Add bond material and primitive if it's going to be used
    if molecule["bonds"]:
        key = "bond"
        bpy.data.materials.new(name=key)
        bpy.data.materials[key].diffuse_color = atom_data[key]["color"]
        bpy.data.materials[key].specular_intensity = 0.2
        bpy.ops.mesh.primitive_cylinder_add()
        cylinder = bpy.context.object
        cylinder.active_material = bpy.data.materials["bond"]

    # Draw atoms
    for atom in molecule["atoms"]:

        # If element is not in dictionary, use undefined values
        if atom["element"] not in atom_data:
            atom["element"] = "undefined"

        # If material for atom type has not yet been defined, do so
        if atom["element"] not in bpy.data.materials:
            key = atom["element"]
            bpy.data.materials.new(name=key)
            bpy.data.materials[key].diffuse_color = atom_data[key]["color"]
            bpy.data.materials[key].specular_intensity = 0.2

        # Copy mesh primitive and edit to make atom
        atom_sphere = sphere.copy()
        atom_sphere.data = sphere.data.copy()
        atom_sphere.location = atom["location"]
        atom_sphere.dimensions = [atom_data[atom["element"]]["radius"] *
                                  scale * 2] * 3
        atom_sphere.active_material = bpy.data.materials[atom["element"]]
        bpy.context.scene.objects.link(atom_sphere)
        shapes.append(atom_sphere)

    # Draw bonds
    for bond in molecule["bonds"]:

        # Extracting locations
        first_loc = molecule["atoms"][bond["atoms"][0]]["location"]
        second_loc = molecule["atoms"][bond["atoms"][1]]["location"]
        diff = [c2 - c1 for c2, c1 in zip(first_loc, second_loc)]
        cent = [(c2 + c1) / 2 for c2, c1 in zip(first_loc, second_loc)]
        mag = sum([(c2 - c1) ** 2
                   for c1, c2 in zip(first_loc, second_loc)]) ** 0.5

        # Euler rotation calculation
        v_axis = Vector(diff).normalized()
        v_obj = Vector((0, 0, 1))
        v_rot = v_obj.cross(v_axis)

        # This check prevents gimbal lock (ie. weird behavior when v_axis is
        # close to (0, 0, 1))
        if v_rot.length > 0.01:
            v_rot = v_rot.normalized()
            axis_angle = [acos(v_obj.dot(v_axis))] + list(v_rot)
        else:
            v_rot = Vector((1, 0, 0))
            axis_angle = [0] * 4

        # Check that the number of bonds is logical
        if bond["order"] not in range(1, 4):
            print("Improper number of bonds! Defaulting to 1.")
            bond["order"] = 1

        # Specify locations of each bond in every scenario
        if bond["order"] == 1:
            trans = [[0] * 3]
        elif bond["order"] == 2:
            trans = [[1.4 * atom_data["bond"]["radius"] * x for x in v_rot],
                     [-1.4 * atom_data["bond"]["radius"] * x for x in v_rot]]
        elif bond["order"] == 3:
            trans = [[0] * 3,
                     [2.2 * atom_data["bond"]["radius"] * x for x in v_rot],
                     [-2.2 * atom_data["bond"]["radius"] * x for x in v_rot]]
        # Draw bonds
        for i in range(bond["order"]):
            bond_cylinder = cylinder.copy()
            bond_cylinder.data = cylinder.data.copy()
            bond_cylinder.dimensions = [atom_data["bond"]["radius"] * scale *
                                        2] * 2 + [mag]
            bond_cylinder.location = [c + scale * v for c,
                                      v in zip(cent, trans[i])]
            bond_cylinder.rotation_mode = "AXIS_ANGLE"
            bond_cylinder.rotation_axis_angle = axis_angle
            bpy.context.scene.objects.link(bond_cylinder)
            shapes.append(bond_cylinder)

    # Remove primitive meshes
    bpy.ops.object.select_all(action='DESELECT')
    sphere.select = True
    if molecule["bonds"]:
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
