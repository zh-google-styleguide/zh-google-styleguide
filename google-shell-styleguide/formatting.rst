格式
================================

缩进
--------------------

.. tip::
    缩进两个空格，没有制表符。

在代码块之间请使用空行以提升可读性。缩进为两个空格。无论你做什么，请不要使用制表符。对于已有文件，保持已有的缩进格式。

行的长度和长字符串
--------------------

.. tip::
    行的最大长度为80个字符。

如果你必须写长度超过80个字符的字符串，如果可能的话，尽量使用here document或者嵌入的换行符。长度超过80个字符的文字串且不能被合理地分割，这是正常的。但强烈建议找到一个方法使其变短。

.. code-block:: shell

    # DO use 'here document's
    cat <<END;
    I am an exceptionally long
    string.
    END

    # Embedded newlines are ok too
    long_string="I am an exceptionally
      long string."

管道
--------------------

.. tip::
    如果一行容不下整个管道操作，那么请将整个管道操作分割成每行一个管段。

如果一行容得下整个管道操作，那么请将整个管道操作写在同一行。

否则，应该将整个管道操作分割成每行一个管段，管道操作的下一部分应该将管道符放在新行并且缩进2个空格。这适用于使用管道符'|'的合并命令链以及使用'||'和'&&'的逻辑运算链。

.. code-block:: shell

    # All fits on one line
    command1 | command2

    # Long commands
    command1 \
      | command2 \
      | command3 \
      | command4

循环
--------------------

.. tip::
    请将 ``; do`` , ``; then`` 和 ``while`` , ``for`` , ``if`` 放在同一行。

shell中的循环略有不同，但是我们遵循跟声明函数时的大括号相同的原则。也就是说， ``; do`` , ``; then`` 应该和 if/for/while 放在同一行。 ``else`` 应该单独一行，结束语句应该单独一行并且跟开始语句垂直对齐。

例如：

.. code-block:: shell

    for dir in ${dirs_to_cleanup}; do
      if [[ -d "${dir}/${ORACLE_SID}" ]]; then
        log_date "Cleaning up old files in ${dir}/${ORACLE_SID}"
        rm "${dir}/${ORACLE_SID}/"*
        if [[ "$?" -ne 0 ]]; then
          error_message
        fi
      else
        mkdir -p "${dir}/${ORACLE_SID}"
        if [[ "$?" -ne 0 ]]; then
          error_message
        fi
      fi
    done

case语句
--------------------

.. tip::
    * 通过2个空格缩进可选项。
    * 在同一行可选项的模式右圆括号之后和结束符 ``;;`` 之前各需要一个空格。
    * 长可选项或者多命令可选项应该被拆分成多行，模式、操作和结束符 ``;;`` 在不同的行。

匹配表达式比 ``case`` 和 ``esac`` 缩进一级。多行操作要再缩进一级。一般情况下，不需要引用匹配表达式。模式表达式前面不应该出现左括号。避免使用 ``;&`` 和 ``;;&`` 符号。

.. code-block:: shell

    case "${expression}" in
      a)
        variable="..."
        some_command "${variable}" "${other_expr}" ...
        ;;
      absolute)
        actions="relative"
        another_command "${actions}" "${other_expr}" ...
        ;;
      *)
        error "Unexpected expression '${expression}'"
        ;;
    esac

只要整个表达式可读，简单的命令可以跟模式和 ``;;`` 写在同一行。这通常适用于单字母选项的处理。当单行容不下操作时，请将模式单独放一行，然后是操作，最后结束符 ``;;`` 也单独一行。当操作在同一行时，模式的右括号之后和结束符 ``;;`` 之前请使用一个空格分隔。

.. code-block:: shell

    verbose='false'
    aflag=''
    bflag=''
    files=''
    while getopts 'abf:v' flag; do
      case "${flag}" in
        a) aflag='true' ;;
        b) bflag='true' ;;
        f) files="${OPTARG}" ;;
        v) verbose='true' ;;
        *) error "Unexpected option ${flag}" ;;
      esac
    done

变量扩展
--------------------

.. tip::
    按优先级顺序：保持跟你所发现的一致；引用你的变量；推荐用 ``${var}`` 而不是 ``$var`` ，详细解释如下。

这些仅仅是指南，因为作为强制规定似乎饱受争议。

以下按照优先顺序列出。

1. 与现存代码中你所发现的保持一致。
2. 引用变量参阅下面一节，引用。
3. 除非绝对必要或者为了避免深深的困惑，否则不要用大括号将单个字符的shell特殊变量或定位变量括起来。推荐将其他所有变量用大括号括起来。

.. code-block:: shell

        # Section of recommended cases.

        # Preferred style for 'special' variables:
        echo "Positional: $1" "$5" "$3"
        echo "Specials: !=$!, -=$-, _=$_. ?=$?, #=$# *=$* @=$@ \$=$$ ..."

        # Braces necessary:
        echo "many parameters: ${10}"

        # Braces avoiding confusion:
        # Output is "a0b0c0"
        set -- a b c
        echo "${1}0${2}0${3}0"

        # Preferred style for other variables:
        echo "PATH=${PATH}, PWD=${PWD}, mine=${some_var}"
        while read f; do
          echo "file=${f}"
        done < <(ls -l /tmp)

        # Section of discouraged cases

        # Unquoted vars, unbraced vars, brace-quoted single letter
        # shell specials.
        echo a=$avar "b=$bvar" "PID=${$}" "${1}"

        # Confusing use: this is expanded as "${1}0${2}0${3}0",
        # not "${10}${20}${30}
        set -- a b c
        echo "$10$20$30"

引用
--------------------

.. tip::
    * 除非需要小心不带引用的扩展，否则总是引用包含变量、命令替换符、空格或shell元字符的字符串。
    * 推荐引用是单词的字符串（而不是命令选项或者路径名）。
    * 千万不要引用整数。
    * 注意 ``[[`` 中模式匹配的引用规则。
    * 请使用 ``$@`` 除非你有特殊原因需要使用 ``$*`` 。

    .. code-block:: shell

        # 'Single' quotes indicate that no substitution is desired.
        # "Double" quotes indicate that substitution is required/tolerated.

        # Simple examples
        # "quote command substitutions"
        flag="$(some_command and its args "$@" 'quoted separately')"

        # "quote variables"
        echo "${flag}"

        # "never quote literal integers"
        value=32
        # "quote command substitutions", even when you expect integers
        number="$(generate_number)"

        # "prefer quoting words", not compulsory
        readonly USE_INTEGER='true'

        # "quote shell meta characters"
        echo 'Hello stranger, and well met. Earn lots of $$$'
        echo "Process $$: Done making \$\$\$."

        # "command options or path names"
        # ($1 is assumed to contain a value here)
        grep -li Hugo /dev/null "$1"

        # Less simple examples
        # "quote variables, unless proven false": ccs might be empty
        git send-email --to "${reviewers}" ${ccs:+"--cc" "${ccs}"}

        # Positional parameter precautions: $1 might be unset
        # Single quotes leave regex as-is.
        grep -cP '([Ss]pecial|\|?characters*)$' ${1:+"$1"}

        # For passing on arguments,
        # "$@" is right almost everytime, and
        # $* is wrong almost everytime:
        #
        # * $* and $@ will split on spaces, clobbering up arguments
        #   that contain spaces and dropping empty strings;
        # * "$@" will retain arguments as-is, so no args
        #   provided will result in no args being passed on;
        #   This is in most cases what you want to use for passing
        #   on arguments.
        # * "$*" expands to one argument, with all args joined
        #   by (usually) spaces,
        #   so no args provided will result in one empty string
        #   being passed on.
        # (Consult 'man bash' for the nit-grits ;-)

        set -- 1 "2 two" "3 three tres"; echo $# ; set -- "$*"; echo "$#, $@")
        set -- 1 "2 two" "3 three tres"; echo $# ; set -- "$@"; echo "$#, $@")

