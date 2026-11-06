#!/usr/bin/env python3
"""Genereer echte DSP-graphics voor de SDR-presentatie (donker thema)."""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams.update({
    "figure.facecolor": "#111111", "axes.facecolor": "#0a0f1a",
    "axes.edgecolor": "#555", "axes.labelcolor": "#ddd",
    "xtick.color": "#aaa", "ytick.color": "#aaa",
    "text.color": "#ddd", "font.size": 13, "axes.titlesize": 16,
    "axes.titlecolor": "#4fc3f7",
})
rng = np.random.default_rng(42)
OUT = "assets"

# ---------------------------------------------------------------- waterfall
# Echte FFT-waterfall van gesimuleerde IQ-data: WBFM, NBFM, pager-bursts, hopping
fs = 2.4e6
N = int(fs * 0.6)           # 0.6 s
t = np.arange(N) / fs
iq = (rng.normal(0, .18, N) + 1j * rng.normal(0, .18, N))   # ruisvloer

def fm(fc, dev, msg_bw, amp):
    msg = np.cumsum(rng.normal(0, 1, N))
    msg = np.convolve(msg, np.ones(200)/200, "same")
    msg = msg / np.abs(msg).max()
    return amp * np.exp(1j * (2*np.pi*fc*t + 2*np.pi*dev*np.cumsum(msg)/fs))

iq += fm(-800e3, 75e3, 15e3, 0.9)          # breedband FM-omroep
iq += fm(-250e3, 5e3, 3e3, 0.5)            # smalle FM
iq += fm(-200e3, 5e3, 3e3, 0.35)           # nog een smalle FM

# pager bursts (FSK @ +300 kHz)
burst = np.zeros(N, complex)
for start in [0.05, 0.22, 0.31, 0.47]:
    s, e = int(start*fs), int((start+0.05)*fs)
    bits = np.repeat(rng.integers(0, 2, (e-s)//2000 + 1), 2000)[:e-s]
    f = 300e3 + (bits*2-1)*4.5e3
    burst[s:e] = 0.8 * np.exp(1j*2*np.pi*np.cumsum(f)/fs)
iq += burst

# frequency hopper rond +700 kHz
hop = np.zeros(N, complex)
seg = int(0.03*fs)
for i in range(0, N-seg, seg):
    fc = 700e3 + rng.choice([-150e3, -75e3, 0, 75e3, 150e3])
    hop[i:i+seg] = 0.7 * np.exp(1j*2*np.pi*fc*t[:seg])
iq += hop

nfft = 2048
nrows = N // nfft
S = np.fft.fftshift(np.fft.fft(iq[:nrows*nfft].reshape(nrows, nfft), axis=1), axes=1)
P = 10*np.log10(np.abs(S)**2 + 1e-12)

fig, ax = plt.subplots(figsize=(12, 5.2), dpi=110)
ax.imshow(P, aspect="auto", cmap="turbo",
          extent=[-fs/2/1e6, fs/2/1e6, 0.6, 0], vmin=P.mean()-6, vmax=P.max()-6)
ax.set_xlabel("Frequentie-offset (MHz)"); ax.set_ylabel("Tijd (s)")
ax.set_title("Waterfall — 2.4 MHz spectrum (gesimuleerde IQ-opname, echte FFT)")
for x, lbl in [(-0.8, "WBFM\nomroep"), (-0.22, "2× NBFM"), (0.3, "pager-\nbursts"), (0.7, "freq.\nhopper")]:
    ax.annotate(lbl, (x, 0.02), color="white", ha="center", va="top", fontsize=12,
                bbox=dict(boxstyle="round", fc="#000a", ec="none"))
fig.tight_layout(); fig.savefig(f"{OUT}/waterfall_real.png"); plt.close(fig)

# ---------------------------------------------------------------- spectrum
f_axis = np.fft.fftshift(np.fft.fftfreq(nfft, 1/fs))/1e6
avg = P.mean(axis=0)
fig, ax = plt.subplots(figsize=(12, 3.4), dpi=110)
ax.plot(f_axis, avg, color="#4fc3f7", lw=1.2)
ax.fill_between(f_axis, avg.min()-2, avg, color="#4fc3f7", alpha=.25)
ax.set_xlabel("Frequentie-offset (MHz)"); ax.set_ylabel("Vermogen (dB)")
ax.set_title("Spectrum (gemiddelde FFT) — dezelfde opname")
ax.grid(alpha=.2)
fig.tight_layout(); fig.savefig(f"{OUT}/spectrum_real.png"); plt.close(fig)

# ---------------------------------------------------------------- constellaties
fig, axs = plt.subplots(1, 3, figsize=(12, 4.2), dpi=110)
n = 3000
# BPSK / QPSK / 16-QAM met ruis
bpsk = (rng.integers(0, 2, n)*2-1) + 0j
qpsk = ((rng.integers(0, 2, n)*2-1) + 1j*(rng.integers(0, 2, n)*2-1)) / np.sqrt(2)
lv = np.array([-3, -1, 1, 3]) / np.sqrt(10)
qam = rng.choice(lv, n) + 1j*rng.choice(lv, n)
for ax, sym, name, snr in zip(axs, [bpsk, qpsk, qam], ["BPSK (1 bit/sym)", "QPSK (2 bits/sym)", "16-QAM (4 bits/sym)"], [12, 14, 18]):
    noise = (rng.normal(0, 1, n) + 1j*rng.normal(0, 1, n)) * 10**(-snr/20)
    r = sym + noise
    ax.scatter(r.real, r.imag, s=4, c="#4fc3f7", alpha=.4, linewidths=0)
    ax.set_title(name, fontsize=13); ax.set_xlim(-1.5, 1.5); ax.set_ylim(-1.5, 1.5)
    ax.axhline(0, color="#444", lw=.8); ax.axvline(0, color="#444", lw=.8)
    ax.set_xticks([]); ax.set_yticks([]); ax.set_aspect("equal")
fig.suptitle("Constellatiediagrammen — I/Q-samples van digitale modulaties (met ruis)", color="#4fc3f7")
fig.tight_layout(); fig.savefig(f"{OUT}/constellations.png"); plt.close(fig)

# ---------------------------------------------------------------- FM-demodulatie keten
fig, axs = plt.subplots(3, 1, figsize=(12, 6.4), dpi=110, sharex=False)
fs2 = 240e3; n2 = int(fs2*0.02); t2 = np.arange(n2)/fs2
msg = np.sin(2*np.pi*1000*t2) + 0.4*np.sin(2*np.pi*2500*t2)
fmsig = np.exp(1j*2*np.pi*75e3*np.cumsum(msg)/fs2 * 0.5)
axs[0].plot(t2*1e3, msg, color="#66bb6a"); axs[0].set_title("1. Audioboodschap (1 kHz + 2.5 kHz)")
axs[1].plot(t2*1e3, fmsig.real, color="#4fc3f7", lw=.6); axs[1].set_title("2. FM-gemoduleerd signaal (reëel deel van IQ)")
demod = np.angle(fmsig[1:] * np.conj(fmsig[:-1]))
axs[2].plot(t2[1:]*1e3, demod/np.abs(demod).max(), color="#ffb74d")
axs[2].set_title("3. Gedemoduleerd:  np.angle(iq[1:] * conj(iq[:-1]))  → audio terug!")
axs[2].set_xlabel("Tijd (ms)")
for a in axs: a.set_yticks([]); a.grid(alpha=.15)
fig.tight_layout(); fig.savefig(f"{OUT}/fm_demod_chain.png"); plt.close(fig)

# ---------------------------------------------------------------- ADS-B polar bereik
fig = plt.figure(figsize=(6.4, 6.4), dpi=110)
ax = fig.add_subplot(projection="polar", facecolor="#0a0f1a")
az = np.deg2rad(np.arange(0, 360, 5))
base = 180 + 90*np.sin(np.deg2rad(np.arange(0, 360, 5))*1.0 + 1.2)
base[20:30] *= 0.35   # blokkade (gebouw)
base = np.convolve(np.r_[base[-2:], base, base[:2]], np.ones(5)/5, "valid")
rmax = base + rng.normal(0, 12, len(az))
ax.fill(az, rmax, color="#4fc3f7", alpha=.3)
ax.plot(np.r_[az, az[0]], np.r_[rmax, rmax[0]], color="#4fc3f7", lw=1.5)
ax.set_theta_zero_location("N"); ax.set_theta_direction(-1)
ax.set_title("ADS-B: max. ontvangstafstand per richting (km)\n— dip = flatgebouw ten NO", pad=18, fontsize=13)
ax.tick_params(colors="#aaa"); ax.grid(alpha=.3)
fig.tight_layout(); fig.savefig(f"{OUT}/adsb_polar.png"); plt.close(fig)

# ---------------------------------------------------------------- rtl_433 sensor-log (24h temperatuur)
fig, ax = plt.subplots(figsize=(12, 3.6), dpi=110)
hours = np.linspace(0, 24, 24*12)
for sid, (off, amp, col) in {"Nexus-TH #42 (tuin)": (9, 6, "#4fc3f7"),
                              "LaCrosse #7 (zolder)": (14, 8, "#ffb74d"),
                              "Oregon #19 (schuur)": (10, 5, "#66bb6a")}.items():
    temp = off + amp*np.sin((hours-14)/24*2*np.pi*1.0)*0.5 + amp/2 + rng.normal(0, .25, len(hours))
    ax.plot(hours, temp, lw=1.4, label=sid, color=col)
ax.legend(facecolor="#111", edgecolor="#444", labelcolor="#ddd", fontsize=11)
ax.set_xlabel("Uur van de dag"); ax.set_ylabel("°C"); ax.set_xlim(0, 24)
ax.set_title("rtl_433 → 24 uur buurt-sensoren gelogd (433.92 MHz)")
ax.grid(alpha=.2)
fig.tight_layout(); fig.savefig(f"{OUT}/rtl433_log.png"); plt.close(fig)

# ---------------------------------------------------------------- APT-stijl weersatelliet-strip
# Synthetisch NOAA-APT-achtig beeld: twee kanalen + sync + telemetrie
w, h = 909, 360
img = np.zeros((h, 2*w+80))
yy, xx = np.mgrid[0:h, 0:w]
clouds = np.zeros((h, w))
for _ in range(60):
    cx, cy, r, a = rng.uniform(0, w), rng.uniform(0, h), rng.uniform(15, 90), rng.uniform(.2, 1)
    clouds += a*np.exp(-(((xx-cx)**2+(yy-cy)**2)/(2*r**2)))
clouds = np.clip(clouds/clouds.max()*1.6, 0, 1)
coast = (np.sin(xx/90 + yy/140) + np.sin(xx/37) > 1.1).astype(float)*0.25 + 0.3
visible = np.clip(coast + clouds*0.7, 0, 1)
ir = np.clip(1 - clouds*0.9 + 0.1*rng.normal(0, .05, clouds.shape), 0, 1)*0.8
img[:, 20:20+w] = visible
img[:, 60+w:60+2*w] = ir
img[:, :20] = (np.arange(h) % 4 < 2)[:, None] * 1.0        # sync A
img[:, 40+w:60+w] = (np.arange(h) % 8 < 4)[:, None] * 0.8  # sync B
img += rng.normal(0, .02, img.shape)
fig, ax = plt.subplots(figsize=(12, 3.4), dpi=110)
ax.imshow(np.clip(img, 0, 1), cmap="gray", aspect="auto")
ax.set_xticks([]); ax.set_yticks([])
ax.set_title("NOAA APT-formaat: sync | zichtbaar-licht kanaal | sync | infrarood kanaal  (gesimuleerd)")
fig.tight_layout(); fig.savefig(f"{OUT}/apt_sim.png"); plt.close(fig)

print("alle graphics gegenereerd")
