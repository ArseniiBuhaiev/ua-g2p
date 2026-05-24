from setuptools import setup, find_packages

setup(
    name="ua-g2p",
    version="1.0",
    description="Rule-based Ukrainian G2P with text preprocessing.",
    author="Arsenii Buhaiev",
    author_email="bugaev3202@ukr.net",
    url="https://github.com/ArseniiBuhaiev/ua-g2p",
    license="CC BY-NC 4.0",
    packages=find_packages(include=("ua_g2p", "ua_g2p.*")),
    python_requires=">=3.9",
    install_requires=[
        "num2words==0.5.14",
        "ukrainian_word_stress==1.1.1",
        "ua_text_stressifier @ git+https://github.com/ArseniiBuhaiev/ua-text-stressifier.git",
        "tokenize_uk==0.2.0"
    ]
)