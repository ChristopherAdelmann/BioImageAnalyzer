from typing import List

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from models.image.abstract_identifiable_image import Identifiable_Image_Protocol
from models.image.image_index import Image_Index


class Multipage_Image_Fig(object):
    def __init__(self, image_models: List[Identifiable_Image_Protocol]):
        self.image_models = image_models
        self.page_index = Image_Index(len(image_models) - 1)

    def setup(self):
        self.fig, self.ax = plt.subplots()
        plt.subplots_adjust(bottom=0.2)

        self.ax.set_title(self.image_models[self.page_index.index].image_description)

        self.aximg = self.ax.imshow(
            self.image_models[self.page_index.index].image_data, cmap="gray"
        )

        axprev = plt.axes([0.7, 0.05, 0.1, 0.05])
        axnext = plt.axes([0.81, 0.05, 0.1, 0.05])
        ax_slider = plt.axes([0.12, 0.06, 0.5, 0.0225])

        self.bnext = Button(axnext, "Next")
        self.bnext.on_clicked(self.next_image)
        self.bprev = Button(axprev, "Previous")
        self.bprev.on_clicked(self.prev_image)
        self.image_slider = plt.Slider(
            ax=ax_slider,
            label="Slice",
            valmin=1,
            valmax=self.page_index.max_index + 1,
            valinit=1,
            valstep=1,
            orientation="horizontal",
        )
        self.image_slider.on_changed(self.slider_update)

    def next_image(self, event):
        index = self.page_index.next()
        self.aximg.set_data(self.image_models[index].image_data)
        self.ax.set_title(self.image_models[self.page_index.index].image_name)
        self.fig.canvas.flush_events()
        plt.draw()

    def prev_image(self, event):
        index = self.page_index.prev()
        self.aximg.set_data(self.image_models[index].image_data)
        self.ax.set_title(self.image_models[self.page_index.index].image_description)
        self.fig.canvas.flush_events()
        plt.draw()

    def slider_update(self, value):
        index = round(value) - 1
        self.page_index.index = index
        self.aximg.set_data(self.image_models[index].image_data)
        self.ax.set_title(self.image_models[index].image_description)
        self.fig.canvas.flush_events()
        plt.draw()
