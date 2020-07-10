import os

import fire
import tifffile
import ashlar_pyramid


def make_pyramid(in_filepaths: str, out_filepath: str, tile_size: int):
    """
    """
    in_filepath_list = in_filepaths.split(",")

    def arr_gen():
        for fp in in_filepath_list:
            yield tifffile.imread(fp)

    name_list = [os.path.splitext(fp)[0] for fp in in_filepath_list]

    ashlar_pyramid.main(
        arr_gen(),
        channel_name_list=name_list,
        out_path=out_filepath,
        tile_size=tile_size,
    )


if __name__ == "__main__":
    fire.Fire(make_pyramid)
