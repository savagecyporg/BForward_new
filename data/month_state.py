import pandas as pd
from calendar import monthrange

def generate_monthly_schedule(ready, test_year, test_month):
    """
    Generate a monthly diving schedule with summary rows.
    
    Parameters:
        ready (pd.DataFrame): Input DataFrame containing booking data.
        test_year (int): Year for which to generate the schedule.
        test_month (int): Month for which to generate the schedule.
    
    Returns:
        pd.DataFrame: Monthly schedule with summary rows.
    """
   
    # Copy the DataFrame to avoid modifying the original
    df_month = ready.copy()

   
   # Convert 'Arrival' column to datetime with explicit format
    df_month['Arrival'] = pd.to_datetime(df_month['Arrival'], format='%Y-%m-%d', errors='coerce')  # Specify format
    # Filter bookings for the specified year and month
    month_bookings = df_month[
        (df_month['Arrival'].dt.year == test_year) & 
        (df_month['Arrival'].dt.month == test_month)
    ].copy()

    # Create columns for each day in the month
    days_in_month = monthrange(test_year, test_month)[1]
    date_columns = [f"{test_month:02d}-{day:02d}" for day in range(1, days_in_month + 1)]

    # Handle NaN values in 'Name' and 'Family Name' columns
    month_bookings['Name'] = month_bookings['Name'].fillna('')
    month_bookings['Family Name'] = month_bookings['Family Name'].fillna('')
    diver_names = month_bookings['Name'] + ' ' + month_bookings['Family Name']

    # Initialize the month DataFrame
    additional_columns = ['Tour Operator', 'Activity', 'Course', 'Diving Days']
    month_df = pd.DataFrame(index=diver_names.unique(), columns=additional_columns + date_columns)

    # Set default values
    month_df[additional_columns] = month_df[additional_columns].astype(object)
    month_df[date_columns] = 0

    # Populate the month DataFrame
    for _, row in month_bookings.iterrows():
        if not pd.isna(row['Arrival']):
            arrival_date = row['Arrival']
            diver_name = row['Name'] + ' ' + row['Family Name']
            tour_operator = row['Tour Operator']
            activity_type = row['Activity Type']
            course = activity_type if activity_type in ['OWC', 'AOW'] else ''

            # Update additional columns
            month_df.loc[diver_name, additional_columns] = [tour_operator, activity_type, course, row['Diving Days']]

            # Mark the guest as present on each diving day
            if activity_type in ['Diver', 'OWC', 'AOW', 'DSD', 'DM']:
                for day_offset in range(row['Diving Days']):
                    diving_date = arrival_date + pd.Timedelta(days=day_offset)
                    if diving_date.month == test_month:
                        date_str = diving_date.strftime('%m-%d')
                        if date_str in month_df.columns:
                            month_df.loc[diver_name, date_str] = 1

    # Sort the index by arrival date
    month_bookings['Diver Name'] = diver_names
    sorted_divers = month_bookings.sort_values(by='Arrival')['Diver Name'].unique()
    month_df = month_df.loc[sorted_divers]

    # Add summary rows
    summary_rows = pd.DataFrame(index=['Total Guests (Diving/Courses)', 'Total Cash'], columns=month_df.columns)
    summary_rows.loc['Total Guests (Diving/Courses)'] = month_df[date_columns].sum()
    summary_rows.loc['Total Cash'] = 0  # Placeholder for cash totals
    month_df = pd.concat([month_df, summary_rows])

    # Calculate tour operator totals
    tour_operator_totals = month_bookings.groupby('Tour Operator')['Name'].nunique().reset_index(name='Total Guests')
    tour_operator_names = pd.DataFrame([tour_operator_totals['Tour Operator'].values], 
                                       index=['Tour Operators'], 
                                       columns=[f"Operator {i+1}" for i in range(len(tour_operator_totals))])
    tour_operator_values = pd.DataFrame([tour_operator_totals['Total Guests'].values], 
                                        index=['Total Guests'], 
                                        columns=[f"Operator {i+1}" for i in range(len(tour_operator_totals))])

    # Calculate course totals
    course_totals = month_bookings[month_bookings['Activity Type'].isin(['OWC', 'AOW', 'DSD', 'DM'])].groupby('Activity Type')['Name'].nunique().reset_index(name='Total Guests')
    course_names = pd.DataFrame([course_totals['Activity Type'].values], 
                                index=['Courses'], 
                                columns=[f"Course {i+1}" for i in range(len(course_totals))])
    course_values = pd.DataFrame([course_totals['Total Guests'].values], 
                                 index=['Total Guests'], 
                                 columns=[f"Course {i+1}" for i in range(len(course_totals))])

    # Append tour operator and course totals to the end of the DataFrame
    # First, add placeholder columns for totals
    total_columns = list(tour_operator_names.columns) + list(course_names.columns)
    month_df[total_columns] = 0  # Add empty columns for totals

    # Append tour operator and course totals
    month_df = pd.concat([month_df, tour_operator_names, tour_operator_values, course_names, course_values])

    return month_df
   



generate_monthly_schedule(ready, 2023, 2)