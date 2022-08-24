import json


class AppConfig:

    DEFAULT_CONFIG_FILE_PATH = '..\\switchbot_config.json'

    def get_config(self):
        # TODO: error handling for missing file or token
        return self.load_json_file(self.DEFAULT_CONFIG_FILE_PATH)

    def load_json_file(self, file_name_and_path):
        json_file = None

        try:
            with open(file_name_and_path, 'r') as f:
                json_file = json.load(f)
        except Exception as ex:
            print(f'Exception opening file: {ex}')

        return json_file

