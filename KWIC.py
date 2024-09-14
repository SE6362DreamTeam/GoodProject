import csv
import pprint
# Class KWIC
class KWIC:

# method readInput:
    def readInput(self, file_name):
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
                    KWIC.circularShift(self, line[0], file_lines[line[0]])
                # print(line[0], ":" , file_lines[line[0]])
        

# method circularshift:
    def circularShift(self, current_term, URLs):
        # Create a dictionary to keep track of the URLs as circular shifts occur
        # Key:  circular shift
        # Value: its corresponding URL given in the input file
        lines_with_urls = dict()

        # Split the current line by spaces
        words = current_term.split(" ")

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
            # Add the circular shift to the lines_with_urls dictionary, along with its URL
            lines_with_urls[line] = URLs[i]
        # print(lines_with_urls)
        # Call alphabetize for the current search phrase (after circular shifts are complete for it)
        KWIC.alphabetize(self, lines_with_urls)
            
# method alphabetize:
    def alphabetize(self, circular_shifts_with_urls):
        # Create an dictionary to keep track of the URLs as the shifts are alphabetized
        # Key: circular shift line
        # Value: URL
        alphabetized_dict = dict()

        # Sort the circular shifts alphabetically and store in a new list
        sorted_shifts = sorted(circular_shifts_with_urls, key=lambda s: s.lower())

        # Go through each index of the sorted list
        for circular_shift in sorted_shifts:
            # Add the current circular shift line and its corresponding url to a new alphabetized dictionary
            alphabetized_dict[circular_shift] = circular_shifts_with_urls[circular_shift]
        
        print(alphabetized_dict)

# method storeOutput:

# method main:
def main():
    # calls readInput, passes input file to it
    kwic_system = KWIC()
    kwic_system.readInput("SE 6362 Project Engine Data.csv")
    # calls storeOutput once a flag (lineProcessed is set to true)

if __name__ == '__main__':
    main()