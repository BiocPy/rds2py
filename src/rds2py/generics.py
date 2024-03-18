from functools import singledispatch
from importlib import import_module

from .rds_interface import get_class, load_rds

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"

REGISTRY = {}


@singledispatch
def save_rds(x, path: str):
    """Save a Python object as RDS file.

    Args:
        x:
            Object to save.

        path:
            Path to save the object.
    """
    raise NotImplementedError(
        f"No `save_rds` method implemented for '{type(x).__name__}' objects."
    )


def read_rds(path: str, **kwargs):
    """Read an RDS file as Python object.

    Args:
        path:
            Path to the RDS file.

        kwargs:
            Further arguments, passed to individual methods.

    Returns:
        Some kind of object.
    """
    _robj = load_rds(path=path)
    _class_name = get_class(_robj)

    if _class_name not in REGISTRY:
        raise NotImplementedError(
            "no `read_rds` method implemented for '{_class_name}' objects."
        )

    # from Aaron's dolomite-base package
    command = REGISTRY[_class_name]
    if isinstance(command, str):
        first_period = command.find(".")
        mod = import_module(command[:first_period])
        command = getattr(mod, command[first_period + 1 :])
        REGISTRY[_class_name] = command

    return command(path, **kwargs)