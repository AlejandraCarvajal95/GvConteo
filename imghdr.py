"""Temporary shim for the stdlib `imghdr` module.

This file provides a minimal `what()` implementation using Pillow (PIL)
to detect image format when the platform runtime is missing the
`imghdr` stdlib module (some minimal Python runtimes used by hosts
may omit it).

This is a temporary workaround — the recommended long-term fix is to
ensure the deployment uses a full Python runtime (e.g. pin to python-3.11
via a `runtime.txt`).
"""
from PIL import Image
import io


def what(file, h=None):
    """Return the image type string if recognized, otherwise None.

    Parameters:
    - file: filename, file-like object or bytes
    - h: optional header bytes
    """
    try:
        if h is None:
            # If file is bytes/bytearray, use it directly
            if isinstance(file, (bytes, bytearray)):
                data = file
            else:
                # Otherwise try to open file path or file-like object
                try:
                    # file may be a path-like string
                    with open(file, "rb") as f:
                        data = f.read(512)
                except Exception:
                    # Fallback: if file is file-like, attempt to read
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
