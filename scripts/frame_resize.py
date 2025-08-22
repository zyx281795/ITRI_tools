import cv2
import os

# ======== 設定參數 ========
input_image_path = r"frame_5_x4\frame_000008.png"     # 輸入影格路徑
output_image_path = r"exp_result\frame_000008.png"  # 輸出影格路徑
scale_factor = 0.25  # 縮放比例 (0.5 = 縮小一半, 2.0 = 放大兩倍)

# ======== 讀取影格 ========
img = cv2.imread(input_image_path)
if img is None:
    raise FileNotFoundError(f"無法讀取影格: {input_image_path}")

# ======== 計算新尺寸並縮放 ========
h, w = img.shape[:2]
new_w = int(w * scale_factor)
new_h = int(h * scale_factor)
resized_img = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_AREA)

# ======== 儲存縮小後影格 ========
cv2.imwrite(output_image_path, resized_img)
print(f"✅ 完成！縮小後的影格已儲存到: {output_image_path}")
