4. 命名约定
----------------

CMake 大多数关键字是不区分大小写的，约定 CMake 的关键字全部使用小写，变量使用大写，私有的变量前缀 _

4.1. 符合约定
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: cmake
    ###############################################################
    # CMake 设置
    ###############################################################
    cmake_minimum_required(VERSION 3.27)
    project(yunbo_base)
    # find package 目录设置
    list(PREPEND CMAKE_MODULE_PATH ${CMAKE_CURRENT_SOURCE_DIR}/cmake)
 
    ###############################################################
    # C/C++ 编译器设置
    ###############################################################
    set(CMAKE_CXX_STANDARD 17)
    set(CMAKE_C_STANDARD 11)

    if ("${CMAKE_CXX_COMPILER_ID}" STREQUAL "GNU")
        set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fPIC")
    elseif ("${CMAKE_CXX_COMPILER_ID}" STREQUAL "MSVC")
        add_definitions(-DYBBASE_EXPORTS)
        if(NOT ENABLE_WARNING)
            set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} /wd4291 /wd4311 /wd4312 /wd4313 /wd4477 /wd4715 /wd4834 /wd4838")
        endif()        
    else()
        message(VERBOSE "unsupport compiler: ${CMAKE_CXX_COMPILER_ID}")
    endif()

    ###############################################################
    # 查找依赖库
    ###############################################################
    find_package(zlib REQUIRED)
    find_package(spdlog REQUIRED)
    #...
 
    ###############################################################
    # 用file全递归所搜所有源码文件
    ###############################################################
    file(GLOB_RECURSE ALL_SOURCE_FILES include/*.h include/*.hpp src/*.h src/*.cpp src/*.cxx src/*.c)

    # VS xcode等IDE的fileter支持
    source_group(TREE ${CMAKE_CURRENT_SOURCE_DIR}
        FILES ${ALL_SOURCE_FILES}
    )

    ###############################################################
    # 动态库，静态库，可执行程序以及属性设置
    ###############################################################
    add_library(${PROJECT_NAME} SHARED ${ALL_SOURCE_FILES})
 
    # 这个属性仅msvc的sln等少于IDE中有用
    set_target_properties(${PROJECT_NAME} PROPERTIES FOLDER "layer1")

    ###############################################################
    # 编译链接选项设置
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

    target_link_libraries(${PROJECT_NAME} PRIVATE
        zlib
        spdlog::spdlog
    )
 
    ########################
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
 
    add_library(yunbo::layer1::${PROJECT_NAME} ALIAS ${PROJECT_NAME})

4.2. 不符合约定
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

如下 CMakeLists.txt 不符合约定，但可以正常工作，我们必须禁止这种情况的发生.

.. code-block:: cmake
    ###############################################################
    # CMake 设置
    ###############################################################
    CMAKE_MINIMUM_REQUIRED(VERSION 3.27)
    PROJECT(yunbo_base)
    # find package 目录设置
    LIST(PREPEND CMAKE_MODULE_PATH ${CMAKE_CURRENT_SOURCE_DIR}/cmake)
 
    ###############################################################
    # C/C++ 编译器设置
    ###############################################################
    SET(CMAKE_CXX_STANDARD 17)
    SET(CMAKE_C_STANDARD 11)

    IF ("${CMAKE_CXX_COMPILER_ID}" STREQUAL "GNU")
        set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fPIC")
    ELSEIF ("${CMAKE_CXX_COMPILER_ID}" STREQUAL "MSVC")
        add_definitions(-DYBBASE_EXPORTS)
        IF(NOT ENABLE_WARNING)
            set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} /wd4291 /wd4311 /wd4312 /wd4313 /wd4477 /wd4715 /wd4834 /wd4838")
        ENDIF()        
    ELSE()
        MESSAGE(VERBOSE "unsupport compiler: ${CMAKE_CXX_COMPILER_ID}")
    ENDIF()
    
    ###############################################################
    # 查找依赖库
    ###############################################################
    find_package(zlib REQUIRED)
    find_package(spdlog REQUIRED)
    #...
 
    ###############################################################
    # 用file全递归所搜所有源码文件
    ###############################################################
    FILE(GLOB_RECURSE ALL_SOURCE_FILES include/*.h include/*.hpp src/*.h src/*.cpp src/*.cxx src/*.c)

    # VS xcode等IDE的fileter支持
    SOURCE_GROUP(TREE ${CMAKE_CURRENT_SOURCE_DIR}
        FILES ${ALL_SOURCE_FILES}
    )

    ###############################################################
    # 动态库，静态库，可执行程序以及属性设置
    ###############################################################
    ADD_LIBRARY(${PROJECT_NAME} SHARED ${ALL_SOURCE_FILES})
 
    # 这个属性仅msvc的sln等少于IDE中有用
    SET_TARGET_PROPERTIES(${PROJECT_NAME} PROPERTIES FOLDER "layer1")

    ###############################################################
    # 编译链接选项设置
    # 附加包含目录设置:
    #   BUILD_INTERFACE    构建阶段生效的变量
    #   INSTALL_INTERFACE  install的export会到处这个变量到 INTERFACE_INCLUDE_DIRECTORIES变量中
    #   链接库:
    #   现代的C++ cmake工程都是用如下这种链接target的方式将包含目录和，链接lib引起引入的, 只有比较老旧的库才会出现include,lib分开的情况
    # 注意区分PRIVATE、PUBLIC、INTERFACE的用法
    ###############################################################
    TARGET_INCLUDE_DIRECTORIES(${PROJECT_NAME} PRIVATE
        $<BUILD_INTERFACE:${YUNBO_ROOT}/${CMAKE_INSTALL_INCLUDEDIR}/layer1>
        PUBLIC
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}>
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
        INTERFACE
        $<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}/layer1>
        $<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}>
    )

    TARGET_LINK_LIBRARIES(${PROJECT_NAME} PRIVATE
        zlib
        spdlog::spdlog
    )
 
    ########################
    # install
    ########################
    INCLUDE(CMakePackageConfigHelpers)
    WRITE_BASIC_PACKAGE_VERSION_FILE(
        ${CMAKE_CURRENT_BINARY_DIR}/${PROJECT_NAME}-config-version.cmake
        VERSION 0.0.1
        COMPATIBILITY AnyNewerVersion
    )
 
    CONFIGURE_PACKAGE_CONFIG_FILE(${CMAKE_CURRENT_SOURCE_DIR}/config.cmake.in
        ${CMAKE_CURRENT_BINARY_DIR}/${PROJECT_NAME}-config.cmake
        INSTALL_DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake
        NO_SET_AND_CHECK_MACRO
        NO_CHECK_REQUIRED_COMPONENTS_MACRO
    )
 
    INSTALL(TARGETS ${PROJECT_NAME}
        EXPORT ${PROJECT_NAME}-targets
        RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
        LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
        ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
    )
 
    INSTALL(FILES ${PUBLIC_INC_FILES} DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/layer1)
    INSTALL(DIRECTORY include DESTINATION .)
 
    INSTALL(EXPORT ${PROJECT_NAME}-targets
        FILE ${PROJECT_NAME}-targets.cmake
        NAMESPACE yunbo::layer1::
        DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake
    )
 
    INSTALL(FILES
        ${CMAKE_CURRENT_BINARY_DIR}/${PROJECT_NAME}-config.cmake
        DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake
    )
 
    ADD_LIBRARY(yunbo::layer1::${PROJECT_NAME} ALIAS ${PROJECT_NAME})