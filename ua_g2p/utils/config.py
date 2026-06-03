# Словник відображення йотованих букв до їх звуків
JOTTED_MAP = {
    "я": "а",
    "ю": "у",
    "є": "е",
    "ї": "і"
}

# Словник відображення літер до їхніх назв
LETTERS_NAME = {
    "б": "бе",
    "в": "ве",
    "г": "ге",
    "ґ": "ґе",
    "д": "де",
    "ж": "же",
    "з": "зе",
    "к": "ка",
    "л": "ел",
    "м": "ем",
    "н": "ен",
    "п": "пе",
    "р": "ер",
    "с": "ес",
    "т": "те",
    "ф": "еф",
    "х": "ха",
    "ц": "це",
    "ч": "че",
    "ш": "ша",
    "щ": "ща"
}

# Набір енклітиків
ENCLITICS = {
    "б",
    "би",
    "ж",
    "же",
    "бо",
    "но",
    "то",
    "таки"
}

# Словник відображення літер до позначуваних звуків
CONVERSION_MAP = {
    "щ": "шч",
    "дж": "д͡ж",
    "дз": "д͡з"
}

# Словник відображення приголосних до їхніх вокалізованих відповідників
VOCALIZED_MAP = {
    "в": "ў",
    "j": "ĭ"
}

# Словник відображення голосних до їхніх назалізованих відповідників
NASALIZED_MAP = {
    "а": "ã",
    "у": "ỹ",
    "о": "õ",
    "е": "ẽ",
    "і": "ĩ",
    "и": "ũ",
    "": ""
}

# Словник відображення результатів асиміляції за дзвінкістю
VOICE_ASSIMILATION_MAP = {
    "ц": "д͡з",
    "к": "ґ",
    "ш": "ж",
    "х": "г", 
    "п": "б",
    "ч": "д͡ж",
    "с": "з",
    "т": "д"
}

# Словник відображення результатів асиміляції за способом творення
WOP_ASSIMILATION_MAP = {
    "д": "д͡з",
    "т": "ц"
}

# Словник відображення результатів асиміляції за способом творення
POPWOP_ASSIMILATION_MAP = {
    "д": "д͡ж",
    "т": "ч",
    "з": "ж",
    "с": "ш",
    "д͡з": "д͡ж",
    "ц": "ч",
    "ж": "з",
    "ш": "с",
    "д͡ж": "д͡з",
    "ч": "ц"
}

# Словник відображення пунктуаційних знаків до позначок паузи
PUNCTUATION_TO_PAUSES_MAP = {
    "\"": "",
    " '": "",
    "' ": "",
    "«": "",
    "»": "",
    "“": "",
    "”": "",
    "„": "",
    ",": " |",
    "(": "| ",
    ")": " |",
    "–": "|",
    "—": "|",
    " - ": " | ",
    ".": " ||",
    ":": " ||",
    ";": " ||",
    "!": " ||",
    "?": " ||"
}

# Набір правил для транскрибування
RULES = {
    r"([ауоеіиїєяюьj']\u0301?|\b)([яюєї])": lambda x: x.group(1) + "j" + JOTTED_MAP[x.group(2)], # jotted letters marking 2 sounds
    r"'": r"", # clear the apostrophes
    r"й": r"j", # replace Й with J
    r"([цншзрлджст])([яюєї])": lambda x: x.group(1) + "'" + JOTTED_MAP[x.group(2)], # jotted letters marking 1 sound, palatalised
    r"([бпвмфчґкхг])([яюєї])": lambda x: x.group(1) + "ߴ" + JOTTED_MAP[x.group(2)], # jotted letters marking 1 sound, half-palatalised
    r"([ауоеіиїєяю]\u0301?|\b)([вj])([цкнгшзхфвпрлджчсмтбґj]|\b)": lambda x: x.group(1) + VOCALIZED_MAP[x.group(2)] + x.group(3), # vocalized consonants
    r"((?:(?:по|с)?пі|(?:по)?на|(?:ві|о)|пе?ре)д)([жз])": r"\1/\2", # segment affricates
    r"(щ|д[жз])": lambda x: CONVERSION_MAP[x.group(1)], # convert Щ, ДЖ and ДЗ letters to corresponding sounds
    r"/": r"", # clear segmentation
    r"([аоуеіи])(\u0301?)([нм])": lambda x: NASALIZED_MAP[x.group(1)] + x.group(2) + x.group(3), # regressive nasalization
    r"([нм]'?)([аоуеіи]?)": lambda x: x.group(1) + NASALIZED_MAP[x.group(2)], # progressive nasalization
    r"([дтзсцлнр])([ьіĩ])": r"\1'\2", # palatalization
    r"([бпвмфґгкхшчж])([ьіĩ])": r"\1ߴ\2", # half palatalization
    r"ь": r"", # clear the softness signs
    r"(запjа́|хва)стн": r"\1t", # reduction exceptions
    r"(с|н)т(ч|ц'|н|д|с)": r"\1\2", # consonant reduction
    r"(?<!шߴі)сс(?!о́т)": r"с", # consonant contraction
    r"t": r"стн", # restore reduction exceptions
    r"([бпвмфґкхшчжгдтзсцлнрj])(['ߴ]?)([оõуỹ])": r"\1\2°\3", # labialisation
    r"([цкшхпчст])('?)([гзджбґ])": lambda x: VOICE_ASSIMILATION_MAP[x.group(1)] + x.group(2) + x.group(3), # voice assimilation
    r"(ле|в°?о|(?:кߴі|н'[ĩі])|д'°?о)(\u0301?)г(к|т)": r"\1\2х\3", # voicelessness assimilation - exceptions
    r"^(з)([цкшхфпчст])": r"с\2", # voicelessness assimilation
    r"т'с'а$": r"ц':а", # way of producing assimilation - verbs
    r"([дт])('?)([зсц]|д͡з)": lambda x: WOP_ASSIMILATION_MAP[x.group(1)] + x.group(2) + x.group(3), # way of producing regressive assimilation
    r"цс'": r"ц'", # way of producing progressive assimilation
    r"([дт])('?)([жшч]|д͡ж)": lambda x: POPWOP_ASSIMILATION_MAP[x.group(1)] + x.group(2) + x.group(3), # place of producing and way of producing assimilation
    r"([зсц]|д͡з)('?)([жшч]|д͡ж)": lambda x: POPWOP_ASSIMILATION_MAP[x.group(1)] + x.group(2) + x.group(3),
    r"([жшч]|д͡ж)('?)([зсц]|д͡з)": lambda x: POPWOP_ASSIMILATION_MAP[x.group(1)] + x.group(2) + x.group(3),
    r"([дтнлзсц]|д͡з)([дтнлзсц]|д͡з)'": r"\1'\2'", # softness assimilation
    r"(бб|пп|вв|мм|фф|ґґ|кк|хх|шш|чч|(?<!д͡)жж|гг|д'?д|т'?т|(?<!д͡)з'?з|с'?с|ц'?ц|л'?л|н'?н|рр|jj|д͡жд͡ж|д͡зд͡з)([ߴ'°]*)": lambda x: f"{x.group(1)[:1]}{x.group(2)}:", # sound lengthening
    r"([оõ])((?:[^аоуеиі]*)(?:[уі]\u0301))": r"\1ʸ\2", # O assimilation
    r"([аоуеãõỹẽ])(\u0301?)(j|\w'|д͡з')": r"\1\2·\3", # regressive I type articulation
    r"([j'][:°]*)([аоуеãõỹẽ])": r"\1·\2", # progressive I type articulation
    r"([еẽ])(?!\u0301|\b)": r"\1ᴻ", # E to И reduction
    r"·([еẽ])ᴻ·": r"·\1ⁱ·", # E to I reduction
    r"([иũ])(?!\u0301|\b)": r"\1ᵉ", # И to Е reduction
    r"ũ": "и\u0303", # formatting
    r"і\u0301": r"í"
}

# Правила, що повторюються, для симуляції складних явищ у мовленні
POST_PROCESS = {
    r"([цкшхпчст])('?)([гзджбґ])": lambda x: VOICE_ASSIMILATION_MAP[x.group(1)] + x.group(2) + x.group(3), # voice assimilation
    r"^(з)([цкшхфпчст])": r"с\2", # voicelessness assimilation
    r"т'с'а$": r"ц':а", # way of producing assimilation - verbs
    r"([дт])('?)([зсц]|д͡з)": lambda x: WOP_ASSIMILATION_MAP[x.group(1)] + x.group(2) + x.group(3), # way of producing regressive assimilation
    r"цс'": r"ц'", # way of producing progressive assimilation
    r"([дт])('?)([жшч]|д͡ж)": lambda x: POPWOP_ASSIMILATION_MAP[x.group(1)] + x.group(2) + x.group(3), # place of producing and way of producing assimilation
    r"([зсц]|д͡з)('?)([жшч]|д͡ж)": lambda x: POPWOP_ASSIMILATION_MAP[x.group(1)] + x.group(2) + x.group(3),
    r"([жшч]|д͡ж)('?)([зсц]|д͡з)": lambda x: POPWOP_ASSIMILATION_MAP[x.group(1)] + x.group(2) + x.group(3),
    r"([дтнлзсц]|д͡з)([дтнлзсц]|д͡з)'": r"\1'\2'" # softness assimilation
}

# Перетворення у фонематичну транскрипцію
PHONEMES_MAP = {
    r"[ߴ°·\u0303]": r"",
    r"ã": r"а",
    r"õ": r"о",
    r"ỹ": r"у",
    r"ẽ": r"е",
    r"ĩ": r"і",
    r"[jĭ]": r"й",
    r"ў": r"в",
    r"і\u0301": r"í"
}

# Перетворення з символів МФА на українську
IPA_TO_UA = {
    r"ˌ": "",
    r"ː": "",
    r"ɑ": "а",
    r"æ": "е",
    r"ʌ": "а",
    r"ə": "е",
    r"ɔ": "о",
    r"aʊ": "ау",
    r"aɪ": "ай",
    r"b": "б",
    r"tʃ": "ч",
    r"d": "д",
    r"ð": "з",
    r"ɛ": "е",
    r"ɝ": "ер",
    r"ɚ": "ер",
    r"eɪ": "ей",
    r"f": "ф",
    r"g": "ґ",
    r"h": "г",
    r"ɪ": "и",
    r"i": "і",
    r"dʒ": "дж",
    r"k": "к",
    r"l": "л",
    r"m": "м",
    r"n": "н",
    r"ŋ": "н",
    r"oʊ": "оу",
    r"ɔɪ": "ой",
    r"p": "п",
    r"r": "р",
    r"ɹ": "р",
    r"s": "с",
    r"ʃ": "ш",
    r"t": "т",
    r"θ": "т",
    r"ʊ": "у",
    r"u": "у",
    r"v": "в",
    r"w": "в",
    r"j": "й",
    r"z": "з",
    r"ʒ": "ж",
    r"y": "й",
    r"x": "кс"
}

# Перетворення кирилиці у символи МФА
TO_IPA = {
    "í": "i\u0301",
    r"[ᵉᴻⁱ°ʸ·\u0303]": r"",
    r"ã": r"ɑ",
    r"õ": r"o",
    r"ỹ": r"u",
    r"ẽ": r"ɛ",
    r"ĩ": r"і",
    r"ў": r"в",
    r"і": r"i",
    r"и": r"ɪ",
    r"ĭ": r"j",
    r"е": r"ɛ",
    r"у": r"u",
    r"о": r"o",
    r"а": r"ɑ",
    r"м": r"m",
    r"н": r"n",
    r"п": r"p",
    r"б": r"b",
    r"т": r"t",
    r"д": r"d",
    r"к": r"k",
    r"ґ": r"g",
    r"в": r"v",
    r"ф": r"f",
    r"с": r"s",
    r"з": r"z",
    r"ш": r"ʃ",
    r"ж": r"ʒ",
    r"х": r"x",
    r"г": r"ɦ",
    r"ц": r"ʦ",
    r"д͡з": r"ʣ",
    r"ч": r"ʧ",
    r"д͡ж": r"ʤ",
    r"р": r"r",
    r"л": r"ɫ",
    r"ɫ'": r"lʲ",
    r"'": r"ʲ",
    r"ߴ": r"ʲ",
    r":": r"ː",
    r"\u0301": r"ˈ"
}