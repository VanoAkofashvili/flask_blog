import os
import secrets

from PIL import Image
from flask_login import current_user


def save_picture(form_picture):
    # remove old profile picture if not default
    old_fn = os.path.join(app.root_path, 'static', 'profile_pics', current_user.image_file)

    if current_user.image_file != 'default.png' and os.path.exists(old_fn):
        os.remove(old_fn)
    r_hex = secrets.token_hex(8)
    p_extension = os.path.splitext(form_picture.filename)[1]
    new_filename = r_hex + p_extension
    i = Image.open(form_picture)

    i.thumbnail((125, 125))

    path = os.path.join(app.root_path, 'static', 'profile_pics', new_filename)

    i.save(path)
    return new_filename


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    msg.body = f"""To reset your password, visit the following link:
    {url_for('reset_token', token=token, _external=True)}

    If you did not make this request then simply ignore this email and no changes will be made
        """
    mail.send(msg)