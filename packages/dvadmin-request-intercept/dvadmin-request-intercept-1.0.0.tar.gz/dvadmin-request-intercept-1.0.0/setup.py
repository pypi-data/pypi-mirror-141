import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dvadmin-request-intercept",
    version="1.0.0",
    author="DVAdmin",
    author_email="liqiang@django-vue-admin.com",
    description="dvadmin用来全局拦截指定请求方式及请求插件",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitee.com/huge-dream/dvadmin-request-intercept",
    packages=setuptools.find_packages(),
    python_requires='>=3.6, <4',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
