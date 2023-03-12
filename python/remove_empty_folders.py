import os
from pathlib import Path


path: Path = Path("/home/nicolas/Pictures/not_organized")
os.chdir(path)


for year_dir in os.listdir(path):
    for month_dir in os.listdir(year_dir):
        print(month_dir)
        if os.path.isdir(month_dir):
            print(os.listdir(month_dir))
        # files = os.listdir(month_dir)
        # if not files:
        #     print(year_dir, month_dir)

    # for file in files:
    #     origin = Path(path.joinpath(file))
    #     year, month = file.split('-')[0], months[file.split('-')[1]]
    #     if int(year) >= 2002:
    #         dest = path.joinpath(year, month, file)
    #         os.rename(origin, dest)
