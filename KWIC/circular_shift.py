from alphabetizer import Alphabetizer


class CircularShift:
    # method circularshift:
    def circular_shift(self, current_term, URLs):
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
        Alphabetizer.alphabetize_with_urls(self, lines_with_urls)

    # def circular_shift_for_search(self, search_phrase)
    # Perform circular shift on the search phrase that is given

