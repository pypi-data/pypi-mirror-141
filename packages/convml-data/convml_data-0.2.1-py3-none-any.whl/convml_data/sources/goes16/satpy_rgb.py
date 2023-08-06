import satpy
import satpy.composites.abi
import satpy.composites.cloud_products
import satpy.composites.viirs
import satpy.enhancements
import xarray as xr


def _cleanup_composite_da_attrs(da_composite):
    """
    When we want to save the RGB composite to a netCDF file there are some
    attributes that can't be saved that satpy adds so we remove them here
    """

    def fix_composite_attrs(da):
        fns = [
            ("start_time", lambda v: v.isoformat()),
            ("end_time", lambda v: v.isoformat()),
            ("area", lambda v: None),
            ("prerequisites", lambda v: None),
            ("crs", lambda v: str(v)),
            ("orbital_parameters", lambda v: None),
            ("_satpy_id", lambda v: None),
        ]

        for v, fn in fns:
            try:
                da.attrs[v] = fn(da.attrs[v])
            except Exception:
                pass

        to_delete = [k for (k, v) in da.attrs.items() if v is None]
        for k in to_delete:
            del da.attrs[k]

    fix_composite_attrs(da_composite)

    return da_composite


def load_rgb_files_and_get_composite_da(scene_fns):
    scene = satpy.Scene(reader="abi_l1b", filenames=scene_fns)

    # instruct satpy to load the channels necessary for the `true_color`
    # composite
    scene.load(["true_color"])

    # it is necessary to "resample" here because the different channels are at
    # different spatial resolution. By not passing in an "area" the highest
    # resolution possible will be used
    new_scn = scene.resample(resampler="native")

    # get out a dask-backed DataArray for the composite
    da_truecolor = new_scn["true_color"]

    if "crs" in da_truecolor.coords:
        da_truecolor = da_truecolor.drop("crs")

    # save the grid-mapping information for the first radiance channel (they
    # all use the same grid) into the coordinate of the data-array. This will
    # make sure that if the data-array is saved to file that CF-compliant
    # projection information is still available
    ds_ch1 = xr.open_dataset(scene_fns[0])
    grid_mapping = ds_ch1.Rad.grid_mapping
    da_truecolor.coords[grid_mapping] = ds_ch1[grid_mapping]

    # remove all attributes that satpy adds which can't be serialised to a netCDF file
    da_truecolor = _cleanup_composite_da_attrs(da_truecolor)

    return da_truecolor


def load_aux_file(scene_fn):
    # aux fields we simply open so we can crop them
    # but we need to pick out the right variable in the dataset
    ds = xr.open_dataset(scene_fn)
    vars_2d = [
        name for (name, da) in ds.data_vars.items() if set(da.dims) == {"x", "y"}
    ]
    vars_2d.remove("DQF")
    if len(vars_2d) != 1:
        raise Exception(
            "More than the data-quality variable (DQF) was found "
            f"in the aux dataset: {','.join(vars_2d)}"
        )
    var_name = vars_2d[0]

    scene = satpy.Scene(reader="abi_l2_nc", filenames=[scene_fn])
    scene.load([var_name])

    da = scene[var_name]
    if "crs" in da.coords:
        da = da.drop("crs")

    # set the projection info in a CF-compliant manner so we can load it later
    grid_mapping_var = da.grid_mapping
    da[grid_mapping_var] = ds[grid_mapping_var]

    # remove all attributes that satpy adds which can't be serialised to a netCDF file
    da = _cleanup_composite_da_attrs(da)

    return da


def load_radiance_channel(scene_fn, channel_number, derived_variable=None):
    """
    satpy has implemented functionality to convert for example from radiance to
    brightness temperature, which can be selected by defining
    `derived_variable` (e.g. `brightness_temperature`)
    """
    # for radiance channel fields we simply open so we can crop them
    # but we need to pick out the right variable in the dataset

    var_name = f"C{channel_number:02d}"
    ds = xr.open_dataset(scene_fn)

    if derived_variable is None:
        calibration = "radiance"
    else:
        calibration = derived_variable

    scene = satpy.Scene(reader="abi_l1b", filenames=[scene_fn])
    scene.load([var_name], calibration=calibration)

    da = scene[var_name]
    if "crs" in da.coords:
        da = da.drop("crs")

    # set the projection info in a CF-compliant manner so we can load it later
    grid_mapping_var = da.grid_mapping
    da[grid_mapping_var] = ds[grid_mapping_var]

    # remove all attributes that satpy adds which can't be serialised to a netCDF file
    da = _cleanup_composite_da_attrs(da)

    return da


def rgb_da_to_img(da):
    # need to sort by y otherize resulting image is flipped... there must be a
    # better way
    da_ = da.sortby("y", ascending=False)
    return satpy.writers.get_enhanced_image(da_)
