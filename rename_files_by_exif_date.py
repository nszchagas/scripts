import os
from pathlib import Path
from exif import Image

pictures_folder = Path("/home/nicolas/Pictures/folders/")
os.chdir(pictures_folder)
for dir in pictures_folder.iterdir():
    if dir.is_dir:
        for file in dir.iterdir():
            try:
                extension: str = str(file).split('.')[-1].lower()
                error: bool = 'home' in extension
                try:
                    with open(file, 'rb') as img_file:
                        img: Image = Image(img_file)
                        if error:
                            print(file.absolute())
                        if (img.has_exif):
                            if (img.get('datetime')):
                                key: str = 'datetime'
                            elif (img.get('datetime_original')):
                                key: str = 'datetime_original'
                            # else:
                                # print(
                                #     f'File doesn\'t contain datetime: {file}')
                                # print(f'File keys: {img.get_all()}')
                            filename: str = str(img.get(key))
                            if (filename):
                                [year, month, day_hour, minute, seconds,
                                    *kwargs] = filename.split(':')
                                [day, hour] = day_hour.split(' ')
                                filename = f'{year}-{month}-{day}-{hour}{minute}{seconds}.{extension}'
                                # os.rename(file, filename)
                            else:
                                print(f'File has no exif info: {file}')

                except Exception as e:
                    pass
            except ValueError as e:
                print(f'Couldn\'t open file: {file}')
                pass
