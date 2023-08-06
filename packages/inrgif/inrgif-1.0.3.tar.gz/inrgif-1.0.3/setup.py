from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="inrgif",
    version="1.0.3",
    description="A Python package to make gif from images and videos",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/jyotiprakash-work/inrgif.git",
    author="jyotiprakash panigrahi",
    author_email="jyotiprakash.work@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    packages=["inrgif"],
    include_package_data=True,
    install_requires=["opencv-python","scikit-learn", "Pillow"],
    entry_points={
        "console_scripts": [
            "",
        ]
    },
)