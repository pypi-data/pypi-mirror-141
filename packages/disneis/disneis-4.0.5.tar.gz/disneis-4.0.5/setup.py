import os

import setuptools

requirements = []

path = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/")
with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setuptools.setup(
    name="disneis",
    version="4.0.5",
    license="MIT",
    author="花 ༉ ָ࣪네먀ℓ•₯ζ°²#0919",
    author_email="dofiya6199@xindax.com",
    description="나이스 api를 이용한 파이썬 모듈입니다.",
    long_description=open("README.md", "rt", encoding="UTF8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/disocord/neispy",
    package_data={"disneis": ["py.typed"]},
    packages=setuptools.find_packages(),
    install_requires=requirements,
    classifiers=[
        # 패키지에 대한 태그
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
