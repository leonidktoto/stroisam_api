from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from PIL import Image
import boto3
from io import BytesIO
from botocore.exceptions import NoCredentialsError
from app.config import settings
from app.users.router import http_bearer


router=APIRouter(
    prefix="/managment",
    tags=["Администрирование"],
    #dependencies=[Depends(http_bearer)]
)

# Инициализация клиента S3
s3 = boto3.client('s3',
                  endpoint_url=settings.ENDPOINT_URL,
                  aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                  aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)


def resize_image(image: Image.Image, size: tuple) -> BytesIO:
    """
    Функция для изменения размера изображения с сохранением пропорций.
    Возвращает изображение в виде байтового потока.
    """
    resized_image = image.copy()
    resized_image.thumbnail(size)  # Сохранение пропорций
    img_byte_arr = BytesIO()
    resized_image.save(img_byte_arr, format='JPEG')
    img_byte_arr.seek(0)
    return img_byte_arr

@router.post("/upload-image/")
async def upload_image(file_dir: str, file: UploadFile = File(...)):
    try:
        # Открытие исходного изображения с помощью Pillow
        image = Image.open(file.file)
        
        # Создание изображений в трех разных разрешениях
        sizes = {
            "small": (150, 150),
            "medium": (600, 600),
            "large": (1200, 1200)
        }
        file_urls = {}

        for size_name, size in sizes.items():
            # Изменение размера изображения
            resized_image = resize_image(image, size)
            
            # Имя файла с добавлением префикса для разрешения
            filename = f"{file_dir}/{size_name}_{file.filename}"

            # Загрузка изображения в S3
            s3.upload_fileobj(
                resized_image,
                settings.BUCKET_NAME,
                filename,
                ExtraArgs={"ContentType": "image/jpeg"}
            )

            # Формирование URL для каждого изображения
            file_urls[size_name] = f"{settings.ENDPOINT_URL}/{settings.BUCKET_NAME}/{filename}"

        # Возвращаем ссылки на изображения в JSON-ответе
        return JSONResponse(content={"images": file_urls}, status_code=200)

    except NoCredentialsError:
        raise HTTPException(status_code=500, detail="Credentials not available")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))