#!/bin/sh

# g++ PostMeshBase.cpp -std=c++11 -fPIC -shared -O3 -o PostMeshBase.so -I../include/ -I/usr/local/include/oce -I/home/roman/Dropbox/eigen-devel
# g++ PostMeshCurve.cpp -std=c++11 -fPIC -shared -O3 -o PostMeshCurve.so -I../include/ -I/usr/local/include/oce -I/home/roman/Dropbox/eigen-devel
# g++ PostMeshSurface.cpp -std=c++11 -fPIC -shared -O3 -o PostMeshSurface.so -I../include/ -I/usr/local/include/oce -I/home/roman/Dropbox/eigen-devel

# g++ main.cpp Examples.cpp -o Run -std=c++11 -O3 -L. PostMeshBase.so PostMeshCurve.so PostMeshSurface.so -I../include/ -I/usr/local/include/oce -I/home/roman/Dropbox/eigen-devel \
# 	-L/usr/local/lib -l:libTKIGES.so.9 -l:libTKSTEP.so.9 -l:libTKXSBase.so.9 -l:libTKBRep.so.9 -l:libTKernel.so.9 -l:libTKTopAlgo.so.9 \
# 	     -l:libTKGeomBase.so.9 -l:libTKMath.so.9 -l:libTKHLR.so.9 -l:libTKG2d.so.9 -l:libTKBool.so.9 -l:libTKG3d.so.9 -l:libTKOffset.so.9 \
# 		      -l:libTKXMesh.so.9 -l:libTKMesh.so.9 -l:libTKMeshVS.so.9 -l:libTKGeomAlgo.so.9 -l:libTKShHealing.so.9 -l:libTKFeat.so.9 -l:libTKFillet.so.9 \
# 			       -l:libTKBO.so.9 -l:libTKPrim.so.9 -l:libTKAdvTools.so -l:libTKPShape.so -l:libTKBO.so.9 -l:libTKXSBase.so.9 -l:libTKTopAlgo.so.9
#

# g++ main.cpp Examples.cpp -o Run -std=c++11 -O3  -I../include/ -I/usr/local/include/oce -I/home/roman/Dropbox/eigen-devel \
# 	-L/usr/local/lib -l:libTKIGES.so.9 -l:libTKSTEP.so.9 -l:libTKXSBase.so.9 -l:libTKBRep.so.9 -l:libTKernel.so.9 -l:libTKTopAlgo.so.9 \
# 		 -l:libTKGeomBase.so.9 -l:libTKMath.so.9 -l:libTKHLR.so.9 -l:libTKG2d.so.9 -l:libTKBool.so.9 -l:libTKG3d.so.9 -l:libTKOffset.so.9 \
# 			  -l:libTKXMesh.so.9 -l:libTKMesh.so.9 -l:libTKMeshVS.so.9 -l:libTKGeomAlgo.so.9 -l:libTKShHealing.so.9 -l:libTKFeat.so.9 -l:libTKFillet.so.9 \
# 				   -l:libTKBO.so.9 -l:libTKPrim.so.9 -l:libTKAdvTools.so -l:libTKPShape.so -l:libTKBO.so.9 -l:libTKXSBase.so.9 -l:libTKTopAlgo.so.9

# g++ main.cpp Examples.cpp -o Run -std=c++11 -O3  -L. PostMesh.so -I../include/ -I/usr/local/include/oce -I/home/roman/Dropbox/eigen-devel \
# 	-L/usr/local/lib -l:libTKIGES.so.9 -l:libTKSTEP.so.9 -l:libTKXSBase.so.9 -l:libTKBRep.so.9 -l:libTKernel.so.9 -l:libTKTopAlgo.so.9 \
# 		 -l:libTKGeomBase.so.9 -l:libTKMath.so.9 -l:libTKHLR.so.9 -l:libTKG2d.so.9 -l:libTKBool.so.9 -l:libTKG3d.so.9 -l:libTKOffset.so.9 \
# 			  -l:libTKXMesh.so.9 -l:libTKMesh.so.9 -l:libTKMeshVS.so.9 -l:libTKGeomAlgo.so.9 -l:libTKShHealing.so.9 -l:libTKFeat.so.9 -l:libTKFillet.so.9 \
# 				   -l:libTKBO.so.9 -l:libTKPrim.so.9 -l:libTKAdvTools.so -l:libTKPShape.so -l:libTKBO.so.9 -l:libTKXSBase.so.9 -l:libTKTopAlgo.so.9


g++ main.cpp Examples.cpp -o Run -std=c++11 -O3  -L. PostMesh.so -I../include/ -I/usr/local/include/oce -I/home/roman/Dropbox/eigen-devel -L/usr/local/lib -l:libTKIGES.so.9 -l:libTKSTEP.so.9 -l:libTKXSBase.so.9 -l:libTKBRep.so.9 -l:libTKernel.so.9 -l:libTKTopAlgo.so.9 		 -l:libTKGeomBase.so.9 -l:libTKMath.so.9 -l:libTKHLR.so.9 -l:libTKG2d.so.9 -l:libTKBool.so.9 -l:libTKG3d.so.9 -l:libTKOffset.so.9 -l:libTKXMesh.so.9 -l:libTKMesh.so.9 -l:libTKMeshVS.so.9 -l:libTKGeomAlgo.so.9 -l:libTKShHealing.so.9 -l:libTKFeat.so.9 -l:libTKFillet.so.9 -l:libTKBO.so.9 -l:libTKPrim.so.9 -l:libTKAdvTools.so -l:libTKPShape.so -l:libTKBO.so.9 -l:libTKXSBase.so.9 -l:libTKTopAlgo.so.9

