from gtts import gTTS
import os


words = [
    'person',
    'object',
    'closer',
    'warning',
    'obstacle',
    'stop',
    'detected',
    'left',
    'right'
]

while True:
    for word in words:
        tts = gTTS(text=word, lang='en')
        mp3 = f"{word}.mp3"
        wav = f"./wavs/{word}.wav"

        tts.save(mp3)

        os.system(f'ffmpeg -y -i {mp3} -ac 1 -ar 22050 {wav}')

        os.remove(mp3)
    print('done')
    break
