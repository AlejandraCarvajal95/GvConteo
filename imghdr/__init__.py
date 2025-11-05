"""Installable shim package named `imghdr` to provide minimal stdlib behavior.

This package will be installed into site-packages when the repo is installed
with `pip install -e .` and will satisfy `import imghdr` during Streamlit
startup.
"""
from PIL import Image
import io

def what(file, h=None):
    try:
        if h is None:
            if isinstance(file, (bytes, bytearray)):
                data = file
            else:
                try:
                    with open(file, "rb") as f:
                        data = f.read(512)
                except Exception:
                    try:
                        data = file.read(512)
                    except Exception:
                        return None
            img = Image.open(io.BytesIO(data))
        else:
            img = Image.open(io.BytesIO(h))
        fmt = img.format
        if fmt:
            return fmt.lower()
    except Exception:
        return None
