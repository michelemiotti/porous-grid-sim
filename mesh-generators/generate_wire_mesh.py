import bpy  # type: ignore
import bmesh  # type: ignore
import sys

from math import pi


# Function to parse arguments manually.
# We're not using `argparse` because it messes with Blender's CLI arguments.
def parse_blender_args():
    args = {
        # These are the default values.
        "square_size": 1.2,
        "square_amount": 4,
        "curve_smoothing_offset": 0.1,
        "overlap_offset": 0.1,
        "bevel_resolution": 16,
        "wire_section_radius": 0.09,
        "curve_bevel_resolution": 4,
        "export_path": "wire_mesh.stl",
    }

    # Get the arguments from the command line.
    for i in range(1, len(sys.argv)):
        if sys.argv[i] == "--square_size":
            args["square_size"] = float(sys.argv[i + 1])
        elif sys.argv[i] == "--square_amount":
            args["square_amount"] = int(sys.argv[i + 1])
        elif sys.argv[i] == "--curve_smoothing_offset":
            args["curve_smoothing_offset"] = float(sys.argv[i + 1])
        elif sys.argv[i] == "--overlap_offset":
            args["overlap_offset"] = float(sys.argv[i + 1])
        elif sys.argv[i] == "--bevel_resolution":
            args["bevel_resolution"] = int(sys.argv[i + 1])
        elif sys.argv[i] == "--wire_section_radius":
            args["wire_section_radius"] = float(sys.argv[i + 1])
        elif sys.argv[i] == "--curve_bevel_resolution":
            args["curve_bevel_resolution"] = int(sys.argv[i + 1])
        elif sys.argv[i] == "--export_path":
            args["export_path"] = sys.argv[i + 1]

    return args


if __name__ == "__main__":
    # Get the arguments.
    args = parse_blender_args()

    # Clear the scene.
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)

    # This function takes a list of tuples representing vertices
    # in 2D and returns an object that is a concatenation of those
    # vertices.
    def concatenate_vertices(vertices, name="Curve"):
        # Create a new mesh and object
        mesh = bpy.data.meshes.new(name)
        obj = bpy.data.objects.new(name, mesh)
        bpy.context.collection.objects.link(obj)

        # Set the object as the active object and enter edit mode.
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.mode_set(mode="EDIT")

        # Initialize a BMesh to define vertices and edges.
        bm = bmesh.new()

        # Transform the vertices tuples into blender vertices objects.
        vertices = [bm.verts.new((x, y, 0)) for x, y in vertices]

        # Connect them using edges.
        for i in range(len(vertices) - 1):
            bm.edges.new((vertices[i], vertices[i + 1]))

        # Write the BMesh data to the mesh and update.
        bpy.ops.object.mode_set(mode="OBJECT")
        bm.to_mesh(mesh)
        bm.free()

        # Return to object mode
        bpy.ops.object.mode_set(mode="OBJECT")

        return obj

    # The output mesh won't be tileable (periodic boundaries) if
    # the square amount is an odd number.
    if args["square_amount"] % 2 == 1:
        print("Warning: square_amount is odd, the mesh won't be tileable.")

    # Generate vertices for the base curve for a single strand.
    # Add two extra segments, to later cut them off. This will
    # make the mesh easier to tile at a later stage.
    curve_vertices = []
    for i in range(2 * args["square_amount"] + 1 + 2):
        overlap = [
            +args["overlap_offset"],
            0,
            -args["overlap_offset"],
            0,
        ][i % 4]

        curve_vertices.append(((i - 1) * args["square_size"] / 2, overlap))

    # Concatenate them into a single shape.
    curve = concatenate_vertices(curve_vertices, name="Curve")

    # Add a bevel modifier.
    curve.modifiers.new(name="Bevel", type="BEVEL")
    curve.modifiers["Bevel"].affect = "VERTICES"
    curve.modifiers["Bevel"].segments = args["bevel_resolution"]
    curve.modifiers["Bevel"].width = args["curve_smoothing_offset"]

    # Turn the shape into a curve, so that we can add a curve bevel.
    # The curve bevel will give it a three-dimensional volume.
    bpy.data.objects["Curve"].select_set(True)
    bpy.ops.object.convert(target="CURVE")

    # Add the curve bevel.
    curve.data.bevel_resolution = args["curve_bevel_resolution"]
    curve.data.bevel_depth = args["wire_section_radius"]

    # We can now convert the curve back to a mesh.
    bpy.data.objects["Curve"].select_set(True)
    bpy.ops.object.convert(target="MESH")

    # Cut off the two extra extensions, previously added for tileability.
    # To do this we create a cuboid of the required size, and use a
    # boolean intersection modifier.
    cube_scale = (
        args["square_size"] * args["square_amount"],
        4 * (args["wire_section_radius"] + args["overlap_offset"]),
        4 * args["wire_section_radius"],
    )

    # Generate the cube mesh primitive.
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        enter_editmode=False,
        align="WORLD",
        location=((args["square_size"] * args["square_amount"]) / 2, 0, 0),
        scale=cube_scale,
    )

    # Get a reference to it.
    cube = bpy.data.objects["Cube"]

    # Add and apply the boolean modifier to the `Curve` object.
    curve.modifiers.new(name="Boolean", type="BOOLEAN")
    curve.modifiers["Boolean"].solver = "EXACT"
    curve.modifiers["Boolean"].operation = "INTERSECT"
    curve.modifiers["Boolean"].object = cube

    bpy.context.view_layer.objects.active = curve
    bpy.ops.object.mode_set(mode="OBJECT")
    bpy.ops.object.modifier_apply(modifier="Boolean")

    # Remove the dummy `Cube` object.
    bpy.context.view_layer.objects.active = cube
    bpy.ops.object.mode_set(mode="OBJECT")
    bpy.ops.object.delete(use_global=False)

    # Keep duplicating the curve until we create a row-mesh.
    bpy.data.objects["Curve"].select_set(True)
    for i in range(args["square_amount"] - 1):
        bpy.ops.object.duplicate_move(
            OBJECT_OT_duplicate={"linked": False, "mode": "TRANSLATION"},
            TRANSFORM_OT_translate={
                "value": (0, 0, args["square_size"]),
                "orient_type": "GLOBAL",
                "orient_matrix": ((1, 0, 0), (0, 1, 0), (0, 0, 1)),
                "orient_matrix_type": "GLOBAL",
                "constraint_axis": (False, False, True),
                "mirror": False,
            },
        )

        # At each iteration, flip the overlap's direction.
        bpy.ops.transform.resize(value=(1, -1, 1))

    # Join all objects into a single mesh.
    bpy.ops.object.select_all(action="SELECT")
    bpy.context.view_layer.objects.active = curve
    bpy.ops.object.join()

    # Duplicate the mesh, rotate it and form the final mesh.
    bpy.ops.object.duplicate_move()
    bpy.ops.transform.rotate(value=pi / 2, orient_axis="Y")
    bpy.ops.transform.translate(
        value=(args["square_size"] * args["square_amount"], 0, 0)
    )
    bpy.ops.transform.translate(
        value=(-args["square_size"] / 2, 0, -args["square_size"] / 2)
    )

    # Translate everything so that the mesh lies at the world's origin.
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.transform.translate(
        value=(
            -args["square_amount"] * args["square_size"] / 2,
            0,
            0,
        )
    )
    bpy.ops.transform.translate(
        value=(
            0,
            0,
            -(args["square_amount"] - 1) * args["square_size"] / 2,
        )
    )

    # Export the mesh.
    bpy.ops.wm.obj_export(filepath=args["export_path"])
