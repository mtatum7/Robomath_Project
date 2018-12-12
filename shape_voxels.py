#!/usr/bin/env python3

import subprocess
import sys
import time
import numpy as np
import scipy.io
import multiprocessing
import os

def shape(filename):
    wrapper = """\
    module thingy() {
        %s
    }

    module voxel(x, y, z) {
        translate([x, y, z]) cube([%%.2f, %%.2f, %%.2f]);
    }

    module check() {
        intersection() {
            thingy();
            voxel(%%.2f, %%.2f, %%.2f);
        }
    }

    probe(volume=true){
        check();
        echo("volume is ", volume);
    }
    """

    with open(filename) as f:
        template = wrapper % f.read()

    min_x, max_x = -5, 5
    min_y, max_y = -5, 5
    min_z, max_z = 0, 5

    # How many voxels we want in each dimension
    x_resolution = 10
    y_resolution = 10
    z_resolution = 5

    volume_grid = np.zeros((x_resolution, y_resolution, z_resolution))

    x_size = (max_x - min_x) / x_resolution
    y_size = (max_y - min_y) / y_resolution
    z_size = (max_z - min_z) / z_resolution
    voxel_volume = x_size * y_size * z_size
    print(x_size, y_size, z_size, voxel_volume)

    print(multiprocessing.current_process())
    file_id = id(multiprocessing.current_process())
    stl = "/tmp/%d.stl" % file_id
    scad = "/tmp/%d.scad" % file_id
    print(stl, scad)

    start = time.time()
    for z in range(z_resolution):
        for y in range(y_resolution):
            for x in range(x_resolution):
                
                x_coord = min_x + x_size * x
                y_coord = min_y + y_size * y
                z_coord = min_z + z_size * z

                thingy = template % (x_size, y_size, z_size, x_coord, y_coord, z_coord)

                with open(scad, "w") as f:
                    f.write(thingy)

                s2 = time.time()
                result = subprocess.run([
                    "/home/hades/Downloads/openscad_fork/openscad",
                    "-o", stl,
                    scad],
                    stderr=subprocess.PIPE)
                print(filename, ": scad took", time.time() - s2, "seconds")

                lines = result.stderr.splitlines()
                for line in lines:
                    line = line.decode('utf-8')
                    if line.startswith("ECHO: \"volume is"):
                        volume = line.split(",")[-1].strip()
                        volume = 0 if volume == "true" else float(volume)
                        volume /= voxel_volume
                        volume_grid[x, y, z] = volume
                        print(filename, ": [%d, %d, %d](%0.2f, %0.2f, %0.2f) volume is" % 
                                (x, y, z, x_coord, y_coord, z_coord), volume)
                        break

    end = time.time()
    print(filename, ": took", end - start, "seconds to generate voxel grid")

    # https://stackoverflow.com/questions/3685265/how-to-write-a-multidimensional-array-to-a-text-file
    filename += ".mat"
    scipy.io.savemat(filename, mdict={'volumes': volume_grid})

def gen_filenames():
    dirname = "simple_shapes"
    files = os.listdir(dirname)
    files_set = set(files)
    for name in files:
        if name.endswith(".scad") and not (name+".mat") in files_set:
            yield os.path.join(dirname, name)


def main():
    start = time.time()
    p = multiprocessing.Pool(8)
    p.map(shape, gen_filenames())
    end = time.time()
    print("Took", end - start, "seconds overall")


if __name__ == "__main__":
    main()
