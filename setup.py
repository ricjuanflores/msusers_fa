from setuptools import find_packages, setup

setup(
    name='ms_fa',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'fastapi',
        'uvicorn',
        'typer',
    ],
    entry_points={
        'console_scripts': [
            'ms-fa=ms_fa.commands:main',
        ],
    },
)

