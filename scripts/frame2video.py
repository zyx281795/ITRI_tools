import cv2
import os
from natsort import natsorted

# ======== 設定參數 ========
frame_folder = r"frame_1_x4"   # 輸入影格資料夾
output_video = r"output_video.mp4"  # 輸出影片檔案
fps = 30  # 設定影片 FPS

def frames_to_video(frame_folder, output_video, fps=30):
    # 取得影格清單 (排序過，避免 frame_10 在 frame_2 前面)
    frames = [f for f in os.listdir(frame_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    frames = natsorted(frames)

    if not frames:
        raise ValueError("找不到任何影格，請確認資料夾是否正確。")

    # 讀取第一張影格來獲取尺寸
    first_frame = cv2.imread(os.path.join(frame_folder, frames[0]))
    height, width, layers = first_frame.shape

    # 建立 VideoWriter
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # 或 'XVID'
    out = cv2.VideoWriter(output_video, fourcc, fps, (width, height))

    # 逐張寫入影片
    for frame_name in frames:
        frame_path = os.path.join(frame_folder, frame_name)
        img = cv2.imread(frame_path)
        if img is None:
            print(f"警告：讀取失敗 {frame_path}")
            continue
        out.write(img)

    out.release()
    print(f"影片已輸出到 {output_video}")

if __name__ == "__main__":
    frames_to_video(frame_folder, output_video, fps)
