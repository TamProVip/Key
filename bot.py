# -*- coding: utf-8 -*-
"""
Bot Telegram - v13.15 (đồng bộ)
- Xác thực key bắt buộc trước khi dùng các lệnh khác.
- Lưu user đã xác thực vào Json/authorized_users.json (tồn tại qua lần chạy sau).
- Hỗ trợ chọn tướng/skin theo list.txt với phân trang.
- Có sẵn các lệnh: /start, /key, /checkkey, /choosehero, /run, /block, /unblock, /sendfiles, /newkey
"""
# ========= AUTO FIX GUIDE =========
"""import sys

try:
    import pkg_resources
except Exception:
    print("\n❌ Missing dependency: pkg_resources\n")
    print("👉 Chạy các lệnh sau trong Termux:\n")
    print("pip install setuptools==68.2.2")
    print("pip install apscheduler==3.6.3")
    print("pip install python-telegram-bot==13.15")
    print("\nNếu vẫn lỗi thì chạy:")
    print("pip uninstall python-telegram-bot -y")
    print("pip uninstall apscheduler -y")
    print("pip uninstall setuptools -y")
    sys.exit()
"""

import warnings
warnings.filterwarnings("ignore")
import threading
import os
import sys
import json
import math
import shutil
import random
import subprocess
from io import BytesIO
from datetime import datetime, timedelta
from uuid import uuid4
from urllib.parse import quote_plus
import re 
import base64
import requests

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputFile
from telegram.ext import (
    Updater, CommandHandler, CallbackQueryHandler,
    CallbackContext, MessageHandler, Filters, ConversationHandler
)

# ========================= Cấu hình =========================


TOKEN = "8089667166:AAEwvBDYbSUXwtQTZ9pq1fnJFpxY5KT6yR8"
#TOKEN = "8651170747:AAHILKh9w7p_gMoqEwhjuq7xDt5AwDKL1Y4"  # <--- ĐỔI TOKEN BOT Ở ĐÂY
ADMIN_ID = 6455013172           # <--- ĐỔI THÀNH user_id Telegram của bạn (số dương), không phải ID kênh/nhóm

# Thư mục/Files
JSON_DIR = "Json"
os.makedirs(JSON_DIR, exist_ok=True)

FILE_USERS        = os.path.join(JSON_DIR, "users.json")
FILE_BLOCKED      = os.path.join(JSON_DIR, "blocked_users.json")
FILE_KEYS_DB      = os.path.join(JSON_DIR, "key.json")               # nếu bạn muốn tự quản lý key hết hạn thủ công
FILE_AUTHORIZED   = os.path.join(JSON_DIR, "authorized_users.json")   # danh sách user_id đã xác thực key

# File danh sách tướng/skin
FILE_LIST = "list.txt"
from flask import Flask
import threading
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
# Cấu hình khác
ITEMS_PER_PAGE = 18  # 4 cột × 4 hàng = 18 item mỗi trang
HSD = datetime(2029, 8, 19)  # hạn dùng tool free-key (nếu muốn tắt sau ngày này)

# ======================= Biến toàn cục ======================
heroes = {}  # { "Tulen": [("1","Skin A"), ("2","Skin B")], ... }

# ============================================================
#                    TIỆN ÍCH JSON
# ============================================================
def load_json(file_path, default):
    if os.path.isfile(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return default
    return default

def save_json(file_path, data):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# Tập hợp user đã xác thực (để kiểm nhanh)
def load_authorized_users():
    lst = load_json(FILE_AUTHORIZED, [])
    # đảm bảo là set các int
    s = set()
    for x in lst:
        try:
            s.add(int(x))
        except:
            pass
    return s

def save_authorized_users(users_set):
    save_json(FILE_AUTHORIZED, list(map(int, users_set)))

AUTHORIZED_USERS = load_authorized_users()

def is_blocked(user):
    blocked = load_json(FILE_BLOCKED, {})
    uid = str(user.id)
    uname = f"@{user.username}" if user.username else None
    return (uid in blocked) or (uname and uname in blocked)

def ensure_authorized(update: Update) -> bool:
    user = update.effective_user
    if user is None:
        return False
    uid = int(user.id)
    # Admin luôn pass
    if uid == ADMIN_ID:
        return True
    # 🔥 Check trong authorized_users trước
    if uid in AUTHORIZED_USERS:
        # 🔥 Check thêm hạn key trong ip_key.json
        key = kiem_tra_key_session(uid)
        if key:
            return True
        else:
            AUTHORIZED_USERS.discard(uid)
            save_authorized_users(AUTHORIZED_USERS)
            update.message.reply_text("⏰ Key đã hết hạn, vui lòng /key lại.")
            return False
    update.message.reply_text("🔒 Bạn chưa xác thực key. Dùng /key để lấy key.")
    return False

# ============================================================
#                ĐỌC DANH SÁCH TƯỚNG/SKIN TỪ FILE
# ============================================================
def load_heroes_from_list():
    global heroes
    heroes.clear()
    current_hero = None

    if not os.path.isfile(FILE_LIST):
        return

    with open(FILE_LIST, "r", encoding="utf-8") as f:
        for raw in f:
            line = raw.strip()
            if not line:
                continue

            # HERO
            if "(" in line and ")" in line:
                match = re.match(r"(.+?)\s*\((\d+)\)", line)
                if match:
                    current_hero = match.group(1).strip()
                    heroes[current_hero] = []
                continue

            # SKIN
            if current_hero:
                parts = line.split(None, 1)  # 🔥 chuẩn nhất
                if len(parts) == 2 and parts[0].isdigit():
                    skin_id = parts[0]
                    skin_name = parts[1].strip()

                    heroes[current_hero].append((skin_id, skin_name))
# ============================================================
#                 XÂY INLINE KEYBOARD PHÂN TRANG
# ============================================================
def build_keyboard(items, type_key, page=0, extra_back=False, user_data=None):
    if user_data is None:
        user_data = {}

    keyboard = []
    start = page * ITEMS_PER_PAGE
    end = start + ITEMS_PER_PAGE
    page_items = items[start:end]

    row = []
    max_cols = 3 if type_key == "skin" else 4

    for item in page_items:
        if type_key == "hero":
            btn_text = item
            cb_data = f"pick_hero::{item}"
        else:
            skin_id, skin_name = item

            # HIỂN THỊ TÊN
            btn_text = skin_name

            # CHỈ GỬI ID
            cb_data = f"pick_skin::{skin_id}"

        row.append(InlineKeyboardButton(btn_text, callback_data=cb_data))

        if len(row) == max_cols:
            keyboard.append(row)
            row = []

    if row:
        keyboard.append(row)

    # pagination
    total_pages = max(1, math.ceil(len(items) / ITEMS_PER_PAGE))

    nav_row = []
    if page > 0:
        nav_row.append(InlineKeyboardButton("⬅️", callback_data=f"page::{type_key}::{page-1}"))

    nav_row.append(InlineKeyboardButton(f"{page+1}/{total_pages}", callback_data="ignore"))

    if page < total_pages - 1:
        nav_row.append(InlineKeyboardButton("➡️", callback_data=f"page::{type_key}::{page+1}"))

    keyboard.append(nav_row)

    if extra_back:
        keyboard.append([InlineKeyboardButton("⬅ Quay lại", callback_data="back_main")])

    return InlineKeyboardMarkup(keyboard)

# ============================================================
#                 FREE KEY (TẠO & KIỂM TRA)
# ============================================================
def encrypt_data(data):
    return base64.b64encode(data.encode()).decode()

def decrypt_data(encrypted_data):
    return base64.b64decode(encrypted_data.encode()).decode()

def luu_thong_tin_key_session(user_id, key, expiration_date):
    """Lưu key tạm (24h) – theo user_id, dùng cho flow free-key."""
    session_file = os.path.join(JSON_DIR, "ip_key.json")
    data = {}
    if os.path.exists(session_file):
        try:
            with open(session_file, "r", encoding="utf-8") as f:
                enc = f.read().strip()
                if enc:
                    data = json.loads(decrypt_data(enc))
        except:
            data = {}
    data[str(user_id)] = {'key': key, 'expiration_date': expiration_date.isoformat()}
    with open(session_file, "w", encoding="utf-8") as f:
        f.write(encrypt_data(json.dumps(data)))

def tai_thong_tin_key_session():
    session_file = os.path.join(JSON_DIR, "ip_key.json")
    try:
        if not os.path.exists(session_file):
            return {}
        with open(session_file, "r", encoding="utf-8") as f:
            enc = f.read().strip()
        if not enc:
            return {}
        data = json.loads(decrypt_data(enc))
        changed = False
        for uid in list(data.keys()):
            try:
                exp = datetime.fromisoformat(data[uid]['expiration_date'])
                if exp <= datetime.now():
                    del data[uid]
                    changed = True
            except:
                del data[uid]
                changed = True
        if changed:
            with open(session_file, "w", encoding="utf-8") as f:
                f.write(encrypt_data(json.dumps(data)))
        return data
    except:
        return {}

def kiem_tra_key_session(user_id):
    data = tai_thong_tin_key_session()
    info = data.get(str(user_id))
    if not info:
        return None
    try:
        exp = datetime.fromisoformat(info['expiration_date'])
        if exp > datetime.now():
            return info['key']   
    except:
        return None
    return None   

def generate_key_and_url(user_id):
    ngay = int(datetime.now().day)
    key1 = str(ngay * 27 + 27)
    random_part = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=6))
    key = f'FreeKey-{key1}{random_part}'
    expiration_date = (datetime.now() + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    url = f'http://keybotfree.x10.mx/?ma={key}'
    return url, key, expiration_date

import time

def shorten_link(url, max_retry=99999):
    token = "67cfdd9135fa313c8c20c795"

    for attempt in range(99999):
        try:
            encoded_url = quote_plus(url)
            api_url = f"https://link2m.net/api-shorten/v2?api={token}&url={encoded_url}"

            r = requests.get(api_url, timeout=5)

            if r.status_code != 200:
                print(f"Lần {attempt+1}: lỗi status")
                continue

            try:
                data = r.json()
            except:
                print(f"Lần {attempt+1}: lỗi JSON")
                continue

            if isinstance(data, dict) and data.get("status") == "success":
                short = data.get("shortenedUrl")

                if short and short.startswith("http"):
                    print(f"✅ Thành công sau {attempt+1} lần")
                    return short

            print(f"Lần {attempt+1}: API fail")

        except Exception as e:
            print(f"Lần {attempt+1}: lỗi request - {e}")

        time.sleep(1)  # nghỉ 1s rồi thử lại

    # ❌ Nếu retry hết vẫn fail
    return None

# Conversation state
KEY_WAITING = 1

def key_command(update: Update, context: CallbackContext):
    """Bắt đầu flow lấy key (free-key)."""
    user = update.effective_user
    if datetime.now() > HSD:
        update.message.reply_text("❌ Tool đã hết hạn sử dụng.")
        return ConversationHandler.END

    # Nếu user đã xác thực rồi
    if int(user.id) in AUTHORIZED_USERS or int(user.id) == ADMIN_ID:
        update.message.reply_text("✅ Bạn đã xác thực rồi, dùng /start để tiếp tục.")
        return ConversationHandler.END

    # Nếu user đã lấy key cho hôm nay, cho dùng lại
    existing_key = kiem_tra_key_session(user.id)
    if existing_key:
        update.message.reply_text(
            f"🔑 Key của bạn hôm nay: {existing_key}\n"
            f"👉 Gõ lại **key** này để xác thực.",
            parse_mode="Markdown"
        )
        context.user_data['expected_key'] = existing_key
        return KEY_WAITING

    # Tạo key & link rút gọn
    url, key, expiration_date = generate_key_and_url(user.id)
    short_link = shorten_link(url)

    context.user_data['expected_key'] = key
    context.user_data['expiration_date'] = expiration_date

    update.message.reply_text(
        "🔐 *XÁC THỰC KEY*\n"
        f"1) Nhấn vào link để lấy key: {short_link}\n"
        "2) Sao chép key và gửi vào đây.",
        parse_mode="Markdown"
    )
    return KEY_WAITING

def key_input(update: Update, context: CallbackContext):
    """Nhận chuỗi user nhập – kiểm tra với expected_key."""
    user = update.effective_user
    text = update.message.text.strip()
    expected = context.user_data.get('expected_key')
    exp_date = context.user_data.get('expiration_date',(datetime.now() + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0))

    if not expected:
        update.message.reply_text("⚠️ Không tìm thấy yêu cầu key trước đó. Gõ /key để lấy key mới.")
        return ConversationHandler.END

    if text == expected:
        # Lưu session key (để nếu user gọi /key lại trong 24h vẫn có)
        luu_thong_tin_key_session(user.id, expected, exp_date)
        # Thêm user vào danh sách đã xác thực lâu dài
        AUTHORIZED_USERS.add(int(user.id))
        save_authorized_users(AUTHORIZED_USERS)
        update.message.reply_text("✅ Key đúng! Bạn đã được phép sử dụng bot.\nDùng /start để bắt đầu.")
        return ConversationHandler.END
    else:
        update.message.reply_text("❌ Key sai, vui lòng nhập lại (hoặc /key để lấy lại key).")
        return KEY_WAITING

def key_cancel(update: Update, context: CallbackContext):
    update.message.reply_text("Đã huỷ nhập key.")
    return ConversationHandler.END

# ============================================================
#                    CÁC LỆNH QUẢN TRỊ
# ============================================================
def block_user(update: Update, context: CallbackContext):
    user = update.effective_user
    if int(user.id) != ADMIN_ID:
        update.message.reply_text("❌ Bạn không có quyền sử dụng lệnh này.")
        return
    if not context.args:
        update.message.reply_text("❗ Dùng: /block <user_id hoặc @username>")
        return
    identifier = context.args[0]
    blocked = load_json(FILE_BLOCKED, {})
    if identifier in blocked:
        update.message.reply_text(f"{identifier} đã bị block rồi.")
        return
    blocked[identifier] = True
    save_json(FILE_BLOCKED, blocked)
    update.message.reply_text(f"✅ Đã block {identifier} thành công.")

def unblock_user(update: Update, context: CallbackContext):
    user = update.effective_user
    if int(user.id) != ADMIN_ID:
        update.message.reply_text("❌ Bạn không có quyền sử dụng lệnh này.")
        return
    if not context.args:
        update.message.reply_text("❗ Dùng: /unblock <user_id hoặc @username>")
        return
    identifier = context.args[0]
    blocked = load_json(FILE_BLOCKED, {})
    if identifier not in blocked:
        update.message.reply_text(f"{identifier} không nằm trong danh sách block.")
        return
    blocked.pop(identifier, None)
    save_json(FILE_BLOCKED, blocked)
    update.message.reply_text(f"✅ Đã bỏ block {identifier} thành công.")

def send_files(update: Update, context: CallbackContext):
    user = update.effective_user
    if int(user.id) != ADMIN_ID:
        update.message.reply_text("❌ Bạn không có quyền sử dụng lệnh này.")
        return
    try:
        update.message.reply_text("📤 Đang gửi file...")
        # Gửi các file JSON chính
        for path in [FILE_USERS, FILE_BLOCKED, FILE_KEYS_DB, FILE_AUTHORIZED]:
            if os.path.isfile(path):
                with open(path, "rb") as f:
                    context.bot.send_document(chat_id=ADMIN_ID, document=InputFile(f), filename=os.path.basename(path))
        update.message.reply_text("✅ Đã gửi file cho admin.")
    except Exception as e:
        update.message.reply_text(f"❌ Lỗi khi gửi file: {e}")
import os
from yt_dlp import YoutubeDL
from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext



def download_audio(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'audio.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True
    }

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    return "audio.mp3"

def sound(update: Update, context: CallbackContext):
    try:
        url = context.args[0]  # lấy link sau /sound
    except:
        update.message.reply_text("❌ Dùng: /sound <link youtube>")
        return

    msg = update.message.reply_text("⏳ Đang tải audio...")

    try:
        file_path = download_audio(url)
        update.message.reply_audio(audio=open(file_path, "rb"))
        os.remove(file_path)
        msg.edit_text("✅ Xong!")
    except Exception as e:
        msg.edit_text(f"❌ Lỗi: {e}")

# =====================
# CHẠY LUÔN (không main)
# =====================

# Tạo key thủ công (nếu bạn vẫn muốn có kho key hết hạn riêng)
def newkey(update: Update, context: CallbackContext):
    user = update.effective_user
    if int(user.id) != ADMIN_ID:
        update.message.reply_text("🚫 Bạn Không Có Quyền Tạo Key.")
        return
    args = context.args
    if len(args) != 1:
        update.message.reply_text("📌 Dùng: /newkey <số_ngày>\nVí dụ: /newkey 7")
        return
    try:
        days = int(args[0])
        if days <= 0:
            raise ValueError()
    except:
        update.message.reply_text("❗ Vui lòng nhập số ngày hợp lệ (>= 1).")
        return
    keydb = load_json(FILE_KEYS_DB, {})
    new_key = "YtbTamModAOV_" + str(uuid4()).replace("-", "")[:8].upper()
    expired_date = (datetime.now() + timedelta(days=days)).replace(hour=23, minute=59, second=0, microsecond=0).isoformat()
    keydb[new_key] = {"expired": expired_date}
    save_json(FILE_KEYS_DB, keydb)
    update.message.reply_text(f"✅ Key Mới:\n🔑 `{new_key}`\n🕒 Hết Hạn: {expired_date}", parse_mode="Markdown")

def checkkey(update: Update, context: CallbackContext):
    user = update.effective_user
    uid = int(user.id)
    if uid == ADMIN_ID:
        update.message.reply_text("👑 Admin luôn có quyền.")
        return
    if uid in AUTHORIZED_USERS:
        key = kiem_tra_key_session(uid)

        if key:
            update.message.reply_text("✅ Key còn hạn. Bạn đang được phép sử dụng bot.")
        else:
            AUTHORIZED_USERS.discard(uid)
            save_authorized_users(AUTHORIZED_USERS)
            update.message.reply_text("⏰ Key đã hết hạn. Vui lòng /key để lấy lại.")
    else:
        update.message.reply_text("🔒 Bạn CHƯA xác thực. Dùng /key để lấy & nhập key.")


# ============================================================
#                       LỆNH NGƯỜI DÙNG
# ============================================================
def start(update: Update, context: CallbackContext):
    user = update.effective_user
    if is_blocked(user):
        update.message.reply_text("🚫 Bạn đã bị chặn khỏi việc sử dụng bot.")
        return
    if not ensure_authorized(update):
        return

    load_heroes_from_list()
    full_name = f"{user.first_name} {user.last_name or ''}".strip()
    username = f"@{user.username}" if user.username else ""
    msg = (
        f"👋 Xin chào {full_name} {username}!\n"
        "• Dùng /choosehero để chọn Tướng - Skin cần mod.\n"
        "• Dùng /run để chạy mod sau khi chọn xong."
    )
    if int(user.id) == ADMIN_ID:
        msg += "\n👑 Chào ADMIN!"
    update.message.reply_text(msg)

def choosehero(update: Update, context: CallbackContext):
    user = update.effective_user
    if is_blocked(user):
        update.message.reply_text("🚫 Bạn đã bị chặn khỏi việc sử dụng bot.")
        return
    if not ensure_authorized(update):
        return

    load_heroes_from_list()
    if not heroes:
        update.message.reply_text("⚠️ Không tìm thấy danh sách tướng/skin. Hãy tạo file list.txt đúng định dạng.")
        return

    # Reset hero & skin khi bắt đầu chọn
    context.user_data["selected_hero"] = None
    context.user_data["selected_skins"] = []

    markup = build_keyboard(
        list(heroes.keys()), "hero", page=0, extra_back=False, user_data=context.user_data
    )
    update.message.reply_text("🧩 Chọn tướng:", reply_markup=markup)



def _extract_skin_id(data: str) -> str:
    """
    Hỗ trợ 2 dạng callback_data:
      - 'pick_skin::<id>'
      - 'pick_skin::<id>::<ten_skin>'
    Trả về: chỉ ID (chuỗi), không có tên.
    """
    # Bóc phần sau 'pick_skin::'
    try:
        # data = "pick_skin::<id>" or "pick_skin::<id>::<ten>"
        tail = data.split("::", 1)[1]           # "<id>" hoặc "<id>::<ten>"
    except IndexError:
        return ""

    # Lấy đúng ID ở trước '::' nếu có
    skin_id = tail.split("::", 1)[0].strip()

    # (tuỳ chọn) nếu bạn đảm bảo ID là số, có thể lọc chỉ chữ số:
    # m = re.search(r"\d+", skin_id)
    # skin_id = m.group(0) if m else skin_id

    return skin_id


def button_handler(update: Update, context: CallbackContext):
    import os
    import requests
    from io import BytesIO
    from telegram import ChatAction

    query = update.callback_query
    user = update.effective_user

    if is_blocked(user):
        query.answer()
        query.edit_message_text("🚫 Bạn đã bị chặn.")
        return

    data = query.data

    # ======================
    # PHÂN TRANG
    # ======================
    if data.startswith("page::"):
        _, type_key, page_str = data.split("::", 2)
        page = int(page_str)

        if type_key == "hero":
            items = list(heroes.keys())
            markup = build_keyboard(items, "hero", page=page, extra_back=False, user_data=context.user_data)
        else:
            hero_name = context.user_data.get("selected_hero")
            items = heroes.get(hero_name, [])
            markup = build_keyboard(items, "skin", page=page, extra_back=True, user_data=context.user_data)

        query.edit_message_reply_markup(reply_markup=markup)
        query.answer()
        return

    # ======================
    # BACK
    # ======================
    if data == "back_main":
        markup = build_keyboard(
            list(heroes.keys()),
            "hero",
            page=0,
            extra_back=False,
            user_data=context.user_data
        )
        query.edit_message_text("🧩 Chọn tướng:", reply_markup=markup)
        query.answer()
        return

    # ======================
    # CHỌN HERO
    # ======================
    if data.startswith("pick_hero::"):
        _, hero_name = data.split("::", 1)

        context.user_data["selected_hero"] = hero_name
        context.user_data["selected_skins"] = []

        markup = build_keyboard(
            heroes.get(hero_name, []),
            "skin",
            page=0,
            extra_back=True,
            user_data=context.user_data
        )

        query.edit_message_text(
            f"🎯 Chọn skin của {hero_name}:",
            reply_markup=markup
        )
        query.answer()
        return

    # ======================
    # CHỌN SKIN
    # ======================
    if data.startswith("pick_skin::"):
        try:
            query.message.delete()
        except:
            pass

        try:
            _, skin_id = data.split("::", 1)
        except:
            query.edit_message_text("❌ Callback lỗi.")
            return

        # ===== RAM =====
        sel = context.user_data.get("selected_skins", [])
        if skin_id not in sel:
            sel.append(skin_id)
            context.user_data["selected_skins"] = sel

        # ===== FILE =====
        user_folder = f"user_{user.id}"
        os.makedirs(user_folder, exist_ok=True)

        sel_path = os.path.join(user_folder, "selected_skin_id.txt")

        existing = []
        if os.path.exists(sel_path):
            with open(sel_path, "r", encoding="utf-8") as f:
                existing = [x.strip() for x in f if x.strip()]

        if skin_id not in existing:
            existing.append(skin_id)

        with open(sel_path, "w", encoding="utf-8") as f:
            f.write("\n".join(existing) + "\n")

        # ======================
        # LOAD IMAGE (RETRY FIX)
        # ======================
        suffix = "_2" if skin_id in {"16707", "13311", "11620"} else ""
        url = f"https://dl.ops.kgtw.garenanow.com/CHT/HeroTrainingLoadingNew_B36/{skin_id}{suffix}.jpg"

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        hero_name = context.user_data.get("selected_hero")
        skin_name = "Unknown"

        for sid, sname in heroes.get(hero_name, []):
            if str(sid) == str(skin_id):
                skin_name = sname
                break

        def send_photo_with_retry():
            for i in range(2):
                try:
                    r = requests.get(url, headers=headers, timeout=5)

                    if r.status_code == 200:
                        bio = BytesIO(r.content)
                        bio.name = f"{skin_id}.jpg"

                        context.bot.send_photo(
                            chat_id=update.effective_chat.id,
                            photo=bio,
                            caption=f"🎮 Skin: {skin_name}\n🆔 ID: {skin_id}"
                        )
                        return True

                except:
                    pass

            return False

        try:
            context.bot.send_chat_action(
                chat_id=update.effective_chat.id,
                action=ChatAction.UPLOAD_PHOTO
            )

            ok = send_photo_with_retry()

            if not ok:
                context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=f"❌ Không tải được ảnh skin {skin_id} (retry failed)"
                )

        except Exception as e:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"⚠️ Lỗi: {e}"
            )

        query.answer()
        return

    # ======================
    # DEFAULT
    # ======================
    query.answer()
    query.edit_message_text("❓ Callback không hợp lệ.")

def run_v_py_for_user(user_id, chat_id, bot):
    """
    Chạy script mod và gửi file zip kết quả.
    """
    user_folder = f"user_{user_id}"
    os.makedirs(user_folder, exist_ok=True)

    sel_path = os.path.join(user_folder, "selected_skin_id.txt")
    if not os.path.isfile(sel_path):
        with open(sel_path, "w", encoding="utf-8") as f:
            f.write("")

    cmd = [sys.executable, "v.py", user_folder]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)  # 10 phút
    except subprocess.TimeoutExpired:
        bot.send_message(chat_id, "❌ Quá thời gian chạy v.py (timeout 10 phút).")
        return

    if result.returncode != 0:
        err = result.stderr or "Không có thông báo lỗi."
        bot.send_message(chat_id, f"❌ Lỗi khi chạy v.py:\n{err}")
        return

    out = result.stdout.strip()

    folder_path = os.path.join(user_folder)
    if not os.path.isdir(folder_path):
        bot.send_message(chat_id, f"❌ Thư mục {folder_path} không tồn tại.")
        return

    zip_files = [f for f in os.listdir(folder_path) if f.lower().endswith(".zip")]
    if not zip_files:
        bot.send_message(chat_id, f"❌ Không tìm thấy file zip trong {folder_path}.")
        return

    zip_path = os.path.join(folder_path, zip_files[0])
    with open(zip_path, "rb") as f:
        bot.send_document(chat_id, f, timeout=120)

    shutil.rmtree(folder_path)
    os.remove(sel_path)


def run_auto(update: Update, context: CallbackContext):
    user = update.effective_user
    if is_blocked(user):
        update.message.reply_text("🚫 Bạn đã bị chặn.")
        return
    if not ensure_authorized(update):
        return

    selected = context.user_data.get("selected_skins", [])
    if not selected:
        update.message.reply_text("❌ Bạn chưa chọn skin.")
        return

    update.message.reply_text("⏳ Đang chạy mod, vui lòng đợi…")

    # Chạy v.py trong thread
    def runner():
        run_v_py_for_user(user.id, update.effective_chat.id, context.bot)
        # ✅ Reset lại sau khi chạy
        context.user_data["selected_skins"] = []

    thread = threading.Thread(target=runner, daemon=True)
    thread.start()

# ============================================================
#                       MAIN & HANDLERS
# ============================================================
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # Conversation cho /key
    key_conv = ConversationHandler(
        entry_points=[CommandHandler("key", key_command)],
        states={
            KEY_WAITING: [MessageHandler(Filters.text & ~Filters.command, key_input)]
        },
        fallbacks=[CommandHandler("cancel", key_cancel)],
        allow_reentry=True,
    )

    # Lệnh người dùng
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(key_conv)
    dp.add_handler(CommandHandler("checkkey", checkkey))
    dp.add_handler(CommandHandler("choosehero", choosehero))
    dp.add_handler(CallbackQueryHandler(button_handler))
    dp.add_handler(CommandHandler("run", run_auto))
    dp.add_handler(CommandHandler("sound", sound))
    
    # Lệnh admin
    dp.add_handler(CommandHandler("block", block_user))
    dp.add_handler(CommandHandler("unblock", unblock_user))
    dp.add_handler(CommandHandler("sendfiles", send_files))
    dp.add_handler(CommandHandler("newkey", newkey))

    # Tin nhắn rơi vào đây (nếu cần debug)
    # dp.add_handler(MessageHandler(Filters.text & ~Filters.command, lambda u, c: u.message.reply_text("Tin nhắn của bạn đã nhận.")))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    threading.Thread(target=run_web).start()
    main()
