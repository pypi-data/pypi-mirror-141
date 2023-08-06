from setuptools import setup, find_packages

if __name__ == "__main__":
    version = "2.9.43.2"

    setup(
        name='dqdatasdk',
        version=version,
        author='digquant',
        author_email='it@digquant.com',
        description='dqdatasdk api system',
        keywords='dqdatasdk',
        license='LICENSE',
        packages=find_packages(),
        package_dir={'': '.'},
        install_requires=[
            'rqdatac>=' + version + ',' + '<=' + version,
            ],
        dependency_links=[

        ],
        url='',

    )