from setuptools import setup

setup(
    name='blender-chemicals',
    version='0.2.0',
    description="Imports chemicals into blender with open babel.",
    url='http://github.com/patrickfuller/blender-chemicals/',
    author="Patrick Fuller",
    author_email='patrickfuller@gmail.com',
    entry_points={
        'console_scripts': [
            'blender-chemicals = blender_chemicals.run:run'
        ]
    },
    packages=['blender_chemicals'],
    data_files=[
        ('blender_chemicals', ['blender_chemicals/atoms.json'])
    ],
    include_package_data=True,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: Chemistry"
    ]
)
