"""
EGOPY - Ego your python for trading.

Only for testing now!
Only for testing now!
Only for testing now!

The egopy project is an open-source quantitative trading framework
that is developed by traders, for traders.

The project is mainly written in Python and uses C++ for low-layer
and performance sensitive infrastructure.

Using the egopy project, institutional investors and professional
traders, such as hedge funds, prop trading firms and investment banks,
can easily develop complex trading strategies with the Event Engine
Strategy Module, and automatically route their orders to the most
desired destinations, including equity, commodity, forex and many
other financial markets.
"""

from setuptools import find_packages, setup


setup(
    name="egopy",
    version="0.0.1.2022.304.20",
    author="egopy team",
    author_email="egopy@egopy.cn",
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
        "Topic :: Office/Business :: Financial :: Investment",
        "Programming Language :: Python :: Implementation :: CPython",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: Chinese (Simplified)"
    ]
)
