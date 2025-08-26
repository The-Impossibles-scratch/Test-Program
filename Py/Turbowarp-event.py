import websocket
import json
import threading

project_id = "あなたのプロジェクトID"
username = "PythonBot"

first_handshake_done = False  # 最初のハンドシェイク確認用フラグ

def on_message(ws, message):
    global first_handshake_done
    for line in message.strip().split("\n"):
        if not line.strip():
            continue
        try:
            data = json.loads(line)
        except json.JSONDecodeError:
            print("[WARN] JSON decode失敗:", line)
            continue

        # 接続直後の既存値は無視
        if not first_handshake_done:
            continue

        print("[RAW]", data)

        if data.get("method") == "set":
            var_name = data["name"].replace("☁ ", "")
            value = data["value"]
            user = data.get("user", "?")  # Scratch側はuser情報を送ってこないので無い場合が多い
            print(f"[EVENT] {user} set {var_name} = {value}")

    # 最初のメッセージを受け取ったらフラグを立てる
    if not first_handshake_done:
        first_handshake_done = True

def on_open(ws):
    print("[INFO] Connected! Sending handshake as", username)
    handshake = {
        "method": "handshake",
        "user": username,
        "project_id": project_id
    }
    ws.send(json.dumps(handshake))

def on_close(ws, close_status_code, close_msg):
    print(f"[INFO] Connection closed {close_status_code} {close_msg}")

def run():
    ws = websocket.WebSocketApp(
        "wss://clouddata.scratch.mit.edu",
        on_open=on_open,
        on_message=on_message,
        on_close=on_close
    )
    ws.run_forever()

if __name__ == "__main__":
    run()
