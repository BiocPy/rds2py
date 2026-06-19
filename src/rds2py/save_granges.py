from typing import Optional

from biocutils.package_utils import is_package_installed

from .generics import save_rds

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"


if is_package_installed("genomicranges", verbose=True):
    from genomicranges import CompressedGenomicRangesList, GenomicRanges, SeqInfo

    @save_rds.register(SeqInfo)
    def _save_rds_seqinfo(x: SeqInfo, path: Optional[str] = None):
        from .lib_rds_parser import write_rds as _write_rds_native

        def _get(obj, name):
            if hasattr(obj, f"get_{name}"):
                return getattr(obj, f"get_{name}")()
            return getattr(obj, name, None)

        converted = {
            "seqnames": save_rds(_get(x, "seqnames")),
            "seqlengths": save_rds(_get(x, "seqlengths")),
            "is_circular": save_rds(_get(x, "is_circular")),
            "genome": save_rds(_get(x, "genome")),
        }

        if path is not None:
            _write_rds_native(converted, path)

        return converted

    @save_rds.register(GenomicRanges)
    def _save_rds_genomicranges(x: GenomicRanges, path: Optional[str] = None):
        from .lib_rds_parser import write_rds as _write_rds_native

        def _get(obj, name):
            if hasattr(obj, f"get_{name}"):
                return getattr(obj, f"get_{name}")()
            return getattr(obj, name, None)

        converted = {
            "seqnames": save_rds(_get(x, "seqnames")),
            "ranges": save_rds(_get(x, "ranges")),
            "strand": save_rds(_get(x, "strand")),
            "seqinfo": save_rds(_get(x, "seqinfo")),
            "mcols": save_rds(_get(x, "mcols")),
            "metadata": save_rds(_get(x, "metadata")),
        }

        if path is not None:
            _write_rds_native(converted, path)

        return converted

    @save_rds.register(CompressedGenomicRangesList)
    def _save_rds_cgrl(x: CompressedGenomicRangesList, path: Optional[str] = None):
        from .lib_rds_parser import write_rds as _write_rds_native

        def _get(obj, name):
            if hasattr(obj, f"get_{name}"):
                return getattr(obj, f"get_{name}")()
            return getattr(obj, name, None)

        converted = {
            "unlist_data": save_rds(_get(x, "unlist_data")),
            "partitioning": save_rds(_get(x, "partitioning")),
            "metadata": save_rds(_get(x, "metadata")),
        }

        if path is not None:
            _write_rds_native(converted, path)

        return converted
