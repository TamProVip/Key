import xml.etree.ElementTree as A
from xml.dom import minidom as B

OFFSET_MAP = {}

def BytesToXml(a, b, c=140):
    global OFFSET_MAP
    OFFSET_MAP = {}

    d = bytearray(open(a, "rb").read())
    e = []
    f = c
    while f < len(d):
        if d[f:f+1].isascii() and chr(d[f]).isprintable():
            g = f
            while f < len(d) and d[f:f+1].isascii() and chr(d[f]).isprintable():
                f += 1
            h = d[g:f].decode("utf-8", errors="ignore")
            if f+3 <= len(d) and d[f]==0x00:
                i = d[f+1:f+4]
                j = int.from_bytes(i, "little")
                if j !=0 and len(h)>2:
                    e.append((g,h,j))
                f +=3
            else:
                f +=1
        else:
            f +=1

    k = A.Element("Items")
    for l,(g,h,j) in enumerate(e,1):
        OFFSET_MAP[j] = g  

        m = A.SubElement(k,"Item")
        m.set("id",str(j))
        m.set("SoundTrack",h)

    n = A.tostring(k,encoding="utf-8")
    o = B.parseString(n).toprettyxml(indent="\n  ")
    with open(b,"w",encoding="utf-8") as p:
        p.write(o)


def XmlToBytes(a, b, c=None):
    global OFFSET_MAP
    d = bytearray(open(b, "rb").read())
    e = A.parse(a).getroot()
    for f in e.findall("Item"):
        j = int(f.get("id"))
        g = OFFSET_MAP.get(j)
        if g is None:
            continue
        h = f.get("SoundTrack").encode("utf-8")
        for x in range(len(h)):
            if g + x < len(d):
                d[g + x] = h[x]
        if g + len(h) < len(d):
            d[g + len(h)] = 0x00
        k = j.to_bytes(3, "little")
        l = g + len(h) + 1
        if l + 3 <= len(d):
            d[l:l + 3] = k

    if c is None:
        c = b
    with open(c, "wb") as m:
        m.write(d)
#XmlToBytes("Sound/ChatSound.xml","Sound/ChatSound.bytes")
BytesToXml("Sound/ChatSound.bytes","Sound/ChatSound.xml")