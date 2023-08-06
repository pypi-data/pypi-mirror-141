from setuptools import setup

setup(
    name = "kd_weather",
    packages = ["kd_weather"],
    version = "1.0.2",
    license="MIT",
    description="Forecast weather data for a given city",
    author="Konrad Dorner",
    url = "https://github.com/K-to-the-D",
    keywords = ["weather", "forecast", "openweathermap"],
    install_requires=[
        "requests",
        "matplotlib",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.8",
    ],
)