# References
# https://packaging.python.org/tutorials/packaging-projects/
# https://www.geeksforgeeks.org/how-to-publish-python-package-at-pypi-using-twine-module/
# https://stackoverflow.com/questions/45168408/creating-tar-gz-in-dist-folder-with-python-setup-py-install
# https://docs.python.org/3/distutils/sourcedist.html
# https://github.com/conda-incubator/grayskull
# https://setuptools.pypa.io/en/latest/userguide/datafiles.html
# https://packaging.python.org/en/latest/guides/using-manifest-in/


import setuptools


_ENCODING_UTF8 = "utf-8"
_MODE_R = "r"
_REQUIREMENT_FILE = "requirements.txt"


def _make_long_description():
	with open("README.md", _MODE_R, encoding=_ENCODING_UTF8) as readme_file:
		long_description = readme_file.read()

	start_index = long_description.index("## Français")

	return long_description[start_index:]


def _make_requirement_list():
	with open(_REQUIREMENT_FILE, _MODE_R, encoding=_ENCODING_UTF8) as req_file:
		req_str = req_file.read()

	raw_requirements = req_str.split("\n")

	requirements = list()
	for requirement in raw_requirements:
		if len(requirement) > 0:
			requirements.append(requirement)

	return requirements

if __name__ == "__main__":
	setuptools.setup(
		name = "PyPDF2_Fields",
		version = "1.0.1",
		author = "Guyllaume Rousseau",
		description = "Library PyPDF2_Fields is a complement to PyPDF2. It helps reading and setting a PDF file’s fields, knowing their type and controlling their editability.",
		long_description = _make_long_description(),
		long_description_content_type = "text/markdown",
		url = "https://github.com/GRV96/PyPDF2_Fields",
		classifiers = [
			"Development Status :: 5 - Production/Stable",
			"Intended Audience :: Developers",
			"License :: OSI Approved :: MIT License",
			"Operating System :: OS Independent",
			"Programming Language :: Python :: 3",
			"Topic :: Software Development :: Libraries :: Python Modules",
			"Topic :: Utilities"
		],
		install_requires = _make_requirement_list(),
		packages = setuptools.find_packages(exclude=("tests",)),
		package_data = {"": (_REQUIREMENT_FILE,)},
		license = "MIT",
		license_files = ("LICENSE",))
