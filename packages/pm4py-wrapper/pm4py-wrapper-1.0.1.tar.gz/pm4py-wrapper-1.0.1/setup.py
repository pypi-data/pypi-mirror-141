from setuptools import setup, find_packages

setup(
    name='pm4py-wrapper',
    version='1.0.1',
    packages=find_packages(where='src'),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=[
        'click',
        'pm4py',
        'pandas',
        'pytest',
        'setuptools',
        'pre-commit'
    ],
    entry_points={
        'console_scripts': [
            'pm4py_wrapper = pm4py_wrapper.cli:main',
        ]
    }
)
