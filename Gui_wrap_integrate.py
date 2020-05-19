#TODO: Frame setting, file name filling blank spaces
#TODO: Zoom capabilities
#TODO: Remove passing of permanent parameters such as filename within the program as they remain same throught the program
#TODO: Keyboard Shortcuts
#TODO: Support/Donate

from tkinter import *
from tkinter.ttk import *
from detect_screen_size import detect_screen_size
from PIL import Image, ImageTk
import tkinter as tk
import integrate_audio_video_rec


LOGO_PNG_PATH="pic/logo.png"
LOGO_PATH="pic/logo.ico"
BG_PATH = 'pic/bg.png'
LOGO_LINUX_PATH="@pic/logo.XBM"
LOGO_GIF_PATH="pic/logo.gif"

#for configuring button controls
Stopped_recording = False
play_rec = True

#default FPS for screen recording
FPS = 35

#window config
WIDTH, HEIGHT = 350, 100

#when hit play/pause button
def play():
    global play_rec, Stopped_recording

    if Stopped_recording:
        print("Please press record button to button to start recording")
        # TODO: Alert message to create
    #if playrec is true then, on hitting pause buttton, video rec will pause and when pressed again vice versa
    elif play_rec:
        play_btn.config(image=img_play)
        play_rec = False
        print("pause hit")
        integrate_audio_video_rec.pause_everything()
    else:
        play_btn.config(image=img_pause)
        play_rec = True
        print("play hit", play_rec)
        integrate_audio_video_rec.play_now_func()


#when hit stop recording button
def stop():
    global play_rec, Stopped_recording
    if Stopped_recording:
        print("Please press record button to button to start recording")
        #TODO: Alert message to create
    else:
        Stopped_recording = True
        print("button stop")
        integrate_audio_video_rec.stop_everything("trial.mp4")
        if not play_rec:
            play_btn.config(image=img_play)


#when hit record button
def record():
    global Stopped_recording, play_rec
    print("button rec")
    Stopped_recording = False
    play_rec = True
    integrate_audio_video_rec.record_everything(FPS)



root = Tk()
#FPS = fps_for_screenrec()
#root.geometry('{}x{}'.format(WIDTH, HEIGHT))
root.resizable(0, 0)
root.style = Style()
#('winnative', 'clam', 'alt', 'default', 'classic', 'vista', 'xpnative')
root.style.theme_use("clam")
if detect_screen_size().detect_os()=="Linux":
    #root.tk.call('wm', 'iconphoto', root._w, LOGO_PATH)
    dfg=1
else:
    root.iconbitmap(default=LOGO_PATH)
root.title("Screenvideographer")


frame_display = tk.Frame(relief=FLAT)
#label = tk.Label(master=frame_display, image=LOGO_GIF_PATH, text="Screen Videographer", compound="left")

label = tk.Label(master=frame_display, text="Screen Videographer")
label.pack()
canvas = Canvas(root, width = 250, height = 100)
canvas.pack(side=TOP)
#img = PhotoImage(file=LOGO_PNG_PATH)
img = ImageTk.PhotoImage(Image.open(LOGO_PNG_PATH),master=canvas)
canvas.create_image(125,60, image=img)


frame_display.pack()
frame_controls = tk.Frame(relief=FLAT)

img_record=PhotoImage(file="pic/gui_controls/record.png")
img_pause=PhotoImage(file="pic/gui_controls/symbol.png")
img_stop=PhotoImage(file="pic/gui_controls/stop.png")
img_play=PhotoImage(file="pic/gui_controls/play.png")

Button(master=frame_controls,width=35,image=img_record,command=record).pack(side=LEFT,padx=7,pady=4)

play_btn = Button(master=frame_controls,width=35,image=img_play,command=play)
play_btn.pack(side=LEFT,padx=7,pady=4)

Button(master=frame_controls,width=35,image=img_stop,command=stop).pack(side=RIGHT,padx=7,pady=4)

frame_controls.pack()
root.mainloop()
