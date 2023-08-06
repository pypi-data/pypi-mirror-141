import setuptools


with open("README.md", "r", encoding="utf-8") as f:
    README = f.read()

setuptools.setup(
    name="make_vcard",
    version="0.1.2",
    author="antianshi",
    author_email="948258209@qq.com",
    description="用于以execl文件生成.vcf通讯录导入文件",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://gitee.com/antianshi/make_vcard", 
    packages=setuptools.find_packages(), 
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[ 
        'openpyxl >= 3.0.9',
    ],
)