import sys
from switchbot.switchbot_api import SwitchBotApi
from switchbot.switchbot_devices import Meter
from switchbot.config import AppConfig
from timestream.write_client import WriteClient

def test_devices(bot_press=False):

    switchbot = SwitchBotApi()

    devices = switchbot.get_devices()

    print('DEVICES:')
    print(devices)

    for device in devices:
        print(f"Getting status for {device['deviceId']}")

        status = switchbot.get_device_status(device['deviceId'])

        print(status)

        if bot_press and status and 'deviceType' in status and status['deviceType'] == 'Bot':
            switchbot.bot_press(device['deviceId'])


def desklight():

    switchbot = SwitchBotApi()

    switchbot.bot_press(switchbot.desklight_device_id)

# {'deviceId': 'FD184178F166', 'deviceName': 'Temp 1 Basement', 'deviceType': 'Meter', 'enableCloudService': True, 'hubDeviceId': 'E248AB2668E1'}
def get_meters_from_api_devices():

    switchbot = SwitchBotApi()

    devices = switchbot.get_devices()

    meters = []

    if devices:
        for device in devices:
            # print(device)

            if 'deviceType' in device and device['deviceType'] == 'Meter':
                meter = Meter(name=device['deviceName'], device_id=device['deviceId'])

                status = switchbot.get_device_status(device['deviceId'])

                meter.set_measurements(temp=status['temperature'], humidity=status['humidity'])

                meters.append(meter)

    else:
        print('No devices found')

    return meters

# Gets temp/humidity and prints to console
def print_meter_readings():
    print('Getting temp/humidity..\n')

    meters = get_meters_from_api_devices()

    if meters:
        meters = sorted(meters, key=lambda x: x.device_name)

        for meter in meters:
            print(meter)

    else:
        print('No meters found')

# Gets temp/humidity and stores in timestream
def record_meter_readings():
    print('Recording temp/humidity..')

    meters = get_meters_from_api_devices()

    if meters:

        app_config = AppConfig()

        aws_config = app_config.config['aws']

        write_client = WriteClient(region="us-east-1", aws_config=aws_config)

        current_time = write_client.current_milli_time()

        records = []
        for meter in meters:

            dimensions = [
                {'Name': 'deviceName', 'Value': meter.device_name},
                {'Name': 'deviceType', 'Value': 'Meter'},
                {'Name': 'deviceId', 'Value': meter.device_id}
            ]

            # All values have to be passed as strings, even if the value type is numerical
            temp = {
                'Dimensions': dimensions,
                'MeasureName': 'temperature',
                'MeasureValue': str(meter.temperature),
                'MeasureValueType': 'DOUBLE',
                'Time': current_time
            }

            humid = {
                'Dimensions': dimensions,
                'MeasureName': 'humidity',
                'MeasureValue': str(meter.humidity),
                'MeasureValueType': 'DOUBLE',
                'Time': current_time
            }

            records.append(temp)
            records.append(humid)

        print('Writing records')
        write_client.write_records(
            database_name=aws_config['timestream_db_name'],
            table_name=aws_config['timestream_db_table'],
            records=records
        )

    else:
        print('No meters found')


if __name__ == '__main__':
    command = sys.argv[1] if len(sys.argv) > 1 else None

    if command == 'desklight':
        desklight()
    elif command == 'temp':
        print_meter_readings()
    elif command == 'temp_record':
        record_meter_readings()
    else:
        test_devices(bot_press=False)


