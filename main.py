import cv2
import matplotlib.pyplot as plt
import numpy as np
from flask import Flask, render_template, request, redirect, url_for
import os
from util import get_parking_spots_bboxes, empty_or_not
import sqlite3
app = Flask(__name__)




database ="streetspot.db"
conn = sqlite3.connect(database)
cursor = conn.cursor()


cursor.execute("create table if not exists register ("
               "name TEXT, "
               "email text, "
               "password text) "
               )

conn.commit()
conn.close()


@app.route('/')
@app.route('/user',methods=['POST'])
def user():
   return render_template('register.html')



@app.route('/u_register',methods=['POST'] )
def u_register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        conn = sqlite3.connect(database)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO register (name, email, password) VALUES ( ?, ?, ?)",
                           (name, email, password))
        conn.commit()
        conn.close()
    return render_template('register.html')


@app.route('/u_login',methods=['POST'] )
def u_login():
    if request.method == 'POST':
        email = request.form['email']
        password1 = request.form['password']
        conn = sqlite3.connect(database)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM register WHERE email=? AND password=?", (email, password1))
        data=cursor.fetchall()
        if data:
                return render_template('new.html')
        else:
            return "password mismatch"








def calc_diff(im1, im2):
    return np.abs(np.mean(im1) - np.mean(im2))



@app.route('/process', methods=['POST'])
def process():
    if 'mask' not in request.files or 'video' not in request.files:
        return redirect(url_for('index'))

    mask_file = request.files['mask']
    video_file = request.files['video']

    mask_path = os.path.join('uploads', 'mask.png')
    video_path = os.path.join('uploads', 'video.mp4')

    mask_file.save(mask_path)
    video_file.save(video_path)

    process_video(mask_path, video_path)

    return render_template('new.html')





def process_video(mask, video_path):
    mask = cv2.imread(mask, 0)
    cap = cv2.VideoCapture(video_path)
    connected_components = cv2.connectedComponentsWithStats(mask, 4, cv2.CV_32S)
    spots = get_parking_spots_bboxes(connected_components)
    spots_status = [None for j in spots]
    diffs = [None for j in spots]
    previous_frame = None
    frame_nmr = 0
    ret = True
    step = 30
    while ret:
        ret, frame = cap.read()

        if not ret:
            break  

        if frame_nmr % step == 0 and previous_frame is not None:
            for spot_indx, spot in enumerate(spots):
                x1, y1, w, h = spot

                spot_crop = frame[y1:y1 + h, x1:x1 + w, :]

                diffs[spot_indx] = calc_diff(spot_crop, previous_frame[y1:y1 + h, x1:x1 + w, :])


        if frame_nmr % step == 0:
            if previous_frame is None:
                arr_ = range(len(spots))
            else:
                arr_ = [j for j in np.argsort(diffs) if diffs[j] / np.amax(diffs) > 0.4]
            for spot_indx in arr_:
                spot = spots[spot_indx]
                x1, y1, w, h = spot

                spot_crop = frame[y1:y1 + h, x1:x1 + w, :]

                spot_status = empty_or_not(spot_crop)

                spots_status[spot_indx] = spot_status

        if frame_nmr % step == 0:
            previous_frame = frame.copy()

        for spot_indx, spot in enumerate(spots):
            spot_status = spots_status[spot_indx]
            x1, y1, w, h = spots[spot_indx]

            if spot_status:
                frame = cv2.rectangle(frame, (x1, y1), (x1 + w, y1 + h), (0, 255, 0), 2)
            else:
                frame = cv2.rectangle(frame, (x1, y1), (x1 + w, y1 + h), (0, 0, 255), 2)

        cv2.rectangle(frame, (80, 20), (550, 80), (0, 0, 0), -1)
        cv2.putText(frame, 'Available spots: {} / {}'.format(str(sum(spots_status)), str(len(spots_status))), (100, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        if frame.shape[0] > 0 and frame.shape[1] > 0:
            cv2.imshow('frame', frame)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break

        frame_nmr += 1

    cap.release()
    cv2.destroyAllWindows()







if __name__ == '__main__':
    app.run(debug=False,port=250)




