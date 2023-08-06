from setuptools import setup

name = 'pyManson'
version='1.0.1'
setup(	name=name,
	version=version,
	description='Communcation package for Manson power suply',
	author='Konstantin Niehaus',
    author_email="konstantin+pypi@niehaus-web.com",
	license='MIT',
	install_requires=['pyserial'],
	long_description="Serial communication to Manson power suply is initialized. All commands mentioned in the device manual can be used. Convenience functions for setting current, voltage, locking the device screen, ... have been implemented",
	classifiers=[
		'Development Status :: 4 - Beta',
		'Programming Language :: Python :: 3',
	],
	keywords='power supply, manson, serial',
	packages=['pyManson'],
	include_package_data=True,
	zip_safe=False)
