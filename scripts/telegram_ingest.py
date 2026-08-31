import json,os,re,time,random,string,urllib.request,urllib.parse
from datetime import datetime,timezone

TOK=os.environ["TELEGRAM_BOT_TOKEN"]
API="https://api.telegram.org/bot"+TOK
REF="data/references.json"; OFF="data/tg_offset.txt"

def get(url):
    with urllib.request.urlopen(url,timeout=30) as r: return json.load(r)

def send(chat,text):
    try: get(API+"/sendMessage?chat_id="+str(chat)+"&text="+urllib.parse.quote(text))
    except Exception: pass

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

offset=0
if os.path.exists(OFF):
    try: offset=int(re.sub(r"[^0-9]","",open(OFF).read()) or 0)
    except Exception: pass

ups=get(API+"/getUpdates?offset="+str(offset+1)+"&timeout=0").get("result",[])
if not ups:
    print("no updates"); raise SystemExit(0)

data=json.load(open(REF,encoding="utf-8"))
known={(i.get("platform"),i.get("embedId")) for i in data["items"]}
now=datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")
added=0; last=offset
for up in ups:
    last=max(last,up["update_id"])
    msg=up.get("message") or up.get("channel_post") or {}
    text=(msg.get("text") or msg.get("caption") or "")
    who=(msg.get("from") or {}).get("first_name","")
    chat=(msg.get("chat") or {}).get("id")
    ctype=(msg.get("chat") or {}).get("type","")
    urls=re.findall(r"https?://\S+",text)
    memo=re.sub(r"https?://\S+","",text).strip()
    n=0; dup=0
    for u in urls:
        p=parse(u)
        if not p: continue
        plat,eid,cu=p
        if (plat,eid) in known: dup+=1; continue
        known.add((plat,eid))
        data["items"].append({"id":uid(),"url":cu,"platform":plat,"embedId":eid,
            "title":"","memo":memo,"needs":[],"types":[],"status":"inbox","rating":0,
            "addedBy":(who or "telegram"),"addedAt":now,"updatedAt":now})
        added+=1; n+=1
    if chat and urls:
        if n: send(chat,"✅ "+str(n)+"개 레퍼런스함에 추가됨"+(" (중복 "+str(dup)+"개 제외)" if dup else ""))
        elif dup: send(chat,"이미 등록된 영상이에요 ("+str(dup)+"개)")
        else: send(chat,"지원하지 않는 링크예요 (인스타·유튜브·틱톡만 가능)")
    elif chat and ctype=="private" and text:
        send(chat,"👋 인스타·유튜브·틱톡 링크를 보내면 레퍼런스함에 자동 등록돼요.\n링크와 함께 쓴 글은 메모로 저장됩니다. (반영까지 몇 분 걸릴 수 있어요)")

open(OFF,"w").write(str(last))
if added:
    json.dump(data,open(REF,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
print("added",added,"last_offset",last)
