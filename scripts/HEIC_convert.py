import os
import sys
import time
from pathlib import Path
from typing import Iterable, Tuple, Optional

# ====== 基本設定（可直接修改這裡；也可用命令列參數覆蓋）======
INPUT_DIR   = r"D:\work\2025_ITRI_Intern\實習心得\ITRI-20250819T234145Z-1-001\ITRI"       # 來源 HEIC 資料夾
OUTPUT_DIR  = r"D:\work\2025_ITRI_Intern\實習心得\ITRI-20250819T234145Z-1-001\ITRI_convert"     # 轉檔輸出資料夾
OUTPUT_FMT  = "jpg"                      # "jpg" 或 "png"
KEEP_TREE   = True                       # True: 保留子資料夾結構；False: 全部平放到輸出根目錄
JPEG_QUALITY = 95                        # JPG 品質 (1~100)
MAX_WORKERS  = None                      # 保留參數，現在預設單執行緒；如需加速可改為多執行緒/處理序
# ===========================================================

# 避免在未裝 pillow_heif 時就 ImportError；延後註冊
def _register_heif():
    try:
        import pillow_heif
        pillow_heif.register_heif_opener()
    except Exception as e:
        print("[錯誤] 請先安裝 pillow-heif： pip install pillow-heif")
        raise

def _iter_heic_files(root: Path) -> Iterable[Path]:
    exts = {".heic", ".heif"}
    for p in root.rglob("*"):
        if p.is_file() and p.suffix.lower() in exts:
            yield p

def _ensure_unique_path(dst: Path) -> Path:
    if not dst.exists():
        return dst
    stem, suf = dst.stem, dst.suffix
    i = 1
    while True:
        cand = dst.with_name(f"{stem}_{i}{suf}")
        if not cand.exists():
            return cand
        i += 1

def _compute_out_path(src: Path, in_root: Path, out_root: Path, keep_tree: bool, out_ext: str) -> Path:
    if keep_tree:
        rel = src.relative_to(in_root).with_suffix(out_ext)
        return out_root / rel
    else:
        return out_root / (src.stem + out_ext)

def _save_image(img, dst: Path, fmt: str, exif: Optional[bytes], icc: Optional[bytes], jpg_quality: int):
    from PIL import Image
    dst.parent.mkdir(parents=True, exist_ok=True)
    save_kwargs = {}
    if icc:
        save_kwargs["icc_profile"] = icc

    if fmt == "jpg":
        # JPEG 參數：高品質、保留 EXIF
        save_kwargs.update(dict(quality=jpg_quality, optimize=True, progressive=True, subsampling="4:4:4"))
        if exif:
            save_kwargs["exif"] = exif
        img = img.convert("RGB")  # JPEG 不支援透明
        img.save(dst, "JPEG", **save_kwargs)
    elif fmt == "png":
        # PNG 無損壓縮
        save_kwargs.update(dict(compress_level=6))
        img.save(dst, "PNG", **save_kwargs)
    else:
        raise ValueError(f"不支援的輸出格式：{fmt}")

def convert_one(src: Path, in_root: Path, out_root: Path, keep_tree: bool, out_fmt: str, jpg_quality: int) -> Tuple[bool, str]:
    """
    回傳 (success, message)
    """
    try:
        from PIL import Image, ImageOps  # Pillow
        # 讀檔（pillow-heif 已註冊）
        img = Image.open(src)

        # 自動套用 EXIF 方向（避免橫豎顛倒）
        img = ImageOps.exif_transpose(img)

        exif = img.info.get("exif", None)
        icc  = img.info.get("icc_profile", None)

        dst = _compute_out_path(src, in_root, out_root, keep_tree, "." + out_fmt)
        dst = _ensure_unique_path(dst)
        _save_image(img, dst, out_fmt, exif, icc, jpg_quality)

        return True, f"OK -> {dst}"
    except Exception as e:
        return False, f"失敗: {src} ({e})"

def main():
    # 參數解析（可用命令列覆蓋設定）
    # 用法：
    #   python heic_folder_convert.py
    #   python heic_folder_convert.py <input_dir> <output_dir> [jpg|png] [keep|flat] [quality]
    global INPUT_DIR, OUTPUT_DIR, OUTPUT_FMT, KEEP_TREE, JPEG_QUALITY

    args = sys.argv[1:]
    if len(args) >= 1:
        INPUT_DIR = args[0]
    if len(args) >= 2:
        OUTPUT_DIR = args[1]
    if len(args) >= 3:
        OUTPUT_FMT = args[2].lower()
    if len(args) >= 4:
        KEEP_TREE = (args[3].lower() != "flat")
    if len(args) >= 5:
        try:
            JPEG_QUALITY = int(args[4])
        except:
            pass

    OUTPUT_FMT = OUTPUT_FMT.lower().strip()
    if OUTPUT_FMT not in {"jpg", "png"}:
        print("[警告] 輸出格式僅支援 'jpg' 或 'png'，已改用 'jpg'")
        OUTPUT_FMT = "jpg"

    in_root = Path(INPUT_DIR).expanduser().resolve()
    out_root = Path(OUTPUT_DIR).expanduser().resolve()

    if not in_root.exists():
        print(f"[錯誤] 輸入資料夾不存在：{in_root}")
        sys.exit(1)

    print("========== 批次 HEIC 轉檔 ==========")
    print(f"輸入資料夾：{in_root}")
    print(f"輸出資料夾：{out_root}")
    print(f"輸出格式：  {OUTPUT_FMT}")
    print(f"保留結構：  {KEEP_TREE}")
    if OUTPUT_FMT == "jpg":
        print(f"JPG 品質：  {JPEG_QUALITY}")
    print("===================================")

    # 註冊 HEIF 讀取
    _register_heif()

    heic_files = list(_iter_heic_files(in_root))
    total = len(heic_files)
    if total == 0:
        print("找不到任何 .heic / .heif 檔案。")
        return

    print(f"共找到 {total} 個檔案，開始轉檔...\n")
    start = time.time()

    ok = 0
    fail = 0

    # 單執行緒逐檔處理（穩定且相容性高）
    # 想加速可改成 concurrent.futures.ThreadPoolExecutor / ProcessPoolExecutor
    for i, src in enumerate(heic_files, 1):
        success, msg = convert_one(src, in_root, out_root, KEEP_TREE, OUTPUT_FMT, JPEG_QUALITY)
        if success:
            ok += 1
        else:
            fail += 1
        print(f"[{i}/{total}] {msg}")

    sec = time.time() - start
    print("\n========== 完成 ==========")
    print(f"成功：{ok} 失敗：{fail}  耗時：{sec:.1f}s")
    print(f"輸出位置：{out_root}")

if __name__ == "__main__":
    main()
