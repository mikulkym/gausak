from distutils.core import setup
from Cython.Build import cythonize
from distutils.extension import Extension

from Cython.Distutils import build_ext
setup(

    cmdclass = {'build_ext': build_ext},
    ext_modules = [Extension("gaussian", ["gaussian.pyx", "utils.pyx"])]
    # ext_modules = cythonize("./*.pyx")
)

