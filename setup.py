import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="barium-meal",
    version="0.0.6",
    author="Peckham Data Centre",
    author_email="chris@peckhamdata.com",
    description="Convenience wrapper for OpenTelemetry",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/peckhamdata/barium-meal",
    packages=['barium_meal'],
    license='MIT',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "pytest",
        "opentelemetry-exporter-jaeger",
        "opentelemetry-api",
        "opentelemetry.instrumentation.requests",
        "opentelemetry.instrumentation.boto"
    ]
)