from setuptools import setup,find_packages
setup(name='zsltool',
      version='1.0.4',
      description='some utilities',
      author='Zhou-Shilin',
      author_email='2839997522@qq.com',
      requires= ['xes.tool','math','hashlib','py_compile'], # 定义依赖哪些模块
      packages=find_packages(),
      license="apache 3.0"
      )