import setuptools


with open('README.md') as f:
    readme = f.read()

setuptools.setup(
    name="validatejson",
    description="Simplistic tool to validate JSON payload against JSON schema",
    long_description=readme,
    long_description_content_type="text/markdown",
    version="0.2",
    author="deeppy",
    url="https://github.com/deepakcpakhale06/validatejson",
    download_url="https://github.com/deepakcpakhale06/validatejson/tree/main/dist/validatejson-0.1.tar",
    packages=["validatejson"],
    install_requires=['jsonschema','typer'],
    entry_points={
        'console_scripts': ['validatejson=validatejson.validate:run_app']
    },
    classifiers=[
        'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',      # Define that your audience are developers
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',   # Again, pick a license
        'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    ],
)