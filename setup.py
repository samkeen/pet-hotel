import setuptools


with open("README.md") as fp:
    long_description = fp.read()


setuptools.setup(
    name="pet_hotel",
    version="0.0.1",

    description="Demo Flask App",
    long_description=long_description,
    long_description_content_type="text/markdown",

    author="Sam Keen",

    package_dir={"": "pet_hotel"},
    packages=setuptools.find_packages(where="pet_hotel"),

    install_requires=[
        "flask",
        "flask-mysql",
        "wtforms",
        "cryptography",
    ],

    python_requires=">=3.6",

    classifiers=[
        "Development Status :: 4 - Beta",

        "Intended Audience :: Developers",

        "License :: OSI Approved :: MIT License",

        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Typing :: Typed",
    ],
)