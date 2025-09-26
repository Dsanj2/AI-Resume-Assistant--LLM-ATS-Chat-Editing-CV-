import onnxruntime as ort
import numpy as np
from PIL import Image
from pdf2image import convert_from_path

# Load ONNX model with DirectML execution provider
def load_ocr_model(model_path="ocr_model.onnx"):
    providers = [("DmlExecutionProvider", {"device_id": 0}), "CPUExecutionProvider"]
    return ort.InferenceSession(model_path, providers=providers)

# Preprocess image to fit OCR model
def preprocess_image(img: Image.Image, size=(320, 320)):
    img = img.convert("L").resize(size)  # grayscale + resize
    arr = np.array(img).astype(np.float32) / 255.0
    arr = np.expand_dims(arr, axis=(0, 1))  # [1,1,H,W]
    return arr

# Run OCR on PDF
def extract_text_from_pdf(pdf_path, ocr_model):
    pages = convert_from_path(pdf_path, dpi=200)
    text = []

    for page in pages:
        input_data = preprocess_image(page)
        ort_inputs = {ocr_model.get_inputs()[0].name: input_data}
        ort_outs = ocr_model.run(None, ort_inputs)
        
        # Assuming model outputs decoded text (simplified)
        page_text = ort_outs[0][0] if ort_outs else ""
        text.append(page_text)

    return "\n".join(text)
