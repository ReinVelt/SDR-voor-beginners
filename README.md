# 📻 SDR-cursus — Software Defined Radio

**Rein Velt · [Hackerspace Drenthe](https://hackerspacedrenthe.nl)**

**Live:**
- 📖 **Cursusboek** (leesversie met volledige uitleg en verhaal): https://reinvelt.github.io/SDR-voor-beginners/cursus.html
- 📽 **Slides** (klassikaal / interactieve demo's): https://reinvelt.github.io/SDR-voor-beginners/

Interactieve hands-on [Reveal.js](https://revealjs.com)-cursus (Nederlands) over Software Defined Radio,
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

## Inhoud — 8 lessen

Elke les heeft leerdoelen, duur, benodigdheden en sluit af met een 🔬 **lab-opdracht**;
onderweg zijn er ✋ zelftoetsen. De cursus eindigt met een capstone-eindopdracht
(bouw je eigen ontvangststation).

1. **Radio basics** (25 min) — golven, modulatie (live geanimeerd), dB + SNR-speeltuin · *lab: WebSDR-safari*
2. **Wat is SDR** (25 min) — auto-animate blokschema, IQ-fasor, aliasing-demo · *lab: voorspel het spook*
3. **Hardware** (20 min) — RTL-SDR, HackRF, antennes · *lab: dongle aan de praat*
4. **Tools** (30 min) — live FFT-demo, waterfall, interactieve tuner 🎛️, GNU Radio · *lab: waterfall-safari + flowgraph*
5. **Decoderen** (40 min) — ADS-B radar-animatie, POCSAG (+audio), satellietpass,
   echt NOAA-19 beeld, frequentie-safari NL (↓) · *lab: kies je missie*
6. **Data-analyse** (30 min) — NumPy/pandas met echte plots · *lab: oefenset `assets/sample_rtl433.jsonl`*
7. **Wetgeving NL** (15 min) — RDI, N/F-licentie, ethiek · *lab: mag dit? (casussen)*
8. **Demo's & eindopdracht** (25 min + 2 weken capstone)

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
