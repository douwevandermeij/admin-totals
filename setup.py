from setuptools import setup, find_packages

REQUIREMENTS = (
    'Django',
)
TEST_REQUIREMENTS = (
    'markdown==2.6.4',
    'coverage',
    'flake8',
    'isort',
    'mock',
    'pytz',
    'unittest-xml-reporting',
)


setup(
    name="admin-totals",
    version='1.0',
    author="Douwe van der Meij",
    author_email="douwe@karibu-online.nl",
    description="""Django Admin Totals, add totals to your columns in Django admin.
    """,
    long_description=open('README.md', 'rt').read(),
    url="https://github.com/douwevandermeij/admin-totals",
    packages=find_packages(),
    include_package_data=True,
    install_requires=REQUIREMENTS,
    tests_require=TEST_REQUIREMENTS,
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ]
)
