import csv
import queue

import threading

# from flask import current_app
from flask import Flask
import app.web_scraper
import app.db
# from sqlalchemy.orm import sessionmaker
from abc import abstractmethod
from queue import Queue
import app.db_map
from app.db import db
from flask import current_app
#from run import app
from sqlalchemy.orm import joinedload


# Interface for Record
class Record_interface:

    @abstractmethod
    def __init__(self, scraped_text:str, url:str, data_id:int, url_id:int) -> None:
        pass

    def get_scraped_text(self) -> str:
        pass

    def get_url(self) -> str:
        pass

    def get_data_id(self) -> int:
        pass

    def get_url_id(self) -> int:
        pass



# Interface for the RecordStorage class
class RecordStorage_Interface:
    @abstractmethod
    def __init__(self) -> None:
        pass

    @abstractmethod
    def store_input(self, recordDict: dict) -> None:
        pass

    @abstractmethod
    def getRecord(self, record: int):
        pass

    @abstractmethod
    def getAllRecords(self):
        pass

    @abstractmethod
    def addRecordToQueue(self, record: str):
        pass

    @abstractmethod
    def getQueue(self) -> Queue:
        pass


# Interface for the Input class
class Input_Interface:
    @abstractmethod
    def __init__(self, recordStorage: RecordStorage_Interface) -> None:
        pass

    @abstractmethod
    def read_input(self) -> None:
        pass


    @abstractmethod
    def return_history(self) -> None:
        pass


# Interface for the CircularShift class
class CircularShift_Interface:
    @abstractmethod
    def __init__(self, recordStorage: RecordStorage_Interface) -> None:
        pass

    @abstractmethod
    def retrieve_and_save_records(self) -> None:
        pass

    @abstractmethod
    def circular_shift(self) -> None:
        pass

    @abstractmethod
    def shift_current_record(self, current_record: str) -> str:
        pass

    @abstractmethod
    def get_shifted_records(self) -> list:
        pass

    @abstractmethod
    def getQueue(self) -> Queue:
        pass

    @abstractmethod
    def getHistory(self) -> dict:
        pass


# Interface for the Alphabetize class
class Alphabetize_Interface:
    @abstractmethod
    def __init__(self, circularShift: CircularShift_Interface) -> None:
        pass

    @abstractmethod
    def alphabetize(self) -> None:
        pass

    @abstractmethod
    def get_alphabetized_records(self) -> list:
        pass

    @abstractmethod
    def get_circular_shift_by_index(self, index: int) -> list:
        pass

    @abstractmethod
    def getQueue(self) -> Queue:
        pass

    @abstractmethod
    def getHistory(self) -> dict:
        pass


# Interface for the Output class
class Output_Interface:
    @abstractmethod
    def __init__(self, alphabetize: Alphabetize_Interface) -> None:
        pass

    @abstractmethod
    def get_output(self):
        pass



class ScrapedRecord(Record_interface):

    def __init__(self, scraped_text: str, url: str, search_term: str, data_id: int, url_id: int) -> None:
        self.scraped_text = scraped_text
        self.url = url
        self.search_term = search_term
        self.data_id = data_id
        self.url_id = url_id

    def get_scraped_text(self) -> str:
        return self.scraped_text

    def get_url(self) -> str:
        return self.url

    def get_data_id(self) -> int:
        return self.data_id



'''

# Class for reading the input from a csv
class csv_Input(Input_Interface):
    def __init__(self, lineStorage: LineStorage_Interface) -> None:
        self.lineStorage = lineStorage
        self.records = {}

    def read_input(self, file_name) -> None:
        # Create a dictionary to hold each line we read in
        # Key: search phrase
        # Value: list of URLs for that search phrase
        records = dict()

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
                    if records.get(line[0]) == None:
                        # Key is the query term
                        # Value is a list of URLs for this search phrase
                        records[line[0]] = list()
                    # Go through each URL of the current line and add it to the value
                    for j in range(1, term_length + 1):
                        (records[line[0]]).append(line[j])
                    # Add the line to the lineStorage queue for further processing
                    self.lineStorage.addLineToQueue(line[0])
        self.records = records
        # Add a "None" to the lineStorage queue to show that we are done reading input
        self.lineStorage.addLineToQueue(None)


'''

# Class for reading the input from a database
class database_input(Input_Interface):

    def __init__(self, recordStorage: RecordStorage_Interface, app) -> None:
        self.recordStorage = recordStorage
        self.app = app

    def read_input(self) -> None:
        with self.app.app_context():
            # Perform a join to retrieve related data from ScrapedData and URLs
            scraped_data = db.session.query(app.db_map.ScrapedData).options(joinedload(app.db_map.ScrapedData.url)).all()

            if not scraped_data:
                return

            for data in scraped_data:
                # Access data from both ScrapedData and the related URLs record
                scraped_text = data.scraped_text
                url = data.url.url  # Access the actual URL string from the URLs table
                search_term = data.url.search_term  # Access the search term from the URLs table
                data_id = data.data_id
                url_id = data.url.url_id

                # Create the ScrapedRecord object with all required attributes
                record_object = ScrapedRecord(
                    scraped_text=scraped_text,
                    url=url,
                    search_term=search_term,
                    data_id=data_id,
                    url_id=url_id
                )

                # Add the record object to the queue
                self.recordStorage.addRecordToQueue(record_object)

            # Optionally add a sentinel value (e.g., None) to signal the end of input
            self.recordStorage.addRecordToQueue(None)






class RecordStorage(RecordStorage_Interface):
    def __init__(self) -> None:
        self.records = {}
        self.queue = Queue()

    # Stores the input into the records variable
    def store_input(self, record_Dict: dict) -> None:
        self.records = record_Dict

    # Gets the record from the given index
    def getRecord(self, recordIndex: int):
        return list(self.records)[recordIndex]

    # Returns all records
    def getAllRecords(self):
        return self.records

    # Adds a record to the queue
    def addRecordToQueue(self, record: ScrapedRecord) -> None:
        self.queue.put(record)
        pass

    # Gets the queue
    def getQueue(self) -> Queue:
        return self.queue








# Class for circularly shifting records
class CircularShift(CircularShift_Interface):
    def __init__(self, recordStorage: RecordStorage_Interface) -> None:
        self.recordStorage = recordStorage
        self.records = None
        self.shifted_records = {}
        self.queue = Queue()

    # Retrieves the records form records storage and saves them into this object instance
    def retrieve_and_save_records(self) -> None:
        # Continuously check the recordStorage queue for more records
        while True:
            # Grab a record from the queue
            try:
                record = self.recordStorage.getQueue().get(timeout=5)
            except queue.Empty:
                # Break out if no input is received within the timeout
                break
            # If we grab a "None", then we are done reading input
            if record is None:
                # So we add a "None" to our own queue
                self.queue.put(None)
                # Then we can grab the entirety of the file records for record keeping
                self.records = list(self.recordStorage.getAllRecords())
                break
            # If it is not none, we need to shift the record
            shiftList = self.shift_current_record(record)
            self.shifted_records[record] = shiftList

    # Shifts a single record
    def shift_current_record(self, current_record: str):
        # Split the current record by spaces
        words = current_record.split(" ")

        # If there are n-1 words in a record, then n circular shifts must occur for the record
        # to return to its original state
        num_iterations = len(words)
        # Iterate until n iterations is reached (should have original record at nth iteration)
        shiftedRecords = []
        for i in range(num_iterations):
            # Remove the first word in words array
            popped_term = words.pop(0)
            # Add it to the end of words array
            words.append(popped_term)
            # Join the words array with spaces and store it in record (one whole string now)
            record = " ".join(words)
            shiftedRecords.append(record)
            # We can add the shifted record to the queue to be alphabetized
            self.queue.put(record)
        return shiftedRecords

    # Returns all shifted records
    def get_shifted_Records(self) -> list:
        return list(self.shifted_records)

    # Returns the queue
    def getQueue(self) -> Queue:
        return self.queue

    def getHistory(self) -> dict:
        return self.shifted_records









# Class for alphabetizing the records
class Alphabetize(Alphabetize_Interface):
    def __init__(self, circularShift: CircularShift_Interface) -> None:
        self.circularShift = circularShift
        self.records = []
        self.sorted_shifts = []
        self.sort_history = {}
        self.queue = Queue()

    # Alphabetizes the circular shifts
    def alphabetize(self) -> None:
        # Sort all circular shifts alphabetically and store in a new list
        # We continuously check the queue for new records to add to our list
        while True:
            # First we get a record
            try:
                record = self.circularShift.getQueue().get(timeout=5)
            except queue.Empty:
                # Break out if no input is received within the timeout
                break
            # If the record is "None" then we have reached the end of the input
            if record is None:
                # First we add a "None" to our own queue and break
                self.queue.put(None)
                break
                # If not none, we can append it to our list of records
            self.records.append(record)
            # Then sort the list of records
            self.sorted_shifts = sorted(self.records, key=lambda s: s.lower())
            # And put the sorted list into our queue
            self.queue.put(self.sorted_shifts)
            self.sort_history[record] = self.sorted_shifts
        return self.sort_history

    # Returns the alphabetized records
    def get_alphabetized_records(self) -> list:
        return self.sorted_shifts

    # Gets a certain record out of the array
    def get_circular_shift_by_index(self, index: int) -> list:
        return self.sorted_shifts[index]

    # Returns the queue for this class
    def getQueue(self) -> Queue:
        return self.queue

    def getHistory(self) -> dict:
        return self.sort_history










# Returns the alphabetized array
class Output(Output_Interface):
    def __init__(self, alphabetize: Alphabetize_Interface) -> None:
        self.alphabetize = alphabetize

    def get_output(self):
        # We continuously check with alphabetize to see if there are new records to output
        while True:

            try:
                record = self.alphabetize.getQueue().get(timeout=5)
            except queue.Empty:
                break
            # If the record is "None", we are free from the loop
            if record is None:
                break
        # Then we can return the final output
        return self.alphabetize.get_alphabetized_records()









class Master_Control:
    # Initializes all objects
    def __init__(self, app) -> None:
        # Initialize every object with their constructors
        self.app = app
        recordStorage = RecordStorage()
        self.databaseInput = database_input(recordStorage, app)
        self.circularShift = CircularShift(recordStorage)
        self.alphabetize = Alphabetize(self.circularShift)
        self.output = Output(self.alphabetize)

        #self.database_input = database_input(self.recordStorage)

        # Ends threads
        self.done_event = threading.Event()

    # Takes in input, shifts it, and alphabetizes it
    def run(self) -> None:
        # We make 4 threads for each module and target their while True loops
        input_thread = threading.Thread(target=self.databaseInput.read_input)
        shift_thread = threading.Thread(target=self.circularShift.retrieve_and_save_records)
        alphabetize_thread = threading.Thread(target=self.alphabetize.alphabetize)
        output_thread = threading.Thread(target=self.run_output)

        # Then we start the 4 threads
        input_thread.start()
        shift_thread.start()
        alphabetize_thread.start()
        output_thread.start()

        # Then, we can follow along each thread as the inputs finishes
        # Note: This is still all being done concurrently, this just prevents the program from finishing before all inputs are read
        input_thread.join()
        shift_thread.join()
        alphabetize_thread.join()
        output_thread.join()

        self.shiftHistory = self.circularShift.getHistory()
        self.alphabetizationHistory = self.alphabetize.getHistory()
        # print(self.shiftHistory)
        # print(self.alphabetizationHistory)

    # Prints the output to the command record
    def run_output(self):
        print(self.output.get_output())

    def get_output(self):
        outputString = ""
        listKeys = self.shiftHistory.keys()
        recordCount = 1
        for key in listKeys:
            outputString += f"<div class='output-box'>\n"
            outputString += f"<h1><strong>record {recordCount}:</strong> <span style=\"font-weight:normal\">{key}</span></h1>\n"
            listShifts = self.shiftHistory[key]
            shiftCount = 1
            for shift in listShifts:
                outputString += f"<h2><strong>SHIFT {shiftCount}:</strong> <span style=\"font-weight:normal\">{shift}</span></h2>\n"
                alphabetization = self.alphabetizationHistory[shift]
                outputString += "<h3><strong>NEW ALPHABETIZATION:</strong></h3>\n<ul>\n"
                for element in alphabetization:
                    outputString += f"<li>{element}</li>\n"
                outputString += "</ul>\n"
                shiftCount += 1
            recordCount += 1
            outputString += "</div>\n"
        # test
        # print(outputString)

        return outputString

    def stop_threads(self):
        self.done_event.set()








# Runs the whole program
if __name__ == '__main__':
    master = Master_Control()
    master.run()