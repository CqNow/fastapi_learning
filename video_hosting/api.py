import shutil
from typing import List
from unittest import result

from fastapi import APIRouter, UploadFile, File, Form, Request
from fastapi.responses import JSONResponse
from h11._abnf import status_code

from schemas import UploadVideo, GetVideo, User, Message

video_router = APIRouter()


@video_router.post('/')
async def root(title: str = Form(...), description: str = Form(...), file: UploadFile = File(...)):
    info = UploadVideo(title=title, description=description)
    with open(f'{file.filename}', 'wb') as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {'file_name': file.filename, 'info': info}


@video_router.post('/img', status_code=666)
async def upload_image(files: List[UploadFile] = File(...)):
    for img in files:
        with open(f'{img.filename}', 'wb') as buffer:
            shutil.copyfileobj(img.file, buffer)

    return {'result': 'Success!'}


@video_router.get('/video', response_model=GetVideo, responses={404: {'model': Message}})
async def get_video():
    user = {
        'id': 25,
        'name': 'Test_name'
    }
    video = {
        'title': 'Test',
        'description': 'Description',
    }
    info = GetVideo(user=user, video=video)
    #return info
    return JSONResponse(status_code=200, content=info.dict())
