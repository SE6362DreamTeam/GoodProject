import csv

class Input:
    def __init__(self, circular_shift):
        self.circular_shifter = circular_shift

# method readInput:
    def read_input(self, file_name):
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
                    # Call circular shift for the current line
                    self.circular_shifter.circular_shift(line[0])

    # def read_phrase
        # Use this to pass the search phrase to circular shift

class CircularShift:
    # Constructor
    def __init__(self, file_lines, alphabetizer):
        # Create a dictionary to keep track of the URLs as circular shifts occur
        # Key:  circular shift
        # Value: its corresponding URL given in the input file
        self.file_lines = file_lines
        self.alpha_obj = alphabetizer

    # method circular_shift:
    def circular_shift(self, current_line):
        # Split the current line by spaces
        words = current_line.split(" ")

        # If there are n-1 words in a line, then n circular shifts must occur for the line 
        # to return to its original state
        num_iterations = len(words)
        # Iterate until n iterations is reached (should have original line at nth iteration)
        for i in range(num_iterations):
            # Remove the first word in words array
            popped_term = words.pop(0)
            # Add it to the end of words array
            words.append(popped_term)
            # Join the words array with spaces and store it in line (one whole string now)
            line = " ".join(words)
            self.file_lines.append(line)
        # Call alphabetize for the current search phrase (after circular shifts are complete for it)
        self.alpha_obj.alphabetize(self.file_lines)
    
    # def circular_shift_for_search(self, search_phrase)
        # Perform circular shift on the search phrase that is given

class Alphabetizer:
    def __init__(self, output):
        self.output_obj = output

# method alphabetize:
    def alphabetize(self, file_lines):
        # Sort all circular shifts alphabetically and store in a new list
        sorted_shifts = sorted(file_lines, key=lambda s: s.lower())
        self.output_obj.updateOutput(sorted_shifts)

class Output:
    def __init__(self):
        self.alphabetized_lines = list()
    # store in DB method

    # Update the list of alphabetized_lines as it receives more alphabetized shifts from
    # Alphabetizer
    def updateOutput(self, alphabetized_shifts):
        self.alphabetized_lines = alphabetized_shifts

    # Print all alphabetized lines method
    def print_output(self):
        print(self.alphabetized_lines)

    # query from DB method

class Main:
    # method main:
    def main():
        # Set up database
        print("Setting up database...")

        # Instantiate objects
        kwic_output = Output()
        alphabetizer = Alphabetizer(kwic_output)
        circular_shifter = CircularShift(list(), alphabetizer)
        kwic_input = Input(circular_shifter)

        # Calls read_input, passes input file to it
        kwic_input.read_input("SE 6362 Project Engine Data.csv")

        # Print the output of all circular shifts
        kwic_output.print_output()


if __name__ == '__main__':
    Main.main()