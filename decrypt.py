import qrcode
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

files = listdir('FILES')
assert 'image_stegano.png' in files

STEGANO_IMAGE = cv2.imread(r'FILES\image_stegano.png', cv2.IMREAD_COLOR)
H, W, D = STEGANO_IMAGE.shape

STEGANO_DATA = "".join([f"{x:02b}" for x in (STEGANO_IMAGE & (0xFF >> 6)).reshape((1, W * H * D))[0]])
STEGANO_DATA = STEGANO_DATA[:STEGANO_DATA.index('00000000')+1]
print("\nRecovering %d bits of data from 'image_stegano.png'\n" % len(STEGANO_DATA))
a=''
print("RECOVERED DATA:\n")
for i in range(0, len(STEGANO_DATA), 8):
                a=a+chr(int(STEGANO_DATA[i: i + 8], 2))
                print(chr(int(STEGANO_DATA[i: i + 8], 2)), end='')
print('\n')
#print (STEGANO_DATA)
qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=4, border=.2)
qr.add_data(a)
qr.make(fit=True)

# Create an image from the QR Code instance
qr_img = qr.make_image(fill_color='black', back_color='white')
qr_img.save('decryptedQR.png')
      
