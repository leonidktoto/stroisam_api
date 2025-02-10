import os
from PIL import Image
from io import BytesIO
import boto3
from botocore.exceptions import NoCredentialsError
from fastapi import HTTPException, UploadFile
from app.config import settings



s3 = boto3.client('s3',
                  endpoint_url=settings.ENDPOINT_URL,
                  aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                  aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)




def resize_and_crop_image(image: Image.Image, size: tuple) -> BytesIO:
    """
    Функция для изменения размера изображения с сохранением пропорций,
    центрирования и обрезки по короткой стороне.
    Возвращает изображение в виде байтового потока.
    """
    target_width, target_height = size
    img_width, img_height = image.size
    
    # Определяем соотношения сторон
    img_aspect = img_width / img_height
    target_aspect = target_width / target_height
    
    if img_aspect > target_aspect:
        # Изображение шире, чем нужно: подгоняем по высоте и обрезаем по ширине
        new_height = target_height
        new_width = int(target_height * img_aspect)
    else:
        # Изображение выше, чем нужно: подгоняем по ширине и обрезаем по высоте
        new_width = target_width
        new_height = int(target_width / img_aspect)
    
    # Изменение размера изображения с использованием LANCZOS
    resized_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    # Вычисляем координаты для обрезки (по центру)
    left = (new_width - target_width) / 2
    top = (new_height - target_height) / 2
    right = left + target_width
    bottom = top + target_height
    
    cropped_image = resized_image.crop((left, top, right, bottom))

    # Если изображение имеет прозрачный фон (альфа-канал), заменяем его на белый
    if cropped_image.mode in ('RGBA', 'LA'):
        # Создаем белый фон
        white_bg = Image.new('RGB', cropped_image.size, (255, 255, 255))
        # Вставляем изображение с прозрачностью на белый фон
        white_bg.paste(cropped_image, mask=cropped_image.split()[-1])  # Используем альфа-канал как маску
        cropped_image = white_bg
    elif cropped_image.mode == 'P' and 'transparency' in cropped_image.info:
        # Обработка палитровых изображений с прозрачностью
        cropped_image = cropped_image.convert('RGBA')  # Конвертируем в RGBA для работы с альфа-каналом
        white_bg = Image.new('RGB', cropped_image.size, (255, 255, 255))
        white_bg.paste(cropped_image, mask=cropped_image.split()[-1])
        cropped_image = white_bg
    else:
        # Если изображение не имеет прозрачности, просто конвертируем в RGB
        cropped_image = cropped_image.convert('RGB')

    # Сохранение результата в байтовый поток
    img_byte_arr = BytesIO()
    cropped_image.save(img_byte_arr, format='JPEG')
    img_byte_arr.seek(0)
    
    return img_byte_arr

def load_images_to_s3(file: UploadFile, file_dir: str, product_id: int | None = None) -> str|list[str]:
    try:
        if file.filename:
            # Передаем только строку в splitext
            filename, _ = os.path.splitext(file.filename)
        else:
            raise ValueError("Имя файла отсутствует")

        # Открытие исходного изображения с помощью Pillow
        image = Image.open(file.file)
        
        # Создание изображений в трех разных разрешениях
        sizes = {
            "small": (150, 150),
            "medium": (600, 600),
            "large": (1200, 1200)
        }
       
        dir_image = ""
        dir_for_backet=""
        image_dir_list=[]

        for size_name, size in sizes.items():
            # Изменение размера изображения
            resized_image = resize_and_crop_image(image, size)
            

            if product_id:
                dir_image = f"media/products/{file_dir}/{product_id}/{filename}"
            else:
                dir_image = f"media/{file_dir}/{filename}"
                image_dir_list.append(f"{settings.ENDPOINT_URL}/{settings.BUCKET_NAME}/{dir_image}_{size_name}.jpeg")

            dir_for_backet=f"{dir_image}_{size_name}.jpeg"
            # Загрузка изображения в S3
            s3.upload_fileobj(
                resized_image,
                settings.BUCKET_NAME,
                dir_for_backet,
                ExtraArgs={"ContentType": "image/jpeg"}
            )
        if product_id:
            return f"{settings.ENDPOINT_URL}/{settings.BUCKET_NAME}/{dir_image}"
        else:
            return image_dir_list 


    except NoCredentialsError:
        raise HTTPException(status_code=500, detail="Credentials not available")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))