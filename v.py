
# https://youtube.com/@YtbTamModAOV
import os; import re; import getopt; import random; import pyzstd; from xml.dom import minidom; from colorama import Fore, Style; import sys; import shutil; import zipfile; import uuid; from collections import Counter; import xml.etree.ElementTree as ET; from collections import defaultdict; import os as O, binascii as X; from pathlib import Path; from random import randint; import datetime; import time; import struct; import hashlib; import json; import requests; import io; import glob; from pystyle import *; import builtins; import math; import copy; from Crypto.Cipher import AES; from Crypto.Util.Padding import pad, unpad

URL = "https://raw.githubusercontent.com/TamProVip/Key/main/Resources.zip"
FOLDER_NAME = "Resources"
ZIP_NAME = "Resources.zip"

def progress_bar(percent, width=40):
    filled = int(width * percent // 100)
    bar = '[' + '#' * filled + '-' * (width - filled) + ']'
    sys.stdout.write(f'\r{bar} {percent:6.2f}%')
    sys.stdout.flush()

def download_file(url, filename):
    resp = requests.get(url, stream=True)
    total = int(resp.headers.get("content-length", 0))
    downloaded = 0
    with open(filename, "wb") as f:
        for chunk in resp.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
                downloaded += len(chunk)
                percent = downloaded * 100 / total if total else 100
                progress_bar(percent)
def unzip_file(zip_path, extract_to):
    with zipfile.ZipFile(zip_path, "r") as z:
        infos = z.infolist()
        total = sum(info.file_size for info in infos)
        extracted = 0
        for info in infos:
            z.extract(info, extract_to)
            extracted += info.file_size
            percent = extracted * 100 / total if total else 100
            progress_bar(percent)

def check_resources():
    if os.path.exists(FOLDER_NAME):
        return
    print(f"[-] {FOLDER_NAME} Not Found Download Now...")
    download_file(URL, ZIP_NAME)
    print("\n[-] Doi Tool Unzip...")
    unzip_file(ZIP_NAME, ".")
    os.remove(ZIP_NAME)
check_resources()
os.system('clear')
AutoMod = __file__
TimeUpdate = os.path.getmtime(AutoMod)
TimeLine = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(TimeUpdate))
def menu_key():
    terminal_width = shutil.get_terminal_size().columns
    
    lines = [
        "Key Vip: Liên Hệ Zalo Admin",
        "Giá Key: 30 VND / Month",
        "Mua Source: 400 VND / Year"
    ]

    box_width = max(len(line) for line in lines)

    def center_line(text):
        print(text.center(terminal_width))

    def row(text):
        return f"│ {text.ljust(box_width)} │"

    center_line("╭" + "─" * (box_width + 2) + "╮")
    for line in lines:
        center_line(row(line))
    center_line("╰" + "─" * (box_width + 2) + "╯")

menu_key()

# Đọc version từ file
try:
    folders = os.listdir("Resources")
    Ver = next((f for f in folders if os.path.isdir(os.path.join("Resources", f))), "Unknown")
except:
    Ver = "Unknown"
width = shutil.get_terminal_size(fallback=(80, 20)).columns

def print_centered(line):
    text_only = line.encode('ascii', 'ignore').decode() 
    spaces = max((width - len(text_only)) // 2, 0)
    print(" " * spaces + line)

# In banner
print("╭" + "─" * (width - 2) + "╮")
print_centered("  Ytb Tâm Mod AOV")
print_centered("  Tool: Mod Skin Engine")
print_centered(f"  Version : {Ver}")
print("╰" + "─" * (width - 2) + "╯")
print()

# In thêm info
print_centered(f" {TimeLine}")
print_centered(f" Python {os.sys.version.split()[0]}")

with open("ZSTD_DICT.xml", 'rb') as f:
    ZSTD_DICT = f.read()
ZSTD_LEVEL = 1

def giai(a):
    if os.path.isdir(a):
        for root, dirs, files in os.walk(a):
            if 'imprint' in root.lower():
                continue
            for file in files:
                file_path = os.path.join(root, file)
                _giaima_file(file_path)
    else:
        if 'imprint' not in a.lower():
            _giaima_file(a)

def _giaima_file(filepath):
    try:
        if not os.path.isfile(filepath):
            return

        with open(filepath, "rb") as f:
            input_blob = f.read()

        if input_blob.startswith(b"\x22\x4a\x00\xef"):
            input_blob = input_blob[8:]

        pos = input_blob.find(b"\x28\xb5\x2f\xfd")
        if pos != -1:
            anti_pos = input_blob.rfind(b'ANTI_DECOMP__')
            if anti_pos != -1:
                input_blob = input_blob[:anti_pos]

            input_blob = input_blob[pos:]
            output_blob = pyzstd.decompress(input_blob, pyzstd.ZstdDict(ZSTD_DICT, True))

            with open(filepath, "wb") as f:
                f.write(output_blob)

    except Exception:
        pass

def key(n):
    h = 0
    for c in n.upper():
        h = (h * 31 + ord(c)) & 0xFFFFFFFF
    k = bytearray(bytes.fromhex("9964b1b06b038d7fb77db6a754908b73"))
    for i in range(16):
        k[i] ^= (h >> (8 * (i % 4))) & 0xFF
    return bytes(k)

def process_folder(p):
    files = [p] if os.path.isfile(p) else [
        os.path.join(r, f) for r, _, fs in os.walk(p)
        for f in fs if f.endswith((".bytes", ".xml", ".txt"))
    ]

    for path in files:
        name = os.path.splitext(os.path.basename(path))[0]
        try:
            d = open(path, "rb").read()
            c = AES.new(key(name), AES.MODE_CBC, b"\x00"*16)
    
            if d.startswith(b'\x22\x4a\x67'):
                out = unpad(c.decrypt(d[8:]), 16)
            else:
                ct = c.encrypt(pad(d, 16))
                hdr = (0).to_bytes(4,"little") + len(d).to_bytes(4,"little")
                out = b'\x22\x4a\x67' + hdr[3:] + ct
    
            open(path, "wb").write(out)
    
        except Exception as e:
            print("✗ Lỗi:", path, e)

def antidec(path):
    Path = []

    if os.path.isdir(path):
        for fo, foc, files in os.walk(path):
            for file in files:
                if file.endswith(('.xml', '.bytes', '.txt')):
                    Path.append(os.path.join(fo, file))
    elif os.path.isfile(path):
        Path = [path]

    for file_path in Path:
        try:
            with open(file_path, 'rb') as File:
                All_Code = File.read()

            Code = bytearray(pyzstd.compress(All_Code, 1, pyzstd.ZstdDict(ZSTD_DICT)))

            if file_path.endswith('.xml'):
                Code += b"MODBYRONAOV"
                Code += Code[int(len(Code) / 2):int(len(Code) / 2) + randint(500, 100000)]
            else:
                Code += Code[int(len(Code) / 2):int(len(Code) / 2) + randint(3, 4)]

            Code[0:0] = len(All_Code).to_bytes(4, byteorder="little")
            Code[0:0] = b"\"J\x00\xef"

            with open(file_path, 'wb') as File:
                File.write(Code)

        except Exception as e:
            pass

#print("\033[36m[III]. Chọn Chức Năng Fix Lag\n   [1].Fix Lag AssetRefs\n   [2].Fix Lag Born\n   [3].Không Fix Lag")
fixlag = '1'#input("\n>>> ")
def process_input_numbers(numbers):
    return numbers 
CAMXA = '3'#input("\n\t\033[1;97m[\033[1;92m?\033[1;97m] MOD CAM XA Y/n: ")
cyyy =  Colors.StaticMIX((Col.light_blue, Col.light_gray, Col.light_red))
Anti = input(Colorate.Diagonal(Colors.DynamicMIX((Col.red, cyyy)), ">> Antidec Để Giảm Lag (Y/N): "))
input_numbers = input(Colorate.Diagonal(Colors.DynamicMIX((Col.red, cyyy)), ">> Enter Your IDSkin: "))
numbers = [int(num) for num in input_numbers.split()]
results = process_input_numbers(numbers)
if results is None:
    sys.exit()
result_str = ' '.join(map(str, results))
IDD = result_str
IDMODSKIN = IDD.split()
IDMODSKIN1 = IDD.split()
if len(IDMODSKIN1) == 1:
    pass
    #sys.exit()

DANHSACH = IDD.split()
with open(f'Resources/{Ver}/Databin/Client/Actor/heroSkin.bytes', 'rb') as f:
    giai(f'Resources/{Ver}/Databin/Client/Actor/heroSkin.bytes')
    giai(f"Resources/{Ver}/Languages/VN_Garena_VN/languageMap_Xls.txt")
    VTR = f.read()

TenSkinList = []
for IDCC in IDMODSKIN:
    IDD1 = struct.pack("<I", int(IDCC)) + struct.pack("<I", int(str(IDCC)[:3]))
    VTCT = VTR.find(IDD1)
    ST1 = VTR[VTCT+12:VTCT+60].split(b"\x00",1)[0].decode("utf8","ignore")
    ST2 = VTR[VTCT+40:VTCT+80].split(b"\x00",1)[0].decode("utf8","ignore")
    C1 = C2 = ""
    for file in glob.glob(f"Resources/{Ver}/Languages/VN_Garena_VN/*.txt"):
        with open(file,"r",encoding="utf8",errors="ignore") as f:
            for line in f:
                if not C1 and ST1 in line and "=" in line:
                    n = line.split("=",1)[1].strip()
                    if n and not n.startswith("[ex]"):
                        C1 = n
                if not C2 and ST2 in line and "=" in line:
                    n = line.split("=",1)[1].strip()
                    if n and not n.startswith("[ex]"):
                        C2 = n
                if C1 and C2:
                    break
        if C1 and C2:
            break

    TenSkin = (C1 + " " + C2).strip()
    TenSkinList.append((TenSkin, IDCC))
if len(TenSkinList) == 1:
    FolderMod = TenSkinList[0][0]
else:
    FolderMod = f"Pack {len(TenSkinList)} Skin"
    FolderMod = input(f"Nhập Tên Pack Skin [{FolderMod}]: ") or FolderMod

if not os.path.exists(FolderMod):
    os.makedirs(FolderMod)

with open(os.path.join(FolderMod, 'SkinListMod.txt'), 'w', encoding='utf-8') as f:
    for i, (NameHero, SkinName) in enumerate(TenSkinList, 1):
        f.write(f"{i}. {NameHero} ({SkinName})\n")
directorie = f'{FolderMod}/Resources/{Ver}/AssetRefs/Hero'
os.makedirs(directorie, exist_ok=True)
base_path = f"{FolderMod}/Resources/{Ver}/Databin/Client/"
directories = ["Actor", "Shop", "Sound", "Skill", "Character", "Motion", "Global", "Huanhua"]
for directory in directories:
    os.makedirs(os.path.join(base_path, directory), exist_ok=True)
#-----------------------------------------------
file_actor = f"Resources/{Ver}/Databin/Client/Actor/heroSkin.bytes"
file_actor_mod = f"{FolderMod}/Resources/{Ver}/Databin/Client/Actor/heroSkin.bytes"
shutil.copy(file_actor, file_actor_mod)
#giai(file_actor_mod)

file_shop = f"Resources/{Ver}/Databin/Client/Shop/HeroSkinShop.bytes"
file_shop_mod = f"{FolderMod}/Resources/{Ver}/Databin/Client/Shop/HeroSkinShop.bytes"
shutil.copy(file_shop, file_shop_mod)
giai(file_shop_mod)

file_sound1 = f"Resources/{Ver}/Databin/Client/Sound/BattleBank.bytes"
file_sound_mod1 = f"{FolderMod}/Resources/{Ver}/Databin/Client/Sound/BattleBank.bytes"
shutil.copy(file_sound1, file_sound_mod1)
giai(file_sound_mod1)

file_sound2 = f"Resources/{Ver}/Databin/Client/Sound/ChatSound.bytes"
file_sound_mod2 = f"{FolderMod}/Resources/{Ver}/Databin/Client/Sound/ChatSound.bytes"
shutil.copy(file_sound2, file_sound_mod2)
giai(file_sound_mod2)

file_sound3 = f"Resources/{Ver}/Databin/Client/Sound/HeroSound.bytes"
file_sound_mod3 = f"{FolderMod}/Resources/{Ver}/Databin/Client/Sound/HeroSound.bytes"
shutil.copy(file_sound3, file_sound_mod3)
giai(file_sound_mod3)

file_sound4 = f"Resources/{Ver}/Databin/Client/Sound/LobbyBank.bytes"
file_sound_mod4 = f"{FolderMod}/Resources/{Ver}/Databin/Client/Sound/LobbyBank.bytes"
shutil.copy(file_sound4, file_sound_mod4)
giai(file_sound_mod4)

file_sound5 = f"Resources/{Ver}/Databin/Client/Sound/LobbySound.bytes"
file_sound_mod5 = f"{FolderMod}/Resources/{Ver}/Databin/Client/Sound/LobbySound.bytes"
shutil.copy(file_sound5, file_sound_mod5)
giai(file_sound_mod5)

file_sound6 = f"Resources/{Ver}/Databin/Client/Sound/CoupleSound.bytes"
file_sound_mod6 = f"{FolderMod}/Resources/{Ver}/Databin/Client/Sound/CoupleSound.bytes"
shutil.copy(file_sound6, file_sound_mod6)
giai(file_sound_mod6)

Sound_Files = f"{FolderMod}/Resources/{Ver}/Databin/Client/Sound"

file_skill1 = f"Resources/{Ver}/Databin/Client/Skill/liteBulletCfg.bytes"
file_mod_skill1 = f"{FolderMod}/Resources/{Ver}/Databin/Client/Skill/liteBulletCfg.bytes"
shutil.copy(file_skill1, file_mod_skill1)
giai(file_mod_skill1)

file_skill2 = f"Resources/{Ver}/Databin/Client/Skill/skillmark.bytes"
file_mod_skill2 = f"{FolderMod}/Resources/{Ver}/Databin/Client/Skill/skillmark.bytes"
shutil.copy(file_skill2, file_mod_skill2)
giai(file_mod_skill2)

Huanhua = f"{FolderMod}/Resources/{Ver}/Databin/Client/Huanhua/ResSkinExclusiveBattleEffectCfg.bytes"
Huanhua1 = f"Resources/{Ver}/Databin/Client/Huanhua/ResSkinExclusiveBattleEffectCfg.bytes"
shutil.copy(Huanhua1, Huanhua)
giai(Huanhua)

file_Character = f"Resources/{Ver}/Databin/Client/Character/ResCharacterComponent.bytes"
file_mod_Character = f"{FolderMod}/Resources/{Ver}/Databin/Client/Character/ResCharacterComponent.bytes"
shutil.copy(file_Character, file_mod_Character)
giai(file_mod_Character)

CodeCC = f"Resources/{Ver}/Databin/Client/Actor/ResSkinSeniorLabelCfg.bytes"
入力ファイル = f"{FolderMod}/Resources/{Ver}/Databin/Client/Actor/ResSkinSeniorLabelCfg.bytes"
shutil.copy(CodeCC, 入力ファイル)
process_folder(入力ファイル)

file_Modtion = f"Resources/{Ver}/Databin/Client/Motion/ResSkinMotionBaseCfg.bytes"
file_mod_Modtion = f"{FolderMod}/Resources/{Ver}/Databin/Client/Motion/ResSkinMotionBaseCfg.bytes"
shutil.copy(file_Modtion, file_mod_Modtion)
giai(file_mod_Modtion)

file_vien = f"Resources/{Ver}/Databin/Client/Global/HeadImage.bytes"
file_mod_vien = f"{FolderMod}/Resources/{Ver}/Databin/Client/Global/HeadImage.bytes"
shutil.copy(file_vien, file_mod_vien)
giai(file_mod_vien)

with zipfile.ZipFile(f'Resources/{Ver}/Ages/Prefab_Characters/Prefab_Hero/CommonActions.pkg.bytes') as zipf:
    zipf.extractall(f'{FolderMod}/Resources/{Ver}/Ages/Prefab_Characters/Prefab_Hero/mod1/')
#-----------------------------------------------
def Track_Guid_Skill(directory_path):
    for file in os.listdir(directory_path):
        file_path = os.path.join(directory_path, file)
        with open(file_path, "rb") as r0:
            context = r0.read()
            Tracks = re.findall(rb'<Track trackName="(.*?)</Track>', context, re.DOTALL)
            if Tracks:
                for i in range(len(Tracks)):
                    trackName = Tracks[i]
                    guid_track = (re.findall(rb'guid="(.+?)" enabled', trackName)[0]).decode()
                    guid_true = str.encode(f'id="{i}" guid="{guid_track}"')
                    IdGuidFalse = re.findall(str.encode(rf'id="(.+?)" guid="{guid_track}"'), context)
                    if IdGuidFalse:
                        for j in range(len(IdGuidFalse)):
                            j = IdGuidFalse[j].decode()
                            guid_false = str.encode(f'id="{j}" guid="{guid_track}"')
                            context = context.replace(guid_false, guid_true)
                            
        with open(file_path, "wb") as w0:
            w0.write(context)
#-----------------------------------------------
def HDSkill(ID_SKIN, path):
    ID_HD = [
        "59802", "52710", "51015", "52113", "13613", "52414", "54805",
        "15013", "13706", "13118", "11120", "19109", "10915", "59901",
        "13314", "17408", "13213", "11215", 
    ]

    for fn in os.listdir(path):
        fp = os.path.join(path, fn)
        if not os.path.isfile(fp):
            continue

        with open(fp, "rb") as f:
            data = f.read()

        parts = re.split(rb'(<Track.*?</Track>)', data, flags=re.DOTALL)
        result = b""

        for part in parts:
            if part.startswith(b"<Track") and b"</Track>" in part:
                if (b"AutoY" in part or b"tongyong_effects" in part or b'enabled="false"' in part):
                    result += part
                    continue

                def repl(m):
                    v = m[2]
                    if not v.strip():
                        return m[0]
                    if ID_SKIN in ID_HD and not v.endswith(b"_HD"):
                        v += b"_HD"
                    elif ID_SKIN not in ID_HD and not v.endswith(b".prefab"):
                        v += b".prefab"
                    return m[1] + v + m[3]

                part = re.sub(rb'(resourceName\d*"[^>]*value=")([^"]*)(")', repl, part)

            result += part

        if result != data:
            with open(fp, "wb") as f:
                f.write(result)
#-----------------------------------------------
def Function_Track_Guid_AddGetHoliday(path):
    files = os.listdir(path)
    total = len(files)

    for dem, file in enumerate(files, 1):
        file_path = os.path.join(path, file)
        with open(file_path, "rb") as r0:
            context = r0.read()
            Tracks = re.findall(rb'<Track trackName="(.*?)</Track>', context, re.DOTALL)
            if Tracks:
                for i in range(len(Tracks)):
                    trackName = Tracks[i]
                    guid_track = (re.findall(rb'guid="(.+?)" enabled', trackName)[0]).decode()
                    guid_true = str.encode(f'id="{i}" guid="{guid_track}"')
                    IdGuidFalse = re.findall(str.encode(rf'id="(.+?)" guid="{guid_track}"'), context)
                    if IdGuidFalse:
                        for j in range(len(IdGuidFalse)):
                            j = IdGuidFalse[j].decode()
                            guid_false = str.encode(f'id="{j}" guid="{guid_track}"')
                            context = context.replace(guid_false, guid_true)
        with open(file_path, "wb") as w0:
            w0.write(context)

        bar_length = 30
        filled = int(bar_length * dem / total)
        bar = "#" * filled + "-" * (bar_length - filled)
        sys.stdout.write(f"\r    [{bar}] {dem}/{total}")
        sys.stdout.flush()
    time.sleep(0.5)
    sys.stdout.write("\r" + " " * (bar_length + 20) + "\r")
    sys.stdout.flush()
#-----------------------------------------------
class StringBytes:
    def __init__(self,String):
        self.String=String
        self.OldString=String
    def tell(self):
        return len(self.OldString)-len(self.String)
    def seek(self,I,O=0):
        if O==0:
            self.String=self.OldString[I:]
        elif O==1:
            self.String=self.String[I:]
    def read(self,Int=None):
        if Int==None:
            if type(self.String)==str:
                return ""
            else:
                return b""
        R=self.String[:Int]
        self.String=self.String[Int:]
        return R
class Bytes_XML:
    def decode(String):
        def get_int(A):
            return int.from_bytes(A.read(4), 'little')        
        def get_str(A, pos=None):
            if pos is not None:
                A.seek(pos, 0)
            ofs = get_int(A)
            stri = A.read(ofs-4)
            return stri.decode()        
        def get_node(A, fid=None, sta=None):
            global i
            ofs = get_int(A)
            stri = get_str(A)
            stri1 = stri
            myid = i
            i += 1
            A.seek(4, 1)
            aidx = get_int(A)
            ite = False
            attr = {}
            for j in range(0, aidx):
                attr1 = get_attr(A)
                if type(attr1) == str:
                    text1 = attr1
                    ite = True
                else:
                    attr.update(attr1)
            if fid is None:
                nod[myid] = ET.SubElement(root, stri1, attrib=attr)
            else:
                nod[myid] = ET.SubElement(nod[fid], stri1, attrib=attr)
            if ite:
                if text1 == '':
                    nod[myid].set("value",' ')
                else:
                    nod[myid].set("value",text1)
            check_four(A)
            chk = sta + ofs - A.tell()
            if chk > 12:
                A.seek(4, 1)
                sidx = get_int(A)
                for h in range(0, sidx):
                    get_node(A, myid, A.tell())
            A.seek(sta + ofs, 0)        
        def get_attr(A, pos=None):
            if pos is None:
                pos = A.tell()
            ofs = get_int(A)
            type = get_int(A)
            if type == 5:
                stri = A.read(ofs - 8).decode()[1:]
                check_four(A)
                A.seek(pos + ofs, 0)
                return stri
            else:
                if type == 6:
                    stri = A.read(ofs - 8).decode()
                    if stri[0:2] == 'JT':
                        if stri == 'JTArr':
                            stri = 'Array'
                        elif stri == 'JTPri':
                            stri = 'String'
                        else:
                            stri = stri[2:]
                        name = 'var'
                    else:
                        name = 'var_Raw'
                elif type == 8:
                    stri2 = A.read(ofs - 8).decode()
                    if stri2[0:4] == 'Type':
                        stri = stri2[4:]
                        name = 'type'
                    else:
                        stri = stri2
                        name = 'type_Raw'
                else:
                    stri = A.read(ofs - 8).decode()
                    name = str(type)
                    A.seek(pos + ofs, 0)
                return {name:stri}
        def check_four(A):
            if get_int(A) != 4:
                A.seek(-4, 1)
        A=StringBytes(String)
        global i, nod, root
        i = 0
        nod = {}
        ofs = get_int(A)
        stri = get_str(A)
        stri1 = stri
        A.seek(4, 1)
        aidx = get_int(A)
        ite = False
        attr = {}
        for j in range(0, aidx):
            attr1 = get_attr(A)
            if type(attr1) == str:
                text1 = attr1
                ite = True
            else:
                attr.update(attr1)
        root = ET.Element(stri1, attrib=attr)
        if ite:
            nod[myid].set("value",text1)
        check_four(A)
        chk = ofs - A.tell()
        if chk > 12:
            A.seek(4, 1)
            sidx = get_int(A)
            for h in range(0, sidx):
                get_node(A, None, A.tell())
        try:return minidom.parseString(ET.tostring(root,"utf-8").decode()).toprettyxml(indent="  ",newl="\r\n").encode()
        except: return ET.tostring(root,"utf-8").decode()
    def encode(xmlfile):
        def byteint(num):
            return num.to_bytes(4, byteorder='little')
        def bytestr(stri):
            outbyte = byteint(len(stri) + 4)
            outbyte = outbyte + stri.encode()
            return outbyte
        def byteattr(key, attr):
            if key == 'var':
                if attr[key] == 'Array':
                    stri = 'JTArr'
                elif attr[key] == 'String':
                    stri = 'JTPri'
                else:
                    stri = 'JT' + attr[key]
                aid = 6
            elif key == 'var_Raw':
                stri = attr[key]
                aid = 6
            elif key == 'type':
                stri = 'Type' + attr[key]
                aid = 8
            elif key == 'type_Raw':
                stri = attr[key]
                aid = 8
            elif key == "value": return b""
            else:
                import unicodedata
                if unicodedata.numeric(key):
                    stri = attr[key]
                    aid = int(key)
            stripro = stri.encode()
            outbyte = byteint(len(stripro) + 8) + byteint(aid) + stripro
            return outbyte
        def bytenode(node):
            iftex = False
            name1 = node.tag
            name = bytestr(name1)
            attr1 = b''
            aindex = len(node.attrib)
            plus = 8
            for key in node.attrib:
                if key=="value":aindex-=1
                attr1 = attr1 + byteattr(key, node.attrib)
            if (node.get("value") != None) and (node.get("value")[0:1] != '\n'):
                if node.get("value") == ' ':
                    stri1 = ''
                else:
                    stri1 = node.get("value")
                iftex = True
                stripro = ('V' + stri1).encode()
                attr1 = attr1 + byteint(len(stripro) + 8) + byteint(5) + stripro + byteint(4)
                aindex += 1
                plus = 4
            attr1 = byteint(len(attr1) + plus) + byteint(aindex) + attr1 + byteint(4)
            alchild = b''
            if len(node):
                cindex = 0
                for child in node:
                    alchild = alchild + bytenode(child)
                    cindex += 1
                alchild = byteint(len(alchild) + 8) + byteint(cindex) + alchild
            else:
                if iftex == False:
                    alchild = byteint(4)
            bnode = name + attr1 + alchild
            bnode = byteint(len(bnode) + 4) + bnode
            return bnode
        tree = ET.fromstring(xmlfile)
        byt = bytenode(tree)
        return byt
                          
def process_file(file_path_FL, LC):
    with open(file_path_FL, "rb") as f:
        G = f.read()
        with open(file_path_FL, "wb") as f1:
            try:
                if LC == "1":
                    f1.write(Bytes_XML.decode(G))
                elif LC == "2":
                    f1.write(Bytes_XML.encode(G.decode()))
            except Exception as e:
                pass
        
def process_directory(directory_path, LC):
    file_path_FL = directory_path
    process_file(file_path_FL, LC) 
#-----------------------------------------------
def hex_to_dec(a):
    len(a)
    a=a[::-1]
    a=a.hex()
    a=int(a,16)
    return a
def dec_to_hex(a):
    a=hex(a)[2:]
    if len(a)%2==1:
        a='0'+a
    return (bytes.fromhex(a))[::-1]
def decompress_(strin,ZSTD_DICT=ZSTD_DICT):
    posdecompress = strin.find(b"\x28\xb5\x2f\xfd")
    if posdecompress != -1:
        strin = strin[posdecompress:]
        strin = strin[strin.find(b"\x28\xb5\x2f\xfd"):]
        strin = pyzstd.decompress(strin, pyzstd.ZstdDict(ZSTD_DICT, True))
    return strin

original_locations = {}

def move_skin_action_out(Files_Directory_Path, target_name="skinaction"):
    """
    Tìm skinaction trong Files_Directory_Path
    và đưa nó ra cùng cấp với file .py
    """
    script_root = os.path.dirname(os.path.abspath(__file__))

    for current_root, dirs, files in os.walk(Files_Directory_Path):
        if target_name in dirs:
            skin_path = os.path.join(current_root, target_name)
            new_path = os.path.join(script_root, target_name)

            original_locations[target_name] = skin_path

            if not os.path.exists(new_path):
                shutil.move(skin_path, new_path)
                #shutil.rmtree(skin_path)
            else:
                pass

            return 

def move_skin_action_back(Files_Directory_Path=None, target_name="skinaction"):
    """
    Đưa skinaction về vị trí cũ
    Files_Directory_Path không cần dùng lại
    """
    if target_name not in original_locations:
        return

    script_root = os.path.dirname(os.path.abspath(__file__))
    current_path = os.path.join(script_root, target_name)
    original_path = original_locations[target_name]

    if os.path.exists(current_path):
        shutil.move(current_path, original_path)
#-----------------------------------------------
for IDMODSKIN in IDMODSKIN1:
    NameHero = None
    for TenSkin, SkinID in TenSkinList:
        if SkinID == IDMODSKIN:
            NameHero = TenSkin
            break
    if NameHero:
        print('-' * 53)
        print(f"{NameHero:^53}")
        print('-' * 53)
    fileasset = f'Resources/{Ver}/AssetRefs/Hero/{IDMODSKIN[:3]}_AssetRef.bytes'
    fileasset_mod2 = f'{FolderMod}/Resources/{Ver}/AssetRefs/Hero/{IDMODSKIN[:3]}_AssetRef.bytes'
    os.makedirs(os.path.dirname(fileasset_mod2), exist_ok=True)
    shutil.copy(fileasset, fileasset_mod2)
    SKINEOV = ''
    if IDMODSKIN == '13311':
        SKINEOV = "r"
    if IDMODSKIN == '16707':
        SKINEOV = "b"
    if IDMODSKIN == '15412':
        SKINEOV = "y"
    if IDMODSKIN == '51015':
        SKINEOV = "l"
    
    nhap_id = IDMODSKIN
    IDCODE = IDMODSKIN
    IDCHECK = IDMODSKIN
    skinid = IDMODSKIN.encode()
    IDSOUND_S = IDMODSKIN
    phukien = ''
    phukienb = ''
    phukienv = ''
    IDINFO=int(IDMODSKIN)+1
    IDINFO=str(IDINFO)
    if str(IDINFO)[3:4] == '0':
        IDINFO=IDINFO[:3]+IDINFO[4:]
    IDINFO=str(IDINFO)
    if IDSOUND_S[3:4] == '0':
        IDSOUND_S=IDSOUND_S[:3]+IDSOUND_S[4:]
    IDSOUND1=IDSOUND_S[3:]
    IDSOUND12=IDSOUND1.encode()
    IDSOUND = b"_Skin" + IDSOUND12
    #if IDCHECK == '52007':
        #phukien1 = input(
            #'\033[1;97m[\033[1;91m?\033[1;97m] Mod Component:\n'
            #'\033[1;97m [1] \033[1;92mBlue\n'
            #'\033[1;97m [2] \033[1;92mRed\n'
            #'\033[1;97m [3] \033[1;92mNo Mod Component\n'
            #'\033[1;97m[•] INPUT: ')
        #if phukien1 == "1":
            #phukien = 'xanh'
        #if phukien1 == "2":
            #phukien = 'do'
    #if IDCHECK == '13311':
        #phukien1v = input(
            #'\033[1;97m[\033[1;91m?\033[1;97m] Mod Component:\n'
            #'\033[1;97m [1] \033[1;92mGreen\n'
            #'\033[1;97m [2] \033[1;92mRed\n'
            #'\033[1;97m [3] \033[1;92mNo Mod Component\n'
            #'\033[1;97m[•] INPUT: ')
        #if phukien1v == "1":
            #phukienv = 'vangv'
        #if phukien1v == "2":
            #phukienv = 'dov'
    if IDCHECK == '11620':
        phukien12 = '1'
        if phukien12 == "1":
            phukienb = 'tim'
        if phukien12 == "2":
            phukienb = 'do'
    if IDCHECK in ["16707", "11620", "13311"]:
        def B2Js(blocks_data):
            offset = 140
            blocks = []
            
            def S():
                nonlocal offset
                value = struct.unpack_from("<I", blocks_data, offset)[0]
                offset += 4
                return value
        
            def B1():
                nonlocal offset
                value = struct.unpack_from("<B", blocks_data, offset)[0]
                offset += 1
                return value
            def B2():
                nonlocal offset
                value = struct.unpack_from("<B", blocks_data, offset)[0] == 1
                offset += 1
                return value
        
            def Str():
                nonlocal offset
                length = struct.unpack_from("<I", blocks_data, offset)[0]
                offset += 4
                value = blocks_data[offset : offset + length].decode("utf-8").strip("\x00")
                offset += length
                return value
        
            while offset < len(blocks_data):
                block = {}
                try:
                    blockinfo = S()
                    block['ID'] = S()
                    block['HeroID'] = S()
                    block['HeroName'] = Str()
                    block['SkinID'] = S()
                    block['SkinName'] = Str()
                    block['SkinDesc'] = Str()
                    block['bIsLimitSkin'] = B2()
                    block['LimitQualityPic'] = Str()
                    block['LimitLabelPic'] = Str()
                    block['LimitLabelPicUrl'] = Str()
                    block['bSkinQuality'] = B1()
                    block['bGetPathType'] = B1()
                    block['GetPath'] = Str()
                    
                    block['bIsBuyCoupons'] = B2()
                    block['BuyCoupons'] = S()
                    
                    block['bIsBuySkinCoin'] = B2()
                    block['BuySkinCoin'] = S()
                    
                    block['bIsBuyDiamond'] = B2()
                    block['BuyDiamond'] = S()
                    
                    block['bIsBuyMixPay'] = B2()
                    block['bIsBuyItem'] = B2()
                    block['BuyItemCnt'] = S()
                    
                    block['bIsPresent'] = B2()
                    block['SortId'] = S()
                    
                    block['bPromotionCnt'] = B1()
                    block['PromotionID'] = []
                    for i in range(1, 6):
                        idp = S()
                        if idp:
                            block['PromotionID'].append(idp)
        
                    block['ChgItemCnt'] = S()
        
                    block['OnTimeStr'] = Str()
                    block['OffTimeStr'] = Str()
        
                    block['OnTimeGen'] = S()
                    block['OffTimeGen'] = S()
                    block['ReleaseId'] = S()
                    
                    block['bShowInShop'] = B2()
                    block['bShowInMgr'] = B2()
                    block['bRankLimitType'] = B1()
                    block['bExchangeCoinType'] = B1()
                    block['bRankLimitGrade'] = B1()
                    
                    block['ExchangeCoinCnt'] = S()
                    
                    offset += 34
        
                    
                    block['ConnectionGift'] = S()
                    block['SkinLevel'] = S()
                    
                    block['bIsDefaultT6'] = B2()
                    block['VideoAddress'] = Str()
                    block['bIsWorldConceptVideo'] = B2()
                    
                    block['ShareSkinGroupID'] = S()
                    block['VipShareSkinGroupID'] = S()
                    blocks.append(block)
                except ValueError as e:
                    print(f"Error reading block at offset {offset}: {e}")
                    break
        
            return json.dumps(blocks, indent=4)
        
        
        import hashlib
        
        
        def JstoB(json_data, binary_file):
            blocks = json.loads(json_data)
            binary_data = bytearray()
            header = bytearray()
            header.extend(b'MSES\x07\x00\x00\x00')
            Blast = 0
            total_blocks = len(blocks)
            header.extend(struct.pack("<I", Blast))
            header.extend(struct.pack("<I", total_blocks))
            header.extend(b'\x61' * 32)
            header.extend(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00UTF-8\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
            header.extend(b'\x00' * (140 - len(header)))
            binary_data.extend(header)
        
            def U(fmt, value):
                nonlocal block_data
                block_data.extend(struct.pack(fmt, value))
            
            def S1(value):
                nonlocal block_data
                block_data.extend(pack_string(value))
        
            for block in blocks:
                block_data = bytearray()
        
                U("<I", block.get('ID', 0))
                U("<I", block.get('HeroID', 0))
                S1(block.get('HeroName', ""))
                U("<I", block.get('SkinID', 0))
                S1(block.get('SkinName', ""))
                S1(block.get('SkinDesc', ""))
                block_data.append(1 if block.get('bIsLimitSkin', False) else 0)
                S1(block.get('LimitQualityPic', ""))
                S1(block.get('LimitLabelPic', ""))
                S1(block.get('LimitLabelPicUrl', ""))
                block_data.append(block.get('bSkinQuality', 0))
                block_data.append(block.get('bGetPathType', 0))
                S1(block.get('GetPath', ""))
                
                block_data.append(1 if block.get('bIsBuyCoupons', False) else 0)
                U("<I", block.get('BuyCoupons', 0))
                
                block_data.append(1 if block.get('bIsBuySkinCoin', False) else 0)
                U("<I", block.get('BuySkinCoin', 0))
                
                block_data.append(1 if block.get('bIsBuyDiamond', False) else 0)
                U("<I", block.get('BuyDiamond', 0))
                
                block_data.append(1 if block.get('bIsBuyMixPay', False) else 0)
                block_data.append(1 if block.get('bIsBuyItem', False) else 0)
                U("<I", block.get('BuyItemCnt', 0))
                
        
                
                block_data.append(1 if block.get('bIsPresent', False) else 0)
                U("<I", block.get('SortId', 0))
                block_data.append(block.get('bPromotionCnt', 0))
                promotion_ids = block.get("PromotionID", [])
                promotion_ids.extend([0] * (5 - len(promotion_ids)))
                for idp in promotion_ids[:5]:
                    U("<I", idp)
        
                block["PromotionID"] = promotion_ids
        
                U("<I", block.get('ChgItemCnt', 0))
                S1(block.get('OnTimeStr', ""))
                S1(block.get('OffTimeStr', ""))
                
                U("<I", block.get('OnTimeGen', 0))
                U("<I", block.get('OffTimeGen', 0))
                U("<I", block.get('ReleaseId', 0))
                
                block_data.append(1 if block.get('bShowInShop', False) else 0)
                block_data.append(1 if block.get('bShowInMgr', False) else 0)
                block_data.append(block.get('bRankLimitType', 0))
                block_data.append(block.get('bExchangeCoinType', 0))
                block_data.append(block.get('bRankLimitGrade', 0))
                
                U("<I", block.get('ExchangeCoinCnt', 0))
        
                block_data.extend(b'\x00\x01' + b'\x00' * 32)
                
                U("<I", block.get('ConnectionGift', 0))
                U("<I", block.get('SkinLevel', 0))
                block_data.append(1 if block.get('bIsDefaultT6', False) else 0)
                S1(block.get('VideoAddress', ""))
                block_data.append(1 if block.get('bIsWorldConceptVideo', False) else 0)
                U("<I", block.get('ShareSkinGroupID', 0))
                U("<I", block.get('VipShareSkinGroupID', 0))
        
                Blen = len(block_data)
                final_block = struct.pack("<I", Blen) + block_data
                binary_data.extend(final_block)
                Bflast = Blen
         
        
            Blast = Bflast + 4
            binary_data[8:12] = struct.pack("<I", Blast)
            md5_hash = hashlib.md5(binary_data[140:]).hexdigest().encode('utf-8')
            binary_data[96:96 + len(md5_hash)] = md5_hash
            binary_data[140 - 12:140] = b'\x00\x00\x00\x00\x8c\x00\x00\x00\x00\x00\x00\x00'
        
            with open(binary_file, "wb") as bf:
                bf.write(binary_data)
        
        
        def pack_string(value):
            encoded = value.encode('utf-8') + b'\x00'
            length = len(encoded)
            return struct.pack("<I", length) + encoded
        
        
        
        def process_file_bg(filename, mode):
            directory = os.path.dirname(filename)
            basename = os.path.basename(filename)
            
            if mode == 1:
                # bytes -> json
                with open(file_shop_mod, "rb") as f:
                    json_data = B2Js(f.read())
                output_path = os.path.join(directory, "HeroSkinShop.bytes")
                with open(output_path, "w", encoding="utf-8") as json_file:
                    json_file.write(json_data)
            
            elif mode == 2:
                # json -> bytes
                with open(filename, "r", encoding="utf-8") as json_file:
                    json_data = json_file.read()
                output_path = os.path.join(directory, "HeroSkinShop.bytes")
                JstoB(json_data, output_path)
            else:
                print("Mode không hợp lệ! Chỉ dùng 1 (bytes->json) hoặc 2 (json->bytes).")
        process_file_bg(file_shop_mod, 1)
        with open(file_shop_mod, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        code = next((x for x in data if str(x.get("ID")) == IDCODE), None)
        
        if code:
            if IDCODE in ["13311",'16707','11620']:
                code["LimitLabelPicUrl"] = "Awake_Label_5.png"
        
        with open(file_shop_mod, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        process_file_bg(file_shop_mod, 2)



        def B2Js(file_actor_mod):
        
            with open(file_actor_mod, "rb") as f:
                data = f.read()
        
            pos = 140
            size = len(data)
        
            blocks = []
            
            while pos + 4 <= size:
        
                block_len = struct.unpack_from("<I", data, pos)[0]
                pos += 4
        
                blocks_data = data[pos:pos + block_len]
                pos += block_len
                
                offset = 0
        
                def S():
                    nonlocal offset
                    v = struct.unpack_from("<I", blocks_data, offset)[0]
                    offset += 4
                    return v
        
                def B1():
                    nonlocal offset
                    v = struct.unpack_from("<B", blocks_data, offset)[0]
                    offset += 1
                    return v
        
                def Str():
                    nonlocal offset
                    length = struct.unpack_from("<I", blocks_data, offset)[0]
                    offset += 4
                    value = blocks_data[offset: offset + length].decode("utf-8", errors="ignore").rstrip('\x00')
                    offset += length
                    return value
        
                block = {}
        
                block['ID'] = S()
                block['HeroID'] = S()
                block['HeroName'] = Str()
        
                block['SkinID'] = S()
                block['SkinName'] = Str()
                block['SkinPicID'] = Str()
        
                block['BaseCfgID'] = S()
                block['CombatAbility'] = S()
                
                block['None'] = any(blocks_data[offset:offset + 105]) != 0
                offset += 105
        
                block['GetGoldGain'] = S()
                block['GetGoldUpperLimitGain'] = S()
                block['PresentHeadImg'] = S()
        
                block['HeroSkinShareUrl'] = Str()
                block['SettleShareUrl'] = Str()
                block['WinRateShareUrl'] = Str()
                block['SkinShowUrl'] = Str()
        
                feature_count = S()
        
                block['SkinFeature'] = []
        
                for i in range(10):
                    icon = Str()
                    name = Str()
        
                    if icon or name:
                        block['SkinFeature'].append({
                            "Icon": icon,
                            "Name": name
                        })
        
                block['SkinBgAndTable'] = Str()
                block['VideoWeb'] = Str()
                block['VideoCover'] = Str()
                block['LoadingProjectBox'] = Str()
        
                block['CoinMultiple'] = S()
                block['CoinMultipleLimit'] = S()
        
                block['HeroSelectBuySkinBgColor'] = Str()
                block['HeroLabel'] = Str()
                block['HeroLabelColor'] = Str()
                block['HeroLabelDesc'] = Str()
        
                flags = struct.unpack_from("<5B", blocks_data, offset)
                offset += 5
        
                block['bHideUI'] = flags[0]
                block['bDisableRot'] = flags[1]
                block['bDisableBloom'] = flags[2]
                block['bDisableDirLight'] = flags[3]
                block['bScaleCamera'] = flags[4]
        
                block['IsRecommendAIUsed'] = S()
                block['bEnableComponentLight'] = B1()
                block['iPresentSkinMotion'] = S()
        
                block['bIsDLC'] = B1()
                block['bIsInAB'] = B1()
        
                block['DLCWeight'] = S()
                block['Rarity'] = S()
                block['Level'] = S()
                block['Series'] = S()
        
                block['SkinPicCDNPath'] = Str()
                block['SkinHeadCDNPath'] = Str()
                block['TalePageCDNPath'] = Str()
        
                block['SkinDynamicPath'] = B1()
                block['bIsHeroSkinShareTextOnRight'] = B1()
        
                block['HeroVoiceActor'] = Str()
        
                block['bUseDefaultBackground'] = B1()
                block['iSkinThemeID'] = S()
        
                block['SkinThemeName'] = Str()
                block['HomePageSkinBgAndTable'] = Str()
                block['ImprintAge'] = Str()
                block['ReturnExtarJson'] = Str()
        
                block['bRotation'] = S()
                block['bUseRecordDir'] = S()
        
                offset += 4
        
                block['bFilterInTeam'] = S()
                block['diffTeamHeroID'] = S()
        
                blocks.append(block)
        
            return json.dumps(blocks, ensure_ascii=False, indent=4)
            
        def JstoB(json_data, binary_file):
            blocks = json.loads(json_data)
            binary_data = bytearray()
            header = bytearray()
            header.extend(b'MSES\x07\x00\x00\x00')
            Blast = 0
            total_blocks = len(blocks)
            header.extend(struct.pack("<I", Blast))
            header.extend(struct.pack("<I", total_blocks))
            header.extend(b'\x61' * 32)
            header.extend(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00UTF-8\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
            header.extend(b'\x00' * (140 - len(header)))
            binary_data.extend(header)
        
            def U(fmt, value):
                nonlocal block_data
                block_data.extend(struct.pack(fmt, value))
            
            def S1(value):
                nonlocal block_data
                block_data.extend(pack_string(value))
        
            for block in blocks:
                block_data = bytearray()
        
                U("<I", block.get('ID', 0))
                U("<I", block.get('HeroID', 0))
                S1(block.get('HeroName', ""))
                U("<I", block.get('SkinID', 0))
                S1(block.get('SkinName', ""))
                S1(block.get('SkinPicID', ""))
                U("<I", block.get('BaseCfgID', 0))
                U("<I", block.get('CombatAbility', 0))
        
                has_data = b'\x01' if block.get('None', False) else b'\x00'
                
                if has_data == b'\x01':
                    block_data.extend(b'\x01\x00\x00\x0A\x00\x00\x00\x00' + b'\x00' * 97)
                else:
                    block_data.extend(b'\x00' * 105)
        
                U("<I", block.get('GetGoldGain', 0))
                U("<I", block.get('GetGoldUpperLimitGain', 0))
                U("<I", block.get('PresentHeadImg', 0))
                S1(block.get('HeroSkinShareUrl', ""))
                S1(block.get('SettleShareUrl', ""))
                S1(block.get('WinRateShareUrl', ""))
                S1(block.get('SkinShowUrl', ""))
                features = block.get("SkinFeature", [])
                U("<I", len(features))
                for i in range(10):
                    if i < len(features):
                        S1(features[i].get("Icon", ""))
                        S1(features[i].get("Name", ""))
                    else:
                        S1("")
                        S1("")
                S1(block.get('SkinBgAndTable', ""))
                S1(block.get('VideoWeb', ""))
                S1(block.get('VideoCover', ""))
                S1(block.get('LoadingProjectBox', ""))
                U("<I", block.get('CoinMultiple', 0))
                U("<I", block.get('CoinMultipleLimit', 0))
                S1(block.get('HeroSelectBuySkinBgColor', ""))
                S1(block.get('HeroLabel', ""))
                S1(block.get('HeroLabelColor', ""))
                S1(block.get('HeroLabelDesc', ""))
                flags = [
                    1 if block.get('bHideUI', False) else 0,
                    1 if block.get('bDisableRot', False) else 0,
                    1 if block.get('bDisableBloom', False) else 0,
                    1 if block.get('bDisableDirLight', False) else 0,
                ]
                block_data.extend(struct.pack("<4B", *flags))
                bScaleCamera = block.get('bScaleCamera', 0)
                block_data.append(bScaleCamera)
        
                U("<I", block.get('IsRecommendAIUsed', 0))
                block_data.append(1 if block.get('bEnableComponentLight', False) else 0)
                U("<I", block.get('iPresentSkinMotion', 0))
                block_data.append(block.get('bIsDLC', 0))
                block_data.append(1 if block.get('bIsInAB', False) else 0)
                U("<I", block.get('DLCWeight', 0))
                U("<I", block.get('Rarity', 0))
                U("<I", block.get('Level', 0))
                U("<I", block.get('Series', 0))
                S1(block.get('SkinPicCDNPath', ""))
                S1(block.get('SkinHeadCDNPath', ""))
                S1(block.get('TalePageCDNPath', ""))
                block_data.append(block.get('SkinDynamicPath', 0))
                block_data.append(1 if block.get('bIsHeroSkinShareTextOnRight', False) else 0)
                S1(block.get('HeroVoiceActor', ""))
                block_data.append(1 if block.get('bUseDefaultBackground', False) else 0)
                U("<I", block.get('iSkinThemeID', 0))
                S1(block.get('SkinThemeName', ""))
                S1(block.get('HomePageSkinBgAndTable', ""))
                S1(block.get('ImprintAge', ""))
                S1(block.get('ReturnExtarJson', ""))
                U("<I", block.get('bRotation', 0))
                U("<I", block.get('bUseRecordDir', 0))
                block_data.extend(b'\x00'*4)
                U("<I", block.get('bFilterInTeam', 0))
                
                U("<I", block.get('diffTeamHeroID', 0))
                
                Blen = len(block_data)
                final_block = struct.pack("<I", Blen) + block_data
                binary_data.extend(final_block)
                Bflast = Blen
         
        
            Blast = Bflast + 4
            binary_data[8:12] = struct.pack("<I", Blast)
            md5_hash = hashlib.md5(binary_data[140:]).hexdigest().encode('utf-8')
            binary_data[96:96 + len(md5_hash)] = md5_hash
            binary_data[140 - 12:140] = b'\x00\x00\x00\x00\x8c\x00\x00\x00\x00\x00\x00\x00'
        
            with open(binary_file, "wb") as bf:
                bf.write(binary_data)
        
        
        def pack_string(value):
            encoded = value.encode('utf-8') + b'\x00'
            length = len(encoded)
            return struct.pack("<I", length) + encoded
    
    
        def process_file_actor(filename, mode):
            directory = os.path.dirname(filename)
        
            if mode == 1:
                # bytes -> json
                json_data = B2Js(filename)
        
                output_path = os.path.join(directory, "heroSkin.bytes")
                with open(output_path, "w", encoding="utf-8") as json_file:
                    json_file.write(json_data)
        
            elif mode == 2:
                # json -> bytes
                with open(filename, "r", encoding="utf-8") as json_file:
                    json_data = json_file.read()
        
                output_path = os.path.join(directory, "heroSkin.bytes")
                JstoB(json_data, output_path)
        
            else:
                print("Mode không hợp lệ! Chỉ dùng 1 hoặc 2.")
        process_file_actor(file_actor_mod, 1)
        with open(file_actor_mod, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        code = next((x for x in data if str(x.get("ID")) == IDCODE), None)
        
        if code:
            if IDCODE in ['16707']:
                code["SkinPicID"] = "301677_2"
                code["HeroSkinShareUrl"] = "Share_16707_2.jpg"
                code["SettleShareUrl"] = "Share_16707_2.jpg"
                code["WinRateShareUrl"] = "Share_16707_2.jpg"
                code["SkinShowUrl"] = "16707_2.jpg"
                code["SkinBgAndTable"] = "BG_wukongjuexing2/BG_wukongjuexing2_Platform"
                code["SkinPicCDNPath"] = "301677_2.jpg"
                code["SkinHeadCDNPath"] = "301677_2head.jpg"
            if IDCODE in ['13311']:
                code["SkinPicID"] = "3013311_2"
                code["HeroSkinShareUrl"] = "Share_13311_2.jpg"
                code["SettleShareUrl"] = "Share_13311_2.jpg"
                code["WinRateShareUrl"] = "Share_13311_2.jpg"
                code["SkinShowUrl"] = "13311_2.jpg"
                code["SkinBgAndTable"] = "BG_DiRenJie_13312_T3/BG_yinyingzhishou_01_platform"
                code["SkinPicCDNPath"] = "3013311_2.jpg"
                code["SkinHeadCDNPath"] = "3013311_2head.jpg"
            if IDCODE in ['11620']:
                code["SkinPicID"] = "3011620_1"
                code["HeroSkinShareUrl"] = "Share_11620_2.jpg"
                code["SettleShareUrl"] = "Share_11620_2.jpg"
                code["WinRateShareUrl"] = "Share_11620_2.jpg"
                code["SkinShowUrl"] = "11620_2.jpg"
                code["SkinBgAndTable"] = "BG_DaoFengJiNiang_11621/BG_yinyingzhishou_01_platform"
                code["SkinPicCDNPath"] = "3011620_2.jpg"
                code["SkinHeadCDNPath"] = "3011620_2head.jpg"
        with open(file_actor_mod, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        process_file_actor(file_actor_mod, 2)

            
    

    if IDCHECK in IDCHECK:
        ID = IDCHECK
        Show = 'y'
        IDB = int(ID).to_bytes(4, byteorder="little")
        IDH = int(ID[0:3]).to_bytes(4, byteorder="little")
        Files = [file_actor_mod, file_shop_mod]
        for File in Files:
            All = []
            Skin = ""
            file = open(File, "rb")
            Code = file.read()
            Find= -10
            while True:
                Find = Code.find(b"\x00\x00"+IDH, Find+10)
                if Find == -1: break
                elif str(int.from_bytes(Code[Find-2:Find], byteorder="little"))[0:3] == ID[0:3]:
                    VT2 = int.from_bytes(Code[Find-6:Find-4], byteorder="little")
                    Code2 = Code[Find-6:Find-6+VT2]
                    All.append(Code2)
                    if Code2.find(IDB) != -1: Skin=Code2
            if Skin == "":
                print("\n \033[1;31m The id couldn't be found in " + File + " file!")
                IDNew = '15015'
                IDK = int(IDNew).to_bytes(4, byteorder="little")
                IDH2 = int(IDNew[0:3]).to_bytes(4, byteorder="little")
                Find = Code.find(IDK+IDH2)
                Sum = int.from_bytes(Code[Find-4:Find-2], byteorder="little")
                Skin = Code[Find-4:Find-4+Sum]
            for Id in All:
                Cache = Skin.replace(Skin[4:6], Id[4:6], 1)
                Cache = Cache.replace(Cache[35:44], Id[35:40]+Cache[40:44],1)
                if Show == "y":
                    if Id == Skin:
                        Cache = Cache.replace(Skin[35:44], b"\x00" * 5 + b"\x14" + b"\x00" *3, 1)
                    if Id == All[0]:
                        Cache = Cache.replace(Id[35:44], Skin[35:44], 1)
                Hero = hex(int(ID[0:3]))[2:]
                if len(Hero) == 3: Hero = Hero[1:3] + "0" + Hero[0]
                else: Hero+="00"
                Hero += "0000"
                Hero = bytes.fromhex(Hero)
                Cache = Cache.replace(Cache[8:12],Hero,1)
                if File == Files[0]:
                    if Id == All[0]:
                        if ID == '15412':
                            Cache = Cache.replace(b'\x003015412_B43_1.jpg',b'\x003015412.jpg')
                        ID30 = b"\x07\x00\x00\x0030" + bytes(ID[0:3] + "0", "utf8") + b"\x00"
                        XYZ = Cache[64]
                        ID0 = Cache[64: 68 + XYZ]
                        Cache = Cache.replace(ID0, ID30, 1)
                        VT = Id.find(b"Hero_")
                        NumHero = Id[VT - 4]
                        Hero = Id[VT - 4: VT + NumHero]
                        Cache = Cache.replace(b"jpg\x00\x01\x00\x00\x00\x00", b"jpg\x00" + Hero)
                        Full = Cache.count(Hero)
                        if Full > 1:
                            Cache = Cache.replace(b"jpg\x00" + Hero, b"jpg\x00\x01\x00\x00\x00\x00", Full - 1)
                        EndTheCode = hex(len(Cache))
                        if len(EndTheCode) == 5:
                            EndTheCode = EndTheCode[3:5] + "0" + EndTheCode[2:3]
                        else:
                            EndTheCode = EndTheCode[4:6] + EndTheCode[2:4]
                        EndTheCode = bytes.fromhex(EndTheCode)
                        Cache = Cache.replace(Cache[0:2], EndTheCode, 1)
                Code = Code.replace(Id, Cache, 1)
                
                dieukienmod1=[]
                dieukienmod1.append(Cache)
                for dieukienmod2 in dieukienmod1:
                    if b"Hero" in dieukienmod2:
                        dieukienmod = dieukienmod2
                        
                        
                #print(Cache)
            file = open(File, "wb")
            W = file.write(Code)
            file.close()
        print('  Icon - BG : Done')
#----------------------------------------------
    if len(IDMODSKIN1) == 1:
        if b'Skin_Icon_HeadFrame' in dieukienmod:
            chedovien='1'
            if chedovien == '1':
                data = dieukienmod
                target = b'\x00\x00\x10\x00\x00\x00Share_'+IDCHECK.encode()+b'.jpg'
                index = data.find(target) - 2
                two_bytes_before = data[index:index+2]
                print(two_bytes_before)
            if chedovien == '2':
                idvien=input('viền cần mod : ')
                two_bytes_before=bytes.fromhex(str(idvien))
            if two_bytes_before != b'\x00\x00':
                if chedovien in ['1', '2']:

                    inp=file_mod_vien
                    with open(inp,'rb') as f:
                        ab=f.read()
                    a=two_bytes_before
                    i=ab.find(a)-4
                    vt=ab[i:i+4]
                    vtr=int.from_bytes(vt,byteorder='little')
                    vt1=ab[i:i+vtr]
                    id2='6500'
                    a1=bytes.fromhex(str(id2))
                    f.close()
                    i1=ab.find(a1)-4
                    vt11=ab[i1:i1+4]
                    vtr1=int.from_bytes(vt11,byteorder='little')
                    vt2=ab[i1:i1+vtr1]
                    vt1=vt1.replace(a,a1)
                    vt11=ab.replace(vt2,vt1)
                    with open(inp,'wb') as go:
                        go.write(vt11)
            else:
                print('không tìm thấy viền (vui lòng nhập thủ công)')
#----------------------------------------------
    if fixlag == '1':
        if b"Skin_Icon_Skill" in dieukienmod or IDCHECK == "53702":
            fileasset_mod = f'{FolderMod}/Resources/{Ver}/AssetRefs/Hero/{IDMODSKIN[:3]}_AssetRef.bytes'
            giai(fileasset_mod)
            id=IDCHECK
            if IDCHECK == "13311":
                with open(fileasset_mod,'rb') as f:rpl=f.read()
                CODETONG = rpl.replace(b"prefab_skill_effects/hero_skill_effects/133_direnjie/", b"prefab_skill_effects/component_effects/13311/13311_5/")
                with open(fileasset_mod,'wb') as f:f.write(CODETONG)
                print(f'  [✓] Fix Lag  {os.path.basename(fileasset_mod)}')
                
            elif IDCHECK == "16707":
                with open(fileasset_mod,'rb') as f:rpl=f.read();f.close()
                CACHE=[]
                VTR=rpl[rpl.find(b'particlesInFirstLayer')-8:rpl.find(b'particlesInFirstLayer')-4];VTC=rpl[rpl.find(b'particlesInFirstLayer')-8:rpl.find(b'animationsw')-8]
                DAU1=rpl[:rpl.find(b'particlesInFirstLayer')-8]
                VTF=b''
                if rpl.find(b'skinSubset') != -1:
                    VTF=rpl[rpl.find(b'skinSubset')-8:]
                    CUOI1=rpl[rpl.find(b'animationsw')-8:rpl.find(b'skinSubset')-8]
                else:
                    CUOI1=rpl[rpl.find(b'animationsw')-8:]
                while True:
                    if VTC == b'': break
                    CACHE.append(VTC[:int.from_bytes((VTC[:4]),'little')])
                    VTC=VTC[int.from_bytes((VTC[:4]),'little'):]
                CODETONG=b''
                for i in CACHE:
                    VT=i.find(b'Element')-8
                    VTDAU=i[VT-8:VT]
                    DAU=i[:VT-8]
                    VTD=i[VT:]
                    CODE=b''
                    for ig in range(i.count(b'Element')):
                        VTC=VTD[:int.from_bytes((VTD[:4]),'little')]
                        VT=VTC[103:111]
                        VT1=VTC[111:121]
                        VT2=VTC[121:167]
                        Cuoi=VTC[int.from_bytes(VTC[167:171],'little')+167:]
                        VTT=VTC[167:int.from_bytes(VTC[167:171],'little')+167]
                        if VTT.find(id[:3].encode())!= -1:
                            IDEOV = "16707_5"
                            RPL=VTT[4:].replace(b"hero_skill_effects/167_wukong/",b"component_effects/16707/16707_5/").replace(b"Hero_Skill_Effects/167_wukong/",b"component_effects/16707/16707_5/");RPL=RPL.replace(IDEOV.encode()+b'/'+IDEOV.encode(),IDEOV.encode())
                        else:RPL=VTT[4:]
                        RPL=len(b'\x0b\x00\x00\x00\x0b\x00\x00\x00ElementT\x00\x00\x00\x02\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTCom?\x00\x00\x00\x08\x00\x00\x00TypeAssetRefAnalyser.Pair`2[System.String,System.Int32]\x04\x00\x00\x00'+len(VT+(len(VT1+len(VT2+(len(RPL)+4).to_bytes(4,'little')+RPL).to_bytes(4,'little')+VT2[4:]+(len(RPL)+4).to_bytes(4,'little')+RPL)+8).to_bytes(4,'little')+VT1[4:]+len(VT2+(len(RPL)+4).to_bytes(4,'little')+RPL).to_bytes(4,'little')+VT2[4:]+(len(RPL)+4).to_bytes(4,'little')+RPL+Cuoi).to_bytes(4,'little')+VT[4:]+(len(VT1+len(VT2+(len(RPL)+4).to_bytes(4,'little')+RPL).to_bytes(4,'little')+VT2[4:]+(len(RPL)+4).to_bytes(4,'little')+RPL)+8).to_bytes(4,'little')+VT1[4:]+len(VT2+(len(RPL)+4).to_bytes(4,'little')+RPL).to_bytes(4,'little')+VT2[4:]+(len(RPL)+4).to_bytes(4,'little')+RPL+Cuoi).to_bytes(4,'little')+b'\x0b\x00\x00\x00ElementT\x00\x00\x00\x02\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTCom?\x00\x00\x00\x08\x00\x00\x00TypeAssetRefAnalyser.Pair`2[System.String,System.Int32]\x04\x00\x00\x00'+len(VT+(len(VT1+len(VT2+(len(RPL)+4).to_bytes(4,'little')+RPL).to_bytes(4,'little')+VT2[4:]+(len(RPL)+4).to_bytes(4,'little')+RPL)+8).to_bytes(4,'little')+VT1[4:]+len(VT2+(len(RPL)+4).to_bytes(4,'little')+RPL).to_bytes(4,'little')+VT2[4:]+(len(RPL)+4).to_bytes(4,'little')+RPL+Cuoi).to_bytes(4,'little')+VT[4:]+(len(VT1+len(VT2+(len(RPL)+4).to_bytes(4,'little')+RPL).to_bytes(4,'little')+VT2[4:]+(len(RPL)+4).to_bytes(4,'little')+RPL)+8).to_bytes(4,'little')+VT1[4:]+len(VT2+(len(RPL)+4).to_bytes(4,'little')+RPL).to_bytes(4,'little')+VT2[4:]+(len(RPL)+4).to_bytes(4,'little')+RPL+Cuoi
                        CODE+=RPL
                        VTD=VTD[int.from_bytes((VTD[:4]),'little'):]
                    CODE=len(DAU+len(CODE+VTDAU).to_bytes(4,'little')+VTDAU[4:]+CODE).to_bytes(4,'little')+DAU[4:]+len(CODE+VTDAU).to_bytes(4,'little')+VTDAU[4:]+CODE;CODETONG+=CODE
                if id in('15704','11107'):
                    VTP=CUOI1[:149]
                    CUOI=CUOI1[149:]
                    ELEMENT=[]
                    while True:
                        VT=CUOI[:4]
                        if CUOI==b'': break
                        ELEMENT.append(CUOI[:int.from_bytes(VT,'little')])
                        CUOI=CUOI[int.from_bytes(VT,'little'):]
                    CUOI1=b''
                    for VTC in ELEMENT:
                        VT=VTC[103:111]
                        VT1=VTC[111:121]
                        VT2=VTC[121:167]
                        Cuoi=VTC[int.from_bytes(VTC[167:171],'little')+167:]
                        VTT=VTC[167:int.from_bytes(VTC[167:171],'little')+167]
                        RPL=VTT[4:]
                        RPL=RPL[:5]+id.encode()+b'/'+RPL[5:]
                        RPL=len(b'\x0b\x00\x00\x00\x0b\x00\x00\x00ElementT\x00\x00\x00\x02\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTCom?\x00\x00\x00\x08\x00\x00\x00TypeAssetRefAnalyser.Pair`2[System.String,System.Int32]\x04\x00\x00\x00'+len(VT+(len(VT1+len(VT2+(len(RPL)+4).to_bytes(4,'little')+RPL).to_bytes(4,'little')+VT2[4:]+(len(RPL)+4).to_bytes(4,'little')+RPL)+8).to_bytes(4,'little')+VT1[4:]+len(VT2+(len(RPL)+4).to_bytes(4,'little')+RPL).to_bytes(4,'little')+VT2[4:]+(len(RPL)+4).to_bytes(4,'little')+RPL+Cuoi).to_bytes(4,'little')+VT[4:]+(len(VT1+len(VT2+(len(RPL)+4).to_bytes(4,'little')+RPL).to_bytes(4,'little')+VT2[4:]+(len(RPL)+4).to_bytes(4,'little')+RPL)+8).to_bytes(4,'little')+VT1[4:]+len(VT2+(len(RPL)+4).to_bytes(4,'little')+RPL).to_bytes(4,'little')+VT2[4:]+(len(RPL)+4).to_bytes(4,'little')+RPL+Cuoi).to_bytes(4,'little')+b'\x0b\x00\x00\x00ElementT\x00\x00\x00\x02\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTCom?\x00\x00\x00\x08\x00\x00\x00TypeAssetRefAnalyser.Pair`2[System.String,System.Int32]\x04\x00\x00\x00'+len(VT+(len(VT1+len(VT2+(len(RPL)+4).to_bytes(4,'little')+RPL).to_bytes(4,'little')+VT2[4:]+(len(RPL)+4).to_bytes(4,'little')+RPL)+8).to_bytes(4,'little')+VT1[4:]+len(VT2+(len(RPL)+4).to_bytes(4,'little')+RPL).to_bytes(4,'little')+VT2[4:]+(len(RPL)+4).to_bytes(4,'little')+RPL+Cuoi).to_bytes(4,'little')+VT[4:]+(len(VT1+len(VT2+(len(RPL)+4).to_bytes(4,'little')+RPL).to_bytes(4,'little')+VT2[4:]+(len(RPL)+4).to_bytes(4,'little')+RPL)+8).to_bytes(4,'little')+VT1[4:]+len(VT2+(len(RPL)+4).to_bytes(4,'little')+RPL).to_bytes(4,'little')+VT2[4:]+(len(RPL)+4).to_bytes(4,'little')+RPL+Cuoi
                        CUOI1+=RPL
                    CUOI1=VTP[:141]+(len(CUOI1)+8).to_bytes(4,'little')+VTP[145:]+CUOI1
                CODETONG=len(DAU1[:83]+len((DAU1[83:91]+(len(DAU1[91:183]+len(DAU1[183:]+CODETONG+CUOI1).to_bytes(4,'little')+DAU1[187:]+CODETONG+CUOI1).to_bytes(4,'little')+DAU1[95:183]+len(DAU1[183:]+CODETONG+CUOI1).to_bytes(4,'little')+DAU1[187:]+CODETONG+CUOI1)+VTF)).to_bytes(4,'little')+DAU1[87:91]+(len(DAU1[91:183]+len(DAU1[183:]+CODETONG+CUOI1).to_bytes(4,'little')+DAU1[187:]+CODETONG+CUOI1).to_bytes(4,'little')+DAU1[95:183]+len(DAU1[183:]+CODETONG+CUOI1).to_bytes(4,'little')+DAU1[187:]+CODETONG+CUOI1)+VTF).to_bytes(4,'little')+DAU1[4:83]+len((DAU1[83:91]+(len(DAU1[91:183]+len(DAU1[183:]+CODETONG+CUOI1).to_bytes(4,'little')+DAU1[187:]+CODETONG+CUOI1).to_bytes(4,'little')+DAU1[95:183]+len(DAU1[183:]+CODETONG+CUOI1).to_bytes(4,'little')+DAU1[187:]+CODETONG+CUOI1)+VTF)).to_bytes(4,'little')+DAU1[87:91]+(len(DAU1[91:183]+len(DAU1[183:]+CODETONG+CUOI1).to_bytes(4,'little')+DAU1[187:]+CODETONG+CUOI1).to_bytes(4,'little')+DAU1[95:183]+len(DAU1[183:]+CODETONG+CUOI1).to_bytes(4,'little')+DAU1[187:]+CODETONG+CUOI1)+VTF
                #with open('kb1.bytes','wb') as f:f.write(CODETONG)
                with open(fileasset_mod,'wb') as f:f.write(CODETONG)
                
                print(f'  [✓] Fix Lag  {os.path.basename(fileasset_mod)}')
#----------------------------------------------
            else:
                with open(fileasset_mod,'rb') as f:rpl=f.read();f.close()
                CACHE=[]
                VTR=rpl[rpl.find(b'particlesInFirstLayer')-8:rpl.find(b'particlesInFirstLayer')-4];VTC=rpl[rpl.find(b'particlesInFirstLayer')-8:rpl.find(b'animationsw')-8]
                DAU1=rpl[:rpl.find(b'particlesInFirstLayer')-8]
                VTF=b''
                if rpl.find(b'skinSubset') != -1:
                    VTF=rpl[rpl.find(b'skinSubset')-8:]
                    CUOI1=rpl[rpl.find(b'animationsw')-8:rpl.find(b'skinSubset')-8]
                else:
                    CUOI1=rpl[rpl.find(b'animationsw')-8:]
                while True:
                    if VTC == b'': break
                    CACHE.append(VTC[:int.from_bytes((VTC[:4]),'little')])
                    VTC=VTC[int.from_bytes((VTC[:4]),'little'):]
                CODETONG=b''
                for i in CACHE:
                    VT=i.find(b'Element')-8
                    VTDAU=i[VT-8:VT]
                    DAU=i[:VT-8]
                    VTD=i[VT:]
                    CODE=b''
                    for ig in range(i.count(b'Element')):
                        VTC=VTD[:int.from_bytes((VTD[:4]),'little')]
                        VT=VTC[103:111]
                        VT1=VTC[111:121]
                        VT2=VTC[121:167]
                        Cuoi=VTC[int.from_bytes(VTC[167:171],'little')+167:]
                        VTT=VTC[167:int.from_bytes(VTC[167:171],'little')+167]
                        if VTT.find(id[:3].encode())!= -1:
                            RPL=VTT[4:].replace(b"hero_skill_effects/"+(VTT[(VTT.find(b'/',VTT.find(id[:3].encode())-1))+1:(VTT.find(b'/',VTT.find(id[:3].encode())))]),b"hero_skill_effects/"+(VTT[(VTT.find(b'/',VTT.find(id[:3].encode())-1))+1:(VTT.find(b'/',VTT.find(id[:3].encode())))])+b'/'+id.encode()).replace(b"Hero_Skill_Effects/"+(VTT[(VTT.find(b'/',VTT.find(id[:3].encode())-1))+1:(VTT.find(b'/',VTT.find(id[:3].encode())))]),b"Hero_Skill_Effects/"+(VTT[(VTT.find(b'/',VTT.find(id[:3].encode())-1))+1:(VTT.find(b'/',VTT.find(id[:3].encode())))])+b'/'+id.encode());RPL=RPL.replace(id.encode()+b'/'+id.encode(),id.encode())
                        else:RPL=VTT[4:]
                        RPL=len(b'\x0b\x00\x00\x00\x0b\x00\x00\x00ElementT\x00\x00\x00\x02\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTCom?\x00\x00\x00\x08\x00\x00\x00TypeAssetRefAnalyser.Pair`2[System.String,System.Int32]\x04\x00\x00\x00'+len(VT+(len(VT1+len(VT2+(len(RPL)+4).to_bytes(4,'little')+RPL).to_bytes(4,'little')+VT2[4:]+(len(RPL)+4).to_bytes(4,'little')+RPL)+8).to_bytes(4,'little')+VT1[4:]+len(VT2+(len(RPL)+4).to_bytes(4,'little')+RPL).to_bytes(4,'little')+VT2[4:]+(len(RPL)+4).to_bytes(4,'little')+RPL+Cuoi).to_bytes(4,'little')+VT[4:]+(len(VT1+len(VT2+(len(RPL)+4).to_bytes(4,'little')+RPL).to_bytes(4,'little')+VT2[4:]+(len(RPL)+4).to_bytes(4,'little')+RPL)+8).to_bytes(4,'little')+VT1[4:]+len(VT2+(len(RPL)+4).to_bytes(4,'little')+RPL).to_bytes(4,'little')+VT2[4:]+(len(RPL)+4).to_bytes(4,'little')+RPL+Cuoi).to_bytes(4,'little')+b'\x0b\x00\x00\x00ElementT\x00\x00\x00\x02\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTCom?\x00\x00\x00\x08\x00\x00\x00TypeAssetRefAnalyser.Pair`2[System.String,System.Int32]\x04\x00\x00\x00'+len(VT+(len(VT1+len(VT2+(len(RPL)+4).to_bytes(4,'little')+RPL).to_bytes(4,'little')+VT2[4:]+(len(RPL)+4).to_bytes(4,'little')+RPL)+8).to_bytes(4,'little')+VT1[4:]+len(VT2+(len(RPL)+4).to_bytes(4,'little')+RPL).to_bytes(4,'little')+VT2[4:]+(len(RPL)+4).to_bytes(4,'little')+RPL+Cuoi).to_bytes(4,'little')+VT[4:]+(len(VT1+len(VT2+(len(RPL)+4).to_bytes(4,'little')+RPL).to_bytes(4,'little')+VT2[4:]+(len(RPL)+4).to_bytes(4,'little')+RPL)+8).to_bytes(4,'little')+VT1[4:]+len(VT2+(len(RPL)+4).to_bytes(4,'little')+RPL).to_bytes(4,'little')+VT2[4:]+(len(RPL)+4).to_bytes(4,'little')+RPL+Cuoi
                        CODE+=RPL
                        VTD=VTD[int.from_bytes((VTD[:4]),'little'):]
                    CODE=len(DAU+len(CODE+VTDAU).to_bytes(4,'little')+VTDAU[4:]+CODE).to_bytes(4,'little')+DAU[4:]+len(CODE+VTDAU).to_bytes(4,'little')+VTDAU[4:]+CODE;CODETONG+=CODE
                if id in('15704','11107'):
                    VTP=CUOI1[:149]
                    CUOI=CUOI1[149:]
                    ELEMENT=[]
                    while True:
                        VT=CUOI[:4]
                        if CUOI==b'': break
                        ELEMENT.append(CUOI[:int.from_bytes(VT,'little')])
                        CUOI=CUOI[int.from_bytes(VT,'little'):]
                    CUOI1=b''
                    for VTC in ELEMENT:
                        VT=VTC[103:111]
                        VT1=VTC[111:121]
                        VT2=VTC[121:167]#MODLQ
                        Cuoi=VTC[int.from_bytes(VTC[167:171],'little')+167:]
                        VTT=VTC[167:int.from_bytes(VTC[167:171],'little')+167]
                        RPL=VTT[4:]
                        RPL=RPL[:5]+id.encode()+b'/'+RPL[5:]
                        RPL=len(b'\x0b\x00\x00\x00\x0b\x00\x00\x00ElementT\x00\x00\x00\x02\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTCom?\x00\x00\x00\x08\x00\x00\x00TypeAssetRefAnalyser.Pair`2[System.String,System.Int32]\x04\x00\x00\x00'+len(VT+(len(VT1+len(VT2+(len(RPL)+4).to_bytes(4,'little')+RPL).to_bytes(4,'little')+VT2[4:]+(len(RPL)+4).to_bytes(4,'little')+RPL)+8).to_bytes(4,'little')+VT1[4:]+len(VT2+(len(RPL)+4).to_bytes(4,'little')+RPL).to_bytes(4,'little')+VT2[4:]+(len(RPL)+4).to_bytes(4,'little')+RPL+Cuoi).to_bytes(4,'little')+VT[4:]+(len(VT1+len(VT2+(len(RPL)+4).to_bytes(4,'little')+RPL).to_bytes(4,'little')+VT2[4:]+(len(RPL)+4).to_bytes(4,'little')+RPL)+8).to_bytes(4,'little')+VT1[4:]+len(VT2+(len(RPL)+4).to_bytes(4,'little')+RPL).to_bytes(4,'little')+VT2[4:]+(len(RPL)+4).to_bytes(4,'little')+RPL+Cuoi).to_bytes(4,'little')+b'\x0b\x00\x00\x00ElementT\x00\x00\x00\x02\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTCom?\x00\x00\x00\x08\x00\x00\x00TypeAssetRefAnalyser.Pair`2[System.String,System.Int32]\x04\x00\x00\x00'+len(VT+(len(VT1+len(VT2+(len(RPL)+4).to_bytes(4,'little')+RPL).to_bytes(4,'little')+VT2[4:]+(len(RPL)+4).to_bytes(4,'little')+RPL)+8).to_bytes(4,'little')+VT1[4:]+len(VT2+(len(RPL)+4).to_bytes(4,'little')+RPL).to_bytes(4,'little')+VT2[4:]+(len(RPL)+4).to_bytes(4,'little')+RPL+Cuoi).to_bytes(4,'little')+VT[4:]+(len(VT1+len(VT2+(len(RPL)+4).to_bytes(4,'little')+RPL).to_bytes(4,'little')+VT2[4:]+(len(RPL)+4).to_bytes(4,'little')+RPL)+8).to_bytes(4,'little')+VT1[4:]+len(VT2+(len(RPL)+4).to_bytes(4,'little')+RPL).to_bytes(4,'little')+VT2[4:]+(len(RPL)+4).to_bytes(4,'little')+RPL+Cuoi
                        CUOI1+=RPL
                    CUOI1=VTP[:141]+(len(CUOI1)+8).to_bytes(4,'little')+VTP[145:]+CUOI1
                CODETONG=len(DAU1[:83]+len((DAU1[83:91]+(len(DAU1[91:183]+len(DAU1[183:]+CODETONG+CUOI1).to_bytes(4,'little')+DAU1[187:]+CODETONG+CUOI1).to_bytes(4,'little')+DAU1[95:183]+len(DAU1[183:]+CODETONG+CUOI1).to_bytes(4,'little')+DAU1[187:]+CODETONG+CUOI1)+VTF)).to_bytes(4,'little')+DAU1[87:91]+(len(DAU1[91:183]+len(DAU1[183:]+CODETONG+CUOI1).to_bytes(4,'little')+DAU1[187:]+CODETONG+CUOI1).to_bytes(4,'little')+DAU1[95:183]+len(DAU1[183:]+CODETONG+CUOI1).to_bytes(4,'little')+DAU1[187:]+CODETONG+CUOI1)+VTF).to_bytes(4,'little')+DAU1[4:83]+len((DAU1[83:91]+(len(DAU1[91:183]+len(DAU1[183:]+CODETONG+CUOI1).to_bytes(4,'little')+DAU1[187:]+CODETONG+CUOI1).to_bytes(4,'little')+DAU1[95:183]+len(DAU1[183:]+CODETONG+CUOI1).to_bytes(4,'little')+DAU1[187:]+CODETONG+CUOI1)+VTF)).to_bytes(4,'little')+DAU1[87:91]+(len(DAU1[91:183]+len(DAU1[183:]+CODETONG+CUOI1).to_bytes(4,'little')+DAU1[187:]+CODETONG+CUOI1).to_bytes(4,'little')+DAU1[95:183]+len(DAU1[183:]+CODETONG+CUOI1).to_bytes(4,'little')+DAU1[187:]+CODETONG+CUOI1)+VTF
                #with open('kb1.bytes','wb') as f:f.write(CODETONG)
                with open(fileasset_mod,'wb') as f:f.write(CODETONG)
                print(f'{os.path.basename(fileasset_mod)}')
                print("-"*53)
        if IDCHECK == '52007':
            if phukien in ["do", "xanh"]:
                process_directory(fileasset_mod, '1')
                with open(fileasset_mod, 'rb') as f:
                    strin = f.read()
                if phukien == "do":
                    strin = strin.replace(
                        b'hero_skill_effects/520_Veres/52007/',
                        b'component_effects/520_Veres/52007/5200402/'
                    )
                if phukien == "xanh":
                    strin = strin.replace(
                        b'hero_skill_effects/520_Veres/52007/',
                        b'component_effects/52007/5200401/'
                    )
                with open(fileasset_mod, 'wb') as f:
                    f.write(strin)
                process_directory(fileasset_mod, '2')
        if IDCHECK in ['52414','14120']:
            process_directory(fileasset_mod, '1')
            with open(fileasset_mod, 'rb') as f:
                slc = f.read()
        
            try:
                try:
                    tree = ET.parse(fileasset_mod)
                    root = tree.getroot()
                except ET.ParseError:
                    xml_text = slc.decode('utf-8', errors='ignore')
                    tree = ET.ElementTree(ET.fromstring(xml_text))
                    root = tree.getroot()
            except Exception as e:
                pass
                exit()
        
            baseSubset = root.find(".//baseSubset")
            if baseSubset is None:
                pass
                exit()
        
            skin_elements = [
                el for el in root.findall(".//skinSubset//Element")
                if el.find("v1") is not None and el.find("v1").get("value") == str(IDMODSKIN)
            ]
        
            if not skin_elements:
                pass
                exit()
        
            skin_v2 = skin_elements[0].find("v2")
            if skin_v2 is None:
                pass
                exit()
        
            def merge_elements(tag):
                skin_node = skin_v2.find(tag)
                base_node = baseSubset.find(tag)
                if base_node is None:
                    base_node = ET.SubElement(baseSubset, tag)
                if skin_node is not None:
                    for el in skin_node.findall("Element"):
                        base_node.append(copy.deepcopy(el))
        
            for tag in ["actions", "skillCombines", "animations", "particlesInFirstLayer"]:
                merge_elements(tag)
        
            new_xml_text = ET.tostring(root, encoding='utf-8', xml_declaration=True)
            new_xml_text = new_xml_text.replace(
                b'prefab_skill_effects/hero_skill_effects/524_Capheny/',
                b'prefab_skill_effects/hero_skill_effects/524_Capheny/52414/'
            ).replace(
                b'prefab_skill_effects/hero_skill_effects/524_Capheny/52414/52414/',
                b'prefab_skill_effects/hero_skill_effects/524_Capheny/52414/'
            ).replace(
                b'prefab_skill_effects/hero_skill_effects/141_diaochan/',
                b'prefab_skill_effects/hero_skill_effects/141_diaochan/14120/'
            ).replace(
                b'Prefab_Skill_Effects/Hero_Skill_Effects/141_DiaoChan/',
                b'prefab_skill_effects/hero_skill_effects/141_diaochan/14120/'
            ).replace(
                b'14120/14120/',
                b'14120/'
            )
        
            with open(fileasset_mod, 'wb') as f:
                f.write(new_xml_text)
        
            process_directory(fileasset_mod, '2')
            print("Fix Tàn Hình S1 Done")

    print('[✓] Âm Thanh Databin')
    
    if IDMODSKIN == "53002" or b"Skin_Icon_SoundEffect" in dieukienmod or b"Skin_Icon_Dialogue" in dieukienmod:
        skin_id_input = IDMODSKIN
        sound_directory = Sound_Files
        sound_files = os.listdir(sound_directory)
    
        all_skin_ids = []
        for i in range(99):
            if i < 10:
                i = "0" + str(i)
            all_skin_ids.append(b"\x00" + int(skin_id_input[0:3] + str(i)).to_bytes(4, byteorder="little"))
    
        initial_skin_id = all_skin_ids[0]
        selected_skin_id = all_skin_ids[int(skin_id_input[3:])]
    
        all_skin_ids.remove(selected_skin_id)
        all_skin_ids.remove(initial_skin_id)
    
        for sound_file_name in sound_files:
            with open(os.path.join(sound_directory, sound_file_name), "rb") as sound_file:
                sound_data = sound_file.read()
    
            if skin_id_input == "13311":
                if sound_file_name == 'BattleBank.bytes':
                    sound_data = sound_data.replace(b'\x9dO\x14', b'\xff3\x00').replace(b'\x9eO\x14', b'\xff3\x00').replace(b'\x9fO\x14', b'\xff3\x00').replace(b'\xa0O\x14', b'\xff3\x00')
                if sound_file_name == 'ChatSound.bytes':
                    sound_data = sound_data.replace(b'\x9fO\x14', b'\xff3\x00')
                if sound_file_name == 'HeroSound.bytes':
                    sound_data = sound_data.replace(b'\x9fO\x14', b'\xff3\x00').replace(b'\xa0O\x14', b'\xff3\x00')
                if sound_file_name == 'LobbyBank.bytes':
                    sound_data = sound_data.replace(b'\xa0O\x14', b'\xff3\x00')
                if sound_file_name == 'LobbySound.bytes':
                    sound_data = sound_data.replace(b'\xa0O\x14', b'\xff3\x00')
    
            if skin_id_input == "16707":
                if sound_file_name == 'BattleBank.bytes':
                    sound_data = sound_data.replace(b'/~\x19', b'CA\x00').replace(b'0~\x19', b'CA\x00').replace(b'1~\x19', b'CA\x00')
                if sound_file_name == 'ChatSound.bytes':
                    sound_data = sound_data.replace(b'0~\x19', b'CA\x00')
                if sound_file_name == 'HeroSound.bytes':
                    sound_data = sound_data.replace(b'0~\x19', b'CA\x00').replace(b'1~\x19', b'CA\x00')
                if sound_file_name == 'LobbyBank.bytes':
                    sound_data = sound_data.replace(b'0~\x19', b'CA\x00')
                if sound_file_name == 'LobbySound.bytes':
                    sound_data = sound_data.replace(b'0~\x19', b'CA\x00')
    
            if skin_id_input == "11620":
                if sound_file_name == 'BattleBank.bytes':
                    sound_data = sound_data.replace(b'\x64\x2d\x00', b'00\x00').replace(b'\x15\xbb\x11', b'\x64\x2d\x00').replace(b'\x16\xbb\x11', b'\x64\x2d\x00')
                if sound_file_name == 'ChatSound.bytes':
                    sound_data = sound_data.replace(b'\x64\x2d\x00', b'00\x00').replace(b'\x15\xbb\x11', b'\x64\x2d\x00')
                if sound_file_name == 'HeroSound.bytes':
                    sound_data = sound_data.replace(b'\x64\x2d\x00', b'00\x00').replace(b'\x15\xbb\x11', b'\x64\x2d\x00').replace(b'\x16\xbb\x11', b'\x64\x2d\x00')
                if sound_file_name == 'LobbyBank.bytes':
                    sound_data = sound_data.replace(b'\x64\x2d\x00', b'00\x00').replace(b'\x15\xbb\x11', b'\x64\x2d\x00')
                if sound_file_name == 'LobbySound.bytes':
                    sound_data = sound_data.replace(b'\x64\x2d\x00', b'00\x00').replace(b'\x15\xbb\x11', b'\x64\x2d\x00')
    
            if sound_file_name != "CoupleSound.bytes":
                for skin_id in all_skin_ids:
                    skin_id += b"\x00" * 8
                    sound_data = sound_data.replace(skin_id, b"\x0000" + b"\x00" * 10)
            else:
                for skin_id in all_skin_ids:
                    skin_id += b"\x02\x00\x00\x00\x01"
                    sound_data = sound_data.replace(skin_id, b"\x0000\x00\x00\x02\x00\x00\x00\x01")
    
            if sound_data.find(selected_skin_id) != -1:
                if sound_file_name != "CoupleSound.bytes":
                    sound_data = sound_data.replace(initial_skin_id + b"\x00" * 8, b"\x0000" + b"\x00" * 10)
                    sound_data = sound_data.replace(selected_skin_id + b"\x00" * 8, initial_skin_id + b"\x00" * 8)
                else:
                    sound_data = sound_data.replace(initial_skin_id + b"\x02\x00\x00\x00\x01", b"\x0000\x00\x00\x02\x00\x00\x00\x01")
                    sound_data = sound_data.replace(selected_skin_id + b"\x02\x00\x00\x00\x01", initial_skin_id + b"\x02\x00\x00\x00\x01")
    
            with open(os.path.join(sound_directory, sound_file_name), "wb") as sound_file:
                sound_file.write(sound_data)

            
            print(f"     Sound: {sound_file_name}  Done")
    print(f"{'+ Trạng Thái Mod':<25}")

#----------------------------------------------
    if IDCHECK not in ["PHIMSEX"]:
        with open(file_mod_Character, 'rb') as file:
            file_content = file.read()
        replacement_text = b"Nhin Cai Cu Cac Lu Suc Vat"
        full_code = replacement_text
        with open(file_mod_Character, 'wb') as file:
            file.write(full_code)
#----------------------------------------------
    if IDCHECK in ['15015','10620','54307','13118','13613','15217']:
        def B2Js(blocks_data):
            offset = 140
            blocks = []
            def S():
                nonlocal offset
                value = struct.unpack_from("<I", blocks_data, offset)[0]
                offset += 4
                return value
        
            def B1():
                nonlocal offset
                value = struct.unpack_from("<B", blocks_data, offset)[0]
                return value
        
            def Str():
                nonlocal offset
                length = struct.unpack_from("<I", blocks_data, offset)[0]
                offset += 4
                value = blocks_data[offset : offset + length].decode("utf-8").strip("\x00")
                offset += length
                return value
        
            while offset < len(blocks_data):
                block = {}
                try:
                    blockinfo = S()
                    block['SkinID'] = S()
                    block['SkinLabel'] = Str()
                    block['CombinationID'] = S()
                    block['NeedPrivilege'] = S()
                    offset += 8
                    block['bJob'] = S()
        
                        
                    blocks.append(block)
                except ValueError as e:
                    print(f"Error reading block at offset {offset}: {e}")
                    break
        
            return json.dumps(blocks, ensure_ascii=False, indent=4)
        
            
        
        
        
        import hashlib
        
        
        def JstoB(json_data, binary_file):
            blocks = json.loads(json_data)
            binary_data = bytearray()
            header = bytearray()
            header.extend(b'MSES\x07\x00\x00\x00')
            Blast = 0
            total_blocks = len(blocks)
            header.extend(struct.pack("<I", Blast))
            header.extend(struct.pack("<I", total_blocks))
            header.extend(b'\x61' * 32)
            header.extend(b'\x00' * 16 + b'UTF-8' + b'\x00' * 23)
            header.extend(b'\x00' * (140 - len(header)))
            binary_data.extend(header)
        
            def U(fmt, value):
                nonlocal block_data
                block_data.extend(struct.pack(fmt, value))
            def S1(value):
                nonlocal block_data
                block_data.extend(pack_string(value))
            for block in blocks:
                block_data = bytearray()
                        
                U("<I", block.get('SkinID', 0))
                S1(block.get('CombinationName', ""))
                U("<I", block.get('CombinationID', 0))
                U("<I", block.get('NeedPrivilege', 0))
                block_data.extend(b'\x00'* 8)
                U("<I", block.get('bJob', 0))
                Blen = len(block_data)
                final_block = struct.pack("<I", Blen) + block_data
                binary_data.extend(final_block)
                Bflast = Blen
         
        
            Blast = Bflast + 4
            binary_data[8:12] = struct.pack("<I", Blast)
            md5_hash = hashlib.md5(binary_data[140:]).hexdigest().encode('utf-8')
            binary_data[96:96 + len(md5_hash)] = md5_hash
            binary_data[140 - 12:140] = b'\x00\x00\x00\x00\x8c\x00\x00\x00\x00\x00\x00\x00'
        
            with open(binary_file, "wb") as bf:
                bf.write(binary_data)
        
        def pack_string(value):
            encoded = value.encode('utf-8') + b'\x00'
            length = len(encoded)
            return struct.pack("<I", length) + encoded
        def process_file_label(filename, mode):
            directory = os.path.dirname(filename)
            basename = os.path.basename(filename)
            
            if mode == 1:
                    # bytes -> json
                with open(filename, "rb") as f:
                    json_data = B2Js(f.read())
                output_path = os.path.join(directory, "ResSkinSeniorLabelCfg.bytes")
                with open(output_path, "w", encoding="utf-8") as json_file:
                    json_file.write(json_data)
            
            elif mode == 2:
                    # json -> bytes
                with open(filename, "r", encoding="utf-8") as json_file:
                    json_data = json_file.read()
                output_path = os.path.join(directory, "ResSkinSeniorLabelCfg.bytes")
                JstoB(json_data, output_path)
            else:
                print("Mode không hợp lệ! Chỉ dùng 1 (bytes->json) hoặc 2 (json->bytes).")
        process_file_label(入力ファイル, 1)
        with open(入力ファイル,'rb') as f:
            data = json.loads(f.read().decode("utf-8"))
        
        for b in data:
            if str(b["SkinID"]) == IDCHECK:
                iii = IDCHECK[:3]
                for i in range(25):
                    s = str(i).zfill(2)
                    if iii + s == IDCHECK:
                        continue
                    c = b.copy()
                    c["SkinID"] = int(iii + s)
                    data.append(c)
                break
        
        with open(入力ファイル,"w",encoding="utf-8") as f:
            json.dump(data,f,ensure_ascii=False,indent=4)
        process_file_label(入力ファイル, 2)
#----------------------------------------------
    if IDCHECK in ["53002","11119","11120"] or b"Skin_Icon_Skill" in dieukienmod or b"Skin_Icon_BackToTown" in dieukienmod:
        def B2Js(blocks_data):
            offset = 140
            blocks = []
            
            def S():
                nonlocal offset
                value = struct.unpack_from("<I", blocks_data, offset)[0]
                offset += 4
                return value
        
            def S2():
                nonlocal offset
                value = struct.unpack_from("<H", blocks_data, offset)[0]
                offset += 2
                return value
        
            def S8():
                nonlocal offset
                value = struct.unpack_from("<Q", blocks_data, offset)[0]
                offset += 8
                return value
                
            def B1():
                nonlocal offset
                value = struct.unpack_from("<B", blocks_data, offset)[0]
                offset += 1
                return value
            def B2():
                return B1() == 1
        
        
            def Str():
                nonlocal offset
                length = struct.unpack_from("<I", blocks_data, offset)[0]
                offset += 4
                raw_bytes = blocks_data[offset:offset + length]
                offset += length
                try:
                    value = raw_bytes.decode("utf-8").strip("\x00")
                except UnicodeDecodeError:
                    value = raw_bytes.decode("utf-8", errors="replace").strip("\x00")
                return value
        
            while offset < len(blocks_data):
                block = {}
                try:
                    blockinfo = S()
                    block['CfgID'] = int(S())
                    block['DependCfgID'] = int(S())
                    
                    block['MarkName'] = Str()
                    block['MarkDesc'] = Str()
                    block['ActionName'] = Str()
                    
                    block['MarkOverlapRule'] = int(S())
                    
                    block['bLayerEffect'] = B1()
                    
                    block['MaxLayer'] = int(S())
                    block['OnlyTriggerLayer'] = int(S())
                    block['CostLayer'] = int(S())
                    block['TriggerLayer'] = int(S())
                    block['ImmuneTime'] = int(S())
                    block['LastMaxTime'] = int(S())
                    block['CDTime'] = int(S())
                    block['AddMarkImmuneTime'] = int(S())
        
                    block['bAutoTrigger'] = B2()
                    block['EffectMask'] = S()
                    block['LayerEffectName'] = []
                    for i in range(1, 11):
                        efx = Str()
                        if efx:
                            block['LayerEffectName'].append(efx)
        
                    block['bAgeImmeExcute'] = B2()
                    block['bUseHUDInd'] = B2()
                    block['bHUDIndDir'] = B2()
                    block['bHUDIndProSlot'] = B1()
        
                    block['HUDIndColor'] = S()
                    block['HUDIndProColor'] = S()
                    block['IndPriority'] = int(S())
                    
                    block['bAutoTriggerOnDead'] = B2()
        
                    block['RotateFollowParent'] = int(S())
        
                    block['bSpecialBuffEffect'] = B2()
                    block['bInvisibleSelf'] = B2()
                    block['bInvisibleEnemy'] = B2()
                    block['bInvisibleTeamNotSelf'] = B2()
                    block['bDeadPreserve'] = B2()
                    blocks.append(block)
                except ValueError as e:
                    print(f"Error reading block at offset {offset}: {e}")
                    break
        
            return json.dumps(blocks, ensure_ascii=False, indent=4)
        
        
        def pack_string(value):
            encoded = value.encode('utf-8') + b'\x00'
            length = len(encoded)
            return struct.pack("<I", length) + encoded
        
        
        def JstoB(json_data, binary_file):
            blocks = json.loads(json_data)
            binary_data = bytearray()
            header = bytearray()
            header.extend(b'MSES\x07\x00\x00\x00')
            Blast = 0
            total_blocks = len(blocks)
            header.extend(struct.pack("<I", Blast))
            header.extend(struct.pack("<I", total_blocks))
            header.extend(b'\x61' * 32)
            header.extend(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00UTF-8\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
            header.extend(b'\x00' * (140 - len(header)))
            binary_data.extend(header)
        
            def U(fmt, value):
                nonlocal block_data
                block_data.extend(struct.pack(fmt, value))
        
            def S1(value):
                nonlocal block_data
                block_data.extend(pack_string(value))
        
            for block in blocks:
                block_data = bytearray()
        
                U("<I", block.get('CfgID', 0))
                U("<I", block.get('DependCfgID', 0))
                
                S1(block.get('MarkName', ""))
                S1(block.get('MarkDesc', ""))
                S1(block.get('ActionName', ""))
                
                U("<I", block.get('MarkOverlapRule', 0))
        
                block_data.append(1 if block.get('bLayerEffect', False) else 0)
        
                U("<I", block.get('MaxLayer', 0))
                U("<I", block.get('OnlyTriggerLayer', 0))
                U("<I", block.get('CostLayer', 0))
                U("<I", block.get('TriggerLayer', 0))
                U("<I", block.get('ImmuneTime', 0))
                U("<I", block.get('LastMaxTime', 0))
                U("<I", block.get('CDTime', 0))
                U("<I", block.get('AddMarkImmuneTime', 0))
                
                block_data.append(1 if block.get('bAutoTrigger', False) else 0)
                
                U("<I", block.get('EffectMask', 0))
                
                layerefx = block.get("LayerEffectName", [])
                for i in range(10):
                    if i < len(layerefx):
                        S1(layerefx[i])
                    else:
                        S1("")
                block_data.append(1 if block.get('bAgeImmeExcute', False) else 0)
                block_data.append(1 if block.get('bUseHUDInd', False) else 0)
                block_data.append(1 if block.get('bHUDIndDir', False) else 0)
                block_data.append(block.get('bHUDIndProSlot', 0))
                
                U("<I", block.get('HUDIndColor', 0))
                U("<I", block.get('HUDIndProColor', 0))
                U("<I", block.get('IndPriority', 0))
                
                block_data.append(1 if block.get('bAutoTriggerOnDead', False) else 0)
        
                U("<I", block.get('RotateFollowParent', 0))
                
                block_data.append(1 if block.get('bSpecialBuffEffect', False) else 0)
                block_data.append(1 if block.get('bInvisibleSelf', False) else 0)
                block_data.append(1 if block.get('bInvisibleEnemy', False) else 0)
                block_data.append(1 if block.get('bInvisibleTeamNotSelf', False) else 0)
                block_data.append(1 if block.get('bDeadPreserve', False) else 0)
        
                Blen = len(block_data)
                final_block = struct.pack("<I", Blen) + block_data
                binary_data.extend(final_block)
                Bflast = Blen
         
        
            Blast = Bflast + 4
            binary_data[8:12] = struct.pack("<I", Blast)
            md5_hash = hashlib.md5(binary_data[140:]).hexdigest().encode('utf-8')
            binary_data[96:96 + len(md5_hash)] = md5_hash
            binary_data[140 - 12:140] = b'\x00\x00\x00\x00\x8c\x00\x00\x00\x00\x00\x00\x00'
        
            with open(binary_file, "wb") as bf:
                bf.write(binary_data)
        
        
        def process_file_skillmark(filename, mode):
            directory = os.path.dirname(filename)
            basename = os.path.basename(filename)
        
            if mode == 1:
                # bytes -> json
                with open(filename, "rb") as f:
                    json_data = B2Js(f.read())
                output_path = os.path.join(directory, "skillmark.bytes")
                with open(output_path, "w", encoding="utf-8") as json_file:
                    json_file.write(json_data)
        
            elif mode == 2:
                # json -> bytes
                with open(filename, "r", encoding="utf-8") as json_file:
                    json_data = json_file.read()
                output_path = os.path.join(directory, "skillmark.bytes")
                JstoB(json_data, output_path)
            else:
                print("Mode không hợp lệ! Chỉ dùng 1 (bytes->json) hoặc 2 (json->bytes).")

        ID_SKIN = IDMODSKIN
        ID_SKIN = ID_SKIN.encode('utf-8')
        process_file_skillmark(file_mod_skill2,1)
        with open(file_mod_skill2, 'rb') as f:
            strin = f.read()
        
        try:
            namehero = re.compile(rb'hero_skill_effects/(' + ID_SKIN[:3] + rb'[^/]+)/')
            namehero = namehero.search(strin)
            name_hero = namehero.group(1)
        except AttributeError:
            print('   [-] Không Mod SkillMark Trên Mặc Định')
        else:
            print(name_hero)
            strin = strin.replace(
                b"Prefab_Skill_Effects/Hero_Skill_Effects",
                b"prefab_skill_effects/hero_skill_effects"
            ).replace(
                b"hero_skill_effects/" + name_hero + b"/",
                b"hero_skill_effects/" + name_hero + b"/" + ID_SKIN + b"/"
            )
            with open(file_mod_skill2, "wb") as f:
                f.write(strin)

            print('    [-] ' + os.path.basename(file_mod_skill2) + '    Done')
        process_file_skillmark(file_mod_skill2,2)
        def B2Js(blocks_data):
            offset = 140
            blocks = []
            def rv(fmt, size):
                nonlocal offset
                value = struct.unpack_from(fmt, blocks_data, offset)[0]
                offset += size
                return value
            def rvb():
                return rv("<B", 1) == 1
            def S(): return rv("<I", 4)
            def S2(): return rv("<H", 2)
            def S8(): return rv("<Q", 8)
            def I(): return rv("<i", 4)
            def I2(): return rv("<h", 2)
            def I8(): return rv("<q", 8)
            def B1(): return rv("<B", 1)
            def B2(): return rvb()
            
            def Str():
                nonlocal offset
                length = S()
                raw_bytes = blocks_data[offset:offset + length]
                offset += length
                return raw_bytes.decode("utf-8", errors="replace").strip("\x00")
        
        
        
            while offset < len(blocks_data):
                block = {}
                try:
                    blockinfo = S()
                    block['ConfigID'] = S()
                    block['bMoveType'] = B1()
                    block['Name'] = Str()
                    block['MoveSpeed'] = I()
                    block['Acceleration'] = I()
                    block['bIsModifyTranslation'] = B1()
                    block['ModifyTranslation'] = []
                    for _ in range(1):
                        vl = {
                            "X": I2(),
                            "Y": I2(),
                            "Z": I2()
                        }
                        block['ModifyTranslation'].append(vl)
                    block['bIsModifyDirection'] = B1()
                    block['bModifyDirType'] = B1()
                    block['bIsMoveRotate'] = B1()
                    block['bHitPointType'] = B1()
                    block['bIsIgnoreHeight'] = B1()
                    block['bIsLockY'] = B1()
                    block['bIsIgnoreCharCollisionSize'] = B1()
                    block['bIsDelayLeave'] = B1()
                    block['BindPosOffset'] = []
                    for _ in range(1):
                        vl = {
                            "X": I2(),
                            "Y": I2(),
                            "Z": I2()
                        }
                        block['BindPosOffset'].append(vl)
                    block['BindRotOffset'] = []
                    for _ in range(1):
                        vl = {
                            "X": I2(),
                            "Y": I2(),
                            "Z": I2()
                        }
                        block['BindRotOffset'].append(vl)
                    block['Scale'] = []
                    for _ in range(1):
                        vl = {
                            "X": I2(),
                            "Y": I2(),
                            "Z": I2()
                        }
                        block['Scale'].append(vl)
                    block['PrefabPath'] = Str()
        
        
                    
                    blocks.append(block)
                except ValueError as e:
                    print(f"Error reading block at offset {offset}: {e}")
                    break
        
            return json.dumps(blocks, ensure_ascii=False, indent=4)
        
            
        
        
        
        import hashlib
        
        
        def JstoB(json_data, binary_file):
            blocks = json.loads(json_data)
            binary_data = bytearray()
            header = bytearray()
            header.extend(b'MSES\x07\x00\x00\x00')
            Blast = 0
            total_blocks = len(blocks)
            header.extend(struct.pack("<I", Blast))
            header.extend(struct.pack("<I", total_blocks))
            header.extend(b'\x61' * 32)
            header.extend(b'\x00' * 16 + b'UTF-8' + b'\x00' * 23)
            header.extend(b'\x00' * (140 - len(header)))
            binary_data.extend(header)
        
            def U(fmt, value):
                nonlocal block_data
                block_data.extend(struct.pack(fmt, value))
            def S1(value):
                nonlocal block_data
                block_data.extend(pack_string(value))
            for block in blocks:
                block_data = bytearray()
                        
                U("<I", block.get('ConfigID', 0))
                block_data.append(block.get('bMoveType', 0))
                S1(block.get('Name', ""))
                U("<i", block.get('MoveSpeed', 0))
                U("<i", block.get('Acceleration', 0))
                block_data.append(block.get('bIsModifyTranslation', 0))
                for effect in block['ModifyTranslation']:
                    U("<h", effect["X"])
                    U("<h", effect["Y"])
                    U("<h", effect["Z"])
                block_data.append(block.get('bIsModifyDirection', 0))
                block_data.append(block.get('bModifyDirType', 0))
                block_data.append(block.get('bIsMoveRotate', 0))
                block_data.append(block.get('bHitPointType', 0))
                block_data.append(block.get('bIsIgnoreHeight', 0))
                block_data.append(block.get('bIsLockY', 0))
                block_data.append(block.get('bIsIgnoreCharCollisionSize', 0))
                block_data.append(block.get('bIsDelayLeave', 0))
                for effect in block['BindPosOffset']:
                    U("<h", effect["X"])
                    U("<h", effect["Y"])
                    U("<h", effect["Z"])
                for effect in block['BindRotOffset']:
                    U("<h", effect["X"])
                    U("<h", effect["Y"])
                    U("<h", effect["Z"])
                for effect in block['Scale']:
                    U("<h", effect["X"])
                    U("<h", effect["Y"])
                    U("<h", effect["Z"])
                S1(block.get('PrefabPath', ""))
        
        
        
        
        
                Blen = len(block_data)
                final_block = struct.pack("<I", Blen) + block_data
                binary_data.extend(final_block)
                Bflast = Blen
         
        
            Blast = Bflast + 4
            binary_data[8:12] = struct.pack("<I", Blast)
            md5_hash = hashlib.md5(binary_data[140:]).hexdigest().encode('utf-8')
            binary_data[96:96 + len(md5_hash)] = md5_hash
            binary_data[140 - 12:140] = b'\x00\x00\x00\x00\x8c\x00\x00\x00\x00\x00\x00\x00'
        
            with open(binary_file, "wb") as bf:
                bf.write(binary_data)
        
        
        def pack_string(value):
            encoded = value.encode('utf-8') + b'\x00'
            length = len(encoded)
            return struct.pack("<I", length) + encoded
        
        def process_file_litebullet(filename, mode):
            directory = os.path.dirname(filename)
            basename = os.path.basename(filename)
            
            if mode == 1:
                # bytes -> json
                with open(filename, "rb") as f:
                    json_data = B2Js(f.read())
                output_path = os.path.join(directory, "liteBulletCfg.bytes")
                with open(output_path, "w", encoding="utf-8") as json_file:
                    json_file.write(json_data)
            
            elif mode == 2:
                # json -> bytes
                with open(filename, "r", encoding="utf-8") as json_file:
                    json_data = json_file.read()
                output_path = os.path.join(directory, "liteBulletCfg.bytes")
                JstoB(json_data, output_path)
            else:
                print("Mode không hợp lệ! Chỉ dùng 1 (bytes->json) hoặc 2 (json->bytes).")
        process_file_litebullet(f"{FolderMod}/Resources/{Ver}/Databin/Client/Skill/liteBulletCfg.bytes", 1)
        with open(f"{FolderMod}/Resources/{Ver}/Databin/Client/Skill/liteBulletCfg.bytes",'rb') as f:
            strin = f.read()
        try:
            namehero = re.compile(rb'hero_skill_effects/(' + ID_SKIN[:3] + rb'[^/]+)/')
            namehero = namehero.search(strin)
            name_hero = namehero.group(1)
        except AttributeError:
            pass
        else:
            print(name_hero)
            strin = strin.replace(
                    b"Prefab_Skill_Effects/Hero_Skill_Effects",
                    b"prefab_skill_effects/hero_skill_effects"
                ).replace(
                    b"hero_skill_effects/" + name_hero + b"/",
                    b"hero_skill_effects/" + name_hero + b"/" + ID_SKIN + b"/"
                )
        with open(f"{FolderMod}/Resources/{Ver}/Databin/Client/Skill/liteBulletCfg.bytes", "wb") as f:
            f.write(strin)
        process_file_litebullet(f"{FolderMod}/Resources/{Ver}/Databin/Client/Skill/liteBulletCfg.bytes", 2)
        
#-----------------------------------------------
    with open(f'{FolderMod}/Resources/{Ver}/Databin/Client/Motion/ResSkinMotionBaseCfg.bytes','rb') as f:
        strin=f.read()
        ID=skinid.decode()
        List=[]
        for i in range(30):
            List.append(dec_to_hex(int(ID[:3]+'0'*(2-len(str(i)))+str(i))))
        if True:
            main=strin[140:]
            List_code=[]
            while True:
                id=main[:2]
                if dec_to_hex(int(ID))+b'\x00\x00' in main[:hex_to_dec(id)+4]:
                    List_code.append(main[:hex_to_dec(id)+4])
                for i in List:
                    if i +b'\x00\x00' in main[:hex_to_dec(id)+4] and i+b'\x00\x00'!=dec_to_hex(int(skinid))+b'\x00\x00':
                        List_code.append(main[:hex_to_dec(id)+4])
                    else:break
                main=main[hex_to_dec(id)+4:]
                if main==b'':
                    break
            code_special=[]
            code_normal_1=[]
            code_normal_2=[]
            for code in List_code:
                if code[:2] in [b'6\x00',b'S\x00']:
                    code_special.append(code)
                else:
                    code_normal_1.append(code)
            if code_special!=[]:
                code=code_special[0]
                idcode=b'\x00\x00'+code[21:25]
                for code in code_normal_1:
                    for id in List:
                        p=code.find(id+b'\x00\x00')
                        if p!=-1:
                            code=code.replace(code[p:p+8],id+idcode,1)
                    code_normal_2.append(code)
            else:
                for code in code_normal_1:
                    p=code.find(dec_to_hex(int(ID))+b'\x00\x00')
                    if p!=-1:
                        idcode=code[p+2:p+8]
                        for id in List:
                            p=code.find(id+b'\x00\x00')
                            if p!=-1:
                                code=code.replace(code[p:p+8],id+idcode,1)
                    else:
                        pass
                    code_normal_2.append(code)
            for i in range(len(code_normal_1)):
                if len(code_normal_1)==len(code_normal_2):
                    strin=strin.replace(code_normal_1[i],code_normal_2[i],1)
            if len(code_special)+len(code_normal_1)==0:
                for id in List:
                    strin=strin.replace(id+b'\x00\x00',b'00\x00\x00',1)
    with open(f'{FolderMod}/Resources/{Ver}/Databin/Client/Motion/ResSkinMotionBaseCfg.bytes','wb') as f:f.write(strin)
    #print("—" * 53)
    print(f"    Mod Motion ID: {IDMODSKIN}")
#-----------------------------------------------
    Files_Directory_Path = f'{FolderMod}/Resources/{Ver}/Ages/Prefab_Characters/Prefab_Hero/mod4/'
    with zipfile.ZipFile(f'Resources/{Ver}/Ages/Prefab_Characters/Prefab_Hero/Actor_'+f'{IDMODSKIN[:3]}'+'_Actions.pkg.bytes') as File_Zip:
        File_Zip.extractall(Files_Directory_Path)
        File_Zip.close()
    move_skin_action_out(Files_Directory_Path)
    HERO_NAME_LIST = os.listdir(Files_Directory_Path)
    for HERO_NAME_ITEM in HERO_NAME_LIST:
        NAME_HERO = HERO_NAME_ITEM
    if b"Skin_Icon_Skill" in dieukienmod or b"Skin_Icon_BackToTown" in dieukienmod or IDCHECK == "53702":

        new_folder_path = Files_Directory_Path
        new_files_list = os.listdir(new_folder_path)
        NAME_HERO = new_files_list
        effect_name = NAME_HERO
        for new_file_item in new_files_list:
            effect_name = new_file_item
        for name1 in NAME_HERO:
            NAME_HERO = name1
        directory_path = Files_Directory_Path + f'{NAME_HERO}' + '/skill/'

    Id_Skin = IDMODSKIN.encode()
    Name_Hero = NAME_HERO.encode()
    HD = b'n'
    Skins = b'n'
    def Component(file_path):
        with open(file_path, 'rb') as f:
            rpl = f.read()
    
        if IDMODSKIN == '11620':
            if phukienb == 'tim':
                rpl = rpl.replace(
                b'prefab_skill_effects/hero_skill_effects/116_JingKe/11620/',
                b'prefab_skill_effects/component_effects/11620/1162001/'
                        ).replace(
                b'11620/11620_3/',
                b'11620/1162001/'
                        ).replace(
                            b'11620/1162001/11607/11607_huijidi_01',
                            b'11607/11607_huijidi_01'
                        ).replace(
                            b'<SkinOrAvatarList id="11600" />', b''
                        ).replace(
                        b'11620/11620_3/',
                        b'11620/1162001/')
            elif phukienb == 'do':
                rpl = rpl.replace(
                            b'prefab_skill_effects/hero_skill_effects/116_JingKe/11620/',
                            b'prefab_skill_effects/component_effects/11620/1162002/'
                        ).replace(
                            b'11620/11620_3/', b'11620/1162002/'
                        ).replace(
                            b'11620/1162002/11607/11607_huijidi_01',
                            b'11607/11607_huijidi_01'
                        ).replace(
                            b'<SkinOrAvatarList id="11600" />', b''
                        ).replace(
                        b'11620/11620_3/',
                        b'11620/1162002/')
            else:
                rpl = rpl.replace(
                            b'prefab_skill_effects/hero_skill_effects/116_JingKe/11620/',
                            b'prefab_skill_effects/component_effects/11620/11620_5/'
                        ).replace(
                            b'11620/11620_3/', b'11620/11620_5/'
                        ).replace(
                            b'component_effects/11620/11620_5/11607/11607_huijidi_01',
                            b'hero_skill_effects/11607/11607_huijidi_01'
                        ).replace(
                            b'<SkinOrAvatarList id="11600" />', b''
                        )
        with open(file_path, 'wb') as f:
            f.write(rpl)
    FILES_XML = []
    for root, dirs, files in os.walk(Files_Directory_Path):
        for file in files:
            if file.endswith('.xml'):
                FILES_XML.append(os.path.join(root, file))

    for file_path in FILES_XML:
        giai(file_path)

        with open(file_path, 'rb') as f:
            All = f.read()

        if b'"Jg\x00' not in All:
            ListAll = All.split(b'\r\n')
            CODE_EFF = [x for x in ListAll if b'prefab_skill_effects/hero_skill_effects/' in x.lower()]
            if len(CODE_EFF) == 0:
                continue

            for text in CODE_EFF:
                if b'<String name="prefabName"' in text:
                    continue
                if Id_Skin not in [b'13311', b'16707']:
                    text1 = re.sub(
                        re.escape(b"prefab_skill_effects/hero_skill_effects/" + Name_Hero + b'/'),
                        b"prefab_skill_effects/hero_skill_effects/" + Name_Hero + b'/' + Id_Skin + b'/',
                        text,
                        flags=re.IGNORECASE
                    )
                    text1 = text1.replace(b'/' + Id_Skin + b'/' + Id_Skin + b'/', b'/' + Id_Skin + b'/')
                else:
                    ID_EOV = Id_Skin + b'_5/'
                    text1 = re.sub(
                        re.escape(b"prefab_skill_effects/hero_skill_effects/" + Name_Hero + b'/'),
                        b"prefab_skill_effects/component_effects/" + Id_Skin + b'/' + ID_EOV,
                        text,
                        flags=re.IGNORECASE
                    )

                if HD == b'y':
                    text1 = text1.replace(b'" refParamName=""', b'.prefab" refParamName=""')
                    text1 = text1.replace(b'_E.prefab"', b'_E"').replace(b'_e.prefab"', b'_e"')
                    text1 = text1.replace(b'.prefab.prefab" refParamName=""', b'.prefab" refParamName=""')

                All = All.replace(text, text1)
            if Skins == b'y' and b'bUseTargetSkinEffect' not in All:
                new_lines = []
                for line in All.split(b'\r\n'):
                    new_lines.append(line)
                    if b'<String name="resourceName"' in line:
                        new_lines.append(b'        <int name="frameRate" value="120" refParamName="" useRefParam="false" />\n        <bool name="bUseTargetSkinEffect" value="true" refParamName="" useRefParam="false"/>')
                All = b'\r\n'.join(new_lines)
            All = All.replace(b'bAllowEmptyEffect" value="true"', b'bAllowEmptyEffect" value="false"')
            with open(file_path, 'wb') as f:
                f.write(All)
            AABBCC = 'YtbTâmModAOV'
            
#---------------—------------———----------------
            if IDMODSKIN == '10611' and 'U1B1.xml' in file_path:
                with open(file_path, 'rb') as f:
                    rpl = f.read()
                    rpl = re.sub(
                        br'<Condition id="[^"]+" guid="2e5f463f-105d-4143-b786-e59ea8b34fa2" status="true" />',
                        b'<!-- ' + AABBCC.encode('utf-8') + b' -->', rpl)
                    rpl=rpl.replace(b'<String name="prefab" value="prefab_skill_effects/hero_skill_effects/106_xiaoqiao/xiaoqiao_skill03_cutin" refParamName="" useRefParam="false" />',b'<String name="prefab" value="prefab_skill_effects/hero_skill_effects/106_xiaoqiao/10611/xiaoqiao_skill03_cutin" refParamName="" useRefParam="false" />')
                with open(file_path, 'wb') as f:
                    f.write(rpl)
#---------------—------------———----------------
            if IDMODSKIN == '53702' and 'Change.xml' in file_path and 'ChangeB.xml' in file_path:
                with open(file_path, "rb") as f:
                    All = f.read()
                    All = All.replace(b'/537_Trip/5373_Trip_S_LOD1',b'/537_Trip/53702/5373_Trip_S_LOD1')
                with open(file_path, 'wb') as f:
                    f.write(All)
#---------------—------------———----------------
            if IDMODSKIN == '13213' and 'S1B1.xml' in file_path:
                with open(file_path, "rb") as f:
                    All = f.read()
                
                All = re.sub(
                    rb'(<Track trackName=".*?</Track>)',
                    lambda m: m.group(1) if b"random" in m.group(1).lower() else b'\n'.join(
                        line for line in m.group(1).splitlines() if b"SkinOrAvatar" not in line
                    ),
                    All,
                    flags=re.DOTALL
                )
                
                with open(file_path, "wb") as f:
                    f.write(All)
#---------------—------------———----------------
            if IDMODSKIN == '59901' and 'S1E60.xml' in file_path:
                with open(file_path, 'rb') as f:
                    rpl = f.read().replace(b'<String name="prefabName" value="Prefab_Skill_Effects/Hero_Skill_Effects/599_LvMeng/5991_LvMeng_Shak_Mid" refParamName="" useRefParam="false" />',b'<String name="prefabName" value="Prefab_Skill_Effects/Hero_Skill_Effects/599_LvMeng/59901/5991_LvMeng_Shak_Mid" refParamName="" useRefParam="false" />').replace(b'<String name="prefabName" value="Prefab_Skill_Effects/Hero_Skill_Effects/599_LvMeng/5991_LvMeng_Shak" refParamName="" useRefParam="false" />',b'<String name="prefabName" value="Prefab_Skill_Effects/Hero_Skill_Effects/599_LvMeng/59901/5991_LvMeng_Shak" refParamName="" useRefParam="false" />')
                with open(file_path, 'wb') as f:f.write(rpl)
            if IDMODSKIN == '59902' and 'S1E60.xml' in file_path:
                with open(file_path, 'rb') as f:
                    rpl = f.read().replace(b'<String name="prefabName" value="Prefab_Skill_Effects/Hero_Skill_Effects/599_LvMeng/5991_LvMeng_Shak_Mid" refParamName="" useRefParam="false" />',b'<String name="prefabName" value="Prefab_Skill_Effects/Hero_Skill_Effects/599_LvMeng/59902/5991_LvMeng_Shak_Mid" refParamName="" useRefParam="false" />').replace(b'<String name="prefabName" value="Prefab_Skill_Effects/Hero_Skill_Effects/599_LvMeng/5991_LvMeng_Shak" refParamName="" useRefParam="false" />',b'<String name="prefabName" value="Prefab_Skill_Effects/Hero_Skill_Effects/599_LvMeng/59902/5991_LvMeng_Shak" refParamName="" useRefParam="false" />')
                with open(file_path, 'wb') as f:f.write(rpl)
            if IDMODSKIN == '59901' and 'S1B00.xml' in file_path:
                with open(file_path, 'rb') as f:
                    rpl = f.read().replace(b'59901/59904',b'59901')
                with open(file_path, 'wb') as f:f.write(rpl)
            if IDMODSKIN == '59902' and 'S1B00.xml' in file_path:
                with open(file_path, 'rb') as f:
                    rpl = f.read().replace(b'59902/59904',b'59902')
                with open(file_path, 'wb') as f:f.write(rpl)
#---------------—------------———----------------
            if IDMODSKIN == '17408':
                with open(file_path, 'rb') as f:
                    rpl = f.read()
                    rpl = rpl.replace(b'Project/Assets/Prefabs/', b'').replace(
                        b'Project\\Assets\\Prefabs\\', b'').replace(b'Prefab_Skill_Effects\\Hero_Skill_Effects\\174_YuJi\\17408\\',b'prefab_skill_effects/hero_skill_effects/174_YuJi/17408/')
                with open(file_path, 'wb') as f:
                    f.write(rpl)
#---------------—------------———----------------
            if IDMODSKIN[:3] == '111':
                with open(file_path, 'rb') as f:
                    rpl = f.read().replace(
                    b'<String name="prefabName" value="prefab_skill_effects/hero_skill_effects/111_sunshangxiang/sunshangxiang',
                    b'<String name="prefabName" value="prefab_skill_effects/hero_skill_effects/111_sunshangxiang/'+IDMODSKIN.encode()+b'/sunshangxiang'
        )
                with open(file_path, 'wb') as f:
                    f.write(rpl)
#---------------—------------———----------------
            if IDMODSKIN == '11107' and 'death.xml' not in file_path.lower():
                with open(file_path, 'rb') as f:
                    rpl = f.read().replace(
                    b'<String name="clipName" value="',
                    b'<String name="clipName" value="11107/'
        )
                with open(file_path, 'wb') as f:
                    f.write(rpl)
#---------------—------------———----------------
            if IDMODSKIN == '51504' and 'death.xml' not in file_path.lower():
                with open(file_path, 'rb') as f:
                    rpl = f.read().replace(
                    b'<String name="clipName" value="',
                    b'<String name="clipName" value="51504/'
        )
                with open(file_path, 'wb') as f:
                    f.write(rpl)
#---------------—------------———----------------
            if IDMODSKIN == '12304' and 'death.xml' not in file_path.lower():
                with open(file_path, 'rb') as f:
                    rpl = f.read().replace(
                    b'<String name="clipName" value="',
                    b'<String name="clipName" value="12304/'
        )
                with open(file_path, 'wb') as f:
                    f.write(rpl)
#---------------—------------———----------------
            if IDMODSKIN == '15704' and 'death.xml' not in file_path.lower():
                with open(file_path, 'rb') as f:
                    rpl = f.read().replace(
                    b'<String name="clipName" value="',
                    b'<String name="clipName" value="15704/'
        )
                with open(file_path, 'wb') as f:
                    f.write(rpl)
#---------------—------------———----------------
            if IDMODSKIN[:3] == '173':
                with open(file_path, 'rb') as f:
                    rpl = f.read()

                    rpl = re.sub(
                    b'prefab_skill_effects/hero_skill_effects/173_liyuanfang/' + re.escape(IDMODSKIN.encode()) + b'/Liyuanfang_buff01_spell03', b'prefab_skill_effects/hero_skill_effects/173_liyuanfang/Liyuanfang_buff01_spell03', rpl)

                with open(file_path, 'wb') as f:
                    f.write(rpl)
#---------------—------------———----------------
            if IDMODSKIN == '53802':
                with open(file_path, 'rb') as f:
                    rpl = f.read().replace(
                    b'prefab_skill_effects/hero_skill_effects/538_Iggy/53802/Iggy_Spell3_Circle_01_E',
                    b'prefab_skill_effects/hero_skill_effects/538_Iggy/Iggy_Spell3_Circle_01_E')
                with open(file_path, 'wb') as f:
                    f.write(rpl)
#---------------—------------———----------------
            if IDMODSKIN == '50108' and 'U1E2.xml' in file_path:
                with open(file_path, 'rb') as f:
                    rpl = f.read().replace(b'<String name="prefab" value="Prefab_Skill_Effects/Hero_Skill_Effects/501_TelAnnas/501_Teer_spellC',b'<String name="prefab" value="Prefab_Skill_Effects/Hero_Skill_Effects/501_TelAnnas/50108/501_Teer_spellC').replace(b'        <bool name="bSkipLogicCheck" value="true" refParamName="" useRefParam="false" />',b'')
                with open(file_path, 'wb') as f:
                    f.write(rpl)
#---------------—------------———----------------
            if IDMODSKIN == '14120' and 'S2.xml' in file_path:
                with open(file_path, 'rb') as f:
                    rpl = f.read().replace(b'prefab_skill_effects/hero_skill_effects/141_Diaochan/14120/14112/DiaoChan_attack02_spell03_B',b'prefab_skill_effects/hero_skill_effects/141_Diaochan/14120/DiaoChan_attack02_spell03_B').replace(b'Play_DiaoChan_Skill_B_InUlt_Skin20_Skin20',b'Play_DiaoChan_Skill_B_InUlt_Skin20')
                with open(file_path, 'wb') as f:
                    f.write(rpl)
            if IDMODSKIN == '14120' and 'S214112a.xml' in file_path:
                with open(file_path, 'rb') as f:
                    rpl = f.read().replace(b'prefab_skill_effects/hero_skill_effects/141_Diaochan/14120/14112/DiaoChan_attack02_spell02_a',b'prefab_skill_effects/hero_skill_effects/141_Diaochan/14120/DiaoChan_attack02_spell02_a').replace(b'prefab_skill_effects/hero_skill_effects/141_Diaochan/14120/14112/DiaoChan_attack02_spell02_b',b'prefab_skill_effects/hero_skill_effects/141_Diaochan/14120/DiaoChan_attack02_spell02_b')
                with open(file_path, 'wb') as f:
                    f.write(rpl)
#---------------—------------———----------------
            if IDMODSKIN == '13118' and 'S2.xml' in file_path:
                with open(file_path, 'rb') as f:
                    rpl = f.read().replace(b'<String name="resourceName" value="prefab_skill_effects/hero_skill_effects/Libai_attack_spell02',b'<String name="resourceName" value="prefab_skill_effects/hero_skill_effects/131_LiBai/13118/Libai_attack_spell02.prefab')
                with open(file_path, 'wb') as f:
                    f.write(rpl)
#---------------—------------———----------------
            if IDMODSKIN == '54402' and 'U1B1.xml' in file_path:
                with open(file_path, 'rb') as f:
                    rpl = f.read().replace(b'<String name="prefab" value="prefab_skill_effects/hero_skill_effects/544_Painter/Painter_spell03_cutin" refParamName="" useRefParam="false" />',b'<String name="prefab" value="prefab_skill_effects/hero_skill_effects/544_Painter/54402/Painter_spell03_cutin" refParamName="" useRefParam="false" />')
                with open(file_path, 'wb') as f:
                    f.write(rpl)
#---------------—------------———----------------
            if IDMODSKIN == '54402' and 'U1E0.xml' in file_path:
                with open(file_path, 'rb') as f:
                    rpl = f.read().replace(b'<String name="prefab" value="prefab_skill_effects/hero_skill_effects/544_Painter/Painter_spell03_camera" refParamName="" useRefParam="false" />',b'<String name="prefab" value="prefab_skill_effects/hero_skill_effects/544_Painter/54402/Painter_spell03_camera" refParamName="" useRefParam="false" />')
                with open(file_path, 'wb') as f:
                    f.write(rpl)
#---------------—------------———----------------
            if IDMODSKIN == '11620' and 'S3.xml' in file_path:
                with open(file_path, 'rb') as f:
                    rpl = f.read().replace(b'</Action>',b'  <Track trackName="B" eventType="TriggerParticleTick" guid="154320f4-b071-45d9-a219-60d2d40b643e" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" SkinAvatarFilterType="9">\n      <Event eventName="TriggerParticleTick" time="0.200" isDuration="false" guid="1c18eeae-9938-4123-8768-3dea052a4a06">\n        <TemplateObject name="targetId" objectName="None" id="-1" isTemp="false" refParamName="" useRefParam="false"/>\n        <TemplateObject name="objectSpaceId" objectName="target" id="1" isTemp="false" refParamName="" useRefParam="false"/>\n        <String name="resourceName" value="prefab_skill_effects/component_effects/11620/11620_5/jingke_hurt_spell03_dragona" refParamName="" useRefParam="false"/>\n        <float name="lifeTime" value="3.000" refParamName="" useRefParam="false"/>\n        <Vector3i name="scalingInt" x="10000" y="10000" z="10000" refParamName="" useRefParam="false"/>\n        <bool name="applyActionSpeedToParticle" value="false" refParamName="" useRefParam="false"/>\n      </Event>\n    </Track>\n    <Track trackName="BattleUIAnimationDuration1" eventType="BattleUIAnimationDuration" guid="3d2d80dc-a263-4780-ba18-509858656672" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" SkinAvatarFilterType="9">\n      <Event eventName="BattleUIAnimationDuration" time="0.000" length="2.000" isDuration="true" guid="a080b418-a8cc-40cf-b4d9-c29b57b3730f">\n        <TemplateObject name="targetId" objectName="self" id="0" isTemp="false" refParamName="" useRefParam="false"/>\n        <String name="prefab" value="prefab_skill_effects/component_effects/11620/11620_5/jingke_hurt_spell03_cam" refParamName="" useRefParam="false"/>\n        <String name="animName" value="" refParamName="" useRefParam="false"/>\n      </Event>\n    </Track>\n  </Action>')
                with open(file_path, 'wb') as f:
                    f.write(rpl)
#---------------—------------———----------------
            if IDMODSKIN == '13011' and 'S2B1.xml' in file_path:
                with open(file_path, 'rb') as f: rpl = f.read().replace(b'<TemplateObject name="targetId" id="2" objectName="bullet" isTemp="true" refParamName="" useRefParam="false" />',b'<TemplateObject name="targetId" id="0" objectName="self" isTemp="true" refParamName="" useRefParam="false" />')
                with open(file_path, 'wb') as f:
                    f.write(rpl)
#---------------—------------———----------------
            if IDMODSKIN =='13613' and 'S1E1.xml' in file_path:
                with open(file_path, 'rb') as f: rpl = f.read().replace(b'</Event>\r\n    </Track>\r\n  </Action>\r\n</Project>',b'</Event>\r\n    </Track>\r\n    <Track trackName="Youtuber_You_Mod_Skin" eventType="TriggerParticleTick" guid="daa65ca6-798c-4280-84b3-171fc3a73a82" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Event eventName="TriggerParticleTick" time="0.000" isDuration="false" guid="5f30bc82-d28a-4b25-b3a6-92fc32eac064">\r\n        <TemplateObject name="targetId" objectName="None" id="-1" isTemp="false" refParamName="" useRefParam="false" />\r\n        <TemplateObject name="objectSpaceId" objectName="target" id="1" isTemp="false" refParamName="" useRefParam="false" />\r\n        <String name="resourceName" value="prefab_skill_effects/hero_skill_effects/136_wuzetian/13613/WuZeTian_hurt02" refParamName="" useRefParam="false" />\r\n        <float name="lifeTime" value="0.600" refParamName="" useRefParam="false" />\r\n        <Vector3 name="bindPosOffset" x="0.000" y="1.000" z="0.000" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>\r\n  </Action>\r\n</Project>')
                with open(file_path,'wb') as f: f.write(rpl)
#---------------—------------———----------------
            if IDMODSKIN =='13613' and 'S1E2.xml' in file_path:
                with open(file_path, 'rb') as f: rpl = f.read().replace(b'</Event>\r\n    </Track>\r\n  </Action>\r\n</Project>',b'</Event>\r\n    </Track>\r\n    <Track trackName="Youtuber_You_Mod_Skin" eventType="TriggerParticleTick" guid="daa65ca6-798c-4280-84b3-171fc3a73a82" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Event eventName="TriggerParticleTick" time="0.000" isDuration="false" guid="5f30bc82-d28a-4b25-b3a6-92fc32eac064">\r\n        <TemplateObject name="targetId" objectName="None" id="-1" isTemp="false" refParamName="" useRefParam="false" />\r\n        <TemplateObject name="objectSpaceId" objectName="target" id="1" isTemp="false" refParamName="" useRefParam="false" />\r\n        <String name="resourceName" value="prefab_skill_effects/hero_skill_effects/136_wuzetian/13613/WuZeTian_hurt02" refParamName="" useRefParam="false" />\r\n        <float name="lifeTime" value="0.600" refParamName="" useRefParam="false" />\r\n        <Vector3 name="bindPosOffset" x="0.000" y="1.000" z="0.000" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>\r\n  </Action>\r\n</Project>')
                with open(file_path,'wb') as f: f.write(rpl)
#---------------—------------———----------------
            if IDMODSKIN =='13613' and 'S1E3.xml' in file_path:
                with open(file_path, 'rb') as f: rpl = f.read().replace(b'</Event>\r\n    </Track>\r\n  </Action>\r\n</Project>',b'</Event>\r\n    </Track>\r\n    <Track trackName="Youtuber_You_Mod_Skin" eventType="TriggerParticleTick" guid="daa65ca6-798c-4280-84b3-171fc3a73a82" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Event eventName="TriggerParticleTick" time="0.000" isDuration="false" guid="5f30bc82-d28a-4b25-b3a6-92fc32eac064">\r\n        <TemplateObject name="targetId" objectName="None" id="-1" isTemp="false" refParamName="" useRefParam="false" />\r\n        <TemplateObject name="objectSpaceId" objectName="target" id="1" isTemp="false" refParamName="" useRefParam="false" />\r\n        <String name="resourceName" value="prefab_skill_effects/hero_skill_effects/136_wuzetian/13613/WuZeTian_hurt02" refParamName="" useRefParam="false" />\r\n        <float name="lifeTime" value="0.600" refParamName="" useRefParam="false" />\r\n        <Vector3 name="bindPosOffset" x="0.000" y="1.000" z="0.000" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>\r\n  </Action>\r\n</Project>')

                with open(file_path,'wb') as f: f.write(rpl)
#---------------—------------———----------------
            if IDMODSKIN == '13613' and 'S1B1.xml' in file_path:
                with open(file_path, 'rb') as f: rpl = f.read().replace(b'<Vector3 name="scaling" x="1.300" y="1.000" z="1.000" refParamName="" useRefParam="false" />', b'<Vector3 name="scaling" x="1.000" y="1.000" z="1.000" refParamName="" useRefParam="false" />')
                with open(file_path,'wb') as f: f.write(rpl)
#---------------—------------———----------------
            if IDMODSKIN == '51015' or IDMODSKIN == b'51015':
                with open(file_path, 'rb') as f:
                    rpl = f.read().replace(
                        b'SkinAvatarFilterType="9">', b'SkinAvatarFilterType="8">'
                    ).replace(
                        b'SkinAvatarFilterType="11">', b'SkinAvatarFilterType="9">'
                    ).replace(
                        b'SkinAvatarFilterType="8">', b'SkinAvatarFilterType="11">'
                    ).replace(
                        b'<String name="prefabName" value="Prefab_Skill_Effects/Hero_Skill_Effects/510_Liliana/5101_Fox" refParamName="" useRefParam="false" />',
                        b'<String name="prefabName" value="Prefab_Skill_Effects/Hero_Skill_Effects/510_Liliana/' +
                        IDMODSKIN.encode() + 
                        b'/5101_Fox" refParamName="" useRefParam="false" />'
                    )
            
                with open(file_path,'wb') as f: f.write(rpl)
            if IDMODSKIN == '13210' and 'S1B1.xml' in file_path:
                with open(file_path, 'rb') as f:
                    content = f.read()
                    new_content = content.replace(b'<bool name="useNegateValue" value="true" refParamName="" useRefParam="false" />',b'')
                with open(file_path, 'wb') as f:
                    f.write(new_content)
#---------------—------------———----------------
            if IDMODSKIN[:3] =='510' and 'U11.xml' in file_path:
                with open(file_path, 'rb') as f: rpl = f.read().replace(b'<Track trackName="ChangeActorMeshTick0" eventType="ChangeActorMeshTick" guid="3b065f40-1044-4f90-a2d5-1be4f1a968ee" enabled="false" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">', b'<Track trackName="ChangeActorMeshTick0" eventType="ChangeActorMeshTick" guid="3b065f40-1044-4f90-a2d5-1be4f1a968ee" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">')
                with open(file_path,'wb') as f: f.write(rpl)
#---------------—------------———----------------
            if IDMODSKIN[:3] =='537' and 'S12.xml' in file_path:
                with open(file_path, 'rb') as f:
                    rpl = f.read().replace(b'prefab_skill_effects/hero_skill_effects/537_Trip/'+IDMODSKIN.encode()+b'/Trip_attack_spell01_1prefab_skill_effects/hero_skill_effects/537_Trip/'+IDMODSKIN.encode()+b'/Trip_attack_spell01_1prefab_skill_effects/hero_skill_effects/537_Trip/'+IDMODSKIN.encode()+b'/Trip_attack_spell01_1_S',b'prefab_skill_effects/hero_skill_effects/537_Trip/Trip_attack_spell01_1_S')
                with open(file_path,'wb') as f: f.write(rpl)
#---------------—------------———----------------
            if IDMODSKIN =='53702' and "S13B1.xml" in file_path and "S14B1.xml" in file_path:
                with open(file_path, 'rb') as f:
                    rpl = f.read().replace(b'prefab_skill_effects/hero_skill_effects/537_Trip/53702/Trip_attack_spell01_Indicator',b'prefab_skill_effects/hero_skill_effects/537_Trip/Trip_attack_spell01_Indicator')
                with open(file_path, 'wb') as f:
                    f.write(rpl)
#---------------—------------———----------------
            if IDMODSKIN == '13314':
                with open(file_path, 'rb') as f:
                    rpl = f.read().replace(b'<SkinOrAvatarList id="13314" />',b'')
                with open(file_path, 'wb') as f:
                    f.write(rpl)
            if IDMODSKIN == '13314' and 'skin14E3.xml' in file_path:
                with open(file_path, 'rb') as f:
                    rpl = f.read().replace(
                    b'      </Event>\r\n',b'      </Event>\r\n      <SkinOrAvatarList id="23714" />').replace(b'SkinAvatarFilterType="9">', b'SkinAvatarFilterType="11">')
                with open(file_path, 'wb') as f:
                    f.write(rpl)
            if IDMODSKIN == '13314' and 'U1.xml' in file_path:
                with open(file_path, 'rb') as f:
                    rpl = f.read().replace(b'      </Event>\r\n      \r\n    </Track>\r\n  </Action>\r\n</Project>',b'      </Event>\r\n      <SkinOrAvatarList id="13314" />\n    </Track>\r\n  </Action>\r\n</Project>')
                with open(file_path, 'wb') as f:
                    f.write(rpl)
#---------------—------------———----------------
            if IDMODSKIN == '59802' and 'P0E1.xml' in file_path:
                with open(file_path, 'rb') as f:
                    rpl = f.read().replace(b'<String name="prefabName" value="Prefab_Skill_Effects/Hero_Skill_Effects/598_DaSiKong/59800_DaSiKong_BianShen" refParamName="" useRefParam="false" />',b'<String name="prefabName" value="Prefab_Skill_Effects/Hero_Skill_Effects/598_DaSiKong/59802/59800_DaSiKong_BianShen" refParamName="" useRefParam="false" />')
                with open(file_path, 'wb') as f:
                    f.write(rpl)

#---------------—------------———----------------
            if IDMODSKIN[:3] =='537' and 'Change.xml' in file_path and 'ChangeB.xml' in file_path :
                with open(file_path, 'rb') as f:
                                rpl = f.read().replace(b'537_Trip/',b'537_Trip/53702/')
                with open(file_path,'wb') as f: f.write(rpl)
#---------------—------------———----------------
            if IDMODSKIN =='59702' and 'P1E01.xml' in file_path:
                with open(file_path, 'rb') as f:
                    rpl = f.read().replace(b'e40d96061260" enabled="true"',b'e40d96061260" enabled="false"')
                with open(file_path, 'wb') as f:
                    f.write(rpl)
#---------------—------------———----------------
            if IDMODSKIN =='59702' and 'P2.xml'in file_path:
                with open(file_path, 'rb') as f:
                    rpl = f.read().replace(b'prefab_skill_effects/hero_skill_effects/KuangTie_attack02_spell02A_1',b'prefab_skill_effects/hero_skill_effects/597_kuangtie/59702/KuangTie_attack02_spell02A_1')
                with open(file_path, 'wb') as f:
                    f.write(rpl)
#---------------—------------———----------------
            if IDMODSKIN =='59702' and 'U1.xml'in file_path:
                with open(file_path, 'rb') as f:
                    rpl = f.read().replace(b'<String name="prefab" value="prefab_skill_effects/hero_skill_effects/KuangTie_attack_spell03_1" refParamName="" useRefParam="false" />', b'<String name="prefab" value="prefab_skill_effects/hero_skill_effects/597_kuangtie/59702/KuangTie_attack_spell03_1" refParamName="" useRefParam="false" />')
                with open(file_path, 'wb') as f:
                    f.write(rpl)
#---------------—------------———----------------
            if IDMODSKIN =='59702' and 'U11.xml'in file_path:
                with open(file_path, 'rb') as f:
                    rpl = f.read().replace(b'<String name="prefab" value="prefab_skill_effects/hero_skill_effects/KuangTie_attack02_spell03_1" refParamName="" useRefParam="false" />', b'<String name="prefab" value="prefab_skill_effects/hero_skill_effects/597_kuangtie/59702/KuangTie_attack02_spell03_1" refParamName="" useRefParam="false" />')
                with open(file_path, 'wb') as f:
                    f.write(rpl)
#---------------—------------———----------------
            if IDMODSKIN[:3] == '521':
                with open(file_path, 'rb') as f:
                    rpl = f.read()
                if IDMODSKIN != '52108' and any(x in file_path for x in ['S1B3', 'S1B4']):
                    rpl = rpl.replace(b'Florentino_spell01_bullet03_2"', b'Florentino_spell01_bullet03"')
                    rpl = rpl.replace(b'Florentino_spell01_bullet03_fade_2"', b'Florentino_spell01_bullet03_fade"')
                    rpl = rpl.replace(b'Florentino_spell01_bullet03_2_e"', b'Florentino_spell01_bullet03_e"')
                    rpl = rpl.replace(b'Florentino_spell01_buff01_2"', b'Florentino_spell01_buff01"')
                    rpl = rpl.replace(b'Florentino_spell01_bullet03_3"', b'Florentino_spell01_bullet03"')
                    rpl = rpl.replace(b'Florentino_spell01_bullet03_fade_3"', b'Florentino_spell01_bullet03_fade"')
                    rpl = rpl.replace(b'Florentino_spell01_bullet03_3_e"', b'Florentino_spell01_bullet03_e"')
                    rpl = rpl.replace(b'Florentino_spell01_buff01_3"', b'Florentino_spell01_buff01"')
                with open(file_path, 'wb') as f:
                    f.write(rpl)
#---------------—------------———----------------
            if IDMODSKIN in ['11120','11119'] and 'A1B1.xml' in file_path:
                with open(file_path, 'rb') as f: sec = f.read().replace(b'</Action>', b'    <Track trackName="SpawnLiteObjDuration0" eventType="SpawnLiteObjDuration" guid="\xe9\x83\x91\xe5\x87\xaf\xe6\x98\x8e" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true" SkinAvatarFilterType="11">\n      <Event eventName="SpawnLiteObjDuration" time="0.000" length="5.000" isDuration="true" guid="6d868a6f-8ee5-477f-b215-8168ab03ce28">\n        <String name="OutputLiteBulletName" value="111a1b1" refParamName="" useRefParam="false"/>\n        <uint name="ConfigID" value="11100" refParamName="" useRefParam="false"/>\n        <TemplateObject name="ReferenceID" objectName="self" id="0" isTemp="false" refParamName="" useRefParam="false"/>\n        <TemplateObject name="TargetID" id="1" objectName="target" isTemp="false" refParamName="" useRefParam="false"/>\n      </Event>\n      <SkinOrAvatarList id="11119"/>\n      <SkinOrAvatarList id="11120"/>\n    </Track>')
                with open(file_path,'wb') as f: f.write(sec)
            if IDMODSKIN in ['11120','11119'] and 'A1b2.xml' in file_path:
                with open(file_path, 'rb') as f: sec = f.read().replace(b'</Action>', b'    <Track trackName="SpawnLiteObjDuration0" eventType="SpawnLiteObjDuration" guid="\xe9\x83\x91\xe5\x87\xaf\xe6\x98\x8e" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true" SkinAvatarFilterType="11">\n      <Event eventName="SpawnLiteObjDuration" time="0.000" length="5.000" isDuration="true" guid="6d868a6f-8ee5-477f-b215-8168ab03ce28">\n        <String name="OutputLiteBulletName" value="111a1b2" refParamName="" useRefParam="false"/>\n        <uint name="ConfigID" value="11101" refParamName="" useRefParam="false"/>\n        <TemplateObject name="ReferenceID" objectName="self" id="0" isTemp="false" refParamName="" useRefParam="false"/>\n        <TemplateObject name="TargetID" id="1" objectName="target" isTemp="false" refParamName="" useRefParam="false"/>\n      </Event>\n      <SkinOrAvatarList id="11119"/>\n      <SkinOrAvatarList id="11120"/>\n    </Track>')
                with open(file_path,'wb') as f: f.write(sec)
            if IDMODSKIN in ['11120','11119'] and 'A2B1.xml' in file_path:
                with open(file_path, 'rb') as f: sec = f.read().replace(b'</Action>', b'    <Track trackName="SpawnLiteObjDuration0" eventType="SpawnLiteObjDuration" guid="\xe9\x83\x91\xe5\x87\xaf\xe6\x98\x8e" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true" SkinAvatarFilterType="11">\n      <Event eventName="SpawnLiteObjDuration" time="0.000" length="5.000" isDuration="true" guid="6d868a6f-8ee5-477f-b215-8168ab03ce28">\n        <String name="OutputLiteBulletName" value="111a2b2" refParamName="" useRefParam="false"/>\n        <uint name="ConfigID" value="11103" refParamName="" useRefParam="false"/>\n        <TemplateObject name="ReferenceID" objectName="self" id="0" isTemp="false" refParamName="" useRefParam="false"/>\n        <TemplateObject name="TargetID" id="1" objectName="target" isTemp="false" refParamName="" useRefParam="false"/>\n      </Event>\n      <SkinOrAvatarList id="11119"/>\n      <SkinOrAvatarList id="11120"/>\n    </Track>')
                with open(file_path,'wb') as f: f.write(sec)
            if IDMODSKIN in ['11120','11119'] and 'A4B1.xml' in file_path:
                with open(file_path, 'rb') as f: sec = f.read().replace(b'</Action>', b'    <Track trackName="SpawnLiteObjDuration0" eventType="SpawnLiteObjDuration" guid="\xe9\x83\x91\xe5\x87\xaf\xe6\x98\x8e" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true" SkinAvatarFilterType="11">\n      <Event eventName="SpawnLiteObjDuration" time="0.000" length="5.000" isDuration="true" guid="6d868a6f-8ee5-477f-b215-8168ab03ce28">\n        <String name="OutputLiteBulletName" value="111a4b1" refParamName="" useRefParam="false"/>\n        <uint name="ConfigID" value="11104" refParamName="" useRefParam="false"/>\n        <TemplateObject name="ReferenceID" objectName="self" id="0" isTemp="false" refParamName="" useRefParam="false"/>\n        <TemplateObject name="TargetID" id="1" objectName="target" isTemp="false" refParamName="" useRefParam="false"/>\n      </Event>\n      <SkinOrAvatarList id="11119"/>\n      <SkinOrAvatarList id="11120"/>\n    </Track>')
                with open(file_path,'wb') as f: f.write(sec)
            if IDMODSKIN in ['11120','11119'] and 'A4B1.xml' in file_path:
                with open(file_path, 'rb') as f: sec = f.read().replace(b'</Action>', b'    <Track trackName="SpawnLiteObjDuration0" eventType="SpawnLiteObjDuration" guid="\xe9\x83\x91\xe5\x87\xaf\xe6\x98\x8e" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true" SkinAvatarFilterType="11">\n      <Event eventName="SpawnLiteObjDuration" time="0.000" length="5.000" isDuration="true" guid="6d868a6f-8ee5-477f-b215-8168ab03ce28">\n        <String name="OutputLiteBulletName" value="111a4b1" refParamName="" useRefParam="false"/>\n        <uint name="ConfigID" value="11104" refParamName="" useRefParam="false"/>\n        <TemplateObject name="ReferenceID" objectName="self" id="0" isTemp="false" refParamName="" useRefParam="false"/>\n        <TemplateObject name="TargetID" id="1" objectName="target" isTemp="false" refParamName="" useRefParam="false"/>\n      </Event>\n      <SkinOrAvatarList id="11119"/>\n      <SkinOrAvatarList id="11120"/>\n    </Track>')
                with open(file_path,'wb') as f: f.write(sec)
            if IDMODSKIN in ['11120','11119'] and 'A4b2.xml' in file_path:
                with open(file_path, 'rb') as f: sec = f.read().replace(b'</Action>', b'    <Track trackName="SpawnLiteObjDuration0" eventType="SpawnLiteObjDuration" guid="\xe9\x83\x91\xe5\x87\xaf\xe6\x98\x8e" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true" SkinAvatarFilterType="11">\n      <Event eventName="SpawnLiteObjDuration" time="0.000" length="5.000" isDuration="true" guid="6d868a6f-8ee5-477f-b215-8168ab03ce28">\n        <String name="OutputLiteBulletName" value="111a4b2" refParamName="" useRefParam="false"/>\n        <uint name="ConfigID" value="11105" refParamName="" useRefParam="false"/>\n        <TemplateObject name="ReferenceID" objectName="self" id="0" isTemp="false" refParamName="" useRefParam="false"/>\n        <TemplateObject name="TargetID" id="1" objectName="target" isTemp="false" refParamName="" useRefParam="false"/>\n      </Event>\n      <SkinOrAvatarList id="11119"/>\n      <SkinOrAvatarList id="11120"/>\n    </Track>')
                with open(file_path,'wb') as f: f.write(sec)
#---------------—------------———----------------
            if IDMODSKIN == '10603' and 'death.xml' not in file_path.lower():
                with open(file_path, 'rb') as f:
                    rpl = f.read().replace(
                    b'<String name="clipName" value="',
                    b'<String name="clipName" value="10603/'
        )
                with open(file_path, 'wb') as f:
                    f.write(rpl)
#---------------—------------———----------------
            if IDMODSKIN[:3] == '540' and 'U1B1.xml' in file_path:
                with open(file_path, 'rb') as f:
                    rpl = f.read().replace(b'<String name="prefabName" value="prefab_skill_effects/hero_skill_effects/540_Bright/5401_Bright_God" refParamName="" useRefParam="false" />',b'<String name="prefabName" value="prefab_skill_effects/hero_skill_effects/540_Bright/'+ IDMODSKIN.encode() + b'/5401_Bright_God" refParamName="" useRefParam="false" />')
                with open(file_path, 'wb') as f:
                    f.write(rpl)
#---------------—------------———----------------
            if IDMODSKIN == '54402' and 'A4B1.xml' in file_path:
                with open(file_path, 'rb') as f:
                    rpl = f.read()
                    rpl = rpl.replace(b'prefab_skill_effects/hero_skill_effects/544_Painter/54402/Painter_Atk4_blue',b'prefab_skill_effects/hero_skill_effects/544_Painter/Painter_Atk4_blue').replace(b'prefab_skill_effects/hero_skill_effects/544_Painter/54402/Painter_Atk4_red',b'prefab_skill_effects/hero_skill_effects/544_Painter/Painter_Atk4_red')
                with open(file_path, 'wb') as f:
                    f.write(rpl)
#---------------—------------———----------------
            if IDMODSKIN == '15412' and 'P12E2.xml' in file_path:
                with open(file_path, 'rb') as f:
                    rpl = f.read()
                    rpl = rpl.replace(b'Prefab_Skill_Effects/Hero_Skill_Effects/154_HuaMuLan/15412/15413_HuaMuLan_Red', b'Prefab_Skill_Effects/Hero_Skill_Effects/154_HuaMuLan/15413_HuaMuLan_Red')
                with open(file_path, 'wb') as f:
                    f.write(rpl)
            if IDMODSKIN == '15412' and 'U1B0.xml' in file_path:
                with open(file_path, 'rb') as f:
                    rpl = f.read()
                    rpl = rpl.replace(b'<String name="prefab" value="Prefab_Skill_Effects/Hero_Skill_Effects/154_HuaMuLan/huamulan_Skill_pingmu" refParamName="" useRefParam="false" />', b'<String name="prefab" value="Prefab_Skill_Effects/Hero_Skill_Effects/154_HuaMuLan/15412/huamulan_Skill_pingmu" refParamName="" useRefParam="false" />')
                with open(file_path, 'wb') as f:
                    f.write(rpl)
            if IDMODSKIN == '15412' and 'T1B0.xml' in file_path:
                with open(file_path, 'rb') as f:
                    rpl = f.read()
                    rpl = rpl.replace(b'<String name="prefab" value="Prefab_Skill_Effects/Hero_Skill_Effects/154_HuaMuLan/huamulan_Skill_pingmu" refParamName="" useRefParam="false" />', b'<String name="prefab" value="Prefab_Skill_Effects/Hero_Skill_Effects/154_HuaMuLan/15412/huamulan_Skill_pingmu" refParamName="" useRefParam="false" />')
                with open(file_path, 'wb') as f:
                    f.write(rpl)
#---------------—------------———----------------
            if IDMODSKIN == '19015' and 'U1B0.xml' in file_path:
                with open(file_path, 'rb') as f: rpl = f.read().replace(b'<bool name="useNegateValue" value="true" refParamName="" useRefParam="false" />',b'').replace(b'<String name="prefab" value="prefab_skill_effects/hero_skill_effects/190_ZhuGeLiang/19015/19009/Zhugeliang_attack01_spell03_UI" refParamName="" useRefParam="false" />',b'<String name="prefab" value="prefab_skill_effects/hero_skill_effects/190_ZhuGeLiang/19015/Zhugeliang_attack01_spell03_UI" refParamName="" useRefParam="false" />').replace(b'<Track trackName="19015" eventType="CheckSkinIdVirtualTick" guid="b66d59b2-b5f0-4365-870a-a57357f5df93" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">',b'<Track trackName="19015" eventType="CheckSkinIdTick" guid="b66d59b2-b5f0-4365-870a-a57357f5df93" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">').replace(b'<Event eventName="CheckSkinIdTick" time="0.000" isDuration="false" guid="17c9207c-19af-4061-9d63-109437868f7d">',b'<Event eventName="CheckSkinIdTick" time="0.000" isDuration="false" guid="17c9207c-19af-4061-9d63-109437868f7d">')
                with open(file_path,'wb') as f: f.write(rpl)
            if IDMODSKIN  == '19015':
                with open(file_path, 'rb') as f:
                    rpl = f.read()
                rpl = rpl.replace(b'SkinAvatarFilterType="9">',b'SkinAvatarFilterType="8">').replace(b'SkinAvatarFilterType="11">',b'SkinAvatarFilterType="9">').replace(b'SkinAvatarFilterType="8">',b'SkinAvatarFilterType="11">')
                rpl = re.sub(
                    br'<int name="skinId" value="19015" refParamName="" useRefParam="false"\s*/?>',
                    b'<int name="skinId" value="19000" refParamName="" useRefParam="false" />',
                    rpl
                )
                rpl = re.sub(
                    br'<SkinOrAvatarList\s+id="19015"\s*/?>',
                    b'<SkinOrAvatarList id="99999" />',
                    rpl
                )
                with open(file_path, 'wb') as f:
                    f.write(rpl)

#---------------—------------———----------------
            if IDMODSKIN =='52007':
                if phukien == "do":
                    with open(file_path, 'rb') as f:
                        rpl = f.read().replace(b'prefab_skill_effects/hero_skill_effects/520_Veres/52007/',b'prefab_skill_effects/component_effects/52007/5200402/')
                    with open(file_path, 'wb') as f:
                        f.write(rpl)
                elif phukien == "xanh":
                    with open(file_path, 'rb') as f:
                        rpl = f.read().replace(
                b'prefab_skill_effects/hero_skill_effects/520_Veres/52007/',
                b'prefab_skill_effects/component_effects/52007/5200401/'
            )
                    with open(file_path, 'wb') as f:
                        f.write(rpl)
#---------------—------------———----------------
            if IDMODSKIN =='13015' and 'A4.xml' in file_path:
                with open(file_path, 'rb') as f: rpl = f.read().replace(b'<bool name="useNegateValue" value="true"', b'<bool name="useNegateValue" value="false"')
                with open(file_path,'wb') as f: f.write(rpl)
#---------------—------------———----------------
            if IDMODSKIN == '15013' and'S2.xml'in file_path:
                with open(file_path, 'rb') as f:
                    rpl = f.read()
                    rpl = (rpl
    .replace(
        b'<int name="skinId" value="' + IDCHECK.encode() + b'" refParamName="" useRefParam="false" />\r\n        <bool name="bEqual" value="false" refParamName="" useRefParam="false" />\r\n        <bool name="bSkipLogicCheck" value="true" refParamName="" useRefParam="false" />',
        b'<int name="skinId" value="' + b'9999' + b'" refParamName="" useRefParam="false" />\r\n        <<bool name="bEqual" value="false" refParamName="" useRefParam="false" />>\r\n        <bool name="bSkipLogicCheck" value="true" refParamName="" useRefParam="false" />'
    )
    .replace(
        b'<int name="skinId" value="' + IDCHECK.encode() + b'" refParamName="" useRefParam="false" />\r\n        <bool name="bSkipLogicCheck" value="true" refParamName="" useRefParam="false" />',
        b'<int name="skinId" value="' + b'9999' + b'" refParamName="" useRefParam="false" />\r\n        <bool name="bEqual" value="false" refParamName="" useRefParam="false" />\r\n        <bool name="bSkipLogicCheck" value="true" refParamName="" useRefParam="false" />'
    )
    .replace(
        b'<int name="skinId" value="' + b'9999' + b'" refParamName="" useRefParam="false" />\r\n        <<bool name="bEqual" value="false" refParamName="" useRefParam="false" />>\r\n        <bool name="bSkipLogicCheck" value="true" refParamName="" useRefParam="false" />',
        b'<int name="skinId" value="' + b'9999' + b'" refParamName="" useRefParam="false" />\r\n        <bool name="bSkipLogicCheck" value="true" refParamName="" useRefParam="false" />'
    )
    .replace(
        b'<Condition id="14" guid="b73050c0-0afc-4e3b-98e2-6ffe12d3d489" status="true" />\r\n      <Condition id="15" guid="84b2cbba-51cc-4673-adab-a3624a854953" status="false" />',
        b'<Condition id="15" guid="84b2cbba-51cc-4673-adab-a3624a854953" status="false" />'
    )
    .replace(
        b'<Condition id="14" guid="b73050c0-0afc-4e3b-98e2-6ffe12d3d489" status="true" />\r\n      <Event eventName="CheckActorPositionDuration"',
        b'<Event eventName="CheckActorPositionDuration"'
    )
    .replace(
        b'<Condition id="14" guid="b73050c0-0afc-4e3b-98e2-6ffe12d3d489" status="true" />\r\n      <Event eventName="HitTriggerTick"',
        b'<Event eventName="HitTriggerTick"'
    )
    .replace(
        b'<Condition id="37" guid="173653f1-8aaf-47ee-84a3-92cf343f6711" status="false" />\r\n      <Condition id="14" guid="b73050c0-0afc-4e3b-98e2-6ffe12d3d489" status="true" />\r\n      <Event eventName="SetAnimationParamsTick"',
        b'<Condition id="37" guid="173653f1-8aaf-47ee-84a3-92cf343f6711" status="false" />\r\n      <Event eventName="SetAnimationParamsTick"'
    )
).replace(
    b'    <Track trackName="SetAnimationParamsTick0" eventType="SetAnimationParamsTick" guid="ecc440c2-8021-4dc0-958a-b812278d2407" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Condition id="37" guid="173653f1-8aaf-47ee-84a3-92cf343f6711" status="true" />\r\n      <Condition id="-1" guid="" status="true" />\r\n      <Condition id="41" guid="a8a348b5-aa7c-4d2d-a19c-297310da390f" status="true" />\r\n      <Condition id="14" guid="b73050c0-0afc-4e3b-98e2-6ffe12d3d489" status="true" />\r\n      <Event eventName="SetAnimationParamsTick" time="0.000" isDuration="false" guid="f2d3828f-602b-4092-9a2c-7c139d7be8c4">\r\n        <TemplateObject name="targetId" objectName="self" id="0" isTemp="false" refParamName="" useRefParam="false" />\r\n        <Array name="floatNames" refParamName="" useRefParam="false" type="String">\r\n          <String value="RandomSpell2" />\r\n        </Array>\r\n        <Array name="floatValues" refParamName="" useRefParam="false" type="float">\r\n          <float value="0.500" />\r\n        </Array>\r\n      </Event>\r\n    </Track>', 
    b'    <Track trackName="SetAnimationParamsTick0" eventType="SetAnimationParamsTick" guid="ecc440c2-8021-4dc0-958a-b812278d2407" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Condition id="37" guid="173653f1-8aaf-47ee-84a3-92cf343f6711" status="true" />\r\n      <Condition id="-1" guid="" status="true" />\r\n      <Condition id="41" guid="a8a348b5-aa7c-4d2d-a19c-297310da390f" status="true" />\r\n      <Condition id="14" guid="b73050c0-0afc-4e3b-98e2-6ffe12d3d489" status="true" />\r\n      <Event eventName="SetAnimationParamsTick" time="0.000" isDuration="false" guid="f2d3828f-602b-4092-9a2c-7c139d7be8c4">\r\n        <TemplateObject name="targetId" objectName="self" id="0" isTemp="false" refParamName="" useRefParam="false" />\r\n        <Array name="floatNames" refParamName="" useRefParam="false" type="String">\r\n          <String value="RandomSpell2" />\r\n        </Array>\r\n        <Array name="floatValues" refParamName="" useRefParam="false" type="float">\r\n          <float value="0.500" />\r\n        </Array>\r\n      </Event>\r\n    </Track>\r\n    <Track trackName="SetAnimationParamsTick0" eventType="SetAnimationParamsTick" guid="ecc440c2-8021-4dc0-958a-b812278d2407" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Condition id="37" guid="173653f1-8aaf-47ee-84a3-92cf343f6711" status="true" />\r\n      <Condition id="-1" guid="" status="true" />\r\n      <Condition id="14" guid="b73050c0-0afc-4e3b-98e2-6ffe12d3d489" status="false" />\r\n      <Event eventName="SetAnimationParamsTick" time="0.000" isDuration="false" guid="f2d3828f-602b-4092-9a2c-7c139d7be8c4">\r\n        <TemplateObject name="targetId" objectName="self" id="0" isTemp="false" refParamName="" useRefParam="false" />\r\n        <Array name="floatNames" refParamName="" useRefParam="false" type="String">\r\n          <String value="RandomSpell2" />\r\n        </Array>\r\n        <Array name="floatValues" refParamName="" useRefParam="false" type="float">\r\n          <float value="0.500" />\r\n        </Array>\r\n      </Event>\r\n    </Track>'
)
                with open(file_path, 'wb') as f:
                    f.write(rpl)
#---------------—------------———----------------
            if IDMODSKIN == '13706' and 'S4.xml':
                with open(file_path, 'rb') as f:
                    rpl = f.read()
                    rpl = rpl.replace(b'<String name="prefab" value="prefab_skill_effects/hero_skill_effects/137_simayi/SiMaYi_SkillHud" refParamName="" useRefParam="false" />',b'<String name="prefab" value="prefab_skill_effects/hero_skill_effects/137_simayi/13706/SiMaYi_SkillHud" refParamName="" useRefParam="false" />')
                with open(file_path, 'wb') as f:
                    f.write(rpl)
#---------------—------------———----------------
            if IDMODSKIN == '13011' and 'S2.xml' in file_path:
                with open(file_path, 'rb') as f: rpl = f.read().replace(b'    <Track trackName="T2skin\xe7\xbe\x8e\xe6\x9c\xaftrue" eventType="CheckSkinIdTick" guid="1d2453a9-f234-4489-90f4-dde12f642d17" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Event eventName="CheckSkinIdTick" time="0.000" isDuration="false" guid="77eedf3b-88d2-466f-b13c-d8e44504dc8d">\r\n        <TemplateObject name="targetId" objectName="self" id="0" isTemp="false" refParamName="" useRefParam="false" />\r\n        <int name="skinId" value="13011" refParamName="" useRefParam="false" />\r\n        <bool name="bSkipLogicCheck" value="true" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>',b'    <Track trackName="T2skin\xe7\xbe\x8e\xe6\x9c\xaftrue" eventType="CheckHeroIdTick" guid="1d2453a9-f234-4489-90f4-dde12f642d17" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Event eventName="CheckHeroIdTick" time="0.000" isDuration="false" guid="77eedf3b-88d2-466f-b13c-d8e44504dc8d">\r\n        <TemplateObject name="targetId" objectName="self" id="0" isTemp="false" refParamName="" useRefParam="false" />\r\n        <int name="heroId" value="130" refParamName="" useRefParam="false" />\r\n        <bool name="bSkipLogicCheck" value="true" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>')
                with open(file_path, 'wb') as f:
                    f.write(rpl)
#-----------------------------------------------
            if IDMODSKIN == '13011' and 'S21.xml' in file_path:
                with open(file_path, 'rb') as f:
                    rpl = f.read() 
                    rpl = rpl.replace(b'    <Track trackName="T2skin\xe7\xbe\x8e\xe6\x9c\xaftrue" eventType="CheckSkinIdTick" guid="753f3471-d461-40e5-b0d9-9305c2d4615d" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Event eventName="CheckSkinIdTick" time="0.000" isDuration="false" guid="d302841f-faf8-4336-9895-50109a87ca31">\r\n        <TemplateObject name="targetId" objectName="self" id="0" isTemp="false" refParamName="" useRefParam="false" />\r\n        <int name="skinId" value="13011" refParamName="" useRefParam="false" />\r\n        <bool name="bSkipLogicCheck" value="true" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>',b'    <Track trackName="T2skin\xe7\xbe\x8e\xe6\x9c\xaftrue" eventType="CheckHeroIdTick" guid="753f3471-d461-40e5-b0d9-9305c2d4615d" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Event eventName="CheckHeroIdTick" time="0.000" isDuration="false" guid="d302841f-faf8-4336-9895-50109a87ca31">\r\n        <TemplateObject name="targetId" objectName="self" id="0" isTemp="false" refParamName="" useRefParam="false" />\r\n        <int name="heroId" value="130" refParamName="" useRefParam="false" />\r\n        <bool name="bSkipLogicCheck" value="true" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>').replace(b"""<Track trackName="TriggerParticleTick1" eventType="TriggerParticleTick" guid="a07302eb-cb3b-4146-9996-d018f92247aa" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">""",b"""<Track trackName="TriggerParticleTick1" eventType="TriggerParticleTick" guid="a07302eb-cb3b-4146-9996-d018f92247aa" enabled="false" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">""").replace(b"GongBenWuZang_attack01_spell01_2",b"GongBenWuZang_attack01_spell01_1")
                with open(file_path, 'wb') as f:
                    f.write(rpl)
#-----------------------------------------------
            if IDMODSKIN == '13011' and 'S22.xml' in file_path:
                with open(file_path, 'rb') as f: rpl = f.read().replace(b'    <Track trackName="T2skin\xe7\xbe\x8e\xe6\x9c\xaftrue" eventType="CheckSkinIdTick" guid="cea185dc-6db5-47e8-9a5f-fbf0f2aabacb" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Event eventName="CheckSkinIdTick" time="0.000" isDuration="false" guid="df5f721f-659b-4ce7-8ae0-a869b902e35e">\r\n        <TemplateObject name="targetId" objectName="self" id="0" isTemp="false" refParamName="" useRefParam="false" />\r\n        <int name="skinId" value="13011" refParamName="" useRefParam="false" />\r\n        <bool name="bSkipLogicCheck" value="true" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>',b'    <Track trackName="T2skin\xe7\xbe\x8e\xe6\x9c\xaftrue" eventType="CheckHeroIdTick" guid="cea185dc-6db5-47e8-9a5f-fbf0f2aabacb" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Event eventName="CheckHeroIdTick" time="0.000" isDuration="false" guid="df5f721f-659b-4ce7-8ae0-a869b902e35e">\r\n        <TemplateObject name="targetId" objectName="self" id="0" isTemp="false" refParamName="" useRefParam="false" />\r\n        <int name="heroId" value="130" refParamName="" useRefParam="false" />\r\n        <bool name="bSkipLogicCheck" value="true" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>').replace(b"""<Track trackName="TriggerParticleTick1" eventType="TriggerParticleTick" guid="a07302eb-cb3b-4146-9996-d018f92247aa" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">""",b"""<Track trackName="TriggerParticleTick1" eventType="TriggerParticleTick" guid="a07302eb-cb3b-4146-9996-d018f92247aa" enabled="false" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">""").replace(b"GongBenWuZang_attack01_spell01_3",b"GongBenWuZang_attack01_spell01_2")
                with open(file_path, 'wb') as f:
                    f.write(rpl)
#-----------------------------------------------
            if IDMODSKIN == '13011' and 'S2.xml' not in file_path and 'S21.xml' not in file_path and 'S22.xml' not in file_path:
                with open(file_path, 'rb') as f:
                    rpl = f.read().replace(b'        <int name="skinId" value="13011" refParamName="" useRefParam="false" />\r\n        <bool name="bEqual" value="false" refParamName="" useRefParam="false" />\r\n        <bool name="bSkipLogicCheck" value="true" refParamName="" useRefParam="false" />',b'        <int name="skinId" value="13011" refParamName="" useRefParam="false" />>\r\n        <<bool name="bEqual" value="false" refParamName="" useRefParam="false" />>\r\n        <bool name="bSkipLogicCheck" value="true" refParamName="" useRefParam="false" />').replace(b'        <int name="skinId" value="13011" refParamName="" useRefParam="false" />\r\n        <bool name="bSkipLogicCheck" value="true" refParamName="" useRefParam="false" />',b'        <int name="skinId" value="13011" refParamName="" useRefParam="false" />\r\n        <bool name="bEqual" value="false" refParamName="" useRefParam="false" />\r\n        <bool name="bSkipLogicCheck" value="true" refParamName="" useRefParam="false" />').replace(b'        <int name="skinId" value="13011" refParamName="" useRefParam="false" />>\r\n        <<bool name="bEqual" value="false" refParamName="" useRefParam="false" />>\r\n        <bool name="bSkipLogicCheck" value="true" refParamName="" useRefParam="false" />',b'        <int name="skinId" value="13011" refParamName="" useRefParam="false" />\r\n        <bool name="bSkipLogicCheck" value="true" refParamName="" useRefParam="false" />')
                with open(file_path, 'wb') as f:
                    f.write(rpl)
#---------------—------------———----------------
            if IDMODSKIN =='13015' and 'A4.xml' in file_path:
                with open(file_path, 'rb') as f:
                    rpl = f.read().replace(b'\n        <bool name="useNegateValue" value="true" refParamName="" useRefParam="false" />',b'')
                with open(file_path, 'wb') as f:
                    f.write(rpl)

#---------------—------------———----------------
            if IDMODSKIN[:3] =='524' and 'A1E9.xml' in file_path:
                with open(file_path, 'rb') as f:
                    rpl = f.read().replace(b'prefab_skill_effects/hero_skill_effects/524_Capheny/'+IDMODSKIN.encode()+b'/Atk1_FireRange_Plus',b'prefab_skill_effects/hero_skill_effects/524_Capheny/Atk1_FireRange_Plus')
                with open(file_path, 'wb') as f:
                    f.write(rpl)
#---------------—------------———----------------
            if IDMODSKIN == '13112'and'P1E5.xml' in file_path:
                with open(file_path, 'rb') as f: rpl = f.read().replace(b'Bone_Blade',b'Bip001 Prop1').replace(b'Bone_Weapon01',b'Bip001 Prop1')
                with open(file_path,'wb') as f: f.write(rpl)
            if IDMODSKIN == '13111'and'P1E5.xml' in file_path:
                with open(file_path, 'rb') as f: rpl = f.read().replace(b'Bone_Blade',b'Bone_Weapon01').replace(b'Bip001 Prop1',b'Bone_Weapon01')
                with open(file_path,'wb') as f: f.write(rpl)
            if IDMODSKIN == '13116'and'P1E5.xml' in file_path:
                with open(file_path, 'rb') as f: rpl = f.read().replace(b'Bone_Blade',b'Bip001 Prop1').replace(b'Bone_Weapon01',b'Bip001 Prop1')
                with open(file_path,'wb') as f: f.write(rpl)
#---------------—------------———----------------
            if file_path == 'Death.xml':
                with open(file_path, 'r',encoding='utf8') as f:
                    sec = f.read().replace('</Action>', '    <Track trackName="CommonSkillProcessBarDuration0" eventType="CommonSkillProcessBarDuration" guid="8f26cacc-ee15-4857-94aa-ffccd0b1a87a" enabled="true" refParamName="" useRefParam="false" r="0.933" g="0.000" b="1.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\n      <Event eventName="CommonSkillProcessBarDuration" time="0.000" length="4.500" isDuration="true">\n        <TemplateObject name="targetId" objectName="self" id="0" isTemp="false" refParamName="" useRefParam="false"/>\n        <int name="width" value="0" refParamName="" useRefParam="false"/>\n        <bool name="useCurrentSkillName" value="false" refParamName="" useRefParam="false"/>\n        <String name="skillNameTextKey" value="YtbTâmModAOV" refParamName="" useRefParam="false"/>\n      </Event>\n    </Track>\n  </Action>')
                with open(file_path, 'w',encoding='utf8') as f:
                    f.write(sec)  
#---------------—------------———----------------
            if IDMODSKIN =='11119' and 'A1B1.xml' in file_path:
                with open(file_path, 'rb') as f: rpl = f.read().replace(b'<String name="prefabName" value="prefab_characters/commonempty" refParamName="" useRefParam="false" />', b'<String name="prefabName" value="prefab_skill_effects/hero_skill_effects/111_sunshangxiang/11119/sunshangxiang_fly_01b" refParamName="" useRefParam="false" />\r\n        <Vector3i name="translation" x="0" y="750" z="0" refParamName="" useRefParam="false" />')
                with open(file_path,'wb') as f: 
                    f.write(rpl)
#---------------—------------———----------------
                if IDMODSKIN =='11119' and 'A2B1.xml' in file_path:
                    with open(file_path, 'rb') as f: rpl = f.read().replace(b'<String name="prefabName" value="prefab_characters/commonempty" refParamName="" useRefParam="false" />',b'<String name="prefabName" value="prefab_skill_effects/hero_skill_effects/111_sunshangxiang/11119/sunshangxiang_fly_01b" refParamName="" useRefParam="false" />\r\n        <Vector3i name="translation" x="0" y="700" z="0" refParamName="" useRefParam="false" />')
                    with open(file_path,'wb') as f: 
                        f.write(rpl)
#---------------—------------———----------------
            if IDMODSKIN == '13112' and 'P1E5.xml'in file_path:
                with open(file_path, 'rb') as f: rpl = f.read().replace(b'Bone_Blade',b'Bip001 Prop1').replace(b'Bone_Weapon01',b'Bip001 Prop1')
                with open(file_path,'wb') as f: f.write(rpl)
#---------------—------------———----------------
            if IDMODSKIN == '13111' and 'P1E5.xml'in file_path:
                with open(file_path, 'rb') as f: rpl = f.read().replace(b'Bone_Blade',b'Bone_Weapon01').replace(b'Bip001 Prop1',b'Bone_Weapon01')
                with open(file_path,'wb') as f: f.write(rpl)
#---------------—------------———----------------
            if IDMODSKIN == '13116' and 'P1E5.xml'in file_path:
                with open(file_path, 'rb') as f: rpl = f.read().replace(b'Bone_Blade',b'Bip001 Prop1').replace(b'Bone_Weapon01',b'Bip001 Prop1')
                with open(file_path,'wb') as f: f.write(rpl)
#-----------------------------------------------
            if IDMODSKIN =='14111' and 'S1.xml' in file_path:
                with open(file_path, 'rb') as f: rpl = f.read().replace(b'<Event eventName="PlayAnimDuration" time="0.000" length="1.167" isDuration="true" guid="8c3310a3-4c0c-44ce-9f4e-6273c7d05d98">',b'<Event eventName="PlayAnimDuration" time="0.000" length="1.700" isDuration="true" guid="8c3310a3-4c0c-44ce-9f4e-6273c7d05d98">').replace(b'      </Event>\r\n    </Track>\r\n  </Action>\r\n</Project>',b'      </Event>\r\n    </Track>\r\n    <Track trackName="NOBUFF" eventType="CheckSkillCombineConditionTick" guid="MOD-BY-Tran_Thi_Nhung-FIX-14111-NOBUFF" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Condition id="7" guid="2a6ab8c3-3cba-4002-95c5-b9f3cfa702ef" status="true" />\r\n      <Event eventName="CheckSkillCombineConditionTick" time="0.000" isDuration="false" guid="Tran_Thi_Nhung">\r\n        <TemplateObject name="targetId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <int name="skillCombineId" value="141920" refParamName="" useRefParam="false" />\r\n        <Enum name="checkOPType" value="1" refParamName="" useRefParam="false" />\r\n        <int name="skillCombineLevel" value="1" refParamName="" useRefParam="false" />\r\n        <bool name="bCopyActorUseSrcActor" value="true" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>\r\n    <Track trackName="BUFF" eventType="CheckSkillCombineConditionTick" guid="MOD-BY-Tran_Thi_Nhung-FIX-14111-BUFF" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Condition id="7" guid="2a6ab8c3-3cba-4002-95c5-b9f3cfa702ef" status="true" />\r\n      <Event eventName="CheckSkillCombineConditionTick" time="0.000" isDuration="false" guid="Tran_Thi_Nhung">\r\n        <TemplateObject name="targetId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <int name="skillCombineId" value="141920" refParamName="" useRefParam="false" />\r\n        <Enum name="checkOPType" value="5" refParamName="" useRefParam="false" />\r\n        <int name="skillCombineLevel" value="1" refParamName="" useRefParam="false" />\r\n        <bool name="bCopyActorUseSrcActor" value="true" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>\r\n    <Track trackName="NOBUFF" eventType="TriggerParticle" guid="MOD-BY-Tran_Thi_Nhung" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Condition id="7" guid="2a6ab8c3-3cba-4002-95c5-b9f3cfa702ef" status="true" />\r\n      <Condition id="0" guid="MOD-BY-Tran_Thi_Nhung-FIX-14111-NOBUFF" status="true" />\r\n      <Event eventName="TriggerParticle" time="0.000" length="1.700" isDuration="true" guid="Tran_Thi_Nhung">\r\n        <TemplateObject name="targetId" id="-1" objectName="None" isTemp="false" refParamName="" useRefParam="false" />\r\n        <TemplateObject name="objectSpaceId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <String name="resourceName" value="Prefab_Skill_Effects/Hero_Skill_Effects/141_DiaoChan/14111/14111_spell01_A.prefab" refParamName="" useRefParam="false" />\r\n        <Vector3 name="bindPosOffset" x="0.000" y="0.500" z="1.200" refParamName="" useRefParam="false" />\r\n        <Vector3i name="scalingInt" x="10000" y="10000" z="10000" refParamName="" useRefParam="false" />\r\n        <String name="syncAnimationName" value="" refParamName="" useRefParam="false" />\r\n        <String name="customTagName" value="" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>\r\n    <Track trackName="BUFF" eventType="TriggerParticle" guid="MOD-BY-Tran_Thi_Nhung" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Condition id="7" guid="2a6ab8c3-3cba-4002-95c5-b9f3cfa702ef" status="true" />\r\n      <Condition id="0" guid="MOD-BY-Tran_Thi_Nhung-FIX-14111-BUFF" status="true" />\r\n      <Event eventName="TriggerParticle" time="0.000" length="1.700" isDuration="true" guid="Tran_Thi_Nhung">\r\n        <TemplateObject name="targetId" id="-1" objectName="None" isTemp="false" refParamName="" useRefParam="false" />\r\n        <TemplateObject name="objectSpaceId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <String name="resourceName" value="Prefab_Skill_Effects/Hero_Skill_Effects/141_DiaoChan/14111/14111_spell01_B.prefab" refParamName="" useRefParam="false" />\r\n        <Vector3 name="bindPosOffset" x="0.000" y="0.500" z="1.200" refParamName="" useRefParam="false" />\r\n        <Vector3i name="scalingInt" x="10000" y="10000" z="10000" refParamName="" useRefParam="false" />\r\n        <String name="syncAnimationName" value="" refParamName="" useRefParam="false" />\r\n        <String name="customTagName" value="" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>\r\n  </Action>\r\n</Project>')
                with open(file_path, 'wb') as f:
                    f.write(rpl)
            if IDMODSKIN =='14111' and 'S1B1.xml' in file_path:
                with open(file_path, 'rb') as f: rpl = f.read().replace(b'    <Track trackName="CheckSkinIdVirtualTick0" eventType="CheckSkinIdVirtualTick" guid="8f286ccb-5124-446a-a1b1-b72f7a82dd09" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Event eventName="CheckSkinIdVirtualTick" time="0.000" isDuration="false" guid="3a8b83a4-4375-4c7f-9ba1-e9a1459303c3">\r\n        <TemplateObject name="targetId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <int name="skinId" value="14118" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>\r\n    <Track trackName="TriggerParticle0" eventType="TriggerParticle" guid="f4847356-eaf3-4669-b9ad-ba78401b4c5b" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Event eventName="TriggerParticle" time="0.000" length="1.600" isDuration="true" guid="554fdc14-4ac7-4685-8160-9950a8be03f1">\r\n        <TemplateObject name="targetId" id="2" objectName="bullet" isTemp="true" refParamName="" useRefParam="false" />\r\n        <String name="resourceName" value="prefab_skill_effects/hero_skill_effects/141_Diaochan/14111/diaochan_attack_spell01" refParamName="" useRefParam="false" />\r\n        <Vector3 name="bindPosOffset" x="0.000" y="0.500" z="1.200" refParamName="" useRefParam="false" />\r\n        <Vector3i name="scalingInt" x="10000" y="10000" z="10000" refParamName="" useRefParam="false" />\r\n        <String name="syncAnimationName" value="" refParamName="" useRefParam="false" />\r\n        <String name="customTagName" value="" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>\r\n    <Track trackName="CheckSkillCombineConditionTick0" eventType="CheckSkillCombineConditionTick" guid="5ccf0732-2aa3-4f64-b2f9-bd6de2e6afd9" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Condition id="3" guid="8f286ccb-5124-446a-a1b1-b72f7a82dd09" status="true" />\r\n      <Event eventName="CheckSkillCombineConditionTick" time="0.000" isDuration="false" guid="66fc6cfc-7779-4faa-8a7d-d761e49984ed">\r\n        <TemplateObject name="targetId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <int name="skillCombineId" value="141921" refParamName="" useRefParam="false" />\r\n        <Enum name="checkOPType" value="3" refParamName="" useRefParam="false" />\r\n        <int name="skillCombineLevel" value="1" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>\r\n    <Track trackName="18\xe7\x9a\xae\xe8\x82\xa4\xe5\xbc\x80\xe5\xa4\xa7\xe4\xbb\xa5\xe5\x90\x8e\xe5\x8f\x91\xe6\x8b\x9b" eventType="TriggerParticle" guid="32288ab6-074b-4d86-820d-8ce3dc813663" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Condition id="5" guid="5ccf0732-2aa3-4f64-b2f9-bd6de2e6afd9" status="true" />\r\n      <Event eventName="TriggerParticle" time="0.000" length="1.600" isDuration="true" guid="905c16af-30f5-43da-88dd-0d98ae56640c">\r\n        <TemplateObject name="targetId" id="-1" objectName="None" isTemp="false" refParamName="" useRefParam="false" />\r\n        <TemplateObject name="objectSpaceId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <String name="resourceName" value="prefab_skill_effects/hero_skill_effects/141_Diaochan/14111/14118_spell01_B" refParamName="" useRefParam="false" />\r\n        <Vector3i name="scalingInt" x="10000" y="10000" z="10000" refParamName="" useRefParam="false" />\r\n        <String name="syncAnimationName" value="" refParamName="" useRefParam="false" />\r\n        <String name="customTagName" value="" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>'
,b'    <Track trackName="CheckHeroIdTick0" eventType="CheckHeroIdTick" guid="MOD-BY-Tran_Thi_Nhung-FIX-14111" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Event eventName="CheckHeroIdTick" time="0.000" isDuration="false" guid="3a8b83a4-4375-4c7f-9ba1-e9a1459303c3">\r\n        <TemplateObject name="targetId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <int name="heroId" value="141" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>\r\n    <Track trackName="NOBUFF" eventType="CheckSkillCombineConditionTick" guid="MOD-BY-Tran_Thi_Nhung-FIX-14111-NOBUFF" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Condition id="3" guid="MOD-BY-Tran_Thi_Nhung-FIX-14111" status="true" />\r\n      <Event eventName="CheckSkillCombineConditionTick" time="0.000" isDuration="false" guid="Tran_Thi_Nhung">\r\n        <TemplateObject name="targetId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <int name="skillCombineId" value="141920" refParamName="" useRefParam="false" />\r\n        <Enum name="checkOPType" value="1" refParamName="" useRefParam="false" />\r\n        <int name="skillCombineLevel" value="1" refParamName="" useRefParam="false" />\r\n        <bool name="bCopyActorUseSrcActor" value="true" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>\r\n    <Track trackName="BUFF" eventType="CheckSkillCombineConditionTick" guid="MOD-BY-Tran_Thi_Nhung-FIX-14111-BUFF" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Condition id="3" guid="MOD-BY-Tran_Thi_Nhung-FIX-14111" status="true" />    \t\r\n      <Event eventName="CheckSkillCombineConditionTick" time="0.000" isDuration="false" guid="Tran_Thi_Nhung">\r\n        <TemplateObject name="targetId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <int name="skillCombineId" value="141920" refParamName="" useRefParam="false" />\r\n        <Enum name="checkOPType" value="5" refParamName="" useRefParam="false" />\r\n        <int name="skillCombineLevel" value="1" refParamName="" useRefParam="false" />\r\n        <bool name="bCopyActorUseSrcActor" value="true" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>\r\n    <Track trackName="NOBUFF" eventType="TriggerParticle" guid="MOD-BY-Tran_Thi_Nhung" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Condition id="3" guid="MOD-BY-Tran_Thi_Nhung-FIX-14111" status="true" />    \t\r\n      <Condition id="0" guid="MOD-BY-Tran_Thi_Nhung-FIX-14111-NOBUFF" status="true" />\r\n      <Event eventName="TriggerParticle" time="0.000" length="1.600" isDuration="true" guid="Tran_Thi_Nhung">\r\n        <TemplateObject name="targetId" id="2" objectName="bullet" isTemp="true" refParamName="" useRefParam="false" />\r\n        <String name="resourceName" value="Prefab_Skill_Effects/Hero_Skill_Effects/141_DiaoChan/14111/diaochan_attack_spell01.prefab" refParamName="" useRefParam="false" />\r\n        <Vector3 name="bindPosOffset" x="0.000" y="0.500" z="1.200" refParamName="" useRefParam="false" />\r\n        <Vector3i name="scalingInt" x="10000" y="10000" z="10000" refParamName="" useRefParam="false" />\r\n        <String name="syncAnimationName" value="" refParamName="" useRefParam="false" />\r\n        <String name="customTagName" value="" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>\r\n    <Track trackName="BUFF" eventType="TriggerParticle" guid="MOD-BY-Tran_Thi_Nhung" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Condition id="3" guid="MOD-BY-Tran_Thi_Nhung-FIX-14111" status="true" />    \t\r\n      <Condition id="0" guid="MOD-BY-Tran_Thi_Nhung-FIX-14111-BUFF" status="true" />\r\n      <Event eventName="TriggerParticle" time="0.000" length="1.600" isDuration="true" guid="Tran_Thi_Nhung">\r\n        <TemplateObject name="targetId" id="2" objectName="bullet" isTemp="true" refParamName="" useRefParam="false" />\r\n        <String name="resourceName" value="Prefab_Skill_Effects/Hero_Skill_Effects/141_DiaoChan/14111/diaochan_attack_spell01_S.prefab" refParamName="" useRefParam="false" />\r\n        <Vector3 name="bindPosOffset" x="0.000" y="0.500" z="1.200" refParamName="" useRefParam="false" />\r\n        <Vector3i name="scalingInt" x="10000" y="10000" z="10000" refParamName="" useRefParam="false" />\r\n        <String name="syncAnimationName" value="" refParamName="" useRefParam="false" />\r\n        <String name="customTagName" value="" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>')
                with open(file_path, 'wb') as f:
                    f.write(rpl)
            if IDMODSKIN =='14111' and 'S1B2.xml' in file_path:
                with open(file_path, 'rb') as f: rpl = f.read().replace(b'    <Track trackName="14118\xe6\xa3\x80\xe6\xb5\x8b" eventType="CheckSkinIdTick" guid="4cd2db1b-e00b-4b71-916f-e9c0b1b21d07" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Event eventName="CheckSkinIdTick" time="0.000" isDuration="false" guid="03d1e9c3-a23a-4ead-aaf8-7cd333b318b4">\r\n        <TemplateObject name="targetId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <int name="skinId" value="14118" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>\r\n    <Track trackName="TriggerParticleTick0" eventType="TriggerParticleTick" guid="c6a98de8-8f76-4f6b-8f80-1bcd17efbc2c" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Condition id="4" guid="4cd2db1b-e00b-4b71-916f-e9c0b1b21d07" status="false" />\r\n      <Event eventName="TriggerParticleTick" time="0.000" isDuration="false" guid="a4c68b42-3e79-4aa1-8af2-451b9e077923">\r\n        <TemplateObject name="targetId" id="2" objectName="bullet" isTemp="true" refParamName="" useRefParam="false" />\r\n        <TemplateObject name="objectSpaceId" id="2" objectName="bullet" isTemp="true" refParamName="" useRefParam="false" />\r\n        <String name="resourceName" value="prefab_skill_effects/hero_skill_effects/141_Diaochan/14111/diaochan_attack_spell01_1" refParamName="" useRefParam="false" />\r\n        <float name="lifeTime" value="2.000" refParamName="" useRefParam="false" />\r\n        <Vector3i name="scalingInt" x="10000" y="10000" z="10000" refParamName="" useRefParam="false" />\r\n        <bool name="applyActionSpeedToAnimation" value="true" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>\r\n    <Track trackName="BUFF" eventType="CheckSkillCombineConditionTick" guid="b37bdadd-b8c9-440e-9ea0-2705476cc057" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Condition id="4" guid="4cd2db1b-e00b-4b71-916f-e9c0b1b21d07" status="true" />\r\n      <Event eventName="CheckSkillCombineConditionTick" time="0.000" isDuration="false" guid="a88e4c5e-b65e-4bbf-851d-1bd898e9f7d0">\r\n        <TemplateObject name="targetId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <int name="skillCombineId" value="141920" refParamName="" useRefParam="false" />\r\n        <Enum name="checkOPType" value="5" refParamName="" useRefParam="false" />\r\n        <int name="skillCombineLevel" value="1" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>\r\n    <Track trackName="TriggerParticleTick0" eventType="TriggerParticleTick" guid="685ff200-95ad-4b43-8471-83a9572b039b" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Condition id="6" guid="b37bdadd-b8c9-440e-9ea0-2705476cc057" status="false" />\r\n      <Event eventName="TriggerParticleTick" time="0.000" isDuration="false" guid="9d4c8390-89f0-4ed4-96f3-18dc7af1d978">\r\n        <TemplateObject name="targetId" id="2" objectName="bullet" isTemp="true" refParamName="" useRefParam="false" />\r\n        <TemplateObject name="objectSpaceId" id="2" objectName="bullet" isTemp="true" refParamName="" useRefParam="false" />\r\n        <String name="resourceName" value="prefab_skill_effects/hero_skill_effects/141_Diaochan/14111/diaochan_attack_spell01_1" refParamName="" useRefParam="false" />\r\n        <float name="lifeTime" value="2.000" refParamName="" useRefParam="false" />\r\n        <Vector3i name="scalingInt" x="10000" y="10000" z="10000" refParamName="" useRefParam="false" />\r\n        <bool name="applyActionSpeedToAnimation" value="true" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>\r\n    <Track trackName="TriggerParticleTick0" eventType="TriggerParticleTick" guid="90043ce2-7a80-4e53-b87d-944fe49f7924" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Condition id="6" guid="b37bdadd-b8c9-440e-9ea0-2705476cc057" status="true" />\r\n      <Event eventName="TriggerParticleTick" time="0.000" isDuration="false" guid="96d74687-1dc4-4407-ab36-663b1eb619b2">\r\n        <TemplateObject name="targetId" id="2" objectName="bullet" isTemp="true" refParamName="" useRefParam="false" />\r\n        <TemplateObject name="objectSpaceId" id="2" objectName="bullet" isTemp="true" refParamName="" useRefParam="false" />\r\n        <String name="resourceName" value="prefab_skill_effects/hero_skill_effects/141_Diaochan/14111/diaochan_attack_spell01_1_S" refParamName="" useRefParam="false" />\r\n        <float name="lifeTime" value="2.000" refParamName="" useRefParam="false" />\r\n        <Vector3i name="scalingInt" x="10000" y="10000" z="10000" refParamName="" useRefParam="false" />\r\n        <bool name="applyActionSpeedToAnimation" value="true" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>', b'    <Track trackName="CheckHeroIdTick0" eventType="CheckHeroIdTick" guid="MOD-BY-Tran_Thi_Nhung-FIX-14111" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Event eventName="CheckHeroIdTick" time="0.000" isDuration="false" guid="03d1e9c3-a23a-4ead-aaf8-7cd333b318b4">\r\n        <TemplateObject name="targetId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <int name="heroId" value="141" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>\r\n    <Track trackName="NOBUFF" eventType="CheckSkillCombineConditionTick" guid="MOD-BY-Tran_Thi_Nhung-FIX-14111-NOBUFF" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Condition id="3" guid="MOD-BY-Tran_Thi_Nhung-FIX-14111" status="true" />\r\n      <Event eventName="CheckSkillCombineConditionTick" time="0.000" isDuration="false" guid="Tran_Thi_Nhung">\r\n        <TemplateObject name="targetId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <int name="skillCombineId" value="141920" refParamName="" useRefParam="false" />\r\n        <Enum name="checkOPType" value="1" refParamName="" useRefParam="false" />\r\n        <int name="skillCombineLevel" value="1" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>\r\n     <Track trackName="BUFF" eventType="CheckSkillCombineConditionTick" guid="MOD-BY-Tran_Thi_Nhung-FIX-14111-BUFF" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Condition id="3" guid="MOD-BY-Tran_Thi_Nhung-FIX-14111" status="true" />     \t\r\n      <Event eventName="CheckSkillCombineConditionTick" time="0.000" isDuration="false" guid="Tran_Thi_Nhung">\r\n        <TemplateObject name="targetId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <int name="skillCombineId" value="141920" refParamName="" useRefParam="false" />\r\n        <Enum name="checkOPType" value="5" refParamName="" useRefParam="false" />\r\n        <int name="skillCombineLevel" value="1" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>\r\n    <Track trackName="NOBUFF" eventType="TriggerParticleTick" guid="MOD-BY-Tran_Thi_Nhung" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Condition id="3" guid="MOD-BY-Tran_Thi_Nhung-FIX-14111" status="true" />\r\n      <Condition id="0" guid="MOD-BY-Tran_Thi_Nhung-FIX-14111-NOBUFF" status="true"/>\r\n      <Event eventName="TriggerParticleTick" time="0.000" isDuration="false" guid="Tran_Thi_Nhung">\r\n        <TemplateObject name="targetId" id="2" objectName="bullet" isTemp="true" refParamName="" useRefParam="false" />\r\n        <TemplateObject name="objectSpaceId" id="2" objectName="bullet" isTemp="true" refParamName="" useRefParam="false" />\r\n        <String name="resourceName" value="Prefab_Skill_Effects/Hero_Skill_Effects/141_DiaoChan/14111/diaochan_attack_spell01_1.prefab" refParamName="" useRefParam="false" />\r\n        <float name="lifeTime" value="2.000" refParamName="" useRefParam="false" />\r\n        <Vector3i name="scalingInt" x="10000" y="10000" z="10000" refParamName="" useRefParam="false" />\r\n        <bool name="applyActionSpeedToAnimation" value="true" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>\r\n    <Track trackName="BUFF" eventType="TriggerParticleTick" guid="MOD-BY-Tran_Thi_Nhung" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Condition id="3" guid="MOD-BY-Tran_Thi_Nhung-FIX-14111" status="true" />    \t\r\n      <Condition id="0" guid="MOD-BY-Tran_Thi_Nhung-FIX-14111-BUFF" status="true" />\r\n      <Event eventName="TriggerParticleTick" time="0.000" isDuration="false" guid="Tran_Thi_Nhung">\r\n        <TemplateObject name="targetId" id="2" objectName="bullet" isTemp="true" refParamName="" useRefParam="false" />\r\n        <TemplateObject name="objectSpaceId" id="2" objectName="bullet" isTemp="true" refParamName="" useRefParam="false" />\r\n        <String name="resourceName" value="Prefab_Skill_Effects/Hero_Skill_Effects/141_DiaoChan/14111/diaochan_attack_spell01_1_S.prefab" refParamName="" useRefParam="false" />\r\n        <String name="resourceName2" value="Prefab_Skill_Effects/Hero_Skill_Effects/141_DiaoChan/14111/diaochan_attack_spell01_1_S_B.prefab" refParamName="" useRefParam="false" />\r\n        <float name="lifeTime" value="2.000" refParamName="" useRefParam="false" />\r\n        <Vector3i name="scalingInt" x="10000" y="10000" z="10000" refParamName="" useRefParam="false" />\r\n        <bool name="applyActionSpeedToAnimation" value="true" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>')
                with open(file_path, 'wb') as f:
                    f.write(rpl)
#-----------------------------------------------
            if IDMODSKIN =='15015' and 'U1.xml' in file_path:
                with open(file_path, 'rb') as f:
                    rpl = f.read()
                    rpl=re.sub(b'"resourceName" value="(.*?)"', b'"resourceName" value="Mod_By_Tran_Thi_Nhung_Mod_15015"', rpl).replace(b'  </Action>',b'    <Track trackName="TriggerParticleTick0" eventType="TriggerParticleTick" guid="57036c14-d685-4131-9f93-9a4c65ac9929" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Condition id="28" guid="c0b9dcbe-c83f-4a57-b203-70a202308416" status="true" />\r\n      <Event eventName="TriggerParticleTick" time="0.067" isDuration="false" guid="ca1ffb7f-b6a8-4320-b14a-f4f2b6e5084d">\r\n        <TemplateObject name="targetId" id="-1" objectName="None" isTemp="false" refParamName="" useRefParam="false" />\r\n       <TemplateObject name="objectSpaceId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <int name="frameRate" value="120" refParamName="" useRefParam="false" />\r\n        <bool name="bUseTargetSkinEffect" value="true" refParamName="" useRefParam="false"/>\r\n        <String name="resourceName" value="prefab_skill_effects/hero_skill_effects/150_hanxin/15015/hanxin_attack03_spell01.prefab" refParamName="" useRefParam="false" />\r\n        <Vector3i name="scalingInt" x="10000" y="10000" z="10000" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>\r\n    <Track trackName="TriggerParticleTick0" eventType="TriggerParticleTick" guid="5d4a923f-56f2-4670-ac7e-1c6692324f59" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Event eventName="TriggerParticleTick" time="0.367" isDuration="false" guid="b596efb1-714d-4626-bfed-5d53a538b7e1">\r\n       <TemplateObject name="targetId" id="-1" objectName="None" isTemp="false" refParamName="" useRefParam="false" />\r\n        <TemplateObject name="objectSpaceId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <int name="frameRate" value="120" refParamName="" useRefParam="false" />\r\n        <bool name="bUseTargetSkinEffect" value="true" refParamName="" useRefParam="false"/>\r\n        <String name="resourceName" value="prefab_skill_effects/hero_skill_effects/150_hanxin/15015/hanxin_attack03_spell02.prefab" refParamName="" useRefParam="false" />\r\n        <Vector3i name="scalingInt" x="10000" y="10000" z="10000" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>\r\n    <Track trackName="TriggerParticleTick0" eventType="TriggerParticleTick" guid="aaf02147-7a99-4c02-99d8-89b6e16fc5a3" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Condition id="28" guid="c0b9dcbe-c83f-4a57-b203-70a202308416" status="true" />\r\n      <Event eventName="TriggerParticleTick" time="0.967" isDuration="false" guid="7fdcb80c-b70e-4561-994b-eaf31b8f27d0">\r\n        <TemplateObject name="targetId" id="-1" objectName="None" isTemp="false" refParamName="" useRefParam="false" />\r\n        <TemplateObject name="objectSpaceId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <int name="frameRate" value="120" refParamName="" useRefParam="false" />\r\n        <bool name="bUseTargetSkinEffect" value="true" refParamName="" useRefParam="false"/>\r\n        <String name="resourceName" value="prefab_skill_effects/hero_skill_effects/150_hanxin/15015/hanxin_attack03_spell03.prefab" refParamName="" useRefParam="false" />\r\n        <Vector3i name="scalingInt" x="10000" y="10000" z="10000" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>\r\n    <Track trackName="TriggerParticleTick0" eventType="TriggerParticleTick" guid="888f2edc-d3a7-4a18-bb56-647f9678cf07" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Event eventName="TriggerParticleTick" time="0.466" isDuration="false" guid="b6eb7044-1230-47fe-92c3-e017d0694f3e">\r\n        <TemplateObject name="targetId" id="-1" objectName="None" isTemp="false" refParamName="" useRefParam="false" />\r\n        <TemplateObject name="objectSpaceId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <int name="frameRate" value="120" refParamName="" useRefParam="false" />\r\n        <bool name="bUseTargetSkinEffect" value="true" refParamName="" useRefParam="false"/>\r\n        <String name="resourceName" value="prefab_skill_effects/hero_skill_effects/150_hanxin/15015/hanxin_attack03_spell04.prefab" refParamName="" useRefParam="false" />\r\n        <Vector3i name="scalingInt" x="10000" y="10000" z="10000" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>\r\n    <Track trackName="TriggerParticle1" eventType="TriggerParticle" guid="4ba448f3-97b2-4763-b956-63a0dcecf458" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Condition id="39" guid="6e38b810-2c03-4c25-9331-fd09a03cb2e2" status="true" />\r\n      <Event eventName="TriggerParticle" time="0.100" length="2.000" isDuration="true" guid="0c29a8c5-d7cd-4b8e-b7c8-02ad44aeb5c3">\r\n        <TemplateObject name="targetId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <int name="frameRate" value="120" refParamName="" useRefParam="false" />\r\n        <bool name="bUseTargetSkinEffect" value="true" refParamName="" useRefParam="false"/>\r\n       <String name="resourceName" value="prefab_skill_effects/hero_skill_effects/150_hanxin/15015/hanxin_attack03_spell01a.prefab" refParamName="" useRefParam="false" />\r\n        <Vector3i name="scalingInt" x="10000" y="10000" z="10000" refParamName="" useRefParam="false" />\r\n        <String name="syncAnimationName" value="" refParamName="" useRefParam="false" />\r\n        <String name="customTagName" value="" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>\r\n    <Track trackName="TriggerParticleTick0" eventType="TriggerParticleTick" guid="128c3dc2-2ceb-4c50-845d-540db4c2ea24" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Condition id="39" guid="6e38b810-2c03-4c25-9331-fd09a03cb2e2" status="true" />\r\n      <Event eventName="TriggerParticleTick" time="0.967" isDuration="false" guid="f863d83d-0a9f-4e86-b389-3403a9eef30e">\r\n        <TemplateObject name="targetId" id="-1" objectName="None" isTemp="false" refParamName="" useRefParam="false" />\r\n        <TemplateObject name="objectSpaceId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <int name="frameRate" value="120" refParamName="" useRefParam="false" />\r\n        <bool name="bUseTargetSkinEffect" value="true" refParamName="" useRefParam="false"/>\r\n        <String name="resourceName" value="prefab_skill_effects/hero_skill_effects/150_hanxin/15015/hanxin_attack03_spell03a.prefab" refParamName="" useRefParam="false" />\r\n        <Vector3i name="scalingInt" x="10000" y="10000" z="10000" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>\r\n    <Track trackName="SetAnimationParamsDuration0" eventType="SetAnimationParamsDuration" guid="ec1e4f35-2611-4b30-872c-da1c818e2c29" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n     <Condition id="28" guid="e89a739d-ad18-433f-83c7-ed477652dd8f" status="true" />\r\n      <Event eventName="SetAnimationParamsDuration" time="0.000" length="2.330" isDuration="true" guid="6fb1f212-a88d-4671-8904-8b3def9cda85">\r\n        <TemplateObject name="targetId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <Array name="floatNames" refParamName="" useRefParam="false" type="String">\r\n          <String value="spell3pa" />\r\n        </Array>\r\n        <Array name="floatValues" refParamName="" useRefParam="false" type="float">\r\n          <float value="1.000" />\r\n        </Array>\r\n      </Event>\r\n    </Track>\r\n  </Action>')
                with open(file_path, 'wb') as f:
                    f.write(rpl)
#---------------—------------———----------------
            if IDMODSKIN == '15015' and 'U1.xml' not in file_path:
                with open(file_path, 'rb') as f: rpl = f.read().replace(b'<int name="skinId" value="15015" refParamName="" useRefParam="false" />',b'<int name="skinId" value="15015" refParamName="" useRefParam="false" />\n        <bool name="bEqual" value="false" refParamName="" useRefParam="false" />')
                with open(file_path, 'wb') as f:
                    f.write(rpl)
#---------------—------------———----------------
            if IDMODSKIN =='15012' and 'U1.xml' in file_path:
                with open(file_path, 'rb') as f: rpl = f.read().replace(b'<String name="prefab" value="prefab_skill_effects/hero_skill_effects/150_Hanxin_spellC_01"',b'<String name="prefab" value="prefab_skill_effects/hero_skill_effects/150_hanxin/15012/150_Hanxin_spellC_01"')
                with open(file_path, 'wb') as f:
                    f.write(rpl)
#---------------—------------———----------------
            if IDMODSKIN =='15216':
                with open(file_path, 'rb') as f: rpl = f.read().replace(b'SkinAvatarFilterType="9">',b'SkinAvatarFilterType="8">').replace(b'SkinAvatarFilterType="11">',b'SkinAvatarFilterType="9">').replace(b'SkinAvatarFilterType="8">',b'SkinAvatarFilterType="11">')
                with open(file_path,'wb') as f: f.write(rpl)
#---------------—------------———----------------
            if IDMODSKIN =='15217':
                with open(file_path, 'rb') as f: rpl = f.read().replace(b'<String name="prefabName" value="Prefab_Skill_Effects/Hero_Skill_Effects/152_WangZhaoJun/15218_WangZhaoJunM" refParamName="" useRefParam="false" />',b'<String name="prefabName" value="Prefab_Skill_Effects/Hero_Skill_Effects/152_WangZhaoJun/15217/15218_WangZhaoJunM" refParamName="" useRefParam="false" />')
                with open(file_path,'wb') as f: f.write(rpl)
#---------------—------------———----------------
            if IDMODSKIN == '13311':
                with open(file_path, 'rb') as f: rpl = f.read().replace(b'prefab_skill_effects/hero_skill_effects/133_direnjie/13311/',b'prefab_skill_effects/component_effects/13311/13311_5/').replace(b'"Play_DiRenJie_Attack_1"', b'"Play_DiRenJie_Attack_1_Skin11_AW2"').replace(b'"Play_DiRenJie_Voice_Short"', b'"Play_DiRenJie_Voice_Short_Skin11_AW3"').replace(b'"Play_DiRenJie_Attack_Hit_1"', b'"Play_DiRenJie_Attack_Hit_1_Skin11_AW2"').replace(b'"Play_DiRenJie_Skill_A"', b'"Play_DiRenJie_Skill_A_Skin11_AW2"').replace(b'"Play_DiRenJie_Voice_Anger"', b'"Play_DiRenJie_Voice_Anger_Skin11_AW3"').replace(b'"Play_DiRenJie_Skill_A_Hit"', b'"Play_DiRenJie_Skill_A_Hit_Skin11_AW2"').replace(b'"Play_DiRenJie_Attack_Hit_2"', b'"Play_DiRenJie_Attack_Hit_2_Skin11_AW2"').replace(b'"Play_DiRenJie_Skill_B"', b'"Play_DiRenJie_Skill_B_Skin11_AW2"').replace(b'"Play_DiRenJie_Skill_B_Hit"', b'"Play_DiRenJie_Skill_B_Hit_Skin11_AW2"').replace(b'"Play_DiRenJie_Card_Red"', b'"Play_DiRenJie_Card_Red_Skin11_AW2"').replace(b'"Play_DiRenJie_Card_Blue"', b'"Play_DiRenJie_Card_Blue_Skin11_AW2"').replace(b'"Play_DiRenJie_Card_Yellow"', b'"Play_DiRenJie_Card_Yellow_Skin11_AW2"').replace(b'"Play_DiRenJie_Voice_Dead"', b'"Play_DiRenJie_Voice_Dead_Skin11_AW3"').replace(b'"Play_DiRenJie_Voice_Skill_B"', b'"Play_DiRenJie_Voice_Skill_B_Skin11_AW3"').replace(b'"Play_DiRenJie_Skill_C"', b'"Play_DiRenJie_Skill_C_Skin11_AW2"').replace(b'"Play_DiRenJie_Voice_Skill_C"', b'"Play_DiRenJie_Voice_Skill_C_Skin11_AW3"').replace(b'"Play_DiRenJie_Skill_C_Hit"', b'"Play_DiRenJie_Skill_C_Hit_Skin11_AW2"')
                with open(file_path,'wb') as f: 
                    f.write(rpl)
#---------------—------------———----------------
            if IDMODSKIN == '13311' and 'U1.xml' in file_path:
                if phukienv == "dov":
                    with open(file_path, 'rb') as f:
                        rpl = f.read().replace(b'prefab_skill_effects/component_effects/13311/13311_5/',b'prefab_skill_effects/component_effects/13311/1331102/')
                    with open(file_path, 'wb') as f:
                        f.write(rpl)
#---------------—------------———----------------
            if IDMODSKIN == '16707':
                with open(file_path, 'rb') as f: rpl = f.read().replace(b'prefab_skill_effects/hero_skill_effects/167_wukong/16707/',b'prefab_skill_effects/component_effects/16707/16707_5/').replace(b'"Play_Back_WuKong"', b'"Play_Back_WuKong_Skin7_AW3"').replace(b'"Play_WuKong_Attack_1"', b'"Play_WuKong_Attack_1_Skin7_AW3"').replace(b'"Play_WuKong_VO_Short"', b'"Play_WuKong_VO_Short_Skin7_AW4"').replace(b'"Play_WuKong_Attack_Hit_1"', b'"Play_WuKong_Attack_Hit_1_Skin7_AW3"').replace(b'"Play_WuKong_Attack_2"', b'"Play_WuKong_Attack_2_Skin7_AW3"').replace(b'"Play_WuKong_VO_Anger"', b'"Play_WuKong_VO_Anger_Skin7_AW4"').replace(b'"Play_WuKong_Skill_Passive_Hit1"', b'"Play_WuKong_Skill_Passive_Hit1_Skin7_AW3"').replace(b'"Play_WuKong_Skill_Passive_Hit2"', b'"Play_WuKong_Skill_Passive_Hit2_Skin7_AW3"').replace(b'"Play_WuKong_Skill_Passive_Hit3"', b'"Play_WuKong_Skill_Passive_Hit3_Skin7_AW3"').replace(b'"Play_WuKong_Skill_B_2"', b'"Play_WuKong_Skill_B_2_Skin7_AW3"').replace(b'"Play_WuKong_Skill_B_Hit"', b'"Play_WuKong_Skill_B_Hit_Skin7_AW3"').replace(b'"Play_WuKong_VO_Dead"', b'"Play_WuKong_VO_Dead_Skin7_AW4"').replace(b'"Play_WuKong_Skill_A_2"', b'"Play_WuKong_Skill_A_2_Skin7_AW3"').replace(b'"Play_WuKong_Skill_A_Hit"', b'"Play_WuKong_Skill_A_Hit_Skin7_AW3"').replace(b'"Play_WuKong_Skill_A_1"', b'"Play_WuKong_Skill_A_1_Skin7_AW3"').replace(b'"Play_WuKong_VO_Skill_A"', b'"Play_WuKong_VO_Skill_A_Skin7_AW4"').replace(b'"Play_WuKong_Skill_A_Run"', b'"Play_WuKong_Skill_A_Run_Skin7_AW3"').replace(b'"Stop_WuKong_Skill_A_Run"', b'"Stop_WuKong_Skill_A_Run_Skin7_AW3"').replace(b'"Play_WuKong_Skill_B_1"', b'"Play_WuKong_Skill_B_1_Skin7_AW3"').replace(b'"Play_WuKong_VO_Skill_B"', b'"Play_WuKong_VO_Skill_B_Skin7_AW4"').replace(b'"Play_WuKong_Skill_C"', b'"Play_WuKong_Skill_C_Skin7_AW3"').replace(b'"Play_WuKong_VO_Skill_C"', b'"Play_WuKong_VO_Skill_C_Skin7_AW4"').replace(b'"Play_WuKong_Skill_C_01"', b'"Play_WuKong_Skill_C_01_Skin7_AW3"').replace(b'"Play_WuKong_Skill_C_02"', b'"Play_WuKong_Skill_C_02_Skin7_AW3"').replace(b'"Play_WuKong_Skill_C_Hit"', b'"Play_WuKong_Skill_C_Hit_Skin7_AW3"')
                with open(file_path,'wb') as f: f.write(rpl)
#---------------—------------———----------------
            if IDMODSKIN == '16707' and 'U1B0.xml' in file_path:
                with open(file_path, 'rb') as f: rpl = f.read().replace(b'    <Track trackName="\xe5\xa4\xa7\xe9\x83\xa8\xe5\x88\x86\xe7\x89\xb9\xe6\x95\x88" eventType="TriggerParticleTick" guid="f6e33881-833c-448c-9490-fe53bcc022dc" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Condition id="3" guid="817e473d-e7ad-4d3c-98e3-208f37995506" status="false" />\r\n      <Condition id="13" guid="5d13ff64-966b-4903-9530-d53ad6faeaa7" status="false" />\r\n      <Event eventName="TriggerParticleTick" time="0.133" isDuration="false" guid="e75b172d-2997-4a8f-a8dd-ee0368971d7f">\r\n        <TemplateObject name="targetId" id="-1" objectName="None" isTemp="false" refParamName="" useRefParam="false" />\r\n        <TemplateObject name="objectSpaceId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <String name="resourceName" value="prefab_skill_effects/component_effects/16707/16707_5/wukong_attack_spell03" refParamName="" useRefParam="false" />\r\n        <float name="lifeTime" value="2.000" refParamName="" useRefParam="false" />\r\n        <Vector3 name="bindPosOffset" x="0.000" y="0.100" z="0.000" refParamName="" useRefParam="false" />\r\n        <Vector3i name="scalingInt" x="10000" y="10000" z="10000" refParamName="" useRefParam="false" />\r\n        <bool name="applyActionSpeedToAnimation" value="true" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>', b'    <Track trackName="CreateRandomTick0" eventType="SpawnBulletTick" guid="SpawnBulletTick-Tran_Thi_Nhung" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Condition id="3" guid="817e473d-e7ad-4d3c-98e3-208f37995506" status="false"/>\r\n      <Condition id="15" guid="5d13ff64-966b-4903-9530-d53ad6faeaa7" status="false"/>\r\n      <Event eventName="SpawnBulletTick" time="0.000" isDuration="false">\r\n        <TemplateObject name="targetId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false"/>\r\n        <String name="ActionName" value="prefab_characters/prefab_hero/167_wukong/skill/16707_back" refParamName="" useRefParam="false"/>\r\n        <String name="SpecialActionName" value="prefab_characters/prefab_hero/167_wukong/skill/16707_back" refParamName="" useRefParam="false"/>\r\n        <int name="bulletUpperLimit" value="1" refParamName="" useRefParam="false"/>\r\n      </Event>\r\n    </Track>\r\n    <Track trackName="CheckRandomRangeTick0" eventType="CheckSkillCombineConditionTick" guid="cac41341-211d-4291-8c37-b7586af7e586" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Condition id="3" guid="817e473d-e7ad-4d3c-98e3-208f37995506" status="false"/>\r\n      <Condition id="15" guid="5d13ff64-966b-4903-9530-d53ad6faeaa7" status="false"/>\r\n      <Event eventName="CheckSkillCombineConditionTick" time="0.000" isDuration="false">\r\n        <TemplateObject name="targetId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false"/>\r\n        <int name="skillCombineId" value="130912" refParamName="" useRefParam="false"/>\r\n        <Enum name="checkOPType" value="5" refParamName="" useRefParam="false"/>\r\n        <int name="skillCombineLevel" value="1" refParamName="" useRefParam="false"/>\r\n      </Event>\r\n    </Track>\r\n    <Track trackName="TriggerParticleTick0" eventType="TriggerParticleTick" guid="a0659289-d2c5-47f7-8206-e6a3fecb4ec9" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Condition id="3" guid="817e473d-e7ad-4d3c-98e3-208f37995506" status="false"/>\r\n      <Condition id="15" guid="5d13ff64-966b-4903-9530-d53ad6faeaa7" status="false"/>\r\n      <Condition id="18" guid="cac41341-211d-4291-8c37-b7586af7e586" status="true"/>\r\n      <Event eventName="TriggerParticleTick" time="0.133" isDuration="false">\r\n        <TemplateObject name="targetId" id="-1" objectName="None" isTemp="false" refParamName="" useRefParam="false"/>\r\n        <TemplateObject name="objectSpaceId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false"/>\r\n        <String name="resourceName" value="prefab_skill_effects/component_effects/16707/16707_5/wukong_attack_spell03" refParamName="" useRefParam="false" />\r\n        <int name="frameRate" value="60" refParamName="" useRefParam="false"/>\r\n        <float name="lifeTime" value="2.000" refParamName="" useRefParam="false"/>\r\n        <Vector3 name="bindPosOffset" x="0.000" y="0.100" z="0.000" refParamName="" useRefParam="false"/>\r\n        <Vector3i name="scalingInt" x="10000" y="10000" z="10000" refParamName="" useRefParam="false"/>\r\n        <bool name="applyActionSpeedToAnimation" value="true" refParamName="" useRefParam="false"/>\r\n      </Event>\r\n    </Track>\r\n    <Track trackName="PlayHeroSoundTick0" eventType="PlayHeroSoundTick" guid="96204c97-a0cc-4a3f-825c-37ad1d56e6cf" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Condition id="3" guid="817e473d-e7ad-4d3c-98e3-208f37995506" status="false"/>\r\n      <Condition id="15" guid="5d13ff64-966b-4903-9530-d53ad6faeaa7" status="false"/>\r\n      <Condition id="18" guid="cac41341-211d-4291-8c37-b7586af7e586" status="true"/>\r\n      <Event eventName="PlayHeroSoundTick" time="0.133" isDuration="false">\r\n        <TemplateObject name="targetId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false"/>\r\n        <TemplateObject name="sourceId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false"/>\r\n        <String name="eventName" value="Play_WuKong_Skill_C_01_Skin7_AW3" refParamName="" useRefParam="false"/>\r\n        <bool name="useSkinSwitch" value="false" refParamName="" useRefParam="false"/>\r\n      </Event>\r\n    </Track>\r\n    <Track trackName="TriggerParticleTick0" eventType="TriggerParticleTick" guid="b9a09802-b37d-4562-9963-f566adbddfa5" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Condition id="3" guid="817e473d-e7ad-4d3c-98e3-208f37995506" status="false"/>\r\n      <Condition id="15" guid="5d13ff64-966b-4903-9530-d53ad6faeaa7" status="false"/>\r\n      <Condition id="18" guid="cac41341-211d-4291-8c37-b7586af7e586" status="false"/>\r\n      <Event eventName="TriggerParticleTick" time="0.133" isDuration="false">\r\n        <TemplateObject name="targetId" id="-1" objectName="None" isTemp="false" refParamName="" useRefParam="false"/>\r\n        <TemplateObject name="objectSpaceId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false"/>\r\n        <String name="resourceName" value="prefab_skill_effects/component_effects/16707/16707_5/wukong_attack_spell03_1" refParamName="" useRefParam="false" />\r\n        <float name="lifeTime" value="2.000" refParamName="" useRefParam="false"/>\r\n        <Vector3 name="bindPosOffset" x="0.000" y="0.100" z="0.000" refParamName="" useRefParam="false"/>\r\n        <Vector3i name="scalingInt" x="10000" y="10000" z="10000" refParamName="" useRefParam="false"/>\r\n        <bool name="applyActionSpeedToAnimation" value="true" refParamName="" useRefParam="false"/>\r\n      </Event>\r\n    </Track>\r\n    <Track trackName="PlayHeroSoundTick0" eventType="PlayHeroSoundTick" guid="06e07caf-383b-484f-af7c-5ab073ba3256" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Condition id="3" guid="817e473d-e7ad-4d3c-98e3-208f37995506" status="false"/>\r\n      <Condition id="15" guid="5d13ff64-966b-4903-9530-d53ad6faeaa7" status="false"/>\r\n      <Condition id="18" guid="cac41341-211d-4291-8c37-b7586af7e586" status="false"/>\r\n      <Event eventName="PlayHeroSoundTick" time="0.133" isDuration="false">\r\n        <TemplateObject name="targetId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false"/>\r\n        <TemplateObject name="sourceId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false"/>\r\n        <String name="eventName" value="Play_WuKong_Skill_C_02_Skin7_AW3" refParamName="" useRefParam="false"/>\r\n        <bool name="useSkinSwitch" value="false" refParamName="" useRefParam="false"/>\r\n      </Event>\r\n    </Track>')
                with open(file_path,'wb') as f: f.write(rpl)
#---------------—------------———----------------
            if IDMODSKIN =='11113' and 'S1E2.xml' in file_path:
                with open(file_path, 'rb') as f: rpl = f.read().replace(b'<Condition id="13" guid="ca3dd627-8d6d-4661-b08f-c2fe67130b12" status="true" />',b'<!--'+AABBCC.encode('utf-8') +b'-->')
                with open(file_path,'wb') as f: f.write(rpl)
            if IDMODSKIN =='11113' and 'S2.xml' in file_path:
                with open(file_path, 'rb') as f: rpl = f.read().replace(b'<Condition id="4" guid="d4d3787f-4aca-405b-a25e-3a83e5b3e8bb" status="true" />',b'<!--'+AABBCC.encode('utf-8') +b'-->')
                with open(file_path,'wb') as f: f.write(rpl)
            if IDMODSKIN =='11113' and 'U1.xml' in file_path:
                with open(file_path, 'rb') as f: rpl = f.read().replace(b'<Condition id="7" guid="92b36a35-ec2d-4a50-88e9-73f085da65d8" status="true" />',b'<!--'+AABBCC.encode('utf-8') +b'-->').replace(b'<Condition id="6" guid="f6bb4dff-ef39-4636-9b11-fdf89e1e0461" status="true" />',b'<!--'+AABBCC.encode('utf-8') +b'-->').replace(b'eventType="SpawnBulletTick" guid="cbe5ad61-6542-40fe-9317-c881f4618927" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <!--'+AABBCC.encode('utf-8') +b'-->',b'eventType="SpawnBulletTick" guid="cbe5ad61-6542-40fe-9317-c881f4618927" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Condition id="6" guid="f6bb4dff-ef39-4636-9b11-fdf89e1e0461" status="true" />').replace(b'<TrackObject id="17" guid="036b40ff-08d6-415a-9d97-97e0942d2aee" />\r\n          <TrackObject id="33" guid="f33baa3c-2b9e-4fbb-8650-dacb612888ba" />\r\n          <TrackObject id="18" guid="2d8e1f0d-7f4a-41d6-bef4-aa762513d4fa" />\r\n          <TrackObject id="23" guid="1414bd9d-4a3e-4263-81d9-d5b75fd19390" />',b'<TrackObject id="17" guid="036b40ff-08d6-415a-9d97-97e0942d2aee" />\r\n          <TrackObject id="33" guid="f33baa3c-2b9e-4fbb-8650-dacb612888ba" />\r\n          <TrackObject id="23" guid="1414bd9d-4a3e-4263-81d9-d5b75fd19390" />').replace(b'</Event>\r\n    </Track>\r\n  </Action>\r\n</Project>',b'</Event>\r\n    </Track>\r\n    <Track trackName="StopTracks0" eventType="StopTracks" guid="abfc4701-c38e-4969-925e-fc3ef0f64b78" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Condition id="6" guid="f6bb4dff-ef39-4636-9b11-fdf89e1e0461" status="true" />\r\n      <Condition id="8" guid="fd62cea3-5d27-43e5-950d-d3fb75ed09fc" status="true" />\r\n      <Event eventName="StopTracks" time="0.000" isDuration="false" guid="b889ae65-11d9-4724-aa75-6b874d4d7e48">\r\n        <Array name="trackIds" refParamName="" useRefParam="false" type="TrackObject">\r\n          <TrackObject id="17" guid="036b40ff-08d6-415a-9d97-97e0942d2aee" />\r\n          <TrackObject id="33" guid="f33baa3c-2b9e-4fbb-8650-dacb612888ba" />\r\n          <TrackObject id="18" guid="2d8e1f0d-7f4a-41d6-bef4-aa762513d4fa" />\r\n          <TrackObject id="23" guid="1414bd9d-4a3e-4263-81d9-d5b75fd19390" />\r\n        </Array>\r\n        <bool name="alsoStopNotStartedTrack" value="true" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>\r\n  </Action>\r\n</Project>')
                with open(file_path,'wb') as f: f.write(rpl)

#---------------—------------———----------------
            if IDMODSKIN =='15012' and 'U1.xml' in file_path:
                with open(file_path, 'rb') as f: rpl = f.read().replace(b'<int name="skinId" value="15012" refParamName="" useRefParam="false" />',b'<int name="skinId" value="15092" refParamName="" useRefParam="false" />\n        <bool name="useNegateValue" value="true" refParamName="" useRefParam="false" />')
                with open(file_path, 'wb') as f: f.write(rpl)
#---------------—------------———----------------
            if IDMODSKIN =='10620' and 'S2.xml' not in file_path:
                with open(file_path, 'rb') as f: rpl = f.read().replace(b'        <int name="skinId" value="10620" refParamName="" useRefParam="false" />\r\n        <bool name="bEqual" value="false" refParamName="" useRefParam="false" />\r\n        <bool name="bSkipLogicCheck" value="true" refParamName="" useRefParam="false" />',b'        <int name="skinId" value="10620" refParamName="" useRefParam="false" />>\r\n        <<bool name="bEqual" value="false" refParamName="" useRefParam="false" />>\r\n        <bool name="bSkipLogicCheck" value="true" refParamName="" useRefParam="false" />').replace(b'        <int name="skinId" value="10620" refParamName="" useRefParam="false" />\r\n        <bool name="bSkipLogicCheck" value="true" refParamName="" useRefParam="false" />',b'        <int name="skinId" value="10620" refParamName="" useRefParam="false" />\r\n        <bool name="bEqual" value="false" refParamName="" useRefParam="false" />\r\n        <bool name="bSkipLogicCheck" value="true" refParamName="" useRefParam="false" />').replace(b'        <int name="skinId" value="10620" refParamName="" useRefParam="false" />>\r\n        <<bool name="bEqual" value="false" refParamName="" useRefParam="false" />>\r\n        <bool name="bSkipLogicCheck" value="true" refParamName="" useRefParam="false" />',b'        <int name="skinId" value="10620" refParamName="" useRefParam="false" />\r\n        <bool name="bSkipLogicCheck" value="true" refParamName="" useRefParam="false" />')
                with open(file_path, 'wb') as f: f.write(rpl)
#---------------—------------———----------------
            if IDMODSKIN == '10620' and 'S2.xml' in file_path:
                with open(file_path, 'rb') as f:
                    rpl = f.read().replace(b'        <int name="skinId" value="10620" refParamName="" useRefParam="false" />\r\n        <bool name="bEqual" value="false" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>',b'        <int name="skinId" value="10620" refParamName="" useRefParam="false" />\r\n        <<bool name="bEqual" value="false" refParamName="" useRefParam="false" />>\r\n      </Event>\r\n    </Track>').replace(b'        <int name="skinId" value="10620" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>',b'        <int name="skinId" value="10620" refParamName="" useRefParam="false" />\r\n        <bool name="bEqual" value="false" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>').replace(b'        <int name="skinId" value="10620" refParamName="" useRefParam="false" />\r\n        <<bool name="bEqual" value="false" refParamName="" useRefParam="false" />>\r\n      </Event>\r\n    </Track>',b'        <int name="skinId" value="10620" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>')
                with open(file_path, 'wb') as f: f.write(rpl)
#---------------—------------———----------------
            if IDMODSKIN == '17106' and 'P1E5.xml' in file_path:
                with open(file_path, 'rb') as f:
                    rpl = f.read().replace(b'prefab_skill_effects/hero_skill_effects/171_zhangfei/17106/1719_zhangfei', b'prefab_skill_effects/hero_skill_effects/171_zhangfei/1719_zhangfei')
                with open(file_path, 'wb') as f: f.write(rpl)
#-----------------------------------------------
            if IDMODSKIN == '13210':
                with open(file_path, 'rb') as f:
                    rpl = f.read()
                if 'A1.xml' in file_path:
                    with open(file_path, 'rb') as f:
                        rpl = f.read()
                        rpl = rpl.replace(b'\r\n  </Action>',b'\n    <Track trackName="Tran_Thi_Nhung" eventType="HitTriggerTick" guid="810de6b2-8b68-4614-8762-84bbafe2e77a" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Event eventName="HitTriggerTick" time="0.000" isDuration="false" guid="06468bb9-532f-4c15-819f-4ea3434f2a47">\r\n        <TemplateObject name="targetId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <int name="SelfSkillCombineID_1" value="132111" refParamName="" useRefParam="false" />\r\n        <TemplateObject name="triggerId" id="-1" objectName="None" isTemp="false" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>\r\n    <Track trackName="RemoveBuffTick0" eventType="RemoveBuffTick" guid="3de6a2a7-e28c-4002-b42c-5fa3bdc98217" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Event eventName="RemoveBuffTick" time="0.000" isDuration="false" guid="13b2f181-602e-4ada-b268-cc5399b4d39d">\r\n        <TemplateObject name="targetId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <int name="buffId" value="132113" refParamName="" useRefParam="false" />\r\n        <int name="BuffLayer" value="1" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>\r\n    <Track trackName="RemoveBuffTick0" eventType="RemoveBuffTick" guid="3de6a2a7-e28c-4002-b42c-5fa3bdc98217" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Event eventName="RemoveBuffTick" time="0.000" isDuration="false" guid="13b2f181-602e-4ada-b268-cc5399b4d39d">\r\n        <TemplateObject name="targetId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <int name="buffId" value="132112" refParamName="" useRefParam="false" />\r\n        <int name="BuffLayer" value="1" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>\r\n  </Action>')
                if 'A2.xml' in file_path:
                    with open(file_path, 'rb') as f:
                        rpl = f.read()
                        rpl = rpl.replace(b'  </Action>',b'    <Track trackName="Tran_Thi_Nhung" eventType="HitTriggerTick" guid="810de6b2-8b68-4614-8762-84bbafe2e77a" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Event eventName="HitTriggerTick" time="0.000" isDuration="false" guid="06468bb9-532f-4c15-819f-4ea3434f2a47">\r\n        <TemplateObject name="targetId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <int name="SelfSkillCombineID_1" value="132112" refParamName="" useRefParam="false" />\r\n        <TemplateObject name="triggerId" id="-1" objectName="None" isTemp="false" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>\r\n    <Track trackName="RemoveBuffTick0" eventType="RemoveBuffTick" guid="3de6a2a7-e28c-4002-b42c-5fa3bdc98217" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Event eventName="RemoveBuffTick" time="0.000" isDuration="false" guid="13b2f181-602e-4ada-b268-cc5399b4d39d">\r\n        <TemplateObject name="targetId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <int name="buffId" value="132111" refParamName="" useRefParam="false" />\r\n        <int name="BuffLayer" value="1" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>\r\n    <Track trackName="RemoveBuffTick0" eventType="RemoveBuffTick" guid="3de6a2a7-e28c-4002-b42c-5fa3bdc98217" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Event eventName="RemoveBuffTick" time="0.000" isDuration="false" guid="13b2f181-602e-4ada-b268-cc5399b4d39d">\r\n        <TemplateObject name="targetId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <int name="buffId" value="132113" refParamName="" useRefParam="false" />\r\n        <int name="BuffLayer" value="1" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>\r\n  </Action>    ')
                if 'A3.xml' in file_path:
                    with open(file_path, 'rb') as f:
                        rpl = f.read()
                        rpl = rpl.replace(b'  </Action>',b'    <Track trackName="Tran_Thi_Nhung" eventType="HitTriggerTick" guid="810de6b2-8b68-4614-8762-84bbafe2e77a" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Event eventName="HitTriggerTick" time="0.000" isDuration="false" guid="06468bb9-532f-4c15-819f-4ea3434f2a47">\r\n        <TemplateObject name="targetId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <int name="SelfSkillCombineID_1" value="132113" refParamName="" useRefParam="false" />\r\n        <TemplateObject name="triggerId" id="-1" objectName="None" isTemp="false" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>\r\n    <Track trackName="RemoveBuffTick0" eventType="RemoveBuffTick" guid="3de6a2a7-e28c-4002-b42c-5fa3bdc98217" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Event eventName="RemoveBuffTick" time="0.000" isDuration="false" guid="13b2f181-602e-4ada-b268-cc5399b4d39d">\r\n        <TemplateObject name="targetId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <int name="buffId" value="132111" refParamName="" useRefParam="false" />\r\n        <int name="BuffLayer" value="1" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>\r\n    <Track trackName="RemoveBuffTick0" eventType="RemoveBuffTick" guid="3de6a2a7-e28c-4002-b42c-5fa3bdc98217" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Event eventName="RemoveBuffTick" time="0.000" isDuration="false" guid="13b2f181-602e-4ada-b268-cc5399b4d39d">\r\n        <TemplateObject name="targetId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <int name="buffId" value="132112" refParamName="" useRefParam="false" />\r\n        <int name="BuffLayer" value="1" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>\r\n  </Action>')
                if 'S1B1.xml' in file_path:
                    with open(file_path,'rb') as f:
                        rpl = f.read()
                        rpl = rpl.replace(b'  </Action>',b'    <Track trackName="Tran_Thi_Nhung" eventType="HitTriggerTick" guid="810de6b2-8b68-4614-8762-84bbafe2e77a" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Condition id="3" guid="c83eb09d-73c4-461b-938f-f73070abc892" status="true" />\r\n      <Event eventName="HitTriggerTick" time="0.000" isDuration="false" guid="06468bb9-532f-4c15-819f-4ea3434f2a47">\r\n        <TemplateObject name="targetId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <int name="SelfSkillCombineID_1" value="132111" refParamName="" useRefParam="false" />\r\n        <TemplateObject name="triggerId" id="-1" objectName="None" isTemp="false" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>\r\n    <Track trackName="Tran_Thi_Nhung" eventType="HitTriggerTick" guid="8593531d-6223-4e88-8100-271908335727" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Condition id="5" guid="0509e695-f257-4517-aca1-44a7fcea5df8" status="true" />\r\n      <Event eventName="HitTriggerTick" time="0.000" isDuration="false" guid="e9ad175b-19a2-4349-bbe2-9943b68b27d2">\r\n        <TemplateObject name="targetId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <int name="SelfSkillCombineID_1" value="132112" refParamName="" useRefParam="false" />\r\n        <TemplateObject name="triggerId" id="-1" objectName="None" isTemp="false" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>\r\n    <Track trackName="Tran_Thi_Nhung" eventType="HitTriggerTick" guid="1d752369-b04e-4751-9c2e-bf07c90d34dd" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Condition id="7" guid="76baa7d0-5675-46c1-989a-9ddaf2867faa" status="true" />\r\n      <Event eventName="HitTriggerTick" time="0.000" isDuration="false" guid="5f9271af-ec05-4d4f-af1e-70941661041c">\r\n        <TemplateObject name="targetId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <int name="SelfSkillCombineID_1" value="132113" refParamName="" useRefParam="false" />\r\n        <TemplateObject name="triggerId" id="-1" objectName="None" isTemp="false" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>\r\n    <Track trackName="TriggerParticle6" eventType="TriggerParticle" guid="536a47d0-fdc5-441e-b382-53866c442844" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Condition id="3" guid="c83eb09d-73c4-461b-938f-f73070abc892" status="false" />\r\n      <Condition id="5" guid="0509e695-f257-4517-aca1-44a7fcea5df8" status="false" />\r\n      <Condition id="7" guid="76baa7d0-5675-46c1-989a-9ddaf2867faa" status="false" />\r\n      <Event eventName="TriggerParticle" time="0.000" length="0.700" isDuration="true" guid="38ee198d-1e31-45e7-857a-06c00d811da8">\r\n        <TemplateObject name="targetId" id="2" objectName="bullet" isTemp="true" refParamName="" useRefParam="false" />\r\n        <String name="resourceName" value="prefab_skill_effects/hero_skill_effects/132_makeboluo/13210/Makeboluo_spell01_bullet_01" refParamName="" useRefParam="false" />\r\n        <Vector3i name="scalingInt" x="10000" y="10000" z="10000" refParamName="" useRefParam="false" />\r\n        <String name="syncAnimationName" value="" refParamName="" useRefParam="false" />\r\n        <String name="customTagName" value="" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>\r\n  </Action>').replace(b'<bool name="useNegateValue" value="true" refParamName="" useRefParam="false" />',b'')
                if 'S12B0.xml' in file_path:
                    with open(file_path, 'rb') as f:
                        rpl = f.read()
                        rpl = re.sub(b'"resourceName" value="(.*?)"', b'"resourceName" value="Tran_Thi_Nhung"', rpl)
                        rpl = rpl.replace(b'  </Action>',b'    <Track trackName="1" eventType="CheckSkillCombineConditionTick" guid="Mod_By_Tran_Thi_Nhung_Mod_132111" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Event eventName="CheckSkillCombineConditionTick" time="0.000" isDuration="false" guid="b0dbc04b-5f6d-4610-a37b-b5240f304825">\r\n        <TemplateObject name="targetId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <int name="skillCombineId" value="132111" refParamName="" useRefParam="false" />\r\n        <Enum name="checkOPType" value="3" refParamName="" useRefParam="false" />\r\n        <int name="skillCombineLevel" value="1" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>\r\n    <Track trackName="2" eventType="CheckSkillCombineConditionTick" guid="Mod_By_Tran_Thi_Nhung_Mod_132112" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Event eventName="CheckSkillCombineConditionTick" time="0.000" isDuration="false" guid="fb9ffe1e-fc80-463c-aa04-7e4749711ab8">\r\n        <TemplateObject name="targetId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <int name="skillCombineId" value="132112" refParamName="" useRefParam="false" />\r\n        <Enum name="checkOPType" value="3" refParamName="" useRefParam="false" />\r\n        <int name="skillCombineLevel" value="1" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>\r\n    <Track trackName="3" eventType="CheckSkillCombineConditionTick" guid="Mod_By_Tran_Thi_Nhung_132113" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Event eventName="CheckSkillCombineConditionTick" time="0.000" isDuration="false" guid="6786a65e-f11b-484a-a0ae-613c7521f69e">\r\n        <TemplateObject name="targetId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <int name="skillCombineId" value="132113" refParamName="" useRefParam="false" />\r\n        <Enum name="checkOPType" value="3" refParamName="" useRefParam="false" />\r\n        <int name="skillCombineLevel" value="1" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>\r\n    <Track trackName="TriggerParticle0" eventType="TriggerParticle" guid="91aaf49d-c92c-4481-9957-e3b0448f1479" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Condition id="43" guid="Mod_By_Tran_Thi_Nhung_Mod_132111" status="true" />\r\n      <Event eventName="TriggerParticle" time="0.000" length="1.400" isDuration="true" guid="51311a35-66be-4940-9a41-431050e09e2b">\r\n        <TemplateObject name="targetId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <TemplateObject name="objectSpaceId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <String name="resourceName" value="prefab_skill_effects/hero_skill_effects/132_makeboluo/13210/Makeboluo_spell01_attack_01" refParamName="" useRefParam="false" />\r\n        <Vector3i name="scalingInt" x="10000" y="10000" z="10000" refParamName="" useRefParam="false" />\r\n        <String name="syncAnimationName" value="" refParamName="" useRefParam="false" />\r\n        <String name="customTagName" value="" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>\r\n    <Track trackName="TriggerParticle0" eventType="TriggerParticle" guid="91aaf49d-c92c-4481-9957-e3b0448f1479" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Condition id="43" guid="Mod_By_Tran_Thi_Nhung_Mod_132111" status="true" />\r\n      <Event eventName="TriggerParticle" time="0.000" length="1.400" isDuration="true" guid="51311a35-66be-4940-9a41-431050e09e2b">\r\n        <TemplateObject name="targetId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <TemplateObject name="objectSpaceId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <String name="resourceName" value="prefab_skill_effects/hero_skill_effects/132_makeboluo/13210/Makeboluo_spell01_attack_01_1" refParamName="" useRefParam="false" />\r\n        <Vector3i name="scalingInt" x="10000" y="10000" z="10000" refParamName="" useRefParam="false" />\r\n        <String name="syncAnimationName" value="" refParamName="" useRefParam="false" />\r\n        <String name="customTagName" value="" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>\r\n    <Track trackName="TriggerParticle0" eventType="TriggerParticle" guid="91aaf49d-c92c-4481-9957-e3b0448f1479" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Condition id="44" guid="Mod_By_Tran_Thi_Nhung_Mod_132112" status="true" />\r\n      <Event eventName="TriggerParticle" time="0.000" length="1.400" isDuration="true" guid="51311a35-66be-4940-9a41-431050e09e2b">\r\n        <TemplateObject name="targetId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <TemplateObject name="objectSpaceId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <String name="resourceName" value="prefab_skill_effects/hero_skill_effects/132_makeboluo/13210/Makeboluo_spell01_attack_02" refParamName="" useRefParam="false" />\r\n        <Vector3i name="scalingInt" x="10000" y="10000" z="10000" refParamName="" useRefParam="false" />\r\n        <String name="syncAnimationName" value="" refParamName="" useRefParam="false" />\r\n        <String name="customTagName" value="" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>\r\n    <Track trackName="TriggerParticle0" eventType="TriggerParticle" guid="91aaf49d-c92c-4481-9957-e3b0448f1479" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Condition id="44" guid="Mod_By_Tran_Thi_Nhung_Mod_132112" status="true" />\r\n      <Event eventName="TriggerParticle" time="0.000" length="1.400" isDuration="true" guid="51311a35-66be-4940-9a41-431050e09e2b">\r\n        <TemplateObject name="targetId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <TemplateObject name="objectSpaceId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <String name="resourceName" value="prefab_skill_effects/hero_skill_effects/132_makeboluo/13210/Makeboluo_spell01_attack_02_1" refParamName="" useRefParam="false" />\r\n        <Vector3i name="scalingInt" x="10000" y="10000" z="10000" refParamName="" useRefParam="false" />\r\n        <String name="syncAnimationName" value="" refParamName="" useRefParam="false" />\r\n        <String name="customTagName" value="" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>\r\n    <Track trackName="TriggerParticle0" eventType="TriggerParticle" guid="91aaf49d-c92c-4481-9957-e3b0448f1479" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Condition id="45" guid="Mod_By_Tran_Thi_Nhung_132113" status="true" />\r\n      <Event eventName="TriggerParticle" time="0.000" length="1.400" isDuration="true" guid="51311a35-66be-4940-9a41-431050e09e2b">\r\n        <TemplateObject name="targetId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <TemplateObject name="objectSpaceId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <String name="resourceName" value="prefab_skill_effects/hero_skill_effects/132_makeboluo/13210/Makeboluo_spell01_attack_03" refParamName="" useRefParam="false" />\r\n        <Vector3i name="scalingInt" x="10000" y="10000" z="10000" refParamName="" useRefParam="false" />\r\n        <String name="syncAnimationName" value="" refParamName="" useRefParam="false" />\r\n        <String name="customTagName" value="" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>\r\n    <Track trackName="TriggerParticle0" eventType="TriggerParticle" guid="91aaf49d-c92c-4481-9957-e3b0448f1479" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Condition id="45" guid="Mod_By_Tran_Thi_Nhung_132113" status="true" />\r\n      <Event eventName="TriggerParticle" time="0.000" length="1.400" isDuration="true" guid="51311a35-66be-4940-9a41-431050e09e2b">\r\n        <TemplateObject name="targetId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <TemplateObject name="objectSpaceId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <String name="resourceName" value="prefab_skill_effects/hero_skill_effects/132_makeboluo/13210/Makeboluo_spell01_attack_03_1" refParamName="" useRefParam="false" />\r\n        <Vector3i name="scalingInt" x="10000" y="10000" z="10000" refParamName="" useRefParam="false" />\r\n        <String name="syncAnimationName" value="" refParamName="" useRefParam="false" />\r\n        <String name="customTagName" value="" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>\r\n    <Track trackName="TriggerParticle0" eventType="TriggerParticle" guid="91aaf49d-c92c-4481-9957-e3b0448f1479" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Condition id="Tran_Thi_Nhung" guid="Mod_By_Tran_Thi_Nhung_Mod_132111" status="false" />\r\n      <Condition id="Tran_Thi_Nhung" guid="Mod_By_Tran_Thi_Nhung_Mod_132112" status="false" />\r\n      <Condition id="Tran_Thi_Nhung" guid="Mod_By_Tran_Thi_Nhung_132113" status="false" />\r\n      <Event eventName="TriggerParticle" time="0.000" length="1.400" isDuration="true" guid="51311a35-66be-4940-9a41-431050e09e2b">\r\n        <TemplateObject name="targetId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <TemplateObject name="objectSpaceId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <String name="resourceName" value="prefab_skill_effects/hero_skill_effects/132_makeboluo/13210/Makeboluo_spell01_attack_01" refParamName="" useRefParam="false" />\r\n        <Vector3i name="scalingInt" x="10000" y="10000" z="10000" refParamName="" useRefParam="false" />\r\n        <String name="syncAnimationName" value="" refParamName="" useRefParam="false" />\r\n        <String name="customTagName" value="" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>\r\n    <Track trackName="TriggerParticle0" eventType="TriggerParticle" guid="91aaf49d-c92c-4481-9957-e3b0448f1479" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Condition id="Tran_Thi_Nhung" guid="Mod_By_Tran_Thi_Nhung_Mod_132111" status="false" />\r\n      <Condition id="Tran_Thi_Nhung" guid="Mod_By_Tran_Thi_Nhung_Mod_132112" status="false" />\r\n      <Condition id="Tran_Thi_Nhung" guid="Mod_By_Tran_Thi_Nhung_132113" status="false" />\r\n      <Event eventName="TriggerParticle" time="0.000" length="1.400" isDuration="true" guid="51311a35-66be-4940-9a41-431050e09e2b">\r\n        <TemplateObject name="targetId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <TemplateObject name="objectSpaceId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <String name="resourceName" value="prefab_skill_effects/hero_skill_effects/132_makeboluo/13210/Makeboluo_spell01_attack_01_1" refParamName="" useRefParam="false" />\r\n        <Vector3i name="scalingInt" x="10000" y="10000" z="10000" refParamName="" useRefParam="false" />\r\n        <String name="syncAnimationName" value="" refParamName="" useRefParam="false" />\r\n        <String name="customTagName" value="" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>\r\n    <Track trackName="T2\xe9\x9a\x8f\xe6\x9c\xba1 \xe9\x9f\xb3\xe6\x95\x88" eventType="PlayHeroSoundTick" guid="f92f38f7-c71a-4ea3-abfc-c8e4eb5b3865" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Condition id="Tran_Thi_Nhung" guid="Mod_By_Tran_Thi_Nhung_Mod_132111" status="true" />\r\n      <Event eventName="PlayHeroSoundTick" time="0.000" isDuration="false" guid="9b862449-dea5-4cee-b1f0-8b1b3724ca8f">\r\n        <TemplateObject name="targetId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <TemplateObject name="sourceId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <String name="eventName" value="Play_13210_Hayate_SkillA_03" refParamName="" useRefParam="false" />\r\n        <bool name="useSkinSwitch" value="false" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>\r\n    <Track trackName="T2\xe9\x9a\x8f\xe6\x9c\xba2 \xe9\x9f\xb3\xe6\x95\x88" eventType="PlayHeroSoundTick" guid="c7107416-30e0-4ee8-83fa-5f97bb948faf" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Condition id="Tran_Thi_Nhung" guid="Mod_By_Tran_Thi_Nhung_Mod_132112" status="true" />\r\n      <Event eventName="PlayHeroSoundTick" time="0.000" isDuration="false" guid="4a8d55af-a3b6-4c1a-b7b9-830ea761ccf9">\r\n        <TemplateObject name="targetId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <TemplateObject name="sourceId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <String name="eventName" value="Play_13210_Hayate_SkillA_01" refParamName="" useRefParam="false" />\r\n        <bool name="useSkinSwitch" value="false" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>\r\n    <Track trackName="T2\xe9\x9a\x8f\xe6\x9c\xba3 \xe9\x9f\xb3\xe6\x95\x88" eventType="PlayHeroSoundTick" guid="bca0dd8d-b83a-49da-982c-6cadaef3966a" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Condition id="Tran_Thi_Nhung" guid="Mod_By_Tran_Thi_Nhung_132113" status="true" />\r\n      <Event eventName="PlayHeroSoundTick" time="0.000" isDuration="false" guid="129a0664-39ba-43af-9d93-43c6b7d64878">\r\n        <TemplateObject name="targetId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <TemplateObject name="sourceId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <String name="eventName" value="Play_13210_Hayate_SkillA_02" refParamName="" useRefParam="false" />\r\n        <bool name="useSkinSwitch" value="false" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>\r\n    <Track trackName="T2\xe9\x9a\x8f\xe6\x9c\xba1 \xe9\x9f\xb3\xe6\x95\x88" eventType="PlayHeroSoundTick" guid="f92f38f7-c71a-4ea3-abfc-c8e4eb5b3865" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Condition id="Tran_Thi_Nhung" guid="Mod_By_Tran_Thi_Nhung_Mod_132111" status="false" />\r\n      <Condition id="Tran_Thi_Nhung" guid="Mod_By_Tran_Thi_Nhung_Mod_132112" status="false" />\r\n      <Condition id="Tran_Thi_Nhung" guid="Mod_By_Tran_Thi_Nhung_132113" status="false" />\r\n      <Event eventName="PlayHeroSoundTick" time="0.000" isDuration="false" guid="9b862449-dea5-4cee-b1f0-8b1b3724ca8f">\r\n        <TemplateObject name="targetId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <TemplateObject name="sourceId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <String name="eventName" value="Play_13210_Hayate_SkillA_03" refParamName="" useRefParam="false" />\r\n        <bool name="useSkinSwitch" value="false" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>\r\n    <Track trackName="T2\xe9\x9a\x8f\xe6\x9c\xba1" eventType="HitTriggerTick" guid="810de6b2-8b68-4614-8762-84bbafe2e77a" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Condition id="Tran_Thi_Nhung" guid="Mod_By_Tran_Thi_Nhung_Mod_132111" status="false" />\r\n      <Condition id="Tran_Thi_Nhung" guid="Mod_By_Tran_Thi_Nhung_Mod_132112" status="false" />\r\n      <Condition id="Tran_Thi_Nhung" guid="Mod_By_Tran_Thi_Nhung_132113" status="false" />\r\n      <Event eventName="HitTriggerTick" time="0.000" isDuration="false" guid="06468bb9-532f-4c15-819f-4ea3434f2a47">\r\n        <TemplateObject name="targetId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <int name="SelfSkillCombineID_1" value="132111" refParamName="" useRefParam="false" />\r\n        <TemplateObject name="triggerId" id="-1" objectName="None" isTemp="false" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>\r\n  </Action>')
                if 'S11B0.xml' in file_path:
                    with open(file_path, 'rb') as f:
                        rpl = f.read()
                        rpl = re.sub(b'"resourceName" value="(.*?)"', b'"resourceName" value="Tran_Thi_Nhung"', rpl)
                        rpl = rpl.replace(b'  </Action>',b'    <Track trackName="1" eventType="CheckSkillCombineConditionTick" guid="Mod_By_Tran_Thi_Nhung_Mod_132111" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Event eventName="CheckSkillCombineConditionTick" time="0.000" isDuration="false" guid="b0dbc04b-5f6d-4610-a37b-b5240f304825">\r\n        <TemplateObject name="targetId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <int name="skillCombineId" value="132111" refParamName="" useRefParam="false" />\r\n        <Enum name="checkOPType" value="3" refParamName="" useRefParam="false" />\r\n        <int name="skillCombineLevel" value="1" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>\r\n    <Track trackName="2" eventType="CheckSkillCombineConditionTick" guid="Mod_By_Tran_Thi_Nhung_Mod_132112" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Event eventName="CheckSkillCombineConditionTick" time="0.000" isDuration="false" guid="fb9ffe1e-fc80-463c-aa04-7e4749711ab8">\r\n        <TemplateObject name="targetId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <int name="skillCombineId" value="132112" refParamName="" useRefParam="false" />\r\n        <Enum name="checkOPType" value="3" refParamName="" useRefParam="false" />\r\n        <int name="skillCombineLevel" value="1" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>\r\n    <Track trackName="3" eventType="CheckSkillCombineConditionTick" guid="Mod_By_Tran_Thi_Nhung_132113" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Event eventName="CheckSkillCombineConditionTick" time="0.000" isDuration="false" guid="6786a65e-f11b-484a-a0ae-613c7521f69e">\r\n        <TemplateObject name="targetId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <int name="skillCombineId" value="132113" refParamName="" useRefParam="false" />\r\n        <Enum name="checkOPType" value="3" refParamName="" useRefParam="false" />\r\n        <int name="skillCombineLevel" value="1" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>\r\n    <Track trackName="TriggerParticle0" eventType="TriggerParticle" guid="91aaf49d-c92c-4481-9957-e3b0448f1479" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Condition id="43" guid="Mod_By_Tran_Thi_Nhung_Mod_132111" status="true" />\r\n      <Event eventName="TriggerParticle" time="0.000" length="1.400" isDuration="true" guid="51311a35-66be-4940-9a41-431050e09e2b">\r\n        <TemplateObject name="targetId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <TemplateObject name="objectSpaceId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <String name="resourceName" value="prefab_skill_effects/hero_skill_effects/132_makeboluo/13210/Makeboluo_spell01_attack_01" refParamName="" useRefParam="false" />\r\n        <Vector3i name="scalingInt" x="10000" y="10000" z="10000" refParamName="" useRefParam="false" />\r\n        <String name="syncAnimationName" value="" refParamName="" useRefParam="false" />\r\n        <String name="customTagName" value="" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>\r\n    <Track trackName="TriggerParticle0" eventType="TriggerParticle" guid="91aaf49d-c92c-4481-9957-e3b0448f1479" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Condition id="43" guid="Mod_By_Tran_Thi_Nhung_Mod_132111" status="true" />\r\n      <Event eventName="TriggerParticle" time="0.000" length="1.400" isDuration="true" guid="51311a35-66be-4940-9a41-431050e09e2b">\r\n        <TemplateObject name="targetId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <TemplateObject name="objectSpaceId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <String name="resourceName" value="prefab_skill_effects/hero_skill_effects/132_makeboluo/13210/Makeboluo_spell01_attack_01_1" refParamName="" useRefParam="false" />\r\n        <Vector3i name="scalingInt" x="10000" y="10000" z="10000" refParamName="" useRefParam="false" />\r\n        <String name="syncAnimationName" value="" refParamName="" useRefParam="false" />\r\n        <String name="customTagName" value="" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>\r\n    <Track trackName="TriggerParticle0" eventType="TriggerParticle" guid="91aaf49d-c92c-4481-9957-e3b0448f1479" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Condition id="44" guid="Mod_By_Tran_Thi_Nhung_Mod_132112" status="true" />\r\n      <Event eventName="TriggerParticle" time="0.000" length="1.400" isDuration="true" guid="51311a35-66be-4940-9a41-431050e09e2b">\r\n        <TemplateObject name="targetId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <TemplateObject name="objectSpaceId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <String name="resourceName" value="prefab_skill_effects/hero_skill_effects/132_makeboluo/13210/Makeboluo_spell01_attack_02" refParamName="" useRefParam="false" />\r\n        <Vector3i name="scalingInt" x="10000" y="10000" z="10000" refParamName="" useRefParam="false" />\r\n        <String name="syncAnimationName" value="" refParamName="" useRefParam="false" />\r\n        <String name="customTagName" value="" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>\r\n    <Track trackName="TriggerParticle0" eventType="TriggerParticle" guid="91aaf49d-c92c-4481-9957-e3b0448f1479" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Condition id="44" guid="Mod_By_Tran_Thi_Nhung_Mod_132112" status="true" />\r\n      <Event eventName="TriggerParticle" time="0.000" length="1.400" isDuration="true" guid="51311a35-66be-4940-9a41-431050e09e2b">\r\n        <TemplateObject name="targetId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <TemplateObject name="objectSpaceId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <String name="resourceName" value="prefab_skill_effects/hero_skill_effects/132_makeboluo/13210/Makeboluo_spell01_attack_02_1" refParamName="" useRefParam="false" />\r\n        <Vector3i name="scalingInt" x="10000" y="10000" z="10000" refParamName="" useRefParam="false" />\r\n        <String name="syncAnimationName" value="" refParamName="" useRefParam="false" />\r\n        <String name="customTagName" value="" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>\r\n    <Track trackName="TriggerParticle0" eventType="TriggerParticle" guid="91aaf49d-c92c-4481-9957-e3b0448f1479" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Condition id="45" guid="Mod_By_Tran_Thi_Nhung_132113" status="true" />\r\n      <Event eventName="TriggerParticle" time="0.000" length="1.400" isDuration="true" guid="51311a35-66be-4940-9a41-431050e09e2b">\r\n        <TemplateObject name="targetId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <TemplateObject name="objectSpaceId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <String name="resourceName" value="prefab_skill_effects/hero_skill_effects/132_makeboluo/13210/Makeboluo_spell01_attack_03" refParamName="" useRefParam="false" />\r\n        <Vector3i name="scalingInt" x="10000" y="10000" z="10000" refParamName="" useRefParam="false" />\r\n        <String name="syncAnimationName" value="" refParamName="" useRefParam="false" />\r\n        <String name="customTagName" value="" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>\r\n    <Track trackName="TriggerParticle0" eventType="TriggerParticle" guid="91aaf49d-c92c-4481-9957-e3b0448f1479" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Condition id="45" guid="Mod_By_Tran_Thi_Nhung_132113" status="true" />\r\n      <Event eventName="TriggerParticle" time="0.000" length="1.400" isDuration="true" guid="51311a35-66be-4940-9a41-431050e09e2b">\r\n        <TemplateObject name="targetId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <TemplateObject name="objectSpaceId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <String name="resourceName" value="prefab_skill_effects/hero_skill_effects/132_makeboluo/13210/Makeboluo_spell01_attack_03_1" refParamName="" useRefParam="false" />\r\n        <Vector3i name="scalingInt" x="10000" y="10000" z="10000" refParamName="" useRefParam="false" />\r\n        <String name="syncAnimationName" value="" refParamName="" useRefParam="false" />\r\n        <String name="customTagName" value="" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>\r\n    <Track trackName="TriggerParticle0" eventType="TriggerParticle" guid="91aaf49d-c92c-4481-9957-e3b0448f1479" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Condition id="Tran_Thi_Nhung" guid="Mod_By_Tran_Thi_Nhung_Mod_132111" status="false" />\r\n      <Condition id="Tran_Thi_Nhung" guid="Mod_By_Tran_Thi_Nhung_Mod_132112" status="false" />\r\n      <Condition id="Tran_Thi_Nhung" guid="Mod_By_Tran_Thi_Nhung_132113" status="false" />\r\n      <Event eventName="TriggerParticle" time="0.000" length="1.400" isDuration="true" guid="51311a35-66be-4940-9a41-431050e09e2b">\r\n        <TemplateObject name="targetId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <TemplateObject name="objectSpaceId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <String name="resourceName" value="prefab_skill_effects/hero_skill_effects/132_makeboluo/13210/Makeboluo_spell01_attack_01" refParamName="" useRefParam="false" />\r\n        <Vector3i name="scalingInt" x="10000" y="10000" z="10000" refParamName="" useRefParam="false" />\r\n        <String name="syncAnimationName" value="" refParamName="" useRefParam="false" />\r\n        <String name="customTagName" value="" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>\r\n    <Track trackName="TriggerParticle0" eventType="TriggerParticle" guid="91aaf49d-c92c-4481-9957-e3b0448f1479" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Condition id="Tran_Thi_Nhung" guid="Mod_By_Tran_Thi_Nhung_Mod_132111" status="false" />\r\n      <Condition id="Tran_Thi_Nhung" guid="Mod_By_Tran_Thi_Nhung_Mod_132112" status="false" />\r\n      <Condition id="Tran_Thi_Nhung" guid="Mod_By_Tran_Thi_Nhung_132113" status="false" />\r\n      <Event eventName="TriggerParticle" time="0.000" length="1.400" isDuration="true" guid="51311a35-66be-4940-9a41-431050e09e2b">\r\n        <TemplateObject name="targetId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <TemplateObject name="objectSpaceId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <String name="resourceName" value="prefab_skill_effects/hero_skill_effects/132_makeboluo/13210/Makeboluo_spell01_attack_01_1" refParamName="" useRefParam="false" />\r\n        <Vector3i name="scalingInt" x="10000" y="10000" z="10000" refParamName="" useRefParam="false" />\r\n        <String name="syncAnimationName" value="" refParamName="" useRefParam="false" />\r\n        <String name="customTagName" value="" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>\r\n    <Track trackName="T2\xe9\x9a\x8f\xe6\x9c\xba1 \xe9\x9f\xb3\xe6\x95\x88" eventType="PlayHeroSoundTick" guid="f92f38f7-c71a-4ea3-abfc-c8e4eb5b3865" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Condition id="Tran_Thi_Nhung" guid="Mod_By_Tran_Thi_Nhung_Mod_132111" status="true" />\r\n      <Event eventName="PlayHeroSoundTick" time="0.000" isDuration="false" guid="9b862449-dea5-4cee-b1f0-8b1b3724ca8f">\r\n        <TemplateObject name="targetId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <TemplateObject name="sourceId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <String name="eventName" value="Play_13210_Hayate_SkillA_03" refParamName="" useRefParam="false" />\r\n        <bool name="useSkinSwitch" value="false" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>\r\n    <Track trackName="T2\xe9\x9a\x8f\xe6\x9c\xba2 \xe9\x9f\xb3\xe6\x95\x88" eventType="PlayHeroSoundTick" guid="c7107416-30e0-4ee8-83fa-5f97bb948faf" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Condition id="Tran_Thi_Nhung" guid="Mod_By_Tran_Thi_Nhung_Mod_132112" status="true" />\r\n      <Event eventName="PlayHeroSoundTick" time="0.000" isDuration="false" guid="4a8d55af-a3b6-4c1a-b7b9-830ea761ccf9">\r\n        <TemplateObject name="targetId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <TemplateObject name="sourceId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <String name="eventName" value="Play_13210_Hayate_SkillA_01" refParamName="" useRefParam="false" />\r\n        <bool name="useSkinSwitch" value="false" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>\r\n    <Track trackName="T2\xe9\x9a\x8f\xe6\x9c\xba3 \xe9\x9f\xb3\xe6\x95\x88" eventType="PlayHeroSoundTick" guid="bca0dd8d-b83a-49da-982c-6cadaef3966a" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Condition id="Tran_Thi_Nhung" guid="Mod_By_Tran_Thi_Nhung_132113" status="true" />\r\n      <Event eventName="PlayHeroSoundTick" time="0.000" isDuration="false" guid="129a0664-39ba-43af-9d93-43c6b7d64878">\r\n        <TemplateObject name="targetId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <TemplateObject name="sourceId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <String name="eventName" value="Play_13210_Hayate_SkillA_02" refParamName="" useRefParam="false" />\r\n        <bool name="useSkinSwitch" value="false" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>\r\n    <Track trackName="T2\xe9\x9a\x8f\xe6\x9c\xba1 \xe9\x9f\xb3\xe6\x95\x88" eventType="PlayHeroSoundTick" guid="f92f38f7-c71a-4ea3-abfc-c8e4eb5b3865" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Condition id="Tran_Thi_Nhung" guid="Mod_By_Tran_Thi_Nhung_Mod_132111" status="false" />\r\n      <Condition id="Tran_Thi_Nhung" guid="Mod_By_Tran_Thi_Nhung_Mod_132112" status="false" />\r\n      <Condition id="Tran_Thi_Nhung" guid="Mod_By_Tran_Thi_Nhung_132113" status="false" />\r\n      <Event eventName="PlayHeroSoundTick" time="0.000" isDuration="false" guid="9b862449-dea5-4cee-b1f0-8b1b3724ca8f">\r\n        <TemplateObject name="targetId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <TemplateObject name="sourceId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <String name="eventName" value="Play_13210_Hayate_SkillA_03" refParamName="" useRefParam="false" />\r\n        <bool name="useSkinSwitch" value="false" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>\r\n    <Track trackName="T2\xe9\x9a\x8f\xe6\x9c\xba1" eventType="HitTriggerTick" guid="810de6b2-8b68-4614-8762-84bbafe2e77a" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Condition id="Tran_Thi_Nhung" guid="Mod_By_Tran_Thi_Nhung_Mod_132111" status="false" />\r\n      <Condition id="Tran_Thi_Nhung" guid="Mod_By_Tran_Thi_Nhung_Mod_132112" status="false" />\r\n      <Condition id="Tran_Thi_Nhung" guid="Mod_By_Tran_Thi_Nhung_132113" status="false" />\r\n      <Event eventName="HitTriggerTick" time="0.000" isDuration="false" guid="06468bb9-532f-4c15-819f-4ea3434f2a47">\r\n        <TemplateObject name="targetId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <int name="SelfSkillCombineID_1" value="132111" refParamName="" useRefParam="false" />\r\n        <TemplateObject name="triggerId" id="-1" objectName="None" isTemp="false" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>\r\n  </Action>')
                if 'S1B0.xml' in file_path:
                    with open(file_path, 'rb') as f:
                        rpl = f.read()
                        rpl = re.sub(b'"resourceName" value="(.*?)"', b'"resourceName" value="Tran_Thi_Nhung"', rpl)
                        rpl = rpl.replace(b'  </Action>',b'    <Track trackName="1" eventType="CheckSkillCombineConditionTick" guid="Mod_By_Tran_Thi_Nhung_Mod_132111" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Event eventName="CheckSkillCombineConditionTick" time="0.000" isDuration="false" guid="b0dbc04b-5f6d-4610-a37b-b5240f304825">\r\n        <TemplateObject name="targetId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <int name="skillCombineId" value="132111" refParamName="" useRefParam="false" />\r\n        <Enum name="checkOPType" value="3" refParamName="" useRefParam="false" />\r\n        <int name="skillCombineLevel" value="1" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>\r\n    <Track trackName="2" eventType="CheckSkillCombineConditionTick" guid="Mod_By_Tran_Thi_Nhung_Mod_132112" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Event eventName="CheckSkillCombineConditionTick" time="0.000" isDuration="false" guid="fb9ffe1e-fc80-463c-aa04-7e4749711ab8">\r\n        <TemplateObject name="targetId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <int name="skillCombineId" value="132112" refParamName="" useRefParam="false" />\r\n        <Enum name="checkOPType" value="3" refParamName="" useRefParam="false" />\r\n        <int name="skillCombineLevel" value="1" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>\r\n    <Track trackName="3" eventType="CheckSkillCombineConditionTick" guid="Mod_By_Tran_Thi_Nhung_132113" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Event eventName="CheckSkillCombineConditionTick" time="0.000" isDuration="false" guid="6786a65e-f11b-484a-a0ae-613c7521f69e">\r\n        <TemplateObject name="targetId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <int name="skillCombineId" value="132113" refParamName="" useRefParam="false" />\r\n        <Enum name="checkOPType" value="3" refParamName="" useRefParam="false" />\r\n        <int name="skillCombineLevel" value="1" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>\r\n    <Track trackName="TriggerParticle0" eventType="TriggerParticle" guid="91aaf49d-c92c-4481-9957-e3b0448f1479" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Condition id="43" guid="Mod_By_Tran_Thi_Nhung_Mod_132111" status="true" />\r\n      <Event eventName="TriggerParticle" time="0.000" length="1.400" isDuration="true" guid="51311a35-66be-4940-9a41-431050e09e2b">\r\n        <TemplateObject name="targetId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <TemplateObject name="objectSpaceId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <String name="resourceName" value="prefab_skill_effects/hero_skill_effects/132_makeboluo/13210/Makeboluo_spell01_attack_01" refParamName="" useRefParam="false" />\r\n        <Vector3i name="scalingInt" x="10000" y="10000" z="10000" refParamName="" useRefParam="false" />\r\n        <String name="syncAnimationName" value="" refParamName="" useRefParam="false" />\r\n        <String name="customTagName" value="" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>\r\n    <Track trackName="TriggerParticle0" eventType="TriggerParticle" guid="91aaf49d-c92c-4481-9957-e3b0448f1479" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Condition id="43" guid="Mod_By_Tran_Thi_Nhung_Mod_132111" status="true" />\r\n      <Event eventName="TriggerParticle" time="0.000" length="1.400" isDuration="true" guid="51311a35-66be-4940-9a41-431050e09e2b">\r\n        <TemplateObject name="targetId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <TemplateObject name="objectSpaceId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <String name="resourceName" value="prefab_skill_effects/hero_skill_effects/132_makeboluo/13210/Makeboluo_spell01_attack_01_1" refParamName="" useRefParam="false" />\r\n        <Vector3i name="scalingInt" x="10000" y="10000" z="10000" refParamName="" useRefParam="false" />\r\n        <String name="syncAnimationName" value="" refParamName="" useRefParam="false" />\r\n        <String name="customTagName" value="" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>\r\n    <Track trackName="TriggerParticle0" eventType="TriggerParticle" guid="91aaf49d-c92c-4481-9957-e3b0448f1479" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Condition id="44" guid="Mod_By_Tran_Thi_Nhung_Mod_132112" status="true" />\r\n      <Event eventName="TriggerParticle" time="0.000" length="1.400" isDuration="true" guid="51311a35-66be-4940-9a41-431050e09e2b">\r\n        <TemplateObject name="targetId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <TemplateObject name="objectSpaceId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <String name="resourceName" value="prefab_skill_effects/hero_skill_effects/132_makeboluo/13210/Makeboluo_spell01_attack_02" refParamName="" useRefParam="false" />\r\n        <Vector3i name="scalingInt" x="10000" y="10000" z="10000" refParamName="" useRefParam="false" />\r\n        <String name="syncAnimationName" value="" refParamName="" useRefParam="false" />\r\n        <String name="customTagName" value="" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>\r\n    <Track trackName="TriggerParticle0" eventType="TriggerParticle" guid="91aaf49d-c92c-4481-9957-e3b0448f1479" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Condition id="44" guid="Mod_By_Tran_Thi_Nhung_Mod_132112" status="true" />\r\n      <Event eventName="TriggerParticle" time="0.000" length="1.400" isDuration="true" guid="51311a35-66be-4940-9a41-431050e09e2b">\r\n        <TemplateObject name="targetId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <TemplateObject name="objectSpaceId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <String name="resourceName" value="prefab_skill_effects/hero_skill_effects/132_makeboluo/13210/Makeboluo_spell01_attack_02_1" refParamName="" useRefParam="false" />\r\n        <Vector3i name="scalingInt" x="10000" y="10000" z="10000" refParamName="" useRefParam="false" />\r\n        <String name="syncAnimationName" value="" refParamName="" useRefParam="false" />\r\n        <String name="customTagName" value="" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>\r\n    <Track trackName="TriggerParticle0" eventType="TriggerParticle" guid="91aaf49d-c92c-4481-9957-e3b0448f1479" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Condition id="45" guid="Mod_By_Tran_Thi_Nhung_132113" status="true" />\r\n      <Event eventName="TriggerParticle" time="0.000" length="1.400" isDuration="true" guid="51311a35-66be-4940-9a41-431050e09e2b">\r\n        <TemplateObject name="targetId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <TemplateObject name="objectSpaceId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <String name="resourceName" value="prefab_skill_effects/hero_skill_effects/132_makeboluo/13210/Makeboluo_spell01_attack_03" refParamName="" useRefParam="false" />\r\n        <Vector3i name="scalingInt" x="10000" y="10000" z="10000" refParamName="" useRefParam="false" />\r\n        <String name="syncAnimationName" value="" refParamName="" useRefParam="false" />\r\n        <String name="customTagName" value="" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>\r\n    <Track trackName="TriggerParticle0" eventType="TriggerParticle" guid="91aaf49d-c92c-4481-9957-e3b0448f1479" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Condition id="45" guid="Mod_By_Tran_Thi_Nhung_132113" status="true" />\r\n      <Event eventName="TriggerParticle" time="0.000" length="1.400" isDuration="true" guid="51311a35-66be-4940-9a41-431050e09e2b">\r\n        <TemplateObject name="targetId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <TemplateObject name="objectSpaceId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <String name="resourceName" value="prefab_skill_effects/hero_skill_effects/132_makeboluo/13210/Makeboluo_spell01_attack_03_1" refParamName="" useRefParam="false" />\r\n        <Vector3i name="scalingInt" x="10000" y="10000" z="10000" refParamName="" useRefParam="false" />\r\n        <String name="syncAnimationName" value="" refParamName="" useRefParam="false" />\r\n        <String name="customTagName" value="" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>\r\n    <Track trackName="TriggerParticle0" eventType="TriggerParticle" guid="91aaf49d-c92c-4481-9957-e3b0448f1479" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Condition id="Tran_Thi_Nhung" guid="Mod_By_Tran_Thi_Nhung_Mod_132111" status="false" />\r\n      <Condition id="Tran_Thi_Nhung" guid="Mod_By_Tran_Thi_Nhung_Mod_132112" status="false" />\r\n      <Condition id="Tran_Thi_Nhung" guid="Mod_By_Tran_Thi_Nhung_132113" status="false" />\r\n      <Event eventName="TriggerParticle" time="0.000" length="1.400" isDuration="true" guid="51311a35-66be-4940-9a41-431050e09e2b">\r\n        <TemplateObject name="targetId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <TemplateObject name="objectSpaceId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <String name="resourceName" value="prefab_skill_effects/hero_skill_effects/132_makeboluo/13210/Makeboluo_spell01_attack_01" refParamName="" useRefParam="false" />\r\n        <Vector3i name="scalingInt" x="10000" y="10000" z="10000" refParamName="" useRefParam="false" />\r\n        <String name="syncAnimationName" value="" refParamName="" useRefParam="false" />\r\n        <String name="customTagName" value="" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>\r\n    <Track trackName="TriggerParticle0" eventType="TriggerParticle" guid="91aaf49d-c92c-4481-9957-e3b0448f1479" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Condition id="Tran_Thi_Nhung" guid="Mod_By_Tran_Thi_Nhung_Mod_132111" status="false" />\r\n      <Condition id="Tran_Thi_Nhung" guid="Mod_By_Tran_Thi_Nhung_Mod_132112" status="false" />\r\n      <Condition id="Tran_Thi_Nhung" guid="Mod_By_Tran_Thi_Nhung_132113" status="false" />\r\n      <Event eventName="TriggerParticle" time="0.000" length="1.400" isDuration="true" guid="51311a35-66be-4940-9a41-431050e09e2b">\r\n        <TemplateObject name="targetId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <TemplateObject name="objectSpaceId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <String name="resourceName" value="prefab_skill_effects/hero_skill_effects/132_makeboluo/13210/Makeboluo_spell01_attack_01_1" refParamName="" useRefParam="false" />\r\n        <Vector3i name="scalingInt" x="10000" y="10000" z="10000" refParamName="" useRefParam="false" />\r\n        <String name="syncAnimationName" value="" refParamName="" useRefParam="false" />\r\n        <String name="customTagName" value="" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>\r\n    <Track trackName="T2\xe9\x9a\x8f\xe6\x9c\xba1 \xe9\x9f\xb3\xe6\x95\x88" eventType="PlayHeroSoundTick" guid="f92f38f7-c71a-4ea3-abfc-c8e4eb5b3865" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Condition id="Tran_Thi_Nhung" guid="Mod_By_Tran_Thi_Nhung_Mod_132111" status="true" />\r\n      <Event eventName="PlayHeroSoundTick" time="0.000" isDuration="false" guid="9b862449-dea5-4cee-b1f0-8b1b3724ca8f">\r\n        <TemplateObject name="targetId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <TemplateObject name="sourceId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <String name="eventName" value="Play_13210_Hayate_SkillA_03" refParamName="" useRefParam="false" />\r\n        <bool name="useSkinSwitch" value="false" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>\r\n    <Track trackName="T2\xe9\x9a\x8f\xe6\x9c\xba2 \xe9\x9f\xb3\xe6\x95\x88" eventType="PlayHeroSoundTick" guid="c7107416-30e0-4ee8-83fa-5f97bb948faf" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Condition id="Tran_Thi_Nhung" guid="Mod_By_Tran_Thi_Nhung_Mod_132112" status="true" />\r\n      <Event eventName="PlayHeroSoundTick" time="0.000" isDuration="false" guid="4a8d55af-a3b6-4c1a-b7b9-830ea761ccf9">\r\n        <TemplateObject name="targetId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <TemplateObject name="sourceId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <String name="eventName" value="Play_13210_Hayate_SkillA_01" refParamName="" useRefParam="false" />\r\n        <bool name="useSkinSwitch" value="false" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>\r\n    <Track trackName="T2\xe9\x9a\x8f\xe6\x9c\xba3 \xe9\x9f\xb3\xe6\x95\x88" eventType="PlayHeroSoundTick" guid="bca0dd8d-b83a-49da-982c-6cadaef3966a" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Condition id="Tran_Thi_Nhung" guid="Mod_By_Tran_Thi_Nhung_132113" status="true" />\r\n      <Event eventName="PlayHeroSoundTick" time="0.000" isDuration="false" guid="129a0664-39ba-43af-9d93-43c6b7d64878">\r\n        <TemplateObject name="targetId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <TemplateObject name="sourceId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <String name="eventName" value="Play_13210_Hayate_SkillA_02" refParamName="" useRefParam="false" />\r\n        <bool name="useSkinSwitch" value="false" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>\r\n    <Track trackName="T2\xe9\x9a\x8f\xe6\x9c\xba1 \xe9\x9f\xb3\xe6\x95\x88" eventType="PlayHeroSoundTick" guid="f92f38f7-c71a-4ea3-abfc-c8e4eb5b3865" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Condition id="Tran_Thi_Nhung" guid="Mod_By_Tran_Thi_Nhung_Mod_132111" status="false" />\r\n      <Condition id="Tran_Thi_Nhung" guid="Mod_By_Tran_Thi_Nhung_Mod_132112" status="false" />\r\n      <Condition id="Tran_Thi_Nhung" guid="Mod_By_Tran_Thi_Nhung_132113" status="false" />\r\n      <Event eventName="PlayHeroSoundTick" time="0.000" isDuration="false" guid="9b862449-dea5-4cee-b1f0-8b1b3724ca8f">\r\n        <TemplateObject name="targetId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <TemplateObject name="sourceId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <String name="eventName" value="Play_13210_Hayate_SkillA_03" refParamName="" useRefParam="false" />\r\n        <bool name="useSkinSwitch" value="false" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>\r\n    <Track trackName="T2\xe9\x9a\x8f\xe6\x9c\xba1" eventType="HitTriggerTick" guid="810de6b2-8b68-4614-8762-84bbafe2e77a" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Condition id="Tran_Thi_Nhung" guid="Mod_By_Tran_Thi_Nhung_Mod_132111" status="false" />\r\n      <Condition id="Tran_Thi_Nhung" guid="Mod_By_Tran_Thi_Nhung_Mod_132112" status="false" />\r\n      <Condition id="Tran_Thi_Nhung" guid="Mod_By_Tran_Thi_Nhung_132113" status="false" />\r\n      <Event eventName="HitTriggerTick" time="0.000" isDuration="false" guid="06468bb9-532f-4c15-819f-4ea3434f2a47">\r\n        <TemplateObject name="targetId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <int name="SelfSkillCombineID_1" value="132111" refParamName="" useRefParam="false" />\r\n        <TemplateObject name="triggerId" id="-1" objectName="None" isTemp="false" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>\r\n  </Action>')
                with open(file_path, 'wb') as f:
                    f.write(rpl)
#---------------—------------———----------------
            if IDMODSKIN == '52113':
                with open(file_path, 'rb') as f:
                    rpl = f.read()
                    rpl = re.sub(b'<String name="prefabName" value="Prefab_Skill_Effects/Hero_Skill_Effects/521_Florentino/52113_Florentino_BianShen" refParamName="" useRefParam="false" />', b'<String name="prefabName" value="Prefab_Skill_Effects/Hero_Skill_Effects/521_Florentino/52113/52113_Florentino_BianShen" refParamName="" useRefParam="false" />', rpl, flags=re.IGNORECASE)
                with open(file_path, 'wb') as f:
                    f.write(rpl)
#-----------------------------------------------
    IDNODMODCHECK = ['54309' ,'13210', '13011', '52414', '15013', '13314', '13706','59901','13213','11215','59802','10915','15412','10611','10620','11120', '15710','54804','17408','52113','13118','11119','56301','15903','15015','54402','16707', '19908', '53702', '59902','14120','13316','15905','15217']
    
    if IDCHECK not in IDNODMODCHECK:
        directorypath = Files_Directory_Path + f'{NAME_HERO}' + '/skill/'
        files_list = os.listdir(directorypath)
        
        for filename in files_list:
            filecheck = os.path.join(directorypath, filename)
        
            if not os.path.isfile(filecheck):
                continue  
        
            with open(filecheck, 'rb') as f:
                All = f.read()

            
            # --- Xử lý đặc biệt cho các ID trong list này ---
            if IDMODSKIN in ['14111'] and filename not in ['S1.xml', 'S1B1.xml', 'S1B2.xml', 'S1B11.xml', 'S1B12.xml', 'S1B21.xml', 'S1B22.xml']:

                rpl = All.replace(
                        b'\r\n        <int name="skinId" value="14111" refParamName="" useRefParam="false" />\r\n        <bool name="bEqual" value="false" refParamName="" useRefParam="false" />\r\n        <bool name="bSkipLogicCheck" value="true" refParamName="" useRefParam="false" />',
                        b'\r\n        <int name="skinId" value="14111" refParamName="" useRefParam="false" />\r\n        <<<bool name="bEqual" value="false" refParamName="" useRefParam="false" />>>\r\n        <bool name="bSkipLogicCheck" value="true" refParamName="" useRefParam="false" />'
                    ).replace(
                        b'\r\n        <int name="skinId" value="14111" refParamName="" useRefParam="false" />\r\n        <bool name="bSkipLogicCheck" value="true" refParamName="" useRefParam="false" />',
                        b'\r\n        <int name="skinId" value="14111" refParamName="" useRefParam="false" />\r\n        <bool name="bEqual" value="false" refParamName="" useRefParam="false" />\r\n        <bool name="bSkipLogicCheck" value="true" refParamName="" useRefParam="false" />'
                    ).replace(
                        b'\r\n        <int name="skinId" value="14111" refParamName="" useRefParam="false" />\r\n        <<<bool name="bEqual" value="false" refParamName="" useRefParam="false" />>>\r\n        <bool name="bSkipLogicCheck" value="true" refParamName="" useRefParam="false" />',
                        b'\r\n        <int name="skinId" value="14111" refParamName="" useRefParam="false" />\r\n        <bool name="bSkipLogicCheck" value="true" refParamName="" useRefParam="false" />'
                    )
                with open(filecheck, 'wb') as f:
                    f.write(rpl)
                continue  # Skip file này, KHÔNG xử lý CheckSkinIdTick & FixSkinAvatar
    
            # --- Xử lý CheckSkinIdTick ---
            CheckSkinIdTick = (
                '<int name="skinId" value="' + IDMODSKIN + '" refParamName="" useRefParam="false" />'
            ).encode()
            CheckSkinIdTick0 = (
                '<int name="skinId" value="' + IDMODSKIN[:3] + '00" refParamName="" useRefParam="false" />'
            ).encode()
            if CheckSkinIdTick in All:
                All = All.replace(CheckSkinIdTick, CheckSkinIdTick0)
                print(f'CheckSkinIdTick : {filename}')
    
            # --- Xử lý FixSkinAvatar ---
            FixSkinAvatar = ('<SkinOrAvatarList id="' + IDMODSKIN + '" />').encode()
            FixSkinAvatar1 = ('<SkinOrAvatarList id="' + IDMODSKIN[:3] + '00" />').encode()
            if FixSkinAvatar in All:
                All = All.replace(FixSkinAvatar, FixSkinAvatar1)
            with open(filecheck, 'wb') as f:
                f.write(All)
#-----------------------------------------------
    if IDCHECK == '53002' or b"Skin_Icon_SoundEffect" in dieukienmod or b"Skin_Icon_Dialogue" in dieukienmod:
    
        if IDCHECK not in ["13311", "16707"]:
            directory_path = Files_Directory_Path + f'{NAME_HERO}' + '/skill/'
            o = directory_path
            IDL = (IDSOUND)
            File = os.listdir(o)
            for file in File:
                giai(o + file)
                with open(o + file, 'rb') as f:
                    rpl = f.readlines()
                with open(o + file, 'rb') as f:
                    Rpl = f.read()
    
                Code = []
                for i in rpl:
                    if i.find(b'<String name="eventName" value="') != -1:
                        Code.append(i[40:i.find(b'" refParamName="" useRefParam="false" />')])
    
                for i in Code:
                    a = b'<String name="eventName" value="' + i + b'" refParamName="" useRefParam="false" />'
                    if Code == []:
                        pass
                    else:
                        if IDSOUND in i:
                            continue
                        if IDCHECK == "11620":
                            Rpl = Rpl.replace(
                                a,
                                b'<String name="eventName" value="' + i + IDSOUND + b'_AW5" refParamName="" useRefParam="false" />'
                            )
                        else:
                            Rpl = Rpl.replace(
                                a,
                                b'<String name="eventName" value="' + i + IDSOUND + b'" refParamName="" useRefParam="false" />'
                            )
    
                with open(o + file, 'wb') as f:
                    f.write(Rpl)
    
            print('    Mod Sound : Done')
    
            def remove_extra_skin_array(file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        text = f.read()
                except UnicodeDecodeError:
                    return
    
                lines = text.splitlines()
                processed_lines = []
                inside_event = False
                in_extraskin_block = False
    
                for line in lines:
                    stripped = line.strip()
    
                    if '<Event eventName="PlayHeroSoundTick"' in stripped:
                        inside_event = True
                    if '</Event>' in stripped and inside_event:
                        inside_event = False
    
                    if inside_event and '<Array name="extraSkinId"' in stripped and '/>' in stripped:
                        continue
                    if inside_event and '<Array name="extraSkinId"' in stripped and '/>' not in stripped:
                        in_extraskin_block = True
                        continue
                    if in_extraskin_block:
                        if '</Array>' in stripped:
                            in_extraskin_block = False
                        continue
    
                    processed_lines.append(line)
    
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write('\n'.join(processed_lines))
    
            def remove_extra_skin_array_in_folder(directory_path):
                for filename in os.listdir(directory_path):
                    if filename.endswith('.xml'):
                        file_path = os.path.join(directory_path, filename)
                        remove_extra_skin_array(file_path)
    
            if os.path.isdir(directory_path):
                remove_extra_skin_array_in_folder(directory_path)

    Kiem_Tra_Code = os.path.join(Files_Directory_Path, f'{NAME_HERO}', 'skill')
    for file in os.listdir(Kiem_Tra_Code):
        File_Check_Code = os.path.join(Kiem_Tra_Code, file)
        if IDMODSKIN == '59902':
            with open(File_Check_Code, 'rb') as f:
                rpl = f.read().replace
        if IDMODSKIN == '11620':
            Component(File_Check_Code)
        if IDMODSKIN =='59702':
            with open(File_Check_Code, 'rb') as f:
                rpl = f.read().replace(b'SkinAvatarFilterType="9">',
                    b'SkinAvatarFilterType="X">').replace(b'SkinAvatarFilterType="11">',
                    b'SkinAvatarFilterType="9">').replace(b'SkinAvatarFilterType="X">',
                    b'SkinAvatarFilterType="11">')
            with open(File_Check_Code, 'wb') as f:
                f.write(rpl)
        
        if IDCHECK == '11215' and file in ["A1B1.xml", "A1B2.xml", "A2B1.xml", "A2B2.xml", "A3B1.xml", "A3B2.xml", "A4B1.xml", "A4B2.xml", "S1B1.xml"]:   
            with open(File_Check_Code, 'rb') as f:
                rpl = f.read()
            tracks = rpl.split(b"</Track>")
            modified_tracks = []
            for track in tracks:
                if (b'MoveBulletDuration' in track or b'SpawnObjectDuration' in track):
                    modified_tracks.append(track + b"</Track>")
                else:
                    track = (track.replace(b'<SkinOrAvatarList id="11215" />',b''))
                    modified_tracks.append(track + b"</Track>")      
            rpl = b"".join(modified_tracks)    
            if rpl.endswith(b"</Track>"):
                rpl = rpl[:-8]                            
            with open(File_Check_Code, 'wb') as f:
                f.write(rpl)                                   	
        if IDCHECK == '11215' and file not in ["A1B1.xml", "A1B2.xml", "A2B1.xml", "A2B2.xml", "A3B1.xml", "A3B2.xml", "A4B1.xml", "A4B2.xml", "S1B1.xml"]:
            with open(File_Check_Code, 'rb') as f:
                rpl = f.read()
            tracks = rpl.split(b"</Track>")
            modified_tracks = []
            for track in tracks:
                track = (track.replace(b'<SkinOrAvatarList id="11215" />',b''))
                modified_tracks.append(track + b"</Track>")
            rpl = b"".join(modified_tracks)    
            if rpl.endswith(b"</Track>"):
                rpl = rpl[:-8]                            
            with open(File_Check_Code, 'wb') as f:
                f.write(rpl)                                      
        if IDMODSKIN == '11215' and 'S1B1.xml' in file:  
            with open(File_Check_Code, 'rb') as f: rpl = f.read().replace(b'  </Action>', b'    <Track trackName="SpawnLiteObjDuration0" eventType="SpawnLiteObjDuration" guid="c890e4ed-8300-4e21-8d66-757283ec3cc0" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" SkinAvatarFilterType="11">\r\n      <Event eventName="SpawnLiteObjDuration" time="0.000" length="0.571" isDuration="true" guid="36200992-6a48-47a7-95c6-c2e352151ff4">\r\n        <String name="OutputLiteBulletName" value="112s1b1" refParamName="" useRefParam="false" />\r\n        <uint name="ConfigID" value="11215235" refParamName="" useRefParam="false" />\r\n        <TemplateObject name="ReferenceID" objectName="self" id="0" isTemp="false" refParamName="" useRefParam="false" />\r\n        <TemplateObject name="TargetID" objectName="bullet" id="2" isTemp="false" refParamName="" useRefParam="false" />\r\n      </Event>\r\n      <SkinOrAvatarList id="11215" />\r\n    </Track>\r\n  </Action>')
            with open(File_Check_Code,'wb') as f: f.write(rpl)
        if IDCHECK == '54309':
            with open(File_Check_Code, "rb") as f:
                All = f.read()
        
            tracks = re.findall(rb'(<Track trackName=".*?</Track>)', All, flags=re.DOTALL)
        
            for t in tracks:
                t_low = t.lower()
                if b"simplespawnbufftick" in t_low or b"changeanimduration" in t_low:

                    continue
                All = All.replace(t, t.replace(b'<SkinOrAvatarList id="54309" />',
                                               b''))
        
            with open(File_Check_Code, "wb") as f:
                f.write(All)
        
        if IDMODSKIN == '13706':
            with open(File_Check_Code, "rb") as f:
                All = f.read()
    
            tracks = re.findall(rb'(<Track trackName=".*?</Track>)', All, flags=re.DOTALL)
            for t in tracks:
                t_low = t.lower()
                if (b"changeskilltriggertick" in t_low or b"setattackdirduration" in t_low):
                    continue
    
                All = All.replace(
                    t,
                    t.replace(b'<SkinOrAvatarList id="13706" />', b'')
                )
    
            with open(File_Check_Code, "wb") as f:
                f.write(All)
        if IDMODSKIN == '15905':
            with open(File_Check_Code, "rb") as f:
                All = f.read()
        
            tracks = re.findall(rb'(<Track trackName=".*?</Track>)', All, flags=re.DOTALL)
        
            for t in tracks:
        
                if (b'SpawnObjectDuration' in t):
                    continue
        
                All = All.replace(
                    t,
                    t.replace(b'<SkinOrAvatarList id="15905" />', b'')
                )
        
            with open(File_Check_Code, "wb") as f:
                f.write(All)

        if IDMODSKIN in ['14120']:
            with open(File_Check_Code, "rb") as f:
                All = f.read()
        
            tracks = re.findall(rb'(<Track trackName=".*?</Track>)', All, flags=re.DOTALL)
        
            for t in tracks:
        
                if (b'enabled="false"' in t or b'SpawnObjectDuration' in t):
                    continue
        
                All = All.replace(
                    t,
                    t.replace(b'<SkinOrAvatarList id="'+IDCHECK.encode()+b'" />', b'')
                )
        
            with open(File_Check_Code, "wb") as f:
                f.write(All)
        if IDMODSKIN in ['13316']:
            with open(File_Check_Code, "rb") as f:
                All = f.read()
        
            tracks = re.findall(rb'(<Track trackName=".*?</Track>)', All, flags=re.DOTALL)
        
            for t in tracks:
        
                if (b'NewVariableIntCompareTick' in t or b'StopTrack' in t or b'<SkinOrAvatarList id="13316" />' in t):
                    continue
        
                All = All.replace(
                    t,
                    t.replace(b'<SkinOrAvatarList id="'+IDCHECK.encode()+b'" />', b'<SkinOrAvatarList id="20916" />').replace(b'SkinAvatarFilterType="9">',b'SkinAvatarFilterType="8">').replace(b'SkinAvatarFilterType="11">',b'SkinAvatarFilterType="9">').replace(b'SkinAvatarFilterType="8">',b'SkinAvatarFilterType="11">')
                )
        
            with open(File_Check_Code, "wb") as f:
                f.write(All)
                
        if IDMODSKIN == '15217':
            with open(File_Check_Code, "rb") as f:
                All = f.read()
        
            tracks = re.findall(rb'(<Track trackName=".*?</Track>)', All, flags=re.DOTALL)
        
            for t in tracks:
        
                if (b'CheckSkinIdTick' in t or b'guid="913521f7-05f3-4a60-9485-4717fc9fe4bd" enabled="false"' in t or b'guid="536375a7-2c90-43d5-9262-dae3e8b9dd02" enabled="false"' in t or b'guid="00cf55e5-3ed1-4e18-8f87-4531e04b8059" enabled="false"' in t or b'guid="75907920-ac95-48f1-8200-ba669728c89a" enabled="false"' in t):
                    continue
        
                All = All.replace(
                    t,
                    t.replace(b'<SkinOrAvatarList id="15217" />', b'')
                )
        
            with open(File_Check_Code, "wb") as f:
                f.write(All)
        if IDMODSKIN[:3] == '537' and 'Change.xml' in file or IDMODSKIN[:3] == '537' and 'ChangeB.xml' in file:
            with open(File_Check_Code, "rb") as f:
                rpl = f.read().replace(b'537_Trip/', b'537_Trip/' + IDMODSKIN.encode() + b'/')
            with open(File_Check_Code, "wb") as f:
                f.write(rpl)
        if IDMODSKIN in ['54805','11620','17408','52113']:
            with open(File_Check_Code, "rb") as f:
                All = f.read()
                All = All.replace(b'<SkinOrAvatarList id="' + IDMODSKIN.encode() + b'" />', b'')
            with open(File_Check_Code, "wb") as f:
                f.write(All)

        if IDCHECK == '11120' and file not in ['A2b2.xml', 'A4b2.xml', 'A1b2.xml', 'S2.xml', 'A1B1.xml', 'A4B1.xml', 'A2B1.xml']:
            with open(File_Check_Code, "rb") as f:
                All = f.read()
                All = All.replace(b'<SkinOrAvatarList id="11120" />',b'<SkinOrAvatarList id="23720" />').replace(b'SkinAvatarFilterType="9">',
b'SkinAvatarFilterType="X">').replace(b'SkinAvatarFilterType="11">',b'SkinAvatarFilterType="9">').replace(b'SkinAvatarFilterType="X">',b'SkinAvatarFilterType="11">')
            with open(File_Check_Code, "wb") as f:
                f.write(All)
        if IDCHECK == '10915' and 'U1E1.xml' not in file:
            with open(File_Check_Code, "rb") as f:
                All = f.read()
            
            pattern = rb'(<Track trackName=".*?</Track>)'
            matches = re.findall(pattern, All, re.DOTALL)
            
            for track_content in matches:
                if (
                    b'<int name="changeSkillID" value="10902"' in track_content
                    or b'<int name="changeSkillID" value="10900"' in track_content
                    or b'<bool name="bImmeStop" value="true"' in track_content
                ):
                    continue 
    
                if b'<SkinOrAvatarList id="10915" />' in track_content:
                    new_track = track_content.replace(b'<SkinOrAvatarList id="10915" />', b'')
                    All = All.replace(track_content, new_track)
            
            with open(File_Check_Code, "wb") as f:
                f.write(All)
            
        if IDMODSKIN == '14111' and 'S1.xml' in file:
            with open(File_Check_Code, "rb") as f:
                All = f.read()
                All = All.replace(b'14100',b'14111')
            with open(File_Check_Code, "wb") as f:
                f.write(All)

        if IDCHECK == '59802':
            with open(File_Check_Code, "rb") as f:
                All = f.read()
        
            tracks = re.findall(rb'(<Track trackName=".*?</Track>)', All, flags=re.DOTALL)
        
            for t in tracks:
                t_low = t.lower()
                if b"random" in t_low or b"spawnobjectduration" in t_low or b"spawnbullettick" in t_low or b"filtertargettype" in t_low or b"checkenergyconditionduration0" in t_low or b"setmaterialparamsduration" in t_low or b"setactorhudscaleduration0" in t_low or b"hittriggertick" in t_low or b"removebufftick0" in t_low or b"stoptrack" in t_low:

                    continue
                All = All.replace(t, t.replace(b'<SkinOrAvatarList id="59802" />',
                                               b''))
        
            with open(File_Check_Code, "wb") as f:
                f.write(All)

        if IDMODSKIN == '56301':
            with open(File_Check_Code, "rb") as f:
                All = f.read()
    
            tracks = re.findall(rb'(<Track trackName=".*?</Track>)', All, flags=re.DOTALL)
            for t in tracks:
                t_low = t.lower()
                if (b"stoptrack" in t_low or b"spawnobjectduration" in t_low or
                    b"spawnbullettick" in t_low or b"setactorvisibilitytick" in t_low or
                    b"simplespawnbufftick" in t_low or b'checkskillcombineconditiontick' in t_low):
                    continue
    
                All = All.replace(
                    t,
                    t.replace(b'<SkinOrAvatarList id="56301" />', b'')
                )
    
            with open(File_Check_Code, "wb") as f:
                f.write(All)
        if IDMODSKIN == '15903':
            with open(File_Check_Code, "rb") as f:
                All = f.read()
    
            tracks = re.findall(rb'(<Track trackName=".*?</Track>)', All, flags=re.DOTALL)
            for t in tracks:
                t_low = t.lower()
                if (b"filtertargettype" in t_low or b"spawnobjectduration" in t_low or
                    b"spawnbullettick" in t_low or b"setactorvisibilitytick" in t_low or
                    b"simplespawnbufftick" in t_low or b'checkskillcombineconditiontick' in t_low or b'stoptrack' in t_low):
                    continue
    
                All = All.replace(
                    t,
                    t.replace(b'<SkinOrAvatarList id="15903" />', b'')
                )
    
            with open(File_Check_Code, "wb") as f:
                f.write(All)
        if IDCHECK == '59901' and file not in ['S1B1.xml','Back.xml','P10E2.xml']:
          with open(File_Check_Code,"rb") as f:
            data=f.read()
            tn=[b"random",b"scalemeshduration0",b"spawnobjectduration",b"spawnbullettick",
                b'guid="12d7aef8-3082-4aba-b52d-9af5c9a9053e"',b'<int name="skillid" value="59900"',
                b"setcollisiontick",b"removebufftick",b"hittrigger",b"checkskillidtick"]
            out=b"";p=0
            for m in re.finditer(rb'<Track trackName=".*?</Track>',data,flags=re.DOTALL):
              s,e=m.span();b=data[s:e]
              if not any(t in b.lower() for t in tn):
                b=b.replace(b'<SkinOrAvatarList id="59901" />',b'')
                print(b,"\n"+"-"*40)
              out+=data[p:s]+b;p=e
            out+=data[p:]
            with open(File_Check_Code,"wb") as f:f.write(out)
        if IDCHECK == '59902' and file not in ['P10E2.xml']:
          with open(File_Check_Code,"rb") as f:
            data=f.read()
            tn=[b"BillowNoPro"]
            out=b"";p=0
            for m in re.finditer(rb'<Track trackName=".*?</Track>',data,flags=re.DOTALL):
              s,e=m.span();b=data[s:e]
              if not any(t in b.lower() for t in tn):
                b=b.replace(b'<SkinOrAvatarList id="59902" />',b'')
                print(b,"\n"+"-"*40)
              out+=data[p:s]+b;p=e
            out+=data[p:]
            with open(File_Check_Code,"wb") as f:f.write(out)
        if IDCHECK == '13314' and 'skin14E2.xml' in file:
            with open(File_Check_Code, 'rb') as f:
                rpl = f.read()
                rpl = rpl.replace(b'SkinAvatarFilterType="9">',b'SkinAvatarFilterType="11">').replace(b'<String name="prefab" value="prefab_characters/prefab_hero/133_DiRenJie/DiRenJie_spell03_cutin01" refParamName="" useRefParam="false" />',b'<String name="prefab" value="prefab_skill_effects/hero_skill_effects/133_DiRenJie/13314/DiRenJie_spell03_cutin01" refParamName="" useRefParam="false" />')
            with open(File_Check_Code, 'wb') as f:
                f.write(rpl)
        if IDCHECK == '13213':
            if file in ['A1.xml', 'A2.xml', 'A3.xml','Death.xml', 'P1E42.xml','P1E51.xml','PassiveE3.xml','S1E1.xml','S2.xml','S11B0.xml','S12B0.xml','U1.xml','U2.xml','U3.xml']:
                with open(File_Check_Code, 'rb') as f:
                    A1_CheckFile13213Code = f.read().replace(b'<SkinOrAvatarList id="13213" />',b'')
                    
                with open(File_Check_Code, 'wb') as f:
                    f.write(A1_CheckFile13213Code)
            if 'S1B0.xml' in file:
                with open(File_Check_Code, 'rb') as f:
                    S1B0_CheckFile13213Code = f.read().replace(b'<SkinOrAvatarList id="13213" />',b'',2)
                with open(File_Check_Code, 'wb') as f:
                    f.write(S1B0_CheckFile13213Code)
            if 'S1B1.xml' in file:
                with open(File_Check_Code, 'rb') as f:
                    S1B1_CheckFile13213Code = f.read().replace(b'  </Action>',b'    <Track trackName="TriggerParticle6" eventType="TriggerParticle" guid="536a47d0-fdc5-441e-b382-53866c442844" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" SkinAvatarFilterType="11">\n      <Event eventName="TriggerParticle" time="0.000" length="0.700" isDuration="true" guid="38ee198d-1e31-45e7-857a-06c00d811da8">\n        <TemplateObject name="targetId" objectName="bullet" id="2" isTemp="true" refParamName="" useRefParam="false"/>\n        <String name="resourceName" value="prefab_skill_effects/hero_skill_effects/132_makeboluo/13213/makeboluo_attack_spell01h" refParamName="" useRefParam="false"/>\n        <String name="resourceName2" value="prefab_skill_effects/hero_skill_effects/132_makeboluo/13213/makeboluo_attack_spell01a" refParamName="" useRefParam="false"/>\n        <String name="resourceName3" value="prefab_skill_effects/hero_skill_effects/132_makeboluo/13213/makeboluo_attack_spell01g" refParamName="" useRefParam="false"/>\n        <Vector3i name="scalingInt" x="10000" y="10000" z="10000" refParamName="" useRefParam="false"/>\n        <String name="syncAnimationName" value="" refParamName="" useRefParam="false"/>\n        <String name="customTagName" value="" refParamName="" useRefParam="false"/>\n      </Event>\n    </Track>\n  </Action>')
                with open(File_Check_Code, 'wb') as f:
                    f.write(S1B1_CheckFile13213Code)
        if IDMODSKIN == '52414':
            with open(File_Check_Code, "rb") as f:
                All = f.read()
    
            tracks = re.findall(rb'(<Track trackName=".*?</Track>)', All, flags=re.DOTALL)
            for t in tracks:
                t_low = t.lower()
                if (b"spawnobjectduration" in t_low):
                    continue
    
                All = All.replace(
                    t,
                    t.replace(b'<SkinOrAvatarList id="52414" />', b'<SkinOrAvatarList id="99999" />').replace(b'SkinAvatarFilterType="9">',
                    b'SkinAvatarFilterType="X">').replace(b'SkinAvatarFilterType="11">',
                    b'SkinAvatarFilterType="9">').replace(b'SkinAvatarFilterType="X">',
                    b'SkinAvatarFilterType="11">')
                )
    
            with open(File_Check_Code, "wb") as f:
                f.write(All)
        if IDCHECK == '52414' and 'A1B1.xml' in file:
            with open(File_Check_Code, "rb") as f:
                All = f.read()
                All=All.replace(b'prefab_skill_effects/hero_skill_effects/524_Capheny/52414/Atk1_Bullet',b'prefab_skill_effects/hero_skill_effects/524_Capheny/Atk1_Bullet')
            with open(File_Check_Code, "wb") as f:
                f.write(All)
        if IDCHECK == '52414' and 'S1E1.xml' in file:
            with open(File_Check_Code, "rb") as f:
                All = f.read()
                All=All.replace(b'52414/',b'')
            with open(File_Check_Code, "wb") as f:
                f.write(All)
        if IDCHECK == '52414' and 'A1B12.xml' in file:
            guid = [
                b"e62e4da6-5140-4bf8-8c3f-1926628bb9c6",
                b"35a52ad3-ee5f-4502-b907-7f8e7e2027c9"
            ]
            
            with open(File_Check_Code, "rb") as f:
                context = f.read()
            
            tracks = re.findall(rb'<Track trackName="(.*?)</Track>', context, re.DOTALL)
            
            for g in guid:
                for b in tracks:
                    if g in b and b"52414/" in b:
                        new_block = b.replace(b"52414/", b"")
                        context = context.replace(b, new_block)
            
            with open(File_Check_Code, "wb") as f:
                f.write(context)
        if IDCHECK == '52414':
        
            if 'A2B1.xml' in file:
                guid = [
                    b"142fea44-be35-4d7b-bfac-e3200015e061",
                    b"13e9d9bb-c992-4645-b350-fc7d2ebb8738"
                ]
        
            elif 'A2B1_1.xml' in file:
                guid = [
                    b"5ba58824-3f17-4a0b-8a23-036e4ba261ee"
                ]
        
            elif 'S1E2.xml' in file:
                guid = [
                    b"4aeed5e1-d9ad-4484-8ddc-dc2323bb9abd",
                    b"a73e4d18-7609-45c0-a202-2e345658a3b8",
                    b"2c836540-8287-45e2-9c10-ab1fbb9cb088"
                ]
            else:
                guid = []
        
            if guid:
                with open(File_Check_Code, "rb") as f:
                    context = f.read()
        
                tracks = re.findall(rb'<Track trackName="(.*?)</Track>', context, re.DOTALL)
        
                for g in guid:
                    for b in tracks:
                        if g in b and b"52414/" in b:
                            new_block = b.replace(b"52414/", b"")
                            context = context.replace(b, new_block)
        
                with open(File_Check_Code, "wb") as f:
                    f.write(context)

        if IDCHECK == '52414' and 'S3B2.xml' in file:
            with open(File_Check_Code, 'rb') as f:
                rpl = f.read()
                rpl = rpl.replace(b'<Track trackName="SpawnObjectDuration0" eventType="SpawnObjectDuration" guid="4f8b0297-5520-4d64-969c-42a86ab30a85" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">',b'<Track trackName="SpawnObjectDuration0" eventType="SpawnObjectDuration" guid="4f8b0297-5520-4d64-969c-42a86ab30a85" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true" SkinAvatarFilterType="9">').replace(b'</Event>',b'</Event>\n    <SkinOrAvatarList id="52414"/>',1)
            with open(File_Check_Code, 'wb') as f:
                f.write(rpl)
        if IDCHECK == '19908':
          with open(File_Check_Code,"rb") as f:
            data=f.read()
            tn=[b"setobjbehaviourmodeick"]
            out=b"";p=0
            for m in re.finditer(rb'<Track trackName=".*?</Track>',data,flags=re.DOTALL):
              s,e=m.span();b=data[s:e]
              if not any(t in b.lower() for t in tn):
                b=b.replace(b'<SkinOrAvatarList id="19908" />',b'')
                print(b,"\n"+"-"*40)
              out+=data[p:s]+b;p=e
            out+=data[p:]
            with open(File_Check_Code,"wb") as f:f.write(out)
        if IDCHECK == '19908' and 'S1.xml' in file:
            with open(File_Check_Code, 'rb') as f:
                rpl = f.read()
                rpl = rpl.replace(b'<String name="resourceName" value="prefab_skill_effects/hero_skill_effects/199_Li/19908/li_attack01_spll01" refParamName="" useRefParam="false" />',b'<String name="resourceName" value="prefab_skill_effects/hero_skill_effects/199_Li/19908/li_attack01_spll01" refParamName="" useRefParam="false" />\r\n        <String name="resourceName2" value="prefab_skill_effects/hero_skill_effects/199_Li/19908/li_attack01_spll01_Water" refParamName="" useRefParam="false" />').replace(b'<String name="resourceName" value="prefab_skill_effects/hero_skill_effects/199_Li/19908/li_attack_spell01c" refParamName="" useRefParam="false" />',b'<String name="resourceName" value="prefab_skill_effects/hero_skill_effects/199_Li/19908/li_attack_spell01c" refParamName="" useRefParam="false" />\r\n        <String name="resourceName2" value="prefab_skill_effects/hero_skill_effects/199_Li/19908/Li_attack_spell01c_Water" refParamName="" useRefParam="false" />')
            with open(File_Check_Code, 'wb') as f:
                f.write(rpl)
        if IDCHECK == '19908' and 'S1B1.xml' in file:
            with open(File_Check_Code, 'rb') as f:
                rpl = f.read()
                rpl = rpl.replace(b'<String name="resourceName" value="prefab_skill_effects/hero_skill_effects/199_Li/19908/li_attack_spell01" refParamName="" useRefParam="false" />',b'<String name="resourceName" value="prefab_skill_effects/hero_skill_effects/199_Li/19908/li_attack_spell01" refParamName="" useRefParam="false" />\r\n        <String name="resourceName2" value="prefab_skill_effects/hero_skill_effects/199_Li/19908/li_attack_spell01_Water" refParamName="" useRefParam="false" />').replace(b'<String name="resourceName" value="prefab_skill_effects/hero_skill_effects/199_Li/19908/li_attack_spell01_e" refParamName="" useRefParam="false" />',b'<String name="resourceName" value="prefab_skill_effects/hero_skill_effects/199_Li/19908/li_attack_spell01_e" refParamName="" useRefParam="false" />\r\n        <String name="resourceName2" value="prefab_skill_effects/hero_skill_effects/199_Li/19908/li_attack_spell01_e_Water" refParamName="" useRefParam="false" />').replace(b'<String name="resourceName" value="prefab_skill_effects/hero_skill_effects/199_Li/19908/li_attack_spell01d" refParamName="" useRefParam="false" />',b'<String name="resourceName" value="prefab_skill_effects/hero_skill_effects/199_Li/19908/li_attack_spell01d" refParamName="" useRefParam="false" />\r\n        <String name="resourceName2" value="prefab_skill_effects/hero_skill_effects/199_Li/19908/li_attack_spell01d_Water" refParamName="" useRefParam="false" />').replace(b'<String name="resourceName" value="prefab_skill_effects/hero_skill_effects/199_Li/19908/li_attack_spell01d_E" refParamName="" useRefParam="false" />',b'<String name="resourceName" value="prefab_skill_effects/hero_skill_effects/199_Li/19908/li_attack_spell01d_E" refParamName="" useRefParam="false" />\r\n        <String name="resourceName2" value="prefab_skill_effects/hero_skill_effects/199_Li/19908/li_attack_spell01d_E_Water" refParamName="" useRefParam="false" />')
            with open(File_Check_Code, 'wb') as f:
                f.write(rpl)
        if IDCHECK == '19908' and 'S2B0.xml' in file:
            with open(File_Check_Code, 'rb') as f:
                rpl = f.read()
                rpl = rpl.replace(b'<String name="resourceName" value="prefab_skill_effects/hero_skill_effects/199_Li/19908/li_attack_spell02b" refParamName="" useRefParam="false" />',b'<String name="resourceName" value="prefab_skill_effects/hero_skill_effects/199_Li/19908/li_attack_spell02b" refParamName="" useRefParam="false" />\r\n        <String name="resourceName2" value="prefab_skill_effects/hero_skill_effects/199_Li/19908/li_attack_spell02b_Water" refParamName="" useRefParam="false" />')
            with open(File_Check_Code, 'wb') as f:
                f.write(rpl)
        if IDCHECK == '19908' and 'S2B1.xml' in file:
            with open(File_Check_Code, 'rb') as f:
                rpl = f.read()
                rpl = rpl.replace(b'<String name="resourceName" value="prefab_skill_effects/hero_skill_effects/199_Li/19908/li_attack_spell02d" refParamName="" useRefParam="false" />',b'<String name="resourceName" value="prefab_skill_effects/hero_skill_effects/199_Li/19908/li_attack_spell02d" refParamName="" useRefParam="false" />\r\n        <String name="resourceName2" value="prefab_skill_effects/hero_skill_effects/199_Li/19908/li_attack_spell02d_Water" refParamName="" useRefParam="false" />')
            with open(File_Check_Code, 'wb') as f:
                f.write(rpl)
                
        if IDCHECK == '19908' and file in ["S2B1.xml", "U1B1.xml"]:
            with open(File_Check_Code, 'rb') as f:
                rpl = f.read()
            tracks = rpl.split(b"</Track>")
            modified_tracks = []
            for track in tracks:
                track = (track.replace(b'<String name="resourceName" value="prefab_skill_effects/hero_skill_effects/199_Li/19908/li_attack_buff05" refParamName="" useRefParam="false" />',b'<String name="resourceName" value="prefab_skill_effects/hero_skill_effects/199_Li/19908/li_attack_buff05" refParamName="" useRefParam="false" />\r\n        <String name="resourceName2" value="prefab_skill_effects/hero_skill_effects/199_Li/19908/li_attack_buff05_Water" refParamName="" useRefParam="false" />'))
                modified_tracks.append(track + b"</Track>")
            rpl = b"".join(modified_tracks)
            if rpl.endswith(b"</Track>"):
                rpl = rpl[:-8]
            with open(File_Check_Code, 'wb') as f:
                f.write(rpl)
        if IDCHECK == '19908' and 'S15.xml' in file:
            with open(File_Check_Code, 'rb') as f:
                rpl = f.read()
                rpl = rpl.replace(b'<String name="resourceName" value="prefab_skill_effects/hero_skill_effects/199_Li/19908/li_attack_buff06" refParamName="" useRefParam="false" />',b'<String name="resourceName" value="prefab_skill_effects/hero_skill_effects/199_Li/19908/li_attack_buff06" refParamName="" useRefParam="false" />\r\n        <String name="resourceName2" value="prefab_skill_effects/hero_skill_effects/199_Li/19908/li_attack_buff06_Water" refParamName="" useRefParam="false" />').replace(b'<String name="resourceName" value="prefab_skill_effects/hero_skill_effects/199_Li/19908/li_attack_spell01c" refParamName="" useRefParam="false" />',b'<String name="resourceName" value="prefab_skill_effects/hero_skill_effects/199_Li/19908/li_attack_spell01c" refParamName="" useRefParam="false" />\r\n        <String name="resourceName2" value="prefab_skill_effects/hero_skill_effects/199_Li/19908/li_attack_spell01c_Water" refParamName="" useRefParam="false" />')
            with open(File_Check_Code, 'wb') as f:
                f.write(rpl)
        if IDCHECK == '19908' and file in ["U1.xml", "U11.xml"]:
            with open(File_Check_Code, 'rb') as f:
                rpl = f.read()
            tracks = rpl.split(b"</Track>")
            modified_tracks = []
            for track in tracks:
                track = (track.replace(b'<String name="resourceName" value="prefab_skill_effects/hero_skill_effects/199_Li/19908/li_attack_spell03b" refParamName="" useRefParam="false" />',b'<String name="resourceName" value="prefab_skill_effects/hero_skill_effects/199_Li/19908/li_attack_spell03b" refParamName="" useRefParam="false" />\r\n        <String name="resourceName2" value="prefab_skill_effects/hero_skill_effects/199_Li/19908/li_attack_spell03b_Water" refParamName="" useRefParam="false" />').replace(b'<String name="resourceName" value="prefab_skill_effects/hero_skill_effects/199_Li/19908/li_attack_spell03_shifa" refParamName="" useRefParam="false" />',b'<String name="resourceName" value="prefab_skill_effects/hero_skill_effects/199_Li/19908/Li_attack_spell03_shifa" refParamName="" useRefParam="false" />\r\n        <String name="resourceName2" value="prefab_skill_effects/hero_skill_effects/199_Li/19908/Li_attack_spell03_shifa_Water" refParamName="" useRefParam="false" />'))
                modified_tracks.append(track + b"</Track>")
            rpl = b"".join(modified_tracks)
            if rpl.endswith(b"</Track>"):
                rpl = rpl[:-8]
            with open(File_Check_Code, 'wb') as f:
                f.write(rpl)
        if IDCHECK == '19908' and 'U1B1.xml' in file:
            with open(File_Check_Code, 'rb') as f:
                rpl = f.read()
                rpl = rpl.replace(b'<String name="resourceName" value="prefab_skill_effects/hero_skill_effects/199_Li/19908/li_attack_spell03_e" refParamName="" useRefParam="false" />',b'<String name="resourceName" value="prefab_skill_effects/hero_skill_effects/199_Li/19908/li_attack_spell03_e" refParamName="" useRefParam="false" />\r\n        <String name="resourceName2" value="prefab_skill_effects/hero_skill_effects/199_Li/19908/li_attack_spell03_e_water" refParamName="" useRefParam="false" />').replace(b'<String name="resourceName" value="prefab_skill_effects/hero_skill_effects/199_Li/19908/li_attack_spell03d" refParamName="" useRefParam="false" />',b'<String name="resourceName" value="prefab_skill_effects/hero_skill_effects/199_Li/19908/li_attack_spell03d" refParamName="" useRefParam="false" />\r\n        <String name="resourceName2" value="prefab_skill_effects/hero_skill_effects/199_Li/19908/li_attack_spell03d_water" refParamName="" useRefParam="false" />').replace(b'<String name="resourceName" value="prefab_skill_effects/hero_skill_effects/199_Li/19908/li_attack_spell03d_E" refParamName="" useRefParam="false" />',b'<String name="resourceName" value="prefab_skill_effects/hero_skill_effects/199_Li/19908/li_attack_spell03d_E" refParamName="" useRefParam="false" />\r\n        <String name="resourceName2" value="prefab_skill_effects/hero_skill_effects/199_Li/19908/li_attack_spell03d_E_water" refParamName="" useRefParam="false" />')
            with open(File_Check_Code, 'wb') as f:
                f.write(rpl)
    if (
        b"Skin_Icon_Skill" in dieukienmod
        or b"Skin_Icon_BackToTown" in dieukienmod
        or IDCHECK == "53702"
    ):
        IDNODMODCHECK = [
            '14111', '16707', '13011', '15015', '54307', '10620', '13210',
            '14104', '14107', '12106', '59901', '10915', '52414', '19610'
        ]
        DS_MOD_CHECK = []
    
        if IDCHECK not in IDNODMODCHECK:
            files_list = os.listdir(directory_path)
    
            for filename in files_list:
                if (
                    (filename in ['S1.xml', 'S1B1.xml', 'S1B2.xml'] and IDCHECK == "14111")
                    or (filename in ['S2.xml', 'S21.xml', 'S22.xml'] and IDCHECK == "13011")
                    or (filename not in ['13210_Back.xml', 'S2B2.xml', 't2p1.xml', 't2p2.xml'] and IDCHECK == "13210")
                    or (filename == 'P1E5.xml' and IDCHECK[:3] == '999')
                    or (filename != 'S1B1.xml' and IDCHECK == '13609')
                    or (filename != 'U1E1.xml' and IDCHECK == '10611')
                    or (filename == 'U1.xml' and IDCHECK == '10611')
                    or (filename == 'u1b1.xml' and IDCHECK == '59901')
                    or (filename == 'S2.xml' and IDCHECK == '15013')
                    or (filename == 'U1.xml' and IDCHECK == '15015')
                ):
                    continue
    
                file_path = os.path.join(directory_path, filename)
                with open(file_path, 'rb') as f:
                    All = f.read()
                Chat = All[:]
    
                if b'"Jg\x00' in All:
                    continue
    
                ListAll = All.split(b'\r\n')
                List_DOANAll = All.split(b'    <Track trackName="')
    
                SKM = b'<int name="skinId" value="99999" refParamName="" useRefParam="false" />'
                IDS = b'<int name="skinId" value="' + IDCHECK.encode() + b'" refParamName="" useRefParam="false" />'
                EQF = b'<bool name="bEqual" value="false" refParamName="" useRefParam="false" />'
                EQT = b'<bool name="bEqual" value="true" refParamName="" useRefParam="false" />'
                UNV = b'<bool name="useNegateValue" value="true" refParamName="" useRefParam="false" />'
                UNF = b'<bool name="useNegateValue" value="false" refParamName="" useRefParam="false" />'
                bol = b'<bool name="'
                check_vt = b'CheckSkinIdVirtualTick'
                check_sk = b'CheckSkinIdTick'
    
                CODE_CHECK = [x for x in List_DOANAll if IDS.lower() in x.lower()]
                if len(CODE_CHECK) != 0:
                    for text in CODE_CHECK:
                        # CheckSkinIdTick
                        if check_sk.lower() in text.lower():
                            if bol not in text:
                                text1 = text.replace(IDS, IDS + b'\n'+b'        '+EQF).replace(IDS, b'\n'+b'        '+SKM)
                                All = All.replace(text, text1)
                                continue
                            if EQF not in text and EQT in text:
                                text1 = text.replace(EQT, b'\n'+b'        '+EQF).replace(IDS, b'\n'+b'        '+SKM)
                                All = All.replace(text, text1)
                                continue
                            if EQF in text:
                                text1 = text.replace(EQF, b'').replace(IDS, b'\n'+b'        '+SKM)
                                All = All.replace(text, text1)
                                continue
                            if EQF not in text:
                                text1 = text.replace(IDS, IDS + b'\n'+b'        '+EQF).replace(IDS, b'\n'+b'        '+SKM)
                                All = All.replace(text, text1)
                                continue
    
                        # CheckSkinIdVirtualTick
                        if check_vt.lower() in text.lower():
                            if UNV in text:
                                text1 = text.replace(UNV, b'').replace(IDS, b'\n'+b'        '+SKM)
                                All = All.replace(text, text1)
                                continue
                            if UNF in text:
                                text1 = text.replace(UNF, b'\n'+b'        '+UNV).replace(IDS, b'\n'+b'        '+SKM)
                                All = All.replace(text, text1)
                                continue
                            if UNV not in text:
                                text1 = text.replace(IDS, IDS + b'\n'+b'        '+UNV).replace(IDS, b'\n'+b'        '+SKM)
                                All = All.replace(text, text1)
                                continue
    
                with open(file_path, 'wb') as f:
                    f.write(All)
    
                with open(file_path, 'rb') as file:
                    xml_bytes1 = file.read()
                if filename not in DS_MOD_CHECK and Chat != xml_bytes1:
                    DS_MOD_CHECK.append(filename)
    
            print("\n  ┌" + "\033[1;31m─────────────── CHECK_SKIN ────────────────" + Style.RESET_ALL + "┐\n")
            if not DS_MOD_CHECK:
                print("                [ ĐÉO CÓ MOD CHECK ]                ")
            else:
                for TEN_FILES_MOD_CHECK in DS_MOD_CHECK:
                    total_width = 48
                    spaces = total_width - len(TEN_FILES_MOD_CHECK) - 6
                    spaces_before = math.floor(spaces / 2)
                    spaces_after = math.ceil(spaces / 2)
                    print(' ' * spaces_before + '[ ' + TEN_FILES_MOD_CHECK + ' ]' + ' ' * spaces_after)
            print("\n  └" + "\033[1;31m───────────────────────────────────────────" + Style.RESET_ALL + "┘\n")

#-----------------------------------------------
    if IDCHECK == '15009':
        for file in ["BlueBuff.xml", "RedBuff_Slow.xml"]:
            duongdan = f"{FolderMod}/Resources/{Ver}/Ages/Prefab_Characters/Prefab_Hero/mod1/PassiveResource/{file}"
            giai(duongdan)
            with open(duongdan, 'rb') as f:
                content = f.read().replace(
                    b"CheckSkinIdVirtualTick", b"CheckHeroIdTick"
                    ).replace(
                    b'"skinId" value="15009"', b'"heroId" value="150"'
                    )
            with open(duongdan, 'wb') as f:
                f.write(content)
    if IDCHECK == '15013':
        Youtuber_Name = f'{FolderMod}/Resources/{Ver}/Ages/Prefab_Characters/Prefab_Hero/mod1/PassiveResource/BlueBuff_CD.xml'
        giai(Youtuber_Name)
        with open(Youtuber_Name, 'rb') as f:
            noidung = f.read()
        noidung = noidung.replace(b"CheckSkinIdTick", b"CheckHeroIdTick")\
                         .replace(b'"skinId" value="15013"', b'"heroId" value="150"')\
                         .replace(b'prefab_skill_effects/hero_skill_effects/15013/', 
                                  b'prefab_skill_effects/hero_skill_effects/150_hanxin/15013/')
        with open(Youtuber_Name, 'wb') as f:
            f.write(noidung)
    try:
        with open(f'Resources/{Ver}/assetbundle/resourceverificationinfosetall.assetbundle','rb') as f:
            strin=f.read()
    except:
        strin = b'An Cap Bu Buoi Tao'
    strin = b'An Cap Bu Buoi Tao'
    os.makedirs(f'{FolderMod}/Resources/{Ver}/assetbundle',exist_ok=True)
    i=0
    with open(f'{FolderMod}/Resources/{Ver}/assetbundle/resourceverificationinfosetall.assetbundle','wb') as f:f.write(strin)
#-----------------------------------------------
    fixlag1 = '1'
    if fixlag1 == '1':
        path = Files_Directory_Path + f'{NAME_HERO}' + '/skill/'
        Function_Track_Guid_AddGetHoliday(path)
        move_skin_action_back(Files_Directory_Path)
        ID_SKIN = IDCHECK
        if ID_SKIN not in ["53702"]:
            HDSkill(ID_SKIN, path)
        PathBorn = os.path.join(f"{FolderMod}/Resources/{Ver}/Ages/Prefab_Characters/Prefab_Hero/mod1/commonresource/", "Born.xml")
        giai(PathBorn)
        path1 = [file for file in os.listdir(path) if file.endswith(("A1E1.xml", "A1E0.xml")) and os.path.isfile(os.path.join(path, file))]
        Code = []
        for file in path1:
            try:
                with open(os.path.join(path, file), encoding='utf-8') as F:
                    R = F.read()
                if "resourceName" in R:
                    for i in R.splitlines():
                        if "resourceName" in i:
                            i = i.replace("resourceName2", "resourceName")
                            i = i.replace("resourceName3", "resourceName")
                            if ID in i and i not in Code:
                                Code.append(i)
            except:
                pass
        
        CheckHero = f'  <Track trackName="None" eventType="CheckHeroIdTick" guid="{str(uuid.uuid4())}" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\n      <Event eventName="CheckHeroIdTick" time="0.000" isDuration="false" guid="{str(uuid.uuid4())}">\n        <TemplateObject name="targetId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\n        <int name="heroId" value="IDSKIN" refParamName="" useRefParam="false" />\n      </Event>\n    </Track>\n'
        
        TG = f'    <Track trackName="None" eventType="TriggerParticleTick" guid="{str(uuid.uuid4())}" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\n      <Condition id="NUM" guid="{str(uuid.uuid4())}" status="true" />\n      <Event eventName="TriggerParticleTick" time="0.000" isDuration="false" guid="{str(uuid.uuid4())}">\n        <TemplateObject name="targetId" id="1" objectName="target" isTemp="false" refParamName="" useRefParam="false" />\n\n      </Event>\n    </Track>\n'
        
        with open(PathBorn, encoding='utf-8') as F:
        	Read = F.read()
        
        kh = "</Action>"
        if kh in Read:
        	Read = Read.replace(kh, CheckHero + kh, 1)
        	Read = Read.replace(kh, '  ' + kh, 1)
        	NUM = Read.count('<Track trackName=')-1
        	Read = Read.replace("IDSKIN", ID[:3])
        for code in Code:
            New = TG.replace("\n\n", "\n" + code + "\n")
            print(repr(New.encode()))
            Read = Read.replace("  </Action>", New + "  </Action>")
        Read = Read.replace("NUM", str(NUM))

        with open(PathBorn, "w", encoding='utf-8') as F: F.write(Read)
#-----------------------------------------------
        if IDCHECK in ("50108","14111","11107","15009","13015","13314"):
            organSkin = f"Resources/{Ver}/Databin/Client/Actor/organSkin.bytes"
            organSkin_mod = f"{FolderMod}/Resources/{Ver}/Databin/Client/Actor/organSkin.bytes"
            shutil.copy(organSkin, organSkin_mod)
            giai(organSkin_mod)
        if IDCHECK in ("50108","14111","11107","15009","13015","13314"):
            ID = IDCHECK
            file = open(organSkin_mod, "rb")
            IDN = str(hex(int(ID)))
            IDN = IDN[4:6] + IDN[2:4]
            IDN = bytes.fromhex(IDN)
            ALL_ID = []
            MD = int(ID[0:3] + "00")
            for IDNew in range(21):
                ALL_ID.append(str(MD))
                MD += 1
            ALL_ID.remove(ID)
            for x in range(20):
                IDK = str(hex(int(ALL_ID[x])))
                IDK = IDK[4:6] + IDK[2:4]
                IDK = bytes.fromhex(IDK)
                ALL_ID[x] = IDK
            Begin = file.read(140)
            Read = b"\x00"
            All = []
            while Read != b"":
                Read = file.read(36)
                if Read.find(IDN) != -1:
                    All.append(Read)
                try:
                    Max = Read[4] + (Read[5]*256)
                    Max0 = str(hex(Max))
                    if len(Max0) == 4:
                        Max0 = Max0[2:4] + "00"
                    if len(Max0) == 5:
                        Max0 = Max0[3:5] + "0" + Max0[2]
                    if len(Max0) == 6:
                        Max0 = Max0[4:6] + Max0[2:4]
                    Max0 = bytes.fromhex(Max0)
                except:
                    None
            file.close()
            file = open(organSkin_mod, "ab+")
            Read0 = file.read()
            for i in range(len(ALL_ID)):
                for j in range(len(All)):
                    CT = All[j]
                    if CT.find(IDN) != -1:
                        CT = CT.replace(IDN,ALL_ID[i])
                    else:
                        CT = CT.replace(ALL_ID[i-1],ALL_ID[i])
                    CTN = str(hex(Max0[0]+(Max0[1]*256)+1))
                    if len(CTN) == 4:
                        CTN = CTN[2:4]
                    if len(CTN) == 5:
                        CTN = CTN[3:5] + "0" + CTN[2]
                    if len(CTN) == 6:
                        CTN = CTN[4:6] + CTN[2:4]
                    CTN = bytes.fromhex(CTN)
                    OZ = b" \x00\x00\x00"
                    if len(CTN) == 1:
                        CT = CT.replace(OZ+CT[4:6],OZ+CTN+b"\x00",1)
                    if len(CTN) == 2:
                        CT = CT.replace(OZ+CT[4:6],OZ+CTN,1)
                    All[j] = CT
                    XXX = file.write(CT)
                    Max0 = CT[4:6]
            file.close()
            file = open(organSkin_mod, "rb")
            Read = file.read()
            Read = Read.replace(Begin[12:14],Max0,1)
            file.close()
            file = open(organSkin_mod, "wb")
            Z = file.write(Read)
            file.close()
#-----------------------------------------------
    if IDCHECK in ['13706', '13705'] or b"Skin_Icon_BackToTown" in dieukienmod or b"Skin_Icon_Animation" in dieukienmod:
        import uuid, os, re
        back_path = f'{FolderMod}/Resources/{Ver}/Ages/Prefab_Characters/Prefab_Hero/mod1/commonresource/Back.xml'
        giai(back_path)
        with open(back_path, 'rb') as f:
            data = f.read()
        
        tracks = re.findall(rb'    <Track trackName=.*?</Track>', data, re.DOTALL)
        found_blocks = {}
        for b in tracks:
            if b'<int name="skinId" value="' in b and 'skin' not in found_blocks:
                found_blocks['skin'] = b
            elif b'value="born_back_reborn/huijidi_01"' in b and 'p1' not in found_blocks:
                found_blocks['p1'] = b
            elif b'value="prefab_skill_effects/tongyong_effects/tongyong_hurt/born_back_reborn/huicheng_tongyong_01"' in b and 'p2' not in found_blocks:
                found_blocks['p2'] = b
            elif b'value="Gohome"' in b and 'clip1' not in found_blocks:
                found_blocks['clip1'] = b
            elif b'value="Home"' in b and b'value="Gohome"' not in b and 'clip2' not in found_blocks:
                found_blocks['clip2'] = b
            if len(found_blocks) == 5:
                break
        
            external_file = None
            
            for sf in ['_Back.xml', '_back.xml']:
                path = os.path.join(Files_Directory_Path, NAME_HERO, 'skill', IDMODSKIN + sf)
                if os.path.isfile(path):
                    external_file = path
                    break
            
            if not external_file:
                pass
        def remove_conditions(block: bytes) -> bytes:
            lines = block.splitlines()
            lines = [line for line in lines if b'<Condition ' not in line]
            return b'\n'.join(lines)

        def insert_condition(block: bytes, condition_id: int) -> bytes:
            guid_match = re.search(rb'guid="([^"]+)"', block)
            guid = guid_match.group(1) if guid_match else b'unknown-guid'
            condition = f'      <Condition id="{condition_id}" guid="{str(uuid.uuid4())}" status="true" />'.encode()
            lines = block.splitlines()
            for j, line in enumerate(lines):
                if b'<Track trackName=' in line:
                    lines.insert(j + 1, condition)
                    break
            return b'\n'.join(lines)
        
        def clean_block(block: bytes) -> bytes:
            block = re.sub(rb'\s+SkinAvatarFilterType="[^"]+"', b'', block)
            block = re.sub(
                b'<int name="skinId" value="[^"]*" refParamName="" useRefParam="false" />',
                b'<int name="skinId" value="' + IDMODSKIN[:3].encode() + b'00' + b'" refParamName="" useRefParam="false" />',
                block
            )
            if IDMODSKIN in ['16707', '13311']:
                block = block.replace(
                    b'<String name="resourceName" value="" refParamName="strReturnCityFall" useRefParam="true" />',
                    b'<String name="resourceName" value="prefab_skill_effects/component_effects/' + IDMODSKIN.encode() + b'/' + IDMODSKIN.encode() +
                    b'_5/huijidi_01" refParamName="" useRefParam="false" />'
                ).replace(
                    b'<String name="resourceName" value="" refParamName="strReturnCityEffectPath" useRefParam="true" />',
                    b'<String name="resourceName" value="prefab_skill_effects/component_effects/' + IDMODSKIN.encode() + b'/' + IDMODSKIN.encode() +
                    b'_5/huicheng_tongyong_01" refParamName="" useRefParam="false" />'
                ).replace(
                    b'value="Gohome"',
                    b'value="' + IDMODSKIN.encode() + b'/Awaken/GoHome"'
                ).replace(
                    b'value="Home"',
                    b'value="' + IDMODSKIN.encode() + b'/Awaken/Home"'
                )
            if IDMODSKIN in ['11620']:
                block = block.replace(
                    b'<String name="resourceName" value="" refParamName="strReturnCityFall" useRefParam="true" />',
                    b'<String name="resourceName" value="prefab_skill_effects/component_effects/' + IDMODSKIN.encode() + b'/' + IDMODSKIN.encode() +
                    b'_5_3/huijidi_01" refParamName="" useRefParam="false" />'
                ).replace(
                    b'<String name="resourceName" value="" refParamName="strReturnCityEffectPath" useRefParam="true" />',
                    b'<String name="resourceName" value="prefab_skill_effects/component_effects/' + IDMODSKIN.encode() + b'/' + IDMODSKIN.encode() +
                    b'_5_3/huicheng_tongyong_01" refParamName="" useRefParam="false" />'
                ).replace(
                    b'value="Gohome"',
                    b'value="' + IDMODSKIN.encode() + b'/Awaken/Gohome"'
                ).replace(
                    b'value="Home"',
                    b'value="' + IDMODSKIN.encode() + b'/Awaken/Home"'
                )
            block = block.replace(
                b'<String name="parentResourceName" value="born_back_reborn/huijidi_01" refParamName="" useRefParam="false" />', b''
            ).replace(
                b'<String name="parentResourceName" value="prefab_skill_effects/tongyong_effects/tongyong_hurt/born_back_reborn/huicheng_tongyong_01" refParamName="" useRefParam="false" />', b''
            ).replace(
                b'<String name="resourceName" value="" refParamName="strReturnCityFall" useRefParam="true" />',
                b'<String name="resourceName" value="Prefab_Skill_Effects/Hero_Skill_Effects/NAME_HERO/IDMODSKIN/huijidi_01.prefab" refParamName="" useRefParam="true"/>'
            ).replace(
                b'<String name="resourceName" value="" refParamName="strReturnCityEffectPath" useRefParam="true" />',
                b'<String name="resourceName" value="Prefab_Skill_Effects/Hero_Skill_Effects/NAME_HERO/IDMODSKIN/huicheng_tongyong_01.prefab" refParamName="" useRefParam="true"/>'
            ).replace(
                b'<String name="resourceName" value="prefab_skill_effects/tongyong_effects/tongyong_hurt/born_back_reborn/huicheng_tongyong_01" refParamName="" useRefParam="false" />',
                b'<String name="resourceName" value="Prefab_Skill_Effects/Hero_Skill_Effects/NAME_HERO/IDMODSKIN/huicheng_tongyong_01.prefab" refParamName="" useRefParam="true"/>'
            ).replace(
                b'NAME_HERO', NAME_HERO.encode()
            ).replace(
                b'IDMODSKIN', IDMODSKIN.encode()
            )
        
            # Trường hợp đặc biệt cho component_effects
            # Xoá dòng SkinOrAvatarList
            lines = block.splitlines()
            lines = [line for line in lines if b'<SkinOrAvatarList' not in line]
            cleaned = []
            skip = False
            for i, line in enumerate(lines):
                if b'<Vector3i name="scalingInt"' in line:
                    cleaned.append(line)
                    skip = True
                    continue
                if skip:
                    if b'</Event>' in line or b'</Track>' in line:
                        cleaned.append(line)
                        skip = False
                    continue
                cleaned.append(line)
        
            return b'\n'.join(cleaned)

        
        CODE_BV_HERO = []
        next_condition_id = data.count(b'<Track trackName=') 
        
        block_skin = clean_block(found_blocks['skin'])
        CODE_BV_HERO.append(block_skin)

        if external_file:
            with open(external_file, 'rb') as ef:
                external_data = ef.read()
            raw_blocks = re.findall(rb'    <Track trackName=.*?</Track>', external_data, re.DOTALL)
            for block in raw_blocks:
                block = insert_condition(block, next_condition_id)
                next_condition_id += 0
                CODE_BV_HERO.append(block)
        for k in ['p1', 'p2', 'clip1', 'clip2']:
            blk = clean_block(found_blocks[k])
            blk = remove_conditions(blk)
            blk = insert_condition(blk, next_condition_id)
            next_condition_id += 0
            CODE_BV_HERO.append(blk)
        if IDMODSKIN == '16307':
            ryoma = b'    <Track trackName="PlayAnimationTick0" eventType="PlayAnimationTick" guid="6c6f287e-412d-4011-a513-b2727f068c3a" enabled="true" refParamName="" useRefParam="false" r="0.083" g="1.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\n      <Event eventName="PlayAnimationTick" time="0.000" isDuration="false">\n        <TemplateObject name="targetId" objectName="self" id="0" isTemp="false" refParamName="" useRefParam="false"/>\n        <String name="clipName" value="Dance04_T2" refParamName="" useRefParam="false"/>\n        <float name="crossFadeTime" value="0.150" refParamName="" useRefParam="false"/>\n        <float name="playSpeed" value="1.000" refParamName="" useRefParam="false"/>\n        <int name="layer" value="3" refParamName="" useRefParam="false"/>\n        <int name="subLayer" value="0" refParamName="" useRefParam="false"/>\n        <bool name="loop" value="false" refParamName="" useRefParam="false"/>\n        <bool name="applyActionSpeed" value="false" refParamName="" useRefParam="false"/>\n        <bool name="alwaysAnimate" value="false" refParamName="" useRefParam="false"/>\n        <bool name="bNoTimeScale" value="false" refParamName="" useRefParam="false"/>\n        <bool name="bCanNotBeCulled" value="false" refParamName="" useRefParam="false"/>\n      </Event>\r\n    </Track>'
            ryoma = insert_condition(ryoma, next_condition_id)
            next_condition_id += 0
            CODE_BV_HERO.append(ryoma)
        if IDMODSKIN == '11620':
            V11620=b'    <Track trackName="PlayAnimDuration0" eventType="PlayAnimDuration" guid="b370cde0-135a-4674-9c66-ff9dd825b5e5" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false">\n      <Event eventName="PlayAnimDuration" time="9.000" length="1.000" isDuration="true">\n        <TemplateObject name="targetId" objectName="self" id="0" isTemp="false" refParamName="" useRefParam="false" />\n        <String name="clipName" value="11620/Awaken/Dance16_Sprint" refParamName="" useRefParam="false" />\n        <int name="layer" value="5" refParamName="" useRefParam="false" />\n        <bool name="alwaysAnimate" value="true" refParamName="" useRefParam="false" />\n      </Event>\n    </Track>\n    <Track trackName="PlayAnimDuration0" eventType="PlayAnimDuration" guid="b370cde0-135a-4674-9c66-ff9dd825b5e5" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false">\n      <Event eventName="PlayAnimDuration" time="9.000" length="1.000" isDuration="true">\n        <TemplateObject name="targetId" objectName="self" id="0" isTemp="false" refParamName="" useRefParam="false" />\n        <String name="clipName" value="11620/Awaken/Dance16_Sprint_Idle" refParamName="" useRefParam="false" />\n        <int name="layer" value="5" refParamName="" useRefParam="false" />\n        <bool name="alwaysAnimate" value="true" refParamName="" useRefParam="false" />\n      </Event>\n    </Track>\n    <Track trackName="PlayAnimDuration0" eventType="PlayAnimDuration" guid="b370cde0-135a-4674-9c66-ff9dd825b5e5" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false">\n      <Event eventName="PlayAnimDuration" time="9.000" length="1.000" isDuration="true">\n        <TemplateObject name="targetId" objectName="self" id="0" isTemp="false" refParamName="" useRefParam="false" />\n        <String name="clipName" value="11620/Awaken/Dance16_Sprint_end" refParamName="" useRefParam="false" />\n        <int name="layer" value="5" refParamName="" useRefParam="false" />\n        <bool name="alwaysAnimate" value="true" refParamName="" useRefParam="false" />\n      </Event>\n    </Track>\n'
            V11620 = insert_condition(V11620, next_condition_id)
            next_condition_id += 0
            CODE_BV_HERO.append(V11620)
        injected = b'\n' + b'\n'.join(CODE_BV_HERO) + b'\n'
        if b'</Action>' in data:
            result = data.replace(b'</Action>', injected + b'  </Action>').replace(b'<SkinOrAvatarList id="' + IDMODSKIN.encode() + b'" />',b'<SkinOrAvatarList id="' + IDMODSKIN[:3].encode() + b'00" />')
        else:
            pass
        with open(back_path, 'wb') as f:
            f.write(result)
        print("    Back.xml hoàn tất")
#-----------------------------------------------
    GiaTocEdit = 2
    for haste_file in ['HasteE1.xml', 'HasteE1_leave.xml']:
        duonggia = f'{FolderMod}/Resources/{Ver}/Ages/Prefab_Characters/Prefab_Hero/mod1/commonresource/{haste_file}'
        giai(duonggia)
        ID_SKIN_GT = int(IDCHECK)
        ID_SKIN_GT = b'\x00\x00' + ID_SKIN_GT.to_bytes(2, 'little')
        with open(Huanhua, 'rb') as f:
            ab = f.read()
        
        pos = ab.find(ID_SKIN_GT)
        if pos != -1:
            vt_bytes = ab[pos - 2:pos]
            vtr = int.from_bytes(vt_bytes, byteorder='little')
            vt1 = ab[pos - 2 : pos - 2 + vtr]
            DKMODGT = vt1.lower()
        
            if b'sprint' in DKMODGT or b'jiasu' in DKMODGT or IDMODSKIN == '15015':
                try:
                    with open(duonggia, 'r', encoding='utf-8') as f:
                        text = f.read()
                except Exception as e:
                    continue

                if IDMODSKIN == '11620':
                
                    tracks = re.findall(r'<Track[\s\S]*?</Track>', text)
                    block_ghep = ''
                
                    for block in tracks:
                        if ('value="Sprint_idle"' in block or 'value="Sprint"' in block) and 'SkinOrAvatarList' not in block:
                
                            block_new = block.replace(
                                'value="Sprint"',
                                'value="11620/Awaken/Dance16_Sprint"'
                            ).replace(
                                'value="Sprint_idle"',
                                'value="11620/Awaken/Dance16_Sprint_Idle"'
                            )
                            block_new = re.sub(r'\s*<Condition[^>]*/>\s*', '', block_new)
                
                            lines = block_new.splitlines()
                
                            # thêm SkinAvatarFilterType
                            for i, line in enumerate(lines):
                                if line.strip().startswith('<Track ') and 'SkinAvatarFilterType=' not in line:
                                    lines[i] = line.rstrip('>') + ' SkinAvatarFilterType="9">'
                                    break
                
                            # thêm SkinOrAvatarList
                            for i, line in enumerate(lines):
                                if line.strip().startswith('</Track>'):
                                    lines.insert(i, '      <SkinOrAvatarList id="11600" />')
                                    break
                
                            block_final = '\n'.join(lines).strip()
                            block_ghep += '  ' + block_final + '\n'
                
                    pos = text.find('</Action>')
                    if pos != -1 and block_ghep:
                        text = text[:pos] + block_ghep +'  '+ text[pos:]
                
                    with open(duonggia, 'w', encoding='utf-8') as f:
                        f.write(text)
                
                    continue
                
                tracks = re.findall(r'<Track[\s\S]*?</Track>', text)
                block_skinid = None
                block_effect = None
        
                for block in tracks:
                    if block_skinid is None and re.search(r'name=["\']skinId["\']', block):
                        block_skinid = block
                    elif block_effect is None and 'jiasu_tongyong_01' in block:
                        block_effect = block
                    if block_skinid and block_effect:
                        break
        
                if not block_skinid or not block_effect:
                    exit()
                def remove_lines_after_bUseTargetSkinEffect(block: str) -> str:
                    lines = block.splitlines()
                    new_lines = []
                    skip = False
                    for line in lines:
                        if skip:
                            if line.strip().startswith('</Event>'):
                                new_lines.append(line)
                                skip = False
                            continue
                        new_lines.append(line)
                        if '<bool name="bUseTargetSkinEffect"' in line:
                            skip = True
                    return '\n'.join(new_lines)
                def code(data: str) -> str:
                    return data.replace(f'<SkinOrAvatarList id="{IDCHECK}" />', f'<SkinOrAvatarList id="237{IDCHECK[-2:]}" />')
                text = code(text)
                # Sửa block skinId
                block_skinid = re.sub(
                    r'<int name="skinId" value="\d+" refParamName="" useRefParam="false" ?/>',
                    f'<int name="skinId" value="{IDMODSKIN[:3]}00" refParamName="" useRefParam="false" />',
                    block_skinid
                )
                
                # Sửa block effect
                block_effect = re.sub(r'^\s*<Condition[^>]*?\/>\s*?', '', block_effect, flags=re.MULTILINE)
                block_effect = block_effect.replace('common_effects', f'hero_skill_effects/{NAME_HERO}/{IDMODSKIN}')
        
                if IDMODSKIN == '13314':
                    block_effect = block_effect.replace('<Vector3 name="bindPosOffset" x="0.000" y="0.700" z="-0.600" refParamName="" useRefParam="false" />', '<Vector3 name="bindPosOffset" x="0.000" y="0.000" z="0.000" refParamName="" useRefParam="false" />')
                if IDMODSKIN == '13314':
                    block_effect = block_effect.replace('jiasu_tongyong_01', 'EF_13314_DiRenJie_sprint_loop')
                elif IDMODSKIN == '11607':
                    block_effect = block_effect.replace('jiasu_tongyong_01', 'jingke_sprint_01')
                elif IDMODSKIN == '15009':
                    block_effect = block_effect.replace('jiasu_tongyong_01', 'T2_Spint').replace('<Vector3 name="bindPosOffset" x="0.000" y="0.700" z="-0.600" refParamName="" useRefParam="false" />', '<Vector3 name="bindPosOffset" x="0.000" y="0.000" z="0.000" refParamName="" useRefParam="false" />')
                    
                elif IDMODSKIN == '19908':
                    block_effect = block_effect.replace('jiasu_tongyong_01','EF_19908_Li_sprint_loop')
                elif IDMODSKIN == '15015':
                    block_effect = block_effect.replace('jiasu_tongyong_01', '15015_HanXin_sprint_01')
                elif IDCHECK == "52011":
                    block_effect = block_effect.replace("jiasu_tongyong_01","52011/520_Veres_long_sprint_loop")
                elif IDMODSKIN == '52414':
                    block_effect = block_effect.replace('jiasu_tongyong_01', '52414_Capheny_sprint_loop')
                elif IDMODSKIN == '15217':
                    block_effect = block_effect.replace('jiasu_tongyong_01', 'EF_wangzhaojun_15218_sprint_loop_sun')
                elif IDMODSKIN == '53806':
                    block_effect = block_effect.replace('jiasu_tongyong_01', 'Iggy_sprint_HD').replace('<Vector3 name="bindPosOffset" x="0.000" y="0.700" z="-0.600" refParamName="" useRefParam="false" />', '<Vector3 name="bindPosOffset" x="0.000" y="0.000" z="0.000" refParamName="" useRefParam="false" />')
                elif IDMODSKIN == '54307':
                    block_effect = block_effect.replace('jiasu_tongyong_01', 'yao_sprint')
                elif IDMODSKIN == '13613':
                    block_effect = block_effect.replace('jiasu_tongyong_01', '13613_WuZeTian_sprint')
                elif IDMODSKIN == '16307':
                    block_effect = block_effect.replace('jiasu_tongyong_01', 'JuYouJing_jiasu_01')
                elif IDMODSKIN == '13118':
                    block_effect = block_effect.replace('jiasu_tongyong_01', '13118_Libai_sprint_01_loop')
                elif IDMODSKIN == '13210':
                    if haste_file == 'HasteE1.xml':
                        block_effect = block_effect.replace('jiasu_tongyong_01', 'MaKeBoLuo_Buff_Start')
                    else:
                        block_effect = block_effect.replace('jiasu_tongyong_01', 'MaKeBoLuo_Buff_Start')
                elif IDMODSKIN == '14111':
                    block_effect = block_effect.replace('jiaSu_tongyong_01', '14111_luoer_Sprint').replace(
                        '        <Vector3 name="bindPosOffset" x="0.000" y="0.700" z="-0.600" refParamName="" useRefParam="false" />', '        <Vector3 name="bindPosOffset" x="0.000" y="0.000" z="0.000" refParamName="" useRefParam="false" />')
                block_effect = remove_lines_after_bUseTargetSkinEffect(block_effect)
    
                # Tính số track
                def count_tracks_above_action_name(filepath, action_name):
                    with open(filepath, 'r', encoding='utf-8') as file:
                        lines = file.readlines()
                    count = 0
                    for line in lines:
                        if action_name in line:
                            break
                        if 'trackName' in line:
                            count += 1
                    return count
        
                track_count = count_tracks_above_action_name(duonggia, '</Project>')
                effect_lines = block_effect.splitlines()
                
                if GiaTocEdit == 1:
                    # Dùng CheckSkinIdTick → chèn Condition
                    insert_line = f'      <Condition id="{track_count}" guid="{str(uuid.uuid4())}" status="true" />'
                    if len(effect_lines) >= 2:
                        effect_lines.insert(2, insert_line)
                else:
                    # Dùng SkinOrAvatarList → thêm SkinAvatarFilterType="9" và <SkinOrAvatarList>
                    for i, line in enumerate(effect_lines):
                        if line.strip().startswith('<Track ') and 'SkinAvatarFilterType=' not in line:
                            effect_lines[i] = line.rstrip('>') + ' SkinAvatarFilterType="9">'
                            break
                    for i, line in enumerate(effect_lines):
                        if line.strip().startswith('</Event>'):
                            effect_lines.insert(i + 1, f'      <SkinOrAvatarList id="{IDMODSKIN[:3]}00" />')
                            break
                
                block_effect_final = '\n'.join(effect_lines).strip()
                block_skinid_final = block_skinid.strip() if GiaTocEdit == 1 else ''
                block_ghep = ''
                
                if block_skinid_final:
                    block_ghep += f'  {block_skinid_final}\n'
                block_ghep += f'  {block_effect_final}\n'
                if IDMODSKIN == '16707' and haste_file == 'HasteE1.xml':
                    with open(duonggia, 'r', encoding='utf-8') as f: 
                        rpl=f.read()
                        rpl = rpl.replace('JiaSu_tongyong_01','Wukong_Sprint_Idle')
                if IDMODSKIN == '13118' and haste_file == 'HasteE1.xml':
                    with open(duonggia, 'r', encoding='utf-8') as f: 
                        rpl=f.read()
                        rpl = rpl.replace('<SkinOrAvatarList id="13118" />','')
                if IDMODSKIN == '13118' and haste_file == 'HasteE1_leave.xml':
                    with open(duonggia, 'r', encoding='utf-8') as f: 
                        rpl=f.read()
                        rpl = rpl.replace('<SkinOrAvatarList id="13118" />','')
                if IDMODSKIN == '16707' and haste_file == 'HasteE1_leave.xml':
                    with open(duonggia, 'r', encoding='utf-8') as f: 
                        rpl=f.read()
                        rpl = rpl.replace('JiaSu_tongyong_01','Wukong_Sprint')
                if IDMODSKIN == '13210' and haste_file == 'HasteE1.xml':
                    with open(duonggia, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                    track_count = 0
                    for line in lines:
                        if '</Project>' in line:
                            break
                        if 'trackName' in line:
                            track_count += 1
                    block_ghep += f'    <Track trackName="TriggerParticle0" eventType="TriggerParticle" guid="{str(uuid.uuid4())}" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true" SkinAvatarFilterType="9">\n      <Condition id="{track_count}" guid="{str(uuid.uuid4())}" status="true"/>\n      <Event eventName="TriggerParticle" time="0.000" length="4.000" isDuration="true" guid="{str(uuid.uuid4())}">\n        <TemplateObject name="targetId" id="1" objectName="target" isTemp="false" refParamName="" useRefParam="false"/>\n        <TemplateObject name="objectSpaceId" id="1" objectName="target" isTemp="false" refParamName="" useRefParam="false"/>\n        <String name="resourceName" value="Prefab_Skill_Effects/Hero_Skill_Effects/132_MaKeBoLuo/13210/MaKeBoLuo_Buff_End" refParamName="" useRefParam="false"/>\n        <Vector3 name="bindPosOffset" x="0.000" y="0.000" z="0.000" refParamName="" useRefParam="false"/>\n        <Vector3i name="scalingInt" x="10000" y="10000" z="10000" refParamName="" useRefParam="false"/>\n        <bool name="bUseTargetSkinEffect" value="true" refParamName="" useRefParam="false"/>\n      </Event>\n      <SkinOrAvatarList id="13200" />\n    </Track>\n'
                pos = text.find('</Action>')
                if pos == -1:
                    pass
                    
                text_moi = text[:pos] + block_ghep +'  '+ text[pos:]
                with open(duonggia, 'w', encoding='utf-8') as f:
                    f.write(text_moi)
                    
                print(f"    [+] {os.path.basename(duonggia)} : Done")
#-----------------------------------------------
    def zip_folder(folder_path, output_path):
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_STORED) as zipf:
            for root, _, files in os.walk(folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, start=folder_path)
                    zipf.write(file_path, arcname)
    if IDCHECK == "54402":
        giapcuongnoyan = '3'#input("\033[1;97m[\033[1;92m?\033[1;97m] SPECIAL: 54402 - MOD EFX GIÁP CUỒNG NỘ YAN Y/n \n[\033[1;92m•\033[1;97m] INPUT: ")
        if giapcuongnoyan.lower() == 'y':	
            with zipfile.ZipFile(f'Resources/{Ver}/Ages/Prefab_Gear.pkg.bytes') as f:
                f.extractall(f'{FolderMod}/Resources/{Ver}/Ages/mod2/')
                file_path=f'{FolderMod}/Resources/{Ver}/Ages/mod2/Prefab_Gear/Defense/1338E1.xml'
                giai(file_path)
                with open (file_path, 'rb') as f:
                    noidung = f.read()
                    noidung = noidung.replace(b"</Action>", b"""  <Track trackName="Nhung" eventType="CheckHeroIdTick" guid="NhungAOV-54402" enabled="true" refParamName="" useRefParam="false" r="0.667" g="1.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Event eventName="CheckHeroIdTick" time="0.000" isDuration="false">\r\n        <TemplateObject name="targetId" objectName="target" id="1" isTemp="false" refParamName="" useRefParam="false"/>\r\n        <int name="heroId" value="544" refParamName="" useRefParam="false"/>\r\n      </Event>\r\n    </Track>\r\n    <Track trackName="TriggerParticle0" eventType="TriggerParticle" guid="Nhung_AOV" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true" lod="0">\r\n      <Condition id="0" guid="NhungAOV-54402" status="true" />\r\n      <Event eventName="TriggerParticle" time="0.000" length="2.000" isDuration="true" guid="Nhung_AOV">\r\n        <TemplateObject name="targetId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <TemplateObject name="objectSpaceId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <String name="resourceName" value="prefab_skill_effects/hero_skill_effects/544_Painter/54402/jiasu_tongyong_01" refParamName="" useRefParam="false" />\r\n        <Vector3 name="bindPosOffset" x="0.000" y="0.700" z="-0.600" refParamName="" useRefParam="false" />\r\n        <Vector3i name="scalingInt" x="10000" y="10000" z="10000" refParamName="" useRefParam="false" />\r\n        <String name="syncAnimationName" value="" refParamName="" useRefParam="false" />\r\n        <String name="customTagName" value="" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>\r\n  </Action>""")
                with open (file_path,'wb') as f : f.write(noidung)
                Track_Guid_Skill(f'{FolderMod}/Resources/{Ver}/Ages/mod2/Prefab_Gear/Defense') 
                try:
                    folder_path = f'{FolderMod}/Resources/{Ver}/Ages/mod2/'
                    output_path = f'{FolderMod}/Resources/{Ver}/Ages/Prefab_Gear.pkg.bytes'
                    zip_folder(folder_path, output_path)
                except Exception as e:
                    print(e)
                shutil.rmtree(f'{FolderMod}/Resources/{Ver}/Ages/mod2/', ignore_errors=True)
#-----------------------------------------------
        if IDCHECK == "13011":
            giapcuongnoyan = 'y'#input("\033[1;97m[\033[1;92m?\033[1;97m] SPECIAL: 54402 - MOD EFX GIÁP CUỒNG NỘ YAN Y/n \n[\033[1;92m•\033[1;97m] INPUT: ")
            if giapcuongnoyan.lower() == 'y':	
                with zipfile.ZipFile(f'Resources/{Ver}/Ages/Prefab_Gear.pkg.bytes') as f:
                    f.extractall(f'{FolderMod}/Resources/{Ver}/Ages/mod2/')
                    file_path=f'{FolderMod}/Resources/{Ver}/Ages/mod2/Prefab_Gear/Defense/1338E1.xml'
                    giai(file_path)
                    with open (file_path, 'rb') as f:
                        noidung = f.read()
                        noidung = noidung.replace(b"</Action>", b"""  <Track trackName="CheckHeroIdTick" eventType="CheckHeroIdTick" guid="54402-YanTanJiro" enabled="true" refParamName="" useRefParam="false" r="0.667" g="1.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Event eventName="CheckHeroIdTick" time="0.000" isDuration="false">\r\n        <TemplateObject name="targetId" objectName="target" id="1" isTemp="false" refParamName="" useRefParam="false"/>\r\n        <int name="heroId" value="130" refParamName="" useRefParam="false"/>\r\n      </Event>\r\n    </Track>\r\n    <Track trackName="TriggerParticle0" eventType="TriggerParticle" guid="54402-YanTanJiro" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true" lod="0">\r\n      <Condition id="0" guid="54402-YanTanJiro" status="true" />\r\n      <Event eventName="TriggerParticle" time="0.000" length="2.000" isDuration="true" guid="54402-YanTanJiro">\r\n        <TemplateObject name="targetId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <TemplateObject name="objectSpaceId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <String name="resourceName" value="prefab_skill_effects/hero_skill_effects/130_GongBenWuZang/13011/jiasu_tongyong_01" refParamName="" useRefParam="false" />\r\n        <Vector3 name="bindPosOffset" x="0.000" y="0.700" z="-0.600" refParamName="" useRefParam="false" />\r\n        <Vector3i name="scalingInt" x="10000" y="10000" z="10000" refParamName="" useRefParam="false" />\r\n        <String name="syncAnimationName" value="" refParamName="" useRefParam="false" />\r\n        <String name="customTagName" value="" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>\r\n  </Action>""")
                    with open (file_path,'wb') as f : f.write(noidung)
                    Track_Guid_Skill(f'{FolderMod}/Resources/{Ver}/Ages/mod2/Prefab_Gear/Defense')
                    try:
                        folder_path = f'{FolderMod}/Resources/{Ver}/Ages/mod2/'
                        output_path = f'{FolderMod}/Resources/{Ver}/Ages/Prefab_Gear.pkg.bytes'
                        zip_folder(folder_path, output_path)
                    except Exception as e:
                        print(e)
                    shutil.rmtree(f'{FolderMod}/Resources/{Ver}/Ages/mod2/', ignore_errors=True)
#-----------------------------------------------
        if IDCHECK == "19007":
            giapcuongnoyan = 'y'#input("\033[1;97m[\033[1;92m?\033[1;97m] SPECIAL: 54402 - MOD EFX GIÁP CUỒNG NỘ YAN Y/n \n[\033[1;92m•\033[1;97m] INPUT: ")
            if giapcuongnoyan.lower() == 'y':	
                with zipfile.ZipFile(f'Resources/{Ver}/Ages/Prefab_Gear.pkg.bytes') as f:
                    f.extractall(f'{FolderMod}/Resources/{Ver}/Ages/mod2/')
                    file_path=f'{FolderMod}/Resources/{Ver}/Ages/mod2/Prefab_Gear/Defense/1338E1.xml'
                    giai(file_path)
                    with open (file_path, 'rb') as f:
                        noidung = f.read()
                        noidung = noidung.replace(b"</Action>", b"""  <Track trackName="CheckHeroIdTick" eventType="CheckHeroIdTick" guid="54402-YanTanJiro" enabled="true" refParamName="" useRefParam="false" r="0.667" g="1.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Event eventName="CheckHeroIdTick" time="0.000" isDuration="false">\r\n        <TemplateObject name="targetId" objectName="target" id="1" isTemp="false" refParamName="" useRefParam="false"/>\r\n        <int name="heroId" value="190" refParamName="" useRefParam="false"/>\r\n      </Event>\r\n    </Track>\r\n    <Track trackName="TriggerParticle0" eventType="TriggerParticle" guid="54402-YanTanJiro" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true" lod="0">\r\n      <Condition id="0" guid="54402-YanTanJiro" status="true" />\r\n      <Event eventName="TriggerParticle" time="0.000" length="2.000" isDuration="true" guid="54402-YanTanJiro">\r\n        <TemplateObject name="targetId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <TemplateObject name="objectSpaceId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <String name="resourceName" value="prefab_skill_effects/hero_skill_effects/190_ZhuGeLiang/19007/jiasu_tongyong_01" refParamName="" useRefParam="false" />\r\n        <Vector3 name="bindPosOffset" x="0.000" y="0.700" z="-0.600" refParamName="" useRefParam="false" />\r\n        <Vector3i name="scalingInt" x="10000" y="10000" z="10000" refParamName="" useRefParam="false" />\r\n        <String name="syncAnimationName" value="" refParamName="" useRefParam="false" />\r\n        <String name="customTagName" value="" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>\r\n  </Action>""")
                    with open (file_path,'wb') as f : f.write(noidung)
                    Track_Guid_Skill(f'{FolderMod}/Resources/{Ver}/Ages/mod2/Prefab_Gear/Defense')
                    try:
                        folder_path = f'{FolderMod}/Resources/{Ver}/Ages/mod2/'
                        output_path = f'{FolderMod}/Resources/{Ver}/Ages/Prefab_Gear.pkg.bytes'
                        zip_folder(folder_path, output_path)
                    except Exception as e:
                        print(e)
                    shutil.rmtree(f'{FolderMod}/Resources/{Ver}/Ages/mod2/', ignore_errors=True)
#-----------------------------------------------
        if IDCHECK == "13210":
            giapcuongnoyan =  'y'#input("\033[1;97m[\033[1;92m?\033[1;97m] SPECIAL: 54402 - MOD EFX GIÁP CUỒNG NỘ YAN Y/n \n[\033[1;92m•\033[1;97m] INPUT: ")
            if giapcuongnoyan.lower() == 'y':	
                with zipfile.ZipFile(f'Resources/{Ver}/Ages/Prefab_Gear.pkg.bytes') as f:
                    f.extractall(f'{FolderMod}/Resources/{Ver}/Ages/mod2/')
                    file_path=f'{FolderMod}/Resources/{Ver}/Ages/mod2/Prefab_Gear/Defense/1338E1.xml'
                    giai(file_path)
                    with open (file_path, 'rb') as f:
                        noidung = f.read()
                        noidung = noidung.replace(b"</Action>", b"""  <Track trackName="CheckHeroIdTick" eventType="CheckHeroIdTick" guid="54402-YanTanJiro" enabled="true" refParamName="" useRefParam="false" r="0.667" g="1.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Event eventName="CheckHeroIdTick" time="0.000" isDuration="false">\r\n        <TemplateObject name="targetId" objectName="target" id="1" isTemp="false" refParamName="" useRefParam="false"/>\r\n        <int name="heroId" value="132" refParamName="" useRefParam="false"/>\r\n      </Event>\r\n    </Track>\r\n    <Track trackName="TriggerParticle0" eventType="TriggerParticle" guid="54402-YanTanJiro" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true" lod="0">\r\n      <Condition id="0" guid="54402-YanTanJiro" status="true" />\r\n      <Event eventName="TriggerParticle" time="0.000" length="2.000" isDuration="true" guid="54402-YanTanJiro">\r\n        <TemplateObject name="targetId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <TemplateObject name="objectSpaceId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <String name="resourceName" value="prefab_skill_effects/hero_skill_effects/132_MaKeBoLuo/13210/jiasu_tongyong_01" refParamName="" useRefParam="false" />\r\n        <Vector3 name="bindPosOffset" x="0.000" y="0.700" z="-0.600" refParamName="" useRefParam="false" />\r\n        <Vector3i name="scalingInt" x="10000" y="10000" z="10000" refParamName="" useRefParam="false" />\r\n        <String name="syncAnimationName" value="" refParamName="" useRefParam="false" />\r\n        <String name="customTagName" value="" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>\r\n  </Action>""")
                    with open (file_path,'wb') as f : f.write(noidung) 
                    Track_Guid_Skill(f'{FolderMod}/Resources/{Ver}/Ages/mod2/Prefab_Gear/Defense')
                    try:
                        folder_path = f'{FolderMod}/Resources/{Ver}/Ages/mod2/'
                        output_path = f'{FolderMod}/Resources/{Ver}/Ages/Prefab_Gear.pkg.bytes'
                        zip_folder(folder_path, output_path)
                    except Exception as e:
                        print(e)
                    shutil.rmtree(f'{FolderMod}/Resources/{Ver}/Ages/mod2/', ignore_errors=True)
#-----------------------------------------------
        if IDCHECK == "15710":
            giapcuongnoyan =  'y'#input("\033[1;97m[\033[1;92m?\033[1;97m] SPECIAL: 54402 - MOD EFX GIÁP CUỒNG NỘ YAN Y/n \n[\033[1;92m•\033[1;97m] INPUT: ")
            if giapcuongnoyan.lower() == 'y':	
                with zipfile.ZipFile(f'Resources/{Ver}/Ages/Prefab_Gear.pkg.bytes') as f:
                    f.extractall(f'{FolderMod}/Resources/{Ver}/Ages/mod2/')
                    file_path=f'{FolderMod}/Resources/{Ver}/Ages/mod2/Prefab_Gear/Defense/1338E1.xml'
                    giai(file_path)
                    with open (file_path, 'rb') as f:
                        noidung = f.read()
                        noidung = noidung.replace(b"</Action>", b"""  <Track trackName="CheckHeroIdTick" eventType="CheckHeroIdTick" guid="54402-YanTanJiro" enabled="true" refParamName="" useRefParam="false" r="0.667" g="1.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Event eventName="CheckHeroIdTick" time="0.000" isDuration="false">\r\n        <TemplateObject name="targetId" objectName="target" id="1" isTemp="false" refParamName="" useRefParam="false"/>\r\n        <int name="heroId" value="132" refParamName="" useRefParam="false"/>\r\n      </Event>\r\n    </Track>\r\n    <Track trackName="TriggerParticle0" eventType="TriggerParticle" guid="54402-YanTanJiro" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true" lod="0">\r\n      <Condition id="0" guid="54402-YanTanJiro" status="true" />\r\n      <Event eventName="TriggerParticle" time="0.000" length="2.000" isDuration="true" guid="54402-YanTanJiro">\r\n        <TemplateObject name="targetId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <TemplateObject name="objectSpaceId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <String name="resourceName" value="prefab_skill_effects/hero_skill_effects/157_BuZhiHuoWu/15710/jiasu_tongyong_01" refParamName="" useRefParam="false" />\r\n        <Vector3 name="bindPosOffset" x="0.000" y="0.700" z="-0.600" refParamName="" useRefParam="false" />\r\n        <Vector3i name="scalingInt" x="10000" y="10000" z="10000" refParamName="" useRefParam="false" />\r\n        <String name="syncAnimationName" value="" refParamName="" useRefParam="false" />\r\n        <String name="customTagName" value="" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>\r\n  </Action>""")
                    with open (file_path,'wb') as f : f.write(noidung)
                    Track_Guid_Skill(f'{FolderMod}/Resources/{Ver}/Ages/mod2/Prefab_Gear/Defense')
                    try:
                        folder_path = f'{FolderMod}/Resources/{Ver}/Ages/mod2/'
                        output_path = f'{FolderMod}/Resources/{Ver}/Ages/Prefab_Gear.pkg.bytes'
                        zip_folder(folder_path, output_path)
                    except Exception as e:
                        print(e)
                    shutil.rmtree(f'{FolderMod}/Resources/{Ver}/Ages/mod2/', ignore_errors=True)
#-----------------------------------------------
    if IDMODSKIN == '59702':
        giapcuongnoyan =  'y'#input("\033[1;97m[\033[1;92m?\033[1;97m] SPECIAL: 54402 - MOD EFX GIÁP CUỒNG NỘ YAN Y/n \n[\033[1;92m•\033[1;97m] INPUT: ")
        if giapcuongnoyan.lower() == 'y':	
            with zipfile.ZipFile(f'Resources/{Ver}/Ages/Prefab_Gear.pkg.bytes') as f:
                f.extractall(f'{FolderMod}/Resources/{Ver}/Ages/mod2/')
                file_path=f'{FolderMod}/Resources/{Ver}/Ages/mod2/Prefab_Gear/Defense/1338E1.xml'
                giai(file_path)
                with open (file_path, 'rb') as f:
                    noidung = f.read()
                    noidung = noidung.replace(b'</Action>', b'  <Track trackName="CheckHeroIdTick" eventType="CheckHeroIdTick" guid="54402-YanTanJiro" enabled="true" refParamName="" useRefParam="false" r="0.667" g="1.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Event eventName="CheckHeroIdTick" time="0.000" isDuration="false">\r\n        <TemplateObject name="targetId" objectName="target" id="1" isTemp="false" refParamName="" useRefParam="false"/>\r\n        <int name="heroId" value="597" refParamName="" useRefParam="false"/>\r\n      </Event>\r\n    </Track>\r\n        <Track trackName="TriggerParticle0" eventType="TriggerParticle" guid="3bb07807-0ec8-4d4a-a8fe-385f9e28e4c3" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\n      <Event eventName="TriggerParticle" time="0.000" length="2.000" isDuration="true" guid="2b3af436-2730-4d8d-bb09-c9c742566e4e">\n        <TemplateObject name="targetId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\n        <TemplateObject name="objectSpaceId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\n        <String name="resourceName" value="prefab_skill_effects/hero_skill_effects/597_kuangtie/59702/kuangbao_buff_01" refParamName="" useRefParam="false" />\n        <String name="bindPointName" value="Bip001 L Hand" refParamName="" useRefParam="false" />\n        <Vector3i name="scalingInt" x="10000" y="10000" z="10000" refParamName="" useRefParam="false" />\n        <String name="syncAnimationName" value="" refParamName="" useRefParam="false" />\n        <String name="customTagName" value="" refParamName="" useRefParam="false" />\n      <Event>\n    </Track>\n    <Track trackName="TriggerParticle0" eventType="TriggerParticle" guid="ea95a7f5-5cc8-457d-ba3e-11a5e66f1203" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\n      <Event eventName="TriggerParticle" time="0.000" length="2.000" isDuration="true" guid="018aaa4e-cc46-4269-aaca-595cc79d1b4e">\n        <TemplateObject name="targetId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\n        <TemplateObject name="objectSpaceId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\n        <String name="resourceName" value="prefab_skill_effects/hero_skill_effects/597_kuangtie/59702/kuangbao_buff_01" refParamName="" useRefParam="false" />\n        <String name="bindPointName" value="Bip001 R Hand" refParamName="" useRefParam="false" />\n        <bool name="dontShowIfNoBindPoint" value="false" refParamName="" useRefParam="true" />\n        <Vector3i name="scalingInt" x="10000" y="10000" z="10000" refParamName="" useRefParam="false" />\n        <String name="syncAnimationName" value="" refParamName="" useRefParam="false" />\n        <String name="customTagName" value="" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>\r\n  </Action>')
                    with open (file_path,'wb') as f : f.write(noidung)
                    Track_Guid_Skill(f'{FolderMod}/Resources/{Ver}/Ages/mod2/Prefab_Gear/Defense')
                    try:
                        folder_path = f'{FolderMod}/Resources/{Ver}/Ages/mod2/'
                        output_path = f'{FolderMod}/Resources/{Ver}/Ages/Prefab_Gear.pkg.bytes'
                        zip_folder(folder_path, output_path)
                    except Exception as e:
                        print(e)
                    shutil.rmtree(f'{FolderMod}/Resources/{Ver}/Ages/mod2/', ignore_errors=True)
#-----------------------------------------------
        if CAMXA.lower() == 'y':
            duongdancamxa=f'{FolderMod}/Resources/{Ver}/Ages/Prefab_Characters/Prefab_Hero/mod1/PassiveResource/junglemark.xml'
            giai(duongdancamxa)
            with open (duongdancamxa, 'rb') as f:
                noidungsexx = f.read()            
                noidungsexx = noidungsexx.replace(b'</Action>', b"""  <Track trackName="SetCameraHeightDuration0" eventType="SetCameraHeightDuration" guid="9489c796-894b-4c2e-9a95-acf27873964a" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\n    <Event eventName="SetCameraHeightDuration" time="0.000" length="1.000" isDuration="true" guid="422a1ed9-a12c-44b3-a9c5-3fe899d689dd">\n      <int name="slerpTick" value="0" refParamName="" useRefParam="false"/>\n        <float name="heightRate" value="1.25" refParamName="" useRefParam="false"/>\n        <bool name="bOverride" value="true" refParamName="" useRefParam="false"/>\n        <bool name="leftTimeSlerpBack" value="true" refParamName="" useRefParam="false"/>\n        <String name="refParamName" value="" refParamName="" useRefParam="false"/>\n      </Event>\n	</Track>\n <Track trackName="InBattleMsgSendTick0" eventType="InBattleMsgSendTick" guid="5169fb6a-26eb-4bf0-ae25-0da74fe7d84a" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\n	<Event eventName="InBattleMsgSendTick" time="0.000" isDuration="false" guid="9473c11a-e73b-4a84-b950-3b39d37dee13">\n	  <TemplateObject name="targetId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\n  	<String name="msgKey" value="Create:YtbTamModAOV" refParamName="" useRefParam="false" />\n	</Event>\n  </Track>\n    </Action>""")    
            with open (duongdancamxa,'wb') as f : f.write(noidungsexx)
            giai(duongdancamxa)
    if Anti == 'Y' or Anti == 'y':
        process_folder(FolderMod+f'/Resources/{Ver}/Ages/Prefab_Characters/Prefab_Hero/mod4/')
#-----------------------------------------------
    SkinSpecial = IDMODSKIN
    IDM = IDMODSKIN
    if SkinSpecial in IDMODSKIN:
        if IDM in IDMODSKIN:
            INFOMOD = f'{FolderMod}/Resources/{Ver}/Prefab_Characters/mod/'
            #shutil.rmtree(INFOMOD)
            with zipfile.ZipFile(f'Resources/{Ver}/Prefab_Characters/Actor_'+f'{IDINFO[:3]}'+'_Infos.pkg.bytes') as f:
                f.extractall(INFOMOD)
            Premium = Path(INFOMOD) / "Prefab_Hero"
            
            LosAngles = [
                NCZ
                for BeginSkin in Premium.iterdir() if BeginSkin.is_dir()
                for NCZ in BeginSkin.glob("*.bytes")
                if NCZ.name.lower() == f"{BeginSkin.name.lower()}_actorinfo.bytes"
            ]
            
            print(LosAngles)

            Bulma_Lab = LosAngles[0]
            giai(INFOMOD)
            Goku_Aura = IDINFO.encode()
            with open(Bulma_Lab, "rb") as Capsule:
                Shenron_Energy = bytearray(Capsule.read())
            Power_Limit_SSJ1 = (1 << 16) - 1 # 16-bit
            Power_Limit_SSJ3 = (1 << 32) - 1 # 32-bit
            Pos_Goku = Shenron_Energy.find(Goku_Aura)
            Spirit_Bombs = []
            Vegeta_Focus = 0
            while True:
                Vegeta_Focus = Shenron_Energy.find(b"ArtSkinPrefabLOD0", Vegeta_Focus)
                if Vegeta_Focus == -1:
                    break
                Spirit_Bombs.append(Vegeta_Focus)
                Vegeta_Focus += len(b"ArtSkinPrefabLOD0")
            Piccolo_Block = -1
            for Ki_Pulse in Spirit_Bombs:
                if Ki_Pulse < Pos_Goku:
                    Piccolo_Block = Ki_Pulse
                else:
                    break
            Piccolo_Block = Shenron_Energy.rfind(b"TypeAssets.Scripts.GameLogic.SkinElement", 0, Piccolo_Block) - 44
            Kamehameha_Power = struct.unpack("<H", Shenron_Energy[Piccolo_Block:Piccolo_Block + 2])[0]
            Krillin_Core = Shenron_Energy.find(b"SkinPrefabG")
            Trunks_Left = Krillin_Core - 8
            Trunks_Right = Krillin_Core + 89 - 4
            Energy_Left = struct.unpack("<I", Shenron_Energy[Trunks_Left:Trunks_Left + 4])[0]
            Energy_Right = struct.unpack("<I", Shenron_Energy[Trunks_Right:Trunks_Right + 4])[0]
            Broly_Left = Energy_Left
            Broly_Right = Energy_Right
            Round_Fight = 0
            for Majin_Buu in Spirit_Bombs:
                Majin_Buu = Shenron_Energy.rfind(b"TypeAssets.Scripts.GameLogic.SkinElement", 0, Majin_Buu) - 44
                Frieza_Power = struct.unpack("<H", Shenron_Energy[Majin_Buu:Majin_Buu + 2])[0]
                Saiyan_Dsn = Kamehameha_Power - Frieza_Power
                if Saiyan_Dsn > Power_Limit_SSJ1 // 2:
                    Saiyan_Dsn -= (Power_Limit_SSJ1 + 1)
                elif Saiyan_Dsn < -Power_Limit_SSJ1 // 2:
                    Saiyan_Dsn += (Power_Limit_SSJ1 + 1)
                Round_Fight += 1
                Broly_Left += Saiyan_Dsn
                Broly_Right += Saiyan_Dsn
                if Broly_Left > Power_Limit_SSJ1 or Broly_Left < 0:
                    Broly_Left &= Power_Limit_SSJ3
                    Broly_Right &= Power_Limit_SSJ3
                    Shenron_Energy[Trunks_Left:Trunks_Left + 4] = struct.pack("<I", Broly_Left)
                    Shenron_Energy[Trunks_Right:Trunks_Right + 4] = struct.pack("<I", Broly_Right)
                else:
                    Broly_Left &= Power_Limit_SSJ1
                    Broly_Right &= Power_Limit_SSJ1
                    Shenron_Energy[Trunks_Left:Trunks_Left + 2] = struct.pack("<H", Broly_Left)
                    Shenron_Energy[Trunks_Right:Trunks_Right + 2] = struct.pack("<H", Broly_Right)
            with open(Bulma_Lab, "wb") as Capsule:
                Capsule.write(Shenron_Energy)
            
            
            with open(Bulma_Lab, 'rb') as Jennie:
                Taehyung = bytearray(Jennie.read())
            Suho = Taehyung.find(Goku_Aura)
            Kai = Taehyung.rfind(b'ArtSkinPrefabLOD0', 0, Suho)
            Jisoo = Taehyung.rfind(b"TypeAssets.Scripts.GameLogic.SkinElement", 0, Kai) - 44
            Byte1 = Taehyung[Jisoo]
            Byte2 = Taehyung[Jisoo + 1]
            RM = Byte1 + Byte2 * 256
            Rose = Taehyung[Jisoo:Jisoo + RM]
            Lisa = 0
            Sana = 0
            while True:
                Chaeyoung = Taehyung.find(b'ArtSkinPrefabLOD0', Lisa)
                if Chaeyoung == -1:
                    break
                Dahyun = Taehyung.rfind(b"TypeAssets.Scripts.GameLogic.SkinElement", 0, Chaeyoung) - 44
                if Dahyun < 0:
                    Lisa = Chaeyoung + len(b'ArtSkinPrefabLOD0')
                    continue
                Byte1 = Taehyung[Dahyun]
                Byte2 = Taehyung[Dahyun + 1]
                Mina = Byte1 + Byte2 * 256
                if Dahyun == Jisoo:
                    Lisa = Chaeyoung + len(b'ArtSkinPrefabLOD0')
                    continue
                Taehyung[Dahyun:Dahyun + Mina] = Rose
                Lisa = Chaeyoung + len(b'ArtSkinPrefabLOD0')
                Sana += 1
            with open(Bulma_Lab, 'wb') as Yeri:
                Yeri.write(Taehyung)
            Ferrari = Bulma_Lab
            Lamborghini = Ferrari
            
            with open(Ferrari, "rb") as f1, open(Lamborghini, "rb") as f2:
                Bugatti = f1.read()
                McLaren = f2.read()
            
            AstonMartin = Bugatti.find(b"ArtPrefabLOD0")
            Koenigsegg = Bugatti.find(b"SkinPrefabG")
            
            if AstonMartin != -1 and Koenigsegg != -1:
                Maserati = AstonMartin - 8
                Pagani = Koenigsegg - 8
                CodeMD = Bugatti[Maserati:Pagani]
            if IDM[:3] == '544':  # 544
                Zenvo1 = Bugatti.find(b"ArtLobbyIdleShowLOD")
            else:
                Zenvo1 = Bugatti.find(b"ArtSkinLobbyShowCamera")
                
            Koenigsegg = Bugatti.find(b"SkinPrefabG")
            Hennessey1 = 0
            
            if Zenvo1 != -1:
                Bug1 = Zenvo1 - 8
                if Bug1 < 0:
                    Bug1 = 0
                Lykan1 = int.from_bytes(Bugatti[Bug1:Bug1 + 4], "little")
                Veneno1 = Bug1 + Lykan1
            
                for i in range(99999):
                    try:
                        Devel1 = int.from_bytes(Bugatti[Veneno1:Veneno1 + 4], "little")
                        Apollo1 = Bugatti[Veneno1:Veneno1 + Devel1]
            
                        if b"SkinPrefabG" in Apollo1:
                            break
            
                        if not Apollo1.strip(b'\x00'):
                            break
            
                        Hennessey1 += 1
                        Veneno1 += Devel1
            
                    except Exception:
                        break
            
            RollsRoyce = Goku_Aura
            Bentley = McLaren.find(RollsRoyce)
            Maybach = McLaren.rfind(b"ArtSkinPrefabLOD0", 0, Bentley)
            
            Porsche = McLaren.rfind(b"TypeAssets.Scripts.GameLogic.SkinElement", 0, Maybach) - 44
            Lotus = McLaren[Porsche:Porsche + 2]
            Tesla = int.from_bytes(Lotus, "little")
            Rimac = McLaren[Porsche:Porsche + Tesla]
            Zenvo2 = Rimac.find(b"ArtSkinLobbyShowCamera")
            if Zenvo2 == -1:
                Zenvo2 = Rimac.find(b"ArtSkinLobbyIdleShowLOD")
            Hennessey2 = 0
            if Zenvo2 != -1:
                Bug2 = Zenvo2 - 8
                if Bug2 < 0:
                    Bug2 = 0
                Lykan2 = int.from_bytes(Rimac[Bug2:Bug2 + 4], "little")
                Veneno2 = Bug2 + Lykan2
                IsHokSkin = 0
                while IsHokSkin < Bug2:
                    try:
                        hasHokCameraAnim = int.from_bytes(Rimac[IsHokSkin:IsHokSkin + 4], "little")
                        if hasHokCameraAnim <= 0:
                            break
                        ArtEnemy = Rimac[IsHokSkin:IsHokSkin + hasHokCameraAnim]
                        if not Apollo2.strip(b'\x00'):
                        	break
                        IsHokSkin += hasHokCameraAnim
                        Hennessey2 += 1
                    except Exception:
                        break
                for i in range(99999):
                    try:
                        Devel2 = int.from_bytes(Rimac[Veneno2:Veneno2 + 4], "little")
                        Apollo2 = Rimac[Veneno2:Veneno2 + Devel2]
                        if not Apollo2.strip(b'\x00'):
                            break
                        Hennessey2 += 1
                        Veneno2 += Devel2
                    except Exception:
                        break
            
            if AstonMartin != -1 and Koenigsegg != -1:
                Czinger = bytearray(Bugatti[:Maserati] + Rimac[96:] + Bugatti[Pagani:])
                SSC = [
                    (b"ArtSkinPrefabLOD0", b"ArtPrefabLOD0",1),
                    (b"ArtSkinPrefabLODEx", b"ArtPrefabLODEx",1),
                    (b"ArtSkinLobbyShowLOD0", b"ArtLobbyShowLOD0",1),
                    (b"ArtSkinLobbyIdleShowLOD0", b"ArtLobbyIdleShowLOD0",1)
                ]
            
                for Acura, Alfa, GioiHan in SSC:
                    Lucid = Czinger.find(Acura)
                    if Lucid != -1:
                        Czinger = Czinger.replace(Acura, Alfa, GioiHan)  
                        Karma = Lucid - 4
                        if Karma > 0:
                            Ariel = Czinger[Karma:Lucid]
                            Hispano = int.from_bytes(Ariel, "little")
                            Vector = Hispano - 4
                            print(f" {Ariel} → {Hispano} - 4 = {Vector}")
                            Czinger[Karma:Karma + 4] = Vector.to_bytes(4, "little")
                        BAC = Lucid - 8
                        if BAC > 0:
                            Fisker = Czinger[BAC:BAC + 2]
                            Spania = int.from_bytes(Fisker, "little")
                            Pinin = Spania - 4
                            print(f" {Fisker} → {Spania} - 4 = {Pinin}")
                            Czinger[BAC:BAC + 2] = Pinin.to_bytes(2, "little")
            
                Morgan = Czinger.find(b"ActorName")
                if Morgan != -1:
                    Spyker = Morgan - 12
                    Ultima = Czinger[Spyker:Spyker + 1]
                    Wiesmann = int.from_bytes(Ultima, "little")
                    Ginetta = Wiesmann + Hennessey2 - Hennessey1
                    Arrinera = Ginetta.to_bytes(1, "little")
                    print(f"\n ActorName: {Ultima} ({Wiesmann}) + {Hennessey2} - {Hennessey1} = {Ginetta}")
                    Czinger[Spyker:Spyker + 1] = Arrinera
            
                with open(Ferrari, "wb") as f:
                    f.write(Czinger)

            with open(Bulma_Lab, "rb") as f:
                YuaMikami = bytearray(f.read())

            DsAnimation = [
                (b"5486", [b"useNewMecanim", b"oriSkinUseNewMecanim"], 2),
                (b"19016", [b"useMecanim"], 1),
                (b"5443", [b"useTimeline"], 1),
                (b"1749", [b"useNewMecanim"], 1)
]

            for JavID, Aoi, ActorSub in DsAnimation:
                if JavID in YuaMikami:
                    for Rion in Aoi:
                        while True:
                            Sakura = YuaMikami.find(Rion)
                            if Sakura == -1:
                                break
                            Haruka = Sakura - 8
                            Mio = int.from_bytes(YuaMikami[Haruka:Haruka+4], "little")
                            Akari = Haruka + Mio
                            del YuaMikami[Haruka:Akari]

                    Hina = YuaMikami.find(b"ActorName")
                    if Hina != -1:
                        Yui = Hina - 12
                        YuaMikami[Yui] -= ActorSub

            Rena = len(YuaMikami)
            YuaMikami[0:4] = Rena.to_bytes(4, "little")

            Saki = Rena - 84
            YuaMikami[84:88] = Saki.to_bytes(4, "little")

            with open(Bulma_Lab, "wb") as f:
                f.write(YuaMikami)
            if IDM[:3]=="544":
                with open(Bulma_Lab, "rb") as FPT:
                    Vinamilk = bytearray(FPT.read())
                
                VNG = Vinamilk.find(b"PreloadAnimatorEffects0")
                FPTShop = Vinamilk.find(b"SkinPrefabG", VNG)
                
                Masan = VNG - 8
                HoaPhat = Masan
                Techcombank = 0
                
                while HoaPhat < FPTShop:
                    Sabeco = struct.unpack("<I", Vinamilk[HoaPhat:HoaPhat+4])[0]
                    Bamboo = HoaPhat + Sabeco
                    if Bamboo > FPTShop:
                        break
                    Techcombank += 1
                    HoaPhat = Bamboo
                
                VPBank = HoaPhat
                
                del Vinamilk[Masan:VPBank]
                
                Mobifone = Vinamilk.find(b"ActorName")
                THTrueMilk = Mobifone - 12
                
                Vinamilk[THTrueMilk] = Vinamilk[THTrueMilk] - Techcombank
                
                with open(Bulma_Lab, "wb") as VietnamAirlines: VietnamAirlines.write(Vinamilk)
    
        if IDM == '13311':
            LC = '1'
            process_directory(Bulma_Lab, LC)
            with open(Bulma_Lab, 'rb') as f:
                ALL_CODE_GOC = f.read()
            ALL_CODE_GOC = ALL_CODE_GOC.replace(b'Prefab_Characters/Prefab_Hero/133_DiRenJie/13312_DiRenJie_AW1_', b'Prefab_Characters/Prefab_Hero/133_DiRenJie/Awaken/13312_DiRenJie_04_').replace(b'Prefab_Characters/Prefab_Hero/133_DiRenJie/1331_DiRenJie_Cam', b'Prefab_Characters/Prefab_Hero/133_DiRenJie/Awaken/13312_DiRenJie_AW5_Cam')
            with open(Bulma_Lab, 'wb') as f:
                f.write(ALL_CODE_GOC)
        
            LC = '2'
            process_directory(Bulma_Lab, LC)
        
        if IDM == '16707': 
            LC = '1'
            process_directory(Bulma_Lab, LC)
            with open(Bulma_Lab, 'rb') as f:
                ALL_CODE_GOC = f.read()
            ALL_CODE_GOC = ALL_CODE_GOC.replace(b'Prefab_Characters/Prefab_Hero/167_WuKong/1678_SunWuKong_AW1_Cam"/>', b'Prefab_Characters/Prefab_Hero/167_WuKong/Awaken/1678_SunWuKong_03_Cam"/>\n  <ArtSkinLobbyShowMovie var="String" type="System.String" value="Prefab_Characters/Prefab_Hero/167_WuKong/Awaken/1678_SunWuKong_03_Movie"/>').replace(b'Prefab_Characters/Prefab_Hero/167_WuKong/1678_SunWuKong_AW1_', b'Prefab_Characters/Prefab_Hero/167_WuKong/Awaken/1678_SunWuKong_03_').replace(b'prefab_skill_effects/hero_skill_effects/167_WuKong/', b'prefab_skill_effects/component_effects/16707/16707_5/')
            with open(Bulma_Lab, 'wb') as f:
                f.write(ALL_CODE_GOC)
        
            LC = '2'
            process_directory(Bulma_Lab, LC)
        if IDM == '11620':
            if phukienb == 'do':
                LC = '1'
                process_directory(Bulma_Lab, LC)
                with open(Bulma_Lab, 'rb') as f:
                    pk1 = f.read()
                    pk1 = pk1.replace(
                        b'AW1', b'AW5').replace(b'<ArtSkinLobbyShowCamera var="String" type="System.String" value="Prefab_Characters/Prefab_Hero/116_JingKe/Awaken/11621_JingKe_AW5_Cam"/>', b'<ArtSkinLobbyShowCamera var="String" type="System.String" value="Prefab_Characters/Prefab_Hero/116_JingKe/Awaken/11621_JingKe_AW5_Cam"/>\n  <ArtSkinLobbyShowMovie var="String" type="System.String" value="Prefab_Characters/Prefab_Hero/116_JingKe/Awaken/11621_JingKe_Movie"/>').replace(b'116_JingKe/11621_JingKe_AW5_LOD', b'116_JingKe/Component/11621_JingKe_RT_3_LOD').replace(b'116_JingKe/11621_JingKe_AW5_Show', b'116_JingKe/Component/11621_JingKe_RT_3_Show')
        
                with open(Bulma_Lab, 'wb') as f:
                    f.write(pk1)
        
                LC = '2'
                process_directory(Bulma_Lab, LC)
            elif phukienb == 'tim':
                LC = '1'
                process_directory(Bulma_Lab, LC)
                with open(Bulma_Lab, 'rb') as f:
                    pk2 = f.read()
                    pk2 = pk2.replace(
                        b'AW1', b'AW5').replace(b'<ArtSkinLobbyShowCamera var="String" type="System.String" value="Prefab_Characters/Prefab_Hero/116_JingKe/Awaken/11621_JingKe_AW5_Cam"/>', b'<ArtSkinLobbyShowCamera var="String" type="System.String" value="Prefab_Characters/Prefab_Hero/116_JingKe/Awaken/11621_JingKe_AW5_Cam"/>\n  <ArtSkinLobbyShowMovie var="String" type="System.String" value="Prefab_Characters/Prefab_Hero/116_JingKe/Awaken/11621_JingKe_Movie"/>').replace(b'116_JingKe/11621_JingKe_AW5_LOD', b'116_JingKe/Component/11621_JingKe_RT_2_LOD').replace(b'116_JingKe/11621_JingKe_AW5_Show', b'116_JingKe/Component/11621_JingKe_RT_2_Show')
        
                with open(Bulma_Lab, 'wb') as f:
                    f.write(pk2)
        
                LC = '2'
                process_directory(Bulma_Lab, LC)
                
            else:
                LC = '1'
                process_directory(Bulma_Lab, LC)
                with open(Bulma_Lab, 'rb') as f:
                    nopk = f.read()
                    nopk = nopk.replace(
                        b'AW1', b'AW5').replace(b'<ArtSkinLobbyShowCamera var="String" type="System.String" value="Prefab_Characters/Prefab_Hero/116_JingKe/Awaken/11621_JingKe_AW5_Cam"/>', b'<ArtSkinLobbyShowCamera var="String" type="System.String" value="Prefab_Characters/Prefab_Hero/116_JingKe/Awaken/11621_JingKe_AW5_Cam"/>\n  <ArtSkinLobbyShowMovie var="String" type="System.String" value="Prefab_Characters/Prefab_Hero/116_JingKe/Awaken/11621_JingKe_Movie"/>')
        
                with open(Bulma_Lab, 'wb') as f:
                    f.write(nopk)
        
                LC = '2'
                process_directory(Bulma_Lab, LC)
        if IDM[:3] == '196':
            if b"Skin_Icon_Skill" in dieukienmod:
                giai(f'./{FolderMod}/Resources/{Ver}/Prefab_Characters/mod/Prefab_Hero/196_Elsu/196_Elsu_trap_actorinfo.bytes')
                Directory = f'./{FolderMod}/Resources/{Ver}/Prefab_Characters/mod/Prefab_Hero/196_Elsu/196_Elsu_trap_actorinfo.bytes'
                with open(Directory, "rb") as f:
                    data = bytearray(f.read())
                skin_bytes = IDCHECK.encode("utf-8")
                pos = data.find(skin_bytes)
                
                poster = pos - 203
                cache = data[poster: poster + 2]
                post = int.from_bytes(cache, "little")
                strin = poster
                string = strin + post
                codeskin = data[strin:string]
                
                pos_lod = data.find(b"ArtPrefabLOD")
                if pos_lod == -1:
                    print("Không tìm thấy 'ArtPrefabLOD' trong file.")
                    sys.exit(0)
                
                pos2 = pos_lod - 8
                codess = data[pos2: pos2 + 2]
                post_md = int.from_bytes(codess, "little")
                strin_md = pos2
                string_md = strin_md + post_md
                codemd = data[strin_md:string_md]
                
                new_codeskin = codeskin.replace(b'ArtSkinPrefabLOD', b'ArtPrefabLOD')
                
                lod_pos = new_codeskin.find(b'ArtPrefabLOD')
                if lod_pos != -1:
                    tinhoffset = lod_pos - 4
                    byteskinmd = new_codeskin[tinhoffset]
                    byteskin = byteskinmd - 4
                    new_codeskin = (new_codeskin[:tinhoffset] +bytes([byteskin]) +new_codeskin[tinhoffset+1:])
                    artskinprefab = lod_pos - 8
                    byteart = new_codeskin[artskinprefab: artskinprefab+2]
                    bytelon = int.from_bytes(byteart, "little")
                    bytecantru = bytelon - 4
                    bytesdaonguoc = bytecantru.to_bytes(2, "little")
                    new_codeskin = (new_codeskin[:artskinprefab] +bytesdaonguoc+new_codeskin[artskinprefab+2:])
                
                data = data.replace(codemd, new_codeskin)
                
                bytetinhlai = data[0:2]
                tinhbyte = int.from_bytes(bytetinhlai, "little")
                tinhbyte += 18
                bytefirst = tinhbyte.to_bytes(2, "little")
                data[0:2] = bytefirst
                
                sl0 = 86 - 2
                sl = data[sl0:sl0+2]
                codez = int.from_bytes(sl, "little")
                codez += 18
                elements = codez.to_bytes(2, "little")
                data[sl0:sl0+2] = elements
                
                with open(Directory, "wb") as f:
                    f.write(data)
#-----------------------------------------------
    antidec(FolderMod + '/Resources/' + Ver + '/Prefab_Characters/mod/')
    antidec(FolderMod + "/Resources/" + Ver + f"/AssetRefs/Hero/{IDCHECK[:3]}_AssetRef.bytes")
    with zipfile.ZipFile(FolderMod+f"/Resources/{Ver}/Prefab_Characters/Actor_"+IDMODSKIN[:3]+"_Infos.pkg.bytes", 'w', zipfile.ZIP_STORED) as z:
        for r, d, f in os.walk(FolderMod+f'/Resources/{Ver}/Prefab_Characters/mod/'):
            for file in f:
                p = os.path.join(r, file)
                z.write(p, os.path.relpath(p, FolderMod+'/Resources/'+Ver+'/Prefab_Characters/mod/'))
        shutil.rmtree(FolderMod+'/Resources/'+Ver+'/Prefab_Characters/mod/')
#-----------------------------------------------
    with zipfile.ZipFile(FolderMod+'/Resources/'+Ver+'/Ages/Prefab_Characters/Prefab_Hero/Actor_'+IDMODSKIN[:3]+"_Actions.pkg.bytes", 'w', zipfile.ZIP_STORED) as z:
        for r, d, f in os.walk(FolderMod+f'/Resources/{Ver}/Ages/Prefab_Characters/Prefab_Hero/mod4/'):
            for file in f:
                p = os.path.join(r, file)
                z.write(p, os.path.relpath(p, FolderMod+f'/Resources/{Ver}/Ages/Prefab_Characters/Prefab_Hero/mod4/'))
    shutil.rmtree(FolderMod+f'/Resources/{Ver}/Ages/Prefab_Characters/Prefab_Hero/mod4/')
#-----------------------------------------------
antidec(f"{FolderMod}/Resources/{Ver}/Ages/Prefab_Characters/Prefab_Hero/mod1/commonresource/Back.xml")
antidec(f"{FolderMod}/Resources/{Ver}/Ages/Prefab_Characters/Prefab_Hero/mod1/commonresource/HasteE1.xml")
antidec(f"{FolderMod}/Resources/{Ver}/Ages/Prefab_Characters/Prefab_Hero/mod1/commonresource/HasteE1_leave.xml")
antidec(FolderMod + "/Resources/" + Ver + "/Databin/Client")
with zipfile.ZipFile(f"{FolderMod}/Resources/{Ver}/Ages/Prefab_Characters/Prefab_Hero/CommonActions.pkg.bytes"
, 'w', zipfile.ZIP_STORED) as z:
    for root, _, files in os.walk(f"{FolderMod}/Resources/{Ver}/Ages/Prefab_Characters/Prefab_Hero/mod1"):
        for f in files:
            fp = os.path.join(root, f)
            z.write(fp, os.path.relpath(fp, f"{FolderMod}/Resources/{Ver}/Ages/Prefab_Characters/Prefab_Hero/mod1"))

shutil.rmtree(f"{FolderMod}/Resources/{Ver}/Ages/Prefab_Characters/Prefab_Hero/mod1")
shutil.rmtree("mod5", ignore_errors=True)
#-----------------------------------------------
shutil.make_archive(f'{FolderMod}/Resources', 'zip', f'{FolderMod}/', 'Resources')
os.rename(f'./{FolderMod}/Resources.zip', f'{FolderMod}/IOS.zip')
