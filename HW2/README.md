# HW2 — Todo 앱에 완료 체크 기능 추가

- 이름: 이승민
- 학번: 24013735

## 폴더 설명

- `app.py` — 목록/추가(`/`), 삭제(`/delete/<int:index>`), 완료 토글(`/toggle/<int:index>`)
- `templates/` — `base.html`(공통 틀), `index.html`(목록과 입력창)
- `static/style.css` — 화면 꾸밈과 완료 항목 취소선

## 실행 방법

```
cd HW2
flask --debug run
```

## 실행 화면

<!-- TODO: 아래 세 자리에 캡처를 넣으세요 (GitHub 웹 편집 화면에서 끌어다 놓기) -->

1. 할 일 두 개가 있는 목록 —
2. 하나를 [완료] 눌러 줄이 그어진 화면 —
3. 새로고침한 뒤에도 줄이 남아 있는 화면 —
