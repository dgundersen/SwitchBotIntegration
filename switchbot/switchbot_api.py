from switchbot.api_interface import ApiInterface
from switchbot.config import AppConfig


# Switch-Bot reference
# https://github.com/OpenWonderLabs/SwitchBotAPI
class SwitchBotApi(ApiInterface):

    def __init__(self):
        super(SwitchBotApi, self).__init__(
            base_url='https://api.switch-bot.com/v1.0/'
        )

        app_config = AppConfig()

        self.token = app_config.config['token']
        self.desklight_device_id = app_config.config['desklight_device_id']

    def _get_body_from_response(self, resp):
        if resp and 'message' in resp:
            if resp['message'] == 'success' and 'body' in resp:
                return resp['body']
            else:
                print(f'ERROR: {resp["message"]}')
        else:
            print('Unknown error')

        return None

    # GET /v1.0/devices
    def get_devices(self):

        resp = self._api_request(endpoint='devices', access_token=self.token)

        body = self._get_body_from_response(resp)

        if body and 'deviceList' in body:
            return body['deviceList']

        return []

    # GET /v1.0/devices/{deviceId}/status
    def get_device_status(self, device_id):

        resp = self._api_request(endpoint=f'devices/{device_id}/status', access_token=self.token)

        body = self._get_body_from_response(resp)

        return body

    # POST /v1.0/devices/{deviceId}/commands
    def bot_press(self, device_id):

        cmd_params = {
            "command": "press",
            "parameter": "default",
            "commandType": "command"
        }

        resp = self._api_request(endpoint=f'devices/{device_id}/commands', params=cmd_params, method='POST', access_token=self.token)

        body = self._get_body_from_response(resp)

        return body




