import setuptools

with open("README.md", "r", encoding="utf-8") as file:
    long_description = file.read()

setuptools.setup(
    name="thorndyke",
    version="2022.1.2.1",
    author="Richard Mwewa",
    author_email="richardmwewa@duck.com",
    packages=["thorndyke"],
    description="Lightweight username enumeration tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rlyonheart/thorndyke",
    license="GNU General Public License v3 (GPLv3)",
    install_requires=["requests","tqdm"],
    classifiers=[
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',  
        'Operating System :: POSIX :: Linux',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
    ],
    entry_points={
        "console_scripts": [
            "thorndyke=thorndyke.main:Thorndyke",
        ]
    }
)
