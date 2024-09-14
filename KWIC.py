import csv
import pprint
# Class KWIC
class KWIC:

# method readInput:
    def readInput(self, file_name):
        file_lines = dict()
        # Open the input file (csv format)
        with open(file_name, "r") as f:
            reader = csv.reader(f, delimiter=",")

            # Go through each line
            for i, line in enumerate(reader):
                # Do not count the column header row
                if i == 0:
                    continue
                else:
                    term_length = len(line[0].split())
                    # Create a new entry in the dictionary if there is not one for this query term already
                    if file_lines.get(line[0]) == None:
                        # Key is the query term
                        # Value is a list of URLs for this query term
                        file_lines[line[0]] = list()
                    # Go through each URL of the current line and add it to the value
                    for j in range(1, term_length+1):
                        (file_lines[line[0]]).append(line[j])
                    KWIC.circularShift(self, line[0])
                # print(line[0], ":" , file_lines[line[0]])
        

# method circularshift:
    def circularShift(self, current_term):
        circular_shifts = list()
        words = current_term.split(" ")
        line = ""
        num_iterations = len(words)
        for i in range(num_iterations):
            popped_term = words.pop(0)
            words.append(popped_term)
            line = " ".join(words)
            circular_shifts.append(line)
        # print(circular_shifts)
        KWIC.alphabetize(self,circular_shifts)
            
# method alphabetize:
    def alphabetize(self, circular_shifts):
        # Sort the circular shifts alphabetically
        sorted_shifts = sorted(circular_shifts, key=lambda s: s.lower())
        print(sorted_shifts)

# method storeOutput:

# method main:
def main():
    # calls readInput, passes input file to it
    kwic_system = KWIC()
    kwic_system.readInput("SE 6362 Project Engine Data.csv")
    # calls storeOutput once a flag (lineProcessed is set to true)

if __name__ == '__main__':
    main()