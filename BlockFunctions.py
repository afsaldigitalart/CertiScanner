import qrcode
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import os
import random
import string 

QR_SIZE = 225
codes = set()

class Helper:
    
    def UniCode(self, prefix, length = 7):

        while True:
            code = prefix + ''.join(random.choices(string.digits, k=length))
            if code not in codes:
                codes.add(code)
                return code

     
        
    def makeQR(self, data):
        qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10 )


        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color='white').convert("RGBA")

        datas = img.getdata()
        newData = []
        for item in datas:
            if item[0] > 200 and item[1] > 200 and item[2] > 200:
                newData.append((255, 255, 255, 0))
            else:
                newData.append(item)
        img.putdata(newData)

        img_byte = BytesIO()
        img.save(img_byte, format='PNG')

        return img_byte.getvalue()



    def placeQR(self, img_path, qr_data,code, X=100, Y=100):
        
        try:
            certificate = Image.open(img_path).convert('RGBA')
            qr = Image.open(BytesIO(qr_data)).convert('RGBA')

            qr = qr.resize((QR_SIZE, QR_SIZE))
            positon = (X,Y)
            certificate.paste(qr, positon, qr)

            draw = ImageDraw.Draw(certificate)
            font = ImageFont.load_default(size=30)

            bbox = draw.textbbox((0, 0), code, font=font)
            text_width = bbox[2] - bbox[0]
            
            text_x = X + (QR_SIZE / 2) - (text_width / 2)
            text_y = Y + QR_SIZE + 10
            
            text_color = (255, 255, 255)
            draw.text((text_x, text_y), code, fill=text_color, font=font)

            os.makedirs('generated', exist_ok=True)
            filename = os.path.basename(img_path)
            output_path = os.path.join('generated', filename)
            certificate.save(output_path)

        except Exception as e:
            print(f"An Error Occured: {e}")
