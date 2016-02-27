CC = gcc
CXX = g++

CXXFLAGS = -std=c++11
WARNFLAGS = -Wall -Wextra -Wno-unused
OPTFLAGS = -O3 -march=native -mtune=native -mfpmath=sse -ffast-math -funroll-loops -finline-functions
INCFLAGS = -Iinclude/ -I/usr/local/include/oce -I/usr/local/include/eigen
DYNFLAGS = -shared -fPIC

RM = rm -f
MKDIR = mkdir
DIRECTORY = build

SRCS	= src/PostMeshBase.cpp src/PostMeshCurve.cpp src/PostMeshSurface.cpp  
LIBS 	= $(DIRECTORY)/PostMesh.so

.PHONY: all install

all: $(DIRECTORY) $(LIBS)

# USE @ TO SUPRESS ECHOING COMMANDS 
$(DIRECTORY):
	@: if [ -d "$@" ]; then $(RM) -r $@; fi
	$(MKDIR) $@

$(LIBS): $(SRCS)
	@echo "Building PostMesh shared library"
	$(CXX) $(CXXFLAGS) $(DYNFLAGS) $(WARNFLAGS) $(OPTFLAGS) $(INCFLAGS) $^ -o $@

PREFIX = /usr/local/lib

install: $(LIBS)
	install -m 0755 $(LIBS) $(PREFIX)

uninstall:
	$(RM) $(PREFIX)/PostMesh.so

clean:
	$(RM) -r $(DIRECTORY)