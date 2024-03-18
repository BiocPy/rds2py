from biocutils import BooleanList, FloatList, IntegerList, StringList

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"


def _extract_names(robject: dict):
    _names = None
    if "attributes" in robject and robject["attributes"] is not None:
        if "names" in robject["attributes"]:
            _names = list(parse_string_vector(robject["attributes"]["names"]))

    return _names


def parse_boolean_vector(robject: dict):
    _names = _extract_names(robject)

    obj = BooleanList(robject["data"], names=_names)
    return obj


def parse_integer_vector(robject: dict, **kwargs):
    _names = _extract_names(robject)

    obj = IntegerList(robject["data"], names=_names)
    return obj


def parse_string_vector(robject: dict, **kwargs):
    _names = _extract_names(robject)

    obj = StringList(robject["data"], names=_names)
    return obj


def parse_double_vector(robject: dict, **kwargs):
    _names = _extract_names(robject)

    obj = FloatList(robject["data"], names=_names)
    return obj
