import qrcode
from PIL import Image

n=input('Enter your name')


# Create qr code instance
qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=4, border=.2)

# Add data
text =input('Enter your message')
qr.add_data(text)
qr.make(fit=True)

# Create an image from the QR Code instance
qr_img = qr.make_image(fill_color='black', back_color='white')

# Load the logo
logo_img = Image.open('default.png')

# Scale the logo image. The width of the scaled logo shall be equal to the width of the QR code
qr_width, qr_height = qr_img.size
logo_current_width, logo_current_height = logo_img.size
#scaling_factor = qr_width / logo_current_width
#logo_new_height = int(scaling_factor * logo_current_height)
#logo_new_size = (qr_width, logo_new_height)
#logo_img = logo_img.resize(logo_new_size)

# Create an empty image to paste both images on
margin = 0
result = Image.new(mode='RGB', size=(logo_current_width, logo_current_height ), color='white')
result.paste(qr_img, (0, 0))
result.paste(logo_img, (0, 0))
result.save(n+'.png')
qr_img.save(n+'_Qr.png')



