import numpy as np
import cv2
from Classes import *
import utils
import time

K = 5
SIGMA_INIT = 30
ALPHA = 0.01
SIGMA_THRESH = 5.0
T = 0.7

def main ():
    text_inp = "Input Image"
    text_fg = "Foreground"

    cv2.namedWindow(text_inp, cv2.CV_WINDOW_AUTOSIZE)
    cv2.namedWindow(text_fg, cv2.CV_WINDOW_AUTOSIZE)

    # constructor
    cap = cv2.VideoCapture("../dt_passat.mpg")
    cap.grab()
    img = cap.retrieve()[1]

    width = img.shape[1]
    height = img.shape[0]
    sh_width = width / 2
    sh_height = height / 2

    cv2.moveWindow(text_inp, 0, 0)
    cv2.moveWindow(text_fg, sh_width + 10, 0)
    start = time.time()
    model = Model(sh_width, sh_height, K, SIGMA_INIT, ALPHA, SIGMA_THRESH, T)
    # print model.pm
    # exit()
    end = time.time()
    print 'Model Init time {0}'.format(end - start)

    fg_img = np.zeros((sh_height, sh_width), np.uint8)


    # cap.grab()
    # img = cap.retrieve()[1]
    # show_img = cv2.resize(img, (sh_width, sh_height))
    # inp_gray_img = cv2.cvtColor(show_img, cv2.COLOR_RGB2GRAY)

    # while img:
    while cap.grab():
        #Grabs the next frame from video file or capturing device
        img = cap.retrieve()[1]
        show_img = cv2.resize(img, (sh_width, sh_height))
        inp_gray_img = cv2.cvtColor(show_img, cv2.COLOR_RGB2GRAY)

        # print 'img {0}'.format(img.shape)
        # print 'show_img {0}'.format(show_img.shape)
        # print 'inp_gray_img {0}'.format(inp_gray_img.shape)
        # print 'fg_img {0}'.format(fg_img.shape)
        # print 'model {0}'.format(model.pm.shape)

        start = time.time()
        utils.update_model(model, inp_gray_img)
        end = time.time()
        model_update_time = end - start

        start = time.time()
        utils.extract_fg(model, inp_gray_img, fg_img)
        end = time.time()
        extract_fg_time = end - start

        print 'Update Model time {0}'.format(model_update_time)
        print 'Extract fg time {0}'.format(extract_fg_time)

        cv2.imshow(text_inp, inp_gray_img)
        cv2.imshow(text_fg, fg_img)
        #exit()
        cv2.waitKey(50)



if __name__ == "__main__":
    main()
