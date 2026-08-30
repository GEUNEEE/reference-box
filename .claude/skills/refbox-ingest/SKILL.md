---
name: refbox-ingest
description: 링크 덤프(카카오 나에게 보내기, 메모 등)를 파싱해 영상 레퍼런스함 data/references.json에 추가하고 커밋한다. "레퍼런스함에 넣어줘", "링크 정리해서 레퍼런스함에", "레퍼런스 인제스트" 등에서 사용.
---

# 레퍼런스함 인제스트 스킬

## 역할
링크가 섞인 텍스트 덤프를 받아 인스타/유튜브/틱톡 영상 링크를 추출하고 `data/references.json`에 추가한 뒤 git push한다.

## 동작 순서
1. `data/references.json` 로드 — 기존 `items[].embedId`(deleted 포함) 목록을 중복 제거 기준으로 사용.
2. 덤프에서 URL 추출 후 플랫폼 파싱:
   - instagram: `instagram.com/(reel|reels|p|tv)/{embedId}`
   - youtube: `watch?v= | youtu.be/ | /shorts/ | /embed/` → 11자 id
   - tiktok: `tiktok.com/@user/video/{id}`
3. 링크에 붙은 메모 문장은 해당 항목의 memo로 보존.
4. 항목 생성 (스키마 준수):
   {id, url, platform, embedId, title, memo, needs[], types[], status:"inbox", addedBy:"ingest", addedAt, updatedAt}
   - needs/types 태그는 `tagGroups`의 현재 목록과 제목·메모를 대조해 명확히 일치할 때만 부여, 애매하면 빈 배열(검수 단계에서 사람이 태깅).
   - id는 `Date.now().toString(36)+랜덤5자` 형식.
5. 전체 JSON을 다시 쓰고 커밋: `refbox ingest: N개 추가` → push.

## 주의
- 기존 items를 절대 삭제·수정하지 않는다 (추가만).
- deleted:true 항목은 삭제 기록(톰스톤)이므로 유지하고, 같은 embedId 재추가도 금지.
- tagGroups는 사용자가 관리 — 임의로 태그를 추가하지 않는다.
