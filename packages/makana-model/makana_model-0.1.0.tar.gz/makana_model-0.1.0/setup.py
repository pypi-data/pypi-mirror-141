"""
makana_model setup
"""
import json
from os import environ, path
from pathlib import Path
import warnings

import setuptools

HERE = Path(__file__).parent.resolve()
this_directory = path.abspath(path.dirname(__file__))
# Get the package info from package.json
pkg_json = json.loads((HERE / "package.json").read_bytes())

# The name of the project
name = "makana_model"

lab_path = (HERE / pkg_json["jupyterlab"]["outputDir"])

# Representative files that should exist after a successful build
ensured_targets = [
    str(lab_path / "package.json"),
    str(lab_path / "static/style.js")
]

labext_name = pkg_json["name"]

data_files_spec = [
    ("share/jupyter/labextensions/%s" % labext_name, str(lab_path.relative_to(HERE)), "**"),
    ("share/jupyter/labextensions/%s" % labext_name, str("."), "install.json"),
]

long_description = (HERE / "README.md").read_text()

version = (
    pkg_json["version"]
    .replace("-alpha.", "a")
    .replace("-beta.", "b")
    .replace("-rc.", "rc")
) 

setup_args = dict(
    name=name,
    version=version,
    url=pkg_json["homepage"],
    author=pkg_json["author"]["name"],
    author_email=pkg_json["author"]["email"],
    description=pkg_json["description"],
    license=pkg_json["license"],
    license_file="LICENSE",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=[
        "nbformat",
        "pyyaml",
        "toml",
        "markdown-it-py~=1.0",
        "mdit_py_plugins",
    ],
    extras_require={
        # left for back-compatibility
        "myst": [],
        "toml": ["toml"],
        "rst2md": ["sphinx-gallery~=0.7.0"],
    },
    zip_safe=False,
    include_package_data=True,
    python_requires=">=3.7",
    platforms="Linux, Mac OS X, Windows",
    keywords=["Jupyter", "JupyterLab", "JupyterLab3"],
    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Framework :: Jupyter",
        "Framework :: Jupyter :: JupyterLab",
        "Framework :: Jupyter :: JupyterLab :: 3",
        "Framework :: Jupyter :: JupyterLab :: Extensions",
        "Framework :: Jupyter :: JupyterLab :: Extensions :: Prebuilt",
    ],
)

build_labextension = environ.get("BUILD_JUPYTERLAB_EXTENSION")
if build_labextension in ["0", "False", "false", "No", "no", "N", "n"]:
    build_labextension = False
    
if not build_labextension:
    # We skip the lab extension,
    # cf. https://github.com/mwouts/jupytext/issues/706
    warnings.warn(
        "Makana Model is being built WITHOUT the lab extension. "
        "Please set BUILD_JUPYTERLAB_EXTENSION=1 if you want it."
    )

    setup_args["package_data"] = {"makana_model": ["nbextension/*.*"]}
    setup_args["data_files"] = [
        (
            "etc/jupyter/nbconfig/notebook.d",
            ["jupyter-config/nbconfig/notebook.d/makana_model.json"],
        ),
        (
            "etc/jupyter/jupyter_notebook_config.d",
            ["jupyter-config/jupyter_notebook_config.d/makana_model.json"],
        ),
        (
            "etc/jupyter/jupyter_server_config.d",
            ["jupyter-config/jupyter_server_config.d/makana_model.json"],
        ),
        (
            "share/jupyter/nbextensions/makana_model",
            [
                "makana_model/nbextension/main.js",
                "makana_model/nbextension/README.md",
                "makana_model/nbextension/jupytext_menu.png",
                "makana_model/nbextension/makanamodel.yaml",
            ],
        ),
    ]
else:
    # Install labextension using jupyter_packaging
    from jupyter_packaging import (
        combine_commands,
        create_cmdclass,
        ensure_targets,
        install_npm,
    )

    lab_path = path.join(this_directory, "makana_model", "labextension")
    nb_path = path.join(this_directory, "makana_model", "nbextension")

    jupyter_config_path = path.join(this_directory, "jupyter-config")
    notebook_config_path = path.join(jupyter_config_path, "jupyter_notebook_config.d")
    jupyter_server_config_path = path.join(
        jupyter_config_path, "jupyter_server_config.d"
    )
    nbconfig_path = path.join(jupyter_config_path, "nbconfig", "notebook.d")

    data_files_spec = [
        # Install nbextension
        ("share/jupyter/nbextensions/makana_model", nb_path, "**"),
        ("share/jupyter/nbextensions/makana_model", nbconfig_path, "makana_model.json"),
        # Install config files
        (
            "etc/jupyter/jupyter_server_config.d",
            jupyter_server_config_path,
            "makana_model.json",
        ),
        (
            "etc/jupyter/jupyter_notebook_config.d",
            notebook_config_path,
            "makana_model.json",
        ),
        ("etc/jupyter/nbconfig/notebook.d", nbconfig_path, "makana_model.json"),
        ("share/jupyter/labextensions/%s" % labext_name, str(lab_path.relative_to(HERE)), "**"),
        ("share/jupyter/labextensions/%s" % labext_name, str("."), "install.json"),
    ]
    package_data_spec = {"makana_model": ["nbextension/**"]}

    # Representative files that should exist after a successful build
    jstargets = [
        str(lab_path / "package.json"),
        str(lab_path / "static/style.js")
    ]

    cmdclass = create_cmdclass(
        "jsdeps",
        package_data_spec=package_data_spec,
        data_files_spec=data_files_spec,
    )

    cmdclass["jsdeps"] = combine_commands(
        install_npm(
            path.join(this_directory, "makana_model", "labextension"),
            build_cmd="build:prod",
            npm=["jlpm"],
        ),
        ensure_targets(jstargets),
    )
    setup_args["cmdclass"] = cmdclass
    
# try:
#     from jupyter_packaging import (
#         wrap_installers,
#         npm_builder,
#         get_data_files
#     )
#     post_develop = npm_builder(
#         build_cmd="install:extension", source_dir="src", build_dir=lab_path
#     )
#     setup_args["cmdclass"] = wrap_installers(post_develop=post_develop, ensured_targets=ensured_targets)
#     setup_args["data_files"] = get_data_files(data_files_spec)
# except ImportError as e:
#     import logging
#     logging.basicConfig(format="%(levelname)s: %(message)s")
#     logging.warning("Build tool `jupyter-packaging` is missing. Install it with pip or conda.")
#     if not ("--name" in sys.argv or "--version" in sys.argv):
#         raise e

if __name__ == "__main__":
    setuptools.setup(**setup_args)
