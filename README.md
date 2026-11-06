# 📻 SDR — Software Defined Radio presentatie

Interactieve [Reveal.js](https://revealjs.com)-presentatie (Nederlands) over Software Defined Radio,
voor beginners én gevorderden. 66 slides met live canvas-animaties, interactieve
visualisaties, echte DSP-graphics, gesynthetiseerde signaalgeluiden en een
speelbare SDR-tuner met WebAudio.

## Starten

```bash
python3 -m http.server 8421
# open http://localhost:8421/index.html
```

> Open de presentatie via http (niet via `file://`): de audio-fetch van de
> interactieve tuner werkt dan het betrouwbaarst.

Navigatie: `→` volgende slide · `↓` verdieping (o.a. de frequentie-safari) ·
`Esc` overzicht · `S` sprekersnotities.

## Inhoud

1. **Radio basics** — golven, modulatie (live geanimeerd), decibel + SNR-speeltuin
2. **Wat is SDR** — auto-animate blokschema, IQ-sampling met draaiende fasor, aliasing-demo
3. **Hardware** — RTL-SDR, HackRF, antennes (foto's, CC-gelicenseerd)
4. **Tools** — live FFT-demo, live waterfall, interactieve tuner 🎛️, GNU Radio
5. **Decoderen** — ADS-B radar-animatie, POCSAG (+audio), NOAA-satellietpass-animatie,
   echt ontvangen NOAA-19 beeld, frequentie-safari NL (↓)
6. **Data-analyse** — NumPy/pandas-voorbeelden met echte gegenereerde plots
7. **Wetgeving NL** — RDI, N/F-licentie, ethiek
8. **Demo's** — demoplan + backup-strategie

Plus didactiek: leerdoelen, 3 tussenquizzen, keybox-samenvattingen, leerpad en spiekbrief.

## Media regenereren

```bash
python3 -m venv .venv
.venv/bin/pip install numpy matplotlib
.venv/bin/python make_graphics.py   # waterfall, constellaties, plots → assets/
.venv/bin/python make_audio.py      # morse, POCSAG, APT, FM-sweep → assets/
```

## Licenties media

Eigen gegenereerde graphics/audio: CC0. Foto's via Wikimedia Commons, credits op de
betreffende slides: RTL-SDR (Joeceads, CC BY-SA 4.0) · HackRF One (Gareth Halfacree,
CC BY 2.0) · QFH-antenne (Karsten Lehmann, CC BY-SA 4.0) · discone (mr_t_77,
CC BY-SA 2.0) · NOAA-19 APT-beeld (NOAA, public domain).
