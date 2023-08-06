from setuptools import setup

with open("README.md", "r") as f:
    page_description = f.read()

setup(
    name='img_convert',
    version='0.0.1',
    description = 'Projeto para conversao de imagem RGB.',
    long_description=page_description,
    long_description_content_type="text/markdown",
    packages=['img_convert', 'img_convert.utils'],
    url='https://github.com/ceconelo',
    license='MIT',
    author='Thiago Oliveira',
    author_email='thiceconelo@gmail.com',
    install_requires=[
        'opencv-python',
        'numpy'
    ],
)
