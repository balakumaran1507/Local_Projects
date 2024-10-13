import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

class KeylogAnalyzer:
    def __init__(self, filename):
        self.filename = filename
        self.data = pd.DataFrame()
    
    def read_data(self):
        # Read the log file into a pandas DataFrame
        try:
            self.data = pd.read_csv(self.filename, delimiter=":", names=["timestamp", "message"], skipinitialspace=True)
            self.data['timestamp'] = pd.to_datetime(self.data['timestamp'])
            self.data['message'] = self.data['message'].str.strip()
        except FileNotFoundError:
            print("File not found. Please check the filename and try again.")
        except Exception as e:
            print(f"An error occurred: {e}")
    
    def analyze_data(self):
        if self.data.empty:
            print("No data to analyze. Please read the data first.")
            return
        
        # Frequency of key presses
        key_counts = self.data['message'].value_counts()
        print("Key Press Frequencies:")
        print(key_counts)
        
        # Plotting key press frequency
        plt.figure(figsize=(10, 6))
        key_counts.plot(kind='bar')
        plt.title('Frequency of Key Presses')
        plt.xlabel('Key')
        plt.ylabel('Frequency')
        plt.show()

    def time_between_key_presses(self):
        if self.data.empty:
            print("No data to analyze. Please read the data first.")
            return
        
        # Calculate time between key presses
        self.data['time_diff'] = self.data['timestamp'].diff().dt.total_seconds()
        print("Time Between Key Presses Statistics:")
        print(self.data['time_diff'].describe())

# Usage
if __name__ == "__main__":
    # Initialize the analyzer with the keylog file
    analyzer = KeylogAnalyzer("keylog.txt")
    
    # Read and analyze the data
    analyzer.read_data()
    analyzer.analyze_data()
    analyzer.time_between_key_presses()
