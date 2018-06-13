from setuptools import setup
from setuptools import find_packages
from distutils.command.clean import clean
from distutils.extension import Extension
from distutils.sysconfig import get_config_vars
from Cython.Build import cythonize
import os, platform, sys, fnmatch
import numpy


def setup_package():

    # Get Platform/OS
    _os = sys.platform

    # Get the current directory
    _pwd_ = os.path.dirname(os.path.realpath('__file__'))
    _upwd_ = os.path.dirname(_pwd_)

    # Remove the "-Wstrict-prototypes" compiler option, which isn't valid for C++.
    cfg_vars = get_config_vars()
    for key, value in cfg_vars.items():
        if isinstance(value,str):
            cfg_vars[key] = value.replace("-Wstrict-prototypes", "")

    # Suppress numpy deprecation warnings
    no_deprecated = ("NPY_NO_DEPRECATED_API",None)

    sourcefiles =   [
                        os.path.join(_pwd_,"bindings","PostMeshPy.pyx"),
                        os.path.join(_pwd_,"src","PostMeshBase.cpp"),
                        os.path.join(_pwd_,"src","PostMeshCurve.cpp"),
                        os.path.join(_pwd_,"src","PostMeshSurface.cpp")
                    ]


    # Set the compiler
    # Must be called as: "python setup.py build_ext CXX=/usr/bin/g++"
    args = sys.argv
    _cxx_specified = False
    if len(args) > 1:
        for counter, arg in enumerate(args):
            if "CXX" in arg:
                _cxx_specified = True
                _cxx_compiler = arg.split("=")[-1]
                args.remove(arg)
    if _cxx_specified:
        os.environ["CC"] = _cxx_compiler
        os.environ["CXX"] = _cxx_compiler
    else:
        _cxx_compiler = get_config_vars()['CXX'].split(' ')[0]
        os.environ["CC"] = _cxx_compiler
        os.environ["CXX"] = _cxx_compiler


    # Compiler arguments
    if "clang++" in _cxx_compiler or ("c++" in _cxx_compiler and "darwin" in _os):
        compiler_args = ["-O3","-std=c++11","-m64","-march=native","-mtune=native","-ffp-contract=fast",
                        "-ffast-math","-flto","-DNPY_NO_DEPRECATED_API","-Wno-shorten-64-to-32"]
    else:
        compiler_args = ["-O3","-std=c++11","-m64","-march=native","-mtune=native","-ffp-contract=fast",
                        "-mfpmath=sse","-ffast-math","-ftree-vectorize","-finline-functions","-finline-limit=100000",
                        "-funroll-loops","-Wno-unused-function","-flto","-DNPY_NO_DEPRECATED_API","-Wno-cpp"]

    # if "darwin" in _os:
        # compiler_args.append("-stdlib=libstdc++")


    eigen_include_path = "/usr/local/include/eigen/"
    oce_include_path = "/usr/local/include/oce/"


    # Link to OpenCascade runtime libraries
    # Search for all subdirectories under /usr/local/lib
    # Change the directory name if occ is elsewhere
    occ_dir = "/usr/local/lib"
    all_dir_libs = os.listdir(occ_dir)
    occ_libs = []
    for i in all_dir_libs:
        lib_suffix = i.split(".")[-1]
        if i[:4]=="libT" and (lib_suffix != "a" and lib_suffix != "la" and lib_suffix != "0"):
            if "darwin" in _os:
                occ_libs.append(i[3:-6])
            elif "linux" in _os:
                occ_libs.append(":"+i)

    found_oce = False
    for i in occ_libs:
        if "TKernel" in i:
            found_oce = True
            break


    if found_oce is False:
        if "darwin" in _os:
            version = next(os.walk("/usr/local/Cellar/oce/"))[1][0]
            occ_dir = os.path.join("/usr/local/Cellar/oce",version,"lib")
            oce_include_path = os.path.join("/usr/local/Cellar/oce",version,"include","oce")
        elif "linux" in _os:
            occ_dir = "/usr/lib/x86_64-linux-gnu"
            oce_include_path = "/usr/include/oce/"

        all_dir_libs = os.listdir(occ_dir)
        for i in all_dir_libs:
            lib_suffix = i.split(".")[-1]
            if i[:4]=="libT" and (lib_suffix != "a" and lib_suffix != "la" and lib_suffix != "0"):
                occ_libs.append(":"+i)


    # Create extension module
    extensions = [
        Extension(
                name = "PostMeshPy",
                sources = sourcefiles,
                language="c++",
                include_dirs = [_pwd_,
                                _pwd_+"/include/",
                                eigen_include_path,
                                oce_include_path,
                                numpy.get_include()],
                libraries= ["stdc++"] + occ_libs,
                library_dirs = [_pwd_, os.path.join("/usr","local","lib")],
                extra_compile_args = compiler_args,
                define_macros=[no_deprecated],
            ),
    ]

    with open("README.md", "r") as fh:
        long_description = fh.read()

    setup(
        ext_modules = cythonize(extensions),
        name = "PostMeshPy",
        version = "1.6.1",
        description = "A Python wrapper for PostMesh - a high order curvilinear mesh generator based on OpenCascade",
        long_description=long_description,
        long_description_content_type="text/markdown",
        author="Roman Poya",
        author_email = "roman_poya@yahoo.com",
        url = "https://github.com/romeric/PostMesh",
        license="MIT",
        install_requires=[
          'numpy>=1.9',
          'cython>=0.23'],
        packages=find_packages(),
        include_package_data=True,
        package_data={'': ['bindings/*','src/*','include/*','example/*',
            '*.pyx', '*.pxd', '*.h', '*.hpp', '*.c', '*.cpp', 'Makefile']},
        extra_files = "LICENSE.md"
    )


if __name__ == "__main__":
    setup_package()
