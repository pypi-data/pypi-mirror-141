import os

from setuptools import find_packages, setup

version_contents = {}
version_path = os.path.join(
    os.path.abspath(os.path.dirname(__file__)), "zhipuai/version.py"
)
with open(version_path, "rt") as f:
    exec(f.read(), version_contents)

setup(
    name="zhipuai",
    description="Python client library for the ZhipuAI API",
    version=version_contents["VERSION"],
    install_requires=[
        "requests>=2.20",  # to get the patch for CVE-2018-18074
        "tqdm",  # Needed for progress bars
        "pandas>=1.2.3",  # Needed for CLI fine-tuning data preparation tool
        "pandas-stubs>=1.1.0.11",  # Needed for type hints for mypy
    ],
    extras_require={"dev": ["black~=21.6b0", "pytest==6.*"]},
    python_requires=">=3.7.1",
    # entry_points={
    #     'console_scripts': [
    #         'zhipuai=zhipuai._zhipuai_scripts:main',
    #     ],
    # },
    entry_points={},
    packages=find_packages(exclude=["tests", "tests.*"]),
    package_data={
        "zhipuai": [
            "py.typed",
        ]
    },
    author="ZhipuAI",
    author_email="jiecai.shan@aminer.cn",
    url="https://github.com/shanjiecai/zhipuai-python",
)
