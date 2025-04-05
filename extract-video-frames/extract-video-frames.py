import cv2
import os
import numpy

def extract_frames():
    try:
        video = cv2.VideoCapture("input-video.mp4")

        if video.isOpened():
            fps = video.get(cv2.CAP_PROP_FPS)
            print(f"fps: {fps}")

            total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
            print(f"total frames: {total_frames}")

            duration = total_frames/fps if fps > 0 else 0
            print(f"duration: {duration:.2f}")
            
            frame_rate = 1
            frame_interval = int(fps*frame_rate)
            print(f"frame interval: {frame_interval}")

            video_base_name = os.path.splitext(os.path.basename("input-video.mp4"))[0]
            print(f"video base name: {video_base_name}")

            success, frame = video.read()

            if success:
                cv2.imwrite("frame.png", frame)

            # count = 1

            # while True:
            #     success, frame = video.read()

            #     if not success:
            #         print("video.read failed")
            #         break

            #     frame_path = os.path.join("frames", f"frame {count}.png")

            #     cv2.imwrite(frame_path, frame)

            #     count += 1
            
            video.release()

        else : print(f"error: could not open video")

    except Exception as e:
        print(f"error {e}")

def toonify():
    try:
        print("toonify")
        img = cv2.imread("frame.png")
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray_blur = cv2.medianBlur(gray,5)
        edges = cv2.adaptiveThreshold(gray_blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)
        color = cv2.bilateralFilter(img, 9, 300,300)        
        cartoon = cv2.bitwise_and(color, color,mask=edges)
        cv2.imwrite("cartoon-frame.jpg", cartoon)

    except Exception as e:
        print(f"error {e}")


if __name__ == "__main__":
    if not os.path.exists("frames"):
        os.makedirs("frames")
    
    extract_frames()
    toonify()



