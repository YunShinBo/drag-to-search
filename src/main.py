import sys
import os
import threading
import webbrowser
import urllib.parse
import warnings
from typing import Optional

# 불필요한 경고 숨기기
warnings.filterwarnings("ignore")

from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QPushButton, QFrame, QGridLayout)
from PyQt6.QtCore import Qt, QRect, QPoint, pyqtSignal, QObject
from PyQt6.QtGui import QPainter, QColor, QPen
import mss
from pynput import keyboard
from PIL import Image

# OCR (로컬 글자 인식 도구)
try:
    import pytesseract
    if os.name == 'nt':
        tess_path = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        if os.path.exists(tess_path):
            pytesseract.pytesseract.tesseract_cmd = tess_path
except ImportError:
    pytesseract = None

class SignalHandler(QObject):
    trigger_capture = pyqtSignal()

class FullScreenSelector(QWidget):
    """드래그 후 나타나는 대형 대시보드 (파파고/구글 번역 선택)"""
    def __init__(self, img_pil, signals: SignalHandler):
        super().__init__()
        self.img_pil, self.signals = img_pil, signals
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Tool)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        geo = QApplication.primaryScreen().geometry()
        self.setGeometry(geo)
        
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        card = QFrame()
        card.setFixedSize(700, 450)
        card.setStyleSheet("background-color: rgba(20, 20, 20, 0.98); border-radius: 40px; border: 4px solid #00C853;")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(40, 40, 40, 40)
        
        title = QLabel("번역 서비스를 선택하세요")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: white; font-size: 32px; font-weight: bold; border: none; margin-bottom: 30px;")
        card_layout.addWidget(title)
        
        grid = QHBoxLayout()
        grid.setSpacing(30)
        
        # 버튼: 파파고, 구글번역
        self.btn_papago = self.create_large_btn("🦜\n네이버 파파고", "#00C853", self.on_papago)
        self.btn_google = self.create_large_btn("🔤\n구글 번역", "#4285F4", self.on_google_trans)
        
        grid.addWidget(self.btn_papago)
        grid.addWidget(self.btn_google)
        card_layout.addLayout(grid)
        
        info = QLabel("ESC를 누르거나 빈 곳을 클릭하면 취소됩니다")
        info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info.setStyleSheet("color: #777; font-size: 14px; border: none; margin-top: 30px;")
        card_layout.addWidget(info)
        
        layout.addWidget(card)

    def create_large_btn(self, text, color, callback):
        btn = QPushButton(text)
        btn.setFixedSize(280, 200)
        btn.clicked.connect(callback)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: #2D2D2D;
                color: white;
                border-radius: 30px;
                font-size: 24px;
                font-weight: bold;
                border: 2px solid #444;
            }}
            QPushButton:hover {{
                background-color: {color};
                border: 4px solid white;
            }}
        """)
        return btn

    def get_extracted_text(self):
        if not pytesseract: return ""
        try:
            return pytesseract.image_to_string(self.img_pil, lang='kor+eng').strip()
        except: return ""

    def on_papago(self):
        text = self.get_extracted_text()
        url = f"https://papago.naver.com/?sk=auto&tk=ko&st={urllib.parse.quote(text)}" if text else "https://papago.naver.com/"
        webbrowser.open(url)
        self.close()

    def on_google_trans(self):
        text = self.get_extracted_text()
        url = f"https://translate.google.com/?sl=auto&tl=ko&text={urllib.parse.quote(text)}&op=translate" if text else "https://translate.google.com/"
        webbrowser.open(url)
        self.close()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape: self.close()
    def mousePressEvent(self, event): self.close()

class MainPanel(QWidget):
    def __init__(self, signals: SignalHandler):
        super().__init__()
        self.signals = signals
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Tool)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        layout = QHBoxLayout(self)
        container = QFrame()
        container.setStyleSheet("background-color: #1A1A1A; border-radius: 20px; border: 2px solid #00C853;")
        c_layout = QHBoxLayout(container)
        
        label = QLabel("🔍 Drag to Search")
        label.setStyleSheet("color: white; font-weight: bold; margin: 0 15px;")
        c_layout.addWidget(label)
        
        btn_start = QPushButton("드래그")
        btn_start.clicked.connect(self.signals.trigger_capture.emit)
        btn_start.setStyleSheet("background-color: #00C853; color: white; border-radius: 12px; padding: 8px 15px; font-weight: bold;")
        c_layout.addWidget(btn_start)
        
        btn_quit = QPushButton("종료")
        btn_quit.clicked.connect(QApplication.instance().quit)
        btn_quit.setStyleSheet("background-color: #D32F2F; color: white; border-radius: 12px; padding: 8px 15px; font-weight: bold;")
        c_layout.addWidget(btn_quit)
        
        layout.addWidget(container)
        self.adjustSize()
        geo = QApplication.primaryScreen().geometry()
        self.move(geo.width() - self.width() - 50, 50)

class OverlayWindow(QWidget):
    def __init__(self, signals: SignalHandler):
        super().__init__()
        self.signals = signals
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Tool | Qt.WindowType.X11BypassWindowManagerHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setCursor(Qt.CursorShape.CrossCursor)
        self.begin, self.end, self.is_dragging = QPoint(), QPoint(), False

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(0, 0, 0, 150))
        if self.is_dragging:
            rect = QRect(self.begin, self.end).normalized()
            painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_Clear)
            painter.fillRect(rect, Qt.GlobalColor.transparent)
            painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceOver)
            painter.setPen(QPen(QColor(0, 200, 83), 5)); painter.drawRect(rect)

    def mousePressEvent(self, event): self.begin = event.pos(); self.end = self.begin; self.is_dragging = True; self.update()
    def mouseMoveEvent(self, event): self.end = event.pos(); self.update()
    def mouseReleaseEvent(self, event):
        self.is_dragging = False
        rect_log = QRect(self.begin, self.end).normalized()
        self.hide()
        if rect_log.width() > 10:
            dpr = self.devicePixelRatio()
            rect_phys = QRect(int(rect_log.x() * dpr), int(rect_log.y() * dpr), int(rect_log.width() * dpr), int(rect_log.height() * dpr))
            with mss.mss() as sct:
                img = sct.grab({"top": rect_phys.top(), "left": rect_phys.left(), "width": rect_phys.width(), "height": rect_phys.height()})
                self.selector = FullScreenSelector(Image.frombytes("RGB", img.size, img.bgra, "raw", "BGRX"), self.signals)
                self.selector.show()

class DragToSearchApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.app.setQuitOnLastWindowClosed(False)
        self.signals = SignalHandler()
        self.overlay = OverlayWindow(self.signals)
        self.panel = MainPanel(self.signals)
        self.signals.trigger_capture.connect(self.show_overlay)
        threading.Thread(target=self.start_hotkey_listener, daemon=True).start()
        self.panel.show()
        print("🚀 [Drag to Search] 최종 안정화 버전 실행 중 (파파고/구글)")

    def show_overlay(self):
        total_rect = QRect()
        for screen in QApplication.screens(): total_rect = total_rect.united(screen.geometry())
        self.overlay.setGeometry(total_rect)
        self.overlay.show(); self.overlay.raise_(); self.overlay.activateWindow()

    def start_hotkey_listener(self):
        with keyboard.GlobalHotKeys({'<ctrl>+<alt>+s': self.signals.trigger_capture.emit}) as h: h.join()

    def run(self): sys.exit(self.app.exec())

if __name__ == "__main__":
    DragToSearchApp().run()
