"""Slice module

File slicing functions
"""

from io import BufferedReader
from math import ceil
from functools import partial

def slice_by_size(reader: BufferedReader, filename: str, filelen: int, chunk_size: int):
    """Slice current opened file by filename into fixed bytes parts

    Parameters
    ----------
    reader : BufferedReader
        Buffered binary file reader (Already opened file descriptor with 'rb' mode)
    filename : str
        Path to the current file to split
    filelen : int
        Current file size in bytes (os.stat)
    chunk_size : int
        Size in bytes to split the file into

    Returns
    -------
    p_count : int
        Total splitted parts
    """

    # Computes total parts, ceil result to ensure no byte missing
    p_count = ceil(filelen / chunk_size)

    print(f"File {filename} will be splitted in {p_count} parts")

    for i in range(0,p_count):
        with open(f"{filename}.{i+1}", 'wb') as writer:
            chunk = reader.read(chunk_size)
            writer.write(chunk)
            print(f"-> Splitted {len(chunk)} bytes of part {i+1}/{p_count}")

    return p_count


def slice_by_count(reader: BufferedReader, filename: str, filelen: int, parts_count: int):
    """Slice designed file by filename into a fixed parts count

    Parameters
    ----------
    reader : BufferedReader
        Buffered binary file reader (Already opened file descriptor with 'rb' mode)
    filename : str
        Path to the current file to split
    filelen : int
        Current file size in bytes (os.stat)
    parts_count : int
        Total wanted parts to split

    Returns
    -------
    chunk_size : int
        Maximum splitted part size in bytes
    """

    # Computes each part chunk size, ceil result to ensure remainder will be included
    chunk_size = ceil(filelen / parts_count)

    print(f"File {filename} will be splitted in chunks of {chunk_size} bytes")

    i = 1 # Current part counter

    # Partial from functools is used to read the file by fixed chunk size until
    # EOF is encountered
    for chunk in iter(partial(reader.read, chunk_size), b''):
        with open(f"{filename}.{i}", 'wb') as writer:
            writer.write(chunk)
            print(f"-> Splitted {len(chunk)} bytes in part {i}/{parts_count}")
            i += 1

    return chunk_size
