"""Setup tilebench."""

from setuptools import find_packages, setup

with open("README.md") as f:
    long_description = f.read()

inst_reqs = [
    "aiofiles",
    "fastapi>=0.73",
    "jinja2>=3.0,<4.0.0",
    "geojson-pydantic",
    "loguru",
    "rasterio",
    "rio-tiler>=3.1,<4.0",
    "wurlitzer",
    "uvicorn[standard]>=0.12.0,<0.16.0",
]
extra_reqs = {
    "test": ["pytest", "pytest-cov", "pytest-asyncio"],
    "dev": ["pytest", "pytest-cov", "pytest-asyncio", "pre-commit"],
}


setup(
    name="tilebench",
    description=u"Inspect HEAD/LIST/GET requests withing Rasterio",
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires=">=3.7",
    keywords="",
    author=u"Vincent Sarago",
    author_email="vincent@developmentseed.org",
    url="https://github.com/developmentseed/tilebench",
    classifiers=[
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.7",
        "Topic :: Scientific/Engineering :: GIS",
    ],
    license="MIT",
    packages=find_packages(exclude=["tests*"]),
    include_package_data=True,
    zip_safe=False,
    install_requires=inst_reqs,
    extras_require=extra_reqs,
    entry_points={
        "console_scripts": [
            "tilebench=tilebench.scripts.cli:cli",
        ],
    },
)
