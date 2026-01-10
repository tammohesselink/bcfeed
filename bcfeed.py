"""
Simple GUI wrapper to run the Bandcamp release dashboard generator with
date pickers and a built-in embed proxy.
"""

from __future__ import annotations

import argparse
import threading
import webbrowser
import sys
import json
import shutil
from pathlib import Path
from tkinter import Tk, Button, Frame, messagebox, filedialog, ttk
from tkinter.scrolledtext import ScrolledText

from server import app as proxy_app, start_server
from paths import get_data_dir, GMAIL_CREDENTIALS_FILE, GMAIL_TOKEN_FILE

MULTITHREADING = True
PROXY_PORT = 5050
DATA_DIR = get_data_dir()
SETTINGS_PATH = DATA_DIR / "gui_settings.json"
CREDENTIALS_PATH = DATA_DIR / GMAIL_CREDENTIALS_FILE
TOKEN_PATH = DATA_DIR / GMAIL_TOKEN_FILE


def find_free_port(preferred: int = 5050) -> int:
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(("", preferred))
            return preferred
        except OSError:
            s.bind(("", 0))
            return s.getsockname()[1]
OUTPUT_DIR = Path("output")

def start_proxy_thread():
    port = find_free_port(PROXY_PORT)
    server, thread = start_server(port)
    return server, thread, port

def launch_from_cache(proxy_port: int, *, log=print, launch_browser: bool = True, clear_status_on_load: bool = False):
    """
    Start the proxy and open the static dashboard, which will load releases from the proxy.
    """
    if launch_browser:
        webbrowser.open_new_tab(f"http://localhost:{proxy_port}/dashboard")
    return None


def main():
    root = Tk()
    root.title("bcfeed")
    root.resizable(False, False)
    style = ttk.Style(root)
    style.configure("Run.TButton", padding=(8, 4))
    style.configure("Action.TButton", padding=(8, 4))

    def adjust_date(var: StringVar, is_start: bool, delta: datetime.timedelta):
        if not can_adjust(is_start, delta):
            return
        current = parse_date_var(var, today if is_start else two_months_ago)
        new_date = current + delta
        # clamp to today
        if new_date > today:
            new_date = today
        var.set(new_date.strftime("%Y-%m-%d"))

    proxy_thread = None
    proxy_server = None
    proxy_port = PROXY_PORT

    # Toggle defaults and actions

    # Run / Clear credentials buttons
    actions_frame = Frame(root)
    actions_frame.grid(row=0, column=0, padx=8, pady=(8, 4), sticky="w")

    launch_btn = ttk.Button(actions_frame, text="Launch", width=14, style="Action.TButton", command=lambda: on_launch())
    launch_btn.grid(row=0, column=0, padx=(0, 6), sticky="w")

    # Status box
    status_box = ScrolledText(root, width=80, height=12, state="disabled")
    status_box.grid(row=1, column=0, padx=8, pady=8, sticky="nsew")

    class GuiLogger:
        def __init__(self, callback):
            self.callback = callback

        def write(self, msg):
            if msg.strip():
                self.callback(msg.rstrip())

        def flush(self):
            pass

    def append_log(msg):
        if isinstance(msg, bytes):
            try:
                msg = msg.decode("utf-8", errors="replace")
            except Exception:
                msg = str(msg)
        else:
            msg = str(msg)
        status_box.configure(state="normal")
        status_box.insert("end", msg + "\n")
        status_box.see("end")
        status_box.configure(state="disabled")

    def log(msg: str):
        # marshal to UI thread
        root.after(0, append_log, msg)

    def _ensure_proxy():
        nonlocal proxy_thread, proxy_port
        if proxy_thread is None or not proxy_thread.is_alive():
            proxy_server, proxy_thread, proxy_port = start_proxy_thread()
        return proxy_port

    def on_launch():
        nonlocal proxy_thread, proxy_port
        _ensure_proxy()

        def worker():
            try:
                original_stdout = sys.stdout
                logger = GuiLogger(log)
                sys.stdout = logger

                log(f"~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                log(f"Launching dashboard from cache...")
                log(f"~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                log(f"")
                log(f"Building page from cached releases (proxy port {proxy_port})...")

                try:
                    launch_from_cache(proxy_port, log=log, launch_browser=True, clear_status_on_load=True)
                    log("Dashboard generated from cache and opened in browser.")
                    log("")
                finally:
                    sys.stdout = original_stdout
            except Exception as exc:
                log(f"Error: {exc}")
                root.after(0, lambda exc=exc: messagebox.showerror("Error", str(exc)))

        if MULTITHREADING:
            threading.Thread(target=worker, daemon=True).start()
        else:
            worker()
            
    from tkinter import Checkbutton  # localized import to avoid polluting top
    def on_close():
        nonlocal proxy_server, proxy_thread
        try:
            if proxy_server:
                proxy_server.shutdown()
            if proxy_thread and proxy_thread.is_alive():
                proxy_thread.join(timeout=1)
        finally:
            root.destroy()

    # Auto-launch on start
    root.after(100, on_launch)
    root.protocol("WM_DELETE_WINDOW", on_close)
    root.mainloop()


if __name__ == "__main__":
    main()
