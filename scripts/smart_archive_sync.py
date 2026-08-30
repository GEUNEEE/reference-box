import json,re,time,random,string,urllib.request
from datetime import datetime,timezone

SRC="https://raw.githubusercontent.com/GEUNEEE/smart-archive/master/data/archive.json"
REF="data/references.json"; LEDGER="data/sa_synced.json"

def parse(u):
    m=re.search(r"instagram\.com/(?:reel|reels|p|tv)/([A-Za-z0-9_-]+)",u)
    if m: return ("instagram",m.group(1),u.split("?")[0])
    m=re.search(r"(?:youtube\.com/(?:watch\?v=|shorts/|embed/)|youtu\.be/)([A-Za-z0-9_-]{11})",u)
    if m: return ("youtube",m.group(1),u)
    m=re.search(r"tiktok\.com/@[^/]+/video/(\d+)",u)
    if m: return ("tiktok",m.group(1),u.split("?")[0])
    return None

def uid():
    return format(int(time.time()*1000),"x")+"".join(random.choices(string.ascii_lowercase+string.digits,k=5))

arc=json.load(urllib.request.urlopen(SRC,timeout=30))
data=json.load(open(REF,encoding="utf-8"))
try: ledger=set(json.load(open(LEDGER,encoding="utf-8")))
except Exception: ledger=set()

known={(i.get("platform"),i.get("embedId")) for i in data["items"]}
needsL=data["tagGroups"].get("needs",[]); typesL=data["tagGroups"].get("types",[])
now=datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")
added=0
for e in arc:
    p=parse(e.get("url") or "")
    if not p: continue
    plat,eid,cu=p
    key=plat+":"+eid
    if key in ledger: continue           # 이미 반입했던 항목(앱에서 삭제해도 재반입 안 함)
    ledger.add(key)
    if (plat,eid) in known: continue     # 다른 경로로 이미 등록됨
    hay=(e.get("title") or "")+" "+(e.get("memo") or "")+" "+" ".join(e.get("tags") or [])
    memo="\n".join(x for x in [(e.get("memo") or "").strip(),
        ("SA: "+", ".join(e["tags"])) if e.get("tags") else ""] if x)
    data["items"].append({"id":uid(),"url":cu,"platform":plat,"embedId":eid,
        "title":re.sub(r"^인스타 릴스( - )?","",e.get("title") or ""),"memo":memo,
        "needs":[t for t in needsL if t in hay],"types":[t for t in typesL if t in hay],
        "status":"inbox","addedBy":"스마트아카이브",
        "addedAt":(e.get("date")+"T00:00:00.000Z") if e.get("date") else now,"updatedAt":now})
    added+=1

json.dump(sorted(ledger),open(LEDGER,"w",encoding="utf-8"),ensure_ascii=False,indent=0)
if added:
    json.dump(data,open(REF,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
print("added",added)
