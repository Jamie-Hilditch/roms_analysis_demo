import os
import pathlib

import numpy as np
import xarray as xr

def get_avg_files(output_directory: os.PathLike, glob: str = "*_avg.nc", sort: bool = True) -> list[pathlib.Path]:
    """Find and sort all the average files in  a directory."""
    avg_files = list(pathlib.Path(output_directory).glob(glob))
    if sort:
        avg_files.sort()
    return avg_files

def get_grid_file(output_directory: os.PathLike, glob: str = "*_grid.nc") -> pathlib.Path | None:
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

def add_grid_stretching(ds: xr.Dataset) -> xr.Dataset:
    """Extract the grid stretching out of attrs and add to dataset."""
    ds["Cs_r"] = ("s_rho", ds.attrs["Cs_r"])
    ds["Cs_w"] = ("s_w", ds.attrs["Cs_w"])
    return ds

def open_dataset(avg_files: list[pathlib.Path], grid_file: pathlib.Path | None = None) -> xr.Dataset:
    """Open ROMS average files, add s-coordinates and merge grid if given."""
    ds = xr.open_mfdataset(avg_files, preprocess=make_ocean_time_dim)
    ds = add_s_coordinates(ds)
    ds = add_grid_stretching(ds)
    if grid_file is not None:
        ds_grid = xr.load_dataset(grid_file)
        ds = ds.merge(ds_grid)
    return ds