# coding=utf-8
"""Minimal setup.py shim for Octolapse.

All package metadata lives in pyproject.toml (static version, no versioneer,
no git metadata needed). This shim only provides what cannot be declared
declaratively: the C++ extension (GcodePositionProcessor) and the custom
build_ext command that selects per-platform compiler flags.

Nothing here imports octoprint, so the package builds fine both with and
without pip's build isolation.
"""

from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
import sys

# Compiler options
compiler_opts = {
    'extra_compile_args': [],
    'extra_link_args': [],
    'define_macros': [('DEBUG_chardet', '1'), ('IS_PYTHON_EXTENSION', '1')]
}

# Platform-specific compiler flags
if sys.platform == 'win32':
    compiler_opts['extra_compile_args'].extend(['/std:c++14', '/permissive-'])
elif sys.platform == 'darwin':
    compiler_opts['extra_compile_args'].extend(['-std=c++14', '-mmacosx-version-min=10.9'])
else:
    compiler_opts['extra_compile_args'].append('-std=c++14')


class build_ext_subclass(build_ext):
    def build_extensions(self):
        # Detect compiler type
        compiler_type = self.compiler.compiler_type if hasattr(self.compiler, 'compiler_type') else 'unix'

        print(f"Compiling Octolapse Parser Extension with {compiler_type}.")

        for ext in self.extensions:
            ext.extra_compile_args.extend(compiler_opts['extra_compile_args'])
            ext.extra_link_args.extend(compiler_opts['extra_link_args'])
            ext.define_macros.extend(compiler_opts['define_macros'])

        build_ext.build_extensions(self)


setup(
    cmdclass={'build_ext': build_ext_subclass},
    ext_modules=[
        Extension(
            'GcodePositionProcessor',
            sources=[
                'octoprint_octolapse/data/lib/c/gcode_parser.cpp',
                'octoprint_octolapse/data/lib/c/extruder.cpp',
                'octoprint_octolapse/data/lib/c/gcode_position.cpp',
                'octoprint_octolapse/data/lib/c/position.cpp',
                'octoprint_octolapse/data/lib/c/stabilization.cpp',
                'octoprint_octolapse/data/lib/c/stabilization_smart_layer.cpp',
                'octoprint_octolapse/data/lib/c/stabilization_smart_gcode.cpp',
                'octoprint_octolapse/data/lib/c/stabilization_results.cpp',
                'octoprint_octolapse/data/lib/c/trigger_position.cpp',
                'octoprint_octolapse/data/lib/c/snapshot_plan.cpp',
                'octoprint_octolapse/data/lib/c/snapshot_plan_step.cpp',
                'octoprint_octolapse/data/lib/c/parsed_command.cpp',
                'octoprint_octolapse/data/lib/c/parsed_command_parameter.cpp',
                'octoprint_octolapse/data/lib/c/gcode_comment_processor.cpp',
                'octoprint_octolapse/data/lib/c/gcode_position_processor.cpp',
                'octoprint_octolapse/data/lib/c/python_helpers.cpp',
                'octoprint_octolapse/data/lib/c/logging.cpp',
                'octoprint_octolapse/data/lib/c/utilities.cpp',
            ],
            include_dirs=['octoprint_octolapse/data/lib/c'],
            language='c++',
        )
    ]
)
