import concurrent.futures
import threading
import time
import tkinter as UI
from typing import Callable, List, Type

from analysis_tools.abstract_analysis_method import Analysis_Method_Protocol

from models.analysis_results.abstract_analysis_result import Analysis_Result_Protocol
from models.image.image_model import Image_Model


class Analysis_Task(object):
    def __init__(self, parent_view: UI.Frame, callback: Callable) -> None:
        self.is_running = False
        self.parent_view = parent_view
        self.callback = callback
        self.analysis_methods: List[Type[Analysis_Method_Protocol]] = []
        self.analysis_results: List[Analysis_Result_Protocol] = []

    def add_analysis_method(self, analysis_method: Type[Analysis_Method_Protocol]):
        self.analysis_methods.append(analysis_method)

    def run_analysis(self, image_models: List[Image_Model]):
        self.parent_view.after(2000, self._finished_check)
        self.calculation_thread = threading.Thread(target=lambda: self._start(image_models))
        self.calculation_thread.start()

    def _start(self, image_models: List[Image_Model]):
        self.start_time = time.time()
        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = [
                executor.submit(method.calculate, image_models)
                for method in self.analysis_methods
            ]
            for f in concurrent.futures.as_completed(results):
                self.finished_analysis_callback(f.result())

    def finished_analysis_callback(self, result):
        print("--- %s seconds ---" % (time.time() - self.start_time))
        self.analysis_results.append(result)

    def _finished_check(self):
        if not self.calculation_thread.is_alive():
            print("Results:", self.analysis_results)
            self.callback(self.analysis_results)
        else:
            self.parent_view.after(200, self._finished_check)
