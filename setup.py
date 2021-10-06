import os
import setuptools
from setuptools.command.install import install
from setuptools.command.install_scripts import install_scripts


class InstallWrapper(install):
    def run(self):
        self._postinstall()

    def _postinstall(self):
        install.run(self)
        for filepath in self.get_outputs():
            if self.install_scripts in filepath:
                os.chmod(filepath, 0o755)
            if filepath.endswith('pyapplier.py'):
                os.symlink('/usr/bin/pyapplier.py', '/usr/bin/pyapplier')


with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name='pyapplier',  
    version='0.0.5b',
    scripts=['pyapplier.py'],
    author="Aleksey Kurnosov",
    author_email="akkurnosov@gmail.com",
    description=".scrobbler.log (Rockbox offline last.fm scrobling format) submiter",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ultraelephant/pyapplier",
    packages=setuptools.find_packages(),
    install_requires=[
        'pylast',
        'setuptools',
        'pyaml'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: POSIX :: Linux",
    ],
    cmdclass={'install': InstallWrapper},
 )