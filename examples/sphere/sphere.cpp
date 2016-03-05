#include <PostMeshSurface.hpp>
#include <PyInterfaceEmulator.hpp>


int main()
{
  // THIS IS AN EXAMPLE OF A SPHERE MESH WITH QUARTIC (P=4)
  // TETRAHEDRAL FINITE ELEMENTS

  // GET PROBLEM PATH
  auto exepath = getexepath();
  auto cpath = exepath.substr(0,exepath.size()-std::string("sphere").size());

  // READ MESH DATA FROM FILES
  std::string elem_file = cpath+"sphere_elements.dat";
  std::string point_file = cpath+"sphere_points.dat";
  std::string edge_file = cpath+"sphere_edges.dat";
  std::string face_file = cpath+"sphere_faces.dat";

  // PostMesh NEEDS ALL THIS INFORMATION A PRIORI
  Eigen::MatrixUI elements = PostMeshBase::ReadI(elem_file,',');
  Eigen::MatrixR points = PostMeshBase::ReadR(point_file,',');
  Eigen::MatrixUI edges = PostMeshBase::ReadI(edge_file,',');
  Eigen::MatrixUI faces = PostMeshBase::ReadI(face_file,',');

  // NODAL SPACING OF POINTS IN THE REFRERENCE TRIANGLE (FEKETE POINT SPACING IN THS CASE)
  std::string spacing_file = cpath+"nodal_spacing_p4.dat";
  Eigen::MatrixR nodal_spacing = PostMeshBase::ReadR(spacing_file,',');
  
  // SUPPLY CAD FILE
  std::string iges_filename = cpath+"sphere.igs";

  // DOES THE MESH/CAD FILE NEED TO BE SCALED?
  // THIS IS IMPORTANT AS MOST CAD LIBRARIES SCALE UP/DOWN 
  // IMPORTED CADD FILES
  Real scale = 1000.;
  // THIS CONDITION TELLS PostMesh IF ALL THE BOUNDARY POINTS 
  // IN THE MESH REQUIRE PROJECTION - ANY BOUNDARY POINT FALLING 
  // WITHIN THIS RADIUS WOULD BE PROJECTED
  Real radius = 1.0e10;
  // PRECISION TOLERANCE BETWEEN CAD GEOMETRY AND MESH DATA.
  // NORMALLY, DUE TO MESH DATA AND CAD GEOMETRY COMING FROM DIFFERENT
  // SOURCES, THERE'S AN ARITHMATIC PRECISION ISSUE. THIS PRECISION TELLS
  // PostMesh TO TREAT POINTS FROM CAD AND MESH WITHIN THIS PRECISION AS
  // ONE POINT 
  auto precision = 1.0e-07;


  // MAKE AN INSTANCE OF PostMeshSurface
  auto curvilinear_mesh = PostMeshSurface();
  // PASS MESH DATA TO PostMesh - PostMesh TAKES RAW BUFFERS/POINTERS AS INPUT ARGUMENTS
  curvilinear_mesh.SetMeshElements(elements.data(), elements.rows(), elements.cols());
  curvilinear_mesh.SetMeshPoints(points.data(),points.rows(), points.cols());
  curvilinear_mesh.SetMeshEdges(edges.data(), edges.rows(), edges.cols());
  curvilinear_mesh.SetMeshFaces(faces.data(),  faces.rows(),  faces.cols());
  curvilinear_mesh.SetScale(scale);
  curvilinear_mesh.SetCondition(radius);
  curvilinear_mesh.SetProjectionPrecision(precision);
  curvilinear_mesh.ComputeProjectionCriteria();
  curvilinear_mesh.ScaleMesh();
  curvilinear_mesh.InferInterpolationPolynomialDegree();
  curvilinear_mesh.SetNodalSpacing(nodal_spacing.data(), nodal_spacing.rows(), nodal_spacing.cols());
  // READ THE GEOMETRY FROM THE IGES FILE
  curvilinear_mesh.ReadIGES(iges_filename.c_str());
  // EXTRACT GEOMETRY INFORMATION FROM THE IGES FILE
  curvilinear_mesh.GetGeomVertices();
  // EXTRACT TRUE BOUNDARY FACES FROM CAD FILE
  curvilinear_mesh.GetGeomFaces();
  curvilinear_mesh.GetGeomPointsOnCorrespondingFaces();
  // FIRST IDENTIFY WHICH SURFACES CONTAIN WHICH FACES
  curvilinear_mesh.IdentifySurfacesContainingFaces();
  // PROJECT ALL BOUNDARY POINTS FROM THE MESH TO THE SURFACE
  curvilinear_mesh.ProjectMeshOnSurface();
  // PERFORM POINT INVERSION FOR THE INTERIOR POINTS (ORTHOGONAL PROJECTION)
  // THE TWO ARGUMENTS ARE FOR ALLOWING PROJECTION ON CURVE INTERSECTION AND
  // MODIFYING THE LINEAR MESH IF IT DOES NOT MATCH WITH THE GEOMETRICAL 
  // POINTS IN THE CAD FILE (WITHIN THE SPECFIED PRECISION) 
  curvilinear_mesh.MeshPointInversionSurface(static_cast<Integer>(0),static_cast<Integer>(1));
  // OBTAIN MODIFIED MESH POINTS - THIS IS NECESSARY TO ENSURE LINEAR MESH IS ALSO CORRECT
  curvilinear_mesh.ReturnModifiedMeshPoints(points.data());
  // GET DIRICHLET DATA - (THE DISPLACMENT OF BOUNDARY NODES)
  // nodesDBC IS AN ARRAY OF SIZE [NO OF BOUNDARY NODES] CONTAINING 
  // GLOBAL NODE NUMBERS IN THE ELEMENT CONNECTIVITY AND Dirichlet IS 
  // THE CORRESPONDING DISPLACEMENT ARRAY [NO OF BOUNDARY NODES x DIMENSION]
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
