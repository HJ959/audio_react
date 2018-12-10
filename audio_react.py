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
import pyaudio
import pygame
# -----------------------------------------------------------------------------
def rmsFunction():
    # Creates a generator that can iterate rms values
    CHUNK = 1024
    WIDTH = 2
    CHANNELS = 2
    RATE = 44100
    colourMax = 255
    p = pyaudio.PyAudio()

    stream = p.open(format=p.get_format_from_width(WIDTH),
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    output=True,
                    frames_per_buffer=CHUNK)
    time.sleep(1)
    while True:
        data = stream.read(CHUNK, exception_on_overflow = False)
        #stream.write(data, CHUNK)
        rms = audioop.rms(data, 2)
        # Scale the rms value to be within 0-255
        rmsS = rms * 0.014
        if rmsS < colourMax:
            yield rmsS

def main():
    pygame.init()
    randomNumber = random.seed()
    rms = rmsFunction()

    #create fullscreen display
    screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
    screenW = screen.get_width()
    screenH = screen.get_height()

    # Iterate the rms value and update the pyGame display
    for rmsValue in rms:
        rmsInt = int(rmsValue)
        sOneW = random.getrandbits(10)
        sOneH = random.getrandbits(10)
        sTwoW = random.getrandbits(10)
        sTwoH = random.getrandbits(10)
        sThreeW = random.getrandbits(10)
        sThreeH = random.getrandbits(10)

        posOneW = (sOneW + screenW) * 0.2
        posOneH = (sOneH + screenH) * 0.2
        posTwoW = (sTwoW + screenW) * 0.5
        posTwoH = (sTwoH + screenH) * 0.5
        posThreeW = (sThreeW + screenW) * 0.5
        posThreeH = (sThreeH + screenH) * 0.5

        colourRand = random.getrandbits(8)

        # Draw polygons to the screen
        if rmsValue > 100:
            pygame.draw.polygon(screen, 
                               ((rmsInt+colourRand)*0.3, rmsInt, rmsInt), 
                                 ((posOneW,posOneH), (posTwoW,posTwoH), (posThreeW,posThreeH)))

        pygame.display.update()
        time.sleep(0.01)
        pygame.Surface.fill(screen, (0,0,0))

        # check for quit events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                p.terminate()
                pygame.quit()
                stream.stop_stream()
                stream.close()
            if event.type == pygame.KEYDOWN:
                p.terminate()
                pygame.quit()
                stream.stop_stream()
                stream.close()

if __name__ == "__main__": main()
