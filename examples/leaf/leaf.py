import numpy as np
from PostMeshPy import PostMeshCurvePy as PostMeshCurve


def Leaf():

    # THIS IS AN EXAMPLE OF A 2D LEAF SHAPED GEOMETRY MESHED WITH P=8
    # TRIANGULAR FINITE ELEMENTS - SAME AS THE C++ EXAMPLE

    # READ MESH DATA
    elements = np.loadtxt("leaf_elements.dat",delimiter=",").astype(np.uint64)
    points = np.loadtxt("leaf_points.dat",delimiter=",",dtype=np.float64)
    edges = np.loadtxt("leaf_edges.dat",delimiter=",").astype(np.uint64)
    # SUPPLY CAD FILE
    iges_filename = "leaf.iges" 

    # DOES THE MESH/CAD FILE NEED TO BE SCALED?
    # THIS IS IMPORTANT AS MOST CAD LIBRARIES SCALE UP/DOWN 
    # IMPORTED CADD FILES
    scale = 1000.;
    # THIS CONDITION TELLS PostMesh IF ALL THE BOUNDARY POINTS 
    # IN THE MESH REQUIRE PROJECTION - ANY BOUNDARY POINT FALLING 
    # WITHIN THIS RADIUS WOULD BE PROJECTED
    condition = 1.e10;
    # PRECISION TOLERANCE BETWEEN CAD GEOMETRY AND MESH DATA.
    # NORMALLY, DUE TO MESH DATA AND CAD GEOMETRY COMING FROM DIFFERENT
    # SOURCES, THERE'S AN ARITHMATIC PRECISION ISSUE. THIS PRECISION TELLS
    # PostMesh TO TREAT POINTS FROM CAD AND MESH WITHIN THIS PRECISION AS
    # ONE POINT 
    precision = 1.0e-07;
    # NODAL SPACING OF POINTS IN THE REFRERENCE TRIANGLE (GAUSS-LOBATTO SPACING IN THS CASE)
    nodal_spacing = np.array([-1.,-0.899758,-0.67718628,
        -0.36311746,0.,0.36311746,0.67718628,0.899758,1.])


    curvilinear_mesh = PostMeshCurve("tri",2)
    curvilinear_mesh.SetMeshElements(elements)
    curvilinear_mesh.SetMeshPoints(points)
    curvilinear_mesh.SetMeshEdges(edges)
    curvilinear_mesh.SetMeshFaces(np.zeros((1,4),dtype=np.uint64))
    curvilinear_mesh.SetScale(scale)
    curvilinear_mesh.SetCondition(condition)
    curvilinear_mesh.SetProjectionPrecision(precision)
    curvilinear_mesh.ComputeProjectionCriteria()
    curvilinear_mesh.ScaleMesh()
    curvilinear_mesh.SetNodalSpacing(nodal_spacing.reshape(-1,1))
    curvilinear_mesh.GetBoundaryPointsOrder()
    # READ THE GEOMETRY FROM THE IGES FILE
    curvilinear_mesh.ReadIGES(iges_filename)
    # EXTRACT GEOMETRY INFORMATION FROM THE IGES FILE
    geometry_points = curvilinear_mesh.GetGeomVertices()
    curvilinear_mesh.GetGeomEdges()
    curvilinear_mesh.GetGeomFaces()
    curvilinear_mesh.GetGeomPointsOnCorrespondingEdges()
    # FIRST IDENTIFY WHICH CURVES CONTAIN WHICH EDGES
    curvilinear_mesh.IdentifyCurvesContainingEdges()
    # PROJECT ALL BOUNDARY POINTS FROM THE MESH TO THE CURVE
    curvilinear_mesh.ProjectMeshOnCurve()
    # FIX IMAGES AND ANTI IMAGES IN PERIODIC CURVES/SURFACES
    curvilinear_mesh.RepairDualProjectedParameters()
    # PERFORM POINT INVERSION FOR THE INTERIOR POINTS
    curvilinear_mesh.MeshPointInversionCurveArcLength()
    # OBTAIN MODIFIED MESH POINTS - THIS IS NECESSARY TO ENSURE LINEAR MESH IS ALSO CORRECT
    curvilinear_mesh.ReturnModifiedMeshPoints(points)
    # GET DIRICHLET DATA - (THE DISPLACMENT OF BOUNDARY NODES)
    # Dirichlet_nodes IS AN ARRAY OF SIZE [NO OF BOUNDARY NODES] CONTAINING 
    # GLOBAL NODE NUMBERS IN THE ELEMENT CONNECTIVITY AND Dirichlet_values IS 
    # THE CORRESPONDING ARRAY OF BOUNDARY DISPLACEMENTS [NO OF BOUNDARY NODES x DIMENSIONS]
    Dirichlet_nodes, Dirichlet_values = curvilinear_mesh.GetDirichletData() 

    print(Dirichlet_values)



def Leaf_Shorter():

    # THIS IS AN EXAMPLE OF A 2D LEAF SHAPED GEOMETRY MESHED WITH P=8
    # TRIANGULAR FINITE ELEMENTS - SAME AS THE C++ EXAMPLE

    # READ MESH DATA
    elements = np.loadtxt("leaf_elements.dat",delimiter=",").astype(np.uint64)
    points = np.loadtxt("leaf_points.dat",delimiter=",",dtype=np.float64)
    edges = np.loadtxt("leaf_edges.dat",delimiter=",").astype(np.uint64)
    # SUPPLY CAD FILE
    iges_filename = "leaf.iges" 

    # DOES THE MESH/CAD FILE NEED TO BE SCALED?
    # THIS IS IMPORTANT AS MOST CAD LIBRARIES SCALE UP/DOWN 
    # IMPORTED CADD FILES
    scale = 1000.;
    # THIS CONDITION TELLS PostMesh IF ALL THE POINTS IN THE MESH
    # FALL WITHIN CAD GEOMETRY OR IF THERE ARE POINST OUTISDE WHICH
    # DO NOT TO BE PROJECTED
    condition = 1.e10;
    # PRECISION TOLERANCE BETWEEN CAD GEOMETRY AND MESH DATA.
    # NORMALLY, DUE TO MESH DATA AND CAD GEOMETRY COMING FROM DIFFERENT
    # SOURCES, THERE'S AN ARITHMATIC PRECISION ISSUE. THIS PRECISION TELLS
    # PostMesh TO TREAT POINTS FROM CAD AND MESH WITHIN THIS PRECISION AS
    # ONE POINT 
    precision = 1.0e-07;
    # NODAL SPACING OF POINTS IN THE REFRERENCE TRIANGLE (GAUSS-LOBATTO SPACING IN THS CASE)
    nodal_spacing = np.array([-1.,-0.899758,-0.67718628,
        -0.36311746,0.,0.36311746,0.67718628,0.899758,1.])


    curvilinear_mesh = PostMeshCurve("tri",2)

    curvilinear_mesh.SetScale(scale)
    curvilinear_mesh.SetCondition(condition)
    curvilinear_mesh.SetMesh(elements=elements, points=points, edges=edges,
        faces=np.zeros((1,4),dtype=np.uint64), spacing=nodal_spacing.reshape(-1,1),
        scale_mesh=True)

    curvilinear_mesh.SetProjectionPrecision(precision)
    curvilinear_mesh.ComputeProjectionCriteria()
    # READ THE GEOMETRY FROM THE IGES FILE
    curvilinear_mesh.SetGeometry(iges_filename)
    # PERFORM POINT PROJECTION AND POINT INVERSION
    curvilinear_mesh.PerformPointProjectionInversionCurve(projection_type="arc_length")
    # OBTAIN MODIFIED MESH POINTS - THIS IS NECESSARY TO ENSURE LINEAR MESH IS ALSO CORRECT
    curvilinear_mesh.ReturnModifiedMeshPoints(points)
    # GET DIRICHLET DATA - (THE DISPLACMENT OF BOUNDARY NODES)
    Dirichlet_nodes, Dirichlet_values = curvilinear_mesh.GetDirichletData() 

    print(Dirichlet_values)




if __name__ == "__main__":
    Leaf()
    Leaf_Shorter()