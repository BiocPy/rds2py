"""Functions for parsing Bioconductor GenomicRanges objects.

This module provides parsers for converting Bioconductor's GenomicRanges and GenomicRangesList objects into their Python
equivalents, preserving all genomic coordinates and associated metadata.
"""

from .generics import _dispatcher
from .rdsutils import get_class

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"


def read_genomic_ranges(robject: dict, **kwargs):
    """Convert an R `GenomicRanges` object to a Python :py:class:`~genomicranges.GenomicRanges` object.

    Args:
        robject:
            Dictionary containing parsed `GenomicRanges` data.

        **kwargs:
            Additional arguments.

    Returns:
        A Python `GenomicRanges` object containing genomic intervals
        with associated annotations.
    """

    from genomicranges import GenomicRanges, SeqInfo
    from iranges import IRanges

    _cls = get_class(robject)

    if _cls not in ["GenomicRanges", "GRanges"]:
        raise TypeError(f"obj is not 'GenomicRanges', but is `{_cls}`.")

    _range_start = _dispatcher(robject["attributes"]["ranges"]["attributes"]["start"], **kwargs)
    _range_width = _dispatcher(robject["attributes"]["ranges"]["attributes"]["width"], **kwargs)
    _range_names = None
    if "NAMES" in robject["attributes"]["ranges"]["attributes"]:
        _tmp_names = robject["attributes"]["ranges"]["attributes"]["NAMES"]
        _range_names = _dispatcher(_tmp_names, **kwargs)
        if _range_names is not None:
            _range_names = list(_range_names)

    _ranges = IRanges(_range_start, _range_width, names=_range_names)

    _strands = _dispatcher(robject["attributes"]["strand"], **kwargs)
    _seqnames = _dispatcher(robject["attributes"]["seqnames"], **kwargs)
    _seqinfo_seqnames = _dispatcher(robject["attributes"]["seqinfo"]["attributes"]["seqnames"], **kwargs)
    _seqinfo_seqlengths = _dispatcher(robject["attributes"]["seqinfo"]["attributes"]["seqlengths"], **kwargs)
    _seqinfo_is_circular = _dispatcher(robject["attributes"]["seqinfo"]["attributes"]["is_circular"], **kwargs)
    _seqinfo_genome = _dispatcher(robject["attributes"]["seqinfo"]["attributes"]["genome"], **kwargs)
    _seqinfo = SeqInfo(
        seqnames=_seqinfo_seqnames,
        seqlengths=_seqinfo_seqlengths,
        is_circular=_seqinfo_is_circular,
        genome=_seqinfo_genome,
    )
    _mcols = _dispatcher(robject["attributes"]["elementMetadata"], **kwargs)

    _gr_names = None
    if "NAMES" in robject["attributes"]:
        _tmp_names = robject["attributes"]["NAMES"]
        _gr_names = None if _tmp_names is None else _dispatcher(_tmp_names, **kwargs)

    return GenomicRanges(
        seqnames=_seqnames,
        ranges=_ranges,
        strand=_strands,
        names=_gr_names,
        mcols=_mcols,
        seqinfo=_seqinfo,
    )


def read_granges_list(robject: dict, **kwargs):
    """Convert an R `CompressedGenomicRangesList` object to a Python :py:class:`~genomicranges.grangeslist.CompressedGenomicRangesList`.

    Args:
        robject:
            Dictionary containing parsed CompressedGenomicRangesList data.

        **kwargs:
            Additional arguments.

    Returns:
        A Python `CompressedGenomicRangesList` object containing containing multiple
        `GenomicRanges` objects.
    """

    from compressed_lists import Partitioning
    from genomicranges import CompressedGenomicRangesList

    _cls = get_class(robject)

    if _cls not in ["CompressedGRangesList", "GRangesList"]:
        raise TypeError(f"`robject` is not genomic ranges list, but is `{_cls}`.")

    _gre = _dispatcher(robject["attributes"]["unlistData"], **kwargs)

    _groups = None
    if "NAMES" in robject["attributes"]["partitioning"]["attributes"]:
        _tmp_names = robject["attributes"]["partitioning"]["attributes"]["NAMES"]
        _groups = None if _tmp_names is None else _dispatcher(_tmp_names, **kwargs)

    _partitionends = _dispatcher(robject["attributes"]["partitioning"]["attributes"]["end"], **kwargs)

    _part_obj = Partitioning(ends=_partitionends, names=_groups)

    element_metadata = None
    if "elementMetadata" in robject["attributes"]:
        element_metadata = _dispatcher(robject["attributes"]["elementMetadata"], **kwargs)

    metadata = None
    if "metadata" in robject["attributes"]:
        metadata = _dispatcher(robject["attributes"]["metadata"], **kwargs)

    return CompressedGenomicRangesList(
        unlist_data=_gre, partitioning=_part_obj, element_metadata=element_metadata, metadata=metadata
    )
