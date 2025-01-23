# Porous Grid Sim

This is an OpenFOAM solver for simulating flow through porous media. This is
part of a project for the **(059439) HIGH PERFORMANCE SIMULATION LAB FOR
MECHANICAL ENGINEERING** course.

## Installation

You will need to have a working `blender` executable in your machine. You can download it
[here](https://www.blender.org/download/).


## Mesh Generation

Mesh generation is done using `blender`. Two types of meshes can be
generated: porous and wire meshes. Further details on how to generate each type
of mesh are provided below. The generated mesh has to be saved as
`simulation/constant/triSurface/grid.obj` for the simulation to use it.
You can either follow the instructions in this section and generate the mesh yourself
(not recommended) or use the script provided in `system/change_domany.py`, editing
it based on what mesh you want to generate. Information on the effect of each parameter
is explained here.

### Porous Mesh Generation

The porous mesh generation script generates a slate with a grid of cavities. All
cavities are of the same diameter and are equally spaced. The slate has a
constant thickness, and the amount of cavities is equal in both directions.
The script takes the following parameters:

- `export_path`: The path to the exported `.obj` file.
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
```

```bash
$BLENDER_PATH --background --python mesh-generators/generate_porous_mesh.py -- \
    --export_path $PROJECT_DIR/exported-meshes/porous_mesh.obj \
    --cavity_amount 6        \
    --cavity_diameter 0.2    \
    --cavity_distancing 0.05 \
    --slate_thickness 0.25
```

> [!NOTE]
> The extra `--` after the script name is necessary to pass the arguments to
> the script. The `--background` flag is used to run Blender in the background,
> without opening the GUI. This is useful for running the script in a headless
> environment.

### Wire Mesh Generation

The wire mesh generation script generates a wire mesh assembled as a grid of
square cells. The wires travel above and below each other, at each intersection.
The script takes the following parameters:

- `export_path`: The path to the exported `.obj` file.
- `square_size`: The size of the square cells. This does not take into account
  the thickness of the wires.
- `square_amount`: The number of squares in the grid. Note that, by looking at
  a single exported mesh, it may appear that there is one less square in each
  direction. This is because the script generates a tileable mesh, and the
  periodicity is expressed by a cut between the last and first squares.
- `curve_smoothing_offset`: The `offset` used to smooth the curves. This can be
  used to avoid sharp edges in the mesh. For more information on what exactly
  `offset` means, refer to the [this documentation](https://docs.blender.org/manual/en/latest/modeling/modifiers/generate/bevel.html#options).
- `overlap offset`: The offset used to overlap the wires. This is how much the
  wires keep a distance from the XZ plane at the maximum overlap position.
  Please note that this measurement is only accurate assuming no curve smoothing
  is applied. If curve smoothing is applied, the overlap will be relatively
  smaller than the specified value.
- `bevel_resolution`: This is the amount of segments used to approximate the
  curviness around the intersection points. Increasing this will make the curve
  smoother along the YZ plane. See `curve_smoothing_offset` for more
  information.
- `wire_section_radius`: The radius of the wires.
- `curve_bevel_resolution`: Given a section of a curve (a circle), this is the
  number of segments used to approximate one quarter of it. Increasing this
  value will make the curve smoother along the XZ plane.

> [!NOTE]
> The `square_amount` parameter is supposed to be an even number. Inserting an
> odd number would produce a geometrically untilable mesh.

Here's an example of how to generate a wire mesh.

```bash
export BLENDER_PATH=/path/to/blender/executable
export PROJECT_DIR=/path/to/porous_grid_sim
```

```bash
$BLENDER_PATH --background --python mesh-generators/generate_wire_mesh.py -- \
    --export_path $PROJECT_DIR/exported-meshes/wire_mesh.obj \
    --square_size 0.25     \
    --square_amount 6      \
    --overlap_offset 0.1   \
    --bevel_resolution 10  \
    --wire_section_radius 0.05
```


### Execution

To run the simulation locally:

> Load the OpenFOAM environment.
> Move to the `simulation` folder.
> If you haven't done this yet, generate the mesh, possibly running `python3 change_domain.py`
> Run `chmod +x Allrun`.
> Run `./Allrun`.

To copy this repository and start the simulation on the cluster automatically, after generating the mesh:

> Load the OpenFOAM environment.
> Make sure you are in the root directory of the repository (`porous-grid-sim`).
> Run `chmod +x scripts/run_on_cluster.sh`
> Run `./scripts/run_on_cluster.sh <username> <password>`, where <username> and <password> are your username and password for the cluster respectively.

Note: this only enqueues the simulation, it does not wait until it is fully done.