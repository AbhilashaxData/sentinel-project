import rasterio
from rasterio.windows import from_bounds
def read_band(item, band_name, aoi):
    url=item.assets[band_name].href
    with rasterio.open(url) as src:
        # Convert AOI bounds to the raster CRS
        aoi_proj=aoi.to_crs(src.crs)
        # Calculate only the window covering the AOI
        window=from_bounds(*aoi_proj.total_bounds, transform=src.transform)
        data=src.read(1, window=window)
        profile=src.profile.copy()
        # Update metadata for the cropped image
        profile.update({
            "height": data.shape[0],
            "width": data.shape[1],
            "transform": src.window_transform(window)
        })
    return data, profile


from rasterio.warp import reproject
from rasterio.enums import Resampling
import numpy as np


def resample_band_to_10m(band, source_profile, reference_profile):
    output = np.empty(
        (reference_profile["height"], reference_profile["width"]),
        dtype=np.float32
    )

    reproject(
        source=band,
        destination=output,
        src_transform=source_profile["transform"],
        src_crs=source_profile["crs"],
        dst_transform=reference_profile["transform"],
        dst_crs=reference_profile["crs"],
        resampling=Resampling.nearest
    )

    return output


def calculate_ndvi(band_08, band_04):
    return np.divide(
        band_08.astype(float) - band_04.astype(float),
        band_08.astype(float) + band_04.astype(float),
        where=(band_08 + band_04) != 0,
        out=np.full_like(band_08, np.nan, dtype=float)
    )


def calculate_ndwi(band_03, band_08):
    return np.divide(
        band_03.astype(float) - band_08.astype(float),
        band_03.astype(float) + band_08.astype(float),
        where=(band_03 + band_08) != 0,
        out=np.full_like(band_03, np.nan, dtype=float)
    )


def calculate_ndbi(band_11, band_08):
    return np.divide(
        band_11.astype(float) - band_08.astype(float),
        band_11.astype(float) + band_08.astype(float),
        where=(band_11 + band_08) != 0,
        out=np.full_like(band_08, np.nan, dtype=float)
    )

    