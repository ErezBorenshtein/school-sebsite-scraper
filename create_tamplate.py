import pandas as pd

def create_schedule():
    # Define the days and hours
    days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    hours = [str(i) for i in range(1, 12)]  # Hours from 1 to 11

    # Create a DataFrame with days as rows and hours as columns
    df = pd.DataFrame(index=hours, columns=days)

    # Save the DataFrame to a CSV file
    df.to_csv('schedule_template.csv')
    print("Schedule template created successfully.")

if __name__ == "__main__":
    # Call the function to create the schedule template
    create_schedule()
