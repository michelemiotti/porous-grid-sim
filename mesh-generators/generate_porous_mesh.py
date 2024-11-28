import bpy  # type: ignore
import sys

from math import pi


# Function to parse arguments manually.
# We're not using `argparse` because it messes with Blender's CLI arguments.
def parse_blender_args():
    args = {
        # These are the default values.
        "cavity_amount": 8,
        "cavity_diameter": 0.25,
        "cavity_distancing": 0.25,
        "slate_thickness": 0.25,
        "circle_vertices": 32,
        "export_path": "porous_mesh.stl",
    }

    # Get the arguments from the command line.
    for i in range(1, len(sys.argv)):
        if sys.argv[i] == "--cavity_amount":
            args["cavity_amount"] = int(sys.argv[i + 1])
        elif sys.argv[i] == "--cavity_diameter":
            args["cavity_diameter"] = float(sys.argv[i + 1])
        elif sys.argv[i] == "--cavity_distancing":
            args["cavity_distancing"] = float(sys.argv[i + 1])
        elif sys.argv[i] == "--slate_thickness":
            args["slate_thickness"] = float(sys.argv[i + 1])
        elif sys.argv[i] == "--circle_vertices":
            args["circle_vertices"] = int(sys.argv[i + 1])
        elif sys.argv[i] == "--export_path":
            args["export_path"] = sys.argv[i + 1]

    return args


if __name__ == "__main__":
    # Get the arguments.
    args = parse_blender_args()

    # Clear the scene.
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)

    # Compute some useful values.
    slate_width = (
        2 * args["cavity_distancing"] / 2
        + args["cavity_amount"] * args["cavity_diameter"]
        + (args["cavity_amount"] - 1) * args["cavity_distancing"]
    )

    # Add a cube that we will carve using the `boolean` modifier.
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        enter_editmode=False,
        align="WORLD",
        location=(0, 0, 0),
        scale=(slate_width, args["slate_thickness"], slate_width),
    )

    # Create a `Cylinder` object that contains an array of cylinders.
    for i in range(args["cavity_amount"]):
        for j in range(args["cavity_amount"]):
            x = (
                -slate_width / 2
                + args["cavity_distancing"] / 2
                + args["cavity_diameter"] / 2
                + i * (args["cavity_diameter"] + args["cavity_distancing"])
            )
            z = (
                -slate_width / 2
                + args["cavity_distancing"] / 2
                + args["cavity_diameter"] / 2
                + j * (args["cavity_diameter"] + args["cavity_distancing"])
            )

            # Add a cylinder which we will use to cut a hole out of the slate.
            bpy.ops.mesh.primitive_cylinder_add(
                vertices=args["circle_vertices"],
                enter_editmode=True,
                align="WORLD",
                location=(x, 0, z),
                scale=(1, 1, args["slate_thickness"] * 2),
                radius=args["cavity_diameter"] / 2,
                rotation=(pi / 2, 0, 0),
            )

    # Get a reference to the two objects.
    slate = bpy.data.objects["Cube"]
    cylinder = bpy.data.objects["Cylinder"]

    # Add and apply the boolean modifier to the `Cube` object.
    slate.modifiers.new(name="Boolean", type="BOOLEAN")
    slate.modifiers["Boolean"].solver = "FAST"
    slate.modifiers["Boolean"].object = cylinder

    bpy.context.view_layer.objects.active = slate
    bpy.ops.object.mode_set(mode="OBJECT")
    bpy.ops.object.modifier_apply(modifier="Boolean")

    # Remove the dummy `Cylinder` object.
    bpy.context.view_layer.objects.active = cylinder
    bpy.ops.object.mode_set(mode="OBJECT")
    bpy.ops.object.delete(use_global=False)

    # Export the mesh.
    bpy.ops.wm.obj_export(filepath=args["export_path"])
