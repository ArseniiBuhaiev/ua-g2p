from setuptools import setup, find_packages

setup(
    name="ua-g2p",
    version="1.1",
    description="Rule-based Ukrainian G2P with text preprocessing.",
    author="Arsenii Buhaiev",
    author_email="bugaev3202@ukr.net",
    url="https://github.com/ArseniiBuhaiev/ua-g2p",
    license="CC BY-NC 4.0",
    packages=find_packages(include=("ua_g2p", "ua_g2p.*")),
    python_requires=">=3.9",
    install_requires=[
        "ukrainian_word_stress @ https://github.com/ArseniiBuhaiev/ukrainian-word-stress",
        "ua_text_stressifier @ git+https://github.com/ArseniiBuhaiev/ua-text-stressifier.git",
        "tokenize_uk==0.2.0",
        "english_g2p @ git+https://github.com/ArseniiBuhaiev/english_g2p.git",
        "num2words==0.5.14",
        "pymorphy3==2.0.6",
        "pymorphy3_dicts_uk==2.4.1.1.1663094765",
        "spacy==3.8.14"
    ]
)