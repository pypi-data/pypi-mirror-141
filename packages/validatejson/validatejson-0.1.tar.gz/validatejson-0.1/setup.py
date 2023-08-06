import setuptools

setuptools.setup(
    name="validatejson",
    version="0.1",
    author="deeppy",
    description="Validate JSON payload against the JSON schema",
    url="https://github.com/deepakcpakhale06/validatejson",
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