import setuptools 

setuptools.setup(name = 'rocrateValidator',
	version = '0.0.3', 
	description = 'This is python library for ro-crate validator',
	package=["src", "src.validator"],
	packages=setuptools.find_packages(),
	url = "https://github.com/ResearchObject/ro-crate-validator-py",
	zip_safe = False
	)