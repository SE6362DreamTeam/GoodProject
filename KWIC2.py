import csv
from abc import ABC,abstractmethod

#Interface for the LineStorage class
class LineStorage_Interface:
    @abstractmethod
    def __init__(self) -> None:
        pass
    @abstractmethod
    def store_input(self, lineDict: dict) -> None:
        pass
    @abstractmethod
    def getLine(self, line: int):
        pass
    @abstractmethod
    def getAllLines(self):
        pass

#Interface for the Input class
class Input_Interface:
    @abstractmethod
    def __init__(self, lineStorage: LineStorage_Interface) -> None:
        pass
    @abstractmethod
    def read_input(self) -> None:
        pass
    @abstractmethod
    def store_input(self) -> None:
        pass

#Interface for the CircularShift class
class CircularShift_Interface:
    @abstractmethod
    def __init__(self, lineStorage: LineStorage_Interface) -> None:
        pass
    @abstractmethod
    def retrieve_and_save_lines(self) -> None:
        pass
    @abstractmethod
    def circular_shift(self) -> None:
        pass
    @abstractmethod
    def shift_current_line(self, current_line: str) -> str:
        pass
    @abstractmethod
    def get_shifted_Lines(self) -> list:
        pass

#Interface for the Alphabetize class
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
    def get_circular_shift_by_index(self, index: int) -> list:
        pass

#Interface for the Output class
class Output_Interface:
    @abstractmethod
    def __init__(self, alphabetize: Alphabetize_Interface) -> None:
        pass
    @abstractmethod
    def get_output(self):
        pass
    
#Class for reading the input from a csv
class csv_Input(Input_Interface):
    def __init__(self, lineStorage: LineStorage_Interface) -> None:
        self.lineStorage = lineStorage
        self.file_lines = None
    def read_input(self, file_name) -> None:
        # Create a dictionary to hold each line we read in
        # Key: search phrase
        # Value: list of URLs for that search phrase
        file_lines = dict()

        # Open the input file (csv format)
        with open(file_name, "r") as f:
            reader = csv.reader(f, delimiter=",")

            # Read file line by line
            for i, line in enumerate(reader):
                # Do not count the column header row
                if i == 0:
                    continue
                else:
                    # For each search phrase that has n words, there are n URLs associated with it
                    # term_length will equal how many URLs will be added as a value for the current search phrase
                    term_length = len(line[0].split())
                    # Create a new entry in the dictionary if there is not one for this search phrase already
                    if file_lines.get(line[0]) == None:
                        # Key is the query term
                        # Value is a list of URLs for this search phrase
                        file_lines[line[0]] = list()
                    # Go through each URL of the current line and add it to the value
                    for j in range(1, term_length+1):
                        (file_lines[line[0]]).append(line[j])
        self.file_lines = file_lines
    #Stores the input lines into the lineStorage object instance
    def store_input(self) -> None:
        self.lineStorage.store_input(self.file_lines)

#Class for keeping all lines from a site
class LineStorage(LineStorage_Interface):
    def __init__(self) -> None:
        self.file_lines = None
    #Stores the input into the file_lines variable
    def store_input(self, line_Dict: dict) -> None:
        self.file_lines = line_Dict
    #Gets the line from the given index
    def getLine(self, lineIndex: int):
        return list(self.file_lines)[lineIndex]
    #Returns all lines
    def getAllLines(self):
        return self.file_lines

#Class for circularly shifting lines
class CircularShift(CircularShift_Interface):
    def __init__(self, lineStorage: LineStorage_Interface) -> None:
        self.lineStorage = lineStorage
        self.file_lines = None
        self.shifted_lines = None
    #Retrieves the lines form line storage and saves them into this object instance
    def retrieve_and_save_lines(self) -> None:
        self.file_lines = list(self.lineStorage.getAllLines())
    #Shifts every line stored and saves them
    def circular_shift(self) -> None:
        newLines = []
        for line in self.file_lines:
            shiftedLines = self.shift_current_line(line)
            if(shiftedLines != None):
                for shiftedLine in shiftedLines:
                    newLines.append(shiftedLine)
        self.shifted_lines = newLines
    #Shifts a single line
    def shift_current_line(self, current_line: str) -> str:
        # Split the current line by spaces
        words = current_line.split(" ")

        # If there are n-1 words in a line, then n circular shifts must occur for the line 
        # to return to its original state
        num_iterations = len(words)
        # Iterate until n iterations is reached (should have original line at nth iteration)
        shiftedLines = []
        for i in range(num_iterations):
            # Remove the first word in words array
            popped_term = words.pop(0)
            # Add it to the end of words array
            words.append(popped_term)
            # Join the words array with spaces and store it in line (one whole string now)
            line = " ".join(words)
            shiftedLines.append(line)
        return shiftedLines
    #Returns all shifted lines
    def get_shifted_Lines(self) -> list:
        return list(self.shifted_lines)

#Class for alphabetizing the lines
class Alphabetize(Alphabetize_Interface):
    def __init__(self, circularShift: CircularShift_Interface) -> None:
        self.circularShift = circularShift
        self.file_lines = None
        self.sorted_shifts = None
    #Alphabetizes the circular shifts
    def alphabetize(self) -> None:
        # Sort all circular shifts alphabetically and store in a new list
        self.file_lines = self.circularShift.get_shifted_Lines()
        self.sorted_shifts = sorted(self.file_lines, key=lambda s: s.lower())
    #Returns the alphabetized lines
    def get_alphabetized_lines(self) -> list:
        return self.sorted_shifts
    #Gets a certain line out of the array
    def get_circular_shift_by_index(self, index: int) -> list:
        return self.sorted_shifts[index]

#Returns the alphabetized array
class Output(Output_Interface):
    def __init__(self, alphabetize: Alphabetize_Interface) -> None:
        self.alphabetize = alphabetize
    def get_output(self):
        return self.alphabetize.get_alphabetized_lines()


class Master_Control:
    #Initializes all objects
    def __init__(self) -> None:
        lineStorage = LineStorage()
        self.csvInput = csv_Input(lineStorage)
        self.circularShift = CircularShift(lineStorage)
        self.alphabetize = Alphabetize(self.circularShift)
        self.output = Output(self.alphabetize)
    #Takes in input, shifts it, and alphabetizes it
    def run(self) -> None:
        csvInput = self.csvInput
        circularShift = self.circularShift
        alphabetize = self.alphabetize
        output = self.output
        
        csvInput.read_input("SE 6362 Project Engine Data.csv")
        csvInput.store_input()
        
        circularShift.retrieve_and_save_lines()
        circularShift.circular_shift()
        
        alphabetize.alphabetize()
        
        output.get_output()
    #Prints the output to the command line
    def getOutput(self):
        print(self.output.get_output())

#Runs the whole program   
if __name__ == '__main__':
    master = Master_Control()
    master.run()
    master.getOutput()