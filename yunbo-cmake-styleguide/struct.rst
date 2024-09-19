2. 工程目录结构
----------------

通常一个好的工程目录结构不仅能使开发人员直观的理解功能的作用和源码文件作用，而且还可以为产品的组装和打包提供便利. 当前，因历史原因 YUNBO 的目录结构非常不友好，特此我们制定工程目录结构.

.. tip::

    * 新建库必须使用新的 **工程目录结构**
    * 历史遗留库会逐步进行功能目录重构

2.1. 目录树结构
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    dir
    |
    |- include
        |
        |- yunbo
            |
            |- layer<x>
                |
                | - <libname>
                    |
                    |- ...
    |- src
        |
        | - ...
    |- cmake
        |
        |- FindXXX.cmake
        |- ...
    |- docs
        |
        |- ..
    |- README.md
    |- CMakeLists.txt
    |- .gitignore

* include 对外暴露的头文件
* src 私有的头文件和源文件
* cmake 的 module 文件，用来放置自定义自己使用的依赖库的查找规则的 module 文件
* docs 放置文档文件
* README.md 总体说明文件，包括但不限于，模块概述、编译手册、测试状态、开发路线图等
* CMakeLists.txt CMake 的工程定义文件
* .gitignore 不加入 git 版本管理的文件、文件夹声明文件 