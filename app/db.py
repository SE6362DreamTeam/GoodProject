import db_credentials  # Import your sensitive information from config.py (or hardcode if needed)
from mysql.connector import Error


class Database:

    # class constructor
    def __init__(self):
        self.connection = None


    # The connection to the database
    def connect(self):

        """Establish the connection to the database."""
        if self.connection:
            try:

                host= db_credentials.DB_HOST,
                user= db_credentials.DB_USERNAME,
                password= db_credentials.DB_PASSWORD,
                database= db_credentials.DB_NAME


            except Error as e:
                print(f"Error: ***Connection to database failed*** {e}")


    # close the connection to the databse
    def close(self):
        """Close the database connection."""
        if self.connection:
            self.connection.close()
            self.connection = None



    # execute query in the database
    def execute_query(self, query, params=None):
        """Execute an SQL query."""
        self.connect()  # Ensure connection is established
        cursor = self.connection.cursor()
        cursor.execute(query, params)
        self.connection.commit()
        cursor.close()


    def fetch_all(self, query, params=None):
        """Fetch all rows from an SQL query."""
        self.connect()
        cursor = self.connection.cursor()
        cursor.execute(query, params)
        results = cursor.fetchall()
        cursor.close()
        return results
