from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = ["django>=3.0", "pyTelegramBotAPI>=4.4.0"]

setup(
    name="django-tg-logs",
    version="0.0.2",
    author="Inkviz96",
    author_email="b-semen-b@mail.ru",
    description="A package to convert your Jupyter Notebook",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/inkviz96/django-tg-logs",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
)