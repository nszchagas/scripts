import os
from pathlib import Path
from re import sub
from exif import Image
from datetime import datetime as dt
from typing import Tuple, List


def format_name_from_datetime(datetime: str, filename: Path) -> str:
    [year, month, day_hour, minute, seconds, *kwargs] = datetime.split(':')
    [day, hour] = day_hour.split(' ')
    new_filename: str = str(filename).split(filename.stem)[0]
    return f'{new_filename}{year}-{month}-{day}-{hour}{minute}{seconds}.{get_extension(filename)}'


def get_extension(filename: str):
    return str(filename).split('.')[-1].lower()


def logger(message: str, level: str = 'INFO') -> None:
    if level != 'DEBUG':
        print(dt.now().strftime(f'[%d/%m/%y %T {level}] {message}'))


def log_defect_files(defect_files: List, base_path: Path):
    logs_path: str = f'/home/nicolas/Documents/scripts/{base_path.stem}/'
    if not Path(logs_path).is_dir():
        os.mkdir(logs_path)

    if defect_files:
        defect_path: Path = base_path.joinpath(
            f'../{base_path.stem}-defect')
        with open(f'{logs_path}/move_defect_files.sh', 'a') as logs:
            logs.write(
                '\n'.join([f'mv {str(d)} {defect_path}' for d in defect_files]))
            defect_files = []


def get_datetime(filename: str) -> str:
    datetime: str = ""
    with open(filename, 'rb') as img_item:
        img: Image = Image(img_item)
        if not img.has_exif:
            raise Exception("Image doesn't contain exif data.")

        if (img.get('datetime')):
            datetime = img.get('datetime')
        elif (img.get('datetime_original')):
            key: str = 'datetime_original'
            datetime = img.get('datetime_original')
        else:
            print(
                f'File doesn\'t contain datetime: {filename}')
            print(f'item keys: {img.get_all()}')
            return -1
    return datetime


def main():
    DIR = '/home/nicolas/Pictures/Pictures/Takeout/2020_t'
    logger(f"Starting script for {DIR}")

    base_path = Path(DIR)
    try:
        os.chdir(base_path)
    except FileNotFoundError:
        logger(f'No such directory: {base_path}', level='ERROR')
        return -1
    defect_files: List = []
    for item in os.walk(base_path):
        curr_dir: Path = Path(item[0])
        subdir: List = item[1]
        files: List = item[2]

        for f in files:
            # logger(f'Starting conversion for file: {f}', level='DEBUG')

            extension: str = get_extension(f)
            file_path: Path = curr_dir.joinpath(f)
            if not extension:
                return -1
            elif extension in ['mp4', 'txt', 'sh', 'txt', 'json']:
                logger(f'Skipping file: {f}', level='DEBUG')
                pass
            try:
                datetime: str = get_datetime(file_path)
                if datetime:
                    name: str = format_name_from_datetime(
                        datetime, file_path)
            except Exception as e:
                fixed_name: str = sub('[\ |\(|\)]+', '*', str(file_path))
                defect_files.append(fixed_name)

    log_defect_files(defect_files, base_path)


main()
