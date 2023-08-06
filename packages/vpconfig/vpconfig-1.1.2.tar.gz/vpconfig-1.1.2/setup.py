import setuptools

requirements_path = "requirements.txt"
readme_path = "README.md"

def check_charkset(file_path):
    import chardet
    with open(file_path, "rb") as f:
        data = f.read(4)
        charset = chardet.detect(data)["encoding"]
    return charset

with open(readme_path, "r", encoding=check_charkset(readme_path)) as fh:
    long_description = fh.read()
install_requires = []

with open(requirements_path, "r", encoding=check_charkset(requirements_path)) as f:
    for req in f.readlines():
        install_requires.append(req.strip())

setuptools.setup(
    name="vpconfig",
    version="1.1.2",
    author="huangsenyan",
    author_email="huangsenyan2022@126.com",
    description="config setting",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitee.com/linyin2007/vpconfig.git",
    packages=setuptools.find_packages(),
    # pack_dir={"","vpconfig"},
    # package_data={"":["*.txt","*.md"]},
    install_requires=install_requires,  # 安装依赖的其他包
    classifiers=["Programming Language :: Python :: 3.8",
                 "Topic :: Software Development :: Libraries :: Python Modules"
                 ],
    python_require=">=3.8",  # python版本
    # include_package_data=True
)
