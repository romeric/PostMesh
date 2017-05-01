CXXFLAGS = -std=c++11
WARNFLAGS = -Wall -Wextra -Wno-unused
OPTFLAGS = -O3 -march=native -mtune=native -mfpmath=sse -ffast-math -DNDEBUG
INCFLAGS = -Iinclude/ -I/usr/local/include/oce -I/usr/local/include/eigen
LIBFLAGS = -L/usr/local/lib 
OCELIB = -lTKernel -lTKMath -lTKBRep -lTKIGES -lTKSTEP -lTKG2d -lTKG3d -lTKMeshVS -lTKPrim -lTKGeomBase -lTKGeomAlgo -lTKTopAlgo -lTKShHealing -lTKXSBase
LIBSHAREDFLAGS = -shared -fPIC -pthread

RM = rm -rf
MKDIR = mkdir
DIRECTORY = build

SRCS	= src/PostMeshBase.cpp src/PostMeshCurve.cpp src/PostMeshSurface.cpp
UNAME_S := $(shell uname -s)
ifeq ($(UNAME_S),Linux)
    POSTFIX += libPostMesh.so
endif
ifeq ($(UNAME_S),Darwin)
    POSTFIX += libPostMesh.dylib
endif
LIBS 	= $(POSTFIX)

.PHONY: all install

all: $(DIRECTORY) $(LIBS)

$(DIRECTORY):
	@$(MKDIR) $@

$(LIBS): $(SRCS)
	@echo "Building PostMesh shared library"
	$(CXX) $(CXXFLAGS) $(LIBSHAREDFLAGS) $(WARNFLAGS) $(OPTFLAGS) $(INCFLAGS) $(LIBFLAGS) $(OCELIB) $^ -o $(DIRECTORY)/$@

INSTALLDIR = /usr/local/lib

install: $(LIBS)
	install -m 0755 $(DIRECTORY)/$(LIBS) $(INSTALLDIR)

uninstall:
	$(RM) $(INSTALLDIR)/$(POSTFIX)

clean:
	$(RM) $(DIRECTORY)