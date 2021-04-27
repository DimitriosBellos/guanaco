#
# Copyright (C) 2019 James Parkhurst
#
# This code is distributed under the GPLv3 license.
#
import os
import subprocess
import sys
from setuptools import setup, find_packages, Extension
from setuptools.command.build_ext import build_ext


class CMakeBuild(build_ext):
    """
    Build the extensions

    """

    def build_extensions(self):

        # Set the cmake directory
        cmake_lists_dir = os.path.abspath(".")

        # Ensure the build directory exists
        if not os.path.exists(self.build_temp):
            os.makedirs(self.build_temp)

        # Run Cmake once
        ext = self.extensions[0]

        # Get the directory
        extdir = os.path.abspath(os.path.dirname(self.get_ext_fullpath(ext.name)))

        # Arguments to cmake
        cmake_args = [
            "-DCMAKE_BUILD_TYPE=%s" % "Release",
            "-DCMAKE_LIBRARY_OUTPUT_DIRECTORY=%s" % extdir,
            "-DPYTHON_EXECUTABLE=%s" % sys.executable,
        ]

        # Config and the extension
        subprocess.check_call(
            ["cmake", cmake_lists_dir] + cmake_args, cwd=self.build_temp
        )

        # Build the extension
        subprocess.check_call(["cmake", "--build", "."], cwd=self.build_temp)


def main():
    """
    Setup the package

    """
    tests_require = ["pytest", "pytest-cov", "mock", "scipy"]

    setup(
        package_dir={"": "src"},
        packages=find_packages(where="src"),
        install_requires=["mrcfile", "numpy", "pyyaml"],
        setup_requires=["pytest-runner"],
        tests_require=tests_require,
        test_suite="tests",
        ext_modules=[Extension("guanaco_ext", [])],
        cmdclass={"build_ext": CMakeBuild},
        entry_points={
            "console_scripts": [
                "guanaco=guanaco.command_line:main",
                "guanaco.plot_ctf=guanaco.command_line:plot_ctf",
                "guanaco.generate_ctf=guanaco.command_line:generate_ctf",
                "guanaco.correct=guanaco.command_line:correct",
            ]
        },
        extras_require={
            "build_sphinx": ["sphinx", "sphinx_rtd_theme"],
            "test": tests_require,
        },
    )


if __name__ == "__main__":
    main()
