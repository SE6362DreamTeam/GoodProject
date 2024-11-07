import csv
import queue

from queue import Queue as StandardQueue
import threading
import re
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

from app.db_map import AlphabetizedData
#from app.db import db_session


# Interface for Record
class Record_Interface:

    @abstractmethod
    def __init__(self, text:str, url:str, data_id:int, url_id:int) -> None:
        pass

    def get_scraped_text(self) -> str:
        pass

    def get_url(self) -> str:
        pass

    def get_data_id(self) -> int:
        pass

    def get_url_id(self) -> int:
        pass

class Alpha_Record_interface:

    @abstractmethod
    def __init__(self, text_line: str, url: str, data_id: int, url_id: int) -> None:
        pass

    def get_text_line(self) -> str:
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
    def reduce_whitespace(self, text: str) -> str:
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
    def remove_duplicates(self, queue: Queue) -> Queue:
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

'''
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

'''

# Interface for the Output class
class Output_Interface:
    @abstractmethod
    def __init__(self, cirtularShift: CircularShift_Interface) -> None:
        pass



    @abstractmethod
    def output_to_database(self):
        pass



class ScrapedRecord(Record_Interface):

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


class AlphaRecord:

    def __init__(self, text_line: str, url: str, data_id: int, url_id: int) -> None:
        self.text_line = text_line
        self.url = url
        self.data_id = data_id
        self.url_id = url_id

    def get_text_line(self) -> str:
        return self.text_line

    def get_url(self) -> str:
        return self.url

    def get_data_id(self) -> int:
        return self.data_id

    def get_url_id(self) -> int:
        return self.url_id




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
                scraped_text = self.reduce_whitespace(data.scraped_text)  # Reduce whitespace here
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

    def reduce_whitespace(self, text: str) -> str:
        return re.sub(r'\s+', ' ', text).strip()





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
    def __init__(self, recordStorage: RecordStorage_Interface, done_event: threading.Event) -> None:
        self.recordStorage = recordStorage
        self.records = None

        self.queue = Queue()
        self.done_event = done_event


    # Retrieves the records form records storage and saves them into this object instance
    def retrieve_and_save_records(self) -> None:

        # Continuously check the recordStorage queue for more records
        while not self.done_event.is_set():

            # Grab a record from the queue
            try:
                # this is a single record
                record = self.recordStorage.getQueue().get(timeout=1)
            except queue.Empty:
                # Break out if no input is received within the timeout
                if self.done_event.is_set():
                    break
                continue

            # If we grab a "None", then we this signals the end of the input
            if record is None:
                # So we add a "None" to our own queue
                self.queue.put(None)
                # Then we can grab the entirety of the file records for record keeping
                self.records = list(self.recordStorage.getAllRecords())
                break

            # Assuming `record.scraped_text` is the long string with lines separated by "\n"
            lines = record.scraped_text.split("$")  # Splitting the text by "\n" into individual lines

            # Process each line individually
            for line in lines:
                shiftList = self.shift_current_record(line)

                # For each shifted version, create an AlphaRecord object
                for shifted_line in shiftList:
                    alpha_record = AlphaRecord(
                        text_line=shifted_line,
                        url=record.get_url(),
                        data_id=record.get_data_id(),
                        url_id=record.url_id
                    )

                    # Add the AlphaRecord object to the queue
                    self.queue.put(alpha_record)

         # Clean up duplicate records
        self.queue = self.remove_duplicates(self.queue)



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



        return shiftedRecords

    # Removes duplicate records from the queue
    def remove_duplicates(self, queue: Queue) -> Queue:
        # Create a set to store unique records
        unique_records = set()

        # Create a new queue to store the unique records
        new_queue = Queue()

        # Iterate through the queue
        while not queue.empty():
            record = queue.get()

            # Check if the record is unique
            if record not in unique_records:
                new_queue.put(record)
                unique_records.add(record)

        return new_queue




    # Returns the queue
    def getQueue(self) -> Queue:
        return self.queue



    #def getHistory(self) -> dict:
    #    return self.shifted_records



# Returns the alphabetized array
class Output(Output_Interface):
    def __init__(self, circularShift: CircularShift_Interface, app) -> None:
        self.circularShift = circularShift
        self.app = app

        self.existing_records = set()
        self.records_inserted = 0  # Initialize the number of records inserted

        # Load existing records into a set during initialization
        self.load_existing_records()

    def load_existing_records(self):
        """Load all existing records from the database to check for duplicates."""
        with self.app.app_context():
            existing_data = db.session.query(AlphabetizedData).all()
            # Store as a set of tuples (text_line, url_id, data_id) for quick lookup
            self.existing_records = {(record.text_line, record.url_id, record.data_id) for record in existing_data}

    def send_output_to_database(self, done_event: threading.Event):
        with self.app.app_context():
            records_batch = []
            batch_size = 2000
            batch_num = 0

            while not done_event.is_set() or self.circularShift.getQueue().qsize() > 0:
                try:
                    record = self.circularShift.getQueue().get(timeout=.5)

                except queue.Empty:
                    if done_event.is_set():
                        break

                    continue

                if record is None:
                    break

                record_tuple = (record.text_line, record.url_id, record.data_id)
                if record_tuple not in self.existing_records:
                    alphabetized_data = AlphabetizedData(
                        text_line=record.text_line,
                        url_id=record.url_id,
                        data_id=record.data_id,
                        mfa=0
                    )
                    records_batch.append(alphabetized_data)  # Add to the batch
                    self.existing_records.add(record_tuple)  # Add to the set of existing records

                # Commit in batches
                if len(records_batch) >= batch_size:
                    batch_num += 1
                    db.session.bulk_save_objects(records_batch)
                    db.session.flush()
                    self.records_inserted += len(records_batch)  # Update inserted records counter
                    records_batch = []  # Clear the batch after committing
                    print(f"Batch {batch_num} of {batch_size} records committed to the database.")

            # Commit any remaining records in the last batch
            if records_batch:
                db.session.bulk_save_objects(records_batch)
                db.session.commit()
                self.records_inserted += len(records_batch)  # Update inserted records counter
                print(f"Final batch of {len(records_batch)} records committed to the database.")

            print("All records have been committed to the database.")








class Master_Control:
    # Initializes all objects
    def __init__(self, app) -> None:

        # Ends threads
        self.done_event = threading.Event()

        # Initialize every object with their constructors
        self.app = app
        recordStorage = RecordStorage()
        self.databaseInput = database_input(recordStorage, app)
        self.circularShift = CircularShift(recordStorage, self.done_event)
        #self.alphabetize = Alphabetize(self.circularShift) #skip alphabaetize becase database will do better
        self.output = Output(self.circularShift, app)

        #self.database_input = database_input(self.recordStorage)



    # Takes in input, shifts it, and alphabetizes it
    def run(self) -> None:

        # We make 4 threads for each module and target their while True loops
        input_thread = threading.Thread(target=self.databaseInput.read_input)
        shift_thread = threading.Thread(target=self.circularShift.retrieve_and_save_records)
        #alphabetize_thread = threading.Thread(target=self.alphabetize.alphabetize)
        output_thread = threading.Thread(target=self.run_output)

        # Then we start the 4 threads
        input_thread.start()
        shift_thread.start()
        #alphabetize_thread.start()
        output_thread.start()

        # Then, we can follow along each thread as the inputs finishes
        # Note: This is still all being done concurrently, this just prevents the program from finishing before all inputs are read
        input_thread.join()
        shift_thread.join()
        #alphabetize_thread.join()
        output_thread.join()

        #self.shiftHistory = self.circularShift.getHistory()
        #self.alphabetizationHistory = self.alphabetize.getHistory()
        # print(self.shiftHistory)
        # print(self.alphabetizationHistory)

    # Prints the output to the command record
    def run_output(self):
        self.output.send_output_to_database(self.done_event)

    def get_output(self):
        outputString = ""

        # Get the total records sent to the database during the current run
        records_inserted = self.output.records_inserted  # Access records_inserted from the Output instance

        with self.app.app_context():
            # Query to get the total number of records in the AlphabetizedData table
            total_records_in_db = db.session.query(AlphabetizedData).count()

        # Format the output
        outputString += "<div class='output-box'>\n"
        outputString += "<h1>Database Record Summary:</h1>\n"
        outputString += f"<p><strong>Total records inserted in this run:</strong> {records_inserted}</p>\n"
        outputString += f"<p><strong>Total records in the database:</strong> {total_records_in_db}</p>\n"
        outputString += "</div>\n"

        return outputString



    def stop_threads(self):

        self.done_event.set()
        print("Stopping all threads...")








# Runs the whole program
if __name__ == '__main__':
    master = Master_Control()
    master.run()