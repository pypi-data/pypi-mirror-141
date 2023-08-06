import os

from rkt_lib_toolkit.tool import Tool, Singleton

obj = Tool()


class FakeClass(metaclass=Singleton):
    def __init__(self):
        self.name = "singleton"


class TestTool:
    def test_formatted_from_os(self):
        assert obj.formatted_from_os(os.getcwd()).endswith("\\") if os.name == "nt" else obj.formatted_from_os(os.getcwd()).endswith("/")

    def test_get_cwd(self):
        assert obj.get_cwd() == f"{os.getcwd()}\\" if os.name == "nt" else f"{os.getcwd()}/"

    def test_get_dir(self):
        assert obj.get_dir("tool") == f"{os.getcwd()}\\tool\\" if os.name == "nt" else f"{os.getcwd()}/tool/"


class TestSingleton:
    def test_singleton(self):
        obj_1 = FakeClass()
        obj_2 = FakeClass()
        assert obj_1 == obj_2
