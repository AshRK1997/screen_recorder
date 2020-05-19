from detect_screen_size import detect_screen_size
import cv2
import numpy as np
import time
from mss import mss
import pyautogui
import integrate_audio_video_rec

#TODO: Remove passing of permanent parameters such as filename within the program as they remain same throught the program


rec_pause = False
rec_play = False
rec_stop = False

# Radius of circle
radius = 10

# Blue color in BGR
color = (255, 0, 0)

# Line thickness of 2 px
thickness = 2

#to check if it was passed previously
previously_pause = False

class screen_recoreder():

    def screen_rec_stop(self, stop):
        global rec_stop
        rec_stop = stop


    def screen_rec_pause(self, pause):
        global rec_pause
        rec_pause = pause

    def screen_rec_play(self, play):
        global rec_play
        rec_play = play



    def screen_rec_init(self, stop, FPS,filename):


        global out, frames_count, start_time, sct, FPS_calc, total_duration, previously_pause

        if rec_play:
            previously_pause = False
            start_time = time.time()
        elif rec_pause:
            nothing = 0
        elif rec_stop:
            nothing = 0
        else:
            total_duration = 0
            frames_count = 0
            print("video: init")
            screen = detect_screen_size()
            x, y = screen.detect_screen_siz()
            fourcc = cv2.VideoWriter_fourcc(*'DIVX')

            # create the video write object
            out = cv2.VideoWriter(filename, fourcc, FPS, tuple([x, y]))
            start_time = time.time()
            sct = mss()

        print("video: record/play")
        while True:

            try:
                frames_count = frames_count + 1
                sct_img = np.array(sct.grab(sct.monitors[1]))
                m_x, m_y = pyautogui.position()

                sct_img = np.flip(sct_img[:, :, :3], 2)
                frame = cv2.cvtColor(sct_img, cv2.COLOR_BGR2RGB)

                center_coordinates = (m_x, m_y)
                image = cv2.circle(frame, center_coordinates, radius, color, thickness)
                image = cv2.circle(image, center_coordinates, 6, (0, 0, 255), -1)

                out.write(image)

            except:
                # TODO:creat an alert
                print("error occured")
                break

            if rec_stop:
                print("video: stop")
                if not previously_pause:
                    total_duration = total_duration + (time.time() - start_time)
                FPS_calc = frames_count / total_duration
                print("FPS: ", FPS_calc)
                print("Time: ",total_duration)
                screen_recoreder().screen_rec_close_all()
                previously_pause = False
                break


            if rec_pause:
                print("video pause")
                previously_pause = True
                total_duration = total_duration + (time.time() - start_time)
                break


        while True:
            if rec_stop:
                screen_recoreder().screen_rec_close_all()
                print("video sec close")
                total_duration = 0
                break
            elif rec_play and not rec_pause:
                screen_recoreder().screen_rec_init(False, FPS,filename)
            time.sleep(0.001)






    def screen_rec_close_all(self):
        # make sure everything is closed when exited
        print("video closing")
        cv2.destroyAllWindows()
        out.release()
        screen_recoreder().set_fps_calc()

    #sets calculated FPS for video correction
    def set_fps_calc(self):
        global FPS_calc
        integrate_audio_video_rec.set_fps(FPS_calc)


if __name__ == '__main__':
    screen_recoreder().screen_rec_init(False,35,"trial.avi")
