from distutils.command.build_py import build_py
import os
import sys
import site

from setuptools import (
    setup,
    find_packages,
    Extension
)
from setuptools.command.install import install
from distutils.command.build_py import build_py


PACKAGE = "fisher"


class AfterInstall(build_py):
  def build_c(self, path, filename):
    obj_path = os.path.join(path, PACKAGE, "src", f"{filename}.so")
    c_path = os.path.join(path, PACKAGE, "src", f"{filename}.c")
    ret = os.system(
        f"gcc -o {obj_path} -shared -fPIC {c_path}"
    )
    if ret != 0:
      raise Exception("gcc build failed.")

  def run(self):
    print("!!!!!!Before Install")
    build_py.run(self)
    installed_path = ""
    if "--user" in sys.argv:
      installed_path = site.getusersitepackages()
    else:
      site_path_list = site.getsitepackages()
      for site_path in site_path_list:
        if (os.path.exists(os.path.join(site_path, PACKAGE))):
          installed_path = site_path

    installed_path = self.build_lib
    print("!!!!!!After Install", installed_path)
    self.build_c(installed_path, "fisher")
    self.build_c(installed_path, "asa159")


  # def get_outputs(self):
  #   return [
  #       os.path.join(PACKAGE, "src", "fisher.so"),
  #       os.path.join(PACKAGE, "src", "asa159.so")
  #   ]
    


setup(
    install_requires=[
        "numpy",
        "scipy"
    ],
    test_suite="tests",
    tests_require=["pytest"],
    packages=["fisher"],
    package_data={
      PACKAGE: ["src/*.c", "src/asa159.so", "src/fisher.so"]
    },
    cmdclass={"build_py": AfterInstall},
)
