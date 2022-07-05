import requests, json


DEBUG = False


# TODO: move this into a shared repo to be used by multiple sites
class ApiInterface(object):

    MAX_RETRIES = 3

    def __init__(self, base_url, additional_headers=None):
        self.BASE_URL = base_url
        self.additional_headers = additional_headers


    def _api_request(self, endpoint, params=None, method='GET', access_token=None, is_json=True, retry_failed=True):
        url = self.BASE_URL + endpoint

        if not access_token:
            # TODO: method for getting default token?
            pass

        headers = {
            'Content-type': 'application/json'
        } if is_json else {
            'Content-type': 'application/x-www-form-urlencoded'
        }

        if access_token:
            headers['Authorization'] = f'Bearer {access_token}'

        if self.additional_headers:
            headers.update(self.additional_headers)


        request_succeeded = False
        try:
            if method == 'POST':
                r = requests.post(url, json=params, headers=headers) if is_json else requests.post(url, data=params, headers=headers)

                request_succeeded = True

            else:
                r = requests.get(url, params=params, headers=headers)

                request_succeeded = True

        except Exception as e:
            print(f'Exception: {e}')

            if retry_failed:
                r = self._retry_request(method=method, url=url, params=params, headers=headers, is_json=is_json)


        if DEBUG and request_succeeded and r is not None and r.text:
            print(r.text)

        # Need to check 'if r is not None' and not just 'if r'
        resp_data = json.loads(r.text if request_succeeded and r is not None and r.text else '')

        error_msg = None

        # TODO: log api errors

        return resp_data


    def _retry_request(self, method, url, params, headers, is_json, retry_num=0):

        retry_num +=1
        if retry_num > self.MAX_RETRIES:
            if DEBUG:
                print('Max retries reached')
            return None

        if DEBUG:
            print(f'retrying {method}')

        try:
            if method == 'POST':
                r = requests.post(url, json=params, headers=headers) if is_json else requests.post(url, data=params, headers=headers)

                return r

            else:
                r = requests.get(url, params=params, headers=headers)

                return r

        except Exception as e:
            print(f'Exception: {e}')

            self._retry_request(method=method, url=url, params=params, headers=headers, is_json=is_json, retry_num=retry_num)

