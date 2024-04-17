import requests
import json
import pathlib

class Silo:
    def __init__(self):
        # 設定ファイルパスを指定
        config_path = pathlib.Path("~/.config/silo/config.json").expanduser()

        # ファイルを読み込む
        try:
            with open(config_path, "r") as f:
                self.config = json.load(f)
        except FileNotFoundError:
            print("Silo 設定ファイルが見つかりません: ~/.config/silo/config.json")
            exit(1)

        # "url" キーの値を取得
        if self.config.get("url") is None:
            print("Silo 設定ファイルに 'url' キーが見つかりません")
            exit(1)
        else:
            self.url = self.config.get("url")


    def _build_url(self, path):
        # path の先頭の '/' を削除
        path = path.lstrip('/')
        return f"{self.url}/{path}"

    def get_json(self, path):
        url = self._build_url(path)

        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = json.loads(response.text)
                for d in data:
                    d['filePath'] = d['filePath'][6:]
                print(f'### get_json() called! Response is {data}')
                return data
            else:
                print(f"Error: HTTP status code {response.status_code}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return None

    def get_file(self, path):
        url = self._build_url(path)

        try:
            response = requests.get(url)
            if response.status_code == 200:
                print(f'### get_file() is called! Path is {path}')
                print(f'### get_file() called! Header Content-type is {response.headers["Content-Type"]}')
                return response.content
            else:
                print(f"Error: HTTP status code {response.status_code}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return None

    def delete_file(self, path):
        url = self._build_url(path)

        try:
            response = requests.delete(url)
            if response.status_code == 204:
                print(f'### delete_file() is called! Path is {path}')
                print(f'### delete_file() called! Status code is {response.status_code}')
                return 0
            else:
                print(f"Error: HTTP status code {response.status_code}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return None
