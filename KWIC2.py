import csv
from abc import ABC,abstractmethod

class LineStorage_Interface:
    @abstractmethod
    def __init__(self) -> None:
        pass
    @abstractmethod
    def store_input(self) -> None:
        pass
    @abstractmethod
    def getLine(line: int):
        pass

class Input_Interface:
    @abstractmethod
    def __init__(self, lineStorage: LineStorage_Interface) -> None:
        pass
    @abstractmethod
    def read_input() -> None:
        pass
    @abstractmethod
    def store_input() -> None:
        pass

class CircularShift_Interface:
    @abstractmethod
    def __init__(self, lineStorage: LineStorage_Interface) -> None:
        pass
    @abstractmethod
    def retrieve_lines(self) -> None:
        pass
    @abstractmethod
    def circular_shift(self) -> None:
        pass
    @abstractmethod
    def get_shifts(self) -> list:
        pass

class Alphabetize_Interface:
    @abstractmethod
    def __init__(self, circularShift: CircularShift_Interface) -> None:
        pass
    @abstractmethod
    def alphabetize(self) -> None:
        pass
    @abstractmethod
    def get_alphabetized_lines(self) -> list:
        pass
    @abstractmethod
    def get_circular_shift_by_index(self, index: i) -> list:
        pass

class Output_Interface:
    @abstractmethod
    def __init__(self, alphabetize: Alphabetize_Interface) -> None:
        pass
    

class csv_Input(Input_Interface):
    def __init__(self, lineStorage: LineStorage_Interface) -> None:
        self.lineStorage = lineStorage
    def read_input() -> None:
        pass
    pass

class LineStorage(LineStorage_Interface):
    def __init__(self) -> None:
        pass
    def store_input(self) -> None:
        pass
    def getLine(line: int):
        pass

class CircularShift(CircularShift_Interface):
    def __init__(self, lineStorage: LineStorage_Interface) -> None:
        pass
    def retrieve_lines(self) -> None:
        pass
    def circular_shift(self) -> None:
        pass
    def get_shifts(self) -> list:
        pass
    pass

class Alphabetize(Alphabetize_Interface):
    def __init__(self, circularShift: CircularShift_Interface) -> None:
        pass
    def alphabetize(self) -> None:
        pass
    def get_alphabetized_lines(self) -> list:
        pass
    def get_circular_shift_by_index(self, index: i) -> list:
        pass
    pass

class Output(Output_Interface):
    def __init__(self, alphabetize: Alphabetize_Interface) -> None:
        pass
    pass


class Master_Control:
    lineStorage = LineStorage()
    csvInput = csv_Input(lineStorage)
    circularShift = CircularShift(lineStorage)
    alphabetize = Alphabetize(circularShift)
    output = Output(alphabetize)
    