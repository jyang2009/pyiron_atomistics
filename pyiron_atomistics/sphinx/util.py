__author__ = "Christoph Freysoldt"
__copyright__ = (
    "Copyright 2022, Max-Planck-Institut für Eisenforschung GmbH - "
    "Computational Materials Design (CM) Department"
)
__version__ = "1.0"
__maintainer__ = "Christoph Freysoldt"
__email__ = "freysoldt@mpie.de"
__status__ = "development"
__date__ = "Oct 15, 2022"

from threading import Lock
import json
import warnings
import os.path
import subprocess

from pyiron_base import Settings

_sxversion_lock = Lock ()
_sxversions = None

def sxversions(refresh=False):
    """ Get available SPHInX versions
        returns: a dict
    """
    global _sxversions
    if not refresh and _sxversions is dict:
        return _sxversions

    _sxversion_lock.acquire ()
    def do_update(newfile):
        for v in sxv.keys ():
            if v in version_origin.keys () and _sxversions[v] != sxv[v]:
                warnings.warn ("Overriding sxversion '{}' from {} with the one from {}".format(
                   v, version_origin[v], newfile))
            version_origin[v] = newfile
        _sxversions.update (sxv)

    try:
        if refresh: _sxversions = None
        if _sxversions is None:
            _sxversions = dict ()
            version_origin = dict ()
            for p in Settings ().resource_paths:
                jsonfile=os.path.join (p, "sphinx", "sxversions.json")
                if os.path.exists (jsonfile):
                    sxv = json.load (open(jsonfile))
                    if isinstance(sxv, dict):
                        do_update(jsonfile)
                    else:
                        warnings.warn ("Failed to parse ".jsonfile)

                jsonscript=os.path.join(p, "sphinx", "sxversions.sh")
                if os.path.exists (jsonscript):
                    sxv = json.loads (
                        subprocess.run (jsonscript,
                                        text=True,
                                        stdout=subprocess.PIPE
                                       ).stdout
                        )
                    if isinstance(sxv, dict):
                        do_update(jsonscript)
                    else:
                        warnings.warn ("Failed to parse output from ".jsonscript)
    except:
        _sxversion_lock.release ()
        raise
    _sxversion_lock.release ()
    return _sxversions
