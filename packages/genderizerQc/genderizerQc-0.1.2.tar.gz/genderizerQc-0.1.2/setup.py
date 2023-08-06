from setuptools import setup, find_packages


setup(
    name="genderizerQc",
    version="0.1.2",
    url="https://github.com/jaytouz/genderizeQc",
    author="Jérémie Tousignant",
    author_email="tousijer@gmail.com",
    python_requires=">=3.6",
    packages=find_packages(where='src', exclude=[
                           "tests", "*.tests", "*.tests.*", "tests.*"]),
    package_dir={'': 'src'},
    install_requires=[
        "pandas>=1.4.0",
    ],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
    ],
    include_package_data=True,
    package_data={'': ['./data/*.csv']},
)
