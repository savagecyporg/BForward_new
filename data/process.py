
import re
import pandas as pd
from calendar import monthrange



def parse_activity(activity):
    """
    Parse a diving activity string to extract the number of divers, diving days, and activity type.
    Handles combined activities (e.g., "OWC/3DD") and appends AI/EANX as additional services.

    Parameters:
    activity (str): The activity string to parse.

    Returns:
    tuple: A tuple containing (divers, diving_days, activity_type).
    """
    if pd.isna(activity) or activity == 'NAN':
        return 0, 0, 'Unknown'  # No divers or days for NAN activities

    # Ignore specific cases like "INS" (insurance) or "Unknown"
    if re.search(r'(?i)\bINS\b', activity) or re.search(r'(?i)\bUnknown\b', activity):
        return 0, 0, 'Ignored'  # Return 0 divers, 0 days, and mark as 'Ignored'

    # Define activity patterns and their corresponding values
    activity_patterns = {
        r'(?i)\bND\b': (0, 0, 'NON DIVER'),  # Non-diver
        r'(?i)\bAI\b': (1, 0, 'AI'),  # All-Inclusive (additional service)
        r'(?i)\bCASH\b': (1, 0, 'CASH'),  # Cash payment
        r'(?i)\bOWC[D]?\b': (1, 3, 'OWC'),  # Open Water Course
        r'(?i)\bAOW\b': (1, 2, 'AOW'),  # Advanced Open Water
        r'(?i)\bDSD\b': (1, 1, 'DSD'),  # Discover Scuba Diving
        r'(?i)\bSNK\b': (0, 0, 'Snorkeling'),  # Snorkeling
        r'(?i)\bSD-UPG\b': (1, 2, 'SD-UPG'),  # Skill Development Upgrade
        r'(?i)\bSD\b': (1, 2, 'SD'),  # Skill Development Upgrade
        r'(?i)\bSR\b': (1, 1, 'SR'),  # Specialty Refresher
        r'(?i)\bDM\b': (1, 10, 'DM'),  # Dive Master
        r'(?i)\bSHARE\b': (0, 0, 'SHARING'),  # Sharing
        r'(?i)\bEANX\b': (1, 0, 'EANX'),  # Enriched Air Nitrox (additional service)
        r'(?i)\bNTX\b': (1, 0, 'NTX'),  # Nitrox course
        r'(?i)\bCD\b': (1, 0, 'CD'),  # Check Dive
    }

    parts = re.split(r'[/]+', activity)
    total_divers = 0
    total_diving_days = 0
    activity_types = []
    additional_services = []

    for part in parts:
        part = part.strip()
        divers = 0
        diving_days = 0
        activity_type = 'Unknown'

        # Check for specific activity types
        matched = False
        for pattern, (d, dd, at) in activity_patterns.items():
            if re.search(pattern, part):
                divers, diving_days, activity_type = d, dd, at
                matched = True
                break

        # If no specific activity is matched, check for generic patterns
        if not matched:
            divers_match = re.search(r'(?i)x\s*(\d+)', part)
            days_match = re.search(r'(?i)(\d+)DD', part)

            if divers_match:
                divers = int(divers_match.group(1))
            if days_match:
                diving_days = int(days_match.group(1))
                activity_type = 'Diver'

        # Extract diving days from "DD" suffix for AI
        if activity_type == 'AI':
            days_match = re.search(r'(?i)(\d+)DD', part)
            if days_match:
                diving_days = int(days_match.group(1))

        # Update totals
        total_divers += divers
        total_diving_days += diving_days

        # Append activity type or additional service
        if activity_type in ['AI', 'EANX', 'CD', 'NTX', 'SR', 'SD', 'SD-UPG', 'OWC', 'AOW', 'DM']:
            additional_services.append(activity_type)  # Treat AI/EANX as additional services
        elif activity_type != 'Unknown':
            activity_types.append(activity_type)

    # Combine activity types and additional services
    combined_activity_type = '/'.join(activity_types) if activity_types else 'Unknown'
    if additional_services:
        combined_activity_type += f" (+{', '.join(additional_services)})"

    return total_divers, total_diving_days, combined_activity_type



