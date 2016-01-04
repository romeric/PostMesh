CC = gcc
CXX = g++

CXXFLAGS = -std=c++11
WARNFLAGS = -Wall -Wextra -Wno-unused
OPTFLAGS = -O3 -march=native -mtune=native -mfpmath=sse -ffast-math -funroll-loops -finline-functions
INCFLAGS = -I../../include/ -I/usr/local/include/oce -I/usr/local/include/eigen/

OCELIBS = -L/usr/local/lib -l:libTKIGES.so.9 -l:libTKSTEP.so.9 \
  -l:libTKXSBase.so.9 -l:libTKBRep.so.9 -l:libTKernel.so.9 \
  -l:libTKTopAlgo.so.9 -l:libTKGeomBase.so.9 -l:libTKMath.so.9 \
  -l:libTKHLR.so.9 -l:libTKG2d.so.9 -l:libTKBool.so.9 -l:libTKG3d.so.9 \
  -l:libTKOffset.so.9 -l:libTKXMesh.so.9 -l:libTKMesh.so.9 -l:libTKMeshVS.so.9 \
  -l:libTKGeomAlgo.so.9 -l:libTKShHealing.so.9 -l:libTKFeat.so.9 -l:libTKFillet.so.9 \
  -l:libTKBO.so.9 -l:libTKPrim.so.9 -l:libTKAdvTools.so.9 -l:libTKPShape.so.9 \
  -l:libTKBO.so.9 -l:libTKXSBase.so.9 -l:libTKTopAlgo.so.9 -D_OCC64

RM = rm -f

PREFIX = /home/roman/.local/lib
POSTMESHLIB = -L$(PREFIX)/ -l:PostMesh.so

EXAMPLE_SRC	= leaf.cpp
EXAMPLE = leaf


.PHONY: all clean

all: $(EXAMPLE)

$(EXAMPLE): $(EXAMPLE_SRC)
	@echo "Building leaf example"
	$(CXX) $^ -o $@ $(CXXFLAGS) $(WARNFLAGS) $(OPTFLAGS) $(INCFLAGS) $(LDFLAGS) $(POSTMESHLIB) $(OCELIBS)

clean:
	$(RM) $(EXAMPLE)