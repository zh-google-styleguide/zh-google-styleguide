Python风格规范
================================

分号
--------------------

.. tip::
    不要在行尾加分号, 也不要用分号将两条语句合并到一行.

.. _line_length:    
    
行宽
--------------------

.. tip::
    最大行宽是 80 个字符.
   
例外:
 
#. 长的导入 (import) 语句.
#. 注释里的 URL、路径名以及长的标志 (flag).
#. 不便于换行、不包含空格、模块级的长字符串常量, 比如 URL 或路径名.
#. Pylint 禁用注释. (例如: ``# pylint: disable=invalid-name``)

不要用反斜杠表示 `显式续行 (explicit line continuation) <https://docs.python.org/3/reference/lexical_analysis.html#explicit-line-joining>`_.

应该利用 Python 的 `圆括号, 中括号和花括号的隐式续行 (implicit line joining) <http://docs.python.org/2/reference/lexical_analysis.html#implicit-line-joining>`_ . 如有需要, 你可以在表达式外围添加一对括号. 

正确:

.. code-block:: python

    foo_bar(self, width, height, color='黑', design=None, x='foo',
            emphasis=None, highlight=0)

    if (width == 0 and height == 0 and
        color == '红' and emphasis == '加粗'):

    (bridge_questions.clarification_on
     .average_airspeed_of.unladen_swallow) = '美国的还是欧洲的?'

    with (
        very_long_first_expression_function() as spam,
        very_long_second_expression_function() as beans,
        third_thing() as eggs,
    ):
        place_order(eggs, beans, spam, beans)

错误:

.. code-block:: python

    if width == 0 and height == 0 and \
        color == '红' and emphasis == '加粗':

    bridge_questions.clarification_on \
        .average_airspeed_of.unladen_swallow = '美国的还是欧洲的?'

    with very_long_first_expression_function() as spam, \
            very_long_second_expression_function() as beans, \
            third_thing() as eggs:
        place_order(eggs, beans, spam, beans)

如果字符串的字面量 (literal) 超过一行, 应该用圆括号实现隐式续行:

.. code-block:: python

    x = ('这是一个很长很长很长很长很长很长'
         '很长很长很长很长很长的字符串')

最好在最外层的语法结构上分行. 如果你需要多次换行, 应该在同一层语法结构上换行.

正确:

.. code-block:: python

    bridgekeeper.answer(
         name="亚瑟", quest=questlib.find(owner="亚瑟", perilous=True))

     answer = (a_long_line().of_chained_methods()
               .that_eventually_provides().an_answer())

     if (
         config is None
         or 'editor.language' not in config
         or config['editor.language'].use_spaces is False
     ):
       use_tabs()

错误:

.. code-block:: python

    bridgekeeper.answer(name="亚瑟", quest=questlib.find(
        owner="亚瑟", perilous=True))

    answer = a_long_line().of_chained_methods().that_eventually_provides(
        ).an_answer()

    if (config is None or 'editor.language' not in config or config[
        'editor.language'].use_spaces is False):
      use_tabs()

必要时, 注释中的长 URL 可以独立成行.

正确:

.. code-block:: python

    # 详情参见
    # http://www.example.com/us/developer/documentation/api/content/v2.0/csv_file_name_extension_full_specification.html

错误:

.. code-block:: python

    # 详情参见
    # http://www.example.com/us/developer/documentation/api/content/\
    # v2.0/csv_file_name_extension_full_specification.html     

注意上面各个例子中的缩进; 详情参见 :ref:`缩进 <indentation>` 章节的解释. 

如果一行超过 80 个字符, 且 `Black <https://github.com/psf/black>`_ 或 `Pyink <https://github.com/google/pyink>`_ 自动格式化工具无法继续缩减行宽, 则允许该行超过 80 个字符. 我们也鼓励作者根据上面的规则手动拆分.
    
括号
--------------------

.. tip::
    使用括号时宁缺毋滥.

可以把元组 (tuple) 括起来, 但不强制. 不要在返回语句或条件语句中使用括号, 除非用于隐式续行或表示元组.

正确:

.. code-block:: python    
  
    if foo: 
        bar()
    while x:
        x = bar()
    if x and y:
        bar()
    if not x:
        bar()
    # 对于包含单个元素的元组, 括号比逗号更直观.
    onesie = (foo,)
    return foo
    return spam, beans
    return (spam, beans)
    for (x, y) in dict.items(): ...

错误:

.. code-block:: python
       
    if (x):
        bar()
    if not(x):
        bar()
    return (foo)
         
.. _indentation:  

缩进
--------------------

.. tip::
    用4个空格作为缩进.
    
不要使用制表符. 使用隐式续行时, 应该把括起来的元素垂直对齐(参见 :ref:`行宽 <line_length>` 章节的示例), 或者添加4个空格的悬挂缩进. 右括号 (圆括号, 方括号或花括号) 可以置于表达式结尾或者另起一行. 另起一行时右括号应该和左括号所在的那一行缩进相同.

正确:

.. code-block:: python

    # 与左括号对齐.
    foo = long_function_name(var_one, var_two,
                             var_three, var_four)
    meal = (spam,
            beans)

    # 与字典的左括号对齐.
    foo = {
        'long_dictionary_key': value1 +
                               value2,
        ...
    }

    # 4个空格的悬挂缩进; 首行没有元素
    foo = long_function_name(
        var_one, var_two, var_three,
        var_four)
    meal = (
        spam,
        beans)

    # 4个空格的悬挂缩进; 首行没有元素
    # 右括号另起一行.
    foo = long_function_name(
        var_one, var_two, var_three,
        var_four
    )
    meal = (
        spam,
        beans,
    )

    # 字典中的4空格悬挂缩进.
    foo = {
        'long_dictionary_key':
            long_dictionary_value,
        ...
    }

错误:

.. code-block:: python

    # 首行不能有元素.
    foo = long_function_name(var_one, var_two,
        var_three, var_four)

    # 禁止2个空格的悬挂缩进.
    foo = long_function_name(
      var_one, var_two, var_three,
      var_four)

    # 字典没有悬挂缩进.
    foo = {
        'long_dictionary_key':
        long_dictionary_value,
        ...
    }
         
序列的尾部要添加逗号吗?
-----------------------

.. tip::
    仅当 ``]``, ``)``, ``}`` 和最后一个元素不在同一行时, 推荐在序列尾部添加逗号. 我们的 Python 自动格式化工具会把尾部的逗号视为一种格式提示.

Shebang行
--------------------

.. tip::
    大部分 ``.py`` 文件不必以 ``#!`` 开始. 可以根据 `PEP-394 <http://www.python.org/dev/peps/pep-0394/>`_ , 在程序的主文件开头添加 ``#!/usr/bin/env python3`` (以支持 virtualenv) 或者 ``#!/usr/bin/python3``.

(译者注: 在计算机科学中, `Shebang <http://en.wikipedia.org/wiki/Shebang_(Unix)>`_ (也称为Hashbang)是一个由井号和叹号构成的字符串行(#!), 其出现在文本文件的第一行的前两个字符. 在文件中存在Shebang的情况下, 类Unix操作系统的程序载入器会分析Shebang后的内容, 将这些内容作为解释器指令, 并调用该指令, 并将载有Shebang的文件路径作为该解释器的参数. 例如, 以指令#!/bin/sh开头的文件在执行时会实际调用/bin/sh程序.)

内核会通过这行内容找到Python解释器, 但是Python解释器在导入模块时会忽略这行内容. 这行内容仅对需要直接运行的文件有效.

.. _comments:  
 
注释和文档字符串 (docstring)
----------------------------

.. tip::
    模块、函数、方法的文档字符串和内部注释一定要采用正确的风格.    

**文档字符串**

    Python 的文档字符串用于注释代码. 文档字符串是包、模块、类或函数里作为第一个语句的字符串. 可以用对象的 ``__doc__`` 成员自动提取这些字符串, 并为 ``pydoc`` 所用. (可以试试在你的模块上运行 ``pydoc`` 并观察结果). 文档字符串一定要用三重双引号 ``"""`` 的格式 (依据 `PEP-257 <http://www.python.org/dev/peps/pep-0257/>`_ ). 文档字符串应该是一行概述 (整行不超过 80 个字符), 以句号、问号或感叹号结尾. 如果要写更多注释 (推荐), 那么概述后面必须紧接着一个空行, 然后是剩下的内容, 缩进与文档字符串的第一行第一个引号对齐. 下面是更多有关文档字符串的格式规范. 

**模块**

    每个文件应该包含一个许可协议模版. 应根据项目使用的许可协议 (例如, Apache 2.0, BSD, LGPL, GPL) 选择合适的模版.

    文件的开头应该是文档字符串, 其中应该描述该模块内容和用法.

    .. code-block:: python

        """模块或程序的一行概述, 以句号结尾.

        留一个空行. 接下来应该写模块或程序的总体描述. 也可以选择简要描述导出的类和函数,
        和/或描述使用示例.

        经典的使用示例:

        foo = ClassFoo()
        bar = foo.FunctionBar()
        """

**测试模块**

    测试文件不必包含模块级文档字符串. 只有在文档字符串可以提供额外信息时才需要写入文件.

    例如, 你可以描述运行测试时所需的特殊要求, 解释不常见的初始化模式, 描述外部环境的依赖等等.

    .. code-block:: python

        """这个blaze测试会使用样板文件（golden files）.

        若要更新这些文件, 你可以在 `google3` 文件夹中运行
        `blaze run //foo/bar:foo_test -- --update_golden_files`
        """

    不要使用不能提供额外信息的文档字符串.

    .. code-block:: python

        """foo.bar 的测试."""

**函数和方法**
   
    本节中的函数是指函数、方法、生成器 (generator) 和特性 (property).

    满足下列任意特征的任何函数都必须有文档字符串:

    #. 公开 API 的一部分
    #. 长度过长
    #. 逻辑不能一目了然

    文档字符串应该提供充分的信息, 让调用者无需阅读函数的代码就能调用函数. 文档字符串应该描述函数的调用语法和语义信息, 而不应该描述具体的实现细节, 除非这些细节会影响函数的用法. 比如, 如果函数的副作用是会修改某个传入的对象, 那就需要在文档字符串中说明. 对于微妙、重要但是与调用者无关的实现细节, 相较于在文档字符串里说明, 还是在代码中间加注释更好.

    文档字符串可以是陈述句 (``"""Fetches rows from a Bigtable."""``) 或者祈使句 (``"""Fetch rows from a Bigtable."""``), 不过一个文件内的风格应当一致. 对于 ``@property`` 修饰的数据描述符 (data descriptor), 文档字符串应采用和属性 (attribute) 或 :ref:`函数参数 <doc_function_args>` 一样的风格 (``"""Bigtable 路径."""`` 而非 ``"""返回 Bigtable 路径."""``).

    对于覆写 (override) 基类 (base class) 方法的子类方法, 可以用简单的文档字符串引导读者阅读基类方法的文档字符串, 比如 ``"""参见基类.""""``. 这样是为了避免到处复制基类方法中已有的文档字符串. 然而, 如果覆写的子类方法与基类方法截然不同, 或者有更多细节需要记录 (例如有额外的的副作用), 那么子类方法的文档字符串中至少要描述这些区别.
    
    函数的部分特征应该在以下列出特殊小节中记录. 每小节有一行标题, 标题以冒号结尾. 除标题行外, 小节的其他部分应有2个或4个空格 (同一文件内应保持一致) 的悬挂缩进. 如果函数名和函数签名 (signature) 可以见名知意, 以至于一行文档字符串就能恰当地描述该函数, 那么可以省略这些小节.

.. _doc_function_args:    

    Args: (参数:)
        列出所有参数名. 参数名后面是一个冒号, 然后是一个空格或者换行符, 最后是描述. 如果描述过长以至于一行超出了 80 字符, 则描述部分应该比参数名所在的行多2个或者4个空格 (文件内应当一致) 的悬挂缩进. 如果代码没有类型注解, 则描述中应该说明所需的类型. 如果一个函数有形如 ``*foo`` (可变长参数列表) 或者 ``**bar`` (任意关键字参数) 的参数, 那么列举参数名时应该写成 ``*foo`` 和 ``**bar`` 的这样的格式.

    Returns: ("返回:")
        生成器应该用 "Yields:" ("生成:" )

        描述返回值的类型和意义. 如果函数仅仅返回 ``None``, 这一小节可以省略. 如果文档字符串以 Returns (返回) 或者 Yields (生成) 开头 (例如 ``"""返回 Bigtable 的行, 类型是字符串构成的元组."""``) 且这句话已经足以描述返回值, 也可以省略这一小节. 不要模仿 Numpy 风格的文档 (`例子 <http://numpy.org/doc/stable/reference/generated/numpy.linalg.qr.html>`_). 他们在文档中记录作为返回值的元组时, 写得就像返回值是多个值且每个值都有名字 (没有提到返回的是元组). 应该这样描述此类情况: "返回: 一个元组 (mat_a, mat_b), 其中 mat_a 是..., 且 ...". 文档字符串中使用的辅助名称不需要和函数体的内部变量名一致 (因为这些名称不是 API 的一部分).

    Raises: (抛出:)
        列出与接口相关的所有异常和异常描述. 用类似 Args (参数) 小节的格式，写成异常名+冒号+空格/换行, 并添加悬挂缩进. 不要在文档中记录违反 API 的使用条件时会抛出的异常 (因为这会让违背 API 时出现的效果成为 API 的一部分, 这是矛盾的).

    .. code-block:: python

        def fetch_smalltable_rows(
            table_handle: smalltable.Table,
            keys: Sequence[bytes | str],
            require_all_keys: bool = False,
        ) -> Mapping[bytes, tuple[str, ...]]:
            """从 Smalltable 获取数据行.

            从 table_handle 代表的 Table 实例中检索指定键值对应的行. 如果键值是字符串,
            字符串将用 UTF-8 编码.

            参数:
                table_handle: 处于打开状态的 smalltable.Table 实例.
                keys: 一个字符串序列, 代表要获取的行的键值. 字符串将用 UTF-8 编码.
                require_all_keys: 如果为 True, 只返回那些所有键值都有对应数据的
                    行.

            返回:
                一个字典, 把键值映射到行数据上. 行数据是字符串构成的元组. 例如:

                {b'Serak': ('Rigel VII', 'Preparer'),
                 b'Zim': ('Irk', 'Invader'),
                 b'Lrrr': ('Omicron Persei 8', 'Emperor')}

                返回的键值一定是字节串. 如果字典中没有 keys 参数中的某个键值, 说明
                表格中没有找到这一行 (且 require_all_keys 一定是 false).

            抛出:
                IOError: 访问 smalltable 时出现错误.
            """

    以下这种在 Args (参数) 小节中换行的写法也是可以的:

    .. code-block:: python

        def fetch_smalltable_rows(
            table_handle: smalltable.Table,
            keys: Sequence[bytes | str],
            require_all_keys: bool = False,
        ) -> Mapping[bytes, tuple[str, ...]]:
            """从 Smalltable 获取数据行.

            从 table_handle 代表的 Table 实例中检索指定键值对应的行. 如果键值是字符串,
            字符串将用 UTF-8 编码.

            参数:
                table_handle:
                  处于打开状态的 smalltable.Table 实例.
                keys:
                  一个字符串序列, 代表要获取的行的键值. 字符串将用 UTF-8 编码.
                require_all_keys:
                  如果为 True, 只返回那些所有键值都有对应数据的行.

            返回:
                一个字典, 把键值映射到行数据上. 行数据是字符串构成的元组. 例如:

                {b'Serak': ('Rigel VII', 'Preparer'),
                 b'Zim': ('Irk', 'Invader'),
                 b'Lrrr': ('Omicron Persei 8', 'Emperor')}

                返回的键值一定是字节串. 如果字典中没有 keys 参数中的某个键值, 说明
                表格中没有找到这一行 (且 require_all_keys 一定是 false).

            抛出:
                IOError: 访问 smalltable 时出现错误.
            """

**类 (class)**
            
    类的定义下方应该有一个描述该类的文档字符串. 如果你的类包含公有属性 (attributes), 应该在 ``Attributes`` (属性) 小节中记录这些属性, 格式与函数的 ``Args`` (参数) 小节类似.

    .. code-block:: python

        class SampleClass(object):
            """这里是类的概述.

            这里是更多信息....
            这里是更多信息....

            属性:
                likes_spam: 布尔值, 表示我们是否喜欢午餐肉.
                eggs: 用整数记录的下蛋的数量.
            """

            def __init__(self, likes_spam = False):
                """用某某某初始化 SampleClass."""
                self.likes_spam = likes_spam
                self.eggs = 0

            def public_method(self):
                """执行某某操作."""

    类的文档字符串开头应该是一行概述, 描述类的实例所代表的事物. 这意味着 ``Exception`` 的子类 (subclass) 应该描述这个异常代表什么, 而不是描述抛出异常时的环境. 类的文档字符串不应该有无意义的重复, 例如说这个类是一种类.

    正确:

    .. code-block:: python

        class CheeseShopAddress:
        """奶酪店的地址.

        ...
        """

        class OutOfCheeseError(Exception):
        """没有可用的奶酪."""
    
    错误:

    .. code-block:: python

        class CheeseShopAddress:
        """一个描述奶酪店地址的类.

        ...
        """

        class OutOfCheeseError(Exception):
        """在没有可用的奶酪时抛出."""

**块注释和行注释**

    最后一种需要写注释的地方是代码中复杂的部分. 如果你可能在以后 `代码评审 (code review) <http://en.wikipedia.org/wiki/Code_review>`_ 时要解释某段代码, 那么现在就应该给这段代码加上注释. 应该在复杂的操作开始前写上若干行注释. 对于不是一目了然的代码, 应该在行尾添加注释. 

    .. code-block:: python

        # 我们用加权的字典搜索, 寻找 i 在数组中的位置. 我们基于数组中的最大值和数组
        # 长度, 推断一个位置, 然后用二分搜索获得最终准确的结果.

        if i & (i-1) == 0:  # 如果 i 是 0 或者 2 的整数次幂, 则为真.

    为了提高可读性, 注释的井号和代码之间应有至少2个空格, 井号和注释之间应该至少有一个空格.

    除此之外, 绝不要仅仅描述代码. 应该假设读代码的人比你更懂Python, 只是不知道你的代码要做什么. 

    .. code-block:: python

        # 不好的注释: 现在遍历数组 b, 确保每次 i 出现时, 下一个元素是 i+1

标点符号、拼写和语法
--------------------

.. tip::
    注意标点符号、拼写和语法. 文笔好的注释比差的注释更容易理解.

注释应该和记叙文一样可读, 使用恰当的大小写和标点. 一般而言, 完整的句子比残缺句更可读. 较短的注释 (比如行尾注释) 可以更随意, 但是你要保持风格一致.

尽管你可能会因为代码审稿人指出你误把冒号写作逗号而灰心, 但是保持源代码清晰可读也是非常重要的. 正确的标点、拼写和语法有助于实现这一目标.

字符串
--------------------

.. tip::
    应该用 `f-string <https://docs.python.org/zh-cn/3/reference/lexical_analysis.html#f-strings>`_、 ``%`` 运算符或 ``format`` 方法来格式化字符串. 即使所有参数都是字符串, 也如此. 你可以自行评判合适的选项. 可以用 ``+`` 实现单次拼接, 但是不要用 ``+`` 实现格式化.

正确:

.. code-block:: python

    x = f'名称: {name}; 分数: {n}'
    x = '%s, %s!' % (imperative, expletive)
    x = '{}, {}'.format(first, second)
    x = '名称: %s; 分数: %d' % (name, n)
    x = '名称: %(name)s; 分数: %(score)d' % {'name':name, 'score':n}
    x = '名称: {}; 分数: {}'.format(name, n)
    x = a + b

错误:

.. code-block:: python

    x = first + ', ' + second
    x = '名称: ' + name + '; 分数: ' + str(n)

不要在循环中用 ``+`` 和 ``+=`` 操作符来堆积字符串. 这有时会产生平方而不是线性的时间复杂度. 有时 CPython 会优化这种情况, 但这是一种实现细节. 我们无法轻易预测这种优化是否生效, 而且未来情况可能出现变化. 作为替代方案, 你可以将每个子串加入列表, 然后在循环结束后用 ``''.join`` 拼接列表. 也可以将每个子串写入一个 ``io.StringIO`` 缓冲区中. 这些技巧保证始终有线性的平摊 (amortized) 时间复杂度.

正确:

.. code-block:: python

    items = ['<table>']
    for last_name, first_name in employee_list:
        items.append('<tr><td>%s, %s</td></tr>' % (last_name, first_name))
    items.append('</table>')
    employee_table = ''.join(items)

错误:

.. code-block:: python

    employee_table = '<table>'
    for last_name, first_name in employee_list:
        employee_table += '<tr><td>%s, %s</td></tr>' % (last_name, first_name)
    employee_table += '</table>'

应该保持同一文件中字符串引号的一致性. 选择 ``'`` 或者 ``"`` 以后不要改变主意. 如果需要避免用反斜杠来转义引号, 则可以使用另一种引号. 

正确:

.. code-block:: python

        Python('为什么你要捂眼睛?')
        Gollum("I'm scared of lint errors. (我害怕格式错误.)")
        Narrator('"很好!" 一个开心的 Python 审稿人心想.')

(译者注: 注意 "I'm" 中间有一个单引号，所以这一行的外层引号可以用不同的引号.)

错误:

.. code-block:: python
  
        Python("为什么你要捂眼睛?")
        Gollum('格式检查器. 它在闪耀. 它要亮瞎我们.')
        Gollum("伟大的格式检查器永在. 它在看. 它在看.")

多行字符串推荐使用 ``"""`` 而非 ``'''``. 当且仅当项目中用 ``'`` 给常规字符串打引号时, 才能在文档字符串以外的多行字符串上使用 ``'''``. 无论如何, 文档字符串必须使用 ``"""``.

多行字符串不会跟进代码其他部分的缩进. 如果需要避免字符串中的额外空格, 可以用多个单行字符串拼接, 或者用 `textwrap.dedent() <https://docs.python.org/zh-cn/3/library/textwrap.html#textwrap.dedent>`_ 删除每行开头的空格.

错误:

.. code-block:: python

        long_string = """这样很难看.
    不要这样做.
    """

正确:

.. code-block:: python

    long_string = """如果你可以接受多余的空格,
        就可以这样."""

    long_string = ("如果你不能接受多余的空格,\n" +
                   "可以这样.")

    long_string = ("如果你不能接受多余的空格,\n"
                   "也可以这样.")

.. code-block:: python

    import textwrap

    long_string = textwrap.dedent("""\
      这样也行, 因为 textwrap.dedent()
      会删除每一行开头共有的空格.""")

注意, 这里的反斜杠没有违反 :ref:`显式续行的禁令 <line_length>`. 此时, 反斜杠用于在字符串字面量 (literal) 中 `对换行符转义 <https://docs.python.org/zh-cn/3/reference/lexical_analysis.html#string-and-bytes-literals>`_.

**日志**

    对于那些第一个参数是格式字符串 (包含 ``%`` 占位符) 的日志函数: 一定要用字符串字面量 (而非 f-string!) 作为第一个参数, 并用占位符的参数作为其他参数. 有些日志的实现会收集未展开的格式字符串, 作为可搜索的项目. 这样也可以免于渲染那些被设置为不用输出的消息.

    正确；

    .. code-block:: python

        import tensorflow as tf
        logger = tf.get_logger()
        logger.info('TensorFlow 的版本是: %s', tf.__version__)

    .. code-block:: python

        import os
        from absl import logging

        logging.info('当前的 $PAGER 是: %s', os.getenv('PAGER', default=''))

        homedir = os.getenv('HOME')
        if homedir is None or not os.access(homedir, os.W_OK):
            logging.error('无法写入主目录, $HOME=%r', homedir)

    错误:

    .. code-block:: python

        import os
        from absl import logging

        logging.info('当前的 $PAGER 是:')
        logging.info(os.getenv('PAGER', default=''))

        homedir = os.getenv('HOME')
        if homedir is None or not os.access(homedir, os.W_OK):
            logging.error(f'无法写入主目录, $HOME={homedir!r}')

**错误信息**

    错误信息 (例如: 诸如 ``ValueError`` 等异常的信息字符串和展示给用户的信息) 应该遵守以下三条规范:

    #. 信息需要精确地匹配真正的错误条件.
    #. 插入的片段一定要能清晰地分辨出来.
    #. 要便于简单的自动化处理 (例如正则搜索, 也就是 grepping).

    正确:

    .. code-block:: python

        if not 0 <= p <= 1:
            raise ValueError(f'这不是概率值: {p!r}')

        try:
            os.rmdir(workdir)
        except OSError as error:
            logging.warning('无法删除这个文件夹 (原因: %r): %r',
                            error, workdir)

    错误:

    .. code-block:: python

        if p < 0 or p > 1:  # 问题: 遇到 float('nan') 时也为假!
            raise ValueError(f'这不是概率值: {p!r}')

        try:
            os.rmdir(workdir)
        except OSError:
            # 问题: 信息中存在错误的揣测，
            # 删除操作可能因为其他原因而失败, 此时会误导调试人员.
            logging.warning('文件夹已被删除: %s', workdir)

        try:
            os.rmdir(workdir)
        except OSError:
            # 问题: 这个信息难以搜索, 而且某些 `workdir` 的值会让人困惑.
            # 假如有人调用这段代码时让 workdir = '已删除'. 这个警告会变成:
            # "无法删除已删除文件夹."
            logging.warning('无法删除%s文件夹.', workdir)

文件、套接字 (socket) 和类似的有状态资源
--------------------------------------------

.. tip::
    使用完文件和套接字以后, 显式地关闭它们. 自然地, 这条规则也应该扩展到其他在内部使用套接字的可关闭资源 (比如数据库连接) 和其他需要用类似方法关停的资源. 其他例子还有 `mmap <https://docs.python.org/zh-cn/3/library/mmap.html>`_ 映射、 `h5py 的文件对象 <https://docs.h5py.org/en/stable/high/file.html>`_ 和 `matplotlib.pyplot 的图像窗口 <https://matplotlib.org/2.1.0/api/_as_gen/matplotlib.pyplot.close.html>`_ .

如果保持不必要的文件、套接字或其他有状态对象开启, 会产生很多缺点:

#. 它们可能消耗有限的系统资源, 例如文件描述符. 如果代码需要使用大量类似的资源而没有及时返还给系统, 就有可能出现原本可以避免的资源枯竭情况.
#. 保持文件的开启状态会阻碍其他操作, 例如移动、删除文件, 卸载 (unmont) 文件系统等等.
#. 如果程序的多个部分共享文件和套接字, 即使逻辑上文件已经关闭了, 仍然有可能出现意外的读写操作. 如果这些资源真正关闭了, 读写操作会抛出异常, 让问题早日浮出水面.

此外, 即使文件和套接字 (以及其他行为类似的资源) 会在析构 (destruct) 时自动关闭, 把对象的生命周期和资源状态绑定的行为依然不妥: 

#. 无法保证运行时 (runtime) 调用 ``__del__`` 方法的真正时机. 不同的 Python 实现采用了不同的内存管理技巧 (比如延迟垃圾处理机制, delayed garbage collection), 可能会随意、无限期地延长对象的生命周期.
#. 意想不到的文件引用 (例如全局对象和异常的堆栈跟踪, exception tracebacks) 可能让文件的存续时间比想象的更长.

依赖于终结器 (finalizer) 实现自动清理的方法有显著的副作用. 这在几十年的时间里、在多种语言中 (参见 `这篇 <https://wiki.sei.cmu.edu/confluence/display/java/MET12-J.+Do+not+use+finalizers>`_ Java 的文章) 多次引发严重问题.

推荐使用 `"with"语句 <https://docs.python.org/zh-cn/3/reference/compound_stmts.html#the-with-statement>`_ 管理文件和类似的资源:

.. code-block:: python

      with open("hello.txt") as hello_file:
          for line in hello_file:
              print line

对于不支持 ``with`` 语句且类似文件的对象, 应该使用 ``contextlib.closing()``:

.. code-block:: python

      import contextlib
      
      with contextlib.closing(urllib.urlopen("http://www.python.org/")) as front_page:
          for line in front_page:
              print line
              
少数情况下无法使用基于上下文 (context) 的资源管理, 此时文档应该清楚地解释代码会如何管理资源的生命周期.

TODO (待办) 注释
--------------------

.. tip::
    在临时、短期和不够完美的代码上添加 TODO (待办) 注释.

待办注释以 ``TODO`` (待办) 这个全部大写的词开头, 紧跟着是用括号括起来的上下文标识符 (最好是 bug 链接, 有时是你的用户名). 最好是诸如 ``TODO(https://crbug.com/<bug编号>):`` 这样的 bug 链接, 因为 bug 有历史追踪和评论, 而程序员可能发生变动并忘记上下文. TODO 后面应该解释待办的事情.

统一 TODO 的格式是为了方便搜索并查看详情. TODO 不代表注释中提到的人要做出修复问题的保证. 所以, 当你创建带有用户名的 TODO 时, 大部分情况下应该用你自己的用户名. 

.. code-block:: python

    # TODO(crbug.com/192795): 研究 cpufreq 的优化.
    # TODO(你的用户名): 提交一个议题 (issue), 用 '*' 代表重复.
    
如果你的 TODO 形式类似于"将来做某事", 请确保其中包含特别具体的日期 ("2009年11月前解决") 或者特别具体的事件 ("当所有客户端都能处理 XML 响应时, 删除这些代码"), 以便于未来的代码维护者理解.

导入 (import) 语句的格式
-------------------------

.. tip::
    导入语句应该各自独占一行. :ref:`typing 和 collections.abc 的导入除外 <typing_imports>`. 例如:

正确:

.. code-block:: python  
  
    from collections.abc import Mapping, Sequence
    import os
    import sys
    from typing import Any, NewType

错误:

.. code-block:: python  
   
    import os, sys
    
导入语句必须在文件顶部, 位于模块的注释和文档字符串之后、全局变量和全局常量之前. 导入语句应该按照如下顺序分组, 从通用到特殊:

#. 导入 Python 的 ``__future__``. 例如:

    .. code-block:: python

        from __future__ import annotations

    参见前文有关 ``__future__`` 语句的描述.

#. 导入 Python 的标准库. 例如:

    .. code-block:: python

        import sys

#. 导入 `第三方 <https://pypi.org/>`_ 模块和包. 例如:

    .. code-block:: python

        import tensorflow as tf

#. 导入代码仓库中的子包. 例如:

    .. code-block:: python

        from otherproject.ai import mind

#. **已废弃的规则**: 导入应用专属的、与该文件属于同一个子包的模块. 例如:

    .. code-block:: python

        from myproject.backend.hgwells import time_machine

    你可能会在较老的谷歌风格 Python 代码中遇到这样的模式, 但现在不再执行这条规则. **我们建议新代码忽略这条规则.** 同等对待应用专属的子包和其他子包即可.

在每个分组内部, 应该按照模块完整包路径 (例如 ``from path import ...`` 中的 ``path``) 的字典序排序, 忽略大小写. 可以选择在分组之间插入空行.

.. code-block:: python

    import collections
    import queue
    import sys

    from absl import app
    from absl import flags
    import bs4
    import cryptography
    import tensorflow as tf

    from book.genres import scifi
    from myproject.backend import huxley
    from myproject.backend.hgwells import time_machine
    from myproject.backend.state_machine import main_loop
    from otherproject.ai import body
    from otherproject.ai import mind
    from otherproject.ai import soul

    # 旧的代码可能会把这些导入语句放在下面这里:
    #from myproject.backend.hgwells import time_machine
    #from myproject.backend.state_machine import main_loop 

语句
--------------------

.. tip::
    通常每个语句应该独占一行.

不过, 如果判断语句的主体与判断条件可以挤进一行, 你可以将它们放在同一行. 特别注意这不适用于 ``try`` / ``except``, 因为 ``try`` 和 ``except`` 不能放在同一行. 只有在 ``if`` 语句没有对应的 ``else`` 时才适用.

正确:

.. code-block:: python

    if foo: bar(foo)

错误:

.. code-block:: python

      if foo: bar(foo)
      else:   baz(foo)

      try:               bar(foo)
      except ValueError: baz(foo)

      try:
          bar(foo)
      except ValueError: baz(foo)

.. _getter_setter:  

访问器 (getter) 和设置器 (setter)
--------------------------------------

.. tip::
    在访问和设置变量值时, 如果访问器和设置器 (又名为访问子 accessor 和变异子 mutator) 可以产生有意义的作用或效果, 则可以使用.

特别来说, 如果在当下或者可以预见的未来, 读写某个变量的过程很复杂或者成本高昂, 则应该使用这种函数.

如果一对访问器和设置器仅仅用于读写一个内部属性 (attribute), 你应该直接用公有属性取代它们. 相较而言, 如果设置操作会让部分状态无效化或引发重建, 则需要使用设置器. 显式的函数调用表示可能出现特殊的操作. 如果只有简单的逻辑, 或者在重构代码后不再需要访问器和设置器, 你可以用属性 (property) 替代. 

(译者注: 重视封装的面向对象程序员看到这个可能会很反感, 因为他们一直被教育: 所有成员变量都必须是私有的! 其实, 那真的是有点麻烦啊. 试着去接受Pythonic哲学吧)

访问器和设置器应该遵守命名规范, 例如 ``get_foo()`` 和 ``set_foo()``.

如果之前的代码通过属性获取数据, 则不能把重新编写的访问器/设置器与这一属性绑定. 应该让任何用老办法访问变量的代码出现显眼的错误, 让使用者意识到代码复杂度有变化.
    
命名
--------------------

.. tip::
    模块名: ``module_name``; 包名: ``package_name``; 类名: ``ClassName``; 方法名: ``method_name``; 异常名: ``ExceptionName``; 函数名: ``function_name``, ``query_proper_noun_for_thing``, ``send_acronym_via_https``; 全局常量名: ``GLOBAL_CONSTANT_NAME`` ; 全局变量名: ``global_var_name``; 实例名: ``instance_var_name``; 函数参数名: ``function_parameter_name``; 局部变量名: ``local_var_name``.

函数名、变量名和文件名应该是描述性的, 避免缩写. 特别要避免那些对于项目之外的人有歧义或不熟悉的缩写, 也不要通过省略单词中的字母来进行缩写.

必须用 ``.py`` 作为文件后缀名. 不要用连字符.

**需要避免的名称**
    
    #. 只有单个字符的名称, 除了以下特别批准的情况:

        #. 计数器和迭代器 (例如, ``i``, ``j``, ``k``, ``v`` 等等).
        #. 在 ``try/except`` 语句中代表异常的 ``e``.
        #. 在 ``with`` 语句中代表文件句柄的 ``f``.
        #. 私有的、没有约束 (constrain) 的类型变量 (type variable, 例如 ``_T = TypeVar("_T")``, ``_P = ParamSpec("_P")``).

    #. 包含连字符(``-``) 的包名/模块名.
    #. 首尾均为双下划线的名称, 例如 ``__double_leading_and_trailing_underscore__`` (此类名称是 Python 的保留名称).
    #. 包含冒犯性词语的名称.
    #. 在不必要的情况下包含变量类型的名称 (例如 ``id_to_name_dict``).
    
**命名规范**
    
    #. "内部(Internal)"一词表示仅在模块内可用, 或者在类内是受保护/私有的.
    #. 在一定程度上, 在名称前加单下划线 (``_``) 可以保护模块变量和函数 (格式检查器会对受保护的成员访问操作发出警告).
    #. 在实例的变量或方法名称前加双下划线 (``__``, 又名为 dunder) 可以有效地把变量或方法变成类的私有成员 (基于名称修饰 name mangling 机制). 我们不鼓励这种用法, 因为这会严重影响可读性和可测试性, 而且没有 **真正** 实现私有. 建议使用单下划线.
    #. 应该把相关的类和顶级函数放在同一个模块里. 与Java不同, 不必限制一个模块只有一个类.
    #. 类名应该使用首字母大写的形式 (如 CapWords), 但是模块名应该用小写加下划线的形式 (如 lower_with_under.py). 尽管有些旧的模块使用类似于 CapWords.py 这样的形式, 现在我们不再鼓励这种命名方式, 因为模块名和类名相同时会让人困惑 ("等等, 我刚刚写的是 ``import StringIO`` 还是 ``from StringIO import StringIO``?").
    #. 新的 **单元测试** 文件应该遵守 PEP 8, 用小写加下划线格式的方法名, 例如 ``test_<被测试的方法名>_<状态>``. 有些老旧的模块有形如 ``CapWords`` 这样大写的方法名, 为了保持风格一致, 可以在 test 这个词和方法名之后, 用下划线分割名称中不同的逻辑成分. 比如一种可行的格式之一是 ``test<被测试的方法>_<状态>``.

**文件名**

    所有 Python 文件名都应该以 ``.py`` 为文件后缀且不能包含连字符 (``-``). 这样便于导入这些文件并编写单元测试. 如果想通过不含后缀的命令运行程序, 可以使用软链接文件 (symbolic link) 或者 ``exec "$0.py" "$@"`` 这样简单的 bash 脚本.

**根据Python之父Guido的建议所制定的规范**

.. list-table:: 描述
   :widths: 30 30 40
   :header-rows: 1

   * - 类型
     - 公有
     - 内部
   * - 包
     - 小写下划线
     -
   * - 模块
     - 小写下划线
     - 下划线+小写下划线
   * - 类
     - 大驼峰
     - 下划线+大驼峰
   * - 异常
     - 大驼峰
     -
   * - 函数
     - 小写下划线
     - 下划线+小写下划线
   * - 全局常量/类常量
     - 大写下划线
     - 下划线+大写下划线
   * - 全局变量/类变量
     - 小写下划线
     - 下划线+小写下划线
   * - 实例变量
     - 小写下划线
     - 下划线+小写下划线 (受保护)
   * - 方法名
     - 小写下划线
     - 下划线+小写下划线 (受保护)
   * - 函数参数/方法参数
     - 小写下划线
     -
   * - 局部变量
     - 小写下划线
     -

.. list-table:: 例子
   :widths: 30 35 35
   :header-rows: 1

   * - 类型
     - 公有
     - 内部
   * - 包
     - ``lower_with_under``
     -
   * - 模块
     - ``lower_with_under``
     - ``_lower_with_under``
   * - 类
     - ``CapWords``
     - ``_CapWords``
   * - 异常
     - ``CapWords``
     -
   * - 函数
     - ``lower_with_under()``
     - ``_lower_with_under()``
   * - 全局常量/类常量
     - ``CAPS_WITH_UNDER``
     - ``_CAPS_WITH_UNDER``
   * - 全局变量/类变量
     - ``lower_with_under``
     - ``_lower_with_under``
   * - 实例变量
     - ``lower_with_under``
     - ``_lower_with_under``
   * - 方法名
     - ``lower_with_under()``
     - ``_lower_with_under()``
   * - 函数参数/方法参数
     - ``lower_with_under``
     -
   * - 局部变量
     - ``lower_with_under``
     -

**数学符号**

对于涉及大量数学内容的代码, 如果相关论文或算法中有对应的符号, 则可以忽略以上命名规范并使用较短的变量名. 若要采用这种方法, 应该在注释或者文档字符串中注明你所使用的命名规范的来源. 如果原文无法访问, 则应该在文档中清楚地记录命名规范. 建议公开的 API 使用符合 PEP8 的、描述性的名称, 因为使用 API 的代码很可能缺少相关的上下文信息.

主程序
--------------------

.. tip::
    使用 Python 时, 提供给 ``pydoc`` 和单元测试的模块必须是可导入的. 如果一个文件是可执行文件, 该文件的主要功能应该位于 ``main()`` 函数中. 你的代码必须在执行主程序前检查 ``if __name__ == '__main__'`` , 这样导入模块时不会执行主程序.

使用 `absl <https://github.com/abseil/abseil-py>`_ 时, 请调用 ``app.run`` :

.. code-block:: python

    from absl import app
    ...

    def main(argv):
        # 处理非标志 (non-flag) 参数
        ...

    if __name__ == '__main__':
        app.run(main)

否则, 使用:

.. code-block:: python

    def main():
        ...

    if __name__ == '__main__':
        main()

导入模块时会执行该模块的所有顶级代码. 注意顶级代码中不能有 ``pydoc`` 不该执行的操作, 比如调用函数, 创建对象等.

函数长度
--------------------

.. tip::
    函数应该小巧且专一.

我们承认有时长函数也是合理的, 所以不硬性限制函数长度. 若一个函数超过 40 行, 应该考虑在不破坏程序结构的前提下拆分这个函数.

即使一个长函数现在没有问题, 几个月后可能会有别人添加新的效果. 此时容易出现隐蔽的错误. 保持函数简练, 这样便于别人阅读并修改你的代码.

当你使用某些代码时, 可能发现一些冗长且复杂的函数. 要勇于修改现有的代码: 如果该函数难以使用或者存在难以调试的错误, 亦或是你想在不同场景下使用该函数的片段, 不妨考虑把函数拆分成更小、更容易管理的片段.

类型注解 (type annotation)
-------------------------------

**通用规则** 

    #. 熟读 `PEP-484 <https://www.python.org/dev/peps/pep-0484/>`_ .
    #. 仅在有额外类型信息时才需要注解方法中 ``self`` 或 ``cls`` 的类型. 例如:

        .. code-block:: python

            @classmethod
            def create(cls: Type[_T]) -> _T:
                return cls()

    #. 类似地, 不需要注解 ``__init__`` 的返回值 (只能返回 ``None``).
    #. 对于其他不需要限制变量类型或返回类型的情况, 应该使用 ``Any``.
    #. 无需注解模块中的所有函数.

        #. 至少需要注解你的公开 API.
        #. 你可以自行权衡, 一方面要保证代码的安全性和清晰性, 另一方面要兼顾灵活性.
        #. 应该注解那些容易出现类型错误的代码 (比如曾经出现过错误或疑难杂症).
        #. 应该注解晦涩难懂的代码.
        #. 应该注解那些类型已经确定的代码. 多数情况下，即使注解了成熟的代码中所有的函数，也不会丧失太多灵活性.

**换行**

    尽量遵守前文所述的缩进规则.
    
    添加类型注解后, 很多函数签名 (signature) 会变成每行一个参数的形式. 若要让返回值单独成行, 可以在最后一个参数尾部添加逗号.

    .. code-block:: python

        def my_method(
            self,
            first_var: int,
            second_var: Foo,
            third_var: Bar | None,
        ) -> int:
            ...
    
    尽量在变量之间换行, 避免在变量和类型注解之间换行. 当然, 若所有东西可以挤进一行, 也可以接受.

    .. code-block:: python

        def my_method(self, first_var: int) -> int:
            ...

    若最后一个参数加上返回值的类型注解太长, 也可以换行并添加4格缩进. 添加换行符时, 建议每个参数和返回值都在单独的一行里, 并且右括号和 ``def`` 对齐.

    正确:

    .. code-block:: python

        def my_method(
            self,
            other_arg: MyLongType | None,
        ) -> tuple[MyLongType1, MyLongType1]:
            ...
    
    返回值类型和最后一个参数也可以放在同一行.

    可以接受:

    .. code-block:: python

        def my_method(
            self,
            first_var: int,
            second_var: int) -> dict[OtherLongType, MyLongType]:
            ...

    ``pylint`` 也允许你把右括号放在新行上, 与左括号对齐, 但相较而言可读性更差.

    错误:

    .. code-block:: python

        def my_method(self,
                      other_arg: MyLongType | None,
                     ) -> dict[OtherLongType, MyLongType]:
            ... 

    正如上面所有的例子, 尽量不要在类型注解中间换行. 但是有时注解过长以至于一行放不下. 此时尽量保持子类型中间不换行.

    .. code-block:: python

        def my_method(
            self,
            first_var: tuple[list[MyLongType1],
                             list[MyLongType2]],
            second_var: list[dict[
                MyLongType3, MyLongType4]],
        ) -> None:
            ...

    若某个名称和对应的类型注解过长, 可以考虑用 :ref:`别名 (alias) <type_alias>` 代表类型. 下策是在冒号后换行并添加4格缩进.

    正确:

    .. code-block:: python

        def my_function(
            long_variable_name:
                long_module_name.LongTypeName,
        ) -> None:
            ...

    错误:

    .. code-block:: python

        def my_function(
            long_variable_name: long_module_name.
                LongTypeName,
        ) -> None:
            ...

**前向声明 (foward declaration)**

    若需要使用一个尚未定义的类名 (比如想在声明一个类时使用自身的类名), 可以使用 ``from __future__ import annotations`` 或者字符串来代表类名.

    正确:

    .. code-block:: python
        
        from __future__ import annotations

        class MyClass:
            def __init__(self, stack: Sequence[MyClass], item: OtherClass) -> None:

        class OtherClass:
            ...

    .. code-block:: python

        class MyClass:
            def __init__(self, stack: Sequence['MyClass'], item: 'OtherClass') -> None:

        class OtherClass:
            ...

**默认值**

    根据 `PEP-008 <https://www.python.org/dev/peps/pep-0008/#other-recommendations>`_ , **只有** 对于同时拥有类型注解和默认值的参数, ``=`` 的周围应该加空格.

    正确:

    .. code-block:: python

        def func(a: int = 0) -> int:
            ...

    错误:

    .. code-block:: python

        def func(a:int=0) -> int:
            ...

**NoneType**

    在 Python 的类型系统中, ``NoneType`` 是 "一等" 类型. 在类型注解中, ``None`` 是 ``NoneType`` 的别名. 如果一个变量可能为 ``None``, 则必须声明这种情况! 你可以使用 ``|`` 这样的并集 (union) 类型表达式 (推荐在新的 Python 3.10+ 代码中使用) 或者老的 ``Optional`` 和 ``Union`` 语法.

    应该用显式的 ``X | None`` 替代隐式声明. 早期的 PEP 484 允许将 ``a: str = None`` 解释为 ``a: str | None = None``, 但这不再是推荐的行为.

    正确:

    .. code-block:: python
        
        # 现代的并集写法.
        def modern_or_union(a: str | int | None, b: str | None = None) -> str:
            ...
        # 采用 Union / Optional.
        def union_optional(a: Union[str, int, None], b: Optional[str] = None) -> str:
            ...

    错误:

    .. code-block:: python

        # 用 Union 代替 Optional.
        def nullable_union(a: Union[None, str]) -> str:
            ...
        # 隐式 Optional.
        def implicit_optional(a: str = None) -> str:
            ...

.. _type_alias:

**类型别名 (alias)**

    你可以为复杂的类型声明一个别名. 别名的命名应该采用大驼峰 (例如 ``CapWorded``). 若别名仅在当前模块使用, 应在名称前加 ``_`` 代表私有 (例如 ``_Private``).

    注意下面的 ``: TypeAlias`` 类型注解只能在 3.10 以后的版本使用.

    .. code-block:: python
       
        from typing import TypeAlias

        _LossAndGradient: TypeAlias = tuple[tf.Tensor, tf.Tensor]
        ComplexTFMap: TypeAlias = Mapping[str, _LossAndGradient]

**忽略类型**
    
    你可以使用特殊的注释 ``# type: ignore`` 禁用某一行的类型检查.

    ``pytype`` 有针对特定错误的禁用选项 (类似格式检查器):

    .. code-block:: python
        
        # pytype: disable=attribute-error

**标注变量的类型**

    **带类型注解的赋值**
        
    如果难以自动推理某个内部变量的类型, 可以用带类型注解的赋值操作来指定类型: 在变量名和值的中间添加冒号和类型, 类似于有默认值的函数参数.
    
        .. code-block:: python

            a: Foo = SomeUndecoratedFunction()

    **类型注释**

    你可能在代码仓库中看到这种残留的注释 (在 Python 3.6 之前必须这样写注释), 但是不要再添加 ``# type: <类型>`` 这样的行尾注释了:

        .. code-block:: python
    
            a = SomeUndecoratedFunction()  # type: Foo

**元组还是列表**

    有类型的列表中只能有一种类型的元素. 有类型的元组可以有相同类型的元素或者若干个不同类型的元素. 后面这种情况多用于注解返回值的类型.

    (译者注: 注意这里是指的类型注解中的写法,实际python中,list和tuple都是可以在一个序列中包含不同类型元素的,当然,本质其实list和tuple中放的是元素的引用)

    .. code-block:: python

        a: list[int] = [1, 2, 3]
        b: tuple[int, ...] = (1, 2, 3)
        c: tuple[int, str, float] = (1, "2", 3.5)

**类型变量 (type variable)**

    Python 的类型系统支持 `泛型 (generics) <https://peps.python.org/pep-0484/#generics>`_ . 使用泛型的常见方式是利用类型变量, 例如 ``TypeVar`` 和 ``ParamSpec``.

    例如:

    .. code-block:: python

        from collections.abc import Callable
        from typing import ParamSpec, TypeVar
        _P = ParamSpec("_P")
        _T = TypeVar("_T")
        ...
        def next(l: list[_T]) -> _T:
            return l.pop()

        def print_when_called(f: Callable[_P, _T]) -> Callable[_P, _T]:
            def inner(*args: P.args, **kwargs: P.kwargs) -> R:
                print('函数被调用')
                return f(*args, **kwargs)
        return inner

    ``TypeVar`` 可以有约束条件.

    .. code-block:: python
        
        AddableType = TypeVar("AddableType", int, float, str)
        def add(a: AddableType, b: AddableType) -> AddableType:
            return a + b

    ``AnyStr`` 是 ``typing`` 模块中常用的预定义类型变量. 可以用它注解那些接受 ``bytes`` 或 ``str`` 但是必须保持一致的类型.

    .. code-block:: python

        from typing import AnyStr
        def check_length(x: AnyStr) -> AnyStr:
            if len(x) <= 42:
                return x
            raise ValueError()
    
    (译者注: 这个例子中, x 和返回值必须同时是 ``bytes`` 或者同时是 ``str``.)

    类型变量必须有描述性的名称, 除非满足以下所有标准:

    #. 外部不可见
    #. 没有约束条件

    正确:

    .. code-block:: python

        _T = TypeVar("_T")
        _P = ParamSpec("_P")
        AddableType = TypeVar("AddableType", int, float, str)
        AnyFunction = TypeVar("AnyFunction", bound=Callable)
    
    错误:

    .. code-block:: python

        T = TypeVar("T")
        P = ParamSpec("P")
        _T = TypeVar("_T", int, float, str)
        _F = TypeVar("_F", bound=Callable)

**字符串类型**
    
    不要在新代码中使用 ``typing.Text``. 这种写法只能用于处理 Python 2/3 的兼容问题.

    用 ``str`` 表示字符串/文本数据. 用 ``bytes`` 处理二进制数据.

    .. code-block:: python
    
        # 处理文本数据
        def deals_with_text_data(x: str) -> str:
            ...
        # 处理二进制数据
        def deals_with_binary_data(x: bytes) -> bytes:
            ...

    若一个函数中的字串类型始终一致, 比如上述代码中返回值类型和参数类型相同, 应该使用 `AnyStr <https://google.github.io/styleguide/pyguide.html#typing-type-var>`_.

.. _typing_imports:

**导入类型**

    为了静态分析和类型检查而导入 ``typing`` 和 ``collections.abc`` 模块中的符号时, 一定要导入符号本身. 这样常用的类型注解更简洁, 也符合全世界的习惯. 特别地, 你可以在一行内从 ``typing`` 和 ``collections.abc`` 模块中导入多个特定的类, 例如:

    .. code-block:: python
        
        from collections.abc import Mapping, Sequence
        from typing import Any, Generic
    
    采用这种方法时, 导入的类会进入本地命名空间, 因此所有 ``typing`` 和 ``collections.abc`` 模块中的名称都应该和关键词 (keyword) 同等对待. 你不能在自己的代码中定义相同的名字, 无论你是否采用类型注解. 若类型名和某模块中已有的名称出现冲突, 可以用 ``import x as y`` 的导入形式:

    .. code-block:: python

        from typing import Any as AnyType

    只要可行, 就使用内置类型. 利用 Python 3.9 引入的 `PEP-585 <https://peps.python.org/pep-0585/>`_, 可以在类型注解中使用参数化的容器类型.

    .. code-block:: python

        def generate_foo_scores(foo: set[str]) -> list[float]:
            ...
    
    注意: `Apache Beam <https://github.com/apache/beam/issues/23366>`_ 的用户应该继续导入 ``typing`` 模块提供的参数化容器类型.

    .. code-block:: python

        from typing import Set, List

        # 只有在你使用了 Apache Beam 这样没有为 PEP 585 更新的代码, 或者你的
        # 代码需要在 Python 3.9 以下版本中运行时, 才能使用这种旧风格.
        def generate_foo_scores(foo: Set[str]) -> List[float]:
            ...

**有条件的导入**

    仅在一些特殊情况下, 比如在运行时必须避免导入类型检查所需的模块, 才能有条件地导入. 不推荐这种写法. 替代方案是重构代码, 使类型检查所需的模块可以在顶层导入.

    可以把仅用于类型注解的导入放在 ``if TYPE_CHECKING:`` 语句块内.

    #. 在类型注解中, 有条件地导入的类型必须用字符串表示, 这样才能和 Python 3.6 之前的代码兼容. 因为 Python 3.6 之前真的会对类型注解求值.
    #. 只有那些仅仅用于类型注解的实例才能有条件地导入, 别名也是如此. 否则会引发运行时错误, 因为运行时不会导入这些模块.
    #. 有条件的导入语句应紧随所有常规导入语句之后.
    #. 有条件的导入语句之间不能有空行.
    #. 和常规导入一样, 请对有条件的导入语句排序.

    .. code-block:: python

        import typing
        if typing.TYPE_CHECKING:
            import sketch
        def f(x: "sketch.Sketch"): ...

**循环依赖**

    若类型注解引发了循环依赖, 说明代码可能存在问题. 这样的代码适合重构. 虽然技术上我们可以支持循环依赖, 但是很多构建系统 (build system) 不支持.

    可以用 ``Any`` 替换引起循环依赖的模块. 起一个有意义的别名, 然后使用模块中的真实类型名 (Any 的任何属性依然是 Any). 定义别名的语句应该和最后一行导入语句之间间隔一行.

    .. code-block:: python
        
        from typing import Any

        some_mod = Any  # 因为 some_mod.py 导入了我们的模块.
        ...

        def my_method(self, var: "some_mod.SomeType") -> None:
            ...

**泛型 (generics)**
    
    在注解类型时, 尽量为泛型类型填入类型参数. 否则, `泛型参数默认为 Any <https://www.python.org/dev/peps/pep-0484/#the-any-type>`_ .

    正确:

    .. code-block:: python

        def get_names(employee_ids: Sequence[int]) -> Mapping[int, str]:
            ...
    
    错误:

    .. code-block:: python

        # 这表示 get_names(employee_ids: Sequence[Any]) -> Mapping[Any, Any]
        def get_names(employee_ids: Sequence) -> Mapping:
            ...

    如果泛型类型的参数的确应该是 ``Any``, 请显式地标注, 不过注意 ``TypeVar`` 很可能更合适.

    错误:

    .. code-block:: python

        def get_names(employee_ids: Sequence[Any]) -> Mapping[Any, str]:
            """返回员工ID到员工名的映射."""
    
    正确:

    .. code-block:: python

        _T = TypeVar('_T')
        def get_names(employee_ids: Sequence[_T]) -> Mapping[_T, str]:
            """返回员工ID到员工名的映射.""" 
