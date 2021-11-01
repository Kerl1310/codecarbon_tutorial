from codecarbon import EmissionsTracker
import boto3
import csv
import os

emissions_tracker = EmissionsTracker(project_name='emissions_demo')
# cloudwatch_client = boto3.client('cloudwatch')

def handler():
    emissions_tracker.start()
    my_business_logic()
    emissions_tracker.stop()
    timestamp, emissions_in_kg, energy_consumption_in_kwh = get_emissions_data_from_file()
    delete_emissions_file()
    upload_emissions(emissions_in_kg, timestamp)
    # upload_energy_consumption(energy_consumption_in_kwh, timestamp)

def my_business_logic():
    my_list = []
    my_list.append('Hello')
    my_list.append('World')
    print(my_list)

def get_emissions_data_from_file():
    with open('emissions.csv', newline='') as f:
        i = 0
        reader = csv.reader(f)
        for row in reader:
            if i == 0:
                i += 1
                continue
            timestamp = row[0]
            emissions_in_kg = row[4]
            energy_consumption_in_kwh = row[5]
            print('timestamp: ' + str(timestamp))
            print('emissions_in_kg: ' + str(emissions_in_kg))
            print('energy_consumption_in_kwh: ' + str(energy_consumption_in_kwh))
            return timestamp, emissions_in_kg, energy_consumption_in_kwh

def delete_emissions_file():
    os.remove("emissions.csv")

def upload_emissions(emissions_in_kg, timestamp):
    return upload_to_cloudwatch('emissions_in_kg', emissions_in_kg, 'kg', timestamp)

# def upload_energy_consumption(emissions_in_kg, timestamp):
#     return upload_to_cloudwatch('energy_consumption_in_kwh', energy_consumption_in_kwh, 'kWh', timestamp)

def upload_to_cloudwatch(metric_name, value, unit, timestamp):
    return cloudwatch_client.put_metric_data(
        Namespace='EmissionsDemo',
        MetricData=[
            {
                'MetricName': 'emissions_in_kg',
                'Value': emissions_in_kgm,
                'Unit': 'kg',
                'Timestamp': emissions_timestamp
            },
        ]
    )

handler()