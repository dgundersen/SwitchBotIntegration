import json
from switchbot.api_interface import ApiInterface


# Switch-Bot reference
# https://github.com/OpenWonderLabs/SwitchBotAPI
class SwitchBotApi(ApiInterface):

    DEFAULT_CONFIG_FILE_PATH = 'switchbot_config.json'

    def __init__(self):
        super(SwitchBotApi, self).__init__(
            base_url='https://api.switch-bot.com/v1.0/'
        )

        # TODO: error handling for missing file or token
        config = self.load_json_file(self.DEFAULT_CONFIG_FILE_PATH)

        self.token = config['token']
        self.desklight_device_id = config['desklight_device_id']

    def load_json_file(self, file_name_and_path):
        json_file = None

        try:
            with open(file_name_and_path, 'r') as f:
                json_file = json.load(f)
        except Exception as ex:
            self.log.error(ex, exc_info=False)

        return json_file

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




