"""Functions and classes for parsing Compressed List data structures."""

import numpy as np

from .generics import _dispatcher
from .rdsutils import get_class

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"


def read_partitioning_by_end(robject: dict, **kwargs):
    """Read an partioning by end object.

    Args:
        robject:
            Dictionary containing parsed partioning by end object.

        **kwargs:
            Additional arguments.

    Returns:
       A vector containing the partitions.
    """
    _cls = get_class(robject)

    if _cls not in ["PartitioningByEnd"]:
        raise RuntimeError(f"`robject` does not contain not a `PartitioningByEnd` object, contains `{_cls}`.")

    ends = _dispatcher(robject["attributes"]["end"], **kwargs)

    from compressed_lists import Partitioning

    return Partitioning(ends=np.asarray(ends))


def read_compressed_integer_list(robject: dict, **kwargs):
    """Read an R compressed list.

    Args:
        robject:
            Dictionary containing parsed compressed list.

        **kwargs:
            Additional arguments.

    Returns:
       A `CompressedList` from the 'compressed_lists' package.
    """
    _cls = get_class(robject)

    if _cls not in ["CompressedIntegerList"]:
        raise RuntimeError(f"`robject` does not contain not a compressed integer list object, contains `{_cls}`.")

    if "unlistData" not in robject["attributes"]:
        raise ValueError("Object does not contain unlistData, is it really a `compressedList`?")
    unlist_data = _dispatcher(robject["attributes"]["unlistData"], **kwargs)

    print("unlist_data", unlist_data)

    element_metadata = None
    if "elementMetadata" in robject["attributes"]:
        element_metadata = _dispatcher(robject["attributes"]["elementMetadata"], **kwargs)

    print("element_metadata", element_metadata)

    metadata = None
    if "metadata" in robject["attributes"]:
        metadata = _dispatcher(robject["attributes"]["metadata"], **kwargs)

    print("metadata", metadata)

    partition = None
    if "partitioning" in robject["attributes"]:
        partition = _dispatcher(robject["attributes"]["partitioning"], **kwargs)

    print("partition", partition)

    from compressed_lists import CompressedIntegerList

    return CompressedIntegerList(
        unlist_data=unlist_data, partitioning=partition, element_metadata=element_metadata, metadata=metadata
    )
