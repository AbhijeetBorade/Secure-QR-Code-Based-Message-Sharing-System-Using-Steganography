import qrcode
from PIL import Image

import cv2
import numpy as np

from datetime import datetime as dt
from os import system, listdir
import msvcrt
from tqdm import trange


def get_stegano_or(char_bin: str, size: tuple, depth: int):
    or_arr = np.zeros(size, dtype=np.uint8)

    c = 0
    for x in trange(0, len(char_bin), depth, ncols=100, unit=' bytes', desc='Encoding'):
        k = c % size[2]
        j = (c // size[2]) % size[1]
        i = c // (size[2] * size[1])

        try:
            or_arr[i, j, k] |= int(char_bin[x: x+depth], 2)
        except IndexError:
            break

        c += 1

    return or_arr

files = listdir('FILES')
assert 'text.txt' in files and ('image.jpg' in files or 'image.jpeg' in files or 'image.png' in files)

IMG_FORMAT = ""
for filename in files:
                filename = filename.split('.')
                if filename[1] == 'jpg' or filename[1] == 'jpeg' or filename[1] == 'png':
                    IMG_FORMAT = filename[1]
                    break

BLANK_IMAGE = cv2.imread(rf"FILES\image.{IMG_FORMAT}", cv2.IMREAD_COLOR)
H, W, D = BLANK_IMAGE.shape
BIT_COUNT = W * H * D * 2
BYTE_COUNT = BIT_COUNT // 8

print(f"Resolution of 'image.{IMG_FORMAT}' = {W} x {H}")
print(f"No. of bits of plaintext that can be hidden in this image = {BIT_COUNT}")

print(f"\nIn simple terms, {BYTE_COUNT} characters can be stored in this image")

HIDING_TEXT = input('Enter message: ')

qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=4, border=.2)
qr.add_data(HIDING_TEXT)
qr.make(fit=True)

# Create an image from the QR Code instance
qr_img = qr.make_image(fill_color='black', back_color='white')


TXT_SIZE = len(HIDING_TEXT)
HIDING_CHARS = list(map(ord, list(HIDING_TEXT)))
HIDING_BIN = "".join([f"{x:08b}" for x in HIDING_CHARS])
#print(f"\nThe TXT file has {TXT_SIZE} characters which ",
 #                 end=f"is in the {BYTE_COUNT} character limit\nThe text consumes {TXT_SIZE * 100 / BYTE_COUNT :.3f} % of the available space\n\n" if TXT_SIZE <= BYTE_COUNT else f"EXCEEDS THE {BYTE_COUNT} CHARACTER LIMIT\nOnly {BYTE_COUNT * 100 / TXT_SIZE :.3f} % of the text can be encoded...\n\n")

STEGANO_ERASED_IMAGE = BLANK_IMAGE & 0b11111100
STEGANO_OR = get_stegano_or(HIDING_BIN, (H, W, 3), 2)
STEGANO_WRITTEN_IMAGE = STEGANO_ERASED_IMAGE | STEGANO_OR
cv2.imwrite(rf"FILES\image_stegano.png", STEGANO_WRITTEN_IMAGE)
#qr_img.save('qr.png')
print(f"\nGenerated 'image_stegano.png'!\nYou can find it in the 'FILES' folder")