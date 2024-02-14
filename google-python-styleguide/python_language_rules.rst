Python语言规范
================================

Lint
--------------------

.. tip::
    用 `pylintrc <https://google.github.io/styleguide/pylintrc>`_ 运行 pylint, 以检查你的代码.

定义:
    pylint 是在 Python 代码中寻找 bug 和格式问题的工具. 它寻找的问题就像 C 和 C++ 这些更静态的(译者注: 原文是less dynamic)语言中编译器捕捉的问题. 出于Python的动态特性, 部分警告可能有误. 不过, 误报应该不常见.
    
优点:
    可以发现疏忽, 例如拼写错误, 使用未赋值的变量等.
    
缺点:
    pylint 不完美. 要利用其优势, 我们有时侯需要: a) 绕过它 b) 抑制它的警告 或者 c) 改进它.
    
结论: 
    一定要用pylint检查你的代码.

    抑制不恰当的警告, 以免其他问题被警告淹没。你可以用行注释来抑制警告. 例如:
    
    .. code-block:: python
    
        def do_PUT(self):  # WSGI 接口名, 所以 pylint: disable=invalid-name
            ...

    pylint的警告均以符号名(如 ``empty-docstring`` )来区分. 谷歌特有的警告以 ``g-`` 为前缀.
    
    如果警告的符号名不够见名知意，那么请添加注释。
    
    这种抑制方式的好处是, 我们可以轻易搜索并重新评判这些注释.
    
    你可以用命令 ``pylint --list-msgs`` 来列出 pylint 的所有警告. 你可以用命令 ``pylint --help-msg=invalid-name``  来查询某个警告的详情.
    
    相较于旧的格式 ``pylint: disable-msg`` , 本文推荐使用 ``pylint: disable`` .
    
    如果有“参数未使用”的警告，你可以在函数体开头删除无用的变量，以消除警告. 一定要用注释说明你为什么删除这些变量. 注明"未使用."即可. 例如:
    
    .. code-block:: python
    
        def viking_cafe_order(spam: str, beans: str, eggs: str | None = None) -> str:
            del beans, eggs  # 未被维京人使用.
            return spam + spam + spam

    (译者注：Viking 意为维京人.)

    其他避免这种警告的常用方法还有: 用`_`作为未使用参数的名称; 给这些参数名加上前缀 ``unused_``; 或者把它们赋值给变量 ``_``. 我们允许但是不再推荐这些方法. 这会导致调用者无法通过参数名来传参，也不能保证变量确实没被引用。

导入
--------------------

.. tip::
    使用 ``import`` 语句时, 只导入包和模块, 而不单独导入函数或者类。

定义:
    用于方便模块间共享代码的重用机制.
    
优点:
    命名空间的管理规范十分简单. 每个标识符的来源都用一致的方式来表示. ``x.Obj`` 表示 ``Obj`` 对象定义在模块 ``x`` 中.
    
缺点:
    模块名可能有命名冲突. 有些模块名的长度过长以至于不方便.
    
结论:
    #. 用 ``import x`` 来导入包和模块. 
    
    #. 用 ``from x import y`` , 其中x是包前缀, y是不带前缀的模块名.
    
    #. 在以下情况使用 ``from x import y as z``: 如果有两个模块都叫 ``y``; 如果 ``y`` 和当前模块的某个全局名称冲突; 如果 ``y`` 是长度过长的名称.
    
    #. 仅当缩写 ``z`` 是标准缩写时才能使用 ``import y as z``.(比如 ``np`` 代表 ``numpy``.)
    
    例如, 可以用如下方式导入模块 ``sound.effects.echo``:
    
    .. code-block:: python
    
        from sound.effects import echo
        ...
        echo.EchoFilter(input, output, delay=0.7, atten=4)
     
    导入时禁止使用相对包名. 即使模块在同一个包中, 也要使用完整包名. 这能避免无意间重复导入同一个包.

例外:

    这一规定的例外是：

    #. 以下用于静态分析和类型检查的模块:

        #. ``typing`` 模块
        #. ``collections.abc`` 模块
        #. ``typing_extensions`` 模块

    #. `six.moves <https://six.readthedocs.io/#module-six.moves>`_ 模块中的重定向.
    
包
--------------------

.. tip::
    使用每个模块的完整路径名来导入模块.

优点:
    避免模块名冲突, 或是因模块搜索路径与作者的想法不符而导入错误的包. 也更容易找到模块.
    
缺点:
    部署代码更难, 因为你必须完整复刻包的层次. 在现代的部署模式下不再是问题.
    
结论:
    所有新的代码都应该用完整包名来导入每个模块.
    
    应该像下面这样导入:  

    正确:
    
    .. code-block:: python
    
        # 在代码中引用完整名称 absl.flags (详细版).
        import absl.flags
        from doctor.who import jodie

        _FOO = absl.flags.DEFINE_string(...)

    .. code-block:: python

        # 在代码中仅引用模块名 flags (常见情况).
        from absl import flags
        from doctor.who import jodie

        _FOO = flags.DEFINE_string(...)

    错误: (假设当前文件和 `jodie.py` 都在目录 `doctor/who/` 下)

    .. code-block:: python
    
        # 没有清晰地表达作者想要导入的模块和最终导入的模块.
        # 实际导入的模块取决于由外部环境控制的 sys.path.
        # 那些名为 jodie 的模块中, 哪个才是作者想导入的?
        import jodie

    不能臆测 `sys.path` 包含主程序所在的目录, 即使这种环境的确存在. 因此, 代码必须认定 `import jodie` 表示的是名为 `jodie` 的第三方库或者顶层的包，而非当前目录的 `jodie.py`.


异常
--------------------

.. tip::
    允许使用异常, 但必须谨慎使用.
 
定义:
    异常是一种跳出正常的控制流, 以处理错误或其它异常情况的方法.
    
优点:
    处理正常情况的控制流不会和错误处理代码混在一起. 在特定情况下, 它也能让控制流跳出多层调用帧. 例如, 一步跳出N多层嵌套的函数, 而不必逐层传递错误代码.
    
缺点:
    可能导致控制流晦涩难懂. 调用库函数时容易忘记处理异常.
    
结论:
    使用异常时必须遵守特定要求:
    
    #. 优先使用合适的内置异常类. 比如, 用 ``ValueError`` 表示前置条件错误 (例如给必须为正数的参数传入了负值). 不要使用 ``assert`` 语句来验证公开API的参数值. 应该用 ``assert`` 来保证内部正确性, 不应该用 ``assert`` 来纠正参数或表示意外情况. 若要用异常来表示意外情况, 应该用 ``raise``. 例如:
        
        正确:
        
        .. code-block:: python

            def connect_to_next_port(self, minimum: int) -> int:
                """连接到下一个可用的端口.

                参数:
                    minimum: 一个大于等于 1024 的端口号.

                返回:
                    新的最小端口.

                抛出:
                    ConnectionError: 没有可用的端口.
                """
                if minimum < 1024:
                    # 注意这里抛出 ValueError 的情况没有在文档里说明，因为 API 的
                    # 错误用法应该是未定义行为.
                    raise ValueError(f'最小端口号至少为 1024，不能是 {minimum}.')
                port = self._find_next_open_port(minimum)
                if port is None:
                    raise ConnectionError(
                        f'未能通过 {minimum} 或更高的端口号连接到服务.')
                assert port >= minimum, (
                    f'意外的端口号 {port}, 端口号不应小于 {minimum}.')
                return port

        错误:

        .. code-block:: python

            def connect_to_next_port(self, minimum: int) -> int:
                """连接到下一个可用的端口.

                参数:
                    minimum: 一个大于等于 1024 的端口号.

                返回:
                    新的最小端口.
                """
                assert minimum >= 1024, '最小端口号至少为 1024.'
                port = self._find_next_open_port(minimum)
                assert port is not None
                return port

    #. 模块或包可以定义自己的异常类型, 这些类必须继承已有的异常类. 异常类型名应该以 ``Error`` 为后缀, 并且不应该有重复 (例如 ``foo.FooError``).
    #. 永远不要使用 ``except:`` 语句来捕获所有异常, 也不要捕获 ``Exception`` 或者 ``StandardError`` , 除非你想:

        #. 重新抛出异常.
        #. 在程序中创造一个隔离点, 记录并抑制异常, 让异常不再继续传播. 这种写法可以用在线程的最外层, 以避免程序崩溃.

        如果你使用这种写法, Python 将非常宽容. ``except:`` 真的会捕获任何错误, 包括拼写错误的符号名、 ``sys.exit()`` 调用、 ``Ctrl+C`` 中断、单元测试错误和各种你不想捕获的错误.
    
    #. 最小化 ``try/except`` 代码块中的代码量. ``try`` 的范围越大, 就越容易把你没想到的那些能抛出异常的代码囊括在内. 这样的话, ``try/except`` 代码块就掩盖了真正的错误.
    #. 用 ``finally`` 表示无论异常与否都应执行的代码. 这种写法常用于清理资源, 例如关闭文件.

全局变量
--------------------

.. tip::
    避免全局变量.

定义:
    在程序运行时可以发生变化的模块级变量和类属性 (class attribute).
    
优点:
    偶尔有用. 
    
缺点:
    #. 破坏封装: 这种设计会阻碍一些有用的目标. 例如, 如果用全局变量来管理数据库连接, 那就难以同时连接两个数据库 (比如为了在数据迁移时比较差异). 全局注册表也有类似的问题.
    #. 导入模块时可能改变模块的行为, 因为首次导入模块时会对全局变量赋值.
    
结论:
    避免使用全局变量.

    在特殊情况下需要用到全局变量时, 应将全局变量声明为模块级变量或者类属性, 并在名称前加 `_` 以示为内部状态. 如需从外部访问全局变量, 必须通过公有函数或类方法实现. 详见 `命名规则 <https://google.github.io/styleguide/pyguide.html#s3.16-naming>`_ 章节. 请用注释或文档链接解释这些全局变量的设计思想.
    
    我们允许并鼓励使用模块级常量,例如 ``_MAX_HOLY_HANDGRENADE_COUNT = 3`` 表示内部常量, ``SIR_LANCELOTS_FAVORITE_COLOR = "blue"`` 表示公开API的常量. 注意常量名必须全部大写, 用下划线分隔单词. 详见 `命名规则 <https://google.github.io/styleguide/pyguide.html#s3.16-naming>`_ 章节.
    
嵌套/局部/内部类和函数
------------------------

.. tip::
    可以用局部类和局部函数来捕获局部变量. 可以用内部类.

定义:
    可以在方法、函数和类中定义内部类. 可以在方法和函数中定义嵌套函数. 嵌套函数可以只读访问外层作用域中的变量. (译者注:即内嵌函数可以读外部函数中定义的变量,但是无法改写,除非使用 `nonlocal`)

优点:
    方便定义作用域有限的工具类和函数. 便于实现 `抽象数据类型 <https://en.wikipedia.org/wiki/Abstract_data_type>`_. 常用于实现装饰器. 

缺点:
    无法直接测试嵌套的函数和类. 嵌套函数和嵌套类会让外层函数的代码膨胀, 可读性变差.
    
结论:
    可以谨慎使用. 尽量避免使用嵌套函数和嵌套类, 除非需要捕获 ``self`` 和 ``cls`` 以外的局部变量. 不要仅仅为了隐藏一个函数而使用嵌套函数. 应将需要隐藏的函数定义在模块级别, 并给名称加上 ``_`` 前缀, 以便在测试代码中调用此函数.
    
推导式 (comprehension expression) 和生成式 (generator expression)
--------------------------------

.. tip::
    适用于简单情况.

定义:
    列表、字典和集合的推导式和生成式可以用于简洁高效地创建容器和迭代器, 而无需借助循环、 ``map()``、 ``filter()``, 或者 ``lambda`` . (译者注: 元组是没有推导式的, ``()`` 内加类似推导式的句式返回的是个生成器)
    
优点:
    相较于其它创建字典、列表和集合的方法, 简单的列表推导式更加清晰和简洁. 生成器表达式十分高效, 因为无需创建整个列表.
    
缺点:
    复杂的列表推导式和生成式难以理解. 
    
结论:
    可以用于简单情况. 以下每个部分不应超过一行: 映射表达式、for语句和过滤表达式. 禁止多重for语句和多层过滤. 情况复杂时, 应该用循环.
    
    正确:

    .. code-block:: python 

        result = [mapping_expr for value in iterable if filter_expr]

        result = [{'key': value} for value in iterable
                  if a_long_filter_expression(value)]

        result = [complicated_transform(x)
                  for x in iterable if predicate(x)]

        descriptive_name = [
            transform({'key': key, 'value': value}, color='black')
            for key, value in generate_iterable(some_input)
            if complicated_condition_is_met(key, value)
        ]

        result = []
        for x in range(10):
            for y in range(5):
                if x * y > 10:
                    result.append((x, y))

        return {x: complicated_transform(x)
                for x in long_generator_function(parameter)
                if x is not None}

        squares_generator = (x**2 for x in range(10))

        unique_names = {user.name for user in users if user is not None}

        eat(jelly_bean for jelly_bean in jelly_beans
            if jelly_bean.color == 'black')    
              
    错误:

    .. code-block:: python 

        result = [complicated_transform(
                      x, some_argument=x+1)
                  for x in iterable if predicate(x)]

        result = [(x, y) for x in range(10) for y in range(5) if x * y > 10]

        return ((x, y, z)
                for x in xrange(5)
                for y in xrange(5)
                if x != y
                for z in xrange(5)
                if y != z)
              
默认迭代器和操作符
--------------------

.. tip::
    只要可行, 就用列表、字典和文件等类型的默认迭代器和操作符.
  
定义:
    字典和列表等容器类型具有默认的迭代器和关系运算符 ( ``in`` 和 ``not in`` ).
    
优点:
    默认迭代器和操作符简单高效. 这种写法可以直白地表达运算, 无需调用额外的函数. 使用默认操作符的函数是泛型函数, 可以用于任何支持该操作符的类型.
    
缺点:
    你不能通过方法名来辨别对象的类型 (除非变量有类型注解). 不过这也是优点.
    
结论:
    只要是支持的类型 (例如列表、字典和文件), 就使用默认迭代器和操作符. 内置类型也定义了一些返回迭代器的方法. 优先使用返回迭代器的方法, 而非返回列表的方法, 不过注意使用迭代器时不能修改容器.

    正确:

    .. code-block:: python
    
        for key in adict: ...
        if obj in alist: ...
        for line in afile: ...
        for k, v in adict.items(): ...

    错误:

    .. code-block:: python 
    
        for key in adict.keys(): ...
        for line in afile.readlines(): ...
    
生成器
--------------------

.. tip::
    按需使用生成器.

定义:
    生成器函数会返回一个迭代器. 每当函数执行 ``yield`` 语句时, 迭代器就生成一个值. 随后, 生成器的运行状态将暂停, 直到需要下一个值的时候.
    
优点:
    代码简单, 因为生成器可以保存局部变量和控制流. 相较于直接创建整个列表的函数, 生成器使用的内存更少.
    
缺点:
    必须等到生成结束或者生成器本身被内存回收的时候, 生成器的局部变量才能被内存回收.
    
结论:
    可以使用. 生成器的文档字符串中应使用"Yields:"而不是"Returns:".

    (译者注: 参看 :ref:`注释<comments>` )

    如果生成器占用了大量资源, 一定要强制清理资源.

    一种清理资源的好方法是用上下文管理器包裹生成器 `PEP-0533 <https://peps.python.org/pep-0533/>`_.
    
    
Lambda函数
--------------------

.. tip::
    适用于单行函数. 建议用生成式替代 ``map()/filter()`` 与 ``lambda`` 的组合.

定义:
    lambda 定义匿名函数, 不像语句那样定义具名函数.
    
优点:
    方便.
    
缺点:
    比局部函数更难理解和调试. 缺失函数名会导致调用栈晦涩难懂. 由于 lambda 函数只能包含一个表达式, 因此其表达能力有限.
    
结论:
    适用于单行函数. 如果函数体超过60-80个字符, 最好还是定义为常规的嵌套函数.
    
    对于乘法等常见操作, 应该用 ``operator`` 模块中的函数代替lambda函数. 例如, 推荐用 ``operator.mul`` 代替 ``lambda x, y: x * y`` .
    
条件表达式
--------------------

.. tip::
    适用于简单情况.

定义:
    条件表达式(又名三元运算符)是if语句的缩略版. 例如: ``x = 1 if cond else 2`` .
    
优点:
    比if语句更简短, 更方便.
    
缺点:
    有时比if语句更难理解. 如果表达式很长，就难以一眼望到条件.
    
结论:
    适用于简单情况. 以下每部分均不得长于一行: 真值分支, if 部分和 else 部分. 情况复杂时应使用完整的if语句.

    正确:

    .. code-block:: python 

        one_line = 'yes' if predicate(value) else 'no'
        slightly_split = ('yes' if predicate(value)
                          else 'no, nein, nyet')
        the_longest_ternary_style_that_can_be_done = (
            'yes, true, affirmative, confirmed, correct'
            if predicate(value)
            else 'no, false, negative, nay')

    错误:

    .. code-block:: python 

        bad_line_breaking = ('yes' if predicate(value) else
                             'no')  # 换行位置错误
        portion_too_long = ('yes'
                            if some_long_module.some_long_predicate_function(
                                really_long_variable_name)
                            else 'no, false, negative, nay')   # 过长
    
默认参数值
--------------------

.. tip::
    大部分情况下允许.
    
定义:
    你可以为参数列表的最后几个参数赋予默认值, 例如, ``def foo(a, b = 0):`` . 如果调用foo时只带一个参数, 则b为0. 如果调用时带两个参数, 则b的值等于第二个参数.
    
优点:
    很多时候, 你需要一个拥有大量默认值的函数, 并且偶尔需要覆盖这些默认值. 通过默认参数值可以轻松实现这种功能, 不需要为了覆盖默认值而编写大量额外的函数. 同时, Python不支持重载方法和函数, 而默认参数的写法可以轻松"仿造"重载行为.
    
缺点:
    默认参数在模块被导入时求值且只计算一次. 如果值是列表和字典等可变类型, 就可能引发问题. 如果函数修改了这个值(例如往列表内添加元素), 默认值就变化了.
    
结论:
    可以使用, 不过有如下注意事项:
    
    函数和方法的默认值不能是可变 (mutable) 对象.

    正确:
    
    .. code-block:: python
    
        def foo(a, b=None):
            if b is None:
                b = []
        def foo(a, b: Optional[Sequence] = None):
            if b is None:
                b = []
        def foo(a, b: Sequence = ()):  # 允许空元组，因为元组是不可变的

    错误:

    .. code-block:: python

        from absl import flags
        _FOO = flags.DEFINE_string(...)

        def foo(a, b=[]):
            ...
        def foo(a, b=time.time()):  # 确定要用模块的导入时间吗???
            ...
        def foo(a, b=_FOO.value):  # 此时还没有解析 sys.argv...
            ...
        def foo(a, b: Mapping = {}):  # 可能会赋值给未经过静态检查 (unchecked) 的代码
            ...
        

特性 (properties) 
--------------------

(译者注:参照fluent python.这里将 "property" 译为"特性",而 "attribute" 译为属性. python中数据的属性和处理数据的方法统称属性"(arrtibute)", 而在不改变类接口的前提下用来修改数据属性的存取方法我们称为"特性(property)".)

.. tip::
    可以用特性来读取或设置涉及简单计算、逻辑的属性. 特性的实现必须和属性 (attribute) 一样满足这些通用要求: 轻量、直白、明确.
    
定义:
    把读取、设置属性的函数包装为常规属性操作的写法.
    
优点:
    #. 可以直接实现属性的访问、赋值接口, 而不必添加获取器 (getter) 和设置器 (setter).
    #. 可以让属性变为只读.
    #. 可以实现惰性求值.
    #. 类的内部实现发生变化时, 可以用这种方法让用户看到的公开接口保持不变.
    
缺点:
    #. 可能掩盖副作用, 类似运算符重载 (operator overload).
    #. 子类继承时可能产生困惑.

结论:
    允许使用特性. 但是, 和运算符重载一样, 只能在必要时使用, 并且要模仿常规属性的存取特点. 若无法满足要求, 请参考 :ref:`获取器和写入器 <getter_setter>` 的规则.
    
    举个例子, 一个特性不能仅仅用于获取和设置一个内部属性: 因为不涉及计算, 没有必要用特性 (应该把该属性设为公有). 而用特性来限制属性的访问或者计算 **简单** 的衍生值则是正确的: 这种逻辑简单明了.
    
    应该用 ``@property`` `装饰器 (decorator) <http://google-styleguide.googlecode.com/svn/trunk/pyguide.html#Function_and_Method_Decorators>`_ 来创建特性. 自行实现的特性装饰器属于威力过大的功能.

    特性的继承机制难以理解. 不要用特性实现子类能覆写 (override) 或扩展的计算功能.
    
True/False的求值
--------------------

.. tip::
    尽可能使用"隐式"假值.
    
定义:
    Python在计算布尔值时会把一些值视为 ``False``. 简单来说, 所有的"空"值都是假值. 因此, ``0, None, [], {}, ""`` 作为布尔值使用时相当于 ``False``.
    
优点:
    Python布尔值可以让条件语句更易懂, 减少失误. 多数时候运行速度也更快.
    
缺点:
    对C/C++开发人员来说, 可能看起来有点怪. 
    
结论:
    尽可能使用"隐式"假值, 例如: 使用 ``if foo:`` 而非 ``if foo != []:`` . 不过还是有一些注意事项需要你铭记在心:
    
    #. 一定要用 ``if foo is None:`` (或者 ``is not None``) 来检测 ``None`` 值. 例如, 如果你要检查某个默认值为 ``None`` 的参数有没有被调用者覆盖, 覆盖的值在布尔语义下可能也是假值!
    #. 永远不要用 ``==`` 比较一个布尔值是否等于 ``False``. 应该用 ``if not x:`` 代替. 如果你需要区分 ``False`` 和 ``None``, 你应该用复合表达式, 例如 ``if not x and x is not None:``.
    #. 多利用空序列(字符串, 列表, 元组)是假值的特点. 因此 ``if not seq:``  比 ``if len(seq):`` 更好, ``if not seq:`` 比 ``if not len(seq):`` 更好.
    #. 处理整数时, 使用隐式 False 可能会得不偿失(例如不小心将 ``None`` 当做0来处理). 你可以显式比较整型值与0的关系 (``len()`` 的返回值例外).
    
        正确:

        .. code-block:: python
        
            if not users:
                print('无用户')

            if i % 10 == 0:
                self.handle_multiple_of_ten()

            def f(x=None):
                if x is None:
                    x = []

        错误:

        .. code-block:: python
        
            if len(users) == 0:
                print '无用户'

            if not i % 10:
                self.handle_multiple_of_ten()  

            def f(x=None):
                x = x or []
                     
    #. 注意, '0'(字符串, 不是整数)作为布尔值时等于 ``True``.
    #. 注意, 把 Numpy 数组转换为布尔值时可能抛出异常. 因此建议用 `.size` 属性检查 ``np.array`` 是否为空 (例如 ``if not users.size``).
    
词法作用域(Lexical Scoping, 又名静态作用域)
---------------------------------------------

.. tip::
    可以使用.

定义:
    嵌套的Python函数可以引用外层函数中定义的变量, 但是不能对这些变量赋值. 变量的绑定分析基于词法作用域, 也就是基于静态的程序文本. 任何在代码块内给标识符赋值的操作, 都会让Python将该标识符的所有引用变成局部变量, 即使读取语句写在赋值语句之前. 如果有全局声明, 该标识符会被视为全局变量. 
    
    一个使用这个特性的例子:
    
    .. code-block:: python

        def get_adder(summand1: float) -> Callable[[float], float]:
            """返回一个函数，该函数会给一个数字加上指定的值."""
            def adder(summand2: float) -> float:
                return summand1 + summand2

            return adder  
    
    (译者注: 这个函数的用法大概是: ``fn = get_adder(1.2); sum = fn(3.4)``, 结果是 ``sum == 4.6``.)
    
优点:
    通常会产生更清晰、更优雅的代码. 尤其是让熟练使用Lisp和Scheme(还有Haskell, ML等)的程序员感到舒适.
    
缺点:
    可能引发让人困惑的bug, 例如下面这个依据 `PEP-0227 <http://www.python.org/dev/peps/pep-0227/>`_ 改编的例子:
    
    .. code-block:: python
    
        i = 4
        def foo(x: Iterable[int]):
            def bar():
                print(i, end='')
            # ...
            # 很多其他代码
            # ...
            for i in x:  # 啊哈, i 是 Foo 的局部变量, 所以 bar 得到的是这个变量
                print(i, end='')
            bar()    
    
    因此 ``foo([1, 2, 3])`` 会输出 ``1 2 3 3`` , 而非 ``1 2 3 4`` .
    
    (译者注: x是一个列表, for循环其实是将x中的值依次赋给i.这样对i的赋值就隐式的发生了, 整个foo函数体中的i都会被当做局部变量, 包括bar()中的那个. 这一点与C++之类的语言还是有很大差别的.)
    
结论:
    可以使用.
        
函数与方法装饰器
--------------------

.. tip::
    仅在有显著优势时, 审慎地使用装饰器. 避免使用 ``staticmethod``. 减少使用 ``classmethod``.
    
定义:
    `装饰器(也就是@标记)作用在函数和方法上 <https://docs.python.org/release/2.4.3/whatsnew/node6.html>`_. 常见的装饰器是 ``@property``, 用于把方法转化为动态求值的属性. 不过, 也可以用装饰器语法自行定义装饰器. 具体地说, 若有一个函数 ``my_decorator`` , 下面两段代码是等效的:
    
    .. code-block:: python
    
         class C(object):
            @my_decorator
            def method(self):
                # 函数体 ...
    
    .. code-block:: python
    
        class C(object):
            def method(self):
                # 函数体 ...
            method = my_decorator(method)

            
优点:
    优雅地实现函数的变换; 这种变换可用于减少重复的代码, 或帮助检查不变式 (invariant).
    
缺点:
    装饰器可以在函数的参数和返回值上执行任何操作, 这可能产生意外且隐蔽的效果. 而且, 装饰是在定义对象时执行. 模块级对象(类、模块级函数)的装饰器在导入模块时执行. 当装饰器代码出错时, 很难恢复正常控制流.
    
结论:
    仅在有显著优势时, 审慎地使用装饰器. 装饰器的导入和命名规则与函数相同. 装饰器的pydoc注释应清楚地说明该函数是装饰器. 请为装饰器编写单元测试. 
    
    避免装饰器自身对外界的依赖(即不要依赖于文件, 套接字, 数据库连接等), 因为执行装饰器时(即导入模块时. ``pydoc`` 和其他工具也会导入你的模块) 可能无法连接到这些环境. 只要装饰器的调用参数正确, 装饰器应该 (尽最大努力) 保证运行成功.
    
    装饰器是一种特殊形式的"顶级代码". 参见关于《Python风格规范》中“主程序”的章节.

    不得使用 ``staticmethod``, 除非为了兼容老代码库的 API 不得已而为之. 应该把静态方法改写为模块级函数.

    仅在以下情况可以使用 ``classmethod``: 实现具名构造函数(named constructor); 在类方法中修改必要的全局状态 (例如进程内共享的缓存等)。
    
线程
--------------------

.. tip::
    不要依赖内置类型的原子性.
    
虽然Python的内置类型表面上有原子性, 但是在特定情形下可能打破原子性(例如用Python实现 ``__hash__`` 或 ``__eq__`` 的情况下). 因此它们的原子性不可靠. 你也不能臆测赋值是原子性的(因为赋值的原子性依赖于字典的原子性).

选择线程间的数据传递方式时, 应优先考虑 ``queue`` 模块的 ``Queue`` 数据类型. 如果不适用, 则使用 ``threading`` 模块及其提供的锁原语(locking primitives). 如果可行, 应该用条件变量和 ``threading.Condition`` 替代低级的锁.
    
威力过大的功能
--------------------

.. tip::
    避开这些功能.
    
定义:
    Python是一种异常灵活的语言, 有大量花哨的功能, 诸如自定义元类(metaclasses), 读取字节码(bytecode), 及时编译(on-the-fly compilation), 动态继承, 对象基类重设(object reparenting), 导入(import)技巧, 反射(例如 ``getattr()``), 系统内部状态的修改, ``__del__`` 实现的自定义清理等等.
    
优点:
    强大的语言功能让代码紧凑.
    
缺点:
    这些很"酷"的功能十分诱人, 但多数情况下没必要使用. 包含奇技淫巧的代码难以阅读、理解和调试. 一开始可能还好(对原作者而言), 但以后回顾代码时, 这种代码通常比那些长而直白的代码更加深奥.
    
结论:
    避开这些功能.
    
    可以使用那些在内部利用了这些功能的标准模块和类, 比如 ``abc.ABCMeta``, ``dataclasses`` 和 ``enum``.


现代python: from __future__ imports
--------------------------------------

.. tip::
    可以通过导入 ``__future__`` 包, 在较老的运行时上启用新语法, 并且只在特定文件上生效.

定义:
    通过使用 ``from __future__ import`` 并启用现代的语法, 可以提前使用未来的 Python 特性.

优点:
    实践表明, 该功能可以让版本升级过程更稳定, 因为可以逐步修改各个文件, 并用这样的兼容性声明来防止退化 (regression). 现代的代码便于维护, 因为不容易积累那些阻碍运行时升级的技术债.

缺点:
    此类代码无法在过老的运行时上运行, 过老的版本可能没有实现所需的 ``future`` 功能. 这个问题在那些需要支持大量不同环境的项目中尤为明显.

结论:
    **from __future__ imports**

    鼓励使用 ``from __future__ import`` 语句. 这样, 你的源代码从今天起就能使用更现代的 Python 语法. 当你不再需要支持老版本时, 请自行删除这些导入语句.

    如果你的代码要支持 3.5 版本, 而不是常规的 ``>=3.7``, 请导入:

    .. code-block:: python
        
        from __future__ import generator_stop

    详情参见 `Python future 语句 <https://docs.python.org/3/library/__future__.html>`_ 的文档.
    
    除非你确定代码的运行环境已经足够现代, 否则不要删除 future 语句. 即使你用不到 future 语句, 也要保留它们, 以免其他编辑者不小心对旧的特性产生依赖.

    在你认为恰当的时候, 可以使用其他来自 ``from __future__`` 的语句.


代码类型注释
--------------------

.. tip::
    你可以根据 `PEP-484 <https://www.python.org/dev/peps/pep-0484/>`_ 来对 python3 代码进行注释,并使用诸如 `pytype <https://github.com/google/pytype>`_ 之类的类型检查工具来检查代码.

    类型注释既可以写在源码里,也可以写在 `pyi <https://www.python.org/dev/peps/pep-0484/#stub-files>`_ 中. 推荐尽量写在源码里. 对于第三方代码和扩展包, 请使用 pyi 文件.

定义:
    用在函数参数和返回值上:

    .. code-block:: python

        def func(a: int) -> List[int]:

    也可以使用 `PEP-526 <https://www.python.org/dev/peps/pep-0526/>`_ 中的语法来声明变量类型:
    
    .. code-block:: python

        a: SomeType = some_func()

优点:
    可以提高代码可读性和可维护性. 类型检查器可以把运行时错误变成编译错误, 并阻止你使用威力过大的功能.

缺点:
    必须时常更新类型声明. 正确的代码也可能有误报. 无法使用威力大的功能.

结论:
     强烈推荐你在更新代码时启用 python 类型分析. 在添加或修改公开API时, 请添加类型注释, 并在构建系统(build system)中启用 pytype. 由于python静态分析是新功能, 因此一些意外的副作用(例如类型推导错误)可能会阻碍你的项目采纳这一功能. 在这种情况下, 建议作者在 BUILD 文件或者代码中添加一个 TODO 注释或者链接, 描述那些阻碍采用类型注释的问题.
     
     (译者注: 代码类型注释在帮助IDE或是vim等进行补全倒是很有效)
