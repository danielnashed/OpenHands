import pathlib
import setuptools
import pkg_resources
import subprocess
import sys

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text(encoding='utf-8')

with pathlib.Path('docs/requirements.txt').open() as requirements_txt:
    install_requires = [
        str(requirement)
        for requirement
        in pkg_resources.parse_requirements(requirements_txt)
    ]

# Read meta-data
about = {}
exec(open('openhands/__version.py').read(), about)

# Custom command to install requirements as wheels
class InstallRequirementsCommand(setuptools.Command):
    """A custom command to install all dependencies from requirements.txt."""
    description = 'install all dependencies from requirements.txt as wheels if available'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        # Ensure pip and wheel are updated
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip', 'wheel'])

        # Attempt to install each requirement with wheels
        with pathlib.Path('docs/requirements.txt').open() as requirements_txt:
            for requirement in pkg_resources.parse_requirements(requirements_txt):
                try:
                    subprocess.check_call([sys.executable, '-m', 'pip', 'install', str(requirement)])
                except subprocess.CalledProcessError:
                    print(f"Failed to install {requirement} as a wheel, trying from source.")
                    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--no-binary', ':all:', str(requirement)])

# Setup configuration
setuptools.setup(
    name="OpenHands",
    version=about["__version__"],
    description="👐OpenHands : Making Sign Language Recognition Accessible",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://openhands.ai4bharat.org",
    download_url="https://pypi.org/project/OpenHands",
    project_urls={
        'Source': "https://github.com/AI4Bharat/OpenHands",
        'Issues': "https://github.com/AI4Bharat/OpenHands/issues",
        'Documentation': "https://openhands.readthedocs.io",
    },
    author="AI4Bhārat",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=install_requires,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries"
    ],
    cmdclass={
        'install_requirements': InstallRequirementsCommand,
    }
)

# Command to install the requirements:
if __name__ == "__main__":
    setuptools.setup(
        cmdclass={
            'install_requirements': InstallRequirementsCommand,
        }
    )