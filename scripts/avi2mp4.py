import cv2
import os

def resize_video(input_path, output_path, scale=0.5):
    # 開啟影片
    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        print(f"無法打開影片：{input_path}")
        return

    # 取得影片參數
    fps = cap.get(cv2.CAP_PROP_FPS)
    width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # 編碼格式

    new_width = int(width * scale)
    new_height = int(height * scale)

    # 建立輸出影片寫入器
    out = cv2.VideoWriter(output_path, fourcc, fps, (new_width, new_height))

    # 開始逐幀處理
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        resized_frame = cv2.resize(frame, (new_width, new_height), interpolation=cv2.INTER_AREA)
        out.write(resized_frame)

    # 釋放資源
    cap.release()
    out.release()
    print(f"影片已儲存為：{output_path}")

if __name__ == "__main__":
    input_video = "V000000094.mp4"    # 請替換為你的原始影片路徑
    output_video = "4.mp4"  # 輸出影片名稱
    resize_video(input_video, output_video)
