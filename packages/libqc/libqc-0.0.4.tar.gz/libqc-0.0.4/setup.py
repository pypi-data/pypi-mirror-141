from setuptools import setup

setup(
    name="libqc",
    version="v0.0.4",
    author_email="kenny@latch.bio",
    description="sgRNA Library QC",
    packages=["libqc"],
    package_data={"libqc": ["lib/*"]},
)
