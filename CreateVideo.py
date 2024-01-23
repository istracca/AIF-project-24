import cv2

def create_video(output_path, frames, frame_rate):
    height, width, _ = frames[0].shape
    video_writer = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'DIVX'), frame_rate, (width, height))
    for frame in frames:
        video_writer.write(frame)
    video_writer.release()