import json
from pathlib import Path

from ._version import __version__


HERE = Path(__file__).parent.resolve()


with (HERE / "labextension" / "package.json").open() as fid:
    data = json.load(fid)


def _jupyter_labextension_paths():
    return [{
        "src": "labextension",
        "dest": data["name"]
    }]

# Jupyter Extension points
def _jupyter_nbextension_paths():
    return [dict(
        section="notebook",
        # the path is relative to the `makana_service` directory
        src="nbextension",
        # directory in the `nbextension/` namespace
        dest="makana_model",
        # _also_ in the `nbextension/` namespace
        require="makana_model/main")]