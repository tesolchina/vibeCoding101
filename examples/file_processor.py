"""
File Processing Example
This script demonstrates reading and processing a CSV file.
Students can use this as a reference for their own projects.
"""

import csv

def read_weather_data(filename):
    """Read weather data from a CSV file"""
    weather_data = []
    
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            weather_data.append(row)
    
    return weather_data

def analyze_weather(data):
    """Analyze weather data and print statistics"""
    # Convert temperature strings to integers
    temperatures = [int(row['Temperature']) for row in data]
    
    avg_temp = sum(temperatures) / len(temperatures)
    max_temp = max(temperatures)
    min_temp = min(temperatures)
    
    # Find the hottest and coldest months
    hottest_month = max(data, key=lambda x: int(x['Temperature']))
    coldest_month = min(data, key=lambda x: int(x['Temperature']))
    
    print("Weather Analysis")
    print("=" * 40)
    print(f"Average Temperature: {avg_temp:.1f}°C")
    print(f"Highest Temperature: {max_temp}°C ({hottest_month['Month']})")
    print(f"Lowest Temperature: {min_temp}°C ({coldest_month['Month']})")
    print(f"\nTotal months analyzed: {len(data)}")

def main():
    """Main function"""
    # Read and analyze the sample data
    weather_data = read_weather_data('../sample_data.csv')
    analyze_weather(weather_data)

if __name__ == "__main__":
    main()
