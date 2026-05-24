import re
from typing import Literal
from ua_g2p.utils.config import LETTERS_NAME, PUNCTUATION_TO_PAUSES_MAP, ENCLITICS
from ua_g2p.utils.text_utils import Stressifier, UkrainianStressifier, StressDisambiguator, count_syllables

class PreprocessorG2P():
    """
    Tool to preprocess the text. It handles:
        -numerical numbers
        -acronyms
        -special symbols
        -non-cyrillic characters
        -tokenization
        -enclytics and proclytics
    """
    def __init__(self, accentor: Literal["dictionary", "transformer", "hybrid"] = "dictionary"):
        if accentor == "dictionary":
            self.accentor = Stressifier(stress_symbol="\u0301")
        elif accentor == "transformer":
            self.accentor = UkrainianStressifier()
        elif accentor == "hybrid":
            self.accentor = StressDisambiguator()
        else:
            raise ValueError(f"Invalid accentor: '{accentor}'. Expected one of: 'dictionary', 'transformer', 'hybrid'.")
        
    def stressify_text(self, text):
        if type(self.accentor) in [Stressifier, StressDisambiguator]:
            return self.accentor(text)
        else:
            return self.accentor.apply_stress_marks(text).replace("+", "\u0301")

    def handle_numbers(self, text: str) -> str:
        return text
    
    def handle_acronyms(self, text: str) -> str:
        def acronym_to_word(match):
            word = ""
            acronym = match.group().casefold()
            if re.search(
                r"сша|змі|[цкнгшщзхфвпрлджчсмтб]+[уеїіаоєяию]+[цкнгшщзхфвпрлджчсмтб]+",
                acronym
            ):
                word = acronym
            else:
                for char in acronym:
                    if char in LETTERS_NAME:
                        word += LETTERS_NAME[char]
                    else:
                        word += char
            
            return word
        
        to_sound = re.sub(
            r"(?<=\b)(?:[А-ЯҐЄЇІ]{2,}|[цкнгшщзхфвпрлджчсмтб]{2,})(?=\b)",
            acronym_to_word,
            text
        )

        return to_sound

    def clean_text(self, text: str) -> str:
        clean = text.strip()
        junk = ["*№#^&`₴$@_"]
        for item in junk:
            clean = clean.replace(item, "")
        clean = self.handle_acronyms(clean).casefold()
        stressed = self.stressify_text(clean)
        
        return stressed.replace("+", "\u0301")
    
    def tokenize_words(self, text: str) -> list:
        punct_to_pauses = re.sub(
            r"(\"|\s'|'\s|,|\(|\[|\)|\]|—|\s\-\s|\.|;|!|\?)",
            lambda x: PUNCTUATION_TO_PAUSES_MAP[x.group(1)],
            text
        )
        text = re.sub(r"(?<!\s)-(?!\s)", " ", punct_to_pauses)
        token_list = text.split(" ")
        while "|" in token_list[-1]:
            token_list.pop(-1)
        while "|" in token_list[0]:
            token_list.pop(0)
        return token_list

    def _concat_enclit(self, tokens: list) -> list:
        handled = []
        n = len(tokens)
        i = 0
    
        while i < n:
            w_i = tokens[i]
    
            if w_i.replace("\u0301", "") in ENCLITICS and i != 0 and "|" not in tokens[i-1]:
                i += 1
                continue
            elif "|" in w_i:
                i+=1
                handled.append(w_i)
                continue
            
            if i < n - 1 and tokens[i+1].replace("\u0301", "") in ENCLITICS:
                j = i + 1
                concatenation = w_i
    
                while j < n and tokens[j].replace("\u0301", "") in ENCLITICS:
                    concatenation += tokens[j].replace("\u0301", "")
                    j += 1
    
                handled.append(concatenation)
                i = j
            else:
                handled.append(w_i)
                i += 1
    
        return handled
        
    def _concat_proclit(self, tokens: list) -> list:
        r_tokens = tokens[::-1]
        handled = []
        n = len(r_tokens)
        i = 0

        while i < n:
            w_i = r_tokens[i]

            if "|" in w_i:
                handled.append(w_i)
                i += 1
                continue
            
            if i < n - 1 and count_syllables(r_tokens[i+1]) < 2 and "|" not in r_tokens[i+1]:
                j = i + 1
                while j < n and count_syllables(r_tokens[j]) < 2 and "|" not in r_tokens[j]:
                    j += 1

                proclitic = "".join(r_tokens[i+1:j][::-1])
                concatenation = proclitic.replace("\u0301", "") + w_i

                handled.append(concatenation)
                i = j
            else:
                handled.append(w_i)
                i += 1

        return handled[::-1]
    
    def handle_clitics(self, tokens: str) -> str:
        return self._concat_proclit(self._concat_enclit(tokens))

    def preprocess_text(self, text: str) -> list:

        text = self.clean_text(text)
        tokens = self.tokenize_words(text)
        result = self.handle_clitics(tokens)

        return result