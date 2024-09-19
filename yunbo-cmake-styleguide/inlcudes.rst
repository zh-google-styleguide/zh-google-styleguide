7. 包含目录
----------------

现代的 CMake 包含目录不仅是用来添加附加包含目录的，还包含导出包含目录，本节就详细阐述 **include** 的风格规范.

7.1. 包含目录说明
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

函数: target_include_directories

参数关键字:

    #. PUBLIC 当前库可见，依赖当前库的其他库也可见
    #. PRIVATE 仅当前库可见
    #. INTERFACE 当前库未使用，但依赖当前库的其他库可见

生成期表达式:

    #. INSTALL_INTERFACE 通过 **install(EXPORT)** 将指定文件注入到cmake-targets.cmake文件中
    #. BUILD_INTERFACE 编译阶段，当前库可见，和当前库处在统一构建系统中的依赖此库的其他库也可见 

.. tip::

    此处的概念比较晦涩，建议参考 `CMake官方文档 <https://cmake.org/cmake/help/v3.27/manual/cmake-generator-expressions.7.html#genex:BUILD_INTERFACE>`_
    `推荐学习网文 <https://fancyerii.github.io/procmake/ch10/>`_
    生成器表达式就是在cmake的configure和generate阶段值是不可见的，而是在makefile中可见

7.2. 实例

.. code-block:: cmake
    ###############################################################
    # CMake 设置
    ###############################################################
    # ...
 
    ###############################################################
    # 编译器设置
    ###############################################################
    # ...

    ###############################################################
    # 查找依赖库
    ###############################################################
    # ...
 
    ###############################################################
    # 全递归搜索源码文件生成库或可执行程序及工程属性设置
    ###############################################################
    # ...

    ###############################################################
    # 编译、链接选项设置
    # 附加包含目录设置:
    #   BUILD_INTERFACE    构建阶段生效的变量
    #   INSTALL_INTERFACE  install的export会到处这个变量到 INTERFACE_INCLUDE_DIRECTORIES变量中
    #   链接库:
    #   现代的C++ cmake工程都是用如下这种链接target的方式将包含目录和，链接lib引起引入的, 只有比较老旧的库才会出现include,lib分开的情况
    # 注意区分PRIVATE、PUBLIC、INTERFACE的用法
    ###############################################################
    if ("${CMAKE_CXX_COMPILER_ID}" STREQUAL "GNU")
        set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fPIC")
    elseif ("${CMAKE_CXX_COMPILER_ID}" STREQUAL "MSVC")
        target_compile_definitions(${PROJECT_NAME} PRIVATE YBBASE_EXPORTS)
        if(NOT ENABLE_WARNING)
            set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} /wd4291 /wd4311 /wd4312 /wd4313 /wd4477 /wd4715 /wd4834 /wd4838")
        endif()        
    else()
        message(VERBOSE "unsupport compiler: ${CMAKE_CXX_COMPILER_ID}")
    endif()
 
    target_include_directories(${PROJECT_NAME} PRIVATE
        $<BUILD_INTERFACE:${YUNBO_ROOT}/${CMAKE_INSTALL_INCLUDEDIR}/layer1>
        PUBLIC
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}>
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
        INTERFACE
        $<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}/layer1>
        $<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}>
    )
 
    ########################
    # 安装设置
    # install
    ########################
    # ...

    ########################
    # 其他设置
    # 一起编译和 find_package 的行为一致
    ########################
    add_library(yunbo::layer1::${PROJECT_NAME} ALIAS ${PROJECT_NAME})