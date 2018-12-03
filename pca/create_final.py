#! /usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
import os
from solid import *
from solid.utils import *

from shapes import *
import sys

# Assumes SolidPython is in site-packages or elsewhwere in sys.path
from solid import *
from solid.utils import *

def voxels():
    # shape = cube([1, 1, 1], center=False);
    shape = []
    for x in range(-5, 4, 1):
        for y in range(-5, 4, 1):
            for z in range(0, 10, 1):
                translate([x, y, z])
                new_cube = color([0,0,1, 0.5])(cube([1, 1, 1], center=False));
                # shape = (shape+new_cube)
                shape.append(new_cube)
    return shape

def basic_geometry():
    box_functions = [makeRectBeam, makeCubeBeam, makeTriangleBeam,makeNothingBox, makeCylindBeam, makeHollowCylindBeam, makeHollowCone, makeEye]
    # cylind_functions = [makeCylindBeam, makeHollowCylindBeam, makeHollowCone, makeEye, makeNothingCylind]
    shape_list = []
    for bf in box_functions:
        for cf in box_functions:
            for bf2 in box_functions:
                for i in range(2):
                    shape = union()(
                        # translate([-2, -3, 0])(
                        bf(5, 4, 5),
                        translate([0, 0, 5])(
                        cf(4, 3, 5)),
                        translate([0, 0, 10])(
                        bf2(5, 4, 5))
                    )
                    if i == 0:
                        shapeInner = cylinder(r=0.5, h=20, center=False)
                        shape = shape - shapeInner
                    shape_list.append(shape)

    return shape_list

def export(shape, filename):
    with open(filename + '.scad', 'w+') as f:
        f.write(scad_render(shape, file_header='$fn = %s;' % SEGMENTS))

    f.closed
    print("Success")

if __name__ == '__main__':
    out_dir = sys.argv[1] if len(sys.argv) > 1 else os.curdir
    file_out = os.path.join(out_dir, 'basic_geometry.scad')

    shape_list = basic_geometry()
    for i, shape in enumerate(shape_list):
        export(shape, "output" + str(i))
    print("Created OpenSCAD file...")
    print("Compiling STL file...")