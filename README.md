# Porous Grid Sim

This is an OpenFOAM solver for simulating flow through porous media. This is
part of a project for the **(059439) HIGH PERFORMANCE SIMULATION LAB FOR
MECHANICAL ENGINEERING** course.

## Installation

At this point, we haven't automated the installation process. You will need to
have a working `blender` executable in your machine. You can download it
[here](https://www.blender.org/download/).


## Mesh Generation

Mesh generation is done using `blender`. So far, two types of meshes can be
generated: porous and wire meshes. Further details on how to generate each type
of mesh are provided below.

### Porous Mesh Generation

The porous mesh generation script generates a slate with a grid of cavities. All
cavities are of the same diameter and are equally spaced. The slate has a
constant thickness, and the amount of cavities is equal in both directions.
The script takes the following parameters:

- `export_path`: The path to the exported `.stl` file.
- `cavity_amount`: The number of cavities in the grid.
- `cavity_diameter`: The diameter of the cavities.
- `cavity_distancing`: The distance between the cavities.
- `slate_thickness`: The thickness of the slate.
- `circle_vertices`: The number of vertices in the circle that represents the
  cavity.

Here's an example of how to generate a porous mesh.

```bash
export BLENDER_PATH=/path/to/blender/executable
export PROJECT_DIR=/path/to/porous_grid_sim

$BLENDER_PATH --background --python mesh-generators/generate_porous_mesh.py -- \
    --export_path $PROJECT_DIR/exported-meshes/porous_mesh.stl \
    --cavity_amount 4       \
    --cavity_diameter 0.75  \
    --cavity_distancing 0.2 \
    --slate_thickness 0.25
```

> [!NOTE]
> The extra `--` after the script name is necessary to pass the arguments to
> the script. The `--background` flag is used to run Blender in the background,
> without opening the GUI. This is useful for running the script in a headless
> environment.

### Wire Mesh Generation

> [!WARNING]
> The wire mesh generation script is not yet implemented.