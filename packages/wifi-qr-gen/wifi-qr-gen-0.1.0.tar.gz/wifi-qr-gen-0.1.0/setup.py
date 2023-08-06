from setuptools import setup, find_packages

setup(
    name="wifi-qr-gen",
    version="0.1.0",
    packages=find_packages(),
    author="Tom Buente",
    url="https://github.com/tombuente/wifi-qr",
    include_package_data=True,
    install_requires=[
        "Click",
        "qrcode",
    ],
    entry_points={
        "console_scripts": [
            "wifi-qr = wifi_qr.scripts.wifi_qr:gen_wifi_qr",
        ],
    },
)
