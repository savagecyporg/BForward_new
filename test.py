

def add_summary_rows(main_df, month_bookings):
    # Append summary rows at the end
    total_guests = pd.DataFrame([['Total Guests (Diving/Courses)', '', '']], columns=main_df.columns, index=['Total Guests'])
    cash_summary = pd.DataFrame([['Total Cash', '', '']], columns=main_df.columns, index=['Total Cash'])
    
    # Insert total guests row immediately below the last added column (assuming no additional rows have been appended yet)
    start_idx = len(main_df.columns)  # Assuming no other rows have been added yet
    main_df = pd.concat([main_df.iloc[:, :start_idx], total_guests, main_df.iloc[:, start_idx:]])

    # Calculate totals per tour operator for the entire month
    tour_operator_totals = month_bookings.groupby('Tour Operator')['Name'].nunique().reset_index(name='Total Guests')

    # Create two rows for tour operator totals: one for names, one for totals
    tour_operator_names = pd.DataFrame([tour_operator_totals['Tour Operator'].values], 
                                       index=['Tour Operators'], 
                                       columns=[f"Operator {i+1}" for i in range(len(tour_operator_totals))])
    
    # Insert tour operator names row immediately below 'Total Guests (Dest_year = 2023  # Replace with the year you want to test
test_month = 10   # Replace with the month you want to test

add_summary_rows(month, test_month)
