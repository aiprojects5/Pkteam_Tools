import io
import os

from zipfile import ZipFile, ZIP_DEFLATED


def zip(files_path, zip_path, filename):
    with ZipFile(f'{zip_path}/{filename}.zip', 'w', compression=ZIP_DEFLATED) as zip1:
        for file in files_path:
            zip1.write(file, arcname=f'{os.path.basename(file)}')
            # os.remove(f'{file}')


def store_zip_in_bytes(file_path):
    return_data = io.BytesIO()
    with open(file_path, 'rb') as fo:
        return_data.write(fo.read())
    # (after writing, cursor will be at last byte, so move it to start)
    return_data.seek(0)
    return return_data


def get_size_format(b, factor=1024, suffix="B"):
    for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
        if b < factor:
            return f"{b:.2f}{unit}{suffix}"
        b /= factor
    return f"{b:.2f}Y{suffix}"
