import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="aplicacion-ejemplo-kc",
    version="0.0.1",
    author="Marta Arcones",
    author_email="marta.arcones@gmail.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.9",
    install_requires=[
       'coloredlogs',
   ],
)