import tkinter as tk
from tkinter import filedialog, messagebox
import csv
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib


class HistogramApp:
    def __init__(self, traffic_data, date):
        """
        Initializes the histogram application with the traffic data and selected date.
        """
        self.traffic_data = traffic_data  # Dictionary of {Hour: {Junction: Volume}}
        self.date = date

    def draw_histogram(self):
        """
        Draws the histogram using matplotlib with a cleaner and more modern style.
        """
        if not self.traffic_data:
            messagebox.showerror("No Data", "No traffic data available for visualization.")
            return

        # Prepare data for histogram
        hours = sorted(self.traffic_data.keys())
        junctions = {junction for hour_data in self.traffic_data.values() for junction in hour_data.keys()}
        junctions = sorted(junctions)

        # Set seaborn style
        sns.set(style="whitegrid")

        # Set up the plot
        fig, ax = plt.subplots(figsize=(12, 7))
        bar_width = 0.1

        # Corrected colormap usage
        colors = plt.get_cmap('tab10', len(junctions))

        # Plot bars for each junction
        for i, hour in enumerate(hours):
            for j, junction in enumerate(junctions):
                volume = self.traffic_data[hour].get(junction, 0)
                ax.bar(
                    i + j * bar_width,
                    volume,
                    width=bar_width,
                    label=f'{junction}' if i == 0 else "",
                    color=colors(j),
                )

        # Add x-axis labels for hours
        ax.set_xticks([i + (len(junctions) - 1) * bar_width / 2 for i in range(len(hours))])
        ax.set_xticklabels(hours)

        # Labels and title
        ax.set_xlabel("Hours of the Day", fontsize=12)
        ax.set_ylabel("Traffic Volume", fontsize=12)
        ax.set_title(f"Traffic Data for {self.date}", fontsize=16)

        # Display legend
        ax.legend(title="Junctions", bbox_to_anchor=(1.05, 1), loc='upper left', frameon=False)

        # Customize the gridlines and style
        ax.grid(True, axis='y', linestyle='--', alpha=0.7)

        # Show plot with tight layout
        plt.tight_layout()
        plt.show()


class MultiCSVProcessor:
    def __init__(self):
        """
        Initializes the application for processing multiple CSV files.
        """
        self.current_data = None  # Stores the data for the current CSV file
        self.date = None  # Selected date for analysis
        self.traffic_summary = {}  # Summary of traffic data

    def load_csv_file(self):
        """
        Loads a CSV file and processes its data.
        """
        file_path = filedialog.askopenfilename(
            title="Select Traffic Data CSV File",
            filetypes=[("CSV files", "*.csv")]
        )
        if not file_path:
            messagebox.showerror("No File", "No file selected.")
            return

        try:
            with open(file_path, mode='r', newline='') as file:
                reader = csv.DictReader(file)
                self.current_data = list(reader)

            if not self.current_data:
                raise ValueError("CSV file is empty.")

            # Extract unique dates and process only the first date
            dates = {row['Date'] for row in self.current_data}
            self.date = next(iter(dates))  # Pick the first available date
            if len(dates) > 1:
                messagebox.showwarning("Multiple Dates", "The file contains multiple dates. Using the first date.")

            self.process_data()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file: {e}")

    def process_data(self):
        """
        Processes the traffic data for the selected date and prepares a summary.
        """
        if not self.current_data or not self.date:
            return

        self.traffic_summary.clear()  # Clear previous data

        for row in self.current_data:
            if row['Date'] != self.date:
                continue

            # Extract hour from timeOfDay
            try:
                hour = int(row['timeOfDay'].split(':')[0])  # Extracting hour part
            except (KeyError, ValueError):
                messagebox.showerror("Invalid Data", f"Invalid timeOfDay value: {row.get('timeOfDay')}")
                return

            junction = row.get('JunctionName', 'Unknown')
            if not junction:
                messagebox.showerror("Missing Data", "JunctionName is missing in the dataset.")
                return

            # Count vehicle occurrences
            if hour not in self.traffic_summary:
                self.traffic_summary[hour] = {}
            if junction not in self.traffic_summary[hour]:
                self.traffic_summary[hour][junction] = 0

            # Increment volume (1 vehicle per row)
            self.traffic_summary[hour][junction] += 1

    def clear_previous_data(self):
        """
        Clears data from the previous run to process a new dataset.
        """
        self.current_data = None
        self.date = None
        self.traffic_summary.clear()

    def handle_user_interaction(self):
        """
        Handles user input for processing multiple files.
        """
        while True:
            self.clear_previous_data()
            self.load_csv_file()

            if self.traffic_summary:
                # Display the histogram for the current dataset
                app = HistogramApp(self.traffic_summary, self.date)
                app.draw_histogram()

            # Prompt for another dataset
            response = messagebox.askyesno("New Dataset", "Do you want to select a data file for a different date?")
            if not response:
                messagebox.showinfo("Exit", "Thank you for using the application.")
                break

    def run(self):
        """
        Runs the processor for handling multiple CSV files.
        """
        self.handle_user_interaction()


# Entry point for the program
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Hide the root window for file dialog usage

    processor = MultiCSVProcessor()
    processor.run()
