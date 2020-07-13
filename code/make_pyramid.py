import os

import fire
import tifffile
import ap_lib


def make_pyramid(filelist_filepath: str, out_filepath: str, tile_size: int):
    with open(filelist_filepath, 'r') as f:
        in_filepath_list = [line.strip() for line in f]

    def arr_gen():
        for fp in in_filepath_list:
            yield tifffile.imread(fp)

    name_list = [os.path.splitext(os.path.basename(fp))[0]\
            for fp in in_filepath_list]

    ap_lib.main(
        arr_gen(),
        channel_name_list=name_list,
        out_path=out_filepath,
        tile_size=tile_size,
    )


if __name__ == '__main__':
    fire.Fire(make_pyramid)
