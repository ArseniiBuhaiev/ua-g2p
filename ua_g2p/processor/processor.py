import re
from typing import Literal
from ua_g2p.utils.config import RULES, POST_PROCESS, PHONEMES_MAP, TO_IPA
from ua_g2p.preprocessor.preprocessor import PreprocessorG2P
from ua_g2p.utils.text_utils import shift_stress

class ProcessorG2P():
    """
    A G2P tool to convert orthographic text into phonetic, phonematic and IPA transcriptions.

    This class acts as a callable object. When called, it processes the input 
    string and returns its transcription based on the selected mode.

    Example:
        >>> transcribe = ProcessorG2P()
        >>> result = transcribe("Гарна погода!", mode="ipa", brackets=True)
        "[ˈɦɑrnɑ poˈɦodɑ]"
    """

    def _to_phones(
            self,
            text: str,
            accentor: Literal["dictionary", "transformer", "hybrid"] = "dictionary",
            brackets: bool = True
    ) -> str:
        """
        Transcribes the text phonetically following the ruleset.

        Args:
            text (str): Orthographic text in Ukrainian.
            brackets (bool): Enclose the output in brackets.
        Returns:
            str: Cyrillic phonetical transcription of the input text.
        """
        prep = PreprocessorG2P(accentor=accentor)
        text = prep.preprocess_text(text)
        transcription = ""

        def apply_set(rules, text):
            for rule, replacement in rules.items():
                text = re.sub(rule, replacement, text)
            return text

        for word in text:
            word = apply_set(RULES, word)
            post = apply_set(POST_PROCESS, word)
            while post != word:
                word = post
                post = apply_set(POST_PROCESS, word)
            transcription += f"{word} "

        if brackets:
            return f"[{transcription.strip()}]"
        else:
            return transcription.strip()
    
    def _to_phonemes(self, text: str, accentor: Literal["dictionary", "transformer", "hybrid"] = "dictionary", brackets: bool = True) -> str:
        """
        Transcribes the text phonematically following the ruleset.

        Args:
            text (str): Orthographic text in Ukrainian.
            brackets (bool): Enclose the output in brackets.
        Returns:
            str: Cyrillic phonematical transcription of the input text.
        """
        transcription = self._to_phones(text, accentor, brackets=False)

        for rule, replacement in PHONEMES_MAP.items():
            transcription = re.sub(rule, replacement, transcription)

        if brackets:
            return f"/{transcription}/"
        else:
            return transcription
        
    def _to_ipa(self, text: str, accentor: Literal["dictionary", "transformer", "hybrid"] = "dictionary", brackets: bool = True) -> str:
        """
        Transcribes the text according to IPA standards following the ruleset.

        Args:
            text (str): Orthographic text in Ukrainian.
            brackets (bool): Enclose the output in brackets.
        Returns:
            str: IPA transcription of the input text.
        """

        transcription = self._to_phones(text, accentor, brackets=False)

        for rule, replacement in TO_IPA.items():
            transcription = re.sub(rule, replacement, transcription)

        if brackets:
            return f"[{shift_stress(transcription)}]"
        else:
            return shift_stress(transcription)
        
    def __call__(
            self,
            text: str,
            accentor: Literal["dictionary", "transformer", "hybrid"] = "dictionary",
            mode: Literal["phonetic", "phonematic", "ipa"] = "ipa",
            brackets: bool = False
    ) -> str:
        """
        Transcribes the input Ukrainian text into the specified representation.

        Args:
            text (str): Orthographic text in Ukrainian.
            mode (Literal["phonetic", "phonematic", "ipa"]): Transcription type (phonetic, phonematic or ipa).
                "phonetic": Detailed allophonic transcription in cyrillic.
                "phonematic": Phonematic notation in cyrillic.
                "ipa": International Phonetic Alphabet notation.
                Defaults to "ipa".
            brackets (bool): Whether to enclose the output in appropriate brackets.
                (e.g., [ ] for phonetic and IPA, / / for phonematic).
                Defaults to False
        
        Returns:
            str: The transcription of input text in the requested format.

        Example:
            >>> transcribe = ProcessorG2P()
            >>> transcribe("Гарна погода!")
            "ˈɦɑrnɑ poˈɦodɑ"
            >>> transcribe("Гарна погода!", mode="phonetic", brackets=True)
            "[га́рнã п°ог°о́да]"
        """
        if mode == "phonetic":
            return self._to_phones(text=text, accentor=accentor, brackets=brackets)
        elif mode == "phonematic":
            return self._to_phonemes(text=text, accentor=accentor, brackets=brackets)
        elif mode == "ipa":
            return self._to_ipa(text=text, accentor=accentor, brackets=brackets)
        else:
            raise ValueError(f"Invalid mode: '{mode}'. Expected one of: 'phonetic', 'phonematic, 'ipa'.")