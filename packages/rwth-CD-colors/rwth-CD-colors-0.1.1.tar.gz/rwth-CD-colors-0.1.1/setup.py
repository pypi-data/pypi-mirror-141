from setuptools import setup

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='rwth-CD-colors',
    version='0.1.1',
    packages=[''],
    url='',
    license='MIT',
    author='Thomas Offergeld',
    author_email='t.offergeld@iaew.rwth-aachen.de',
    description='Provider for RWTH colormap aliases',
    long_description=long_description,
    long_description_content_type="text/markdown"
)
