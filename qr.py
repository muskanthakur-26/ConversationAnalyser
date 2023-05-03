import qrcode
from PIL import Image
# //img=qr.make("https://github.com/muskanthakur-26")
# //img.save("git_muskan.png")
qr = qrcode.QRCode(
        version=1,
error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
qr.add_data("https://github.com/muskanthakur-26")
qr.make("fit=True")
img=qr.make_image(fill_color="red", back_color="blue")
img.save("git_4336.png")