#include <PostMeshSurface.hpp>
#include <PyInterfaceEmulator.hpp>


int main()
{
  // THIS IS AN EXAMPLE OF A 2D LEAF SHAPED GEOMETRY MESHED WITH P=8
  // TRIANGULAR FINITE ELEMENTS

  // GET PROBLEM PATH
  auto exepath = getexepath();
  auto cpath = exepath.substr(0,exepath.size()-std::string("leaf").size());

  // READ MESH DATA FROM FILES
  std::string elem_file = cpath+"leaf_elements.dat";
  std::string point_file = cpath+"leaf_points.dat";
  std::string edge_file = cpath+"leaf_edges.dat";

  // PostMesh NEEDS ALL THIS INFORMATION A PRIORI
  Eigen::MatrixUI elements = PostMeshBase::ReadI(elem_file,',');
  Eigen::MatrixR points = PostMeshBase::ReadR(point_file,',');
  Eigen::MatrixUI edges = PostMeshBase::ReadI(edge_file,',');
  Eigen::MatrixUI faces = Eigen::MatrixUI::Zero(1,4);


  // NODAL SPACING OF POINTS IN THE REFRERENCE TRIANGLE (GAUSS-LOBATTO SPACING IN THS CASE)
  Eigen::Matrix<Real,9,1> nodal_spacing;
  nodal_spacing << -1.,-0.899758,-0.67718628,-0.36311746,0.,0.36311746,0.67718628,0.899758,1.; 
  
  // CAD FILE TO BE READ
  std::string iges_filename = cpath+"leaf.iges";

  // DOES THE MESH/CAD FILE NEED TO BE SCALED?
  // THIS IS IMPORTANT AS MOST CAD LIBRARIES SCALE UP/DOWN 
  // IMPORTED CADD FILES
  Real scale = 1000.;
  // THIS CONDITION TELLS PostMesh IF ALL THE BOUNDARY POINTS 
  // IN THE MESH REQUIRE PROJECTION - ANY BOUNDARY POINT FALLING 
  // WITHIN THIS RADIUS WOULD BE PROJECTED
  Real condition = 1.e10;
  // PRECISION TOLERANCE BETWEEN CAD GEOMETRY AND MESH DATA.
  // NORMALLY, DUE TO MESH DATA AND CAD GEOMETRY COMING FROM DIFFERENT
  // SOURCES, THERE'S AN ARITHMATIC PRECISION ISSUE. THIS PRECISION TELLS
  // PostMesh TO TREAT POINTS FROM CAD AND MESH WITHIN THIS PRECISION AS
  // ONE POINT 
  auto precision = 1.0e-07;


  // MAKE AN INSTANCE OF PostMeshCurve
  auto curvilinear_mesh = PostMeshCurve();
  // PASS MESH DATA TO PostMesh - PostMesh takes raw pointers as input arguments
  curvilinear_mesh.SetMeshElements(elements.data(), elements.rows(), elements.cols());
  curvilinear_mesh.SetMeshPoints(points.data(),points.rows(), points.cols());
  curvilinear_mesh.SetMeshEdges(edges.data(), edges.rows(), edges.cols());
  curvilinear_mesh.SetMeshFaces(faces.data(),  faces.rows(),  faces.cols());
  curvilinear_mesh.SetScale(scale);
  curvilinear_mesh.SetCondition(condition);
  curvilinear_mesh.SetProjectionPrecision(precision);
  curvilinear_mesh.ComputeProjectionCriteria();
  curvilinear_mesh.ScaleMesh();
  curvilinear_mesh.InferInterpolationPolynomialDegree();
  curvilinear_mesh.SetNodalSpacing(nodal_spacing.data(), nodal_spacing.rows(), nodal_spacing.cols());
  // GET EDGE NUMBERING ORDER
  curvilinear_mesh.GetBoundaryPointsOrder();
  // READ THE GEOMETRY FROM THE IGES FILE
  curvilinear_mesh.ReadIGES(iges_filename.c_str());
  // EXTRACT GEOMETRY INFORMATION FROM THE IGES FILE
  curvilinear_mesh.GetGeomVertices();
  // FIRST IDENTIFY WHICH CURVES CONTAIN WHICH EDGES
  curvilinear_mesh.GetGeomEdges();
  // FIND WHICH POINTS OR ON WHICH EDGE
  curvilinear_mesh.GetGeomPointsOnCorrespondingEdges();
  // FIRST IDENTIFY WHICH CURVES CONTAIN WHICH EDGES
  curvilinear_mesh.IdentifyCurvesContainingEdges();
  // PROJECT ALL BOUNDARY POINTS FROM THE MESH TO THE CURVE
  curvilinear_mesh.ProjectMeshOnCurve();
  // FIX IMAGES AND ANTI IMAGES IN PERIODIC CURVES/SURFACES
  curvilinear_mesh.RepairDualProjectedParameters();
  // PERFORM POINT INVERSION FOR THE INTERIOR POINTS (ARC-LENGTH BASED POINT PROJECTION)
  curvilinear_mesh.MeshPointInversionCurveArcLength();
  // OBTAIN MODIFIED MESH POINTS - THIS IS NECESSARY TO ENSURE LINEAR MESH IS ALSO CORRECT
  curvilinear_mesh.ReturnModifiedMeshPoints(points.data());
  // GET DIRICHLET DATA - (THE DISPLACMENT OF BOUNDARY NODES)
  // nodesDBC IS AN ARRAY OF SIZE [NO OF BOUNDARY NODES] CONTAINING 
  // GLOBAL NODE NUMBERS IN THE ELEMENT CONNECTIVITY AND Dirichlet IS 
  // THE CORRESPONDING DISPLACEMENT ARRAY [NO OF BOUNDARY NODES x DIMENSIONS]
  DirichletData Dirichlet_data = curvilinear_mesh.GetDirichletData();

  // FINALLY, CHECK DIRICHLET DATA
  print("\n");
  auto counter = 1;
  for (auto &i: Dirichlet_data.displacement_BC_stl) {
    std::cout << i << "\t";
    if (std::remainder(counter,curvilinear_mesh.ndim) == 0) {
      print(" ");
    }
    counter++;
  }
  print("\n\n");

  return 0;
}
