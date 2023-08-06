from setuptools import setup

setup(
    name='cryptoEx',
    version='0.0.2',
    author='Tiancheng Jiao',
    author_email='jtc1246@outlook.com',
    url='https://github.com/jtc1246/cryptoEx',
    description='A simple API for some cryptocurrency exchanges',
    packages=['cryptoEx'],
    install_requires=['urllib3'],
    python_requires='>=3',
    platforms=["all"],
    license='GPL-2.0 License',
    entry_points={
        'console_scripts': [
            'bnGet=cryptoEx:bnGet',
            'bnPPD=cryptoEx:bnPPD',
            'bnSign=cryptoEx:bnSign',
            'hbGet=cryptoEx:hbGet',
            'hbPost=cryptoEx:hbPost',
            'hbSign=cryptoEx:hbSign',
            'okGet=cryptoEx:okGet',
            'okPost=cryptoEx:okPost',
            'okSign=cryptoEx:okSign',
            'kkGet=cryptoEx:kkGet',
            'kkPost=cryptoEx:kkPost',
            'kkSign=cryptoEx:kkSign'
        ]
    }
)