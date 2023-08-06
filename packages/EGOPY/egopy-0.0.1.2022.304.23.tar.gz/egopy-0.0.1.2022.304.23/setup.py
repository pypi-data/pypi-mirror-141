"""
EGOPY - Ego your python for quantitative trading.

Only for testing now!

Only for testing now!

Only for testing now!

"""


from setuptools import find_packages, setup


setup(
    name="egopy",
    version="0.0.1.2022.304.23",
    author="egopy",
    author_email="test@egopy.cn",
    license="MIT",
    url="https://www.egopy.cn",
    description="A framework for developing quant trading systems.",
    long_description=__doc__,
    keywords='quant quantitative investment trading algotrading',
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
        "Operating System :: Microsoft :: Windows :: Windows 10",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Cython",
        "Programming Language :: C",
        "Topic :: Office/Business :: Financial",
        "Topic :: Scientific/Engineering :: Mathematics",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: Chinese (Simplified)"
    ]
)
