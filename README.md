# OCR Project - Optical Character Recognition

![Python](https://img.shields.io/badge/Python-3.x-blue) ![Tesseract](https://img.shields.io/badge/Tesseract-OCR-orange) ![License](https://img.shields.io/badge/license-MIT-green)

## Project Overview

This project is a simple Optical Character Recognition (OCR) application built using Python and Tesseract. The program allows users to upload an image, which is converted to a base64 string. The OCR engine, Tesseract, extracts characters from the image based on trained data. With the help of regular expressions, the system then identifies specific information (e.g., transaction amounts, unique transaction references).

### Key Features
- Image-to-text extraction using Tesseract
- Regex-based extraction of targeted data, like transaction IDs and amounts
- Supports Devanagari and English character recognition
- Base64 encoding for efficient data handling

## Technologies Used

- **Python** - Core programming language for this project
- **Tesseract OCR** - For character recognition
- **Regular Expressions** - For targeted data extraction
- **FastAPI** - API setup for handling user inputs (optional, if used in your project)

## Setup and Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/Alok-Pal/Alok-Pal-OCR-Optical-Character-Recognition.git
   cd ocr-project
