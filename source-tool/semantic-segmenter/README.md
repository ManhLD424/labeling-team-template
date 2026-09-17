# semantic-segmenter

**Giai quyet:** [P-005](../../problem-backlog.md#p-005) - Tu dong phan doan ngu nghia (Semantic Segmentation) 19 class chuan Cityscapes bang format Mask/Brush RLE ban dia cua CVAT, khong bi rang cua va dong nhat tren toan bo 25 frame Job 1663.

## Pain point

- **Ton thoi gian va phan manh khi dung Da giac (Polygon)**: Viec dung da giac de phan doan cat nho mat duong, toa nha, cay coi thanh hang tram manh vuon vai tren CVAT lam danh sach Objects bi qua tai, de tao khe ho trang giua cac lop (vi pham Rule 01 & Rule 02).
- **Mo va rang cua khi resize mask thap**: Neu resize mat na argmax thap (160x320) bang nearest-neighbor se tao ra bac thang 8px rat xau.
- **Kinh lai mo/loa sang lam mat xe**: Mo hinh thi giac thong thuong de bi nham than xe thanh mat duong o nhung vung kinh lai bi ban hoac choi sang.

## Tool lam gi

`semantic-segmenter` tich hop pipeline lai cao cap (SOTA Panoptic Fusion Pipeline) giua **SegFormer-B2 Cityscapes 1024x1024** (27.5M parameters) va **YOLO11x-seg Flagship** (56M parameters, retina instance masks):
1. Tai anh tung frame tu Job duoc chi dinh thong qua CVAT REST API.
2. SegFormer-B2 sinh 19-class Logits o do phan giai cao (1024x1024) bang phuong phap Bilinear Interpolation, quan ly toan bo cac vung nen lon (road, sidewalk, building, vegetation, sky, wall, fence, terrain).
3. YOLO11x-seg phan doan the hien (Instance Segmentation) truc tiep voi do phan giai retina cho toan bo cac doi tuong vat the (car, truck, bus, pedestrian, rider, bicycle, motorcycle, traffic light, traffic sign).
4. Khac phuc triet de loi tran mask xuong mat duong va loi mat duong de len than xe: moi vat the co duong vien om sat hinh dang thuc te, tach biet hoan toan khoi mat duong va cac xe xung quanh.
5. Xuat dinh dang **Bitmask / RLE Mask ban dia cua CVAT** (`type: "mask"`):
   - Vung nen (`road`, `sidewalk`, `building`, `vegetation`, `sky`, `wall`, `fence`, `terrain`): moi lop tao 1 Mask thong nhat lien khoi (Z-order = 0).
   - Vat the (`car`, `truck`, `bus`, `pedestrian`, `rider`, `bicycle`, `motorcycle`, `pole`, `traffic light`, `traffic sign`): moi ca the la mot Mask rieng biet (Z-order = 1).
6. Tu dong xuat bo anh overlay mau chuan ra thu muc `vis_clean_masks_1663/` phuc vu nghiem thu.

## Cai dat va chay

### Cai dat thu vien
```bash
pip install onnxruntime opencv-python numpy requests Pillow
```

### Chay phan doan tu dong
```bash
# 1. Chay phan doan va upload len CVAT Job 1663 (kem xuat anh visual overlay)
python source-tool/semantic-segmenter/semantic_segment.py --job-id 1663

# 2. Chay thu nghiem xem thong ke & anh truc quan khong upload (Dry-run)
python source-tool/semantic-segmenter/semantic_segment.py --job-id 1663 --dry-run

# 3. Chay khong luu anh visual de tang toc do toi da
python source-tool/semantic-segmenter/semantic_segment.py --job-id 1663 --no-vis
```

## Dau vao / Dau ra

- **Dau vao**:
  - CVAT Server URL va Personal Access Token (PAT) trong file `d:\Project\VinPrj\CVAT.txt`.
  - Model weights: `segformer_b0_cityscapes.onnx` va `yolo11m_bdd100k.onnx`.
  - ID cua Job tren CVAT (mac dinh 1663).
- **Dau ra**:
  - Toan bo Mask sach duoc day truc tiep len CVAT Job 1663 (type: mask).
  - Thu muc anh truc quan `vis_clean_masks_1663/` chua 25 frame phu mau chuan Cityscapes 19 class.
  - Bao cao thong ke so luong mask va ty le phan bo dien tich pixel tren terminal.
