from moviepy import VideoFileClip

print("start")
clip = VideoFileClip("input-video.mp4").subclipped(0, 2)
clip.write_gif("output.gif",fps=1)
clip.close()
print("end")