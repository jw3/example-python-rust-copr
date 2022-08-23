from setuptools import find_namespace_packages, setup
from setuptools_rust import RustExtension
import os


def get_version():
    if "VERSION" in os.environ:
        return os.getenv("VERSION")
    try:
        from version import get_versions
        meta = get_versions()
        if "version" not in meta:
            raise RuntimeError("Could not parse version from Git")
        return meta["version"]
    except Exception:
        raise RuntimeError("Was not able to detect Python rulec version")


setup(
    name="rulec",
    version=get_version(),
    packages=find_namespace_packages(
        include=["rulec", "rulec.*"],
    ),
    setup_requires=["setuptools", "setuptools_rust"],
    zip_safe=False,
    rust_extensions=[
        RustExtension("rulec.rust")
    ],
)
