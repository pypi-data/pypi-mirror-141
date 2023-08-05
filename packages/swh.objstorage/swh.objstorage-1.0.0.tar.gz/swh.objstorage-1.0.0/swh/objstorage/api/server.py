# Copyright (C) 2015-2022  The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

import contextlib
import functools
import logging
import os

from flask import request

from swh.core.api import RPCServerApp
from swh.core.api import encode_data_server as encode_data
from swh.core.api import error_handler
from swh.core.config import read as config_read
from swh.core.statsd import statsd
from swh.model import hashutil
from swh.objstorage.exc import Error, ObjNotFoundError
from swh.objstorage.factory import get_objstorage as get_swhobjstorage
from swh.objstorage.interface import ObjStorageInterface
from swh.objstorage.objstorage import DEFAULT_LIMIT


def timed(f):
    @functools.wraps(f)
    def w(*a, **kw):
        with statsd.timed(
            "swh_objstorage_request_duration_seconds", tags={"endpoint": f.__name__}
        ):
            return f(*a, **kw)

    return w


@contextlib.contextmanager
def timed_context(f_name):
    with statsd.timed(
        "swh_objstorage_request_duration_seconds", tags={"endpoint": f_name}
    ):
        yield


def get_objstorage():
    global objstorage
    if not objstorage:
        objstorage = get_swhobjstorage(**app.config["objstorage"])

    return objstorage


class ObjStorageServerApp(RPCServerApp):
    client_exception_classes = (ObjNotFoundError, Error)
    method_decorators = [timed]

    def pre_add(self, kw):
        """Called before the 'add' method."""
        statsd.increment(
            "swh_objstorage_in_bytes_total",
            len(kw["content"]),
            tags={"endpoint": "add_bytes"},
        )

    def post_get(self, ret, kw):
        """Called after the 'get' method."""
        statsd.increment(
            "swh_objstorage_out_bytes_total", len(ret), tags={"endpoint": "get_bytes"}
        )


app = ObjStorageServerApp(
    __name__, backend_class=ObjStorageInterface, backend_factory=get_objstorage,
)
objstorage = None


@app.errorhandler(Error)
def argument_error_handler(exception):
    return error_handler(exception, encode_data, status_code=400)


@app.errorhandler(Exception)
def my_error_handler(exception):
    return error_handler(exception, encode_data)


@app.route("/")
@timed
def index():
    return "SWH Objstorage API server"


# Streaming methods


@app.route("/content/get_stream/<hex_id>")
def get_stream(hex_id):
    obj_id = hashutil.hash_to_bytes(hex_id)

    def generate():
        with timed_context("get_stream"):
            yield from objstorage.get_stream(obj_id, 2 << 20)

    return app.response_class(generate())


@app.route("/content")
def list_content():
    last_obj_id = request.args.get("last_obj_id")
    if last_obj_id:
        last_obj_id = bytes.fromhex(last_obj_id)
    limit = int(request.args.get("limit", DEFAULT_LIMIT))

    def generate():
        yield b""
        with timed_context("get_stream"):
            yield from objstorage.list_content(last_obj_id, limit=limit)

    return app.response_class(generate())


def load_and_check_config(config_file):
    """Check the minimal configuration is set to run the api or raise an
       error explanation.

    Args:
        config_file (str): Path to the configuration file to load

    Raises:
        Error if the setup is not as expected

    Returns:
        configuration as a dict

    """
    if not config_file:
        raise EnvironmentError("Configuration file must be defined")

    if not os.path.exists(config_file):
        raise FileNotFoundError("Configuration file %s does not exist" % (config_file,))

    cfg = config_read(config_file)
    return validate_config(cfg)


def validate_config(cfg):
    """Check the minimal configuration is set to run the api or raise an
       explanatory error.

    Args:
        cfg (dict): Loaded configuration.

    Raises:
        Error if the setup is not as expected

    Returns:
        configuration as a dict

    """
    if "objstorage" not in cfg:
        raise KeyError("Invalid configuration; missing objstorage config entry")

    missing_keys = []
    vcfg = cfg["objstorage"]
    if "cls" not in vcfg:
        raise KeyError("Invalid configuration; missing cls config entry")

    cls = vcfg["cls"]
    if cls == "pathslicing":
        # Backwards-compatibility: either get the deprecated `args` from the
        # objstorage config, or use the full config itself to check for keys
        args = vcfg.get("args", vcfg)
        for key in ("root", "slicing"):
            v = args.get(key)
            if v is None:
                missing_keys.append(key)

        if missing_keys:
            raise KeyError(
                "Invalid configuration; missing %s config entry"
                % (", ".join(missing_keys),)
            )

    return cfg


def make_app_from_configfile():
    """Load configuration and then build application to run

    """
    config_file = os.environ.get("SWH_CONFIG_FILENAME")
    app.config = load_and_check_config(config_file)
    handler = logging.StreamHandler()
    app.logger.addHandler(handler)
    return app


if __name__ == "__main__":
    print("Deprecated. Use swh-objstorage")
