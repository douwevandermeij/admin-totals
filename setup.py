from setuptools import setup, find_packages

REQUIREMENTS = (
    'Django',
)
TEST_REQUIREMENTS = (
)


setup(
    name="admin-totals",
    version='1.0',
    author="Douwe van der Meij",
    author_email="douwe@karibu-online.nl",
    description="""Django Admin Totals.
    """,
    long_description=open('README.md', 'rt').read(),
    url="",
    packages=find_packages(),
    include_package_data=True,
    install_requires=REQUIREMENTS,
    tests_require=TEST_REQUIREMENTS,
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ]
)
