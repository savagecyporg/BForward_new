import sys
import os 
import subprocess
import pandas as pd
from io import StringIO
import sqlite3
import logging
import re


class AccessExporter:
    def __init__(self, access_path):
        """
        initialize Access Exporter with the Path to the DB 
        """
        self.access_path = os.path.abspath(access_path)
        self.table_names = self._get_table_names()
        
    
    def _get_table_names(self):
        """
        fetch all tables 
        """
        try:
            result = subprocess.Popen(
                ['mdb-tables', '-1', self.access_path],
                stdout = subprocess.PIPE
            ).communicate()[0].decode()
            table_names = result.splitlines()
            return table_names
        except Exception as e:
            print(f'Failed to load table names:{e}')
            return []

    def _export_table_to_df(self, table_name):
        try:
            result = subprocess.run(
                    ['mdb-export', self.access_path, table_name],
                    capture_output = True,
                    text= True,
                    check= True
                    )
            content = result.stdout
            with StringIO(content) as temp_io:
                df = pd.read_csv(temp_io)
            return df
        except subprocess.CalledProcessError as e:
            print(f'Failed to export table {table_name}:{e}')
            return None
        except Exception as e:
            print(f'An error occured while exporting table {table_name}:{e}')
            return None

    def export_all_tables(self):
        if not self.table_names:
            print('No tables found in the database')
            return {}
        out_tables = {}
        for table_name in self.table_names:
            if table_name:
                df = self._export_table_to_df(table_name)
                if df is not None:
                    out_tables[table_name]=df
        return out_tables

    def save_db(self, sqlite_path, data_dict, if_exists='replace'):
        """
        Save a dictionary of DataFrames to an SQLite database.
        If the database doesn't exist, prompt the user to create it.

        Parameters:
        sqlite_path (str): Path to the SQLite database file.
        data_dict (dict): Dictionary where keys are table names and values are DataFrames.
        if_exists (str): Behavior if the table already exists. Options: 'fail', 'replace', 'appe
        """
        conn = None  # Initialize conn to None
        try:
            directory = os.path.dirname(sqlite_path)
            if directory:  # Check if the path contains a directory
                os.makedirs(directory, exist_ok=True)
                
            conn = sqlite3.connect(sqlite_path)
            for table_name , df in data_dict.items():
                df.to_sql(table_name, conn, if_exists=if_exists, index=False)
            
            conn.commit()
            print('Data saved succesfully')
        except Exception as e:
            print(f'Error saving databse: {e}')
        finally:
            if conn:
                conn.close()


    
    def load_db(self, sqlite_path, table_name=None):
        """
        Load tables from an SQLite database.

        Parameters:
        sqlite_path (str): Path to the SQLite database file.
        table_name (str, optional): Name of the specific table to load. If None, all tables are loaded.

        Returns:
        dict: A dictionary where keys are table names and values are DataFrames.
        """
        data_dict = {}
        try:
            # Use a context manager to handle the connection
            with sqlite3.connect(sqlite_path) as conn:
                cursor = conn.cursor()
            
            # Fetch table names
            if table_name is None:
                # Get all table names
                cursor.execute('SELECT name FROM sqlite_master WHERE type="table";')
                table_names = [row[0] for row in cursor.fetchall()]  # Use row[0] for table name
   
            else:
                # Use the provided table name
                table_names = [table_name]
            
            # Load data from each table
            for table in table_names:
                df = pd.read_sql_query(f'SELECT * FROM "{table}"', conn)
                data_dict[table] = df
                #print(f'Loaded table "{table}" from database.')
        
            return data_dict
        except Exception as e:
            print(f'Error loading table: {e}')
            raise  # Re-raise the exception for further debugging
        finally:
            if conn:
                conn.close()


access_path = '/home/ag/Desktop/GP/gp/gp.accdb'

sqlite_path = '/home/ag/Desktop/GP/project/_db'


Gp = AccessExporter(access_path)
tables = Gp.export_all_tables()
_db = Gp.save_db(sqlite_path, tables)
db = Gp.load_db(sqlite_path)



Actual_Guest = db['Actual Guest']