import os
import filetype
from pathlib import Path
import ffmpeg
from patch_ffprobe import FFProbe

videos = []

def get_codec(path: str):
    try:
        metadata = FFProbe(path)
        if len(metadata.video) != 0:
            return metadata.video[0].codec()

        return metadata.audio[0].codec()
    except:
        return None


for dir, folders, files in os.walk('.'):
        base_dir = Path(dir)
        for item in files:

            file_path = base_dir / item
            guess = filetype.guess(str(file_path))

            if guess and 'video' in guess.mime and not '.mkv' in str(file_path):
                videos.append(file_path)

for video in videos:
    if get_codec(str(video)) == 'hevc':
        continue
    try:
        n_video = Path(video)
        stream = ffmpeg.input(n_video)
        stream = ffmpeg.output(stream,str(n_video)+'.mkv')
        ffmpeg.run(stream)
        os.remove(video)
    except:
        pass