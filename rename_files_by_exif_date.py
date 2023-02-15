import os
from pathlib import Path
from exif import Image
from datetime import datetime as dt

DIR = '/home/nicolas/Pictures/Takeout/2020'

pictures_folder = Path(DIR)
os.chdir(pictures_folder)


def format_name_from_datetime(datetime: str, extension: str) -> str:
    [year, month, day_hour, minute, seconds, *kwargs] = datetime.split(':')
    [day, hour] = day_hour.split(' ')
    return f'{year}-{month}-{day}-{hour}{minute}{seconds}.{extension}'


def log(message: str) -> None:
    print(dt.now().strftime(f'[%d/%m/%y %T] {message}'))


log("Starting script")

for item in pictures_folder.iterdir():
    log(f'Starting conversion for item: {item}')
    if not item.is_dir():
        try:
            extension: str = str(item).split('.')[-1].lower()
            try:
                with open(item, 'rb') as img_item:
                    img: Image = Image(img_item)
                    log(f'File {item} has exif data? {img.has_exif}')
                    if (img.has_exif):
                        if (img.get('datetime')):
                            key: str = 'datetime'
                        elif (img.get('datetime_original')):
                            key: str = 'datetime_original'
                        else:
                            print(
                                f'item doesn\'t contain datetime: {item}')
                            print(f'item keys: {img.get_all()}')

                        datetime_photo: str = str(img.get(key))
                        if datetime_photo:
                            new_name = format_name_from_datetime(
                                datetime_photo, extension)

                            print(f'{DIR}/{item} {DIR}/{new_name}')
                            # os.rename(item, itemname)
                    else:
                        print(f'item has no exif info: {item}')

            except Exception as e:
                pass
        except ValueError as e:
            print(f'Couldn\'t open item: {item}')
            pass
