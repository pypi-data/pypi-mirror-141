import unittest

from fastforward.__test__.metric.benchmark import benchmark
from fastforward.__test__.metric.profiler import Profiler
from fastforward.engine.listener.onnx_listener import OnnxListener
from fastforward.model_for_summarization import ModelForSummarization


class ModelForSummarizationTest(unittest.TestCase):

    def test_distilbart_cnn_12_6_samsun(self):
        text = """Please close this task on success with closing reason "Direct solved" or "Solved" otherwise with an 
        other reason (e.g. "Aborted"). Create a new doorplate for room C 205 Start Date: 01.09.2019 Employee: 
        Max Mustermann Comment:"""

        with Profiler():
            listeners = [OnnxListener(enable_cpu_mem_arena=False)]
            model = ModelForSummarization.restore("x-and-y", "distilbart-cnn-12-6-samsum", "1.0.0", "cpu-fp32",
                                                  listeners=listeners)
            benchmark("distilbart", lambda: model(text, num_beams=2))

    def test_pegasus_xsum(self):
        text = """The tower is 324 metres (1,063 ft) tall, about the same height as an 81-storey building, and the 
        tallest structure in Paris. Its base is square, measuring 125 metres (410 ft) on each side. During its 
        construction, the Eiffel Tower surpassed the Washington Monument to become the tallest man-made structure in 
        the world, a title it held for 41 years until the Chrysler Building in New York City was finished in 1930. 
        It was the first structure to reach a height of 300 metres. Due to the addition of a broadcasting aerial at 
        the top of the tower in 1957, it is now taller than the Chrysler Building by 5.2 metres (17 ft). Excluding 
        transmitters, the Eiffel Tower is the second tallest free-standing structure in France after the Millau 
        Viaduct."""

        with Profiler():
            onnx_model = ModelForSummarization.restore("x-and-y", "pegasus-xsum", "1.0.0")
            print(onnx_model(text))

    def test_t5_small(self):
        text = """summarize: The tower is 324 metres (1,063 ft) tall, about the same height as an 81-storey building, and the 
        tallest structure in Paris. Its base is square, measuring 125 metres (410 ft) on each side. During its 
        construction, the Eiffel Tower surpassed the Washington Monument to become the tallest man-made structure in 
        the world, a title it held for 41 years until the Chrysler Building in New York City was finished in 1930. 
        It was the first structure to reach a height of 300 metres. Due to the addition of a broadcasting aerial at 
        the top of the tower in 1957, it is now taller than the Chrysler Building by 5.2 metres (17 ft). Excluding 
        transmitters, the Eiffel Tower is the second tallest free-standing structure in France after the Millau 
        Viaduct."""

        with Profiler():
            onnx_model = ModelForSummarization.restore("x-and-y", "t5-small", "1.0.0")
            print(onnx_model(text))
