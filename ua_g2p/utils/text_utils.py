import re
import regex
from typing import Literal
from num2words import num2words
from tokenize_uk import tokenize_words
from ukrainian_word_stress import Stressifier
from ua_text_stressifier import UkrainianStressifier

def _reconstruct_text(tokens: list) -> str:
    text = " ".join(tokens)

    text = re.sub(r'(["«„\(\[\{]) ([^"«„»“\(\)\[\]\{\}]+) (["»“\)\]\}])', r"\1\2\3", text)
    text = re.sub(r'([^\.\:\,\;\!\?\*\%]+) ([\.\:\,\;\!\?\*\%])', r"\1\2", text)

    return text.rstrip()

VOWELS = "аоуеиіяюєї"
VOWELS += VOWELS.upper()

def count_syllables(word: str) -> int:
    return sum(1 for ch in word if ch in VOWELS)

def syllabify(text: str, mode: Literal["default", "ipa"] = "default", to_list: bool = True) -> list[str]|str:
    """
    Syllabifies the given text in Ukrainian.

    Args:
        text (str): Input text in Ukrainian.
        mode (Literal["default", "ipa"]): How to represent the word.
        to_list (bool): What object to return.
    Returns:
        list[str]|str: List of syllables in the text or a str instance with separators between syllables.
    """
    if mode == "default":
        V = r"[аоуеіияюєї]"
        C = r"дз|дж|[ймнпбтвкґвфсзшжхгцчкл]|д(?![жз])"
        CV = r"дз|дж|[бґзжг]|д(?![жз])"
        CUV = r"[пткфсшхцч]"
        CN = r"дз|дж|[бґзжгпткфсшхцч]|д(?![жз])"
        CS = r"[ймнврл]"
    elif mode == "ipa":
        V = r"[ɑouɛiɪ]ˈ?"
        C = r"[jmnpbtdkgvfszʃʒxɦʦʣʧʤrɫl]ʲ?ː?"
        CV = r"[bdgzʒɦʣʤ]ʲ?ː?"
        CUV = r"[ptkfsʃxʦʧ]ʲ?ː?"
        CN = r"[bdgzʒɦʣʤptkfsʃxʦʧ]ʲ?ː?"
        CS = r"[jmnvrɫl]ʲ?ː?"
    else:
        raise ValueError(f"Invalid mode: '{mode}'. Expected one of: 'default', 'ipa'.")
    
    SYLLABIFICATION = {
        rf"(?<={V})({C})(?={V})": r"-\1",
        rf"(?<={V})((?:{CV}){{2}}|(?:{CUV}){{2}})(?=.*(?:{V})*.*)": r"-\1",
        rf"(?<={V})()((?:{CV}){{2}}|(?:{CUV}){{2}})(?={CS})": r"-\1",
        rf"(?|({CS}|{CV})({CUV})|({CS})({CV}))": r"\1-\2",
        rf"(?<={V}(?:{CS}))((?:{C})+)(?={V})": r"-\1",
        rf"(?<={V})({CN}{CS}(?:{C})?)(?={V})": r"-\1",
        rf"(?<={V}{CS})({CS})(?!=\b)": r"-\1"
    }

    for rule, separation in SYLLABIFICATION.items():
        text = regex.sub(rule, separation, text)

    if not to_list:
        return text
    else:
        return regex.sub(r"\s", "-", text).split("-")

def shift_stress(text: str) -> str:
    """
    Shifts stress mark according to the IPA standards (before the stressed syllable)

    Args:
        text (str): Transcribed text.
    Returns:
        str: Transcribed text with shifted stress. 
    """

    text = syllabify(text, mode="ipa", to_list=False)

    shifted_stress = regex.sub(
        r"(?<=\-|\b)([^-]*ˈ[^-]*)(?=\-|\b)",
        lambda x: f"ˈ{x.group().replace('ˈ', '')}",
        text
    ).replace("-", "")

    return(shifted_stress)

class StressDisambiguator():
    """
    A tool to help distinguish heteronyms when using dictionary-based approach in stressing words
    by using transformer-based approach.
    """
    def __init__(self):
        self.dict_method = Stressifier(stress_symbol="\u0301")
        self.transformer_method = UkrainianStressifier()
    
    def _get_options(self, text) -> list[tuple]:
        dict_method = tokenize_words(self.dict_method(text))
        transformer_method = tokenize_words(self.transformer_method.apply_stress_marks(text).replace("+","\u0301"))

        probable_stress = list(zip(dict_method, transformer_method))

        return probable_stress

    # def _approximate(self, word: str) -> str:
    #     if len(word) >= 2:
    #         syllables = syllabify(word.casefold())
    #         syllables[-2] = re.sub(fr"([{self.VOWELS}])", r"\1" + "\u0301", syllables[-2])

    #         word = "".join(syllables)

    #         return word
    #     else:
    #         return word

    def _choose_stress(self, pairs) -> str:
        tokens = []

        for pair in pairs:
            if not pair[0].isalpha() and len(pair[0]) == 1:
                tokens.append(pair[0])
            else:
                use_dict = pair[0].count("\u0301") == 1
                use_transformer = not use_dict and "\u0301" in pair[1]
                monosyllabic = count_syllables(pair[0]) == 1 and "\u0301" not in pair[1]
                # no_auto_stress = "\u0301" not in pair[0] and "\u0301" not in pair[1]
                # assume_second_last = not monosyllabic and no_auto_stress

                if use_dict:
                    tokens.append(pair[0])
                elif use_transformer:
                    tokens.append(pair[1])
                elif monosyllabic:
                    manual = re.sub(r"([аоуеиіяюєїАОУЕИІЯЮЄЇ])", r"\1" + "\u0301", pair[0])
                    tokens.append(manual)
                # elif assume_second_last:
                #     approximation = self._approximate(pair[0])
                #     tokens.append(approximation)
                else:
                    tokens.append(pair[0])

        return tokens

    def __call__(self, text: str) -> str:
        """
        Apply stress marks to Ukrainian text based on a hybrid approach.

        Args:
            text (str): Input text in Ukrainian.
        Returns:
            str: Text with stress marks.
        """
        options = self._get_options(text)
        tokens = self._choose_stress(options)

        return _reconstruct_text(tokens)