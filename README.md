# 🔍 Drag to Search (드래그 투 서치) - 최종 제출 패키지

삼성 갤럭시의 '서클 투 서치' 경험을 데스크탑으로 가져온 초간단 번역 유틸리티입니다. 어떤 화면에서든 원하는 영역을 드래그하여 **네이버 파파고** 또는 **구글 번역**으로 즉시 연결합니다.

## ✨ 주요 특징
- **API 키 필요 없음:** 유료 결제나 복잡한 설정 없이 설치 즉시 모든 기능을 무료로 사용 가능합니다.
- **다중 서비스 지원:** 드래그 후 원하는 번역 서비스(파파고/구글)를 선택할 수 있습니다.
- **크로스 플랫폼:** 윈도우와 리눅스(Ubuntu) 환경을 완벽하게 지원합니다.
- **스마트 대시보드:** 화면 짤림 없는 전체 화면 UI로 쾌적한 조작이 가능합니다.

## 🛠 설치 및 실행 방법

### 1. 시스템 의존성 설치 (필수)
텍스트 인식을 위해 시스템에 OCR 엔진이 설치되어 있어야 합니다.

- **리눅스 (Ubuntu):**
  ```bash
  sudo apt update && sudo apt install -y tesseract-ocr tesseract-ocr-kor tesseract-ocr-eng
  ```
- **윈도우:**
  [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki) 설치 후 `C:\Program Files\Tesseract-OCR` 경로에 설치하세요. (환경 변수 PATH에 추가 권장)

### 2. 파이썬 라이브러리 설치
```bash
pip install -r requirements.txt
```

### 3. 프로그램 실행
```bash
python src/main.py
```

## 📦 Windows 실행 파일(.exe) 직접 빌드하기
현재 패키지에 포함된 `build_exe.bat` 파일을 사용하거나 다음 명령어를 실행하세요.

```bash
# PyInstaller 설치
pip install pyinstaller

# 빌드 실행
pyinstaller --noconsole --onefile --name "DragToSearch" src/main.py
```
빌드 완료 후 `dist/` 폴더 내의 `DragToSearch.exe`를 실행하면 설치 과정 없이 즉시 유틸리티를 사용할 수 있습니다.

## ⌨️ 사용 방법
1.  **`Ctrl + Alt + S`** 를 누르거나 우측 상단 패널의 **[드래그]** 버튼을 누릅니다.
2.  화면에서 번역하고 싶은 영역을 마우스로 드래그합니다.
3.  중앙에 나타나는 **[네이버 파파고]** 또는 **[구글 번역]** 버튼을 클릭합니다.
4.  기본 브라우저에서 번역이 완료된 결과 페이지가 즉시 열립니다.

---
**Developed with ❤️ using Gemini CLI (Vibe Coding Style)**
