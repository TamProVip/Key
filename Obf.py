import base64
import os
import json
import random
import requests
import sys
import uuid
from datetime import datetime, timedelta
import string
import platform

# =========================
# ==== Firebase Config ====
# =========================
FIREBASE_BASE = "https://server-a1e13-default-rtdb.firebaseio.com"
FIREBASE_KEYS_URL = f"{FIREBASE_BASE}/keys.json"
REQUEST_TIMEOUT = 10  # giây

# Nếu bạn dùng Firebase Auth (database secret / idToken), thêm ?auth=... vào URL:
# FIREBASE_KEYS_URL = f"{FIREBASE_BASE}/keys.json?auth=<YOUR_TOKEN>"

# ============================================
# ==== Base64 encrypt/decrypt local backup ====
# ============================================
def encrypt_data(data: str) -> str:
    return base64.b64encode(data.encode()).decode()

def decrypt_data(encrypted_data: str) -> str:
    return base64.b64decode(encrypted_data.encode()).decode()

# ======================================
# ==== Device ID và thông tin máy ======
# ======================================
def get_fixed_device_id():
    file_path = 'device_info.json'
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                info = json.load(f)
            return info['device_id'], info['machine_name'], info['platform']
        except Exception:
            pass

    device_id = str(uuid.getnode())
    machine_name = platform.node()
    machine_platform = f"{platform.system()} {platform.release()}"

    info = {
        'device_id': device_id,
        'machine_name': machine_name,
        'platform': machine_platform
    }
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(info, f, indent=2)
    return device_id, machine_name, machine_platform

def display_device_info(device_id, machine_name, machine_platform):
    print(f"ID Thiết Bị: {device_id}")
    print(f"Tên máy: {machine_name}")
    print(f"Hệ điều hành: {machine_platform}")

# =================================
# ==== Lưu/Load key local =========
# =================================
def luu_thong_tin_device(device_id, key, expiration_date: datetime):
    data = {device_id: {'key': key, 'expiration_date': expiration_date.isoformat()}}
    encrypted_data = encrypt_data(json.dumps(data))
    with open('device_key.json', 'w', encoding='utf-8') as file:
        file.write(encrypted_data)

def tai_thong_tin_device():
    try:
        with open('device_key.json', 'r', encoding='utf-8') as file:
            return json.loads(decrypt_data(file.read()))
    except Exception:
        return None

def kiem_tra_device(device_id):
    data = tai_thong_tin_device()
    if data and device_id in data:
        try:
            exp = datetime.fromisoformat(data[device_id]['expiration_date'])
            if exp > datetime.now():
                return data[device_id]['key']
        except Exception:
            pass
    return None

# =================================
# ==== Firebase API helpers =======
# =================================
def firebase_get_keys() -> dict:
    try:
        r = requests.get(FIREBASE_KEYS_URL, timeout=REQUEST_TIMEOUT)
        if r.status_code == 200:
            return r.json() or {}
        print("Không lấy được keys từ Firebase:", r.status_code, r.text)
        return {}
    except Exception as e:
        return {}

def firebase_put_keys(data: dict) -> bool:
    """Ghi đè toàn bộ node /keys (PUT)."""
    try:
        r = requests.put(FIREBASE_KEYS_URL, json=data, timeout=REQUEST_TIMEOUT)
        return r.status_code == 200
    except Exception as e:
        return False

def firebase_patch_keys(partial: dict) -> bool:
    """Cập nhật một phần node /keys (PATCH). Tránh ghi đè toàn bộ."""
    try:
        url = FIREBASE_KEYS_URL  # .../keys.json
        r = requests.patch(url, json=partial, timeout=REQUEST_TIMEOUT)
        return r.status_code == 200
    except Exception as e:
        return False

# =================================
# ==== Key free & tiện ích ========
# =================================
def generate_free_key():
    random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    key = f'KeyFree-{random_part}'
    expiration_date = datetime.now().replace(hour=23, minute=59, second=0, microsecond=0)
    url = f'https://www.webkey.x10.mx/?ma={key}'
    return url, key, expiration_date

def get_shortened_link_phu(url, max_retries=5):
    """Thử rút gọn link nhiều lần cho tới khi thành công."""
    token = "67cfdd9135fa313c8c20c795"
    api_url = f"https://link2m.net/api-shorten/v2?api={token}&url={url}"

    for _ in range(max_retries):
        try:
            response = requests.get(api_url, timeout=8)
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "success" and "shortenedUrl" in data:
                    return data
        except Exception as e:
            last_error = str(e)
    return {"status": "error", "message": last_error if 'last_error' in locals() else "Không kết nối dịch vụ rút gọn URL."}

# =================================
# ==== Server (global) key =========
# =================================
def tao_server_key(days=30):
    key = "ServerKey-" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))
    expiration_date = (datetime.now() + timedelta(days=days)).isoformat()
    payload = {
        "all": {
            "key": key,
            "expiration_date": expiration_date
        }
    }
    if firebase_patch_keys(payload):
        print(f" Đã tạo/ghi đè Server Key: {key}")
        print(f" Hết hạn vào: {expiration_date}")
    else:
        print(" Lỗi khi cập nhật server key lên Firebase")

# =================================
# ============ Main ================
# =================================
def main():
    device_id, machine_name, machine_platform = get_fixed_device_id()
    display_device_info(device_id, machine_name, machine_platform)

    # Lấy keys từ Firebase
    keys_data = firebase_get_keys()
    if not isinstance(keys_data, dict):
        keys_data = {}

    # 1) Kiểm tra key 'all' (server key)
    global_key = None
    exp_all = None
    if "all" in keys_data:
        try:
            exp_all = datetime.fromisoformat(keys_data["all"]["expiration_date"])
            if exp_all > datetime.now():
                global_key = keys_data["all"]["key"].strip()
        except Exception as e:
            pass

    if global_key:
        print(f" Key Free Chung từ server: {global_key}")
        luu_thong_tin_device(device_id, global_key, exp_all)
        return

    # 2) Kiểm tra key riêng cho device
    existing_key = None
    exp_device = None
    if device_id in keys_data:
        try:
            exp_device = datetime.fromisoformat(keys_data[device_id]['expiration_date'])
            if exp_device > datetime.now():
                existing_key = keys_data[device_id]['key'].strip()
            else:
                # Key hết hạn → thu hồi
                print(f" Key device {device_id} đã hết hạn, thu hồi...")
                if firebase_patch_keys({device_id: None}):
                    pass
                else:
                    print("⚠️ Không xóa được key hết hạn trên Firebase.")
        except Exception as e:
            pass

    if existing_key:
        print(f" Sử dụng key server cho thiết bị: {existing_key}")
        print(f" Hết hạn vào: {exp_device.strftime('%d-%m-%Y %H:%M:%S')}")
        luu_thong_tin_device(device_id, existing_key, exp_device)
        return

    # 3) Kiểm tra key local
    local_key = kiem_tra_device(device_id)
    if local_key:
        if (device_id in keys_data and 'key' in keys_data[device_id] and
            keys_data[device_id]['key'].strip() == local_key.strip()):
            try:
                exp_local = datetime.fromisoformat(keys_data[device_id]['expiration_date'])
                if exp_local > datetime.now():
                    print(f" Key hợp lệ từ file local: {local_key}")
                    return
            except Exception:
                pass
        print(f" Key local {local_key} đã bị thu hồi hoặc hết hạn.")
        if os.path.exists('device_key.json'):
            os.remove('device_key.json')

    # 4) Tạo key free mới
    url, key, expiration_date = generate_free_key()
    print("Nhập 1 để lấy key (Free)")

    while True:
        choice = input("Nhập lựa chọn: ").strip()
        if choice == "1":
            short_data = get_shortened_link_phu(url)
            link_key = short_data.get('shortenedUrl') or url
            print(f"Link lấy key: {link_key}")
            while True:
                keynhap = input("Nhập key đã nhận: ").strip()
                if keynhap == key:
                    print(" Key đúng — Mời bạn dùng Tool")
                    luu_thong_tin_device(device_id, key, expiration_date)
                    payload = {
                        device_id: {
                            "key": key,
                            "expiration_date": expiration_date.isoformat()
                        }
                    }
                    if firebase_patch_keys(payload):
                        print(" Đã lưu key của thiết bị lên server Firebase.")
                    else:
                        print("⚠️ Lưu key thiết bị lên server thất bại, nhưng vẫn dùng key local.")
                    return
                else:
                    print(f" Key sai — Vui lòng nhập lại hoặc truy cập: {link_key}")
        else:
            print("Vui lòng nhập 1.")

if __name__ == '__main__':
    main()
import requests, sys, time

url_raw = "https://raw.githubusercontent.com/TamProVip/Key/refs/heads/main/v.py"
url_api = "https://api.github.com/repos/TamProVip/Key/contents/v.py?ref=main"
headers = {"Accept": "application/vnd.github.v3.raw"}

while True:
    try:
        try:
            data = requests.get(url_raw, timeout=10).text
            if len(data) < 20:
                raise ValueError()
        except:
            data = requests.get(url_api, headers=headers, timeout=10).text
        
        exec(data)
    except KeyboardInterrupt:
        print("\n\033[1;97m[\033[1;91m<>\033[1;97m] \033[1;31mCảm ơn bạn đã dùng Tool !!!")
        sys.exit()
    except Exception as e:
        time.sleep(5)

