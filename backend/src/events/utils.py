import numpy as np
import base64
import cv2


def base64_to_frame(base64_string: str):
    """
    Convert base64-encoded string back to a frame
    """
    frame_bytes = base64.b64decode(base64_string)

    if not isinstance(frame_bytes, np.ndarray):
        frame_bytes = np.frombuffer(frame_bytes, dtype=np.uint8)
    frame = cv2.imdecode(frame_bytes, cv2.IMREAD_COLOR)
    return frame