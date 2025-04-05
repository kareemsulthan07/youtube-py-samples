from moviepy import VideoFileClip


if __name__ == "__main__":
    try:
        print("start")

        video = VideoFileClip("video-file.mp4")
        video.audio.write_audiofile("audio-file.mp3")
        video.close()

        print("succeeded")

    except Exception as e:
        print("error")