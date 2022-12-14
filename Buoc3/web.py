from flask import Flask, render_template, request
import os
from random import random
import cv2
import sys
import tkinter
from tkinter import Frame, Tk, BOTH, Text, Menu, END
from tkinter.filedialog import Open, SaveAs

import numpy as np
import os.path
import cv2
import joblib
import sys
from sklearn.svm import LinearSVC
import database as databaseLite

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "static/upload"

detector = cv2.FaceDetectorYN.create(
    "face_detection_yunet_2022mar.onnx",
    "",
    (320, 320),
    0.9,
    0.3,
    5000
)
detector.setInputSize((320, 320))

recognizer = cv2.FaceRecognizerSF.create(
    "face_recognition_sface_2021dec.onnx", "")

svc = joblib.load('svc.pkl')
mydict = ['BanAnh', 'BanBao', 'BanDat', 'BanDien', 'BanKy', 'BanNam', 'BanNgoc', 'BanNinh', 'BanSon', 'BanThanh',
          'BanTuan', 'DaiNghia', 'DucHoa', 'HoaiNam', 'HuuDat', 'LeTai', 'SongHuy', 'ThayDuc', 'TieuHan', 'TieuTien']


@app.route('/', methods=['GET'])
def home():
    return render_template("index.html")


@app.route('/profile', methods=['GET'])
def profile():
    return render_template("profile.html")


@app.route("/process", methods=['POST'])
def recognizeFace():
    try:
        image = request.files['file']
        print(image)
        if image:
            # save
            path_to_save = os.path.join(
                app.config['UPLOAD_FOLDER'], image.filename)
            print("Save = ", path_to_save)
            image.save(path_to_save)

            imgin = cv2.imread(path_to_save)
            width = 320
            height = 320  # keep original height
            dim = (width, height)
            # resize image
            imgin = cv2.resize(imgin, dim, interpolation=cv2.INTER_AREA)

            faces = detector.detect(imgin)
            face_align = recognizer.alignCrop(imgin, faces[1][0])
            face_feature = recognizer.feature(face_align)
            test_prediction = svc.predict(face_feature)

            result = mydict[test_prediction[0]]
            cv2.putText(imgin, result, (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2, cv2.LINE_AA)

            cv2.imwrite(path_to_save, imgin)
            # get information by username
            user = databaseLite.get_user_by_name(result)
            print(user)
            pathImage = 'upload/' + image.filename
            return render_template("profile.html", user_image=pathImage, result=user,
                                   msgSuccess="Nh???n di???n l??n th??nh c??ng")

        else:
            return render_template('index.html', msg='H??y ch???n file ????? t???i l??n')

    except Exception as ex:
        print(ex)
        return render_template('index.html', msg=ex)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
