1. cmake设置
----------------------

通常 CMakeLists.txt 的首行应设置好 CMake 自身的设置

1.1. 设定 CMake 版本号
~~~~~~~~~~~~~~~~~~~~~~~~

.. tip::
    设定版本号，可以避免使用不同特性的CMake的检测.

.. code-block:: cmake

    cmake_minimum_required(VERSION 3.27)

cmake 版本不能大于3.28，如需要使用新版本的特性请联系自己的PL进行其他环境配置的兼容性验证.

1.2. 设置工程
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: cmake

    project(yunbo_base VERSION major_version.minor_version.patch_version.tweak_version)
    # 生成版本定义头文件, 将生成的version.h添加到.gitignore中
    configure_file(${CMAKE_CURRENT_SOURCE_DIR}/version.h.in ${CMAKE_CURRENT_SOURCE_DIR}/include/yunbo/${PROJECT_NAME}/version.h @ONLY)

通常工程版本定义的模版文件如下:

.. code-block:: C++

    #ifndef YUNBO_LAYER1_@PROJECT_NAME@_VERSION_H_
    #define YUNBO_LAYER1_@PROJECT_NAME@_VERSION_H_

    #ifndef @PROJECT_NAME@_VERSION_MAJOR
    #define @PROJECT_NAME@_VERSION_MAJOR @PROJECT_VERSION_MAJOR@
    #endif // !@PROJECT_NAME@_VERSION_MAJOR

    #ifndef @PROJECT_NAME@_VERSION_MINOR
    #define @PROJECT_NAME@_VERSION_MINOR @PROJECT_VERSION_MINOR@
    #endif // !@PROJECT_NAME@_VERSION_MINOR

    #ifndef @PROJECT_NAME@_VERSION_PATCH
    #define @PROJECT_NAME@_VERSION_PATCH @PROJECT_VERSION_PATCH@
    #endif // !@PROJECT_NAME@_VERSION_PATCH

    #ifndef @PROJECT_NAME@_VERSION_TWEAK
    #define @PROJECT_NAME@_VERSION_TWEAK @PROJECT_VERSION_TWEAK@
    #endif //!@PROJECT_NAME@_VERSION_TWEAK

    #ifndef @PROJECT_NAME@_VERSION_CYCLE
    #define @PROJECT_NAME@_VERSION_CYCLE "release"
    #endif // !@PROJECT_NAME@_VERSION_CYCLE

    #ifndef @PROJECT_NAME@_VERSION_STR
    #define @PROJECT_NAME@_VERSION_STR "@PROJECT_VERSION_MAJOR@.@PROJECT_VERSION_MINOR@.@PROJECT_VERSION_PATCH@.@PROJECT_VERSION_TWEAK@_@PROJECT_NAME@_VERSION_CYCLE"
    #endif // @PROJECT_NAME@_VERSION_STR

    #endif // YUNBO_LAYER1_@PROJECT_NAME@_VERSION_H_

project 关键字定义 CMakeLists.txt 可以独立进行 cmake 即可以生成 **Visual Studio** 的 sln, 可选参数 VERSION 可以设置工程版本信息，详细命令说明可阅读官网说明 `CMake project <https://cmake.org/cmake/help/v3.27/command/project.html#project>`_

1.3. 设置策略
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: cmake

    cmake_policy(PUSH)
    cmake_policy(SET CMP0048 NEW)
    ...
    cmake_policy(POP)

CMake策略控制不同版本一些命令参数和作用的设置，cmake_policy(PUSH) 和 cmake_policy(POP) 之间是控制策略生效的作用域

1.4. 本节整体实例
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: cmake
    
    cmake_minimum_required(VERSION 3.27)
    cmake_policy(PUSH)
    # 使 project VERSION 参数生效
    cmake_policy(SET CMP0048 NEW)

    # 精确到分的时间戳为 TWEAK 版本号
    string(TIMESTAMP _BUILD_TIME %Y%m%d%H%M)
    project(yunbo_base VERSION 1.0.0.${_BUILD_TIME})
    # 生成版本定义头文件, 将生成的version.h添加到.gitignore中
    configure_file(${CMAKE_CURRENT_SOURCE_DIR}/version.h.in ${CMAKE_CURRENT_SOURCE_DIR}/include/yunbo/${PROJECT_NAME}/version.h @ONLY)

    ...
    cmake_policy(POP)