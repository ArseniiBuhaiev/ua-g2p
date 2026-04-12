# Ukrainian G2P
A robust rule-based G2P (Grapheme-to-Phoneme) tool designed specifically for the Ukrainian language. This tool automates complex phonetic transformations, ensuring high-quality transcriptions for NLP and TTS tasks, and linguistic research.

## Key Features
- **Linguistic Precision:** Handles abbreviations, pausation, and clitics.
- **Stress Management:** Resolves ambiguous stress using dictionary and transformer-based models.
- **Multiple Output Formats:** Supports three phonetic representations:
  - *Phonetic* (narrow transcription)
  - *Phonematic* (broad transcription)
  - *IPA* (International Phonetic Alphabet)

## Quickstart
Install using:
```bash
pip install git+https://github.com/ArseniiBuhaiev/ua-g2p.git
```
Code example:
```python
from ua_g2p import ProcessorG2P

transcribe = ProcessorG2P()
result = transcribe(
    "Гарна погода!",
    accentor="hybrid", # dictionary, transformer, or hybrid
    mode="ipa",        # phonetic, phonematic, or ipa
    brackets=True
)

print(result)

>>> [ˈɦɑrnɑ poˈɦodɑ]
```

## Acknowledgements
Special thanks to *[lang-uk group](https://github.com/lang-uk)* for their tokenization and stress handling tools:
* [tokenize-uk](https://github.com/lang-uk/tokenize-uk) robust tokenization algorithm
* [ukrainian-word-stress](https://github.com/lang-uk/ukrainian-word-stress) dictionary-based stress handling
* [ukrainian-tts-preprocessing](https://github.com/lang-uk/ukrainian-tts-preprocessing) transformer-based stress handling