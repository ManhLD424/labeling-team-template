#!/usr/bin/env python3
"""
AI Browser Co-pilot cho CVAT tren Windows (Phuong an 2).
Ket noi truc tiep vao phien trinh duyet Chrome/Edge dang mo qua Chrome DevTools Protocol (CDP port 9222).
Cho phep AI Agent va Nguoi dung cung thao tac tren giao dien CVAT ma khong can dang nhap lai.
"""

from __future__ import annotations

import argparse
import asyncio
import os
import sys
import time
from pathlib import Path
from typing import Any

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

from playwright.async_api import async_playwright


class CVATBrowserCopilot:
    def __init__(self, cdp_url: str = "http://localhost:9222"):
        self.cdp_url = cdp_url
        self.browser = None
        self.context = None
        self.page = None

    async def connect(self) -> bool:
        """Ket noi vao trinh duyet Chrome dang chay o cong 9222."""
        self.playwright = await async_playwright().start()
        try:
            self.browser = await self.playwright.chromium.connect_over_cdp(self.cdp_url)
            contexts = self.browser.contexts
            if not contexts:
                print("Khong tim thay browser context nao. Hay dam bao Chrome dang mo.")
                return False

            self.context = contexts[0]
            pages = self.context.pages

            # Tim tab CVAT
            for p in pages:
                url = p.url
                if "cvat.note.transformerlabs.ai" in url or "cvat" in url:
                    self.page = p
                    break

            if not self.page and pages:
                self.page = pages[0]

            if not self.page:
                print("Khong tim thay tab CVAT dang mo trong Chrome.")
                return False

            print(f"Ket noi thanh cong den tab: {self.page.url}")
            return True
        except Exception as e:
            print(f"Loi ket noi den {self.cdp_url}: {e}")
            print("Goi y: Hay chay start_chrome_debug.bat truoc de mo Chrome o cong 9222.")
            return False

    async def get_state(self) -> dict[str, Any]:
        """Doc trang thai hien tai tren man hinh CVAT."""
        if not self.page:
            return {}

        title = await self.page.title()
        url = self.page.url

        # Doc frame hien tai tu o input frame tren thanh cong cu
        frame_number = None
        try:
            frame_input = await self.page.query_selector("input.cvat-player-frame-selector")
            if frame_input:
                frame_number = await frame_input.input_value()
        except Exception:
            pass

        return {
            "title": title,
            "url": url,
            "frame": frame_number,
        }

    async def next_frame(self) -> None:
        """Nhay sang frame ke tiep (phim tat F hoac nut Next tren CVAT)."""
        if self.page:
            await self.page.keyboard.press("f")
            print("Da chuyen sang frame tiep theo.")

    async def prev_frame(self) -> None:
        """Quay lai frame truoc (phim tat D tren CVAT)."""
        if self.page:
            await self.page.keyboard.press("d")
            print("Da quay lai frame truoc.")

    async def save(self) -> None:
        """Luu annotations tren CVAT (Ctrl + S)."""
        if self.page:
            await self.page.keyboard.press("Control+s")
            print("Da kich hoat lenh Luu (Ctrl+S).")

    async def take_screenshot(self, output_path: str = "current_screen.jpg") -> str:
        """Chup man hinh CVAT de AI kiem tra truc quan."""
        if self.page:
            await self.page.screenshot(path=output_path, full_page=False)
            print(f"Da luu anh chup man hinh vao {output_path}")
            return output_path
        return ""

    async def close(self) -> None:
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()


async def main_async():
    parser = argparse.ArgumentParser(description="CVAT Browser Co-pilot (Windows)")
    parser.add_argument("--action", default="status", choices=["status", "next", "prev", "save", "screenshot"], help="Hanh dong can thuc hien")
    parser.add_argument("--cdp", default="http://localhost:9222", help="CDP URL")
    args = parser.parse_args()

    copilot = CVATBrowserCopilot(args.cdp)
    connected = await copilot.connect()
    if not connected:
        return 1

    if args.action == "status":
        state = await copilot.get_state()
        print("\n--- THONG TIN TRINH DUYET CVAT ---")
        print(f"URL: {state.get('url')}")
        print(f"Tieu de trang: {state.get('title')}")
        print(f"Frame hien tai: {state.get('frame')}")
    elif args.action == "next":
        await copilot.next_frame()
    elif args.action == "prev":
        await copilot.prev_frame()
    elif args.action == "save":
        await copilot.save()
    elif args.action == "screenshot":
        await copilot.take_screenshot("current_screen.jpg")

    await copilot.close()
    return 0


def main():
    return asyncio.run(main_async())


if __name__ == "__main__":
    sys.exit(main())
