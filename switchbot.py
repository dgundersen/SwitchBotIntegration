import sys
from switchbot.switchbot_api import SwitchBotApi


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


if __name__ == '__main__':
    command = sys.argv[1] if len(sys.argv) > 1 else None

    if command == 'desklight':
        desklight()
    else:
        test_devices(bot_press=True)


