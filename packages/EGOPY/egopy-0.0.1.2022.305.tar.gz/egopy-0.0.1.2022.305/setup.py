"""
EGOPY - Ego your python for quantitative trading.

Only for testing now!

Only for testing now!

Only for testing now!

"""


from setuptools import find_packages, setup


setup(
    name="egopy",
    version="0.0.1.2022.305",
    author="EGOPY",
    author_email="",
    license="MIT",
    url="https://pypi.org/project/egopy",
    description="A framework for developing quant trading systems.",
    long_description=__doc__,
    keywords='quant investment quantitative trading algotrading',
    include_package_data=True,
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.8",
    package_data={"": [
        "*.ico",
        "*.ini",
        "*.dll",
        "*.so",
        "*.pyd",
    ]},
    classifiers=[
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Programming Language :: Cython",
        "Programming Language :: C",
        "Topic :: Office/Business :: Financial",
        "Topic :: Scientific/Engineering :: Mathematics",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: Chinese (Simplified)"
    ]
)
