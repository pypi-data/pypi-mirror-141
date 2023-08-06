import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="smolog",
    version="0.0.1",
    author="Mateusz Bednarski",
    author_email="msz.bednarski@gmail.com",
    description="Smol log pkg in python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
    py_modules=["smolog"],
    package_dir={'': 'smolog/src'},
)
