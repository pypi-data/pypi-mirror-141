#coding:utf-8

from setuptools import setup, find_packages

setup(
    name='sunhpcSnack',        # 项目名
    version='1.0.0',           # 版本号
    author="sunhpc",
    author_email="admin@sunhpc.com",
    description="Snack built with sunhpc",
    url="https://www.sunhpc.com",
    packages=find_packages(),   # 自动搜索所有包含__init__.py文件的目录.

    package_data={'':['*.so']}, # 希望被打包的文件.
    #packages=['sunhpcSnack'],  # 包括在安装包内的Python包
    #include_package_data=True, # 启用清单文件MANIFEST.in
    install_requires=[],        # 依赖列表,eg.. Flask>=0.10
    dependency_links=[],        # 如果在PyPi中无法找到,则会从这里标识的URL中获取.,eg.. 'http://www.xxx.com/exp.whl'
    exclude_package_data={'':['.gitignore']}, # 需要排除的目录
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent"],
    python_requires='>=3.6',

)
