import pathlib
import setuptools

long_description = (pathlib.Path(__file__).parent / "README.md").read_text()

with open("requirements.txt", "r") as requirements_file:
    requirements = requirements_file.readlines()


setuptools.setup(
    name='abstractEasyT',
    version='0.2.1',
    license='MIT',
    author="Joao Paulo Euko",
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(),
    install_requires=[requirement for requirement in requirements],
)
