CXXFLAGS = -std=c++11
WARNFLAGS = -Wall -Wextra -Wno-unused
OPTFLAGS = -O3 -march=native -mtune=native -mfpmath=sse -ffast-math -D_OCC64 -DNDEBUG
INCFLAGS = -I../../include/ -I/usr/local/include/oce -I/usr/local/include/eigen/

# For both OCE and PostMesh
LIBDIR = -L/usr/local/lib/  
POSTMESHLIB = -lPostMesh
OCELIBS = -lTKernel -lTKMath -lTKBRep -lTKIGES -lTKSTEP -lTKG2d -lTKG3d -lTKMeshVS -lTKPrim -lTKGeomBase -lTKGeomAlgo -lTKTopAlgo -lTKShHealing -lTKXSBase


RM = rm -rf

EXAMPLE_SRC	= leaf.cpp
EXAMPLE = leaf


.PHONY: all clean

all: $(EXAMPLE)

$(EXAMPLE): $(EXAMPLE_SRC)
	@echo "Building leaf example"
	$(CXX) $^ -o $@ $(CXXFLAGS) $(WARNFLAGS) $(OPTFLAGS) $(INCFLAGS) $(LIBDIR) $(POSTMESHLIB) $(OCELIBS)

clean:
	$(RM) $(EXAMPLE)