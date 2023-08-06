from setuptools import setup, find_packages


classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]
setup(
    name='TremorGan',
    author='Anas Ibrahim',
    author_email = 'aibrah43@uwo.ca',
    version='0.0.1',
    description='Generate Tremor data using a Generative Adversarial Network',
    Long_description = open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url = '',
    License='MIT',
    classifiers = classifiers,
    keywords = 'Tremor data generator',
    packages = find_packages(),
    install_requires=['numpy','tensorflow','keras']
)