
*************
I/O Functions
*************

OpenMesh provides functions that read and write meshes from and to files:
:func:`~openmesh.read_trimesh`, :func:`~openmesh.read_polymesh` and :func:`~openmesh.write_mesh`

.. code:: python

    import openmesh as om

    trimesh = om.read_trimesh("bunny.ply")
    polymesh = om.read_polymesh("bunny.ply")
    # modify mesh ...
    om.write_mesh(trimesh, "bunny.ply")

OpenMesh currently supports five file types: .obj, .off, .ply, .stl and .om

For writing .obj files there is also support for textures. You can pass the path of a texture image and
optionally the suffix for the material file, default is ".mat", but some programs, e.g. Blender expect ".mtl" as suffix

.. code:: python

    om.write_mesh(
        "out.obj",
        trimesh,
        texture_file="moon.png",
        material_file_extension=".mtl"  # default is ".mat", blender needs ".mtl"
    )
