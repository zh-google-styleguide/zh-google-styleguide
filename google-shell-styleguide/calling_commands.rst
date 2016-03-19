调用命令
================================

检查返回值
--------------------

.. tip::
    总是检查返回值，并给出信息返回值。

对于非管道命令，使用 ``$?`` 或直接通过一个 ``if`` 语句来检查以保持其简洁。

例如：

.. code-block:: shell

    if ! mv "${file_list}" "${dest_dir}/" ; then
      echo "Unable to move ${file_list} to ${dest_dir}" >&2
      exit "${E_BAD_MOVE}"
    fi

    # Or
    mv "${file_list}" "${dest_dir}/"
    if [[ "$?" -ne 0 ]]; then
      echo "Unable to move ${file_list} to ${dest_dir}" >&2
      exit "${E_BAD_MOVE}"
    fi

Bash也有 ``PIPESTATUS`` 变量，允许检查从管道所有部分返回的代码。如果仅仅需要检查整个管道是成功还是失败，以下的方法是可以接受的：

.. code-block:: shell

    tar -cf - ./* | ( cd "${dir}" && tar -xf - )
    if [[ "${PIPESTATUS[0]}" -ne 0 || "${PIPESTATUS[1]}" -ne 0 ]]; then
      echo "Unable to tar files to ${dir}" >&2
    fi

可是，只要你运行任何其他命令， ``PIPESTATUS`` 将会被覆盖。如果你需要基于管道中发生的错误执行不同的操作，那么你需要在运行命令后立即将 ``PIPESTATUS`` 赋值给另一个变量（别忘了 ``[`` 是一个会将 ``PIPESTATUS`` 擦除的命令）。

.. code-block:: shell

    tar -cf - ./* | ( cd "${DIR}" && tar -xf - )
    return_codes=(${PIPESTATUS[*]})
    if [[ "${return_codes[0]}" -ne 0 ]]; then
      do_something
    fi
    if [[ "${return_codes[1]}" -ne 0 ]]; then
      do_something_else
    fi

内建命令和外部命令
--------------------

.. tip::
    可以在调用shell内建命令和调用另外的程序之间选择，请选择内建命令。

我们更喜欢使用内建命令，如在 ``bash(1)`` 中参数扩展函数。因为它更强健和便携（尤其是跟像 ``sed`` 这样的命令比较）

例如：

.. code-block:: shell

    # Prefer this:
    addition=$((${X} + ${Y}))
    substitution="${string/#foo/bar}"

    # Instead of this:
    addition="$(expr ${X} + ${Y})"
    substitution="$(echo "${string}" | sed -e 's/^foo/bar/')"

