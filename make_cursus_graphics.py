#!/usr/bin/env python3
"""Figuren voor het cursusboek (cursus.html) — donker thema."""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mp

plt.rcParams.update({
    "figure.facecolor": "#15181d", "axes.facecolor": "#10141a",
    "axes.edgecolor": "#555", "axes.labelcolor": "#ddd",
    "xtick.color": "#aaa", "ytick.color": "#aaa",
    "text.color": "#ddd", "font.size": 13, "axes.titlesize": 15,
    "axes.titlecolor": "#4fc3f7",
})
rng = np.random.default_rng(3)
OUT = "assets"

# ---------------------------------------------------- 1. anatomie van een golf
t = np.linspace(0, 3, 1200)
y = np.sin(2 * np.pi * t)
fig, ax = plt.subplots(figsize=(10, 3.4), dpi=110)
ax.plot(t, y, color="#4fc3f7", lw=2.5)
ax.axhline(0, color="#444", lw=.8)
ax.annotate("", xy=(1.25, 1.12), xytext=(0.25, 1.12),
            arrowprops=dict(arrowstyle="<->", color="#ffb74d", lw=2))
ax.text(0.75, 1.22, "golflengte λ (= 300/f MHz in meters)", color="#ffb74d", ha="center")
ax.annotate("", xy=(2.25, 0), xytext=(2.25, 1),
            arrowprops=dict(arrowstyle="<->", color="#66bb6a", lw=2))
ax.text(2.33, 0.5, "amplitude\n(sterkte)", color="#66bb6a", va="center")
ax.plot([0.25, 1.25], [1, 1], ":", color="#ffb74d55")
ax.set_ylim(-1.4, 1.5); ax.set_xticks([]); ax.set_yticks([])
ax.set_title("Anatomie van een golf: amplitude, golflengte (en fase = waar je bent in de cyclus)")
fig.tight_layout(); fig.savefig(f"{OUT}/cursus_golf.png"); plt.close(fig)

# ---------------------------------------------------- 2. modulatie-overzicht
fig, axs = plt.subplots(3, 1, figsize=(10, 5.6), dpi=110)
tt = np.linspace(0, 1, 4000)
msg = np.sin(2 * np.pi * 3 * tt)
am = (0.62 + 0.38 * msg) * np.sin(2 * np.pi * 48 * tt)
axs[0].plot(tt, am, color="#4fc3f7", lw=1)
axs[0].plot(tt, 0.62 + 0.38 * msg, "--", color="#ffb74d", lw=1.4)
axs[0].plot(tt, -(0.62 + 0.38 * msg), "--", color="#ffb74d", lw=1.4)
axs[0].set_title("AM — de sterkte (envelop, oranje) volgt de boodschap")
fm = np.sin(2 * np.pi * 48 * tt + 14 * np.cumsum(msg) / len(tt) * 2 * np.pi * 3)
axs[1].plot(tt, fm, color="#66bb6a", lw=1)
axs[1].set_title("FM — de frequentie (dichtheid van de golven) volgt de boodschap")
bits = np.repeat(rng.integers(0, 2, 10), 400)
fsk = np.sin(2 * np.pi * (30 + bits * 40) * tt)
axs[2].plot(tt, fsk, color="#ffb74d", lw=1)
for i in range(10):
    axs[2].text(i / 10 + .05, 1.25, str(bits[i * 400]), color="#ffb74d", ha="center", fontsize=12)
axs[2].set_ylim(-1.5, 1.7)
axs[2].set_title("FSK (digitaal) — bits als sprongen tussen twee frequenties")
for a in axs: a.set_xticks([]); a.set_yticks([])
fig.tight_layout(); fig.savefig(f"{OUT}/cursus_modulatie.png"); plt.close(fig)

# ---------------------------------------------------- 3. bandkaart (log-schaal)
fig, ax = plt.subplots(figsize=(10, 2.9), dpi=110)
bands = [("LF/MF", 0.03, 3, "#5c6bc0"), ("HF", 3, 30, "#26a69a"),
         ("VHF", 30, 300, "#66bb6a"), ("UHF", 300, 3000, "#ffb74d"),
         ("SHF", 3000, 30000, "#ef5350")]
for naam, lo, hi, kleur in bands:
    ax.axvspan(lo, hi, color=kleur, alpha=.25)
    ax.text(np.sqrt(lo * hi), .82, naam, ha="center", fontsize=14, color=kleur, weight="bold")
markers = [(0.0775, "DCF77", .18), (1, "AM", .18), (7, "amateurs", .18), (14, "DX", .55),
           (100, "FM", .18), (137, "NOAA", .55), (170, "P2000", .18), (434, "sensoren", .55),
           (1090, "ADS-B", .18), (12000, "sat-TV", .18)]
for f, naam, ty in markers:
    ax.plot(f, .35, "o", color="#fff", ms=5)
    ax.text(f, ty, naam, rotation=45, ha="right" if ty < .4 else "left",
            va="top" if ty < .4 else "bottom", fontsize=10, color="#cde")
ax.set_xscale("log"); ax.set_xlim(0.05, 30000); ax.set_ylim(0, 1)
ax.set_yticks([]); ax.set_xlabel("frequentie (MHz, logaritmisch)")
ax.set_title("Het radiospectrum — lage frequenties reizen ver, hoge dragen veel data")
fig.tight_layout(); fig.savefig(f"{OUT}/cursus_bandkaart.png"); plt.close(fig)

# ---------------------------------------------------- 4. dB / SNR figuur
f = np.linspace(0, 1, 1200)
noise = -100 + rng.normal(0, 1.6, f.size)
piek = 24 * np.exp(-((f - 0.48) ** 2) / (2 * 0.012 ** 2))
spec = noise + piek
fig, ax = plt.subplots(figsize=(10, 3.4), dpi=110)
ax.plot(f, spec, color="#4fc3f7", lw=1.2)
ax.axhline(-100, ls="--", color="#888", lw=1.2)
ax.annotate("", xy=(0.56, -76), xytext=(0.56, -100),
            arrowprops=dict(arrowstyle="<->", color="#ffb74d", lw=2))
ax.text(0.575, -88, "SNR = 24 dB\n(≈ 250× het ruisvermogen)", color="#ffb74d")
ax.text(0.03, -97.4, "ruisvloer — die is er áltijd", color="#999")
ax.set_xlabel("frequentie →"); ax.set_ylabel("vermogen (dBm)")
ax.set_xticks([]); ax.set_title("Niet de sterkte maar de afstand tot de ruis (SNR) bepaalt of je kunt decoderen")
fig.tight_layout(); fig.savefig(f"{OUT}/cursus_snr.png"); plt.close(fig)

# ---------------------------------------------------- 5. klassiek vs SDR blokschema
fig, axs = plt.subplots(2, 1, figsize=(10, 4.2), dpi=110)
def blok(ax, x, w, naam, kleur, rand):
    ax.add_patch(mp.FancyBboxPatch((x, 0.25), w, 0.5, boxstyle="round,pad=0.02",
                                    fc=kleur, ec=rand, lw=1.8))
    ax.text(x + w / 2, 0.5, naam, ha="center", va="center", fontsize=12, color="#fff")
def pijl(ax, x):
    ax.annotate("", xy=(x + .035, 0.5), xytext=(x, 0.5),
                arrowprops=dict(arrowstyle="->", color="#ffb74d", lw=2.2))
ax = axs[0]
for i, naam in enumerate(["filter", "mixer", "IF-filter", "demodulator", "audio"]):
    blok(ax, .02 + i * .2, .15, naam, "#37474f", "#78909c")
    if i < 4: pijl(ax, .175 + i * .2)
ax.set_title("Klassieke radio: elke functie een eigen stuk hardware — één apparaat, één taak")
ax = axs[1]
blok(ax, .02, .15, "tuner/\nversterker", "#1b5e20", "#66bb6a"); pijl(ax, .175)
blok(ax, .22, .15, "ADC", "#1b5e20", "#66bb6a"); pijl(ax, .375)
blok(ax, .42, .56, "SOFTWARE — filteren · demoduleren · decoderen · analyseren", "#0d47a1", "#4fc3f7")
ax.set_title("SDR: digitaliseer zo vroeg mogelijk — de rest is code. Eén apparaat, duizend radio's")
for a in axs: a.set_xlim(0, 1); a.set_ylim(0, 1); a.axis("off")
fig.tight_layout(); fig.savefig(f"{OUT}/cursus_blokschema.png"); plt.close(fig)

# ---------------------------------------------------- 6. IQ-fasor
fig, axs = plt.subplots(1, 2, figsize=(10, 3.8), dpi=110, width_ratios=[1, 1.6])
th = np.linspace(0, 2 * np.pi, 200)
ax = axs[0]
ax.plot(np.cos(th), np.sin(th), color="#555")
ax.axhline(0, color="#444", lw=.8); ax.axvline(0, color="#444", lw=.8)
hoek = 0.9
ax.annotate("", xy=(np.cos(hoek), np.sin(hoek)), xytext=(0, 0),
            arrowprops=dict(arrowstyle="->", color="#4fc3f7", lw=2.5))
ax.plot([np.cos(hoek), np.cos(hoek)], [0, np.sin(hoek)], ":", color="#66bb6a")
ax.plot([0, np.cos(hoek)], [np.sin(hoek), np.sin(hoek)], ":", color="#ffb74d")
ax.text(np.cos(hoek) + .05, np.sin(hoek) / 2, "Q", color="#66bb6a", fontsize=14)
ax.text(np.cos(hoek) / 2, np.sin(hoek) + .07, "I", color="#ffb74d", fontsize=14)
ax.plot(np.cos(hoek), np.sin(hoek), "o", color="#ffb74d", ms=8)
ax.set_aspect("equal"); ax.set_xticks([]); ax.set_yticks([])
ax.set_title("één IQ-sample =\npunt op het 'wijzertje'")
ax = axs[1]
tt = np.linspace(0, 3, 600)
ax.plot(tt, np.cos(2 * np.pi * tt), color="#ffb74d", lw=2, label="I = cos(ωt)")
ax.plot(tt, np.sin(2 * np.pi * tt), color="#66bb6a", lw=2, label="Q = sin(ωt), 90° later")
ax.legend(facecolor="#15181d", edgecolor="#444", labelcolor="#ddd")
ax.set_xticks([]); ax.set_yticks([])
ax.set_title("het signaal twee keer gemeten: direct (I) en een kwartslag verschoven (Q)")
fig.tight_layout(); fig.savefig(f"{OUT}/cursus_iq.png"); plt.close(fig)

# ---------------------------------------------------- 7. aliasing
fig, ax = plt.subplots(figsize=(10, 3.6), dpi=110)
tt = np.linspace(0, 1, 2000)
f0 = 10
ax.plot(tt, np.sin(2 * np.pi * f0 * tt), color="#4fc3f7", lw=1.8, label="echt signaal (10 Hz)")
fs = 13
ts = np.arange(0, 1, 1 / fs)
ax.plot(ts, np.sin(2 * np.pi * f0 * ts), "o", color="#ffb74d", ms=8, label=f"samples ({fs} S/s — te weinig!)")
fa = f0 - round(f0 / fs) * fs
ax.plot(tt, np.sin(2 * np.pi * fa * tt), "--", color="#ff7043", lw=2.2,
        label=f"wat de SDR reconstrueert: spook op {abs(fa)} Hz")
ax.legend(facecolor="#15181d", edgecolor="#444", labelcolor="#ddd", loc="upper right", fontsize=11)
ax.set_xticks([]); ax.set_yticks([]); ax.set_ylim(-1.35, 1.75)
ax.set_title("Aliasing: sample je trager dan 2× de signaalfrequentie, dan past er een tweede signaal\nperfect door dezelfde punten — en dát is wat je ontvanger ziet")
fig.tight_layout(); fig.savefig(f"{OUT}/cursus_aliasing.png"); plt.close(fig)

print("cursusfiguren klaar")
