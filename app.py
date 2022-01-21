import tkinter as UI
from controller.main_controller import Main_Controller
import config as cfg

class App():

    def __init__(self):
        self.root = UI.Tk()
        self.root.title("Spheroid Image Analyzer")

        screen_width: int = self.root.winfo_screenwidth()
        screen_height: int = self.root.winfo_screenheight()
        
        cfg.window_width = 600
        cfg.window_height = 200
        

        self.root.geometry(f"{cfg.window_width}x{cfg.window_height}")

        self.main_view = Main_Controller(self.root)

        self.root.mainloop()


if __name__ == "__main__":
    app = App()
