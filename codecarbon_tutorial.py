from codecarbon import EmissionsTracker
from decimal import Decimal
import boto3
import csv
import os

emissions_tracker = EmissionsTracker(project_name='emissions_demo')
cloudwatch_client = boto3.client('cloudwatch', 'eu-west-1')

def handler():
    '''
    This is my handler function
    '''
    # Track the emissions of our business logic
    emissions_tracker.start()
    my_business_logic()
    emissions_tracker.stop()

    # Extract the data we want to keep from the file
    timestamp, emissions_in_kg, energy_consumption_in_kwh = get_emissions_data_from_file()

    # Remove file created by CodeCarbon
    delete_emissions_file()

    # Upload metrics for visibility
    upload_emissions(emissions_in_kg, timestamp)
    upload_energy_consumption(energy_consumption_in_kwh, timestamp)

def my_business_logic():
    '''
    My business logic should go in here
    '''
    my_list = []
    my_list.append('Hello')
    my_list.append('World')
    my_list.reverse()
    print(my_list)

def get_emissions_data_from_file():
    '''
    Gets the emissions data from the file produced by CodeCarbon
    '''
    with open('emissions.csv', newline='') as f:
        i = 0
        reader = csv.reader(f)
        for row in reader:
            if i == 0:
                i += 1
                continue
            if row == []:
                i += 1
                continue

            timestamp = row[0]
            emissions_in_kg = format(Decimal(row[4]), '.10f')
            energy_consumption_in_kwh = format(Decimal(row[5]), '.10f')

            print('timestamp: ' + str(timestamp))
            print('emissions_in_kg: ' + str(emissions_in_kg))
            print('energy_consumption_in_kwh: ' + str(energy_consumption_in_kwh))
            
            return timestamp, emissions_in_kg, energy_consumption_in_kwh

def delete_emissions_file():
    '''
    Removes the file produced by CodeCarbon
    '''
    os.remove("emissions.csv")

def upload_emissions(emissions_in_kg, timestamp):
    '''
    Uploads emissions to improve visibility
    '''
    return upload_custom_metric_to_cloudwatch('emissions_in_kg', emissions_in_kg, timestamp)

def upload_energy_consumption(energy_consumption_in_kwh, timestamp):
    '''
    Uploads energy consumption to improve visibility
    '''
    return upload_custom_metric_to_cloudwatch('energy_consumption_in_kwh', energy_consumption_in_kwh, timestamp)

def upload_custom_metric_to_cloudwatch(metric_name, value, timestamp):
    '''
    Uploads custom metric to CloudWatch
    '''
    return cloudwatch_client.put_metric_data(
        Namespace='EmissionsDemo',
        MetricData=[
            {
                'MetricName': metric_name,
                'Value': Decimal(value),
                'Unit': 'None',
                'Timestamp': timestamp
            },
        ]
    )

handler()