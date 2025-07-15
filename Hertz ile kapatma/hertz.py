import numpy as np
import pyaudio
import ctypes

TARGET_FREQ = 1248
TOLERANCE = 5
CHUNK = 4096
RATE = 44100

def lock_screen():
    ctypes.windll.user32.LockWorkStation()

def detect_freq(data):
    fft_data = np.fft.fft(data)
    freqs = np.fft.fftfreq(len(fft_data), 1.0 / RATE)
    idx = np.argmax(np.abs(fft_data[:len(fft_data)//2]))
    freq = abs(freqs[idx])
    return freq

def listen():
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("Dinleniyor...")

    try:
        while True:
            data = np.frombuffer(stream.read(CHUNK, exception_on_overflow=False), dtype=np.int16)
            freq = detect_freq(data)
            print(f"{freq:.2f} Hz algılandı!")
            if TARGET_FREQ - TOLERANCE <= freq <= TARGET_FREQ + TOLERANCE:
                print("2000 Hz algılandı! Ekran kilitleniyor...")
                lock_screen()
                break
    except KeyboardInterrupt:
        print("Manuel durduruldu.")
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()

listen()
