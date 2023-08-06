from glob import glob
import os
import numpy as np
import platform
import pybind11
import setuptools
from setuptools import Extension, setup
from setuptools.command.build_ext import build_ext
import sys
import tempfile

extra_objects = []
include_dirs = [
	pybind11.get_include(),
	np.get_include(),
	"./src/chm/"
]
libraries = []
source_files = glob("./src/chm/*.cpp")

ext_modules = [
	Extension(
		"chm_hnsw",
		source_files,
		include_dirs=include_dirs,
		libraries=libraries,
		language="c++",
		extra_objects=extra_objects
	)
]

class BuildExt(build_ext):
	"""A custom build extension for adding compiler-specific options."""
	c_opts = {
		"msvc": ["/EHsc", "/openmp", "/O2"],
		"unix": ["-O3"]
	}

	if not os.environ.get("CHM_HNSW_NO_NATIVE"):
		c_opts["unix"].append("-march=native")

	link_opts = {
		"unix": [],
		"msvc": []
	}

	if sys.platform == "darwin":
		if platform.machine() == "arm64":
			c_opts["unix"].remove("-march=native")
		c_opts["unix"] += ["-stdlib=libc++", "-mmacosx-version-min=10.7"]
		link_opts["unix"] += ["-stdlib=libc++", "-mmacosx-version-min=10.7"]
	else:
		c_opts["unix"].append("-fopenmp")
		link_opts["unix"].extend(["-fopenmp", "-pthread"])

	def build_extensions(self):
		ct = self.compiler.compiler_type
		opts = self.c_opts.get(ct, [])
		flag = "-std=c++17"

		if ct == "unix":
			opts.append('-DVERSION_INFO="%s"' % self.distribution.get_version())

			if has_flag(self.compiler, "-fvisibility=hidden"):
				opts.append("-fvisibility=hidden")

		elif ct == "msvc":
			flag = "/std:c++17"
			opts.append('/DVERSION_INFO=\\"%s\\"' % self.distribution.get_version())

		opts.append(flag)

		for ext in self.extensions:
			ext.extra_compile_args.extend(opts)
			ext.extra_link_args.extend(self.link_opts.get(ct, []))

		build_ext.build_extensions(self)

# As of Python 3.6, CCompiler has a `has_flag` method.
# cf http://bugs.python.org/issue26689
def has_flag(compiler, flag):
	"""Returns a boolean indicating whether a flag name is supported on the specified compiler."""

	with tempfile.NamedTemporaryFile("w", suffix=".cpp") as f:
		f.write("int main(int argc, char **argv){return 0;}")

		try:
			compiler.compile([f.name], extra_postargs=[flag])
		except setuptools.distutils.errors.CompileError:
			return False

	return True

setup(
	name="chm_hnsw",
	version="0.0.6",
	description="Custom implementation of HNSW index.",
	author="Matěj Chmel",
	url="https://github.com/Matej-Chmel/hnsw-index",
	long_description="Custom implementation of HNSW index.",
	ext_modules=ext_modules,
	install_requires=["numpy"],
	cmdclass={"build_ext": BuildExt},
	zip_safe=False
)
