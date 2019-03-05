# ----------------------------
# Audio reactive shapes script
# Author: Henry James
# email: henryjaames@gmail.com
# ----------------------------

#import python3 std modules
import wave
import audioop
import time
import random
#import python3 third party
import numpy as np
import pyaudio
import pygame as pyg
import cv2

# -----------------------------------------------------------------------------
def rmsFunction():
    # Creates a generator that can iterate rms values
    CHUNK = 1024
    WIDTH = 2
    CHANNELS = 2
    RATE = 44100
    colourMax = 255

    p = pyaudio.PyAudio()

    try:
        stream = p.open(format=p.get_format_from_width(WIDTH),
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        output=True,
                        frames_per_buffer=CHUNK)

        time.sleep(1)
        while True:
            data = stream.read(CHUNK, exception_on_overflow = False)
            rms = audioop.rms(data, 2)
            # Scale the rms value to be within 0-255
            rmsS = rms * 0.014
            if rmsS < colourMax:
                yield rmsS
    finally:
        p.terminate()
        stream.stop_stream()
        stream.close()

# ----------------------------------------------------------------------------
def draw_func(pos_1_x,
              pos_1_y,
              pos_2_x,
              pos_2_y,
              pos_3_x,
              pos_3_y,
              colourRand,
              rmsInt):
    width = rmsInt
    pyg.draw.polygon(screen,
                        ((rmsInt+colourRand)*0.3, rmsInt, rmsInt),
                        ((pos_1_x, pos_1_y),
                         (pos_2_x, pos_2_y),
                         (pos_3_x, pos_3_y)),
                        width)

    pyg.display.update()

    if pos_3_x < LIMIT:
        draw_func((pos_1_x-(pos_3_x/2), pos_1_y-(pos_3_y/2)),
                  (pos_2_x-(pos_3_x/2), pos_2_y-(pos_3_y/2)),
                  (pos_3_x-(pos_1_x/2), pos_3_y-(pos_1_y/2)),
                  colourRand,
                  rmsInt)
        draw_func((pos_1_x+(pos_3_x/2), pos_1_y+(pos_3_y/2)),
                  (pos_2_x-(pos_3_x/2), pos_2_y-(pos_3_y/2)),
                  (pos_3_x-(pos_1_x/2), pos_3_y-(pos_1_y/2)),
                  colourRand,
                  rmsInt)
        draw_func((pos_1_x+(pos_3_x/2), pos_1_y+(pos_3_y/2)),
                  (pos_2_x+(pos_3_x/2), pos_2_y+(pos_3_y/2)),
                  (pos_3_x-(pos_1_x/2), pos_3_y-(pos_1_y/2)),
                  colourRand,
                  rmsInt)

# ----------------------------------------------------------------------------
def webcam_func(cap):
    # Capture frame by frame
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
    frame = np.rot90(frame)
    webcam_frame = pyg.surfarray.make_surface(frame)
    return(webcam_frame)
# ----------------------------------------------------------------------------
if __name__ == "__main__":
    LIMIT = 200
    gain_ = 1000

    # init pyg, random and rms rmsFunction
    pyg.init()
    time.sleep(1)
    randomNumber = random.seed()
    rms = rmsFunction()

    # get camera object
    cap = cv2.VideoCapture(0)

    #create fullscreen display
    screen = pyg.display.set_mode((0,0), pyg.FULLSCREEN)
    s_W = screen.get_width()
    s_H = screen.get_height()

    # Hide the mousey
    pyg.mouse.set_visible(False)

    # Iterate the rms value and update the pyg display
    for rmsValue in rms:
        colourRand = random.getrandbits(8)
        # webcam rmsFunction
        webcam = webcam_func(cap)
        screen.blit(webcam, (0,0))

        # Draw polygons to the screen
        if rmsValue > 25:
            rmsInt = int(rmsValue)
            pos_1_x = random.getrandbits(10) - (s_W/2)
            pos_1_y = random.getrandbits(8) + (s_H/2)
            pos_2_x = random.getrandbits(8) + (s_W/2)
            pos_2_y = random.getrandbits(10) - (s_H/2)
            pos_3_x = random.getrandbits(10) + (s_W/2)
            pos_3_y = random.getrandbits(10) + (s_H/2)

            screen.blit(webcam, (0,0))

            draw_func(pos_1_x, pos_1_y,
                      pos_2_x, pos_2_y,
                      pos_3_x, pos_3_y,
                      colourRand,
                      rmsInt)
            pyg.display.update()

        pyg.display.update()
        pyg.Surface.fill(screen, (0,0,0))

        time.sleep(0.01)

        # check for quit events
        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                pyg.quit()
                cap.release()
                cv2.destroyAllWindows()
            if event.type == pyg.KEYDOWN:
                pyg.quit()
                cap.release()
                cv2.destroyAllWindows()
# ----------------------------------------------------------------------------
