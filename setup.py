#!/usr/bin/env python

"""Distutils setup file"""

execfile('src/setup/prologue.py')

include_tests      = True   # edit this to stop installation of test modules
include_metamodels = True   # edit this to stop installation of MOF, UML, etc.
include_fcgiapp    = True   # edit this to stop installation of 'fcgiapp'

# Metadata
PACKAGE_NAME = "PEAK"
PACKAGE_VERSION = "0.5a2"

HAPPYDOC_IGNORE = [
    '-i', 'examples',  '-i', 'old', '-i', 'tests', '-i', 'setup',
    '-i', 'kjbuckets', '-i', 'ZConfig', '-i', 'persistence',
]


# Base packages for installation
scripts = ['scripts/peak']

packages = [
    'peak', 'peak.api', 'peak.binding', 'peak.config', 'peak.model',
    'peak.naming', 'peak.naming.factories', 'peak.running',
    'peak.storage', 'peak.util', 'protocols',
]

extensions = [
    Extension("kjbuckets", ["src/kjbuckets/kjbucketsmodule.c"]),
    Extension(
        "peak.binding._once", [
            "src/peak/binding/_once" + EXT,
            "src/peak/binding/getdict.c"
        ]
    ),
    Extension("peak.util.buffer_gap", ["src/peak/util/buffer_gap" + EXT]),
    Extension("peak.util._Code", ["src/peak/util/_Code" + EXT]),
]

# Base data files

data_files = [
    ('peak', ['src/peak/peak.ini']),
] + findDataFiles('src/peak/running', 1, '*.xml')


if include_tests:

    packages += [
        'peak.tests', 'peak.binding.tests', 'peak.config.tests',
        'peak.model.tests', 'peak.naming.tests', 'peak.running.tests',
        'peak.storage.tests', 'peak.util.tests', 'protocols.tests',
    ]

    data_files += [
        ('peak/running/tests', ['src/peak/running/tests/test_cluster.txt']),
    ]


if include_metamodels:

    packages += [
        'peak.metamodels',
        'peak.metamodels.UML13', 'peak.metamodels.UML14',
        'peak.metamodels.UML13.model', 'peak.metamodels.UML14.model',
        'peak.metamodels.UML13.model.Foundation',
        'peak.metamodels.UML13.model.Behavioral_Elements',
    ]

    if include_tests:

        packages += [ 'peak.metamodels.tests' ]

        data_files += findDataFiles('src/peak/metamodels/tests', 1, '*.xml')



        


try:
    # Check if Zope X3 is installed; we use zope.component
    # because we don't install it ourselves; if we used something we
    # install, we'd get a false positive if PEAK was previously installed.
    import zope.component
    zope_installed = True

except ImportError:
    zope_installed = False


if not zope_installed:

    packages += [
        'persistence', 'ZConfig',
    ]

    extensions += [
        Extension("persistence._persistence", ["src/persistence/persistence.c"])
    ]

    if include_tests:
        packages += [
            'persistence.tests', 'ZConfig.tests',
        ]

        data_files += findDataFiles(
            'src/ZConfig/tests', 1, '*.xml', '*.txt', '*.conf'
        )












import os

if os.name=='posix':

    # install 'fcgiapp' module on posix systems
    if include_fcgiapp:
        extensions += [
            Extension("fcgiapp", [
                "src/fcgiapp/fcgiappmodule.c", "src/fcgiapp/fcgiapp.c"
            ])
        ]



execfile('src/setup/common.py')

setup(
    name=PACKAGE_NAME,
    version=PACKAGE_VERSION,

    description="The Python Enterprise Application Kit",
    author="Phillip J. Eby",
    author_email="transwarp@eby-sarna.com",
    url="http://peak.telecommunity.com/",
    license="PSF or ZPL",
    platforms=['UNIX','Windows'],

    package_dir = {'':'src'},
    packages    = packages,
    cmdclass = SETUP_COMMANDS,
    data_files = data_files,
    ext_modules = extensions,
    scripts = scripts,
)







