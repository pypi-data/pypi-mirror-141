from setuptools import setup
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()
setup(name='hplib',
version='0.0.2',
description='Database and code to simulate heat pumps',
long_description=long_description,
long_description_content_type='text/markdown',
py_modules=['hplib'],
package_dir={'hplib':'src'},
package_data={'hplib': ['src/hplib-database.py']}
)
