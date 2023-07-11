import time
from emailing import send_email
import os
import cv2
import glob
from threading import Thread

vedio = cv2.VideoCapture(0)
time.sleep(1)

first_frame = None
status_list = []
count = 1


def clean_folder():
    images = glob.glob("images/*.png")
    for image in images:
        os.remove(image)
    print("folder has been deleted")


while True:
    status = 0

    state, frame = vedio.read()
    gray_vedio = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur_vedio_gaus = cv2.GaussianBlur(gray_vedio, (21, 21), 0)

    if first_frame is None:
        first_frame = blur_vedio_gaus

    diff_vedio = cv2.absdiff(first_frame, blur_vedio_gaus)

    thresh_vedio = cv2.threshold(diff_vedio, 60, 255, cv2.THRESH_BINARY)[1]

    dilated_vedio = cv2.dilate(thresh_vedio, None, iterations=2)

    highlited_matrix_of_vedio, check = cv2.findContours(dilated_vedio, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for highlited in highlited_matrix_of_vedio:
        if cv2.contourArea(highlited) < 5000:
            continue

        x, y, w, h = cv2.boundingRect(highlited)
        rectangle = cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0))
        if rectangle.any():
            status = 1
            cv2.imwrite(f"images/{count}.png", frame)
            count = count + 1
            all_images = glob.glob("images/*.png")
            index = int(len(all_images) / 2)
            images_with_object = all_images[index]

    status_list.append(status)
    status_list = status_list[-2:]
    print(status_list)
    if status_list[0] == 1 and status_list[1] == 0:
        email_thread = Thread(target=send_email, args=(images_with_object,))
        email_thread.daemon = True

        email_thread.start()


    cv2.imshow("My video", frame)

    key = cv2.waitKey(1)

    if key == ord("q"):
        break

vedio.release()
clean_folder()


