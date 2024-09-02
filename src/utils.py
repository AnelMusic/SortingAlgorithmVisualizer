import numpy as np
import simpleaudio as sa

def generate_sound(frequency=1000, duration=10, sample_rate=44100):
    """
    Generate a sine wave sound signal.

    Parameters:
        frequency (int): The frequency of the sound in Hertz (default is 1000 Hz).
        duration (int): The duration of the sound in milliseconds (default is 10 ms).
        sample_rate (int): The number of samples per second (default is 44100, which is CD quality).

    Returns:
        numpy.ndarray: A NumPy array representing the generated sound wave in 16-bit PCM format.
    """
    t = np.linspace(0, duration / 1000, int(sample_rate * duration / 1000), False)
    wave = 0.5 * np.sin(2 * np.pi * frequency * t)
    wave = (wave * 32767).astype(np.int16)
    return wave

def play_short_beep(wave, sample_rate=44100):
    """
    Play a short beep sound from a given wave signal.

    Parameters:
        wave (numpy.ndarray): The sound wave data to be played.
        sample_rate (int): The sample rate of the sound wave in Hertz (default is 44100 Hz).

    Returns:
        None
    """
    beep_obj = sa.play_buffer(wave, 1, 2, sample_rate)
    beep_obj.wait_done()
