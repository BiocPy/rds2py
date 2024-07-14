from biocframe import BiocFrame
from genomicranges import GenomicRanges, GenomicRangesList, SeqInfo
from iranges import IRanges

from .parser import get_class
from .pdf import as_pandas_from_dframe

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"


def as_granges(robj):
    """Parse an R object as a :py:class:`~genomicranges.GenomicRanges.GenomicRanges`.

    Args:
        robj:
            Object parsed from the `RDS` file.

            Usually the result of :py:func:`~rds2py.parser.read_rds`.

    Returns:
        A ``GenomicRanges`` object.
    """
    _cls = get_class(robj)

    if _cls not in ["GenomicRanges", "GRanges"]:
        raise TypeError(f"obj is not genomic ranges, but is `{_cls}`.")

    _range_start = robj["attributes"]["ranges"]["attributes"]["start"]["data"]
    _range_width = robj["attributes"]["ranges"]["attributes"]["width"]["data"]
    _range_names = None
    if "NAMES" in robj["attributes"]["ranges"]["attributes"]:
        _range_names = robj["attributes"]["ranges"]["attributes"]["NAMES"]["data"]
    _ranges = IRanges(_range_start, _range_width, names=_range_names)

    _seqnames = _as_list(robj["attributes"]["seqnames"])

    _strands = robj["attributes"]["strand"]
    _fstrand = None
    if "attributes" in _strands:
        _lengths = _strands["attributes"]["lengths"]["data"]
        _factors = _strands["attributes"]["values"]["data"]
        _levels = _strands["attributes"]["values"]["attributes"]["levels"]["data"]
        _strds = [_levels[x - 1] for x in _factors]
        _fstrand = []
        for i, x in enumerate(_lengths):
            _fstrand.extend([_strds[i]] * x)

    _seqinfo_seqnames = robj["attributes"]["seqinfo"]["attributes"]["seqnames"]["data"]
    _seqinfo_seqlengths = robj["attributes"]["seqinfo"]["attributes"]["seqlengths"][
        "data"
    ]
    _seqinfo_is_circular = robj["attributes"]["seqinfo"]["attributes"]["is_circular"][
        "data"
    ]
    _seqinfo_genome = robj["attributes"]["seqinfo"]["attributes"]["genome"]["data"]
    _seqinfo = SeqInfo(
        seqnames=_seqinfo_seqnames,
        seqlengths=[None if x == -2147483648 else int(x) for x in _seqinfo_seqlengths],
        is_circular=[
            None if x == -2147483648 else bool(x) for x in _seqinfo_is_circular
        ],
        genome=_seqinfo_genome,
    )

    _mcols = BiocFrame.from_pandas(
        as_pandas_from_dframe(robj["attributes"]["elementMetadata"])
    )

    _gr_names = None
    if "NAMES" in robj["attributes"]:
        _gr_names = robj["attributes"]["NAMES"]["data"]

    return GenomicRanges(
        seqnames=_seqnames,
        ranges=_ranges,
        strand=_fstrand,
        names=_gr_names,
        mcols=_mcols,
        seqinfo=_seqinfo,
    )


def _as_list(robj):
    """Parse an R object as a :py:class:`~list`.

    Args:
        robj:
            Object parsed from the `RDS` file.

            Usually the result of :py:func:`~rds2py.parser.read_rds`.

    Returns:
        A ``list`` of the Rle class.
    """
    _cls = get_class(robj)

    if _cls not in ["Rle"]:
        raise TypeError(f"obj is not Rle, but is `{_cls}`.")

    _attr_vals = robj["attributes"]
    _data = _attr_vals["values"]["data"].tolist()
    if "attributes" in _attr_vals["values"]:
        if "levels" in _attr_vals["values"]["attributes"]:
            _levels_data = _attr_vals["values"]["attributes"]["levels"]["data"]
            _data = [_levels_data[x - 1] for x in _data]

    if "lengths" in _attr_vals:
        _final = []
        _lengths = _attr_vals["lengths"]["data"]

        for idx, lg in enumerate(_lengths.tolist()):
            _final.extend([_data[idx]] * lg)

        _data = _final

    return _data


def as_granges_list(robj):
    """Parse an R object as a :py:class:`~genomicranges.GenomicRangesList.GenomicRangesList`.

    Args:
        robj:
            Object parsed from the `RDS` file.

            Usually the result of :py:func:`~rds2py.parser.read_rds`.

    Returns:
        A ``GenomicRangesList`` object.
    """

    _cls = get_class(robj)

    if _cls not in ["CompressedGRangesList", "GRangesList"]:
        raise TypeError(f"obj is not genomic ranges list, but is `{_cls}`.")

    _gre = as_granges(robj["attributes"]["unlistData"])

    _groups = robj["attributes"]["partitioning"]["attributes"]["NAMES"]["data"]
    _partitionends = robj["attributes"]["partitioning"]["attributes"]["end"]["data"]

    _grelist = []

    current = 0
    for _pend in _partitionends:
        _grelist.append(_gre[current:_pend])
        current = _pend

    return GenomicRangesList(ranges=_grelist, names=_groups)
