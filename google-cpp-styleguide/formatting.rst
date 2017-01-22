8. 格式
------------

代码风格和格式确实比较随意, 但一个项目中所有人遵循同一风格是非常容易的. 个体未必同意下述每一处格式规则, 但整个项目服从统一的编程风格是很重要的, 只有这样才能让所有人能很轻松的阅读和理解代码.

另外, 我们写了一个 `emacs 配置文件 <http://google-styleguide.googlecode.com/svn/trunk/google-c-style.el>`_ 来帮助你正确的格式化代码.

.. _line-length:

8.1. 行长度
~~~~~~~~~~~~~~~~~~~~

.. tip::

    每一行代码字符数不超过 80.

我们也认识到这条规则是有争议的, 但很多已有代码都已经遵照这一规则, 我们感觉一致性更重要.

优点:

    提倡该原则的人主张强迫他们调整编辑器窗口大小很野蛮. 很多人同时并排开几个代码窗口, 根本没有多余空间拉伸窗口. 大家都把窗口最大尺寸加以限定, 并且 80 列宽是传统标准. 为什么要改变呢?

缺点:

    反对该原则的人则认为更宽的代码行更易阅读. 80 列的限制是上个世纪 60 年代的大型机的古板缺陷; 现代设备具有更宽的显示屏, 很轻松的可以显示更多代码.

结论:

    80 个字符是最大值.

    特例:

    - 如果一行注释包含了超过 80 字符的命令或 URL, 出于复制粘贴的方便允许该行超过 80 字符.
    - 包含长路径的 ``#include`` 语句可以超出80列. 但应该尽量避免.
    - :ref:`头文件保护 <define-guard>` 可以无视该原则.

8.2. 非 ASCII 字符
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. tip::

    尽量不使用非 ASCII 字符, 使用时必须使用 UTF-8 编码.

即使是英文, 也不应将用户界面的文本硬编码到源代码中, 因此非 ASCII 字符要少用. 特殊情况下可以适当包含此类字符. 如, 代码分析外部数据文件时, 可以适当硬编码数据文件中作为分隔符的非 ASCII 字符串; 更常见的是 (不需要本地化的) 单元测试代码可能包含非 ASCII 字符串. 此类情况下, 应使用 UTF-8 编码, 因为很多工具都可以理解和处理 UTF-8 编码.

十六进制编码也可以, 能增强可读性的情况下尤其鼓励 —— 比如 ``"\xEF\xBB\xBF"`` 在 Unicode 中是 *零宽度 无间断* 的间隔符号, 如果不用十六进制直接放在 UTF-8 格式的源文件中, 是看不到的.

(Yang.Y 注: ``"\xEF\xBB\xBF"`` 通常用作 UTF-8 with BOM 编码标记)

用 ``u8`` 前缀以把带 ``uXXXX`` 转义序列的字符串字面值编码成 UTF-8. 不要用在本身就带 UTF-8 字符的字符串字面值上，因为如果编译器不把源代码识别成 UTF-8, 输出就会出错。

别用 C++11 的 ``char16_t`` 和 ``char32_t``, 它们和 UTF-8 文本没有关系，``wchar_t`` 同理，除非您写的代码要调用 Windows API, 后者有用到 ``wchar_t`` 扩展。

8.3. 空格还是制表位
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. tip::

    只使用空格, 每次缩进 2 个空格.

我们使用空格缩进. 不要在代码中使用制符表. 你应该设置编辑器将制符表转为空格.

8.4. 函数声明与定义
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. tip::

    返回类型和函数名在同一行, 参数也尽量放在同一行，如果放不下就对形参分行。

函数看上去像这样:

    .. code-block:: c++

        ReturnType ClassName::FunctionName(Type par_name1, Type par_name2) {
            DoSomething();
            ...
        }

如果同一行文本太多, 放不下所有参数:

    .. code-block:: c++

        ReturnType ClassName::ReallyLongFunctionName(Type par_name1, Type par_name2,
                                                     Type par_name3) {
            DoSomething();
            ...
        }

甚至连第一个参数都放不下:

    .. code-block:: c++

        ReturnType LongClassName::ReallyReallyReallyLongFunctionName(
                Type par_name1,  // 4 空格缩进
                Type par_name2,
                Type par_name3) {
            DoSomething();  // 2 空格缩进
            ...
        }

注意以下几点:

    - 如果返回类型和函数名在一行放不下，分行。

    - 如果返回类型那个与函数声明或定义分行了，不要缩进。

    - 左圆括号总是和函数名在同一行;

    - 函数名和左圆括号间没有空格;

    - 圆括号与参数间没有空格;

    - 左大括号总在最后一个参数同一行的末尾处;

    - 如果其它风格规则允许的话，右大括号总是单独位于函数最后一行，或者与左大括号同一行。

    - 右大括号和左大括号间总是有一个空格;

    - 函数声明和定义中的所有形参必须有命名且一致;

    - 所有形参应尽可能对齐;

    - 缺省缩进为 2 个空格;

    - 换行后的参数保持 4 个空格的缩进;

如果有些参数没有用到, 在函数定义处将参数名注释起来:

    .. code-block:: c++

        // 接口中形参恒有命名。
        class Shape {
         public:
          virtual void Rotate(double radians) = 0;
        }

        // 声明中形参恒有命名。
        class Circle : public Shape {
         public:
          virtual void Rotate(double radians);
        }

        // 定义中注释掉无用变量。
        void Circle::Rotate(double /*radians*/) {}

    .. warning::

        .. code-block:: c++

            // 差 - 如果将来有人要实现，很难猜出变量是干什么用的。
            void Circle::Rotate(double) {}

8.5. Lambda 表达式
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. tip::

    其它函数怎么格式化形参和函数体，Lambda 表达式就怎么格式化；捕获列表同理。

    若用引用捕获，在变量名和 ``&`` 之间不留空格。

    .. code-block:: c++

        int x = 0;
        auto add_to_x = [&x](int n) { x += n; };

    短 lambda 就写得和内联函数一样。

    .. code-block:: c++

        std::set<int> blacklist = {7, 8, 9};
        std::vector<int> digits = {3, 9, 1, 8, 4, 7, 1};
        digits.erase(std::remove_if(digits.begin(), digits.end(), [&blacklist](int i) {
                        return blacklist.find(i) != blacklist.end();
                    }),
                    digits.end());

8.6. 函数调用
~~~~~~~~~~~~~~~~~~~~~~

.. tip::

    要么一行写完函数调用，要么在圆括号里对参数分行，要么参数另起一行且缩进四格。如果没有其它顾虑的话，尽可能精简行数，比如把多个参数适当地放在同一行里。

    函数调用遵循如下形式：

    .. code-block:: c++

        bool retval = DoSomething(argument1, argument2, argument3);

    如果同一行放不下，可断为多行，后面每一行都和第一个实参对齐，左圆括号后和右圆括号前不要留空格：

    .. code-block:: c++

        bool retval = DoSomething(averyveryveryverylongargument1,
                                  argument2, argument3);

    参数也可以放在次行，缩进四格：

        .. code-block:: c++

            if (...) {
              ...
              ...
              if (...) {
                DoSomething(
                    argument1, argument2,  // 4 空格缩进
                    argument3, argument4);
              }

    把多个参数放在同一行，是为了减少函数调用所需的行数，除非影响到可读性。有人认为把每个参数都独立成行，不仅更好读，而且方便编辑参数。不过，比起所谓的参数编辑，我们更看重可读性，且后者比较好办：

    如果一些参数本身就是略复杂的表达式，且降低了可读性。那么可以直接创建临时变量描述该表达式，并传递给函数：

    .. code-block:: c++

        int my_heuristic = scores[x] * y + bases[x];
        bool retval = DoSomething(my_heuristic, x, y, z);

    或者放着不管，补充上注释：

    .. code-block:: c++

        bool retval = DoSomething(scores[x] * y + bases[x],  // Score heuristic.
                                  x, y, z);

    如果某参数独立成行，对可读性更有帮助的话，就这么办。

    此外，如果一系列参数本身就有一定的结构，可以酌情地按其结构来决定参数格式：

    .. code-block:: c++

        // 通过 3x3 矩阵转换 widget.
        my_widget.Transform(x1, x2, x3,
                            y1, y2, y3,
                            z1, z2, z3);

.. _braced-initializer-list-format

8.7. 列表初始化格式
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. tip::

    您平时怎么格式化函数调用，就怎么格式化 :ref:`braced_initializer_list`。

    如果列表初始化伴随着名字，比如类型或变量名，您可以当名字是函数、{} 是函数调用的括号来格式化它。反之，就当它有个长度为零的名字。

    .. code-block:: c++

        // 一行列表初始化示范。
        return {foo, bar};
        functioncall({foo, bar});
        pair<int, int> p{foo, bar};

        // 当不得不断行时。
        SomeFunction(
            {"assume a zero-length name before {"},
            some_other_function_parameter);
        SomeType variable{
            some, other, values,
            {"assume a zero-length name before {"},
            SomeOtherType{
                "Very long string requiring the surrounding breaks.",
                some, other values},
            SomeOtherType{"Slightly shorter string",
                          some, other, values}};
        SomeType variable{
            "This is too long to fit all in one line"};
        MyType m = {  // 注意了，您可以在 { 前断行。
            superlongvariablename1,
            superlongvariablename2,
            {short, interior, list},
            {interiorwrappinglist,
             interiorwrappinglist2}};

8.8. 条件语句
~~~~~~~~~~~~~~~~~~~~~~

.. tip::

    倾向于不在圆括号内使用空格. 关键字 ``if`` 和 ``else`` 另起一行.

对基本条件语句有两种可以接受的格式. 一种在圆括号和条件之间有空格, 另一种没有.

最常见的是没有空格的格式. 哪种都可以, 但 *保持一致性*. 如果你是在修改一个文件, 参考当前已有格式. 如果是写新的代码, 参考目录下或项目中其它文件. 还在徘徊的话, 就不要加空格了.

    .. code-block:: c++

        if (condition) {  圆括号里没空格紧邻。
          ...  // 2 空格缩进。
        } else {  // else 与 if 的右括号同一行。
          ...
        }

如果你更喜欢在圆括号内部加空格:

    .. code-block:: c++

        if ( condition ) {  // 圆括号与空格紧邻 - 不常见
          ...  // 2 空格缩进。
        } else {  // else 与 if 的右括号同一行。
          ...
        }

注意所有情况下 ``if`` 和左圆括号间都有个空格. 右圆括号和左大括号之间也要有个空格:

    .. warning::

        .. code-block:: c++

            if(condition)     // 差 - IF 后面没空格。
            if (condition){   // 差 - { 前面没空格。
            if(condition){    // 变本加厉地差。

    .. code-block:: c++

        if (condition) {  // 可 - IF 和 { 都与空格紧邻。

如果能增强可读性, 简短的条件语句允许写在同一行. 只有当语句简单并且没有使用 ``else`` 子句时使用:

    .. code-block:: c++

        if (x == kFoo) return new Foo();
        if (x == kBar) return new Bar();

如果语句有 ``else`` 分支则不允许:

    .. warning::

        .. code-block:: c++

            // 不可以这样子 - 当有 ELSE 分支时 IF 块却只有一行
            if (x) DoThis();
            else DoThat();

通常, 单行语句不需要使用大括号, 如果你喜欢用也没问题; 复杂的条件或循环语句用大括号可读性会更好. 也有一些项目要求 ``if`` 必须总是使用大括号:

    .. code-block:: c++

        if (condition)
          DoSomething();  // 2 空格缩进。

        if (condition) {
          DoSomething();  // 2 空格缩进。
        }

但如果语句中某个 ``if-else`` 分支使用了大括号的话, 其它分支也必须使用:

    .. warning::

        .. code-block:: c++

            // 不可以这样子 - IF 有大括号 ELSE 却没有。
            if (condition) {
                foo;
            } else
                bar;

            // 不可以这样子 - ELSE 有大括号 IF 却没有。
            if (condition)
                foo;
            else {
                bar;
            }


    .. code-block:: c++

        // 只要其中一个分支用了大括号，两个分支都要用上大括号。
        if (condition) {
          foo;
        } else {
          bar;
        }

8.9. 循环和开关选择语句
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. tip::

    ``switch`` 语句可以使用大括号分段，以表明 cases 之间不是连在一起的。在单语句循环里，括号可用可不用。空循环体应使用 ``{}`` 或 ``continue``.

``switch`` 语句中的 ``case`` 块可以使用大括号也可以不用, 取决于你的个人喜好. 如果用的话, 要按照下文所述的方法.

如果有不满足 ``case`` 条件的枚举值, ``switch`` 应该总是包含一个 ``default`` 匹配 (如果有输入值没有 case 去处理, 编译器将报警). 如果 ``default`` 应该永远执行不到, 简单的加条 ``assert``:

    .. code-block:: c++

        switch (var) {
          case 0: {  // 2 空格缩进
            ...      // 4 空格缩进
            break;
          }
          case 1: {
            ...
            break;
          }
          default: {
            assert(false);
          }
        }

在单语句循环里，括号可用可不用：

    .. code-block:: c++

        for (int i = 0; i < kSomeNumber; ++i)
            printf("I love you\n");

        for (int i = 0; i < kSomeNumber; ++i) {
            printf("I take it back\n");
        }

空循环体应使用 ``{}`` 或 ``continue``, 而不是一个简单的分号.

    .. code-block:: c++

        while (condition) {
          // 反复循环直到条件失效。
        }
        for (int i = 0; i < kSomeNumber; ++i) {}  // 可 - 空循环体。
        while (condition) continue;  // 可 - contunue 表明没有逻辑。

    .. warning::

        .. code-block:: c++

            while (condition);  // 差 - 看起来仅仅只是 while/loop 的部分之一。

8.10. 指针和引用表达式
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. tip::

    句点或箭头前后不要有空格. 指针/地址操作符 (``*, &``) 之后不能有空格.

下面是指针和引用表达式的正确使用范例:

    .. code-block:: c++

        x = *p;
        p = &x;
        x = r.y;
        x = r->y;

注意:啊
    - 在访问成员时, 句点或箭头前后没有空格.
    - 指针操作符 ``*`` 或 ``&`` 后没有空格.

在声明指针变量或参数时, 星号与类型或变量名紧挨都可以:

    .. code-block:: c++

        // 好样的，空格前置。
        char *c;
        const string &str;

        // 好样的，空格后置。
        char* c;    // 但别忘了 "char* c, *d, *e, ...;"!
        const string& str;

    .. warning::

        .. code-block:: c++

            char * c;  // 差 - * 两边都有空格
            const string & str;  // 差 - & 两边都有空格。

在单个文件内要保持风格一致, 所以, 如果是修改现有文件, 要遵照该文件的风格.

8.11. 布尔表达式
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. tip::

    如果一个布尔表达式超过 :ref:`标准行宽 <line-length>`, 断行方式要统一一下.

下例中, 逻辑与 (``&&``) 操作符总位于行尾:

    .. code-block:: c++

        if (this_one_thing > this_other_thing &&
            a_third_thing == a_fourth_thing &&
            yet_another & last_one) {
          ...
        }

注意, 上例的逻辑与 (``&&``) 操作符均位于行尾. 这格式在 Google 里很常见，您要把所有操作符放在开头也可以。可以考虑额外插入圆括号, 合理使用的话对增强可读性是很有帮助的. 此外直接用符号形式的操作符，比如 ``&&`` 和 ``~``, 不要用词语形式的 ``and`` 和 ``compl``.

8.12. 函数返回值
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. tip::

    ``return`` 表达式里时没必要都用圆括号。

假如您写 ``x = epr`` 时本来就会加上括号，那 ``return expr;`` 也可如法炮制。

函数返回时不要使用圆括号:

    .. code-block:: c++

        return result;                  // 返回值很简单，没有圆括号。
        // 可以用圆括号把复杂表达式圈起来，改善可读性。
        return (some_long_condition &&
                another_condition);

    .. warning::

        .. code-block:: c++

            return (value);                // 毕竟您从来不会写 var = (value);
            return(result);                // return 可不是函数！

8.13. 变量及数组初始化
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. tip::

    用 ``=``, ``()`` 和 ``{}`` 均可.

您可以用 ``=``, ``()`` 和 ``{}``, 以下都对：

    .. code-block:: c++

        int x = 3;
        int x(3);
        int x{3};
        string name("Some Name");
        string name = "Some Name";
        string name{"Some Name"};

请务必小心列表初始化 {...} 用 ``std::initializer_list`` 构造函数初始化出的类型。非空列表初始化就会优先调用 ``std::initializer_list``, 不过空列表初始化除外，后者原则上会调用默认构造函数。为了强制禁用 ``std::initializer_list`` 构造函数，请改用括号。

    .. code-block:: c++

        vector<int> v(100, 1);  // A vector of 100 1s.
        vector<int> v{100, 1};  // A vector of 100, 1.

此外，列表初始化不允许整型类型的四舍五入，这可以用来避免一些类型上的编程失误。

    .. code-block:: c++

        int pi(3.14);  // 可 -- pi == 3.
        int pi{3.14};  // Compile error: narrowing conversion.

8.14. 预处理指令
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. tip::

    预处理指令不要缩进, 从行首开始.

即使预处理指令位于缩进代码块中, 指令也应从行首开始.

    .. code-block:: c++

        // 可 - directives at beginning of line
          if (lopsided_score) {
        #if DISASTER_PENDING      // 正确 -- 行开头起。
            DropEverything();
        #endif
            BackToNormal();
          }

    .. warning::

        .. code-block:: c++

            // 差 - indented directives
              if (lopsided_score) {
                #if DISASTER_PENDING  // 错了！ "#if" 应该放在行开头
                DropEverything();
                #endif                // 错了！ "#endif" 不要缩进
                BackToNormal();
              }

8.15. 类格式
~~~~~~~~~~~~~~~~~~~~~~

.. tip::

    访问控制块的声明依次序是 ``public:``, ``protected:``, ``private:``, 每次缩进 1 个空格.

类声明 (对类注释不了解的话, 参考 :ref:`类注释 <class-comments>`) 的基本格式如下:

    .. code-block:: c++

        class MyClass : public OtherClass {
         public:      // 注意有 1 空格缩进!
          MyClass();  // 照常，2 空格缩进。
          explicit MyClass(int var);
          ~MyClass() {}

          void SomeFunction();
          void SomeFunctionThatDoesNothing() {
          }

          void set_some_var(int var) { some_var_ = var; }
          int some_var() const { return some_var_; }

         private:
          bool SomeInternalFunction();

          int some_var_;
          int some_other_var_;
          DISALLOW_COPY_AND_ASSIGN(MyClass);
        };

注意事项:

    - 所有基类名应在 80 列限制下尽量与子类名放在同一行.

    - 关键词 ``public:``, ``protected:``, ``private:`` 要缩进 1 个空格.

    - 除第一个关键词 (一般是 ``public``) 外, 其他关键词前要空一行. 如果类比较小的话也可以不空.

    - 这些关键词后不要保留空行.

    - ``public`` 放在最前面, 然后是 ``protected``, 最后是 ``private``.

    - 关于声明顺序的规则请参考 :ref:`声明顺序 <declaration-order>` 一节.

8.16. 构造函数初始值列表
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. tip::

    构造函数初始值列表放在同一行或按四格缩进并排几行.

下面两种初始值列表方式都可以接受:

    .. code-block:: c++

        // 当全放在一行合适时：
        MyClass::MyClass(int var) : some_var_(var), some_other_var_(var + 1) {

或

    .. code-block:: c++

        // 如果要断成多行，缩进四格，冒号放在第一行初始化句：
        MyClass::MyClass(int var)
            : some_var_(var),             // 4 空格缩进
              some_other_var_(var + 1) {  // 对准
          ...
          DoSomething();
          ...
        }

8.17. 名字空间格式化
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. tip::

    名字空间内容不缩进.

:ref:`名字空间 <namespaces>` 不要增加额外的缩进层次, 例如:

    .. code-block:: c++

        namespace {

        void foo() {  // 正确。命名空间内没有额外的缩进。
          ...
        }

        }  // namespace

不要缩进名字空间:

    .. warning::

        .. code-block:: c++

            namespace {

              // 错，缩进多余了。
              void foo() {
                ...
              }

            }  // namespace

声明嵌套命名空间时，每命名空间都独立成行。

    .. code-block:: c++

        namespace foo {
        namespace bar {

8.18. 水平留白
~~~~~~~~~~~~~~~~~~~~~~~~

.. tip::

    水平留白的使用因地制宜. 永远不要在行尾添加没意义的留白.

常规:

    .. code-block:: c++

        void f(bool b) {  // 左大括号前恒有空格。
          ...
        int i = 0;  // 分号前不加空格。
        int x[] = { 0 };  // 大括号内部可与空格紧邻也不可，不过两边都要加上。
        int x[] = {0};
        // 继承与初始化列表中的冒号前后恒有空格。
        class Foo : public Bar {
         public:
          // 至于内联函数实现，在大括号内部加上空格并编写实现。
          Foo(int b) : Bar(), baz_(b) {}  // 大括号里面是空的话，不加空格。
          void Reset() { baz_ = 0; }  // 用括号把大括号与实现分开。
          ...

    添加冗余的留白会给其他人编辑时造成额外负担. 因此, 行尾不要留空格. 如果确定一行代码已经修改完毕, 将多余的空格去掉; 或者在专门清理空格时去掉（确信没有其他人在处理). (Yang.Y 注: 现在大部分代码编辑器稍加设置后, 都支持自动删除行首/行尾空格, 如果不支持, 考虑换一款编辑器或 IDE)

循环和条件语句:

    .. code-block:: c++

        if (b) {          // if 条件语句和循环语句关键字后均有空格。
        } else {          // else 前后有空格。
        }
        while (test) {}   // 圆括号内部不紧邻空格。
        switch (i) {
        for (int i = 0; i < 5; ++i) {
        switch ( i ) {    // 循环和条件语句的圆括号里可以与空格紧邻。
        if ( test ) {     // 圆括号，但这很少见。总之要一致。
        for ( int i = 0; i < 5; ++i ) {
        for ( ; i < 5 ; ++i) {  // 循环里内 ; 后恒有空格，； 前可以加个空格。
        switch (i) {
          case 1:         // switch case 的冒号前无空格。
            ...
          case 2: break;  // 如果冒号有代码，加个空格。

操作符:

    .. code-block:: c++

        // 赋值操作系统前后恒有空格。
        x = 0;

        // 其它二元操作符也前后恒有空格，不过对 factors 前后不加空格也可以。
        // 圆括号内部不紧邻空格。
        v = w * x + y / z;
        v = w*x + y/z;
        v = w * (x + z);

        // 在参数和一元操作符之间不加空格。
        x = -5;
        ++x;
        if (x && !y)
          ...

模板和转换:

    .. code-block:: c++

        // 尖叫括号(< and >) 不与空格紧邻，< 前没有空格，>( 之间也没有。
        vector<string> x;
        y = static_cast<char*>(x);

        // 在类型与指针操作符之间留空格也可以，但要保持一致。
        vector<char *> x;
        set<list<string>> x;        // 在 C++11 代码里可以这样用了。
        set<list<string> > x;       // C++03 中要在 > > 里留个空格。

        // 您或许可以在 < < 里加上一对对称的空格。
        set< list<string> > x;

8.19. 垂直留白
~~~~~~~~~~~~~~~~~~~~~~~~

.. tip::

    垂直留白越少越好.

这不仅仅是规则而是原则问题了: 不在万不得已, 不要使用空行. 尤其是: 两个函数定义之间的空行不要超过 2 行, 函数体首尾不要留空行, 函数体中也不要随意添加空行.

基本原则是: 同一屏可以显示的代码越多, 越容易理解程序的控制流. 当然, 过于密集的代码块和过于疏松的代码块同样难看, 取决于你的判断. 但通常是垂直留白越少越好.

空行心得如下：

* 函数体内开头或结尾的空行可读性微乎其微。
* 在多重 if-else 块里加空行或许有点可读性。

译者 (YuleFox) 笔记
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#. 对于代码格式, 因人, 系统而异各有优缺点, 但同一个项目中遵循同一标准还是有必要的;
#. 行宽原则上不超过 80 列, 把 22 寸的显示屏都占完, 怎么也说不过去;
#. 尽量不使用非 ASCII 字符, 如果使用的话, 参考 UTF-8 格式 (尤其是 UNIX/Linux 下, Windows 下可以考虑宽字符), 尽量不将字符串常量耦合到代码中, 比如独立出资源文件, 这不仅仅是风格问题了;
#. UNIX/Linux 下无条件使用空格, MSVC 的话使用 Tab 也无可厚非;
#. 函数参数, 逻辑条件, 初始化列表: 要么所有参数和函数名放在同一行, 要么所有参数并排分行;
#. 除函数定义的左大括号可以置于行首外, 包括函数/类/结构体/枚举声明, 各种语句的左大括号置于行尾, 所有右大括号独立成行;
#. ``.``/``->`` 操作符前后不留空格, ``*``/``&`` 不要前后都留, 一个就可, 靠左靠右依各人喜好;
#. 预处理指令/命名空间不使用额外缩进, 类/结构体/枚举/函数/语句使用缩进;
#. 初始化用 ``=`` 还是 ``()`` 依个人喜好, 统一就好;
#. ``return`` 不要加 ``()``;
#. 水平/垂直留白不要滥用, 怎么易读怎么来.
#. 关于 UNIX/Linux 风格为什么要把左大括号置于行尾 (``.cc`` 文件的函数实现处, 左大括号位于行首), 我的理解是代码看上去比较简约, 想想行首除了函数体被一对大括号封在一起之外, 只有右大括号的代码看上去确实也舒服; Windows 风格将左大括号置于行首的优点是匹配情况一目了然.

译者（acgtyrant）笔记
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#. 80 行限制事实上有助于避免代码可读性失控，比如超多重嵌套块，超多重函数调用等等。
#. Linux 上设置好了 Locale 就几乎一劳永逸设置好所有开发环境的编码，不像奇葩的 Windows.
#. Google 强调有一对 if-else 时，不论有没有嵌套，都要有大括号。Apple 正好 `有栽过跟头 <http://coolshell.cn/articles/11112.html>`_ .
#. 其实我主张指针／地址操作符与变量名紧邻，``int* a, b`` vs ``int *a, b``, 新手会误以为前者的 ``b`` 是 ``int *`` 变量，但后者就不一样了，高下立判。
#. 在这风格指南里我才刚知道 C++ 原来还有所谓的 `Alternative operator representations <http://en.cppreference.com/w/cpp/language/operator_alternative>`_, 大概没人用吧。
#. 注意构造函数初始值列表（Constructer Initializer List）与列表初始化（Initializer List）是两码事，我就差点混淆了它们的翻译。
#. 事实上，如果您熟悉英语本身的书写规则，就会发现该风格指南在格式上的规定与英语语法相当一脉相承。比如普通标点符号和单词后面还有文本的话，总会留一个空格；特殊符号与单词之间就不用留了，比如 ``if (true)`` 中的圆括号与 ``true``.
#. 本风格指南没有明确规定 void 函数里要不要用 return 语句，不过就 Google 开源项目 leveldb 并没有写；此外从 `Is a blank return statement at the end of a function whos return type is void necessary? <http://stackoverflow.com/questions/9316717/is-a-blank-return-statement-at-the-end-of-a-function-whos-return-type-is-void-ne>`_ 来看，``return;`` 比 ``return ;`` 更约定俗成（事实上 cpplint 会对后者报错，指出分号前有多余的空格），且可用来提前跳出函数栈。
