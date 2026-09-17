# browser-copilot

Giai phap Co-pilot tu dong hoa trinh duyet danh cho Windows (Phuong an 2).

Giai quyet nhu cau AI truc tiep thao tac va dong hanh cung Annotator tren giao dien web CVAT ma khong can dang nhap lai, hoat dong tuong tu co che cua ego-lite tren macOS.

## Nguyen ly hoat dong

1. Khoi chay Google Chrome hoac Microsoft Edge tren Windows voi co Remote Debugging:
   `--remote-debugging-port=9222`
2. Nguoi dung mo tab CVAT Job can lam viec (phien dang nhap, cookies va toan bo cai dat hien thi duoc giu nguyen 100%).
3. Script `copilot.py` su dung thu vien Playwright ket noi qua Chrome DevTools Protocol (CDP) vao cong 9222.
4. AI Agent va Nguoi dung co the cung thao tac tren man hinh: AI co the doc frame hien tai, chuyen frame, bam luu (Ctrl+S), chup anh man hinh phuc vu review, hoac ho tro tu dong hoa cac tac vu lap lai.

## Cach su dung khi can kich hoat

### Buoc 1: Khoi dong Chrome o che do ket noi
Nhay dup vao file `start_chrome_debug.bat` hoac chay trong terminal:
```cmd
start_chrome_debug.bat
```

Trinh duyet se mo ra trang CVAT. Dang nhap va mo Job 1663.

### Buoc 2: Chay Co-pilot
Trong terminal, chay cac lenh tuong tac:
```bash
# Kiem tra trang thai tab CVAT hien tai (Frame nao dang mo)
python source-tool/browser-copilot/copilot.py --action status

# Chup anh man hinh tab CVAT de AI danh gia truc tiep
python source-tool/browser-copilot/copilot.py --action screenshot

# Chuyen sang frame tiep theo
python source-tool/browser-copilot/copilot.py --action next

# Luu bai tren CVAT (Ctrl + S)
python source-tool/browser-copilot/copilot.py --action save
```
