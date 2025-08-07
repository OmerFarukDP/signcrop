import fitz  # PyMuPDF
import cv2
import numpy as np
import tempfile
import os

def extract_signature(file_storage):
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
        file_storage.save(tmp.name)

    doc = fitz.open(tmp.name)
    page = doc.load_page(0)
    pix = page.get_pixmap(dpi=200)
    img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)

    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    _, thresh = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY_INV)

    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    height = img.shape[0]
    signature_img = None

    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        if h < 100 and y > height * 0.6:
            signature_img = img[y:y+h, x:x+w]
            break

    os.unlink(tmp.name)

    if signature_img is None:
        return {"success": False, "message": "Signature not found"}

    _, buffer = cv2.imencode('.png', signature_img)
    encoded = buffer.tobytes()
    import base64
    b64 = base64.b64encode(encoded).decode()

    return {"success": True, "signature_base64": b64}
