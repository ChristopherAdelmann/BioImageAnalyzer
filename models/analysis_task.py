from typing import Callable, List, Type
from concurrent.futures import Future
import concurrent.futures
from analysis_tools.abstract_analysis_method import Analysis_Method
from models.analysis_results.abstract_analysis_result import Analysis_Result_Protocol
from models.image.image_model import Image_Model
import threading
import tkinter as UI
import time

class Analysis_Task(object):
    def __init__(self, parent_view: UI.Frame, callback: Callable, image_models: List[Image_Model]) -> None:
        self.is_running = False
        self.parent_view = parent_view
        self.callback = callback
        self.image_models = image_models
        self.analysis_methods: List[Type[Analysis_Method]] = []
        self.analysis_results: List[Analysis_Result_Protocol] = []

    def add_analysis_method(self, analysis_method: Type[Analysis_Method]):
        self.analysis_methods.append(analysis_method)

    def run_analysis(self):
        self.parent_view.after(2000, self._finished_check)
        self.calculation_thread= threading.Thread(target=self._start)
        self.calculation_thread.start()
        
    def _start(self):
        self.start_time = time.time()
        with concurrent.futures.ProcessPoolExecutor() as executor:
            results = [executor.submit(method.calculate, self.image_models) for method in self.analysis_methods]
            for f in concurrent.futures.as_completed(results):
                self.finished_analysis_callback(f.result())
                
    def finished_analysis_callback(self, result):
        print("--- %s seconds ---" % (time.time() - self.start_time))
        self.analysis_results.append(result)
        
    def _finished_check(self):
        if not self.calculation_thread.is_alive():
            self.callback(self.analysis_results)
        else:
            self.parent_view.after(200, self._finished_check)