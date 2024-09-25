"""
modified from trimesh.remesh, only subdivide the longest edge
"""
import numpy as np
import trimesh

def subdivide2(vertices,
              faces,
              face_index=None):
    """
    Subdivide a mesh into smaller triangles.

    Note that if `face_index` is passed, only those
    faces will be subdivided and their neighbors won't
    be modified making the mesh no longer "watertight."

    Parameters
    ------------
    vertices : (n, 3) float
      Vertices in space
    faces : (m, 3) int
      Indexes of vertices which make up triangular faces
    face_index : faces to subdivide.
      if None: all faces of mesh will be subdivided
      if (n,) int array of indices: only specified faces

    Returns
    ----------
    new_vertices : (q, 3) float
      Vertices in space
    new_faces : (p, 3) int
      Remeshed faces
    """
    if face_index is None:
        face_index = np.arange(len(faces))
    else:
        face_index = np.asanyarray(face_index)

    # the (c, 3) int array of vertex indices
    faces_subset = faces[face_index]  # (F,3)

    # find max edge of each face
    face_edges = faces_subset[:, [0, 1, 1, 2, 2, 0]].reshape((-1, 3, 2))  # (F,3,2)
    face_edges_length = ((np.diff(vertices[face_edges], axis=2) ** 2).sum(axis=3) ** 0.5).reshape((-1, 3))  # (F,3)
    face_edges_argmax = np.argmax(face_edges_length, axis=1)  # (F,)
    face_max_edge = face_edges[np.arange(len(face_edges_argmax)), face_edges_argmax]  # (F,2)

    # subdivide max_edge
    mid = vertices[face_max_edge].mean(axis=1)
    mid_idx = np.arange(len(mid)) + len(vertices)

    # find another vertex of triangle out of max edge
    vertex_in_edge = np.full_like(faces_subset, fill_value=False)
    for i in range(faces_subset.shape[1]):
        for j in range(face_max_edge.shape[1]):
            vertex_in_edge[:, i] = np.logical_or(vertex_in_edge[:, i], faces_subset[:, i] == face_max_edge[:, j])
    another_vertices = faces_subset[np.logical_not(vertex_in_edge)]

    # the new faces_subset with correct winding
    f = np.column_stack([another_vertices,
                         face_max_edge[:, 0],
                         mid_idx,

                         mid_idx,
                         face_max_edge[:, 1],
                         another_vertices,
                         ]).reshape((-1, 3))
    # add new faces_subset per old face
    new_faces = np.vstack((faces, f[len(face_index):]))
    # replace the old face with a smaller face
    new_faces[face_index] = f[:len(face_index)]

    new_vertices = np.vstack((vertices, mid))

    return new_vertices, new_faces

def decimate(mesh: trimesh.Trimesh, target: int) -> trimesh.Trimesh:
    while len(mesh.vertices) > target:
        mesh = mesh.simplify_quadric_decimation(percent=0.1, aggression=0)
    return mesh

def subdivide(shape: trimesh.Trimesh, target: int) -> trimesh.Trimesh:
    while len(shape.vertices) < target:
        (new_verts, new_faces) = subdivide2(shape.vertices, shape.faces)
        shape.vertices = new_verts
        shape.faces = new_faces
    return shape

def distribute_faces(mesh: trimesh.Trimesh, passes: int, lower_target: int, upper_target: int) -> trimesh.Trimesh:
    for _ in range(passes):
        mesh = subdivide(mesh, lower_target * 4)
        mesh = decimate(mesh, upper_target)
    return mesh

def refine_mesh(file_path: str, passes: int, lower_target: int, upper_target: int) -> None:
    mesh = trimesh.load(file_path)

    vertex_count = len(mesh.vertices)
    if vertex_count < lower_target:
        refined_mesh = subdivide(mesh, lower_target)
    elif vertex_count > upper_target:
        refined_mesh = decimate(mesh, upper_target)
    else:
        refined_mesh = mesh
    refined_mesh = distribute_faces(refined_mesh, passes, lower_target, upper_target)
    refined_mesh.export(file_path)
    print(f"Refined mesh saved to {file_path}")