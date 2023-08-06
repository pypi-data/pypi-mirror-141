from setuptools import setup

setup(
    name='dahua',
    version='1.0.1',
    packages=[''],
    url='https://github.com/dongyi0412/dahua.git',
    license='MIT',
    author='dongyi',
    author_email='1193272767@qq.com',
    description='大华的记录',
    entry_points="""
            [console_scripts]
            dahua=src.main:cli
        """, # 启动命令行脚本的文件
)
