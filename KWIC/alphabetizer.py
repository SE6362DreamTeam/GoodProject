class Alphabetizer:

    # method alphabetize_with_urls:
    def alphabetize_with_urls(self, circular_shifts_with_urls):
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

    # def alphabetize_line()
    # Use this to alphabetize the circular shifts of a search phrase
