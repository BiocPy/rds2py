from typing import Literal

from numpy import ndarray
from singlecellexperiment import SingleCellExperiment
from summarizedexperiment import SummarizedExperiment
from biocframe import BiocFrame

from .parser import get_class
from .pdf import as_pandas_from_data_frame, as_pandas_from_dframe

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"


def as_pandas(robj):
    """Parse an R object as a :py:class:`~pandas.DataFrame`.

    Currently supports ``DFrame`` or ``data.frame`` class objects from R.

    Args:
        robj:
            Object parsed from the `RDS` file.

            Usually the result of :py:func:`~rds2py.parser.read_rds`.

    Returns:
        A :py:class:`~pandas.DataFrame` containing the data from the R Object.
    """
    _cls = get_class(robj)

    if _cls == "DFrame":
        return as_pandas_from_dframe(robj)
    elif _cls == "data.frame":
        return as_pandas_from_data_frame(robj)
    else:
        raise TypeError(
            f"`robj` must be either a 'DFrame' or 'data.frame' but is {_cls}."
        )


def as_sparse_matrix(robj):
    """Parse an R object as a sparse matrix.

    Only supports reading of `dgCMatrix`, `dgRMatrix`, `dgTMatrix` marices.

    Args:
        robj:
            Object parsed from the `RDS` file.

            Usually the result of :py:func:`~rds2py.parser.read_rds`.

    Returns:
        A sparse matrix of the R object.
    """
    from scipy.sparse import csc_matrix, csr_matrix

    _cls = get_class(robj)

    if _cls not in ["dgCMatrix", "dgRMatrix", "dgTMatrix"]:
        raise TypeError(
            f"`robj` does not contain not a supported sparse matrix format, contains `{_cls}`."
        )

    if _cls == "dgCMatrix":
        return csc_matrix(
            (
                robj["attributes"]["x"]["data"],
                robj["attributes"]["i"]["data"],
                robj["attributes"]["p"]["data"],
            ),
            shape=tuple(robj["attributes"]["Dim"]["data"].tolist()),
        )

    if _cls == "dgRMatrix":
        return csr_matrix(
            (
                robj["attributes"]["x"]["data"],
                robj["attributes"]["i"]["data"],
                robj["attributes"]["p"]["data"],
            ),
            shape=tuple(robj["attributes"]["Dim"]["data"].tolist()),
        )

    if _cls == "dgTMatrix":
        return csr_matrix(
            (
                robj["attributes"]["x"]["data"],
                (
                    robj["attributes"]["i"]["data"],
                    robj["attributes"]["j"]["data"],
                ),
            ),
            shape=tuple(robj["attributes"]["Dim"]["data"].tolist()),
        )


def as_dense_matrix(robj, order: Literal["C", "F"] = "F") -> ndarray:
    """Parse an R object as a :py:class:`~numpy.ndarray`.

    Args:
        robj:
            Object parsed from the `RDS` file.

            Usually the result of :py:func:`~rds2py.parser.read_rds`.

        order:
            Row-major (**C**-style) or Column-major (**F**ortran-style)
            order.

            Defaults to "F".

    Returns:
        An ``ndarray`` of the R object.
    """
    _cls = get_class(robj)

    if order not in ["C", "F"]:
        raise ValueError("order must be either 'C' or 'F'.")

    if _cls not in ["densematrix"]:
        raise TypeError(f"obj is not a supported dense matrix format, but is `{_cls}`.")

    return ndarray(
        shape=tuple(robj["attributes"]["dim"]["data"].tolist()),
        dtype=robj["data"].dtype,
        buffer=robj["data"],
        order=order,
    )


def as_summarized_experiment(robj):
    """Parse an R object as a :py:class:`~singlecellexperiment.SingleCellExperiment.SingleCellExperiment` or
    :py:class:`~summarizedexperiment.SummarizedExperiment.SummarizedExperiment`.

    Note: This function demonstrates how to parse a complex RDS objects in Python and may not work for all
    scenarios.

    Args:
        robj:
            Object parsed from the `RDS` file.

            Usually the result of :py:func:`~rds2py.parser.read_rds`.

        order:
            Row-major (**C**-style) or Column-major (**F**ortran-style)
            order. Only used if the ``robj`` contains a :py:class:`~numpy.ndarray`.

            Defaults to "F".

    Returns:
        A `SummarizedExperiment` or
        `SingleCellExperiment` from the R object.
    """

    _cls = get_class(robj)

    if _cls not in ["SingleCellExperiment", "SummarizedExperiment"]:
        raise TypeError(
            "`robj` does not contain a `SingleCellExperiment` or `SummarizedExperiment`."
        )

    # parse assays  names
    robj_asys = {}
    assay_dims = None
    asy_names = robj["attributes"]["assays"]["attributes"]["data"]["attributes"][
        "listData"
    ]["attributes"]["names"]["data"]
    for idx in range(len(asy_names)):
        idx_asy = robj["attributes"]["assays"]["attributes"]["data"]["attributes"][
            "listData"
        ]["data"][idx]

        asy_class = get_class(idx_asy)

        if asy_class in ["dgCMatrix", "dgRMatrix", "dgTMatrix"]:
            robj_asys[asy_names[idx]] = as_sparse_matrix(idx_asy)
            if assay_dims is None:
                assay_dims = robj_asys[asy_names[idx]].shape
        elif asy_class == "densematrix":
            robj_asys[asy_names[idx]] = as_dense_matrix(idx_asy)
            if assay_dims is None:
                assay_dims = robj_asys[asy_names[idx]].shape
        else:
            robj_asys[asy_names[idx]] = None

    # parse coldata
    robj_coldata = as_pandas_from_dframe(robj["attributes"]["colData"])
    if robj_coldata.empty:
        robj_coldata = BiocFrame({"_cols": range(assay_dims[1])})

    # parse rowRanges
    robj_rowdata = None
    if "rowRanges" in robj["attributes"]:
        robj_rowdata = as_pandas_from_dframe(
            robj["attributes"]["rowRanges"]["attributes"]["elementMetadata"]
        )
    else:
        robj_rowdata = BiocFrame({"_rows": range(assay_dims[0])})

    # check red. dims, alternative expts
    robj_reduced_dims = None
    robj_altExps = None
    if _cls == "SingleCellExperiment":
        col_attrs = robj["attributes"]["int_colData"]["attributes"]["listData"][
            "attributes"
        ]["names"]["data"]

        for idx in range(len(col_attrs)):
            idx_col = col_attrs[idx]
            idx_value = robj["attributes"]["int_colData"]["attributes"]["listData"][
                "data"
            ][idx]

            if idx_col == "reducedDims" and idx_value["data"] is not None:
                robj_reduced_dims = as_dense_matrix(
                    robj["attributes"]["int_colData"]["attributes"]["listData"]["data"]
                )

            if idx_col == "altExps":
                alt_names = idx_value["attributes"]["listData"]["attributes"]["names"][
                    "data"
                ]
                robj_altExps = {}
                for idx_alt_names in range(len(alt_names)):
                    altn = alt_names[idx_alt_names]

                    alt_key = list(
                        idx_value["attributes"]["listData"]["data"][idx_alt_names][
                            "attributes"
                        ].keys()
                    )[0]

                    robj_altExps[altn] = as_summarized_experiment(
                        idx_value["attributes"]["listData"]["data"][idx_alt_names][
                            "attributes"
                        ][alt_key]
                    )

            # ignore colpairs for now, does anyone even use this ?
            # if col == "colPairs":

    if _cls == "SummarizedExperiment":
        return SummarizedExperiment(
            assays=robj_asys, row_data=robj_rowdata, column_data=robj_coldata
        )
    elif _cls == "SingleCellExperiment":
        return SingleCellExperiment(
            assays=robj_asys,
            row_data=robj_rowdata,
            column_data=robj_coldata,
            alternative_experiments=robj_altExps,
            reduced_dims=robj_reduced_dims,
        )
    else:
        raise TypeError(
            "`robj` is neither a `SummarizedExperiment` nor `SingleCellExperiment`."
        )
