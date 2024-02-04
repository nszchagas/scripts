from sys import argv
import os
from pathlib import Path
from datetime import datetime


number_of_files = int(argv[1])
dummy_files_home = '/home/nicolas/Documents/dummy_files/'
for x in range(number_of_files + 1):
    filename = datetime.now().strftime("%s")
    dest = f'{dummy_files_home}/{filename}'
    content = os.system(f'/home/nicolas/Documents/dev/scripts/shell/generate_dummy_pdf.sh > {dest}.txt')
    content = bytearray(content)
    with open(dest, 'wb') as file:
        file.write(content)
