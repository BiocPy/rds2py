import rds2py
from rds2py.generics import _dispatcher

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"


def test_register_parser():
    @rds2py.register_parser("DummyRClass")
    def parse_dummy(robj, **kwargs):
        return {"coerced": True, "value": robj.get("data", None)}

    robj = {"type": "S4", "class_name": "DummyRClass", "data": 42}
    res = _dispatcher(robj)

    assert res == {"coerced": True, "value": 42}
