import cv2
import pytesseract
import uvicorn
from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
from typing import Any
import base64
import numpy as np
import re


app = FastAPI(
    title="Optical Character Recognition Server",
    docs_url=None,
    redoc_url=None,
    openapi_url=None
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"


@app.get("/ping", tags=["readiness"])
def ping():
    """
    Ping to check is server live
    :return: dict
    """
    return {"result": "ok"}


# @app.post("/ocr", tags=["get_ocr"])
# def get_ocr(file_data: Any = Body(None)):
#     try:
#         data = file_data.get("image")
#         try:
#             im_bytes = base64.b64decode(data)
#             im_arr = np.frombuffer(im_bytes, dtype=np.uint8)
#             img = cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)
#         except:
#             return {"status": "failure", "data": "Unable to convert base64 to image"}
#
#         config = "-l Devanagari -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz:' ',₹0123456789@.#/"
#         result = pytesseract.image_to_string(img, config=config)
#         print(result)
#         amount_regex = r'₹([\d,]+(?:\.\d+)?)'
#         twelve_digit_pattern = r'\b\d{12}\b'
#         amount = re.findall(amount_regex, result)[0]
#         amount = float(amount.replace(",", ""))
#         transaction_id = re.findall(twelve_digit_pattern, result)[0]
#         return {"status": "success", "data": {"amount": amount, "transaction_id": transaction_id}}
#     except Exception as e:
#         print(e)
#         return {"status": "failure", "data": e}


@app.post("/ocr", tags=["get_ocr"])
def get_ocr(file_data: Any = Body(None)):
    try:
        data = file_data.get("image")
        try:
            im_bytes = base64.b64decode(data)
            im_arr = np.frombuffer(im_bytes, dtype=np.uint8)
            img = cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)
        except:
            return {"status": "failure", "data": "Unable to convert base64 to image"}

        config = "-l Devanagari -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz:' ',₹0123456789@.#/"
        result = pytesseract.image_to_string(img, config=config)
        print(result)

        # Regex for amount extraction
        amount_regex = r'₹([\d,]+(?:\.\d+)?)'
        amount_matches = re.findall(amount_regex, result)
        amount = float(amount_matches[0].replace(",", "")) if amount_matches else "undefined"

        # List of regex patterns for UTR extraction
        utr_patterns = [
            r'UTR\s*[:\-]?\s*(\w+)',               # PhonePe
            r'UPI\s*Ref\s*No\s*[:\-]?\s*([A-Z0-9]+)', # Paytm
            r'UPI\s*transaction\s*ID\s*[:\-]?\s*([A-Z0-9]+)', # GPay
            r'UPI\/CR\/(\d{12})',                    # Bank 12-digit UTR
            r'\b\d{12}\b',                           # Generic 12-digit UTR
            r'UPI\s*Transaction\s*ID\s*[:\-]?\s*(\w+)', # Another pattern
            r'UPI\s*Ref\.\s*No:\s*(\d{7}\s\d{5})'    # Another pattern with a space in between
        ]

        # Extract UTR using the patterns
        transaction_id = "undefined"
        for pattern in utr_patterns:
            utr_matches = re.findall(pattern, result)
            if utr_matches:
                transaction_id = utr_matches[0].replace(" ", "")  # Remove spaces
                break

        return {"status": "success", "data": {"amount": amount, "transaction_id": transaction_id}}
    except Exception as e:
        print(e)
        return {"status": "failure", "data": str(e)}




if __name__ == '__main__':
    try:
        print("App server init called")
        uvicorn.run(app, host="0.0.0.0", port=11000)
        print("Server started")
    except Exception:
        print("Exception in app start: ")
