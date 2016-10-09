# import numpy as np
# import cv2
from Classes import *
import utils
import time
import json
# import numpy
import subprocess
# import sys
import Tkinter as tk
from PIL import Image,  ImageTk
import platform

isPyPy = platform.python_implementation() == 'PyPy'

K = 5
SIGMA_INIT = 30
ALPHA = 0.01
SIGMA_THRESH = 5.0
T = 0.7

FILE_PATH = '../dt_passat.mpg'

def main ():
    text_inp = "Input Image"
    text_fg = "Foreground"

    # cv2.namedWindow(text_inp, cv2.CV_WINDOW_AUTOSIZE)
    # cv2.namedWindow(text_fg, cv2.CV_WINDOW_AUTOSIZE)
    #######

    probe_command = ('ffprobe', '-v', 'quiet', '-print_format', 'json', '-show_streams', FILE_PATH)

    process = subprocess.Popen(probe_command, stdout=subprocess.PIPE, stderr=None)
    video_info = json.load(process.stdout)
    process.stdout.close()
    process.wait()

    width = None
    height = None

    try:
        width, height = video_info['streams'][0]['width'], video_info['streams'][0]['height']
    except:
        raise RuntimeError("Error acquiring video dimensions from file '%s'." % FILE_PATH)

    print "Video is %s x %s" % (width, height)

    frame_size = width * height  # in Bytes

    # Protoze video je monochromaticke, pouzijeme pixelovy format rgb8, coz zmensi proud.

    load_command = ('ffmpeg', '-v', 'quiet', '-i', FILE_PATH, '-f', 'image2pipe', '-pix_fmt', 'rgb8','-vcodec', 'rawvideo', '-')

    process = subprocess.Popen(load_command, stdout=subprocess.PIPE, bufsize=10**8)

    #######

    sh_width = width / 2
    sh_height = height / 2

    # cv2.moveWindow(text_inp, 0, 0)
    # cv2.moveWindow(text_fg, sh_width + 10, 0)
    start = time.time()
    model = Model(sh_width, sh_height, K, SIGMA_INIT, ALPHA, SIGMA_THRESH, T)
    end = time.time()
    print 'Model Init time {0}'.format(end - start)

    # fg_img = np.zeros((sh_height, sh_width), np.uint8)

    original = tk.Tk()
    original.canvas = tk.Canvas(original, width = width, height = sh_height)
    original.canvas.grid(row = 0, column = 0)
    fg_img = Image.new('L', (sh_width, sh_height))
    fg_img = fg_img.transpose(Image.FLIP_TOP_BOTTOM)


    # computed = tk.Tk()
    # computed.canvas = tk.Canvas(computed, width = sh_width, height = sh_height)
    # computed.canvas.grid(row = 0, column = 0)

    def mainLoop():
        # while img:
        frame = process.stdout.read(frame_size)

        if frame:
            # print frame[0:width]
            img = Image.frombuffer('L', (width, height), frame)
            img = img.transpose(Image.FLIP_TOP_BOTTOM)
            inp_gray_img = img.resize((sh_width, sh_height), Image.ANTIALIAS)

            print 'PIXEL'
            print inp_gray_img.getpixel((sh_width/2, sh_height/2))
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

            if isPyPy:
                fg_img.save('pypyobrazek.bmp')
                # fg_img.show(title='titulek')
            else:
                # ########## Pro PYPY zakomentovat ###########
                original.phorig = ImageTk.PhotoImage(inp_gray_img)
                original.ph = ImageTk.PhotoImage(fg_img)
                original.canvas.create_image(sh_width/2, sh_height/2, image=original.phorig)
                original.canvas.create_image(sh_width + sh_width/2, sh_height/2, image=original.ph)
                original.canvas.update_idletasks()

            original.after(0, mainLoop)

    # mainLoop()
    # original.mainloop()
    # computed.mainloop()
    original.after(0, mainLoop)
    original.mainloop()





if __name__ == "__main__":
    main()
