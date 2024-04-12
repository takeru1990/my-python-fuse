import requests
import json
import pathlib
import pprint

def get_json(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return json.loads(response.text)
        else:
            print(f"Error: HTTP status code {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

# 設定ファイルパスを指定
config_path = pathlib.Path("~/.config/silo/config.json").expanduser()

# ファイルを読み込む
try:
  with open(config_path, "r") as f:
    config = json.load(f)
except FileNotFoundError:
  print("Silo 設定ファイルが見つかりません: ~/.config/silo/config.json")
  exit(1)

# "url" キーの値を取得
url = config.get("url")

# url が存在するかどうかを確認
if url is None:
  print("Silo 設定ファイルに 'url' キーが見つかりません")
  exit(1)

# HTTP get を実行
data = get_json(url)

if data:
    pprint.pprint(data)
else:
    print("JSON データの取得に失敗しました。")