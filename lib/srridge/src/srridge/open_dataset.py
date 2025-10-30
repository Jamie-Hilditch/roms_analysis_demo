import os
import pathlib

import numpy as np
import xarray as xr

from typing import Literal

def get_output_files(output_directory: os.PathLike, glob: str = "*_his.*.nc", sort: bool = True) -> list[pathlib.Path]:
    """Find and maybe sort all the output files in a directory."""
    output_files = list(pathlib.Path(output_directory).glob(glob))
    if sort:
        output_files.sort()
    return output_files

def get_grid_file(output_directory: os.PathLike, glob: str = "*_grd.nc") -> pathlib.Path | None:
    """Find the grid file in a directory."""
    grid_file = next(pathlib.Path(output_directory).glob(glob), None)
    return grid_file

def make_ocean_time_dim(ds: xr.Dataset) -> xr.Dataset:
    """Make ocean time the dimension."""
    return ds.swap_dims(time="ocean_time")

def add_s_coordinates(ds: xr.Dataset) -> xr.Dataset:
    """Construct and add the s-coordinates."""
    ds["s_w"] = (s_w := np.linspace(-1,0,ds.s_w.size, endpoint=True))
    ds["s_rho"] = s_w[:-1] + np.diff(s_w) / 2
    return ds

def add_grid_stretching(ds: xr.Dataset, Vtransform: Literal[1,2] = 2) -> xr.Dataset:
    """Extract the grid stretching out of attrs and add to dataset."""
    ds["Cs_r"] = ("s_rho", ds.attrs["Cs_r"])
    ds["Cs_w"] = ("s_w", ds.attrs["Cs_w"])
    ds["Vtransform"] = Vtransform
    return ds