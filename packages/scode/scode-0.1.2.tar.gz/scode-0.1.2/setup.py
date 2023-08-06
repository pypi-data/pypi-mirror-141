import setuptools
import scode
with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="scode", # Replace with your own username
    version=scode.__version__,
    author="강동욱, 선준우, 강진영, 박태준, 김도현",
    maintainer = '강동욱',
    maintainer_email="ehddnr2981@gmail.com",
    description="The Private Package of Showm Company.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/showm-dev/Standard",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
    ],
    python_requires='>=3.6',
    install_requires = [
        "selenium==3.141.0",
        "telegram==0.0.1",
        "paramiko==2.7.2",
        "dropbox==11.19.0"
        ]
)