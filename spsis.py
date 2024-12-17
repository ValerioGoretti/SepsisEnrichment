import xml.etree.ElementTree as ET
import pandas as pd
import matplotlib.pyplot as plt

# Function to parse XES file and extract data
def parse_xes(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Define XES namespace
    namespace = {'xes': 'http://www.xes-standard.org/'}

    # Prepare a list to store events
    data = []

    # Iterate over traces
    for trace in root.findall('trace', namespace):
        print(trace)
        case_id = None
        case_attributes = {}

        # Extract case attributes
        for attr in trace.findall('string', namespace):
            if attr.get('key') == 'concept:name':
                print(attr.get('value'))
                case_id = attr.get('value')
            else:
                case_attributes[attr.get('key')] = attr.get('value')

        for attr in trace.findall('int', namespace):
            case_attributes[attr.get('key')] = int(attr.get('value'))

        for attr in trace.findall('float', namespace):
            case_attributes[attr.get('key')] = float(attr.get('value'))

        for attr in trace.findall('boolean', namespace):
            case_attributes[attr.get('key')] = attr.get('value') == 'true'

        # Extract events in the trace
        for event in trace.findall('event', namespace):
            event_data = case_attributes.copy()
            event_data['case_id'] = case_id

            for attr in event.findall('int', namespace):
                event_data[attr.get('key')] = int(attr.get('value'))

            for attr in event.findall('string', namespace):
                event_data[attr.get('key')] = attr.get('value')

            for attr in event.findall('date', namespace):
                event_data[attr.get('key')] = attr.get('value')

            for attr in event.findall('float', namespace):
                event_data[attr.get('key')] = float(attr.get('value'))

            for attr in event.findall('boolean', namespace):
                event_data[attr.get('key')] = attr.get('value') == 'true'

            data.append(event_data)

    return pd.DataFrame(data)

def analyze_age_distribution(df, age_column='age'):
    # Convert age values to numeric, ignoring errors
    df[age_column] = pd.to_numeric(df[age_column], errors='coerce')

    # Drop rows with NaN age
    age_data = df[age_column].dropna()

    # Summary statistics
    print("Age Statistics:")
    print(age_data.describe())

    # Plot distribution
    plt.figure(figsize=(10, 6))
    plt.hist(age_data, bins=20, color='skyblue', edgecolor='black')
    plt.title("Distribution of Ages")
    plt.xlabel("Age")
    plt.ylabel("Frequency")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()

# Load and parse the XES file
file_path = 'Sepsis/sepsis.xes'
event_log_df = parse_xes(file_path)

# Save the parsed data to a CSV for further analysis
event_log_df.to_csv('event_log.csv', index=False)

# Display summary of the data
print("Event log parsed successfully!")
print(event_log_df.head())

# Example analysis: Count events per case
case_event_counts = event_log_df.groupby('case_id').size()
print("\nNumber of events per case:")
print(case_event_counts)

# Example: Analyze activities by frequency
activity_counts = event_log_df['concept:name'].value_counts()
print("\nActivity frequency:")
print(activity_counts)


print(event_log_df.columns)


# Analyze and plot age distribution
analyze_age_distribution(event_log_df, age_column='Age')