import setuptools 

setuptools.setup(name = 'rocrateValidator',
	version = '0.0.6', 
	description = 'This is python library for ro-crate validator',
	package=["src", "src.validator"],
	package_data = {"validator": ["validator/workflow_extension.txt", "validator/check_list.txt"]},
  	include_package_data=True,
	packages=setuptools.find_packages(),
	url = "https://github.com/ResearchObject/ro-crate-validator-py",
	zip_safe = False
	)