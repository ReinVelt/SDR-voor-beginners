#!/usr/bin/env python3
"""Synthetiseer herkenbare radiogeluiden voor de SDR-presentatie."""
import numpy as np
import wave

FS = 22050
OUT = "assets"
rng = np.random.default_rng(7)


def save(name, sig, gain=0.85):
    sig = sig / (np.abs(sig).max() + 1e-9) * gain
    data = (sig * 32767).astype(np.int16)
    with wave.open(f"{OUT}/{name}.wav", "wb") as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(FS)
        f.writeframes(data.tobytes())
    print(name, f"{len(sig)/FS:.1f}s")


def t_axis(sec):
    return np.arange(int(FS * sec)) / FS


# ---------------------------------------------------------------- Morse (CW)
MORSE = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.',
    'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
    'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
    'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
    'Y': '-.--', 'Z': '--..', '0': '-----', '1': '.----', '2': '..---',
    '3': '...--', '4': '....-', '5': '.....', ' ': ' ',
}
def morse(text, wpm=18, tone=600):
    unit = 1.2 / wpm
    env = []
    for ch in text.upper():
        code = MORSE.get(ch, '')
        if ch == ' ':
            env += [0] * int(4 * unit * FS)
            continue
        for sym in code:
            env += [1] * int((1 if sym == '.' else 3) * unit * FS)
            env += [0] * int(unit * FS)
        env += [0] * int(2 * unit * FS)
    env = np.array(env, float)
    # zachte flanken tegen klikken
    k = np.hanning(int(0.005 * FS))
    env = np.convolve(env, k / k.sum(), "same")
    t = np.arange(len(env)) / FS
    sig = env * np.sin(2 * np.pi * tone * t)
    sig += 0.04 * rng.normal(0, 1, len(sig))          # etherruis
    return sig

save("morse", morse("CQ CQ DE PA0SDR K"))

# ---------------------------------------------------------------- POCSAG-achtige FSK-bursts
def pocsag_burst(n_bits=350, baud=1200, f_mark=1200, f_space=2200):
    bits = np.r_[np.tile([1, 0], 60), rng.integers(0, 2, n_bits)]  # preamble + data
    spb = int(FS / baud)
    freq = np.repeat(np.where(bits > 0, f_mark, f_space), spb)
    ph = 2 * np.pi * np.cumsum(freq) / FS
    return np.sin(ph)

sig = 0.05 * rng.normal(0, 1, int(FS * 1.0))
for _ in range(3):
    sig = np.r_[sig, pocsag_burst(int(rng.integers(250, 500))),
                0.05 * rng.normal(0, 1, int(FS * rng.uniform(0.4, 0.9)))]
save("pocsag", sig)

# ---------------------------------------------------------------- NOAA APT "tik-tok"
dur = 8.0
t = t_axis(dur)
line = (t % 0.5) / 0.5                                    # 2 lijnen/s
sync = ((t % 0.5) < 0.04) * (np.sin(2 * np.pi * 1040 * t) > 0)   # sync-buzz
img = 0.45 + 0.35 * np.clip(np.convolve(rng.normal(0, 1, len(t)),
                                        np.ones(800) / 800, "same") * 6, -1, 1)
envel = np.where(sync > 0, 1.0, img)
sig = envel * np.sin(2 * np.pi * 2400 * t)                 # APT-subcarrier
sig += 0.05 * rng.normal(0, 1, len(sig))
save("apt", sig)

# ---------------------------------------------------------------- FM-tuning sweep (ruis -> zender -> ruis)
dur = 7.0
t = t_axis(dur)
noise = rng.normal(0, 1, len(t))
# "zender": eenvoudig deuntje (pentatonisch) + bas
notes = [220, 262, 294, 330, 392, 330, 294, 262]
mel = np.zeros(len(t))
for i, f in enumerate(np.tile(notes, 3)[:int(dur / 0.3)]):
    s, e = int(i * 0.3 * FS), int((i + 1) * 0.3 * FS)
    seg = t[s:e]
    mel[s:e] = 0.6 * np.sin(2 * np.pi * f * seg) + 0.3 * np.sin(2 * np.pi * f * 2 * seg)
mel += 0.25 * np.sin(2 * np.pi * 110 * t) * (np.sin(2 * np.pi * 2 * t) > 0)
# tuning: zender komt voorbij in het midden
prox = np.exp(-((t - dur / 2) ** 2) / (2 * 1.1 ** 2))
wobble = np.sin(2 * np.pi * (800 + 600 * (1 - prox)) * t)  # fluittoon naast de zender
sig = (1 - prox) * 0.55 * noise + prox * mel + np.clip(prox * (1 - prox) * 4, 0, 1) * 0.25 * wobble
save("fm_tuning", sig)

print("audio klaar")
