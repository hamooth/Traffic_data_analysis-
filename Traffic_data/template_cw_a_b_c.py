import csv
import os
from collections import defaultdict
from datetime import datetime


# Task A: Input Validation
def validate_day_input():
    """
    Prompts the user for a day input and validates if it's an integer within range (1-31).
    """
    while True:
        try:
            day = int(input("Please enter the day of the survey in the format dd: "))
            if 1 <= day <= 31:
                return day
            else:
                print("Out of range - values must be in the range 1 and 31.")
        except ValueError:
            print("Integer required")


def validate_month_input():
    """
    Prompts the user for a month input and validates if it's an integer within range (1-12).
    """
    while True:
        try:
            month = int(input("Please enter the month of the survey in the format MM: "))
            if 1 <= month <= 12:
                return month
            else:
                print("Out of range - values must be in the range 1 to 12.")
        except ValueError:
            print("Integer required")


def validate_year_input():
    """
    Prompts the user for a year input and validates if it's an integer within range (2000-2024).
    """
    while True:
        try:
            year = int(input("Please enter the year of the survey in the format YYYY: "))
            if 2000 <= year <= 2024:
                return year
            else:
                print("Out of range - values must range from 2000 and 2024.")
        except ValueError:
            print("Integer required")


def validate_continue_input():
    """
    Prompts the user to decide whether to load another dataset:
    - Validates "Y" or "N" input
    """
    while True:
        continue_input = input("Do you want to analyze another dataset? (Y/N): ").strip().upper()
        if continue_input in ['Y', 'N']:
            return continue_input
        else:
            print("Invalid input. Please enter 'Y' or 'N'.")


# Task B: Processed Outcomes
def process_csv_data(filename):
    """
    Processes the CSV data for the selected date and extracts:
    - Total vehicles
    - Total trucks
    - Total electric vehicles
    - Two-wheeled vehicles, and other requested metrics
    """
    if not os.path.exists(filename):
        raise FileNotFoundError(f"File {filename} not found.")

    data = []
    with open(filename, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)  # Collecting rows as dictionaries into a list
    return data


def analyze_data(data, filename):
    """Analyze data and generate results."""
    total_vehicles = len(data)
    trucks = sum(1 for row in data if row['VehicleType'] == 'Truck')
    electric_vehicles = sum(1 for row in data if row['elctricHybrid'] == 'True')
    two_wheeled_vehicles = sum(1 for row in data if row['VehicleType'] in ['Bicycle', 'Motorcycle', 'Scooter'])
    elm_buses_north = sum(
        1 for row in data
        if row['JunctionName'] == 'Elm Avenue/Rabbit Road' and row['travel_Direction_in'] == 'N' and row['VehicleType'] == 'Buss'
    )
    no_turns = sum(1 for row in data if row['travel_Direction_in'] == row['travel_Direction_out'])
    over_speed = sum(
        1 for row in data if int(row['VehicleSpeed']) > int(row['JunctionSpeedLimit'])
    )

    # Vehicles at specific junctions
    elm_avenue_vehicles = sum(1 for row in data if row['JunctionName'] == 'Elm Avenue/Rabbit Road')
    hanley_highway_vehicles = sum(1 for row in data if row['JunctionName'] == 'Hanley Highway/Westway')

    # Scooter percentage at Elm Avenue/Rabbit Road
    elm_scooters = sum(1 for row in data if row['JunctionName'] == 'Elm Avenue/Rabbit Road' and row['VehicleType'] == 'Scooter')
    elm_scooter_percentage = round((elm_scooters / elm_avenue_vehicles) * 100) if elm_avenue_vehicles else 0

    # Bicycles per hour (Assuming each entry represents a 10-minute interval)
    bicycle_data = [row for row in data if row['VehicleType'] == 'Bicycle']
    bicycle_count_per_hour = defaultdict(int)
    for row in bicycle_data:
        hour = row.get('timeOfDay')  # Modify this if 'Time' is the wrong column name
        if hour:
            hour = hour.split(':')[0]  # Assuming 24-hour format
            bicycle_count_per_hour[hour] += 1
    avg_bicycles_per_hour = round(sum(bicycle_count_per_hour.values()) / len(bicycle_count_per_hour)) if bicycle_count_per_hour else 0

    # Peak hour at Hanley Highway/Westway
    hanley_peak_hour = defaultdict(int)
    for row in data:
        if row['JunctionName'] == 'Hanley Highway/Westway':
            hour = row.get('timeOfDay')
            if hour:
                hour = hour.split(':')[0]  # Assuming 24-hour format
                hanley_peak_hour[hour] += 1
    peak_hour_count = max(hanley_peak_hour.values()) if hanley_peak_hour else 0
    peak_hours = [hour for hour, count in hanley_peak_hour.items() if count == peak_hour_count]

    # Rain hours (assuming there's a column "Rain" that marks if it rained during the hour)
    rain_hours = sum(1 for row in data if row.get('timeOfDay') == 'True')

    results = {
        "CSV File Name": filename,
        "Total Vehicles": total_vehicles,
        "Total Trucks": trucks,
        "Electric Vehicles": electric_vehicles,
        "Two-Wheeled Vehicles": two_wheeled_vehicles,
        "Elm Buses North": elm_buses_north,
        "No Turns": no_turns,
        "Over Speeding": over_speed,
        "Truck Percentage": round((trucks / total_vehicles) * 100) if total_vehicles else 0,
        "Avg Bicycles per Hour": avg_bicycles_per_hour,
        "Over Speeding Vehicles": over_speed,
        "Elm Avenue/Rabbit Road Vehicles": elm_avenue_vehicles,
        "Hanley Highway/Westway Vehicles": hanley_highway_vehicles,
        "Scooter Percentage Elm Avenue": elm_scooter_percentage,
        "Peak Hour(s) Hanley Highway/Westway": peak_hours,
        "Total Rain Hours": rain_hours
    }
    return results


# Task C: Save Results to Text File
def save_results_to_file(outcomes, file_name="results.txt"):
    """
    Saves the processed outcomes to a text file and appends if the program loops.
    """
    with open(file_name, mode='a') as file:
        file.write(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        file.write(f"CSV File: {outcomes['CSV File Name']}\n")  # Corrected line to output the file name
        file.write("Traffic Analysis Results:\n")
        for key, value in outcomes.items():
            if key != 'CSV File Name':  # Skip writing the 'CSV File Name' again
                file.write(f"{key}: {value}\n")
        file.write("\n")


def main():
    while True:
        # Task A: Input Validation
        day = validate_day_input()
        month = validate_month_input()
        year = validate_year_input()

        # Format the date for the filename
        date_input = f"traffic_data{day:02d}{month:02d}{year}.csv"
        print(f"Valid date input: {date_input}")

        # Load and analyze data (Tasks B and C)
        try:
            data = process_csv_data(date_input)
            results = analyze_data(data, date_input)  # Use date_input as filename

            # Display results
            print("\nAnalysis Results:")
            for key, value in results.items():
                print(f"{key}: {value}")

            # Save results to file
            save_results_to_file(results)
            print("\nResults saved to 'results.txt'")

        except FileNotFoundError as e:
            print(e)
        except Exception as e:
            print(f"An error occurred: {e}")

        # Ask if the user wants to analyze another dataset
        continue_input = validate_continue_input()
        if continue_input == 'N':
            print("Exiting the program.")
            break


if __name__ == "__main__":
    main()
