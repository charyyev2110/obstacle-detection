from gtts import gTTS
from pathlib import Path
import subprocess
import shutil
import os


words = [
    # 'person',
    # 'object',
    # 'closer',
    # 'warning',
    # 'obstacle',
    # 'stop',
    # 'detected',
    # 'left',
    # 'right'
    'moving'
]

WAV_DIR = Path("wavs")
TEMP_DIR = Path("mp3")


# def remove_old(folder: Path) -> None:
#     folder.mkdir(exist_ok=True)
#     for item in folder.iterdir():
#         if item.is_file():
#             item.unlink()


while True:
    for word in words:
        tts = gTTS(text=word, lang='en')
        mp3 = f"{word}.mp3"
        wav = f"./wavs/{word}.wav"

        tts.save(mp3)

        os.system(f'ffmpeg -y -i {mp3} -ac 2 -ar 44100 -sample_fmt s16 {wav}')

        os.remove(mp3)
    print('done')
    break
