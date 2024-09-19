8. 安装
----------------

install 命令是将编译的产物组装成完成的制品的机制，设计哲学为管理模块管好自己的内容，总体组装方案最终集成的方来做。搭配 **cpack** 可以方便的完成产品打包。因为Win下的安装流派很多，但类UNIX的 install 是有事实标准的，我们规定采用GNU的安装目录组织方式.

.. tip::

    目前大家诟病 **YUNBOMech** install 慢的原因是额外安装了 ACIS（4-7GB）, Qt, Boost 这种巨量的库,解决方法也很简单使用环境变量的方式引入这种三方库，只有在打包的过程才需要触发这些三方库的install.


.. code-block:: cmake

    # ...

    ########################
    # 安装设置
    # install
    ########################
    include(CMakePackageConfigHelpers)
    write_basic_package_version_file(
        ${CMAKE_CURRENT_BINARY_DIR}/${PROJECT_NAME}-config-version.cmake
        VERSION 0.0.1
        COMPATIBILITY AnyNewerVersion
    )
 
    configure_package_config_file(${CMAKE_CURRENT_SOURCE_DIR}/config.cmake.in
        ${CMAKE_CURRENT_BINARY_DIR}/${PROJECT_NAME}-config.cmake
        INSTALL_DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake
        NO_SET_AND_CHECK_MACRO
        NO_CHECK_REQUIRED_COMPONENTS_MACRO
    )
 
    install(TARGETS ${PROJECT_NAME}
        EXPORT ${PROJECT_NAME}-targets
        RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
        LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
        ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
    )
 
    install(FILES ${PUBLIC_INC_FILES} DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/layer1)
    install(DIRECTORY include DESTINATION .)
 
    install(EXPORT ${PROJECT_NAME}-targets
        FILE ${PROJECT_NAME}-targets.cmake
        NAMESPACE yunbo::layer1::
        DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake
    )
 
    install(FILES
        ${CMAKE_CURRENT_BINARY_DIR}/${PROJECT_NAME}-config.cmake
        DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake
    )

    ########################
    # 其他设置
    # 一起编译和 find_package 的行为一致
    ########################
    add_library(yunbo::layer1::${PROJECT_NAME} ALIAS ${PROJECT_NAME})

8.1. 安装制品
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: cmake

    # ...

    ########################
    # 安装设置
    # install
    ########################
    include(CMakePackageConfigHelpers)
    write_basic_package_version_file(
        ${CMAKE_CURRENT_BINARY_DIR}/${PROJECT_NAME}-config-version.cmake
        VERSION 0.0.1
        COMPATIBILITY AnyNewerVersion
    )
 
    configure_package_config_file(${CMAKE_CURRENT_SOURCE_DIR}/config.cmake.in
        ${CMAKE_CURRENT_BINARY_DIR}/${PROJECT_NAME}-config.cmake
        INSTALL_DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake
        NO_SET_AND_CHECK_MACRO
        NO_CHECK_REQUIRED_COMPONENTS_MACRO
    )
 
    install(TARGETS ${PROJECT_NAME}
        EXPORT ${PROJECT_NAME}-targets
        RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
        LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
        ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
    )

#. include(CMakePackageConfigHelpers) 引入GNU的install安装规范变量 **${CMAKE_INSTALL_BINDIR}** ， **${CMAKE_INSTALL_LIBDIR}**， **${CMAKE_INSTALL_INCLUDEDIR}** 等变量，会根据系统等信息有不同的值，详细请参考官网说明.
#. write_basic_package_version_file 导出的module文件中生成库的版本信息
#. configure_package_config_file 导出一个可以使用 **find_package(*** CONFIG)** 引入库的 module 文件
#. install 安装制品
    #. TARGETS ${PROJECT_NAME} 固定为当前库的名字
    #. EXPORT ${PROJECT_NAME}-targets 将安装信息注入到 ${PROJECT_NAME}-targets-debug.cmake , ${PROJECT_NAME}-targets-debug.cmake 文件中，原理就是一相对目录的方式记录可执行文件，导出符号，头文件的安装位置等， **target_include_directories** 中的 **生成器表达式** $<INSTALL_INTERFACE:...> 的值会注入到 export 的 targets.cmake 文件中。 
    #. RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR} 可执行文件的安装位置 ${CMAKE_INSTALL_BINDIR} = bin 首字符为 **/** 是为绝对路径，没有为相对路径 安装到 **CMAKE_INSTALL_PREFIX** 下
    #. LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR} 导入导出符号，win下动态库 **.lib** ，unix 下为 .so
    #. ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR} 静态库

8.2. 安装头文件
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: cmake
    install(DIRECTORY include DESTINATION .)

#. 根据 `工程目录结构 <https://zh-yunbo-styleguide.readthedocs.io/zh-cn/latest/yunbo-cmake-styleguide/struct.html#>`_ 的结构仅需要上述一行代码即可，如果未按此组织工程结构，就需要额外的处理了.

8.3. 安装 module 文件
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

按如下，代码控制 **cmake** 的 **module** 的文件安装

.. code-block:: cmake
    install(EXPORT ${PROJECT_NAME}-targets
        FILE ${PROJECT_NAME}-targets.cmake
        NAMESPACE yunbo::layer1::
        DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake
    )
 
    install(FILES
        ${CMAKE_CURRENT_BINARY_DIR}/${PROJECT_NAME}-config.cmake
        DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake
    )

8.4. 安装其他文件
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

通过 **install** 的 **FILES** **DIRECTORY** 可以完成安装各种文件，还可以控制安装文件的权限等(在类UNIX多用户系统权限是很重要的win没有这个问题)，