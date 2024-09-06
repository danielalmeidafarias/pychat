from werkzeug.utils import secure_filename
from PIL import Image
import os

def save_profile_pic(profile_pic, user_id):
    filename = secure_filename(f"{user_id}.png")
    profile_pic.save(f"media/temp/{filename}")

    try:
        img = Image.open(f"media/temp/{filename}")
    except OSError:
        return {"message": "The file is not a valid image or unsupported format."}, 404

    crop_size = min(img.width, img.height)

    left = (img.width - crop_size) / 2
    top = (img.height - crop_size) / 2
    right = (img.width + crop_size) / 2
    bottom = (img.height + crop_size) / 2

    cropped_img = img.crop((left, top, right, bottom))

    img_300 = cropped_img.resize((300, 300))
    img_300_filename = secure_filename(f"300_{filename}")
    img_300.save(f"media/300/{img_300_filename}", format='PNG')

    img_150 = cropped_img.resize((150, 150))
    img_150_filename = secure_filename(f"150_{filename}")
    img_150.save(f"media/150/{img_150_filename}", format='PNG')

    img_50 = cropped_img.resize((50, 50))
    img_50_filename = secure_filename(f"50_{filename}")
    img_50.save(f"media/50/{img_50_filename}", format='PNG')

    os.remove(f"media/temp/{filename}")

