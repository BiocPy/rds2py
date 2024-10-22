from genomicranges import GenomicRanges, GenomicRangesList, SeqInfo
from iranges import IRanges

from .generics import _dispatcher
from .rdsutils import get_class

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"


def parse_genomic_ranges(robj):
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

    _range_start = _dispatcher(robj["attributes"]["ranges"]["attributes"]["start"])
    _range_width = _dispatcher(robj["attributes"]["ranges"]["attributes"]["width"])
    _range_names = None
    if "NAMES" in robj["attributes"]["ranges"]["attributes"]:
        _range_names = _dispatcher(robj["attributes"]["ranges"]["attributes"]["NAMES"])

    _ranges = IRanges(_range_start, _range_width, names=list(_range_names))

    _strands = _dispatcher(robj["attributes"]["strand"])
    _seqnames = _dispatcher(robj["attributes"]["seqnames"])
    _seqinfo_seqnames = _dispatcher(
        robj["attributes"]["seqinfo"]["attributes"]["seqnames"]
    )
    _seqinfo_seqlengths = _dispatcher(
        robj["attributes"]["seqinfo"]["attributes"]["seqlengths"]
    )
    _seqinfo_is_circular = _dispatcher(
        robj["attributes"]["seqinfo"]["attributes"]["is_circular"]
    )
    _seqinfo_genome = _dispatcher(robj["attributes"]["seqinfo"]["attributes"]["genome"])
    _seqinfo = SeqInfo(
        seqnames=_seqinfo_seqnames,
        seqlengths=[None if x == -2147483648 else int(x) for x in _seqinfo_seqlengths],
        is_circular=[
            None if x == -2147483648 else bool(x) for x in _seqinfo_is_circular
        ],
        genome=_seqinfo_genome,
    )
    _mcols = _dispatcher(robj["attributes"]["elementMetadata"])

    _gr_names = None
    if "NAMES" in robj["attributes"]:
        _gr_names = _dispatcher(robj["attributes"]["NAMES"])

    print("starts here", _seqnames, _ranges, _strands, _gr_names, _mcols, _seqinfo)

    return GenomicRanges(
        seqnames=_seqnames,
        ranges=_ranges,
        strand=_strands,
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
