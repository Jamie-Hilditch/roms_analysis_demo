import pathlib
import xarray as xr

from . import open_dataset

from .open_dataset import get_grid_file, get_output_files

__all__ = [
    "get_output_files",
    "get_grid_file",
    "open_santa_rosa_dataset",
]

def open_santa_rosa_dataset(
    his_files: list[pathlib.Path], grid_file: pathlib.Path | None = None
) -> xr.Dataset:
    """Open ROMS his files, add s-coordinates and merge grid if given."""
    ds = xr.open_mfdataset(
        his_files,
        preprocess=open_dataset.make_ocean_time_dim,
        join="outer",
        compat="override",
        combine="by_coords",
        data_vars="minimal",
        coords="minimal",
    )
    ds = open_dataset.add_s_coordinates(ds)
    ds = open_dataset.add_grid_stretching(ds)
    if grid_file is not None:
        ds_grid = xr.load_dataset(grid_file)
        ds = ds.merge(ds_grid)
    return ds
