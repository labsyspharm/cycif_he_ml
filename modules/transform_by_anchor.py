from pathlib import Path

import fire
import h5py
import tifffile
import numpy as np
import pandas as pd

from skimage import transform, img_as_uint


def fn(src_img, tform, shape):
    dst_img = transform.warp(src_img, tform.inverse, preserve_range=True).astype(
        src_img.dtype
    )
    dst_img = img_as_uint(dst_img)

    xu = min(dst_img.shape[0], shape[0])
    yu = min(dst_img.shape[1], shape[1])
    out_img = np.zeros(shape, dtype=dst_img.dtype)
    out_img[:xu, :yu] = dst_img[:xu, :yu]

    return out_img


def run(
    template_filepath: str,
    src_filepath: str,
    anchor_filepath: str,
    out_filepath: str,
    overwrite: bool = True,
):
    """
    Anchor-based alignment.
    """
    # prep
    template_filepath = Path(template_filepath)
    src_filepath = Path(src_filepath)
    anchor_filepath = Path(anchor_filepath)
    out_filepath = Path(out_filepath)

    if out_filepath.exists() and overwrite:
        out_filepath.unlink()
    elif out_filepath.exists() and not overwrite:
        raise ValueError(f"{out_filepath} exists and overwrite set to {overwrite}")

    anchor_df = pd.read_csv(anchor_filepath)
    cycif_anchor = anchor_df[["cycif_x", "cycif_y"]].values
    he_anchor = anchor_df[["he_x", "he_y"]].values
    tform = transform.estimate_transform(
        ttype="affine", src=he_anchor, dst=cycif_anchor
    )

    shape = tifffile.imread(template_filepath).shape

    if src_filepath.suffix == ".h5":
        src_f = h5py.File(src_filepath, "r")
        dst_f = h5py.File(out_filepath, "w")

        for key in src_f.keys():
            src_img = src_f[key]
            dst_img = fn(src_img, tform, shape)
            dst_f.create_dataset(name=key, data=dst_img)

        src_f.close()
        dst_f.close()
    elif src_filepath.suffix == ".tif":
        src_img = tifffile.imread(src_filepath)
        dst_img = fn(src_img, tform, shape)
        tifffile.imsave(out_filepath, dst_img)
    else:
        raise ValueError(f"unsupported file extension {src_filepath.suffix}")


if __name__ == "__main__":
    fire.Fire(run)
