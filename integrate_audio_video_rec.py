from threading import Thread
from audio_rec import audio_rec
from screen_rec_1 import screen_recoreder
import subprocess
import shutil
import sys, os

#TODO: if a file is already present don't remove it
# TODO: Remove passing of permanent parameters such as filename within the program as they remain same throught the program

def stop_everything(filename):
    global stop_threads, pause_threads, play_now, FPS

    stop_threads = True
    pause_threads = False
    play_now = False

    screen_recoreder().screen_rec_play(play_now)
    screen_recoreder().screen_rec_pause(pause_threads)
    screen_recoreder().screen_rec_stop(stop_threads)
    audio_rec().audio_rec_stop(stop_threads)
    audio_rec().audio_rec_play(play_now)
    audio_rec().audio_rec_pause(pause_threads)

    t2.join()
    t1.join()

    if os.path.isfile("output.mp4"):
        os.remove("output.mp4")

    if abs(FPS_calc - 35) >= 0.01:  # If the fps rate was higher/lower than expected, re-encode it to the expected
        print("Re-encoding")

        cmd = "ffmpeg -i temp_video.avi -f mp4 temp_video.mp4"
        subprocess.call(cmd,shell=True)

        cmd = "ffmpeg -y -r "+str(FPS_calc)+" -i temp_video.mp4 temp_video2.mp4"
        subprocess.call(cmd, shell=True)

        cmd = "ffmpeg -i temp_audio.wav temp_audio.mp4"
        subprocess.call(cmd,shell=True)

        cmd = "ffmpeg -i temp_video2.mp4 -i temp_audio.mp4 -c copy output.mp4"
        subprocess.call(cmd, shell=True)

        if os.path.isfile("temp_video2.mp4"):
            os.remove("temp_video2.mp4")


    else:
        print("Normal recording\nMuxing")

        cmd = "ffmpeg -i temp_video.avi -f mp4 temp_video.mp4"
        subprocess.call(cmd, shell=True)

        cmd = "ffmpeg -i temp_audio.wav temp_audio.mp4"
        subprocess.call(cmd, shell=True)

        cmd = "ffmpeg -i temp_video.mp4 -i temp_audio.mp4 -c copy output.mp4"
        subprocess.call(cmd, shell=True)

    #cmd = "ffmpeg -i temp_video.avi -i temp_audio.wav -vcodec copy -acodec copy output.avi"
    #subprocess.call(cmd, shell=True)

    if os.path.isfile("temp_audio.wav"):
        os.remove("temp_audio.wav")

    if os.path.isfile("temp_video.avi"):
        os.remove("temp_video.avi")

    if os.path.isfile("temp_audio.mp4"):
        os.remove("temp_audio.mp4")

    if os.path.isfile("temp_video.mp4"):
        os.remove("temp_video.mp4")

    if os.path.isfile(filename):
        os.remove(filename)
    try:
        shutil.copy("output.mp4", filename)
        os.remove("output.mp4")
    except IOError as e:
        print("Unable to copy file. %s" % e)
    except:
        print("Unexpected error:", sys.exc_info())


def pause_everything():
    global pause_threads, play_now

    pause_threads = True
    play_now = False

    screen_recoreder().screen_rec_play(play_now)
    screen_recoreder().screen_rec_pause(pause_threads)
    audio_rec().audio_rec_play(play_now)
    audio_rec().audio_rec_pause(pause_threads)


def play_now_func():
    global play_now, pause_threads

    play_now = True
    pause_threads = False

    screen_recoreder().screen_rec_play(play_now)
    screen_recoreder().screen_rec_pause(pause_threads)
    audio_rec().audio_rec_play(play_now)
    audio_rec().audio_rec_pause(pause_threads)


def record_everything(FPS):
    global stop_threads, pause_threads, play_now, filename, t1, t2

    stop_threads = False
    pause_threads = False
    play_now = False

    screen_recoreder().screen_rec_play(play_now)
    screen_recoreder().screen_rec_pause(pause_threads)
    screen_recoreder().screen_rec_stop(stop_threads)
    audio_rec().audio_rec_stop(stop_threads)
    audio_rec().audio_rec_play(play_now)
    audio_rec().audio_rec_pause(pause_threads)

    t2 = Thread(target=screen_recoreder().screen_rec_init, args=(lambda: stop_threads, FPS, "temp_video.avi",))
    t1 = Thread(target=audio_rec().audio_rec_start, args=(lambda: stop_threads, "temp_audio.wav"))

    t2.start()
    t1.start()

def set_fps(fps):
    global FPS_calc
    FPS_calc = fps

if __name__ == '__main__':
    record_everything(35)
    a = input()
    if a == "q":
        stop_everything("trial.avi")

