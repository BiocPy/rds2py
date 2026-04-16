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


def _get_compressed_common_attrs(robject, **kwargs):
    if "unlistData" not in robject["attributes"]:
        raise ValueError("Object does not contain unlistData, is it really a `CompressedList`?")
    unlist_data = _dispatcher(robject["attributes"]["unlistData"], **kwargs)

    element_metadata = None
    if "elementMetadata" in robject["attributes"]:
        element_metadata = _dispatcher(robject["attributes"]["elementMetadata"], **kwargs)

    metadata = None
    if "metadata" in robject["attributes"]:
        metadata = _dispatcher(robject["attributes"]["metadata"], **kwargs)

    partition = None
    if "partitioning" in robject["attributes"]:
        partition = _dispatcher(robject["attributes"]["partitioning"], **kwargs)

    return unlist_data, element_metadata, metadata, partition


def read_compressed_integer_list(robject: dict, **kwargs):
    """Read an R compressed integer list.

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

    unlist_data, element_metadata, metadata, partition = _get_compressed_common_attrs(robject=robject, **kwargs)

    from compressed_lists import CompressedIntegerList

    return CompressedIntegerList(
        unlist_data=unlist_data, partitioning=partition, element_metadata=element_metadata, metadata=metadata
    )


def read_compressed_string_list(robject: dict, **kwargs):
    """Read an R compressed string/character list.

    Args:
        robject:
            Dictionary containing parsed compressed list.

        **kwargs:
            Additional arguments.

    Returns:
       A `CompressedList` from the 'compressed_lists' package.
    """
    _cls = get_class(robject)

    if _cls not in ["CompressedCharacterList"]:
        raise RuntimeError(f"`robject` does not contain not a compressed string list object, contains `{_cls}`.")

    unlist_data, element_metadata, metadata, partition = _get_compressed_common_attrs(robject=robject, **kwargs)

    from compressed_lists import CompressedCharacterList

    return CompressedCharacterList(
        unlist_data=unlist_data, partitioning=partition, element_metadata=element_metadata, metadata=metadata
    )


def read_compressed_character_list(robject: dict, **kwargs):
    """Read an R compressed string/character list.

    Args:
        robject:
            Dictionary containing parsed compressed string list.

        **kwargs:
            Additional arguments.

    Returns:
       A `CompressedList` from the 'compressed_lists' package.
    """
    return read_compressed_string_list(robject, **kwargs)


def read_compressed_boolean_list(robject: dict, **kwargs):
    """Read an R compressed boolean list.

    Args:
        robject:
            Dictionary containing parsed compressed list.

        **kwargs:
            Additional arguments.

    Returns:
       A `CompressedList` from the 'compressed_lists' package.
    """
    _cls = get_class(robject)

    if _cls not in ["CompressedLogicalList"]:
        raise RuntimeError(f"`robject` does not contain not a compressed boolean list object, contains `{_cls}`.")

    unlist_data, element_metadata, metadata, partition = _get_compressed_common_attrs(robject=robject, **kwargs)

    from compressed_lists import CompressedBooleanList

    return CompressedBooleanList(
        unlist_data=unlist_data, partitioning=partition, element_metadata=element_metadata, metadata=metadata
    )


def read_compressed_float_list(robject: dict, **kwargs):
    """Read an R compressed float list.

    Args:
        robject:
            Dictionary containing parsed compressed list.

        **kwargs:
            Additional arguments.

    Returns:
       A `CompressedList` from the 'compressed_lists' package.
    """
    _cls = get_class(robject)

    if _cls not in ["CompressedNumericList"]:
        raise RuntimeError(f"`robject` does not contain not a compressed float list object, contains `{_cls}`.")

    unlist_data, element_metadata, metadata, partition = _get_compressed_common_attrs(robject=robject, **kwargs)

    from compressed_lists import CompressedFloatList

    return CompressedFloatList(
        unlist_data=unlist_data, partitioning=partition, element_metadata=element_metadata, metadata=metadata
    )


def read_compressed_frame_list(robject: dict, **kwargs):
    """Read an R compressed dataframe list.

    Args:
        robject:
            Dictionary containing parsed compressed list.

        **kwargs:
            Additional arguments.

    Returns:
       A `CompressedList` from the 'compressed_lists' package.
    """
    _cls = get_class(robject)

    if _cls not in ["CompressedSplitDataFrameList", "CompressedSplitDFrameList"]:
        raise RuntimeError(f"`robject` does not contain not a compressed dataframe list object, contains `{_cls}`.")

    unlist_data, element_metadata, metadata, partition = _get_compressed_common_attrs(robject=robject, **kwargs)

    from compressed_lists import CompressedSplitBiocFrameList

    return CompressedSplitBiocFrameList(
        unlist_data=unlist_data, partitioning=partition, element_metadata=element_metadata, metadata=metadata
    )
