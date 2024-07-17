from setuptools import setup, find_packages

setup(
    name="pygwan",
    version="0.1.3",
    packages=find_packages(),
    description="We are so very very back! This is my very own python sdk for the whatsapp cloud api",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author="Tarmica Sean Chiwara",
    author_email="tarimicac+pypi@gmail.com",
    license="MIT",
    url="https://github.com/lordskyzw/pygwan",
    install_requires=[
        "requests>=2.25.0",
        "colorama>=0.4.3",
        "requests_toolbelt>=0.9.1"
    ],
)
