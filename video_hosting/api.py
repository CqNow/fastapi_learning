import shutil
from typing import List

from uuid import uuid4
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, BackgroundTasks, Request
from starlette.responses import StreamingResponse, HTMLResponse
from starlette.templating import Jinja2Templates

from schemas import UploadVideo, GetVideo, Message, GetListVideo
from models import Video, User
from services import save_video, open_file

video_router = APIRouter()
templates = Jinja2Templates(directory='templates')


@video_router.post('/')
async def create_video(
        background_tasks: BackgroundTasks,
        title: str = Form(...),
        description: str = Form(...),
        file: UploadFile = File(...),
):
    user = await User.objects.first()
    return await save_video(user, file, title, description, background_tasks)


# @video_router.get('/video/{video_pk}', responses={404: {'model': Message}})
# async def get_video(video_pk: int):
#     file = await Video.objects.select_related('user').get(pk=video_pk)
#     file_like = open(file.dict().get('file'), mode='rb')
#     return StreamingResponse(file_like, media_type='video/mp4')


@video_router.get('/user/{user_pk}', response_model=List[GetListVideo])
async def get_list_video(user_pk: int):
    video_list = await Video.objects.filter(user=user_pk).all()
    return video_list


@video_router.get('/index/{video_pk}', response_class=HTMLResponse)
async def get_video(request: Request, video_pk: int):
    return templates.TemplateResponse('index.html', {'request': request, 'path': video_pk})


@video_router.get('/video/{video_pk}')
async def get_streaming_video(request: Request, video_pk: int) -> StreamingResponse:
    file, status_code, content_lenght, headers = await open_file(request, video_pk)
    response = StreamingResponse(
        file,
        media_type='video/mp4',
        status_code=status_code,
    )

    response.headers.update({
        'Accept-Ranges': 'bytes',
        'Content-Length': str(content_lenght),
        **headers
    })
    return response
