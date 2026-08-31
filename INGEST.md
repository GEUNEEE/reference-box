# 레퍼런스함 등록 절차 (cokacdir 봇용)

메시지에 인스타그램/유튜브/틱톡 링크가 포함되면 아래 절차로 `data/references.json`에 등록한다.

## 절차
1. `cd C:\Users\user\reference-box` 후 `git pull` (항상 최신화 먼저)
2. 메시지에서 URL 추출, 플랫폼 파싱:
   - instagram: `instagram.com/(reel|reels|p|tv)/{embedId}` → url은 `https://www.instagram.com/reel/{embedId}/` (p면 /p/)로 정규화
   - youtube: `watch?v= | youtu.be/ | /shorts/ | /embed/` → 11자 embedId
   - tiktok: `tiktok.com/@계정/video/{숫자}` → 숫자가 embedId
3. 중복 확인: 기존 `items[]`에 같은 platform+embedId가 있으면(삭제 표시 `deleted:true` 포함) 건너뜀
4. 새 항목 추가 (스키마 엄수):
```json
{"id":"<ms를 16진수로>+<영숫자5자>","url":"","platform":"instagram|youtube|tiktok","embedId":"",
 "title":"","memo":"<링크 외 함께 온 텍스트>","needs":[],"types":[],"status":"inbox","rating":0,
 "addedBy":"<보낸 사람 이름>","addedAt":"<UTC ISO>","updatedAt":"<UTC ISO>"}
```
   - needs/types 태그는 메시지 내용이 tagGroups 목록의 태그와 명확히 일치할 때만 부여, 애매하면 빈 배열
   - 기존 항목·계정·로그·태그그룹은 절대 수정/삭제하지 않는다 (추가만)
5. `git add data/references.json && git commit -m "refbox: cokacdir ingest" && git push`
   - push 거부되면 `git pull --rebase` 후 다시 push
6. 답장은 짧게: `✅ N개 레퍼런스함에 추가됨` (중복이면 `이미 등록된 영상이에요`)

## 링크가 없는 메시지
한두 문장으로만 짧게 답한다. 파일이나 저장소는 건드리지 않는다.
