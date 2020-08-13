特性及错误
================================

命令替换
--------------------

.. tip::
    使用 ``$(command)`` 而不是反引号。

嵌套的反引号要求用反斜杠转义内部的反引号。而 ``$(command)`` 形式嵌套时不需要改变，而且更易于阅读。

例如：

.. code-block:: shell

    # This is preferred:
    var="$(command "$(command1)")"

    # This is not:
    var="`command \`command1\``"

test，[和[[
--------------------

.. tip::
    推荐使用 ``[[ ... ]]`` ，而不是 ``[`` , ``test`` , 和 ``/usr/bin/[`` 。

因为在 ``[[`` 和 ``]]`` 之间不会有路径名称扩展或单词分割发生，所以使用 ``[[ ... ]]`` 能够减少错误。而且 ``[[ ... ]]`` 允许正则表达式匹配，而 ``[ ... ]`` 不允许。

.. code-block:: shell

    # This ensures the string on the left is made up of characters in the
    # alnum character class followed by the string name.
    # Note that the RHS should not be quoted here.
    # For the gory details, see
    # E14 at http://tiswww.case.edu/php/chet/bash/FAQ
    if [[ "filename" =~ ^[[:alnum:]]+name ]]; then
      echo "Match"
    fi

    # This matches the exact pattern "f*" (Does not match in this case)
    if [[ "filename" == "f*" ]]; then
      echo "Match"
    fi

    # This gives a "too many arguments" error as f* is expanded to the
    # contents of the current directory
    if [ "filename" == f* ]; then
      echo "Match"
    fi

测试字符串
--------------------

.. tip::
    尽可能使用引用，而不是过滤字符串。

Bash足以在测试中处理空字符串。所以，请使用空（非空）字符串测试，而不是填充字符，使得代码更易于阅读。

.. code-block:: shell

    # Do this:
    if [[ "${my_var}" = "some_string" ]]; then
      do_something
    fi

    # -z (string length is zero) and -n (string length is not zero) are
    # preferred over testing for an empty string
    if [[ -z "${my_var}" ]]; then
      do_something
    fi

    # This is OK (ensure quotes on the empty side), but not preferred:
    if [[ "${my_var}" = "" ]]; then
      do_something
    fi

    # Not this:
    if [[ "${my_var}X" = "some_stringX" ]]; then
      do_something
    fi

为了避免对你测试的目的产生困惑，请明确使用`-z`或者`-n`

.. code-block:: shell

    # Use this
    if [[ -n "${my_var}" ]]; then
      do_something
    fi

    # Instead of this as errors can occur if ${my_var} expands to a test
    # flag
    if [[ "${my_var}" ]]; then
      do_something
    fi

文件名的通配符扩展
--------------------

.. tip::
    当进行文件名的通配符扩展时，请使用明确的路径。

因为文件名可能以 ``-`` 开头，所以使用扩展通配符 ``./*`` 比 ``*`` 来得安全得多。

.. code-block:: shell

    # Here's the contents of the directory:
    # -f  -r  somedir  somefile

    # This deletes almost everything in the directory by force
    psa@bilby$ rm -v *
    removed directory: `somedir'
    removed `somefile'

    # As opposed to:
    psa@bilby$ rm -v ./*
    removed `./-f'
    removed `./-r'
    rm: cannot remove `./somedir': Is a directory
    removed `./somefile'

Eval
--------------------

.. tip::
    应该避免使用eval。

当用于给变量赋值时，Eval解析输入，并且能够设置变量，但无法检查这些变量是什么。

.. code-block:: shell

    # What does this set?
    # Did it succeed? In part or whole?
    eval $(set_my_variables)

    # What happens if one of the returned values has a space in it?
    variable="$(eval some_function)"

管道导向while循环
--------------------

.. tip::
    请使用过程替换或者for循环，而不是管道导向while循环。在while循环中被修改的变量是不能传递给父shell的，因为循环命令是在一个子shell中运行的。

管道导向while循环中的隐式子shell使得追踪bug变得很困难。

.. code-block:: shell

    last_line='NULL'
    your_command | while read line; do
      last_line="${line}"
    done

    # This will output 'NULL'
    echo "${last_line}"

如果你确定输入中不包含空格或者特殊符号（通常意味着不是用户输入的），那么可以使用一个for循环。

.. code-block:: shell

    total=0
    # Only do this if there are no spaces in return values.
    for value in $(command); do
      total+="${value}"
    done

使用过程替换允许重定向输出，但是请将命令放入一个显式的子shell中，而不是bash为while循环创建的隐式子shell。

.. code-block:: shell

    total=0
    last_file=
    while read count filename; do
      total+="${count}"
      last_file="${filename}"
    done < <(your_command | uniq -c)

    # This will output the second field of the last line of output from
    # the command.
    echo "Total = ${total}"
    echo "Last one = ${last_file}"

当不需要传递复杂的结果给父shell时可以使用while循环。这通常需要一些更复杂的“解析”。请注意简单的例子使用如awk这类工具可能更容易完成。当你特别不希望改变父shell的范围变量时这可能也是有用的。

.. code-block:: shell

    # Trivial implementation of awk expression:
    #   awk '$3 == "nfs" { print $2 " maps to " $1 }' /proc/mounts
    cat /proc/mounts | while read src dest type opts rest; do
      if [[ ${type} == "nfs" ]]; then
        echo "NFS ${dest} maps to ${src}"
      fi
    done
