class detect_screen_size():
    def detect_os(self):
        import platform
        os_name = platform.system()
        return os_name

    def detect_screen_siz(self):

        import tkinter as tk
        root = tk.Tk()
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        return screen_width, screen_height





