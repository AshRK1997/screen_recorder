#redundant





from detect_screen_size import detect_screen_size
import cv2
import pyautogui
import numpy as np
import time
class screen_recoreder():

    def __init__(self,fps,filename):
        self.FPS =fps
        self.filename=filename
    def screen_rec(self,stop,pause,previous):
        global out,frames_count,start_time
        frames_count=0
        screen = detect_screen_size()
        SCREEN_SIZE = screen.detect_screen_siz()
        # define the codec
        print(SCREEN_SIZE)
        fourcc = cv2.VideoWriter_fourcc(*"XVID")
        # create the video write object
        out = cv2.VideoWriter(self.filename, fourcc, self.FPS, (SCREEN_SIZE))
        start_time=time.time()
        while True:

            try:
                frames_count = frames_count+1
                img = pyautogui.screenshot()
                frame = np.array(img)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                out.write(frame)
                #StopIteration(0.25)
            except:
                break
            if stop():
                print("FPS: ", frames_count / (time.time() - start_time))
                screen_recoreder(self.FPS,self.screen_rec_stop()).screen_rec_stop()
                break

    def screen_rec_stop(self):
        # make sure everything is closed when exited

        print(self.filename)
        cv2.destroyAllWindows()
        out.release()



if __name__=='__main__' :
    screen_recoreder(50,"output.avi").screen_rec(False,False,False)
