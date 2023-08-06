from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='oubihiBasicCalculator',
    version='0.0.1',
    description='A very basic calculator',
    long_description=open('README').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='Abderahhmane Oubihi',
    author_email='abderrahmane.oubihi@edu.uiz.ac.ma',
    license='MIT',
    classifiers=classifiers,
    keywords='calculation',
    packages=find_packages(),
    install_requires=['']
)
