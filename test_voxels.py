import subprocess
import sys
import time
import numpy as np
import scipy.io
import multiprocessing

def twist(rotation):
    twist = """\
    module thingy(height, twist) {
        color("gray")
        linear_extrude(height = height, twist = twist, scale = 0, center = false, slices = 20)
            square([10, 10], center = true);
    }

    module voxel(x, y, z) {
        translate([x, y, z]) cube([%d, %d, %d]);
    }

    module check() {
        intersection() {
            thingy(20, %d);
            voxel(%d, %d, %d);
        }
    }

    check();
    probe(volume=true){
        check();
        echo("volume is ", volume);
    }
    """

    min_x, max_x = -5, 5
    min_y, max_y = -5, 5
    min_z, max_z = 0, 20

    # How many voxels we want in each dimension
    x_resolution = 10
    y_resolution = 10
    z_resolution = 20

    volume_grid = np.zeros((x_resolution, y_resolution, z_resolution))

    x_size = (max_x - min_x) // x_resolution
    y_size = (max_y - min_y) // y_resolution
    z_size = (max_z - min_z) // z_resolution
    voxel_volume = x_size * y_size * z_size

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

                thingy = twist % (x_size, y_size, z_size, rotation, x_coord, y_coord, z_coord)

                with open(scad, "w") as f:
                    f.write(thingy)

                result = subprocess.run([
                    "/home/hades/Downloads/openscad_fork/openscad",
                    "-o", stl,
                    scad],
                    stderr=subprocess.PIPE)

                lines = result.stderr.splitlines()
                for line in lines:
                    line = line.decode('utf-8')
                    if line.startswith("ECHO: \"volume is"):
                        volume = line.split(",")[-1].strip()
                        volume = 0 if volume == "true" else float(volume)
                        volume /= voxel_volume
                        volume_grid[x, y, z] = volume
                        print("[%d, %d, %d] volume is" % (x, y, z), volume)
                        break

    end = time.time()
    print("Took", end - start, "seconds to generate voxel grid")

    # https://stackoverflow.com/questions/3685265/how-to-write-a-multidimensional-array-to-a-text-file
    filename = "twist_%d.mat" % rotation
    scipy.io.savemat(filename, mdict={'volumes': volume_grid})

def main():
    start = time.time()
    p = multiprocessing.Pool()
    p.map(twist, [-360, -270, -180, -90, 0])
    end = time.time()
    print("Took", end - start, "seconds overall")

if __name__ == "__main__":
    main()
