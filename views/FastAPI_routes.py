import os
import numpy as np
import cv2
import shutil

from PIL import Image
from io import BytesIO
from fastapi import FastAPI, UploadFile, APIRouter, File
from typing import Optional, List
from pydantic import BaseModel
from classes.pdf_convertor import Pdf_convertor
from classes.background_remove import Background_remove
from classes.mp3_to_mp4 import MP3ToMP4
from classes.to_pdf_convertor import To_pdf_convertor
from functions.function import store_zip_in_bytes
from starlette.responses import StreamingResponse

router = APIRouter()


@router.get("/")
async def index():
    return {'api': 'working'}


@router.post("/pdf_to_jpg")
async def pdf_image(file: UploadFile):
    filename = file.filename
    pdf_obj = Pdf_convertor(file, filename, api='pdf_to_jpg')
    file_path = pdf_obj.returned_value
    return_data = store_zip_in_bytes(file_path)
    os.remove(file_path)
    response = StreamingResponse(return_data, media_type="application/x-zip-compressed", )
    response.headers["Content-Disposition"] = f"attachment; filename={pdf_obj.filename}.zip"
    return response


@router.post("/pdf_to_png")
async def pdf_image(file: UploadFile):
    filename = file.filename
    pdf_obj = Pdf_convertor(file, filename, api='pdf_to_png')
    file_path = pdf_obj.returned_value
    return_data = store_zip_in_bytes(file_path)
    os.remove(file_path)
    response = StreamingResponse(return_data, media_type="application/x-zip-compressed", )
    response.headers["Content-Disposition"] = f"attachment; filename={pdf_obj.filename}.zip"
    return response


@router.post("/pdf_to_docx")
async def pdf_docx(file: UploadFile):
    filename = file.filename
    pdf_obj = Pdf_convertor(file, filename, api='pdf_to_docx')
    file_path = pdf_obj.returned_value
    return_data = store_zip_in_bytes(file_path)
    os.remove(file_path)
    response = StreamingResponse(return_data, media_type="application/docx", )
    response.headers["Content-Disposition"] = f"attachment; filename={pdf_obj.filename}.docx"
    return response


@router.post("/pdf_to_pptx")
async def pdf_pptx(file: UploadFile):
    filename = file.filename
    pdf_obj = Pdf_convertor(file, filename, api='pdf_to_pptx')
    file_path = pdf_obj.returned_value
    return_data = store_zip_in_bytes(file_path)
    os.remove(file_path)
    response = StreamingResponse(return_data, media_type="application/pptx", )
    response.headers["Content-Disposition"] = f"attachment; filename={pdf_obj.filename}.pptx"
    return response


@router.post("/pdf_to_excel")
async def pdf_excel(file: UploadFile):
    filename = file.filename
    pdf_obj = Pdf_convertor(file, filename, api='pdf_to_excel')
    file_path = pdf_obj.returned_value
    return_data = store_zip_in_bytes(file_path)
    os.remove(file_path)
    response = StreamingResponse(return_data, media_type='application/xlsx')
    response.headers["Content-Disposition"] = f"attachment; filename={pdf_obj.filename}.xlsx"
    return response


@router.post("/pdf_to_html")
async def pdf_html(file: UploadFile):
    filename = file.filename
    pdf_obj = Pdf_convertor(file, filename, api='pdf_to_html')
    file_path = pdf_obj.returned_value
    return_data = store_zip_in_bytes(file_path)
    os.remove(file_path)
    response = StreamingResponse(return_data, media_type='application/html')
    response.headers["Content-Disposition"] = f"attachment; filename={pdf_obj.filename}.html"
    return response


@router.post("/image_background")
async def image_background(file: UploadFile):
    content = await file.read()
    np_arr = np.fromstring(content, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    filename = file.filename
    image_obj = Background_remove(img, filename, api='image_background')
    file_path = image_obj.returned_value
    return_data = store_zip_in_bytes(file_path)
    os.remove(file_path)
    response = StreamingResponse(return_data, media_type='application/png')
    response.headers["Content-Disposition"] = f"attachment; filename={image_obj.filename}.png"
    return response


@router.post("/image_to_qrcode")
async def image_qrcode(file: UploadFile):
    content = await file.read()
    np_arr = np.fromstring(content, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    filename = file.filename
    image_obj = Background_remove(img, filename, api='image_to_qrcode')
    file_path = image_obj.returned_value
    return_data = store_zip_in_bytes(file_path)
    os.remove(file_path)
    response = StreamingResponse(return_data, media_type='application/png')
    response.headers["Content-Disposition"] = f"attachment; filename={image_obj.filename}.png"
    return response


@router.post("/image_audio_to_video")
async def image_audio_video(audio: UploadFile, images: List[UploadFile] = File()):
    images_list = []
    images_names = []
    for image in images:
        image_content = await image.read()
        np_arr = np.fromstring(image_content, np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        images_list.append(img)
        images_names.append(image.filename)
    # image_name = image.filename
    audio_name = audio.filename
    obj = MP3ToMP4(images_list, images_names, audio, audio_name)
    file_path = obj.returned_value
    return_data = store_zip_in_bytes(file_path)
    # os.remove(file_path)
    response = StreamingResponse(return_data, media_type='application/mp4')
    response.headers["Content-Disposition"] = f"attachment; filename={obj.audio_name[:-4]}.mp4"
    return response


@router.post("/images_to_pdf")
async def image_pdf(images: List[UploadFile] = File()):
    images_list = []
    for image in images:
        image_content = await image.read()
        im_pil = Image.open(BytesIO(image_content))
        im_pil = im_pil.convert('RGB')
        images_list.append(im_pil)
        filename = image.filename
    obj = To_pdf_convertor(images_list, filename, api='image_to_pdf')
    file_path = obj.returned_value
    return_data = store_zip_in_bytes(file_path)
    os.remove(file_path)
    response = StreamingResponse(return_data, media_type='application/pdf')
    response.headers["Content-Disposition"] = f"attachment; filename={obj.filename}.pdf"
    return response


@router.post("/docx_to_pdf")
async def docx_pdf(file: UploadFile):
    filename = file.filename
    obj = To_pdf_convertor(file, filename, api='docx_to_pdf')
    file_path = obj.returned_value
    return_data = store_zip_in_bytes(file_path)
    os.remove(file_path)
    response = StreamingResponse(return_data, media_type='application/pdf')
    response.headers["Content-Disposition"] = f"attachment; filename={obj.filename}.pdf"
    return response


@router.post("/ppt_to_pdf")
async def ppt_pdf(file: UploadFile):
    filename = file.filename
    obj = To_pdf_convertor(file, filename, api='ppt_to_pdf')
    file_path = obj.returned_value
    return_data = store_zip_in_bytes(file_path)
    os.remove(file_path)
    response = StreamingResponse(return_data, media_type='application/pdf')
    response.headers["Content-Disposition"] = f"attachment; filename={obj.filename}.pdf"
    return response
