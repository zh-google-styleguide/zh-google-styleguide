命名约定
================================

函数名
--------------------

.. tip::
    使用小写字母，并用下划线分隔单词。使用双冒号 ``::`` 分隔库。函数名之后必须有圆括号。关键词 ``function`` 是可选的，但必须在一个项目中保持一致。

如果你正在写单个函数，请用小写字母来命名，并用下划线分隔单词。如果你正在写一个包，使用双冒号 ``::`` 来分隔包名。大括号必须和函数名位于同一行（就像在Google的其他语言一样），并且函数名和圆括号之间没有空格。

.. code-block:: shell

    # Single function
    my_func() {
      ...
    }

    # Part of a package
    mypackage::my_func() {
      ...
    }

当函数名后存在 ``()`` 时，关键词 ``function`` 是多余的。但是其促进了函数的快速辨识。

变量名
--------------------

.. tip::
    如函数名。

循环的变量名应该和循环的任何变量同样命名。

.. code-block:: shell

    for zone in ${zones}; do
      something_with "${zone}"
    done

常量和环境变量名
--------------------

.. tip::
    全部大写，用下划线分隔，声明在文件的顶部。

常量和任何导出到环境中的都应该大写。

.. code-block:: shell

    # Constant
    readonly PATH_TO_FILES='/some/path'

    # Both constant and environment
    declare -xr ORACLE_SID='PROD'

第一次设置时有一些就变成了常量（例如，通过getopts）。因此，可以在getopts中或基于条件来设定常量，但之后应该立即设置其为只读。值得注意的是，在函数中 ``declare`` 不会对全局变量进行操作。所以推荐使用 ``readonly`` 和 ``export`` 来代替。

.. code-block:: shell

    VERBOSE='false'
    while getopts 'v' flag; do
      case "${flag}" in
        v) VERBOSE='true' ;;
      esac
    done
    readonly VERBOSE

源文件名
--------------------

.. tip::
    小写，如果需要的话使用下划线分隔单词。

这是为了和在Google中的其他代码风格保持一致： ``maketemplate`` 或者 ``make_template`` ，而不是 ``make-template`` 。

只读变量
--------------------

.. tip::
    使用 ``readonly`` 或者 ``declare -r`` 来确保变量只读。

因为全局变量在shell中广泛使用，所以在使用它们的过程中捕获错误是很重要的。当你声明了一个变量，希望其只读，那么请明确指出。

.. code-block:: shell

    zip_version="$(dpkg --status zip | grep Version: | cut -d ' ' -f 2)"
    if [[ -z "${zip_version}" ]]; then
      error_message
    else
      readonly zip_version
    fi

使用本地变量
--------------------

.. tip::
    使用 ``local`` 声明特定功能的变量。声明和赋值应该在不同行。

使用 ``local`` 来声明局部变量以确保其只在函数内部和子函数中可见。这避免了污染全局命名空间和不经意间设置可能具有函数之外重要性的变量。

当赋值的值由命令替换提供时，声明和赋值必须分开。因为内建的 ``local`` 不会从命令替换中传递退出码。

.. code-block:: shell

    my_func2() {
      local name="$1"

      # Separate lines for declaration and assignment:
      local my_var
      my_var="$(my_func)" || return

      # DO NOT do this: $? contains the exit code of 'local', not my_func
      local my_var="$(my_func)"
      [[ $? -eq 0 ]] || return

      ...
    }

函数位置
--------------------

.. tip::
    将文件中所有的函数一起放在常量下面。不要在函数之间隐藏可执行代码。

如果你有函数，请将他们一起放在文件头部。只有includes， ``set`` 声明和常量设置可能在函数声明之前完成。不要在函数之间隐藏可执行代码。如果那样做，会使得代码在调试时难以跟踪并出现意想不到的讨厌结果。

主函数main
--------------------

.. tip::
    对于包含至少一个其他函数的足够长的脚本，需要称为 ``main`` 的函数。

为了方便查找程序的开始，将主程序放入一个称为 ``main`` 的函数，作为最下面的函数。这使其和代码库的其余部分保持一致性，同时允许你定义更多变量为局部变量（如果主代码不是一个函数就不能这么做）。文件中最后的非注释行应该是对 ``main`` 函数的调用。

.. code-block:: shell

    main "$@"

显然，对于仅仅是线性流的短脚本， ``main`` 是矫枉过正，因此是不需要的。

