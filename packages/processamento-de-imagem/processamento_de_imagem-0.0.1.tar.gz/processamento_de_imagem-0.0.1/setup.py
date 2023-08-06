from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="processamento_de_imagem",
    version="0.0.1",
    author="Jhonathan Alves",
    description="Processamento de imagem usando combinação de histograma",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Jhonathanalvesbr/processamento-de-imagem",
    packages=find_packages(),
    package_data = {
        "processamento_de_imagem": ["sample_images/*.jpg"]
    },
    include_package_data = True,
    install_requires=requirements,
    python_requires='>=3.5',
)