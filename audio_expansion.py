from machine import I2S, Pin
import os
import utime

file = './audio2.wav'

# I2S setup
audio = I2S(  # creates I2S audio object
    0,  # I2S interface number
    sck=Pin(27),  # bit clock
    ws=Pin(28),  # word select / left/right clock
    sd=Pin(26),  # audio data pin
    mode=I2S.TX,
    bits=16,  # each samples 16 bits wide
    format=I2S.STEREO,
    rate=44100,  # 44.1 Hz / samples/sec
    ibuf=20000
)


# WAV Player
def play_audio(file):
    """

    """
    # create a chunk of memory to temp. hold audio bytes
    buffer = bytearray(4096)
    with open(file, 'rb') as f:
        f.read(44)  # skip the wav header

        while True:
            n = f.readinto(buffer)
            if n == 0:
                break
            audio.write(buffer[:n])


def talk(text):
    words = text.lower().split()
    # print(os.listdir())

    for word in words:
        # file = f'wavs/{word}.wav'
        file = "wavs/" + word + ".wav"

        try:
            play_audio(file)
            utime.sleep_ms(100)
        except OSError:
            print("Something went wrong", file)


# print(os.listdir("wavs"))
print(os.listdir())
talk('closer detected')
# play_audio(file)


# ////////// HAVE TO FIX THE FOLDER LOCATION /////////
