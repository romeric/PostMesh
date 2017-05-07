from setuptools import setup
from distutils.command.clean import clean
from distutils.extension import Extension
from distutils.sysconfig import get_config_vars 
from Cython.Build import cythonize
import os, platform
import sys
import numpy


# Get Platform/OS
_os = sys.platform

# Get the current directory
_pwd_ = os.path.dirname(os.path.realpath('__file__'))

# Remove the "-Wstrict-prototypes" compiler option, which isn't valid for C++.
cfg_vars = get_config_vars()
for key, value in cfg_vars.items():
    if isinstance(value,str):
        cfg_vars[key] = value.replace("-Wstrict-prototypes", "")

# Suppress numpy deprecation warnings
no_deprecated = ("NPY_NO_DEPRECATED_API",None)

sourcefiles = ["PostMeshPy.pyx",
                _pwd_+"/src/PostMeshBase.cpp",
                _pwd_+"/src/PostMeshCurve.cpp",
                _pwd_+"/src/PostMeshSurface.cpp"]



# Set the compiler
_cxx_compiler = get_config_vars()['CXX'].split(' ')[0]
os.environ["CC"] = _cxx_compiler
os.environ["CXX"] = _cxx_compiler

# Compiler arguments
if "clang++" in _cxx_compiler or ("c++" in _cxx_compiler and "darwin" in _os):
    compiler_args = ["-std=c++11","-m64","-march=native","-mtune=native", "-ffp-contract=fast",
                    "-ffast-math", "-flto","-DNPY_NO_DEPRECATED_API", "-Wno-shorten-64-to-32"]
else:
    compiler_args = ["-std=c++11","-m64","-march=native","-mtune=native", "-ffp-contract=fast",
                    "-mfpmath=sse","-ffast-math","-ftree-vectorize", "-finline-limit=100000",
                    "-funroll-loops","-finline-functions","-Wno-unused-function",
                    "-flto","-DNPY_NO_DEPRECATED_API","-Wno-cpp"]

# Link to OpenCascade runtime libraries
# Search for all subdirectories under /usr/local/lib
# Change the directory name if occ is elsewhere 
occ_dir = "/usr/local/lib"
all_dir_libs = os.listdir(occ_dir)
occ_libs = []
for i in all_dir_libs:
    lib_suffix = i.split(".")[-1]
    if i[:4]=="libT" and (lib_suffix != "a" and lib_suffix != "la" \
    and lib_suffix != "0"):
        if "darwin" in _os:
            occ_libs.append(i[3:-6])
        elif "linux" in _os:
            occ_libs.append(":"+i)

# Create extension module
extensions = [
    Extension(
        name = "PostMeshPy",  
        sources = sourcefiles,
        language="c++",
        include_dirs = [_pwd_,_pwd_+"/include/",
                        "/usr/local/include/eigen/",
                        "/usr/local/include/oce/",
                        numpy.get_include()],
        libraries= ["stdc++"] + occ_libs, 
        library_dirs = [_pwd_,"/usr/local/lib/"],
        extra_compile_args = compiler_args,
        define_macros=[no_deprecated],
        ),
]

setup(
    ext_modules = cythonize(extensions),
    name = "PostMeshPy",
    version = "1.3",
    description = "A Python wrapper for PostMesh - a high order curvilinear mesh generator based on OpenCascade",
    author="Roman Poya",
    author_email = "r.poya@swansea.ac.uk",
    url = "https://github.com/romeric/PostMesh",
)