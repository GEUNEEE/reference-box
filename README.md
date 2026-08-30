# 📼 영상 레퍼런스함

영상 레퍼런스 수집 → 분류·검수 → 선정 공용 아카이브.
사이트: https://geuneee.github.io/reference-box/

- 태그 2축: 욕구 / 타입 (앱에서 추가·삭제 가능)
- 상태: 📥수집됨 → ✅검수완료 → ⭐선정 / 🗑제외
- 인스타·유튜브·틱톡 카드 안 인라인 재생 + 자동 미리보기
- 데이터: `data/references.json` (앱이 GitHub API로 자동 커밋)
- 스마트 아카이브 가져오기: 앱 ⚙️설정에서 버튼 한 번

## 인스타에서 넣는 4가지 방법
1. 공유 → 링크 복사 → 앱 ＋버튼 (클립보드 자동 감지)
2. 안드로이드: 사이트를 홈 화면에 설치하면 인스타 공유시트에 "레퍼런스함" 등록 (PWA)
3. 아이폰: 단축어로 `사이트주소?add=링크` 열기
4. 텔레그램 봇 (공통·추천): 인스타 공유 → Telegram → 봇 채팅 → 자동 등록

## 텔레그램 봇 설정 (1회, 3분)
1. 텔레그램에서 `@BotFather` → `/newbot` → 이름 정하면 **토큰** 발급
2. 이 저장소 Settings → Secrets and variables → **Actions** → New repository secret
   - Name: `TELEGRAM_BOT_TOKEN`, Value: 발급받은 토큰
3. 봇과 1:1 채팅 시작(`/start`) → 인스타 링크를 공유하면 10분 주기로 자동 등록 + ✅ 답장
   - 팀원도 같은 봇에게 보내면 등록됨 (보낸 사람 이름이 등록자로 표시)
   - 즉시 실행: Actions 탭 → telegram-ingest → Run workflow
   - 주의: 저장소에 60일간 커밋이 없으면 GitHub이 예약 실행을 잠시 끄므로, Actions 탭에서 다시 켜면 됨

## 등록·검수 권한 (웹앱)
GitHub fine-grained PAT(이 저장소 Contents R/W)을 앱 ⚙️설정에 입력. 보기만 할 팀원은 주소만 공유받으면 됨.
