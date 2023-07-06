import time

import cv2

vedio = cv2.VideoCapture(0)
time.sleep(1)

first_frame = None
while True:

    state, frame = vedio.read()
    gray_vedio = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur_vedio_gaus = cv2.GaussianBlur(gray_vedio, (21, 21), 0)

    if first_frame is None:
        first_frame = blur_vedio_gaus

    diff_vedio = cv2.absdiff(first_frame,blur_vedio_gaus)

    thresh_vedio = cv2.threshold(diff_vedio, 60, 255, cv2.THRESH_BINARY)[1]

    dilated_vedio = cv2.dilate(thresh_vedio, None, iterations=2)

    highlited_matrix_of_vedio, check = cv2.findContours(dilated_vedio, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for highlited in highlited_matrix_of_vedio:
        if cv2.contourArea(highlited) < 500 :
            continue

        x, y, w, h = cv2.boundingRect(highlited)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0))

    cv2.imshow("My video", frame)



    key = cv2.waitKey(1)

    if key == ord("q"):
        break

vedio.release()



