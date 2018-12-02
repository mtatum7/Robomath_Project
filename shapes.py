# NOTE: sudo ln -s /Applications/OpenSCAD.app/Contents/MacOS/OpenSCAD /usr/local/bin/openscad
# ! /usr/bin/python
# -*- coding: UTF-8 -*-
from __future__ import division
import os, sys, re

from solid import *
from solid.utils import *

SEGMENTS = 48


def makeRectBeam(length, width, height):
    shape = cube(size=[length, width, height], center=False)
    return shape

def makeNothingBox(length, width, height):
    shape = cube(size=[0, 0, 0], center=False)
    return shape

def makeCubeBeam(width, length, thickness):
    shape = cube(size=[width, width, length], center=False)
    return shape


def makeCylindBeam(radius, length):
    shape = cylinder(r=radius, h=length, center=False)
    return shape

def makeNothingCylind(radius, length):
    shape = cylinder(r=0, h=0, center=False)
    return shape

def makeCylinderBeam(diameter, length, thickness):
    shape = cylinder(r=(diameter / 2.0), h=length, center=False)
    return shape


def makeHollowRectBeam(length, width, height):
    shapeTotal = cube(size=[length, width, height], center=False)

    # Holes will be punched in from the top
    # For best printing
    # Also because CSAIL printers are deepest in z dir
    thickness = 1
    shapeInner = cube([length - 2 * thickness, width - 2 * thickness, height], center=False)
    return shapeTotal - shapeInner


def makeHollowCubeBeam(width, length, thickness):
    shapeTotal = cube(size=[width, width, length], center=False)

    # Holes will be punched in from the top
    # For best printing
    # Also because CSAIL printers are deepest in z dir
    shapeInner = cube([width - 2 * thickness, width - 2 * thickness, length], center=False)
    return shapeTotal - shapeInner


def makeHollowCylindBeam(width, length):
    radius = width / 2
    shapeTotal = cylinder(r=radius, r2=radius, h=length, center=False)
    # Holes will be punched in from the top
    # For best printing
    # Also because CSAIL printers are deepest in z dir
    thickness = 0.1
    newRadius = radius - thickness
    shapeInner = cylinder(r=newRadius, h=length, center=False)

    return shapeTotal - shapeInner


def makeEye(radius, length):
    shapeTotal = translate([0, 0, 1])( cylinder(r=radius, r2=0, h=length+2, center=False))

    # Holes will be punched in from the top
    # For best printing
    # Also because CSAIL printers are deepest in z dirthickness
    thickness = 0.1
    newRadius = radius - 2 * thickness
    shapeInner = translate([0, 0, 1])(cylinder(r2=newRadius, r=0, h=length+4, center=False))

    return shapeTotal - shapeInner


def makeHollowCone(radius, length):
    shapeTotal = cylinder(r=radius, r2=0, h=length, center=False)

    # Holes will be punched in from the top
    # For best printing
    # Also because CSAIL printers are deepest in z dir
    thickness = 0.1
    newRadius = radius - 2 * thickness
    # length = length + 1
    shapeInner = cylinder(r=newRadius, r2=0, h=length, center=False)

    return shapeTotal - shapeInner


def makeTriangleBeam(beamWidth, length, dummy):
    # Beam shaped like a solid triangle
    shape = getEquilateral(beamWidth)
    shape = linear_extrude(height=length, center=False, convexity=10, twist=0, slices=1)(shape)

    return shape


def makeH(width, thickness):
    # Creates a 2d H shape
    shape = square(size=[thickness, width], center=True)
    cross = rotate(a=[0, 0, 90])(shape)
    shift = width / 2.0 - thickness / 2.0
    # return cross
    return shape + translate([0, shift, 0])(cross) + translate([0, -shift, 0])(cross)


def makeI(width, thickness):
    # Creates a 2D I shape
    cross = square(size=[thickness, width], center=True)
    shape = rotate(a=[0, 0, 90])(cross)
    shift = width / 2.0 - thickness / 2.0
    return shape + translate([shift, 0, 0])(cross) + translate([-shift, 0, 0])(cross)


def makeHBeam(width, length, thickness=1):
    # Extrudes the H into a beam
    shape = makeH(width, thickness)
    shape = linear_extrude(height=length, center=True, convexity=10, twist=0, slices=1)(shape)
    return shape


def makeIBeam(width, length, thickness=1):
    # Extrudes an I into a beam
    shape = makeI(width, thickness)
    shape = linear_extrude(height=length, center=True, convexity=10, twist=0, slices=1)(shape)
    return shape


def makeDiamondBeam(width, length, thickness=1):
    shape = makeCubeBeam(width, length)
    return rotate([0, 0, 45])(shape)


def makeDiamondBeam(width, length, thickness=1):
    shape = makeHollowCubeBeam(width, length, thickness)
    return rotate([0, 0, 45])(shape)


def getEquilateral(edgeLength):
    degrees = math.radians(60)
    a = [1 * edgeLength, 0]
    b = [-cos(degrees) * edgeLength, sin(degrees) * edgeLength]
    c = [-cos(degrees) * edgeLength, -1 * sin(degrees) * edgeLength]

    myPoints = [a, b, c]
    shape = translate([2,3,0])(polygon(points=myPoints))

    return shape


def makeHollowTriangleBeam(width, length, thickness):
    shape = getEquilateral(width)
    shape = linear_extrude(height=length, center=True, convexity=10, twist=0, slices=1)(shape)

    shape2 = getEquilateral(width - 2 * thickness)
    shape2 = linear_extrude(height=length, center=True, convexity=10, twist=0, slices=1)(shape2)

    return shape - shape2


def makeSquareTruss(width, length, thickness):
    side01 = makeTrussPanel(width, length, thickness)
    side02 = rotate([0, 0, 90])(side01)

    side1 = translate([0, width / 2.0, 0])(side01)
    side2 = translate([width / 2.0, 0, 0])(side02)

    side1 = translate([0, -thickness, 0])(side1)
    side2 = translate([-thickness, 0, 0])(side2)

    total = side1 + side2

    side1 = rotate([0, 0, 180])(side01)
    side2 = rotate([0, 0, 180])(side02)

    side1 = translate([0, -width / 2.0, 0])(side1)
    side2 = translate([-width / 2.0, 0, 0])(side2)

    side1 = translate([0, thickness, 0])(side1)
    side2 = translate([thickness, 0, 0])(side2)

    total = total + side1 + side2

    return total


def makeTriangleTruss(width, length, thickness):
    side1 = makeTrussPanel(width, length, thickness)
    side1 = rotate([0, 0, 90])(side1)

    side2 = rotate([0, 0, 60])(side1)
    side3 = rotate([0, 0, -60])(side1)

    side1 = translate([-(width / 2), 0, 0])(side1)
    side2 = translate([0, width / (sqrt(3) * 2), 0])(side2)
    side3 = translate([0, -width / (sqrt(3) * 2), 0])(side3)

    side1 = translate([2 * thickness, 0, 0])(side1)
    side2 = translate([0, -1.5 * thickness, 0])(side2)
    side3 = translate([0, 1.5 * thickness, 0])(side3)

    total = side1 + side2 + side3
    return total


def makeTrussPanel(width, length, thickness):
    shape = makeCylindBeam(thickness, length)
    shape = translate([width / 2.0 - thickness, 0, 0])(shape) + translate([-1 * width / 2.0 + thickness, 0, 0])(shape)
    crossbeam = makeCylindBeam(thickness, width)
    crossbeam = rotate([0, 90, 0])(crossbeam)
    shape = shape + translate([0, 0, -1 * length / 2.0 + thickness / 2.0])(crossbeam) + translate(
        [0, 0, length / 2.0 - thickness / 2.0])(crossbeam)

    crossbeam = makeCylindBeam(thickness, 2 * width / sqrt(3))
    crossleft = rotate([0, 60, 0])(crossbeam)
    crossright = rotate([0, -60, 0])(crossbeam)

    slats = (length / 2.0) / (width / sqrt(3))
    slats = int(slats / 2)
    slats = slats

    slatdist = 2 * width / sqrt(3)

    for i in range(-slats, slats + 1):
        dist = -.5 * width / sqrt(3) + i * slatdist
        if (abs(dist) < abs(length / 2.0 - slatdist / 2)):
            shape = shape + translate([0, 0, -dist])(crossleft)
            shape = shape + translate([0, 0, dist])(crossright)
            furthestslat = dist

    return shape


def export(shape, filename):
    with open(filename + '.scad', 'w+') as f:
        f.write(scad_render(shape, file_header='$fn = %s;' % SEGMENTS))

    f.closed
    print("Success")

# s1 = makeTriangleTruss(70, 380, 3)
# s1 = s1 + makeTriangleBeam(50, 380, 2)
# export(s1, "thisThing")
