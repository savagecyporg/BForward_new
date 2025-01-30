mapping = {
    'Hotel':{
        't_name':'Hotel List',
        'id_col': 'Hotel ID',
        'name_col':'Hotel Name',
    },
    'Country':{
        't_name':'Countries',
        'id_col': 'Country ID',
        'name_col':'Country Name',
    },
    'Tour Operator':{
        't_name':'Tour Operators',
        'id_col': 'ID Tour',
        'name_col':'Tour Operators',}
}




def replace_ids_with_names(actual_guest, mapping, tables_df):
    """
    Replace IDs in the Actual Guest DataFrame with corresponding names based on mapping tables.

    Parameters:
    actual_guest (pd.DataFrame): The DataFrame containing IDs to be replaced.
    mapping (dict): A dictionary specifying the mapping between columns and lookup tables.
    tables_df (dict): A dictionary of DataFrames containing the lookup tables.

    Returns:
    pd.DataFrame: A copy of the Actual Guest DataFrame with IDs replaced by names.
    """
    # Create a copy of the Actual Guest DataFrame to avoid modifying the original
    actual_guest_copy = actual_guest.copy()
    for column_name, details in mapping.items():
        # Check if the column exists in the Actual Guest DataFrame
        if column_name in actual_guest_copy.columns:
            # Get the lookup table and columns
            lookup_table = tables_df[details['t_name']]
            id_col = details['id_col']
            name_col = details['name_col']
            id_to_name_map = dict(zip(lookup_table[id_col], lookup_table[name_col]))

            # Replace IDs with names in the Actual Guest DataFrame
            actual_guest_copy[column_name] = actual_guest_copy[column_name].map(id_to_name_map)

            # Handle cases where IDs are not found in the lookup table
            actual_guest_copy[column_name] = actual_guest_copy[column_name].fillna('Unknown')

    return actual_guest_copy



