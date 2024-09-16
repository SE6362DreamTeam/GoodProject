from KWIC.input import Input


class Output:
    # store in DB method

    # print contents method
    def print_output(self, alphabetized_dict):
        print(alphabetized_dict)

    # query from DB method


def main(self):
    # Set up database
    print("Setting up database...")
    # calls read_input, passes input file to it
    kwic_input = Input()
    kwic_input.read_input("SE 6362 Project Engine Data.csv")
