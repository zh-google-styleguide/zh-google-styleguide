3. 查找依赖
----------------

通常每个库都会依赖其他库，有的依赖是开源的库，有的依赖是商业库，有得是自研体系下的库. 正确的设置依赖库会使的工程结构更加清晰。

3.1. target 方式引用依赖
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

现代的 CMake 推荐使用 target 的方式引用依赖库，由于 CMake 官方文档比较晦涩建议大家阅读 `cmake 查找依赖 <https://fancyerii.github.io/procmake/ch25/>`_ 。

.. code-block:: cmake

    # cmake 设置
    find_package(spdlog REQUIRED)
    # 设置编译时期的 target 属性，MinSizeRel和RelWithDebInfo使用Release一致的属性，通常只有引用静态库才需要此设置
    set_target_properties(spdlog::spdlog PROPERTIES
        MAP_IMPORTED_CONFIG_MINSIZEREL Release
        MAP_IMPORTED_CONFIG_RELWITHDEBINFO Release
    )

    ...
    add_library(${PROJECT_NAME} ${ALL_SOURCE_FILES})

    target_link_libraries(${PROJECT_NAME} PRIVATE 
        spdlog::spdlog
    )

CMake 的 target 引入依赖方式和 Java，dotnet 的 import package 类似，使用 target 的方式引入依赖不在需要分开设置 **附加包含目录** 和 **链接库**

3.2. 分别设置 inlcude 和 library
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

cmake 依然保留了传统分离设置 C/C++ **附加包含目录** 和 **附加依赖库** 的方式，这种方式不推荐使用，仅当引用了古老的依赖库的情况下作为备用，示例如下：

.. code-block:: cmake

    # cmake 设置
    find_package(TCL REQUIRED)

    ...

    add_library(${PROJECT_NAME})

    target_include_directories(${PROJECT_NAME} PRIVATE
        $<BUILD_INTERFACE:${TCL_INCLUDE_PATH}>
        $<BUILD_INTERFACE:${TK_INCLUDE_PATH}>
    )
    target_link_libraries(${PROJECT_NAME} PRIVATE
        ${TCL_LIBRARY}
        ${TK_LIBRARY}
    )

3.3. 调试

可以通过参数设置参数来调试 **find_package** 的执行过程. 假设，CMakeLists.txt 文件中的 find_package 如下：

.. code-block:: cmake

    # cmake 设置
    #...
    find_package(zlib REQUIRED)

    ...

命令行执行调试的如下:

.. code-block:: bash

    cmake -S <source_dir> -B <build_dir> --debug-find-pkg=zlib

即调试 find_package(***) 那么 --debug-find-pkg=*** 就可以显示查找的整个过程。如下是一段，调试出错的信息：

.. code-block:: bash
      Env variable zlib_DIR [CMAKE_FIND_USE_CMAKE_ENVIRONMENT_PATH].                                                                                                                                                                                                                                          [0/1326]

    none

  CMAKE_PREFIX_PATH env variable [CMAKE_FIND_USE_CMAKE_ENVIRONMENT_PATH].

    none

  CMAKE_FRAMEWORK_PATH and CMAKE_APPBUNDLE_PATH env variables
  [CMAKE_FIND_USE_CMAKE_ENVIRONMENT_PATH].

    none

  Paths specified by the find_package HINTS option.

    none

  Standard system environment variables
  [CMAKE_FIND_USE_SYSTEM_ENVIRONMENT_PATH].

    /opt/rh/devtoolset-8/root/usr
    /usr/local
    /usr
    /home/developer/.local
    /home/developer
    /home/xhc800009@yunbosoft.com/.local
    /home/xhc800009@yunbosoft.com

  CMake User Package Registry [CMAKE_FIND_USE_PACKAGE_REGISTRY].

    none

  CMake variables defined in the Platform file
  [CMAKE_FIND_USE_CMAKE_SYSTEM_PATH].

    /
    /home/xhc800009@yunbosoft.com/dev/test/install
    /usr/X11R6
    /usr/pkg
    /opt

  CMake System Package Registry
  [CMAKE_FIND_PACKAGE_NO_SYSTEM_PACKAGE_REGISTRY].

    none

  Paths specified by the find_package PATHS option.

    none

  find_package considered the following locations for zlib's Config module:

    /home/xhc800009@yunbosoft.com/dev/test/build/CMakeFiles/pkgRedirects/zlibConfig.cmake
    /home/xhc800009@yunbosoft.com/dev/test/build/CMakeFiles/pkgRedirects/zlib-config.cmake
    /opt/rh/devtoolset-8/root/usr/zlibConfig.cmake
    /opt/rh/devtoolset-8/root/usr/zlib-config.cmake
    /usr/local/zlibConfig.cmake
    /usr/local/zlib-config.cmake
    /usr/zlibConfig.cmake
    /usr/zlib-config.cmake
    /home/developer/zlibConfig.cmake
    /home/developer/zlib-config.cmake
    /home/xhc800009@yunbosoft.com/.local/zlibConfig.cmake
    /home/xhc800009@yunbosoft.com/.local/zlib-config.cmake
    /home/xhc800009@yunbosoft.com/zlibConfig.cmake
    /home/xhc800009@yunbosoft.com/zlib-config.cmake
    /zlibConfig.cmake
    /zlib-config.cmake
    /home/xhc800009@yunbosoft.com/dev/test/install/zlibConfig.cmake
    /home/xhc800009@yunbosoft.com/dev/test/install/zlib-config.cmake
    /opt/zlibConfig.cmake
    /opt/zlib-config.cmake

  The file was not found.



  -- Configuring incomplete, errors occurred!
