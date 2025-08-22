import cv2
import os

# ======== 設定參數 ========
frame_image1_path = r"frame_5\frame_000008.png"         # 左/上：較小影格（會縮放）
frame_image2_path = r"frame_5_x4\frame_000008.png"      # 右/下：較大影格
output_image_path  = r"exp_result\frame_000008_combined_x4.png"

scale_factor = 4.0  # 調整 frame_image1 的縮放倍數（>1 放大，<1 縮小）
combine_mode = "horizontal"  # "horizontal" 或 "vertical" 決定拼接方向

# ======== 讀取影格 ========
img1 = cv2.imread(frame_image1_path)
img2 = cv2.imread(frame_image2_path)

if img1 is None:
    raise FileNotFoundError(f"無法讀取影格: {frame_image1_path}")
if img2 is None:
    raise FileNotFoundError(f"無法讀取影格: {frame_image2_path}")

# ======== 調整 img1 尺寸 ========
h1, w1 = img1.shape[:2]
new_w1 = int(w1 * scale_factor)
new_h1 = int(h1 * scale_factor)
img1_resized = cv2.resize(img1, (new_w1, new_h1), interpolation=cv2.INTER_CUBIC)

# ======== 在圖片上加文字 ========
"""
#video 1、2
x1 = "956x1080"
font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 2
font_color = (255, 255, 255)  # 白色
thickness = 8
cv2.putText(img1_resized, f"original({x1})", (10, 50), font, font_scale, font_color, thickness, cv2.LINE_AA)
cv2.putText(img2, f"realesr({x1})", (10, 50), font, font_scale, font_color, thickness, cv2.LINE_AA)


x4 = "3824x4320"
font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 8
font_color = (255, 255, 255)  # 白色
thickness = 16
cv2.putText(img1_resized, f"original({x4})", (40, 200), font, font_scale, font_color, thickness, cv2.LINE_AA)
cv2.putText(img2, f"realesr({x4})", (40, 200), font, font_scale, font_color, thickness, cv2.LINE_AA)

#video 5、6
x1 = "1056x918"
font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 2
font_color = (255, 255, 255)  # 白色
thickness = 8
cv2.putText(img1_resized, f"original({x1})", (10, 50), font, font_scale, font_color, thickness, cv2.LINE_AA)
cv2.putText(img2, f"realesr({x1})", (10, 50), font, font_scale, font_color, thickness, cv2.LINE_AA)
"""
x4 = "4224x3672"
font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 8
font_color = (255, 255, 255)  # 白色
thickness = 16
cv2.putText(img1_resized, f"original({x4})", (40, 200), font, font_scale, font_color, thickness, cv2.LINE_AA)
cv2.putText(img2, f"realesr({x4})", (40, 200), font, font_scale, font_color, thickness, cv2.LINE_AA)


# ======== 對齊尺寸 ========
if combine_mode == "horizontal":
    # 高度對齊
    target_height = max(img1_resized.shape[0], img2.shape[0])
    img1_padded = cv2.copyMakeBorder(img1_resized, 0, target_height - img1_resized.shape[0], 0, 0, cv2.BORDER_CONSTANT, value=(0, 0, 0))
    img2_padded = cv2.copyMakeBorder(img2, 0, target_height - img2.shape[0], 0, 0, cv2.BORDER_CONSTANT, value=(0, 0, 0))
    combined = cv2.hconcat([img1_padded, img2_padded])
else:
    # 寬度對齊
    target_width = max(img1_resized.shape[1], img2.shape[1])
    img1_padded = cv2.copyMakeBorder(img1_resized, 0, 0, 0, target_width - img1_resized.shape[1], cv2.BORDER_CONSTANT, value=(0, 0, 0))
    img2_padded = cv2.copyMakeBorder(img2, 0, 0, 0, target_width - img2.shape[1], cv2.BORDER_CONSTANT, value=(0, 0, 0))
    combined = cv2.vconcat([img1_padded, img2_padded])

# ======== 儲存合成圖 ========
cv2.imwrite(output_image_path, combined)
print(f"✅ 完成！合成圖已儲存到: {output_image_path}")
