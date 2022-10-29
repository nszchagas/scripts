import os
from pathlib import Path


months = {
    '01':  'jan',    '02':  'fev',    '03':  'mar',    '04':  'abr',    '05':  'mai',    '06':  'jun',
    '07':  'jul',    '08':  'ago',    '09':  'set',    '10':  'out',    '11':  'nov',    '12':  'dez',
}

path: Path = Path("/home/nicolas/Pictures/not_organized")
os.chdir(path)

# Create folders
for year in range(2002, 2023):
    if not os.path.isdir(f'{year}'):
        os.mkdir(f'{year}')
        for month in months.keys():
            os.chdir(f'{year}')
            os.mkdir(months[month])
            os.chdir('..')

# File names are year-month-day-hms
for root, dirs, files in os.walk(path):
    for file in files:
        origin = Path(path.joinpath(file))
        year, month = file.split('-')[0], months[file.split('-')[1]]
        if int(year) >= 2002:
            dest = path.joinpath(year, month, file)
            os.rename(origin, dest)
