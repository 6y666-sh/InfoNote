# tray.py

import threading
import webbrowser
import subprocess
import sys
import os
from PIL import Image, ImageDraw
import pystray

# Flask 서버 프로세스
server_process = None

def create_icon_image():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    icon_path = os.path.join(script_dir, "choco.ico")
    print(f"아이콘 경로: {icon_path}")  # 임시 확인용
    img = Image.open(icon_path)
    img = img.resize((64, 64))
    return img



def start_server():
    """Flask 서버 실행"""
    global server_process
    script_dir = os.path.dirname(os.path.abspath(__file__))
    server_process = subprocess.Popen(
        [sys.executable, "app.py"],
        cwd=script_dir,
        creationflags=subprocess.CREATE_NO_WINDOW  # 터미널 창 숨김
    )

def open_browser(icon, item):
    """브라우저 열기"""
    webbrowser.open("http://127.0.0.1:5000" )

def quit_app(icon, item):
    """앱 종료"""
    global server_process
    if server_process:
        server_process.terminate()
    icon.stop()

def main():
    # 서버 백그라운드 실행
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()

    # 브라우저 자동 열기 (서버 준비 대기 1.5초)
    import time
    time.sleep(1.5)
    webbrowser.open("http://127.0.0.1:5000" )

    # 트레이 아이콘 메뉴
    menu = pystray.Menu(
        pystray.MenuItem("브라우저 열기", open_browser),
        pystray.MenuItem("종료", quit_app)
    )

    icon = pystray.Icon(
        name="InfoNote",
        icon=create_icon_image(),
        title="InfoNote 실행 중",
        menu=menu
    )

    icon.run()

if __name__ == "__main__":
    main()
