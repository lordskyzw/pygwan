from setuptools import setup, find_packages

setup(
    name="pygwan",
    version="0.1.6",
    packages=find_packages(),
    description="WhatsApp Cloud API is complicated, Twilio is expensive, PyGwan is the opposite of both. Free & Intuitive! ~ Tarmica Chiwara.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author="Tarmica Chiwara",
    author_email="tarimicac+pypi@gmail.com",
    license="MIT",
    url="https://github.com/lordskyzw/pygwan",
    install_requires=[
        "requests>=2.25.0",
        "colorama>=0.4.3",
        "requests_toolbelt>=0.9.1"
    ],
)
