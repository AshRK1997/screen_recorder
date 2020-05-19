import pyaudio

rec_play = False
rec_pause = False
rec_stop = False

#TODO: Remove passing of permanent parameters such as filename within the program as they remain same throught the program
Filename = "temp_audio.wav"

class audio_rec():

    def __init__(self):

        self.chunk = 512  # Record in chunks of 1024 samples
        self.sample_format = pyaudio.paInt16  # 16 bits per sample
        self.channels = 2
        self.fs = 44100  # Record at 44100 samples per second
        self.seconds = 3

    def audio_rec_stop(self, stop):
        global rec_stop
        rec_stop = stop


    def audio_rec_pause(self, pause):
        global rec_pause
        rec_pause = pause


    def audio_rec_play(self, play):
        global rec_play
        rec_play = play


    def audio_rec_start(self, stop, filename):
        import pyaudio

        global p,stream,frames, Filename
        Filename = filename
        if rec_play:

            nothing = 0
        elif rec_pause:
            nothing = 0
        else:
            p = pyaudio.PyAudio()  # Create an interface to PortAudio
            print('audio: init')
            stream = p.open(format=self.sample_format,
                            channels=self.channels,
                            rate=self.fs,
                            frames_per_buffer=self.chunk,
                            input=True)

            frames = []  # Initialize array to store frames
        print("audio: record/play")

        while True:
            # Store data in chunks
            data = stream.read(self.chunk,  exception_on_overflow = False)
            frames.append(data)
            if rec_stop:
                print("audio rec stop primary")
                audio_rec().audio_rec_close_all()
                break
            if rec_pause:
                print("audio pause")
                break

        import time

        while True:
            if rec_stop:
                print("audio secondary stop")
                audio_rec().audio_rec_close_all()
                break
            elif rec_play and not rec_pause:
                audio_rec().audio_rec_start(False,Filename)
            time.sleep(0.001)


    def audio_rec_close_all(self):
        import wave
        print("closing audio_Rec")
        stream.stop_stream()
        stream.close()
        # Terminate the PortAudio interface
        p.terminate()
        # Save the recorded data as a WAV file

        wf = wave.open(Filename, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(p.get_sample_size(self.sample_format))
        wf.setframerate(self.fs)
        wf.writeframes(b''.join(frames))
        wf.close()


if __name__=='__main__':
    a=audio_rec()
    a.audio_rec_start(False, "temp_audio.wav")