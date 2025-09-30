# -*- coding: utf-8 -*-

path = "Prefab_Hero/544_Painter/544_Painter_actorinfo.bytes"
with open(path, "rb") as f:
    strin = f.read()

IDMODSKIN = input("Nhập IDMODSKIN: ")
IDINFO = str(int(IDMODSKIN) + 1)
if IDINFO[3:4] == '0':
    IDINFO = IDINFO[:3] + IDINFO[4:]
IDINFO = IDINFO.encode()
pos = strin.find(IDINFO)

# --- CodeSkin ---
prefab = strin.rfind(b"ArtSkinPrefabLOD", 0, pos)
codeskin = prefab - 104
len_codeskin = int.from_bytes(strin[codeskin:codeskin+2], "little")
codeskin = strin[codeskin:codeskin+len_codeskin]

# --- ArtSkinPrefabLOD0 ---
p = codeskin.find(b"ArtSkinPrefabLOD0")
l = int.from_bytes(codeskin[p-8:p-4], "little")
ArtSkinPrefabLOD0 = codeskin[p-8:p-8+l]
print("=== ArtSkinPrefabLOD0 ===")
print(ArtSkinPrefabLOD0)

# --- ArtSkinLobbyShowLOD0 ---
p = codeskin.find(b"ArtSkinLobbyShowLOD0")
l = int.from_bytes(codeskin[p-8:p-4], "little")
ArtSkinLobbyShowLOD0 = codeskin[p-8:p-8+l]
print("=== ArtSkinLobbyShowLOD0 ===")
print(ArtSkinLobbyShowLOD0)

# --- ArtSkinLobbyIdleShowLOD ---
p = codeskin.find(b"ArtSkinLobbyIdleShowLOD")
l = int.from_bytes(codeskin[p-8:p-4], "little")
ArtSkinLobbyIdleShowLOD = codeskin[p-8:p-8+l]
print("=== ArtSkinLobbyIdleShowLOD ===")
print(ArtSkinLobbyIdleShowLOD)

# --- ArtSkinLobbyShowCamera ---
p = codeskin.find(b"ArtSkinLobbyShowCamera")
l = int.from_bytes(codeskin[p-8:p-4], "little")
ArtSkinLobbyShowCamera = codeskin[p-8:p-8+l]
print("=== ArtSkinLobbyShowCamera ===")
print(ArtSkinLobbyShowCamera)

# --- ArtSkinLobbyNode ---
p = codeskin.find(b"ArtSkinLobbyNode")
if p != -1:
    l = int.from_bytes(codeskin[p-8:p-4], "little")
    ArtSkinLobbyNode = codeskin[p-8:p-8+l]
    print("=== ArtSkinLobbyNode ===")
    print(ArtSkinLobbyNode)
else:
    ArtSkinLobbyNode = b''
    print("=== ArtSkinLobbyNode NOT FOUND ===")

# --- ArtSkinLobbyShowMovie ---
p = codeskin.find(b"ArtSkinLobbyShowMovie")
if p != -1:
    l = int.from_bytes(codeskin[p-8:p-4], "little")
    ArtSkinLobbyShowMovie = codeskin[p-8:p-8+l]
    print("=== ArtSkinLobbyShowMovie ===")
    print(ArtSkinLobbyShowMovie)
else:
    ArtSkinLobbyShowMovie = b''
    print("=== ArtSkinLobbyShowMovie NOT FOUND ===")

# --- useNewMecanim ---
p = codeskin.find(b"useNewMecanim")
if p != -1:
    l = int.from_bytes(codeskin[p-8:p-4], "little")
    useNewMecanim = codeskin[p-8:p-8+l]
    print("=== useNewMecanim ===")
    print(useNewMecanim)
else:
    useNewMecanim = b''
    print("=== useNewMecanim NOT FOUND ===")

# --- bDisableDirLight ---
p = codeskin.find(b"bDisableDirLight")
if p != -1:
    l = int.from_bytes(codeskin[p-8:p-4], "little")
    bDisableDirLight = codeskin[p-8:p-8+l]
    print("=== bDisableDirLight ===")
    print(bDisableDirLight)
else:
    bDisableDirLight = b''
    print("=== bDisableDirLight NOT FOUND ===")
# --- bUnityLight ---
p = codeskin.find(b"bUnityLight")
if p != -1:
    l = int.from_bytes(codeskin[p-8:p-4], "little")
    bUnityLight = codeskin[p-8:p-8+l]
    print("=== bUnityLight ===")
    print(bUnityLight)
else:
    bUnityLight = b''
    print("=== bUnityLight NOT FOUND ===")
# --- PreloadAnimatorEffects ---
p = codeskin.find(b"PreloadAnimatorEffects")
if p != -1:
    l = int.from_bytes(codeskin[p-8:p-4], "little")
    PreloadAnimatorEffects = codeskin[p-8:p-8+l]
    print("=== PreloadAnimatorEffects ===")
    print(PreloadAnimatorEffects)
else:
    PreloadAnimatorEffects = b''
    print("=== PreloadAnimatorEffects NOT FOUND ===")

# --- useStateDrivenMecanim ---
p = codeskin.find(b"useStateDrivenMecanim")
if p != -1:
    l = int.from_bytes(codeskin[p-8:p-4], "little")
    useStateDrivenMecanim = codeskin[p-8:p-8+l]
    print("=== useStateDrivenMecanim ===")
    print(useStateDrivenMecanim)
else:
    useStateDrivenMecanim = b''
    print("=== useStateDrivenMecanim NOT FOUND ===")
# --- oriSkinUseNewMecanim ---
p = codeskin.find(b"oriSkinUseNewMecanim")
if p != -1:
    l = int.from_bytes(codeskin[p-8:p-4], "little")
    oriSkinUseNewMecanim = codeskin[p-8:p-8+l]
    print("=== oriSkinUseNewMecanim ===")
    print(oriSkinUseNewMecanim)
else:
    oriSkinUseNewMecanim = b''
    print("=== oriSkinUseNewMecanim NOT FOUND ===")

#----------- Code Mặc Định -----------
# --- ArtPrefabLOD0 ---
p = strin.find(b'ArtPrefabLOD0')
l = int.from_bytes(strin[p-8:p-4], "little")
ArtPrefabLOD0 = strin[p-8:p-8+l]
print("=== ArtPrefabLOD0 ===")
print(ArtPrefabLOD0)
# --- ArtPrefabLOD0 ---
p = strin.find(b'ArtLobbyShowLOD0')
l = int.from_bytes(strin[p-8:p-4], "little")
ArtLobbyShowLOD0 = strin[p-8:p-8+l]
print("=== ArtLobbyShowLOD0 ===")
print(ArtLobbyShowLOD0)
# --- ArtLobbyIdleShowLOD0 ---
p = strin.find(b'ArtLobbyIdleShowLOD0')
l = int.from_bytes(strin[p-8:p-4], "little")
ArtLobbyIdleShowLOD0 = strin[p-8:p-8+l]
print("=== ArtLobbyIdleShowLOD0 ===")
print(ArtLobbyIdleShowLOD0)
# --- ArtSkinLobbyShowCameraMd ---
p = strin.find(b"ArtSkinLobbyShowCamera")
l = int.from_bytes(strin[p-8:p-4], "little")
ArtSkinLobbyShowCameraMd = strin[p-8:p-8+l]
print("=== ArtSkinLobbyShowCameraMd ===")
print(ArtSkinLobbyShowCameraMd)
#---------- Tính Offset ----------
# --- Thay ArtPrefabLOD0 bằng ArtSkinPrefabLOD0 ---
strin = strin.replace(ArtPrefabLOD0, ArtSkinPrefabLOD0)

# --- Tìm vị trí ArtSkinPrefabLOD0 ---
pos = strin.find(b"ArtSkinPrefabLOD0")
if pos != -1:
    # đổi tên
    strin = strin[:pos] + b"ArtPrefabLOD0" + strin[pos+len(b"ArtSkinPrefabLOD0"):]

    # --- Lấy 2 byte lùi 8 byte ---
    byte2 = strin[pos-8:pos-6]        # b'\x14\x00'
    tinhbyte2 = int.from_bytes(byte2, "little")  # 20
    bytedatru = tinhbyte2 - 4
    kqbyte = bytedatru.to_bytes(2, "little")  # b'\x10\x00'

    # --- Lấy 4 byte lùi 4 byte ---
    byte4 = strin[pos-4:pos]  # đây là 4 byte ngay trước "ArtSkinPrefabLOD0"
    tinhbyte4 = int.from_bytes(byte4, "little")
    bytedatru2 = tinhbyte4 - 4
    kqbyte4 = bytedatru2.to_bytes(4, "little")
    strin = strin[:pos-8] + kqbyte + strin[pos-6:pos-4] + kqbyte4 + strin[pos:]
# --- Thay ArtLobbyShowLOD0 bằng ArtSkinLobbyShowLOD0 ---
strin = strin.replace(ArtLobbyShowLOD0, ArtSkinLobbyShowLOD0)

# --- Tìm vị trí ArtSkinLobbyShowLOD0 ---
pos = strin.find(b"ArtSkinLobbyShowLOD0")
if pos != -1:
    # đổi tên
    strin = strin[:pos] + b"ArtLobbyShowLOD0" + strin[pos+len(b"ArtSkinLobbyShowLOD0"):]

    # --- Lấy 2 byte lùi 8 byte ---
    byte2 = strin[pos-8:pos-6]        # b'\x14\x00'
    tinhbyte2 = int.from_bytes(byte2, "little")  # 20
    bytedatru = tinhbyte2 - 4
    kqbyte = bytedatru.to_bytes(2, "little")  # b'\x10\x00'

    # --- Lấy 4 byte lùi 4 byte ---
    byte4 = strin[pos-4:pos]  # đây là 4 byte ngay trước "ArtSkinPrefabLOD0"
    tinhbyte4 = int.from_bytes(byte4, "little")
    bytedatru2 = tinhbyte4 - 4
    kqbyte4 = bytedatru2.to_bytes(4, "little")
    strin = strin[:pos-8] + kqbyte + strin[pos-6:pos-4] + kqbyte4 + strin[pos:]
# --- Thay ArtLobbyIdleShowLOD bằng ArtSkinLobbyIdleShowLOD ---
strin = strin.replace(ArtLobbyIdleShowLOD0, ArtSkinLobbyIdleShowLOD)

# --- Tìm vị trí ArtSkinLobbyShowLOD0 ---
pos = strin.find(b"ArtSkinLobbyIdleShowLOD")
if pos != -1:
    # đổi tên
    strin = strin[:pos] + b"ArtLobbyIdleShowLOD" + strin[pos+len(b"ArtSkinLobbyIdleShowLOD"):]

    # --- Lấy 2 byte lùi 8 byte ---
    byte2 = strin[pos-8:pos-6]        # b'\x14\x00'
    tinhbyte2 = int.from_bytes(byte2, "little")  # 20
    bytedatru = tinhbyte2 - 4
    kqbyte = bytedatru.to_bytes(2, "little")  # b'\x10\x00'

    # --- Lấy 4 byte lùi 4 byte ---
    byte4 = strin[pos-4:pos]  # đây là 4 byte ngay trước "ArtSkinPrefabLOD0"
    tinhbyte4 = int.from_bytes(byte4, "little")
    bytedatru2 = tinhbyte4 - 4
    kqbyte4 = bytedatru2.to_bytes(4, "little")
    strin = strin[:pos-8] + kqbyte + strin[pos-6:pos-4] + kqbyte4 + strin[pos:]
# --- Thay ArtSkinLobbyShowCamera bằng ArtSkinLobbyShowCamera ---
pos = strin.find(ArtSkinLobbyShowCameraMd)
if pos != -1:
    strin = strin[:pos] + strin[pos + len(ArtSkinLobbyShowCameraMd):]
    strin = strin[:pos] + ArtSkinLobbyShowCamera + strin[pos:]
if IDMODSKIN in ['54805','19015','17408','54402']:
    codexoa = 0
    
    # --- Tìm ArtPrefabLOD0 ---
    codecantim = strin.find(b"ArtPrefabLOD0")
    if codecantim == -1:
        pass
    else:
        codedaydu = strin[:codecantim]
    
        # --- useNewMecanim ---
        pos_use = codedaydu.rfind(b"useNewMecanim")
        if pos_use != -1:
            finduse = pos_use - 8
            codefulluse = strin[finduse]
            strin = strin[:finduse] + strin[finduse + codefulluse:]
            codexoa += 1
        else:
            pass
    
        codecantim = strin.find(b"ArtPrefabLOD0")
        codedaydu = strin[:codecantim]
    
        # --- oriSkinUseNewMecanim ---
        pos_ori = codedaydu.rfind(b"oriSkinUseNewMecanim")
        if pos_ori != -1:
            findori = pos_ori - 8
            codefullori = strin[findori]
            strin = strin[:findori] + strin[findori + codefullori:]
            codexoa += 1
        else:
            pass
        # --- useTimeline ---
        pos_imeline = codedaydu.rfind(b"useTimeline")
        if pos_imeline != -1:
            findimeline = pos_imeline - 8
            codefullimeline = strin[findimeline]
            strin = strin[:findimeline] + strin[findimeline + codefullimeline:]
            codexoa += 1
        else:
            print('Khong Co useTimeline')

        # --- ActorName ---
        findactorname = strin.find(b"ActorName")
        if findactorname != -1:
            bytecancheck = findactorname - 12
            bytecallator = strin[bytecancheck]
            bytemoi = bytecallator - codexoa
            strin = strin[:bytecancheck] + bytes([bytemoi]) + strin[bytecancheck+1:]
        else:
            pass
    
# Tìm vị trí từ b'SkinPrefabG'
pos = strin.find(b"SkinPrefabG")
CodeNgoaiLuong = 0

if pos != -1:
    insert = pos - 8  # lùi 8 byte trước "SkinPrefabG"

    if ArtSkinLobbyNode:
        strin = strin[:insert] + ArtSkinLobbyNode + strin[insert:]
        insert += len(ArtSkinLobbyNode)
        CodeNgoaiLuong += 1

    if ArtSkinLobbyShowMovie:
        strin = strin[:insert] + ArtSkinLobbyShowMovie + strin[insert:]
        insert += len(ArtSkinLobbyShowMovie)
        CodeNgoaiLuong += 1

    if useNewMecanim:
        strin = strin[:insert] + useNewMecanim + strin[insert:]
        insert += len(useNewMecanim)
        CodeNgoaiLuong += 1

    if bDisableDirLight:
        strin = strin[:insert] + bDisableDirLight + strin[insert:]
        insert += len(bDisableDirLight)
        CodeNgoaiLuong += 1
    if bUnityLight:
        strin = strin[:insert] + bUnityLight + strin[insert:]
        insert += len(bUnityLight)
        CodeNgoaiLuong += 1
    if PreloadAnimatorEffects:
        strin = strin[:insert] + PreloadAnimatorEffects + strin[insert:]
        insert += len(PreloadAnimatorEffects)
        CodeNgoaiLuong += 1
    if useStateDrivenMecanim:
        strin = strin[:insert] + useStateDrivenMecanim + strin[insert:]
        insert += len(useStateDrivenMecanim)
        CodeNgoaiLuong += 1
        
# Tìm vị trí ActorName
pos_actor = strin.find(b'ActorName')
if pos_actor != -1:
    offset_pos = pos_actor - 12
    ActorName = strin[offset_pos]
    ByteActorName = ActorName + CodeNgoaiLuong
    strin = strin[:offset_pos] + bytes([ByteActorName]) + strin[offset_pos+1:]

with open(path, "wb") as f:
    f.write(strin)
with open(path, "rb") as f:
    string = f.read()

fullbyte = len(string)
fullbyte_bytes = fullbyte.to_bytes(2, "little")
string = fullbyte_bytes + string[2:]

a1 = fullbyte - 84
a10 = a1.to_bytes(2, "little").hex()
vtrt = a10[2:4] + a10[0:2]

vtrp = bytes.fromhex(vtrt)
head = string[:86][:-2] + vtrp
string = head + string[86:]

with open(path, "wb") as f:
    f.write(string)

