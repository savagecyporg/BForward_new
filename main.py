from data.export import AccessExporter
from data.settings import *
from data.process import parse_activity
from data.month_state import generate_monthly_schedule, add_summary_rows



access_path = '/home/ag/Desktop/GP/gp/gp.accdb'
sqlite_path = '/home/ag/Desktop/GP/project/_db'
Gp = AccessExporter(access_path)
tables = Gp.export_all_tables()
db = Gp.load_db(sqlite_path)
actual_guest = replace_ids_with_names(db['Actual Guest'],mapping,tables) 



ready = actual_guest
ready['Arrival'] = pd.to_datetime(ready['Arrival'])
#divers, diving_days, activity_types = zip(*ready['Booked Activity'].map(parse_activity))
#ready['Divers'] = list(divers)
#ready['Diving Days'] = list(diving_days)
#ready['Activity Type'] = list(activity_types)

test_year = 2023  # Replace with the year you want to test
test_month = 2   # Replace with the month you want to test
month_df = generate_monthly_schedule(ready, test_year, test_month)




output_file = 'monthly_diving_schedule_with_summary.xlsx'  # Name of the output Excel file
month_df.to_excel(output_file, sheet_name='Diving Schedule', index=True, na_rep='')


month_df








