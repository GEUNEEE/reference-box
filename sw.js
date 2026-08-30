// 최소 서비스워커: PWA 설치(홈 화면 추가·공유 타깃) 요건 충족용
self.addEventListener("install", e => self.skipWaiting());
self.addEventListener("activate", e => self.clients.claim());
self.addEventListener("fetch", e => {}); // 네트워크 그대로 통과
