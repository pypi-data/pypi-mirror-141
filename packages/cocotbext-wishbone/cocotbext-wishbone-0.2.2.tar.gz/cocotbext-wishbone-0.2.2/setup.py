import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cocotbext-wishbone",
    version="0.2.2",
    author="Staf Verhaegen, Mathias Kreider",
    author_email="staf@stafverhaegen.be, m.kreider@gsi.de",
    description="Cocotb extension Wishbone module",
    long_description="Cocotb extension Wishbone module",
    packages=["cocotbext.wishbone"],
    install_requires=['cocotb>=1.6.0', 'cocotb_bus'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Electronic Design Automation (EDA)",
    ],
)
