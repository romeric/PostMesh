import numpy as np
from PostMeshPy import PostMeshSurfacePy as PostMeshSurface


def Sphere():

   # THIS IS AN EXAMPLE OF A SPHERE MESH WITH QUARTIC (P=4)
   # TETRAHEDRAL FINITE ELEMENTS - SAME AS THE C++ EXAMPLE

    # READ MESH DATA
    elements = np.loadtxt("sphere_elements.dat",delimiter=",").astype(np.uint64)
    points = np.loadtxt("sphere_points.dat",delimiter=",",dtype=np.float64)
    edges = np.loadtxt("sphere_edges.dat",delimiter=",").astype(np.uint64)
    faces = np.loadtxt("sphere_faces.dat",delimiter=",").astype(np.uint64)
    # SUPPLY CAD FILE
    iges_filename = "sphere.igs" 

    # DOES THE MESH/CAD FILE NEED TO BE SCALED?
    # THIS IS IMPORTANT AS MOST CAD LIBRARIES SCALE UP/DOWN 
    # IMPORTED CADD FILES
    scale = 1000.;
    # THIS CONDITION TELLS PostMesh IF ALL THE BOUNDARY POINTS 
    # IN THE MESH REQUIRE PROJECTION - ANY BOUNDARY POINT FALLING 
    # WITHIN THIS RADIUS WOULD BE PROJECTED
    radius = 1.e10;
    # PRECISION TOLERANCE BETWEEN CAD GEOMETRY AND MESH DATA.
    # NORMALLY, DUE TO MESH DATA AND CAD GEOMETRY COMING FROM DIFFERENT
    # SOURCES, THERE'S AN ARITHMATIC PRECISION ISSUE. THIS PRECISION TELLS
    # PostMesh TO TREAT POINTS FROM CAD AND MESH WITHIN THIS PRECISION AS
    # ONE POINT 
    precision = 1.0e-07;
    # NODAL SPACING OF POINTS IN THE REFRERENCE TRIANGLE (GAUSS-LOBATTO SPACING IN THS CASE)
    nodal_spacing = np.loadtxt("nodal_spacing_p4.dat",delimiter=",",dtype=np.float64)

    curvilinear_mesh = PostMeshSurface("tet",3)
    curvilinear_mesh.SetMeshElements(elements)
    curvilinear_mesh.SetMeshPoints(points)
    curvilinear_mesh.SetMeshEdges(edges)
    curvilinear_mesh.SetMeshFaces(faces)
    curvilinear_mesh.SetScale(scale)
    curvilinear_mesh.SetCondition(radius)
    curvilinear_mesh.SetProjectionPrecision(precision)
    curvilinear_mesh.ComputeProjectionCriteria()
    curvilinear_mesh.ScaleMesh()
    curvilinear_mesh.SetNodalSpacing(nodal_spacing)
    # READ THE GEOMETRY FROM THE IGES FILE
    curvilinear_mesh.ReadIGES(iges_filename)
    # EXTRACT GEOMETRY INFORMATION FROM THE IGES FILE
    geometry_points = curvilinear_mesh.GetGeomVertices()
    # curvilinear_mesh.GetGeomEdges()
    curvilinear_mesh.GetGeomFaces()
    curvilinear_mesh.GetGeomPointsOnCorrespondingFaces()
    # FIRST IDENTIFY WHICH SURFACES CONTAIN WHICH FACES
    curvilinear_mesh.IdentifySurfacesContainingFaces()
    # PROJECT ALL BOUNDARY POINTS FROM THE MESH TO THE CURVE
    curvilinear_mesh.ProjectMeshOnSurface()
    # PERFORM POINT INVERSION FOR THE INTERIOR POINTS
    # PERFORM POINT INVERSION FOR THE INTERIOR POINTS (ORTHOGONAL PROJECTION)
    # THE TWO ARGUMENTS ARE FOR ALLOWING PROJECTION ON CURVE INTERSECTION AND
    # MODIFYING THE LINEAR MESH IF IT DOES NOT MATCH WITH THE GEOMETRICAL 
    # POINTS IN THE CAD FILE (WITHIN THE SPECFIED PRECISION) 
    curvilinear_mesh.MeshPointInversionSurface(project_on_curves=0,modify_linear_mesh=1)
    # OBTAIN MODIFIED MESH POINTS - THIS IS NECESSARY TO ENSURE LINEAR MESH IS ALSO CORRECT
    curvilinear_mesh.ReturnModifiedMeshPoints(points)
    # GET DIRICHLET DATA - (THE DISPLACMENT OF BOUNDARY NODES)
    # nodesDBC IS AN ARRAY OF SIZE [NO OF BOUNDARY NODES] CONTAINING 
    # GLOBAL NODE NUMBERS IN THE ELEMENT CONNECTIVITY AND Dirichlet IS 
    # THE CORRESPONDING DISPLACEMENT ARRAY [NO OF BOUNDARY NODES x DIMENSION]
    nodesDBC, Dirichlet = curvilinear_mesh.GetDirichletData() 

    print(Dirichlet)


if __name__ == "__main__":
    Sphere()