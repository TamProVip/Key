# -*- coding: utf-8 -*-
import os, sys

path = "Prefab_Hero/196_Elsu/196_Elsu_trap_actorinfo.bytes"

with open(path, "rb") as f:
    data = bytearray(f.read())
idskin = input("IDSkin: ").strip()
skin_bytes = idskin.encode("utf-8")
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

with open(path, "wb") as f:
    f.write(data)

