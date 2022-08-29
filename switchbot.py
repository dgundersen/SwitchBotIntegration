import sys
from switchbot.switchbot_api import SwitchBotApi
from switchbot.switchbot_devices import Meter

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

def print_meter_readings():
    print('Getting temp/humidity..\n')

    switchbot = SwitchBotApi()

    # TODO: configure list of meter ids rather than fetching them every time
    devices = switchbot.get_devices()

    meters = []

    if devices:
        for device in devices:
            print(device)

            if 'deviceType' in device and device['deviceType'] == 'Meter':
                meter = Meter(name=device['deviceName'])

                status = switchbot.get_device_status(device['deviceId'])

                meter.set_measurements(temp=status['temperature'], humidity=status['humidity'])

                meters.append(meter)
    else:
        print('No devices found')

    if meters:
        meters = sorted(meters, key=lambda x: x.device_name)

        for meter in meters:
            print(meter)
    else:
        print('No meters found')



if __name__ == '__main__':
    command = sys.argv[1] if len(sys.argv) > 1 else None

    if command == 'desklight':
        desklight()
    elif command == 'temp':
        print_meter_readings()
    else:
        test_devices(bot_press=False)


