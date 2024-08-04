from typing import List
import cv2

def create_video(image_files: List[str], durations: List[int], output_file: str, fps: int = 24) -> None:
    frame = cv2.imread(image_files[0])
    height, width, _ = frame.shape

    fourcc = cv2.VideoWriter.fourcc(*"mp4v")
    video = cv2.VideoWriter(output_file, fourcc, fps, (width, height))

    for image_file, duration in zip(image_files, durations):
        frame = cv2.imread(image_file)
        num_frames = int(fps * duration)
        for _ in range(num_frames):
            video.write(frame)
    
    video.release()

