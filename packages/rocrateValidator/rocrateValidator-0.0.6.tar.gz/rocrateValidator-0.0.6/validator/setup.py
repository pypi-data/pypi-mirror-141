import setuptools 

setuptools.setup(name = 'rocrateValidator',
	version = '0.0.2', 
	description = 'This is python library for ro-crate validator',
	package_dir={"": "src"},
	packages=setuptools.find_packages(where="src"),
	url = "https://github.com/ResearchObject/ro-crate-validator-py",
	zip_safe = False
	)