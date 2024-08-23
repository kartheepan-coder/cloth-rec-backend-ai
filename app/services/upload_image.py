from datetime import datetime
import math
import os
import cv2
from flask import g, jsonify, request

from app.services.image_resizer import image_resizer




def handle_upload(image,name):
    from app import create_app
    app =create_app()   

    user_name = name
    user_image = image

    if user_image:
        print(app.config['UPLOAD_FOLDER'])
        current_time = datetime.now().strftime('%Y%m%d_%H%M%S')  # Format: YYYYMMDD_HHMMSS
        filename = f"{user_name}_{current_time}{os.path.splitext(user_image.filename)[1]}" 
        print(filename)
        # # filename = name
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename) # type: ignore
        print(file_path)
        # file_path = f"/Users/karthi/Development/mayoo-project/ai-project-backend-main/uploads/{filename}"
        user_image.save(file_path)
        img_file = cv2.imread(file_path)
        resized_img = image_resizer(img_file)
        os.remove(file_path)
        cv2.imwrite(file_path,resized_img)
        g.csv_helper.append_row(name, file_path)
        print(g.csv_helper.append_row())
        # print(g.csv_helper.read_row())
        
        return f"File successfully resized and uploaded: "


    else:
        return jsonify("No image is uploaded")