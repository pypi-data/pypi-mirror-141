from setuptools import setup, find_packages  # type: ignore

setup(
    name='onnx-simplifier',
    # The version will be updated automatically in CI
    version='0.3.7',
    description='Simplify your ONNX model',
    author='daquexian',
    author_email='daquexian566@gmail.com',
    url='https://github.com/daquexian/onnx-simplifier',
    packages=find_packages(),
    package_data={'': ['LICENSE']},
    license='Apache',
    keywords='deep-learning ONNX',
    install_requires=[
        'onnx',
        'onnxoptimizer >= 0.2.5',
        'onnxruntime >= 1.6.0',
        'protobuf >= 3.7.0'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Scientific/Engineering',
        'Topic :: Software Development'
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'onnxsim=onnxsim:main',
        ],
    },
)
