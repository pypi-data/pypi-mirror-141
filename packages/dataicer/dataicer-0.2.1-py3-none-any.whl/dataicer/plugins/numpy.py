"""This plugin is modelled on jsonpickles own implementation of a numpy extension for saving ndarray to json txt.

We however use numpy save and load for txt/binary files.
"""
from __future__ import absolute_import
import ast
import sys
from typing import Literal

import numpy as np

from jsonpickle.handlers import BaseHandler
import jsonpickle.ext.numpy as jpxnp
from jsonpickle import compat

from .file import BaseFileHandler

native_byteorder = "<" if sys.byteorder == "little" else ">"


def get_byteorder(arr):
    """translate equals sign to native order"""
    byteorder = arr.dtype.byteorder
    return native_byteorder if byteorder == "=" else byteorder


class NumpyBaseHandler(BaseHandler, BaseFileHandler):
    def __init__(self, mode: Literal["txt", "npy", "npz"] = "txt"):
        BaseFileHandler.__init__(self)
        self._mode = mode

    def flatten_dtype(self, dtype, data):
        if hasattr(dtype, "tostring"):
            data["dtype"] = dtype.tostring()
        else:
            dtype = compat.ustr(dtype)
            prefix = "(numpy.record, "
            if dtype.startswith(prefix):
                dtype = dtype[len(prefix) : -1]
            data["dtype"] = dtype

    def restore_dtype(self, data):
        dtype = data["dtype"]
        if dtype.startswith(("{", "[")):
            dtype = ast.literal_eval(dtype)
        return np.dtype(dtype)

    def get_file_id(self):
        return self.get_uuid() + f".{self._mode}"


class NumpyNDArrayHandler(NumpyBaseHandler):
    """Stores arrays as .npy files"""

    def flatten_flags(self, obj, data):
        if obj.flags.writeable is False:
            data["writeable"] = False

    def restore_flags(self, data, arr):
        if not data.get("writeable", True):
            arr.flags.writeable = False

    def flatten(self, obj, data):
        self.flatten_dtype(obj.dtype.newbyteorder("N"), data)
        self.flatten_flags(obj, data)
        data["file_uuid"] = self.get_file_id()
        data["shape"] = obj.shape
        data["mode"] = self._mode

        if self._mode in ["npy", "npz"]:
            with self._ah.open_file(data["file_uuid"], mode="wb") as open_file:
                if self._mode == "npy":
                    np.save(open_file, obj, allow_pickle=False)
                elif self._mode == "npz":
                    np.savez(open_file, obj)
        elif self._mode == "txt":
            with self._ah.open_file(data["file_uuid"], mode="w") as open_file:
                np.savetxt(
                    open_file,
                    obj.ravel(),  # ravel object to any ndim can be saved to txt (usually only 1d/2d)
                )

        return data

    def restore(self, data):
        mode = data["mode"]

        if mode in ["npy", "npz"]:
            with self._ah.open_file(data["file_uuid"], mode="rb") as open_file:
                arr = np.load(open_file)  # @, dtype=self.restore_dtype(data))
                if mode == "npz":
                    arr = arr["arr_0"]
        elif mode == "txt":
            with self._ah.open_file(data["file_uuid"], mode="r") as open_file:
                arr = np.loadtxt(open_file)  # @@, dtype=self.restore_dtype(data))

        shape = data.get("shape", None)
        if shape is not None:
            arr = arr.reshape(shape)

        self.restore_flags(data, arr)
        return arr


def get_numpy_handlers(
    array_mode: Literal["txt", "npy", "npz", "json"] = "txt"
) -> dict:
    """Get a dictionary of numpy dtype, handler pairs."""
    type_handlers = {
        np.dtype: jpxnp.NumpyDTypeHandler,
        np.generic: jpxnp.NumpyGenericHandler,
        # Numpy 1.20 has custom dtypes that must be registered separately.
        np.dtype(np.void).__class__: jpxnp.NumpyDTypeHandler,
        np.dtype(np.float32).__class__: jpxnp.NumpyDTypeHandler,
        np.dtype(np.int32).__class__: jpxnp.NumpyDTypeHandler,
        np.dtype(np.datetime64).__class__: jpxnp.NumpyDTypeHandler,
    }
    if array_mode == "json":
        type_handlers[np.ndarray] = jpxnp.NumpyNDArrayHandlerView()
    else:
        type_handlers[np.ndarray] = NumpyNDArrayHandler(mode=array_mode)
    return type_handlers
