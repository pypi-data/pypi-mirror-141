from setuptools import setup, find_packages

setup(
    name='python-example-package',
    version='0.1',
    license='MIT',
    author='Juan Talamante',
    author_email='juantarrel@gmail.com',
    packages=find_packages('src'),
    packages_dir={'': 'src'},
    url='https://github.com/juantarrel/python-package-test',
    keywords='example package',
    install_requires=[
        'scikit-learn',
    ],
)
