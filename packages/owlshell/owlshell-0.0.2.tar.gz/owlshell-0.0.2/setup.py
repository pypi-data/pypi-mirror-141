import setuptools
setuptools.setup(
    name="owlshell",
    version="0.0.2",
    author="Sovenok-Hacker",
    author_email="artemka.hvsotov@yandex.ru",
    description="A tool to use the OS functions and SEE AN ASCII ART OWL!",
    url="https://github.com/Sovenok-Hacker/owlshell",
    package_dir={"": "owlshell"},
    packages=setuptools.find_packages(where="owlshell"),
    python_requires=">=3.6",
)
