from dfrost.lib.log import debug
from gzip import open as gzip_open


def get_chunk_size():
    return 64 * 1024 * 1024


def compress_file(src, dst):
    debug(f"Compressing file: {src}, writing to: {dst}")
    with open(src, "rb") as src_f, gzip_open(dst, "wb") as dst_f:
        while True:
            chunk = src_f.read(get_chunk_size())
            if chunk == b"":
                break
            dst_f.write(chunk)


def decompress_file(src, dst):
    debug(f"Decompressing file: {src}, writing to: {dst}")
    with gzip_open(src, "rb") as src_f, open(dst, "wb") as dst_f:
        while True:
            chunk = src_f.read(get_chunk_size())
            if chunk == b"":
                break
            dst_f.write(chunk)
