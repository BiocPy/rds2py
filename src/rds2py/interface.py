from .core import PyParsedObject

import pandas as pd
from scipy import sparse as sp
import numpy as np

from biocpy.singlecellexperiment import SingleCellExperiment
from biocpy.summarizedexperiment import SummarizedExperiment

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"


def read_rds(file: str) -> dict:
    """Read a Rds file and get a python representation

    Args:
        file (str): Path to file

    Returns:
        dict: realized R object
    """
    parsed_obj = PyParsedObject(file)
    robject_obj = parsed_obj.get_robject()
    realized = robject_obj.realize_value()

    return realized


def get_class(robj: dict) -> str:
    """generic method to get the class of the realized R object

    Args:
        robj (dict): realized R object

    Returns:
        str: class name
    """
    if "class_name" in robj:
        return robj["class_name"]

    if "attributes" in robj and len(robj["attributes"].keys()) > 0:
        obj_attr = robj["attributes"]
        if "class" in obj_attr:
            return obj_attr["class"]["data"][0]

        # kind of making this assumption, if we ever see a dim, its a matrix
        if "dim" in obj_attr:
            return "densematrix"

    return None


def as_pandas_from_data_frame(robj: dict) -> pd.DataFrame:
    """Convert a realized R object to a pandas data frame representation

    Args:
        obj (dict): object parsed from the Rds file

    Raises:
        Exception: incorrect class

    Returns:
        pd.DataFrame: a pandas dataframe of the R Object
    """

    cls = get_class(robj)

    if cls != "data.frame":
        raise Exception(f"obj is not a `data.frame` but is `{cls}`")

    df = pd.DataFrame(
        robj["data"],
        columns=robj["attributes"]["names"]["data"],
        index=robj["attributes"]["row.names"]["data"],
    )

    return df


def as_pandas_from_dframe(robj: dict) -> pd.DataFrame:
    """Convert a realized R object to a pandas data frame representation

    Args:
        obj (dict): object parsed from the Rds file

    Raises:
        Exception: incorrect class

    Returns:
        pd.DataFrame: a pandas dataframe of the R Object
    """

    cls = get_class(robj)

    if cls != "DFrame":
        raise Exception(f"obj is not a `DFrame` but is `{cls}`")

    data = {}
    col_names = robj["attributes"]["listData"]["attributes"]["names"]["data"]
    for idx in range(len(col_names)):
        idx_asy = robj["attributes"]["listData"]["data"][idx]

        data[col_names[idx]] = idx_asy["data"]

    index = None
    if robj["attributes"]["rownames"]["data"]:
        index = robj["attributes"]["rownames"]["data"]

    df = pd.DataFrame(data, columns=col_names, index=index,)

    return df


def as_sparse_matrix(robj: dict) -> sp.spmatrix:
    """Convert a realized R object to a sparse representation

    Args:
        robj (dict): object parsed from the Rds file

    Raises:
        Exception: incorrect class

    Returns:
        sp.spmatrix: a sparse matrix of the R object
    """
    cls = get_class(robj)

    if cls not in ["dgCMatrix", "dgRMatrix"]:
        raise Exception(
            f"obj is not a supported sparse matrix format (`dgCMatrix`, `dgRMatrix`) but is `{cls}`"
        )

    if cls == "dgCMatrix":
        return sp.csc_matrix(
            (
                robj["attributes"]["x"]["data"],
                robj["attributes"]["i"]["data"],
                robj["attributes"]["p"]["data"],
            ),
            shape=tuple(robj["attributes"]["Dim"]["data"].tolist()),
        )

    if cls == "dgRMatrix":
        return sp.csr_matrix(
            (
                robj["attributes"]["x"]["data"],
                robj["attributes"]["i"]["data"],
                robj["attributes"]["p"]["data"],
            ),
            shape=tuple(robj["attributes"]["Dim"]["data"].tolist()),
        )


def as_dense_matrix(robj: dict, order: str = "F") -> np.ndarray:
    """Convert a realized R object to a dense matrix representation

    Args:
        robj (dict): object parsed from the Rds file
        order (str): Row-major (C-style) or column-major (Fortran-style) order. Defaults to "F".

    Raises:
        Exception: incorrect class

    Returns:
        np.ndarray: a dense np array of the R object
    """
    cls = get_class(robj)

    if cls not in ["densematrix"]:
        raise Exception(f"obj is not a supported dense matrix format, but is `{cls}`")

    return np.ndarray(
        shape=tuple(robj["attributes"]["dim"]["data"].tolist()),
        buffer=robj["data"],
        order=order,
    )


def as_SCE(robj: dict) -> np.ndarray:
    """Convert a realized R object to a SingleCellExperiment or SummarizedExperiment.

    Feel free to modify or write your own custom function to fully represent an SCE/SE.

    Args:
        robj (dict): object parsed from the Rds file
        order (str): Row-major (C-style) or column-major (Fortran-style) order. Defaults to "F".

    Raises:
        Exception: incorrect class

    Returns:
        np.ndarray: a dense np array of the R object
    """
    cls = get_class(robj)

    if cls not in ["SingleCellExperiment", "SummarizedExperiment"]:
        raise Exception(
            f"obj is not a `SingleCellExperiment` or `SummarizedExperiment`, but is `{cls}`"
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

        asy_cls = get_class(idx_asy)

        if asy_cls in ["dgCMatrix", "dgRMatrix"]:
            robj_asys[asy_names[idx]] = as_sparse_matrix(idx_asy)
            if assay_dims is None:
                assay_dims = robj_asys[asy_names[idx]].shape
        elif asy_cls == "densematrix":
            robj_asys[asy_names[idx]] = as_dense_matrix(idx_asy)
            if assay_dims is None:
                assay_dims = robj_asys[asy_names[idx]].shape
        else:
            robj_asys[asy_names[idx]] = None

    # parse coldata
    robj_coldata = as_pandas_from_dframe(robj["attributes"]["colData"])
    if robj_coldata.empty:
        robj_coldata = pd.DataFrame({"_cols": range(assay_dims[1])})

    # parse rowRanges
    robj_rowdata = None
    if "rowRanges" in robj["attributes"]:
        robj_rowdata = as_pandas_from_dframe(
            robj["attributes"]["rowRanges"]["attributes"]["elementMetadata"]
        )
    else:
        robj_rowdata = pd.DataFrame({"_rows": range(assay_dims[0])})

    # check red. dims, alternative expts
    robj_reduced_dims = None
    robj_altExps = None
    if cls == "SingleCellExperiment":
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

                    robj_altExps[altn] = as_SCE(
                        idx_value["attributes"]["listData"]["data"][idx_alt_names][
                            "attributes"
                        ][alt_key]
                    )

            # ignore colpairs for now, does anyone even use this ?
            # if col == "colPairs":

    if cls == "SummarizedExperiment":
        return SummarizedExperiment(
            assays=robj_asys, rowData=robj_rowdata, colData=robj_coldata
        )
    elif cls == "SingleCellExperiment":
        return SingleCellExperiment(
            assays=robj_asys,
            rowData=robj_rowdata,
            colData=robj_coldata,
            alterExps=robj_altExps,
            reducedDims=robj_reduced_dims,
        )
