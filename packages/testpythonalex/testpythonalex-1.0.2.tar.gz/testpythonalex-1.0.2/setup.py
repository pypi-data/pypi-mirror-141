import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='testpythonalex',
    version='1.0.2',
    author='alexguo247',
    author_email='alexguo247@gmail.com',
    description='Test Python Library',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/alexguo247/cohere-python',
    packages=setuptools.find_packages(),
    install_requires=[
        'requests'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
