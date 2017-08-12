from setup import setup, find_packages

setup(
  name="nexus",
  version="0.0.1",
  description="Open REST API package manager",
  url="https://github.com/daemon/nexus",
  author="tetrisd",
  author_email="0x8badc0de@gmail.com",
  license="MIT",
  packages=find_packages(exclude=["examples"]),
  install_requires=["requests"],
  python_requires="~=3.4")

