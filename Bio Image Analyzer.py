import tkinter as UI

import config as cfg
from controller.main_controller import Main_Controller

class App:
    def __init__(self):
        self.root = UI.Tk()
        self.root.title("Bio Image Analyzer")

        cfg.window_width = 500
        cfg.window_height = 150

        self.root.geometry(f"{cfg.window_width}x{cfg.window_height}")

        self.main_controller = Main_Controller(self.root)

        self.root.mainloop()


if __name__ == "__main__":
    app = App()

    