from machine import I2S, Pin
import math
import array

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
    this plays whatever file you pass it as parameter
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


play_audio(file)
