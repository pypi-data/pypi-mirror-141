from setuptools import setup

setup(
    name="gunes-ustunalp-dictionary",
    author="Asım Güneş Üstünalp",
    version="2.0.0",
    packages=["dictionary"],
    install_requires=[
        "requests>=2.23.0",
    ],
    python_requires=">=3.8",

)
