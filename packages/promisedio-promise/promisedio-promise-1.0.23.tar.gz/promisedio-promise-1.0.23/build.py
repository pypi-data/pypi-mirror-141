import pkg_resources
from setuptools.extension import Extension
from setuptools.command.build_ext import build_ext

define_macros_release = [
    ("Py_BUILD_CORE", "1")
]

define_macros_debug = define_macros_release + [
    ("BUILD_DEBUG_LOG", "1"),
    ("BUILD_DEBUG_MEM", "1"),
    # ("BUILD_DISABLE_FREELISTS", "1")
]

undef_macros_debug = ["NDEBUG"]

pkg_resources.get_distribution("promisedio-build-environment>=1.0.26,<1.1.0")
build_environment_include = pkg_resources.resource_filename("promisedio_build_environment", "include")

extension_defaults = {
    "include_dirs": [build_environment_include, "promisedio/promise"],
    "extra_compile_args": ["-O2"]
}

ext_modules = [
    Extension(
        "promisedio.promise._promise",
        sources=["promisedio/promise/promise.c"],
        define_macros=define_macros_release,
        **extension_defaults
    ),
    Extension(
        "promisedio.promise._promise_debug",
        sources=["promisedio/promise/promise.c"],
        define_macros=define_macros_debug,
        undef_macros=undef_macros_debug,
        **extension_defaults
    )
]


def build(setup_kwargs):
    setup_kwargs.update({
        "ext_modules": ext_modules,
        "cmdclass": {"build_ext": build_ext}
    })
