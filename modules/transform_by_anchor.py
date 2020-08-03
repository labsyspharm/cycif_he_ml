from pathlib import Path

import fire
import h5py
import tifffile
import pandas as pd

from skimage import transform, img_as_uint


def run(
    src_filepath: str, anchor_filepath: str, out_filepath: str, overwrite: bool = True
):
    """
    Anchor-based alignment.
    """
    # prep
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

    if src_filepath.suffix == ".h5":
        src_f = h5py.File(src_filepath, "r")
        dst_f = h5py.File(out_filepath, "w")

        for key in src_f.keys():
            src_img = src_f[key]
            dst_img = transform.warp(
                src_img, tform.inverse, preserve_range=True
            ).astype(src_img)
            dst_img = img_as_uint(dst_img)
            dst_f.create_dataset(name=key, data=dst_img)

        src_f.close()
        dst_f.close()
    elif src_filepath.suffix == ".tif":
        src_img = tifffile.imread(src_img)
        dst_img = transform.warp(src_img, tform.inverse, preserve_range=True).astype(
            src_img.dtype
        )
        dst_img = img_as_uint(dst_img)

        tifffile.imsave(out_filepath, dst_img)
    else:
        raise ValueError(f"unsupported file extension {src_filepath.suffix}")


if __name__ == "__main__":
    fire.Fire(run)
