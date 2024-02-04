from PyPDF2 import PdfReader
from typing import List, Optional
from dataclasses import dataclass, field
from os import makedirs
from log import log
from pathlib import Path


@dataclass
class Page:
    text: List[str]
    imgs: List[bytes]


@dataclass
class File:
    path: Path
    pages: List = field(default_factory=lambda: [])
    save_imgs: bool = False

    def read_pages(self):
        log(f'Reading file: {self.path}')
        r = PdfReader(self.path)

        log(f'Found {len(r.pages)} pages, extracting text...', sev='DEBUG')
        for i, x in enumerate(r.pages):
            text = x.extract_text()
            imgs = []
            if self.save_imgs:
                imgs = [img.data for img in x.images]
                log(f'\tPage {i+1} has {len(imgs)} images.', sev='DEBUG')
            self.pages.append(Page(text, imgs))

    def write_pages(self, dest_dir: Path):

        dest_file = dest_dir / self.path.name.replace('.pdf', '.txt')
        dest_dir_img = dest_dir / f'{self.path.stem}_imgs/'

        msg = f'Saving text to {dest_file}'

        if self.save_imgs:
            msg += f' and images to {dest_dir_img}'

        log(f'{msg}.')
        with dest_file.open('w', encoding='utf-8') as txt:
            txt.write('\n'.join([p.text for p in self.pages]))

        if not self.save_imgs:
            return

        makedirs(dest_dir_img, exist_ok=True)

        for i, p in enumerate(self.pages):
            i += 1
            for x, img in enumerate(p.imgs):
                x += 1
                file_dest = dest_dir_img / f'pg{i:03d}_img{x:03d}.png'
                log(f'\tSaving image from page {i} to {file_dest}', sev="DEBUG")
                with file_dest.open('wb') as img_file:
                    img_file.write(img)


# def main():
#     args = [
#         '../docs/refs/andrade.pdf',
#         '../docs/refs/batista.pdf',
#         '../docs/refs/martins.pdf',
#         '../docs/refs/ribas.pdf']

#     files = [Path(a).absolute() for a in args if Path(a).is_file()]
#     for f in files:
#         x = File(f)
#         x.read_pages()

#         dest_dir = f.parent / 'txt/'

#         makedirs(dest_dir, exist_ok=True)
#         x.write_pages(dest_dir)


# main()
