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
            "type": "S4",
            "class_name": "SeqInfo",
            "package_name": "GenomeInfoDb",
            "attributes": {
                "seqnames": save_rds(_get(x, "seqnames")),
                "seqlengths": save_rds(_get(x, "seqlengths")),
                "is_circular": save_rds(_get(x, "is_circular")),
                "genome": save_rds(_get(x, "genome")),
            },
        }

        if path is not None:
            _write_rds_native(converted, path)

        return converted

    @save_rds.register(GenomicRanges)
    def _save_rds_genomicranges(x: GenomicRanges, path: Optional[str] = None):
        import numpy as np

        from .lib_rds_parser import write_rds as _write_rds_native

        def _get(obj, name):
            if hasattr(obj, f"get_{name}"):
                return getattr(obj, f"get_{name}")()
            return getattr(obj, name, None)

        # Map strand codes: 1 -> 1 (+), -1 -> 2 (-), 0 -> 3 (*)
        strand_data = _get(x, "strand")
        mapped_strand_codes = np.zeros_like(strand_data, dtype=np.int32)
        mapped_strand_codes[strand_data == 1] = 1
        mapped_strand_codes[strand_data == -1] = 2
        mapped_strand_codes[strand_data == 0] = 3

        converted_strand = {
            "type": "integer",
            "data": list(mapped_strand_codes),
            "attributes": {
                "class": {"type": "string", "data": ["factor"]},
                "levels": {"type": "string", "data": ["+", "-", "*"]},
            },
        }

        # R expects seqnames to be a factor vector
        seq_names = _get(x, "seqnames")
        seq_info_names = list(x.seqinfo.seqnames)
        seq_codes = [seq_info_names.index(name) + 1 for name in seq_names]
        converted_seqnames = {
            "type": "integer",
            "data": seq_codes,
            "attributes": {
                "class": {"type": "string", "data": ["factor"]},
                "levels": {"type": "string", "data": seq_info_names},
            },
        }

        converted = {
            "type": "S4",
            "class_name": "GRanges",
            "package_name": "GenomicRanges",
            "attributes": {
                "seqnames": converted_seqnames,
                "ranges": save_rds(_get(x, "ranges")),
                "strand": converted_strand,
                "seqinfo": save_rds(_get(x, "seqinfo")),
                "elementMetadata": save_rds(_get(x, "mcols")),
                "elementType": {"type": "string", "data": ["ANY"]},
                "metadata": save_rds(_get(x, "metadata")),
                "NAMES": save_rds(_get(x, "names")),
            },
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
            "type": "S4",
            "class_name": "CompressedGRangesList",
            "package_name": "GenomicRanges",
            "attributes": {
                "unlistData": save_rds(_get(x, "unlist_data")),
                "partitioning": save_rds(_get(x, "partitioning")),
                "elementMetadata": save_rds(_get(x, "element_metadata")),
                "elementType": {"type": "string", "data": ["GRanges"]},
                "metadata": save_rds(_get(x, "metadata")),
            },
        }

        if path is not None:
            _write_rds_native(converted, path)

        return converted
