from typing import List

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from models.abstract_identifiable_image import Identifiable_Image
from models.base_image_model import Result_Image_Model
from models.image_index import Image_Index


class Multipage_Image_Fig(object):
    def __init__(self, image_models: List[Identifiable_Image]):
        self.image_models = image_models
        self.page_index = Image_Index(len(image_models) - 1)

    def setup(self):
        self.fig, self.ax = plt.subplots()
        plt.subplots_adjust(bottom=0.2)

        self.ax.set_title(self.image_models[self.page_index.index].image_name)

        self.aximg = self.ax.imshow(
            self.image_models[self.page_index.index].image_data, cmap="gray"
        )

        axprev = plt.axes([0.7, 0.05, 0.1, 0.075])
        axnext = plt.axes([0.81, 0.05, 0.1, 0.075])

        self.bnext = Button(axnext, "Next")
        self.bnext.on_clicked(self.next_image)
        self.bprev = Button(axprev, "Previous")
        self.bprev.on_clicked(self.prev_image)

    def next_image(self, event):
        index = self.page_index.next()
        print("Active next", index)
        self.aximg.set_data(self.image_models[index].image_data)
        self.ax.set_title(self.image_models[self.page_index.index].image_name)
        self.fig.canvas.flush_events()
        plt.draw()

    def prev_image(self, event):
        index = self.page_index.prev()
        print("Active prev", index)
        self.aximg.set_data(self.image_models[index].image_data)
        self.ax.set_title(self.image_models[self.page_index.index].image_name)
        self.fig.canvas.flush_events()
        plt.draw()
