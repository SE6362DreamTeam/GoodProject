import csv

from KWIC.circular_shift import CircularShift


class Input:
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
                    for j in range(1, term_length + 1):
                        (file_lines[line[0]]).append(line[j])
                    # Call circular shift for the current line
                    CircularShift.circular_shift(self, line[0], file_lines[line[0]])
                # print(line[0], ":" , file_lines[line[0]])

    # def read_phrase
    # Use this to pass the search phrase to circular shift
