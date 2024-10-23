from genomicranges import GenomicRanges, GenomicRangesList, SeqInfo
from iranges import IRanges

from .generics import _dispatcher
from .rdsutils import get_class

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"


def parse_genomic_ranges(robject):
    """Parse an R object as a :py:class:`~genomicranges.GenomicRanges.GenomicRanges`.

    Args:
        robject:
            Object parsed from the `RDS` file.

            Usually the result of :py:func:`~rds2py.generics.read_rds`.

    Returns:
        A ``GenomicRanges`` object.
    """
    _cls = get_class(robject)

    if _cls not in ["GenomicRanges", "GRanges"]:
        raise TypeError(f"obj is not 'GenomicRanges', but is `{_cls}`.")

    _range_start = _dispatcher(robject["attributes"]["ranges"]["attributes"]["start"])
    _range_width = _dispatcher(robject["attributes"]["ranges"]["attributes"]["width"])
    _range_names = None
    if "NAMES" in robject["attributes"]["ranges"]["attributes"]:
        _tmp_names = robject["attributes"]["ranges"]["attributes"]["NAMES"]
        _range_names = _dispatcher(_tmp_names)
        if _range_names is not None:
            _range_names = list(_range_names)

    _ranges = IRanges(_range_start, _range_width, names=_range_names)

    _strands = _dispatcher(robject["attributes"]["strand"])
    _seqnames = _dispatcher(robject["attributes"]["seqnames"])
    _seqinfo_seqnames = _dispatcher(
        robject["attributes"]["seqinfo"]["attributes"]["seqnames"]
    )
    _seqinfo_seqlengths = _dispatcher(
        robject["attributes"]["seqinfo"]["attributes"]["seqlengths"]
    )
    print("SEQLENGTHS", _seqinfo_seqlengths)
    _seqinfo_is_circular = _dispatcher(
        robject["attributes"]["seqinfo"]["attributes"]["is_circular"]
    )
    _seqinfo_genome = _dispatcher(
        robject["attributes"]["seqinfo"]["attributes"]["genome"]
    )
    _seqinfo = SeqInfo(
        seqnames=_seqinfo_seqnames,
        seqlengths=_seqinfo_seqlengths,
        is_circular=_seqinfo_is_circular,
        genome=_seqinfo_genome,
    )
    _mcols = _dispatcher(robject["attributes"]["elementMetadata"])

    _gr_names = None
    if "NAMES" in robject["attributes"]:
        _tmp_names = robject["attributes"]["NAMES"]
        _gr_names = None if _tmp_names is None else _dispatcher(_tmp_names)

    return GenomicRanges(
        seqnames=_seqnames,
        ranges=_ranges,
        strand=_strands,
        names=_gr_names,
        mcols=_mcols,
        seqinfo=_seqinfo,
    )


def parse_granges_list(robject):
    """Parse an R object as a :py:class:`~genomicranges.GenomicRangesList.GenomicRangesList`.

    Args:
        robject:
            Object parsed from the `RDS` file.

            Usually the result of :py:func:`~rds2py.generics.read_rds`.

    Returns:
        A ``GenomicRangesList`` object.
    """

    _cls = get_class(robject)

    if _cls not in ["CompressedGRangesList", "GRangesList"]:
        raise TypeError(f"`robject` is not genomic ranges list, but is `{_cls}`.")

    _gre = _dispatcher(robject["attributes"]["unlistData"])

    _groups = None
    if "NAMES" in robject["attributes"]["partitioning"]["attributes"]:
        _tmp_names = robject["attributes"]["partitioning"]["attributes"]["NAMES"]
        _groups = None if _tmp_names is None else _dispatcher(_tmp_names)

    _partitionends = _dispatcher(
        robject["attributes"]["partitioning"]["attributes"]["end"]
    )

    _grelist = []

    current = 0
    for _pend in _partitionends:
        _grelist.append(_gre[current:_pend])
        current = _pend

    return GenomicRangesList(ranges=_grelist, names=_groups)
