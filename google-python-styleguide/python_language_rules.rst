Python语言规范
================================

Lint
--------------------

.. tip::
    使用该 `pylintrc <https://google.github.io/styleguide/pylintrc>`_ 对你的代码运行pylint
    
定义:
    pylint是一个在Python源代码中查找bug的工具. 对于C和C++这样的不那么动态的(译者注: 原文是less dynamic)语言, 这些bug通常由编译器来捕获. 由于Python的动态特性, 有些警告可能不对. 不过伪告警应该很少.
    
优点:
    可以捕获容易忽视的错误, 例如输入错误, 使用未赋值的变量等.
    
缺点:
    pylint不完美. 要利用其优势, 我们有时侯需要: a) 围绕着它来写代码 b) 抑制其告警 c) 改进它, 或者d) 忽略它.
    
结论: 
    确保对你的代码运行pylint.
    抑制不准确的警告,以便能够将其他警告暴露出来。你可以通过设置一个行注释来抑制警告. 例如:
    
    .. code-block:: python
    
        dict = 'something awful'  # Bad Idea... pylint: disable=redefined-builtin
        
    pylint警告是以符号名(如 ``empty-docstring`` )来标识的.google特定的警告则是以``g-``开头.
    
    如果警告的符号名不够见名知意，那么请对其增加一个详细解释。
    
    采用这种抑制方式的好处是我们可以轻松查找抑制并回顾它们.
    
    你可以使用命令 ``pylint --list-msgs`` 来获取pylint告警列表. 你可以使用命令 ``pylint --help-msg=C6409`` , 以获取关于特定消息的更多信息.
    
    相比较于之前使用的 ``pylint: disable-msg`` , 本文推荐使用 ``pylint: disable`` .
    
    在函数体中 ``del`` 未使用的变量可以消除参数未使用告警.记得要加一条注释说明你为何 ``del`` 它们,注释使用"Unused"就可以,例如:
    
    .. code-block:: python
    
        def viking_cafe_order(spam, beans, eggs=None):
            del beans, eggs  # Unused by vikings.
            return spam + spam + spam        

    其他消除这个告警的方法还有使用`_`标志未使用参数,或者给这些参数名加上前缀 ``unused_``, 或者直接把它们绑定到 ``_``.但这些方法都不推荐.

导入
--------------------

.. tip::
    仅对包和模块使用导入,而不单独导入函数或者类。`typing`模块例外。   

定义:
    模块间共享代码的重用机制.
    
优点:
    命名空间管理约定十分简单. 每个标识符的源都用一种一致的方式指示. x.Obj表示Obj对象定义在模块x中.
    
缺点:
    模块名仍可能冲突. 有些模块名太长, 不太方便.
    
结论:
    #. 使用 ``import x`` 来导入包和模块. 
    
    #. 使用 ``from x import y`` , 其中x是包前缀, y是不带前缀的模块名.
    
    #. 使用 ``from x import y as z``, 如果两个要导入的模块都叫做y或者y太长了.
    
    #. 仅当缩写 ``z`` 是通用缩写时才可使用 ``import y as z``.(比如 ``np`` 代表 ``numpy``.)
    
    例如, 模块 ``sound.effects.echo`` 可以用如下方式导入:
    
    .. code-block:: python
    
        from sound.effects import echo
        ...
        echo.EchoFilter(input, output, delay=0.7, atten=4)
     
    导入时不要使用相对名称. 即使模块在同一个包中, 也要使用完整包名. 这能帮助你避免无意间导入一个包两次. 

    导入 ``typing`` 和 `six.moves <https://six.readthedocs.io/#module-six.moves>`_ 模块时可以例外.
    
包
--------------------

.. tip::
    使用模块的全路径名来导入每个模块    

优点:
    避免模块名冲突或是因非预期的模块搜索路径导致导入错误. 查找包更容易. 
    
缺点:
    部署代码变难, 因为你必须复制包层次. 
    
结论:
    所有的新代码都应该用完整包名来导入每个模块.
    
    应该像下面这样导入:  

    yes:
    
    .. code-block:: python
    
        # 在代码中引用完整名称 absl.flags (详细情况).
        import absl.flags
        from doctor.who import jodie

        FLAGS = absl.flags.FLAGS

    .. code-block:: python

        # 在代码中仅引用模块名 flags (常见情况).
        from absl import flags
        from doctor.who import jodie

        FLAGS = flags.FLAGS

    No: (假设当前文件和 `jodie.py` 都在目录 `doctor/who/` 下)

    .. code-block:: python
    
        # 没能清晰指示出作者想要导入的模块和最终被导入的模块.
        # 实际导入的模块将取决于 sys.path.
        import jodie

    不应假定主入口脚本所在的目录就在 `sys.path` 中，虽然这种情况是存在的。当主入口脚本所在目录不在 `sys.path` 中时，代码将假设 `import jodie` 是导入的一个第三方库或者是一个名为 `jodie` 的顶层包，而不是本地的 `jodie.py`


异常
--------------------

.. tip::
    允许使用异常, 但必须小心
 
定义:
    异常是一种跳出代码块的正常控制流来处理错误或者其它异常条件的方式. 
    
优点:
    正常操作代码的控制流不会和错误处理代码混在一起. 当某种条件发生时, 它也允许控制流跳过多个框架. 例如, 一步跳出N个嵌套的函数, 而不必继续执行错误的代码. 
    
缺点:
    可能会导致让人困惑的控制流. 调用库时容易错过错误情况. 
    
结论:
    异常必须遵守特定条件:
    
    #. 优先合理的使用内置异常类.比如 ``ValueError`` 指示了一个程序错误, 比如在方法需要正数的情况下传递了一个负数错误.不要使用 ``assert`` 语句来验证公共API的参数值. ``assert`` 是用来保证内部正确性的,而不是用来强制纠正参数使用.若需要使用异常来指示某些意外情况,不要用 ``assert``,用 ``raise`` 语句,例如:
        
        Yes:
        
        .. code-block:: python

            def connect_to_next_port(self, minimum):
                """Connects to the next available port.

                Args:
                    minimum: A port value greater or equal to 1024.

                Returns:
                    The new minimum port.

                Raises:
                    ConnectionError: If no available port is found.
                """
                if minimum < 1024:
                    # Note that this raising of ValueError is not mentioned in the doc
                    # string's "Raises:" section because it is not appropriate to
                    # guarantee this specific behavioral reaction to API misuse.
                    raise ValueError(f'Min. port must be at least 1024, not {minimum}.')
                port = self._find_next_open_port(minimum)
                if not port:
                    raise ConnectionError(
                        f'Could not connect to service on port {minimum} or higher.')
                assert port >= minimum, (
                    f'Unexpected port {port} when minimum was {minimum}.')
                return port

        No:

        .. code-block:: python

            def connect_to_next_port(self, minimum):
                """Connects to the next available port.

                Args:
                minimum: A port value greater or equal to 1024.

                Returns:
                The new minimum port.
                """
                assert minimum >= 1024, 'Minimum port must be at least 1024.'
                port = self._find_next_open_port(minimum)
                assert port is not None
                return port

    #. 模块或包应该定义自己的特定域的异常基类, 这个基类应该从内建的Exception类继承. 模块的异常基类后缀应该叫做 ``Error``.
    #. 永远不要使用 ``except:`` 语句来捕获所有异常, 也不要捕获 ``Exception`` 或者 ``StandardError`` , 除非你打算重新触发该异常, 或者你已经在当前线程的最外层(记得还是要打印一条错误消息). 在异常这方面, Python非常宽容, ``except:`` 真的会捕获包括Python语法错误在内的任何错误. 使用 ``except:`` 很容易隐藏真正的bug. 
    #. 尽量减少try/except块中的代码量. try块的体积越大, 期望之外的异常就越容易被触发. 这种情况下, try/except块将隐藏真正的错误. 
    #. 使用finally子句来执行那些无论try块中有没有异常都应该被执行的代码. 这对于清理资源常常很有用, 例如关闭文件.

全局变量
--------------------

.. tip::
    避免全局变量

定义:
    定义在模块级的变量.
    
优点:
    偶尔有用. 
    
缺点:
    导入时可能改变模块行为, 因为导入模块时会对模块级变量赋值. 
    
结论:
    避免使用全局变量.
    鼓励使用模块级的常量,例如 ``MAX_HOLY_HANDGRENADE_COUNT = 3``.注意常量命名必须全部大写,用 ``_`` 分隔.具体参见 `命名规则 <https://google.github.io/styleguide/pyguide.html#s3.16-naming>`_
    若必须要使用全局变量,应在模块内声明全局变量,并在名称前 ``_`` 使之成为模块内部变量.外部访问必须通过模块级的公共函数.具体参见 `命名规则 <>`_
    
    
嵌套/局部/内部类或函数
------------------------

.. tip::
    使用内部类或者嵌套函数可以用来覆盖某些局部变量.

定义:
    类可以定义在方法, 函数或者类中. 函数可以定义在方法或函数中. 封闭区间中定义的变量对嵌套函数是只读的. (译者注:即内嵌函数可以读外部函数中定义的变量,但是无法改写,除非使用 `nonlocal`)

优点:
    允许定义仅用于有效范围的工具类和函数.在装饰器中比较常用. 

缺点:
    嵌套类或局部类的实例不能序列化(pickled). 内嵌的函数和类无法直接测试.同时内嵌函数和类会使外部函数的可读性变差.
    
结论:
    使用内部类或者内嵌函数可以忽视一些警告.但是应该避免使用内嵌函数或类,除非是想覆盖某些值.若想对模块的用户隐藏某个函数,不要采用嵌套它来隐藏,应该在需要被隐藏的方法的模块级名称加 ``_`` 前缀,这样它依然是可以被测试的.
    
推导式&生成式
--------------------------------

.. tip::
    可以在简单情况下使用    

定义:
    列表,字典和集合的推导&生成式提供了一种简洁高效的方式来创建容器和迭代器, 而不必借助map(), filter(), 或者lambda.(译者注: 元组是没有推导式的, ``()`` 内加类似推导式的句式返回的是个生成器)
    
优点:
    简单的列表推导可以比其它的列表创建方法更加清晰简单. 生成器表达式可以十分高效, 因为它们避免了创建整个列表. 
    
缺点:
    复杂的列表推导或者生成器表达式可能难以阅读. 
    
结论:
    适用于简单情况. 每个部分应该单独置于一行: 映射表达式, for语句, 过滤器表达式. 禁止多重for语句或过滤器表达式. 复杂情况下还是使用循环.
    
    Yes:

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
              
    No:

    .. code-block:: python 
    
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
    如果类型支持, 就使用默认迭代器和操作符. 比如列表, 字典及文件等.
  
定义:
    容器类型, 像字典和列表, 定义了默认的迭代器和关系测试操作符(in和not in)
    
优点:
    默认操作符和迭代器简单高效, 它们直接表达了操作, 没有额外的方法调用. 使用默认操作符的函数是通用的. 它可以用于支持该操作的任何类型. 
    
缺点:
    你没法通过阅读方法名来区分对象的类型(例如, has_key()意味着字典). 不过这也是优点. 
    
结论:
    如果类型支持, 就使用默认迭代器和操作符, 例如列表, 字典和文件. 内建类型也定义了迭代器方法. 优先考虑这些方法, 而不是那些返回列表的方法. 当然，这样遍历容器时，你将不能修改容器. 除非必要,否则不要使用诸如 `dict.iter*()` 这类python2的特定迭代方法.

    Yes:

    .. code-block:: python
    
        for key in adict: ...
        if key not in adict: ...
        if obj in alist: ...
        for line in afile: ...
        for k, v in dict.iteritems(): ...

    No: 

    .. code-block:: python 
    
        for key in adict.keys(): ...
        if not adict.has_key(key): ...
        for line in afile.readlines(): ...
    
生成器
--------------------

.. tip::
    按需使用生成器.

定义:
    所谓生成器函数, 就是每当它执行一次生成(yield)语句, 它就返回一个迭代器, 这个迭代器生成一个值. 生成值后, 生成器函数的运行状态将被挂起, 直到下一次生成. 
    
优点:
    简化代码, 因为每次调用时, 局部变量和控制流的状态都会被保存. 比起一次创建一系列值的函数, 生成器使用的内存更少. 
    
缺点:
    没有.
    
结论:
    鼓励使用. 注意在生成器函数的文档字符串中使用"Yields:"而不是"Returns:".

    (译者注: 参看 :ref:`注释<comments>` )
    
    
Lambda函数
--------------------

.. tip::
    适用于单行函数

定义:
    与语句相反, lambda在一个表达式中定义匿名函数. 常用于为 ``map()`` 和 ``filter()`` 之类的高阶函数定义回调函数或者操作符.
    
优点:
    方便.
    
缺点:
    比本地函数更难阅读和调试. 没有函数名意味着堆栈跟踪更难理解. 由于lambda函数通常只包含一个表达式, 因此其表达能力有限. 
    
结论:
    适用于单行函数. 如果代码超过60-80个字符, 最好还是定义成常规(嵌套)函数.
    
    对于常见的操作符，例如乘法操作符，使用 ``operator`` 模块中的函数以代替lambda函数. 例如, 推荐使用 ``operator.mul`` , 而不是 ``lambda x, y: x * y`` . 
    
条件表达式
--------------------

.. tip::
    适用于单行函数

定义:
    条件表达式(又名三元运算符)是对于if语句的一种更为简短的句法规则. 例如: ``x = 1 if cond else 2`` .
    
优点:
    比if语句更加简短和方便.
    
缺点:
    比if语句难于阅读. 如果表达式很长， 难于定位条件. 
    
结论:
    适用于单行函数. 写法上推荐真实表达式,if表达式,else表达式每个独占一行.在其他情况下，推荐使用完整的if语句.    

    .. code-block:: python 

        one_line = 'yes' if predicate(value) else 'no'
        slightly_split = ('yes' if predicate(value)
                        else 'no, nein, nyet')
        the_longest_ternary_style_that_can_be_done = (
            'yes, true, affirmative, confirmed, correct'
            if predicate(value)
            else 'no, false, negative, nay')

    .. code-block:: python 

        bad_line_breaking = ('yes' if predicate(value) else
                        'no')
        portion_too_long = ('yes'
                            if some_long_module.some_long_predicate_function(
                                really_long_variable_name)
                            else 'no, false, negative, nay')
    
默认参数值
--------------------

.. tip::
    适用于大部分情况.
    
定义:
    你可以在函数参数列表的最后指定变量的值, 例如, ``def foo(a, b = 0):`` . 如果调用foo时只带一个参数, 则b被设为0. 如果带两个参数, 则b的值等于第二个参数. 
    
优点:
    你经常会碰到一些使用大量默认值的函数, 但偶尔(比较少见)你想要覆盖这些默认值. 默认参数值提供了一种简单的方法来完成这件事, 你不需要为这些罕见的例外定义大量函数. 同时, Python也不支持重载方法和函数, 默认参数是一种"仿造"重载行为的简单方式. 
    
缺点:
    默认参数只在模块加载时求值一次. 如果参数是列表或字典之类的可变类型, 这可能会导致问题. 如果函数修改了对象(例如向列表追加项), 默认值就被修改了. 
    
结论:
    鼓励使用, 不过有如下注意事项:
    
    不要在函数或方法定义中使用可变对象作为默认值.
    
    .. code-block:: python
    
        Yes: def foo(a, b=None):
                if b is None:
                    b = []
        Yes: def foo(a, b: Optional[Sequence] = None):
                if b is None:
                    b = []
        Yes: def foo(a, b: Sequence = ()):  # Empty tuple OK since tuples are immutable 

    .. code-block:: python  

        No:  def foo(a, b=[]):
            ...
        No:  def foo(a, b=time.time()):  # The time the module was loaded???
            ...
        No:  def foo(a, b=FLAGS.my_thing):  # sys.argv has not yet been parsed...
            ...
        No:  def foo(a, b: Mapping = {}):  # Could still get passed to unchecked code             
            ...
        

特性(properties) 
--------------------

(译者注:参照fluent python.这里将 "property" 译为"特性",而 "attribute" 译为属性. python中数据的属性和处理数据的方法统称属性"(arrtibute)", 而在不改变类接口的前提下用来修改数据属性的存取方法我们称为"特性(property)".)

.. tip::
    访问和设置数据成员时, 你通常会使用简单, 轻量级的访问和设置函数.建议使用特性(properties)来代替它们.    
    
定义:
    一种用于包装方法调用的方式. 当运算量不大, 它是获取和设置属性(attribute)的标准方式. 
    
优点:
    通过消除简单的属性(attribute)访问时显式的get和set方法调用, 可读性提高了. 允许懒惰的计算. 用Pythonic的方式来维护类的接口. 就性能而言, 当直接访问变量是合理的, 添加访问方法就显得琐碎而无意义. 使用特性(properties)可以绕过这个问题. 将来也可以在不破坏接口的情况下将访问方法加上. 
    
缺点:
    特性(properties)是在get和set方法声明后指定, 这需要使用者在接下来的代码中注意: set和get是用于特性(properties)的(除了用 ``@property`` 装饰器创建的只读属性).  必须继承自object类. 可能隐藏比如操作符重载之类的副作用. 继承时可能会让人困惑. 
    (译者注:这里没有修改原始翻译,其实就是 @property 装饰器是不会被继承的)

结论:
    你通常习惯于使用访问或设置方法来访问或设置数据, 它们简单而轻量. 不过我们建议你在新的代码中使用属性. 只读属性应该用 ``@property`` `装饰器 <http://google-styleguide.googlecode.com/svn/trunk/pyguide.html#Function_and_Method_Decorators>`_ 来创建.

    如果子类没有覆盖属性, 那么属性的继承可能看上去不明显. 因此使用者必须确保访问方法间接被调用, 以保证子类中的重载方法被属性调用(使用模板方法设计模式).
    
    .. code-block:: python
    
        Yes: 
            import math

            class Square:
                """A square with two properties: a writable area and a read-only perimeter.

                To use:
                >>> sq = Square(3)
                >>> sq.area
                9
                >>> sq.perimeter
                12
                >>> sq.area = 16
                >>> sq.side
                4
                >>> sq.perimeter
                16
                """

                def __init__(self, side):
                    self.side = side

                @property
                def area(self):
                    """Area of the square."""
                    return self._get_area()

                @area.setter
                def area(self, area):
                    return self._set_area(area)

                def _get_area(self):
                    """Indirect accessor to calculate the 'area' property."""
                    return self.side ** 2

                def _set_area(self, area):
                    """Indirect setter to set the 'area' property."""
                    self.side = math.sqrt(area)

                @property
                def perimeter(self):
                    return self.side * 4 
        
    (译者注: 老实说, 我觉得这段示例代码很不恰当, 有必要这么蛋疼吗?)
    
True/False的求值
--------------------

.. tip::
    尽可能使用隐式false
    
定义:
    Python在布尔上下文中会将某些值求值为false. 按简单的直觉来讲, 就是所有的"空"值都被认为是false. 因此0， None, [], {}, "" 都被认为是false.
    
优点:
    使用Python布尔值的条件语句更易读也更不易犯错. 大部分情况下, 也更快. 
    
缺点:
    对C/C++开发人员来说, 可能看起来有点怪. 
    
结论:
    尽可能使用隐式的false, 例如: 使用 ``if foo:`` 而不是 ``if foo != []:`` . 不过还是有一些注意事项需要你铭记在心:
    
    #. 对于 ``None`` 等单例对象测试时,使用 ``is`` 或者 ``is not``.当你要测试一个默认值是None的变量或参数是否被设为其它值. 这个值在布尔语义下可能是false!
           (译者注: ``is`` 比较的是对象的id(), 这个函数返回的通常是对象的内存地址,考虑到CPython的对象重用机制,可能会出现生命周不重叠的两个对象会有相同的id)
    #. 永远不要用==将一个布尔量与false相比较. 使用 ``if not x:`` 代替. 如果你需要区分false和None, 你应该用像 ``if not x and x is not None:`` 这样的语句.
    #. 对于序列(字符串, 列表, 元组), 要注意空序列是false. 因此 ``if not seq:`` 或者 ``if seq:`` 比 ``if len(seq):`` 或 ``if not len(seq):`` 要更好.
    #. 处理整数时, 使用隐式false可能会得不偿失(即不小心将None当做0来处理). 你可以将一个已知是整型(且不是len()的返回结果)的值与0比较. 
    
        Yes: 

        .. code-block:: python
        
            if not users:
                print('no users')

            if foo == 0:
                self.handle_zero()

            if i % 10 == 0:
                self.handle_multiple_of_ten()

            def f(x=None):
                if x is None:
                    x = []

        No:

        .. code-block:: python
        
            if len(users) == 0:
                print 'no users'

            if foo is not None and not foo:
                self.handle_zero()

            if not i % 10:
                self.handle_multiple_of_ten()  

            def f(x=None):
                x = x or []
                     
    #. 注意'0'(字符串)会被当做true.

过时的语言特性
--------------------

.. tip::
    尽可能使用字符串方法取代字符串模块. 使用函数调用语法取代apply(). 使用列表推导, for循环取代filter(), map()以及reduce().    

定义:
    当前版本的Python提供了大家通常更喜欢的替代品. 

结论:
    我们不使用不支持这些特性的Python版本, 所以没理由不用新的方式. 
    
    .. code-block:: python
    
        Yes: words = foo.split(':')

             [x[1] for x in my_list if x[2] == 5]
             
             map(math.sqrt, data)    # Ok. No inlined lambda expression.

             fn(*args, **kwargs)   

    .. code-block:: python
    
        No:  words = string.split(foo, ':')

             map(lambda x: x[1], filter(lambda x: x[2] == 5, my_list))

             apply(fn, args, kwargs)             
    
词法作用域(Lexical Scoping)
-----------------------------

.. tip::
    推荐使用

定义:
    嵌套的Python函数可以引用外层函数中定义的变量, 但是不能够对它们赋值. 变量绑定的解析是使用词法作用域, 也就是基于静态的程序文本. 对一个块中的某个名称的任何赋值都会导致Python将对该名称的全部引用当做局部变量, 甚至是赋值前的处理. 如果碰到global声明, 该名称就会被视作全局变量. 
    
    一个使用这个特性的例子:
    
    .. code-block:: python

        def get_adder(summand1):
            """Returns a function that adds numbers to a given number."""
            def adder(summand2):
                return summand1 + summand2

            return adder  
    
    (译者注: 这个例子有点诡异, 你应该这样使用这个函数: ``sum = get_adder(summand1)(summand2)`` )
    
优点:
    通常可以带来更加清晰, 优雅的代码. 尤其会让有经验的Lisp和Scheme(还有Haskell, ML等)程序员感到欣慰. 
    
缺点:
    可能导致让人迷惑的bug. 例如下面这个依据 `PEP-0227 <http://www.python.org/dev/peps/pep-0227/>`_ 的例子:
    
    .. code-block:: python
    
        i = 4
        def foo(x):
            def bar():
                print i,
            # ...
            # A bunch of code here
            # ...
            for i in x:  # Ah, i *is* local to Foo, so this is what Bar sees
                print i,
            bar()    
    
    因此 ``foo([1, 2, 3])`` 会打印 ``1 2 3 3`` , 不是 ``1 2 3 4`` .
    
    (译者注: x是一个列表, for循环其实是将x中的值依次赋给i.这样对i的赋值就隐式的发生了, 整个foo函数体中的i都会被当做局部变量, 包括bar()中的那个. 这一点与C++之类的静态语言还是有很大差别的.)
    
结论:
    鼓励使用. 
        
函数与方法装饰器
--------------------

.. tip::
    如果好处很显然, 就明智而谨慎的使用装饰器,避免使用 ``staticmethod``以及谨慎使用``classmethod``.   
    
定义:
    `用于函数及方法的装饰器 <https://docs.python.org/release/2.4.3/whatsnew/node6.html>`_ (也就是@标记). 最常见的装饰器是@classmethod 和@staticmethod, 用于将常规函数转换成类方法或静态方法. 不过, 装饰器语法也允许用户自定义装饰器. 特别地, 对于某个函数 ``my_decorator`` , 下面的两段代码是等效的:
    
    .. code-block:: python
    
         class C(object):
            @my_decorator
            def method(self):
                # method body ...   
    
    .. code-block:: python
    
        class C(object):
            def method(self):
                # method body ...
            method = my_decorator(method)

            
优点:
    优雅的在函数上指定一些转换. 该转换可能减少一些重复代码, 保持已有函数不变(enforce invariants), 等.
    
缺点:
    装饰器可以在函数的参数或返回值上执行任何操作, 这可能导致让人惊异的隐藏行为. 而且, 装饰器在导入时执行. 从装饰器代码中捕获错误并处理是很困难的.
    
结论:
    如果好处很显然, 就明智而谨慎的使用装饰器. 装饰器应该遵守和函数一样的导入和命名规则. 装饰器的python文档应该清晰的说明该函数是一个装饰器. 请为装饰器编写单元测试. 
    
    避免装饰器自身对外界的依赖(即不要依赖于文件, socket, 数据库连接等), 因为装饰器运行时这些资源可能不可用(由 ``pydoc`` 或其它工具导入). 应该保证一个用有效参数调用的装饰器在所有情况下都是成功的.
    
    装饰器是一种特殊形式的"顶级代码". 参考后面关于 :ref:`Main <main>` 的话题. 

    除非是为了将方法和现有的API集成，否则不要使用 ``staticmethod`` .多数情况下，将方法封装成模块级的函数可以达到同样的效果.

    谨慎使用 ``classmethod`` .通常只在定义备选构造函数，或者写用于修改诸如进程级缓存等必要的全局状态的特定类方法才用。
    
线程
--------------------

.. tip::
    不要依赖内建类型的原子性.
    
虽然Python的内建类型例如字典看上去拥有原子操作, 但是在某些情形下它们仍然不是原子的(即: 如果__hash__或__eq__被实现为Python方法)且它们的原子性是靠不住的. 你也不能指望原子变量赋值(因为这个反过来依赖字典).

优先使用Queue模块的 ``Queue`` 数据类型作为线程间的数据通信方式. 另外, 使用threading模块及其锁原语(locking primitives). 了解条件变量的合适使用方式, 这样你就可以使用 ``threading.Condition`` 来取代低级别的锁了. 
    
威力过大的特性
--------------------

.. tip::
    避免使用这些特性    
    
定义:
    Python是一种异常灵活的语言, 它为你提供了很多花哨的特性, 诸如元类(metaclasses), 字节码访问, 任意编译(on-the-fly compilation), 动态继承, 对象父类重定义(object reparenting), 导入黑客(import hacks), 反射, 系统内修改(modification of system internals), 等等.
    
优点:
    强大的语言特性, 能让你的代码更紧凑.
    
缺点:
    使用这些很"酷"的特性十分诱人, 但不是绝对必要. 使用奇技淫巧的代码将更加难以阅读和调试. 开始可能还好(对原作者而言), 但当你回顾代码, 它们可能会比那些稍长一点但是很直接的代码更加难以理解. 
    
结论:
    在你的代码中避免这些特性.     
    
    当然，利用了这些特性的来编写的一些标准库是值得去使用的，比如 ``abc.ABCMeta``, ``collection.namedtuple``, ``dataclasses`` , ``enum``等.


现代python: python3 和from __future__ imports
--------------------

.. tip::
    尽量使用 python3,  即使使用非 python3 写的代码.也应该尽量兼容.

定义:
    python3 是 python 的一个重大变化,虽然已有大量代码是 python2.7 写的,但是通过一些简单的调整,就可以使之在 python3 下运行.

优点:
    只要确定好项目的所有依赖,那么用 python3 写代码可以更加清晰和方便运行.

缺点:
    导入一些看上去实际用不到的模块到代码里显得有些奇葩.

结论:
    **from __future__ imports**

    鼓励使用 ``from __future__ import`` 语句,所有的新代码都应该包含以下内容,并尽可能的与之兼容:

    .. code-block:: python
        
        from __future__ import absolute_import
        from __future__ import division
        from __future__ import print_function

    以上导入的详情参见 `absolute imports <https://www.python.org/dev/peps/pep-0328/>`_ , `division behavior <https://www.python.org/dev/peps/pep-0238/>`_, `print function <https://www.python.org/dev/peps/pep-3105/>`_ .
    除非代码是只在python3下运行,否则不要删除以上导入.最好在所有文件里都保留这样的导入,这样若有人用到了这些方法时,编辑时不会忘记导入.
    还有其他的一些来自 ``from __future__`` 的语句.请在你认为合适的地方使用它们.本文没有推荐 ``unicode_literals`` ,因为我们认为它不是很棒的改进,它在 python2.7 中大量引入例隐式的默认编码转换.大多数情况下还是推荐显式的使用 ``b`` 和 ``u`` 以及 unicode字符串来显式的指示编码转换.

    **six,future,past**

     当项目需要同时支持 python2 和 python3 时,请根据需要使用 `six <https://pypi.org/project/six/>`_ , `future <https://pypi.org/project/future/>`_ , `past <https://pypi.org/project/past/>`_ . 这些库可以使代码更加清晰和简单.


代码类型注释
--------------------

.. tip::
    你可以根据 `PEP-484 <https://www.python.org/dev/peps/pep-0484/>`_ 来对 python3 代码进行注释,并使用诸如 `pytype <https://github.com/google/pytype>`_ 之类的类型检查工具来检查代码.
    类型注释既可以写在源码,也可以写在 `pyi <https://www.python.org/dev/peps/pep-0484/#stub-files>`_ 中.推荐尽量写在源码里,对于第三方扩展包,可以写在pyi文件里.

定义:
    用于函数参数和返回值的类型注释: 

    .. code-block:: python

        def func(a: int) -> List[int]:

    也可以使用 `PEP-526 <https://www.python.org/dev/peps/pep-0526/>`_ 中的语法来声明变量类型:
    
    .. code-block:: python

        a: SomeType = some_func()

    在必须支持老版本 python 运行的代码中则可以这样注释:

    .. code-block:: python

        a = some_func() #type: SomeType

优点:
    可以提高代码可读性和可维护性.同时一些类型检查器可以帮您提早发现一些运行时错误,并降低您使用大威力特性的必要.

缺点:
    必须时常更新类型声明.过时的类型声明可能会误导您.使用类型检查器会抑制您使用大威力特性.

结论:
     强烈推荐您在更新代码时使用 python 类型分析.在添加或修改公共API时使用类型注释,在最终构建整个项目前使用 pytype 来进行检查.由于静态分析对于 python 来说还不够成熟,因此可能会出现一些副作用(例如错误推断的类型)可能会阻碍项目的部署.在这种情况下,建议作者添加一个 TODO 注释或者链接,来描述当前构建文件或是代码本身中使用类型注释导致的问题.
     
     (译者注: 代码类型注释在帮助IDE或是vim等进行补全倒是很有效)
