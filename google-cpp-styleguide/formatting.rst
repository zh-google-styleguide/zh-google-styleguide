8. 格式
------------

代码风格和格式确实比较随意, 但一个项目中所有人遵循同一风格是非常容易的. 个体未必同意下述每一处格式规则, 但整个项目服从统一的编程风格是很重要的, 只有这样才能让所有人能很轻松的阅读和理解代码.

另外, 我们写了一个 `emacs 配置文件 <http://google-styleguide.googlecode.com/svn/trunk/google-c-style.el>`_ 来帮助你正确的格式化代码.

.. _line-length:

8.1. 行长度
~~~~~~~~~~~~~~~~~~~~~~~~~~

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
    - :ref:`头文件保护 <define_guard>` 可以无视该原则.
    
8.2. 非 ASCII 字符
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. tip::
    尽量不使用非 ASCII 字符, 使用时必须使用 UTF-8 编码.
    
即使是英文, 也不应将用户界面的文本硬编码到源代码中, 因此非 ASCII 字符要少用. 特殊情况下可以适当包含此类字符. 如, 代码分析外部数据文件时, 可以适当硬编码数据文件中作为分隔符的非 ASCII 字符串; 更常见的是 (不需要本地化的) 单元测试代码可能包含非 ASCII 字符串. 此类情况下, 应使用 UTF-8 编码, 因为很多工具都可以理解和处理 UTF-8 编码. 十六进制编码也可以, 能增强可读性的情况下尤其鼓励 —— 比如 ``"\xEF\xBB\xBF"`` 在 Unicode 中是 *零宽度 无间断* 的间隔符号, 如果不用十六进制直接放在 UTF-8 格式的源文件中, 是看不到的. (yospaly 注: ``"\xEF\xBB\xBF"`` 通常用作 UTF-8 with BOM 编码标记)

8.3. 空格还是制表位
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. tip::
    只使用空格, 每次缩进 2 个空格.
    
我们使用空格缩进. 不要在代码中使用制符表. 你应该设置编辑器将制符表转为空格.

8.4. 函数声明与定义
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. tip::
    返回类型和函数名在同一行, 参数也尽量放在同一行.
    
函数看上去像这样:
    .. code-block:: c++
        
        ReturnType ClassName::FunctionName(Type par_name1, Type par_name2) {
            DoSomething();
            ...
        }
    
如果同一行文本太多, 放不下所有参数:
    .. code-block:: c++
        
        ReturnType ClassName::ReallyLongFunctionName(Type par_name1,
                                                     Type par_name2,
                                                     Type par_name3) {
            DoSomething();
            ...
        }
    
甚至连第一个参数都放不下:
    .. code-block:: c++
        
        ReturnType LongClassName::ReallyReallyReallyLongFunctionName(
                Type par_name1,  // 4 space indent
                Type par_name2,
                Type par_name3) {
            DoSomething();  // 2 space indent
            ...
        }
    
注意以下几点:

    - 返回值总是和函数名在同一行;

    - 左圆括号总是和函数名在同一行;

    - 函数名和左圆括号间没有空格;

    - 圆括号与参数间没有空格;

    - 左大括号总在最后一个参数同一行的末尾处;

    - 右大括号总是单独位于函数最后一行;

    - 右圆括号和左大括号间总是有一个空格;

    - 函数声明和实现处的所有形参名称必须保持一致;

    - 所有形参应尽可能对齐;

    - 缺省缩进为 2 个空格;

    - 换行后的参数保持 4 个空格的缩进;

如果函数声明成 ``const``, 关键字 ``const`` 应与最后一个参数位于同一行:=
    .. code-block:: c++
    
        // Everything in this function signature fits on a single line
        ReturnType FunctionName(Type par) const {
          ...
        }
        
        // This function signature requires multiple lines, but
        // the const keyword is on the line with the last parameter.
        ReturnType ReallyLongFunctionName(Type par1,
                                          Type par2) const {
          ...
        }
        
如果有些参数没有用到, 在函数定义处将参数名注释起来:
    .. code-block:: c++
        
        // Always have named parameters in interfaces.
        class Shape {
         public:
          virtual void Rotate(double radians) = 0;
        }
        
        // Always have named parameters in the declaration.
        class Circle : public Shape {
         public:
          virtual void Rotate(double radians);
        }
        
        // Comment out unused named parameters in definitions.
        void Circle::Rotate(double /*radians*/) {}
    
    .. warning::
        .. code-block:: c++
            
            // Bad - if someone wants to implement later, it's not clear what the
            // variable means.
            void Circle::Rotate(double) {}


8.5. 函数调用
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. tip::
    尽量放在同一行, 否则, 将实参封装在圆括号中.
    
函数调用遵循如下形式:
    .. code-block:: c++
        
        bool retval = DoSomething(argument1, argument2, argument3);
        
如果同一行放不下, 可断为多行, 后面每一行都和第一个实参对齐, 左圆括号后和右圆括号前不要留空格:
    .. code-block:: c++
        
        bool retval = DoSomething(averyveryveryverylongargument1,
                                  argument2, argument3);
                                  
如果函数参数很多, 出于可读性的考虑可以在每行只放一个参数:
    .. code-block:: c++
        
        bool retval = DoSomething(argument1,
                                  argument2,
                                  argument3,
                                  argument4);
                                  
如果函数名非常长, 以至于超过 :ref:`行最大长度 <line-length>`, 可以将所有参数独立成行:
    .. code-block:: c++
        
        if (...) {
          ...
          ...
          if (...) {
            DoSomethingThatRequiresALongFunctionName(
                very_long_argument1,  // 4 space indent
                argument2,
                argument3,
                argument4);
          }

8.6. 条件语句
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. tip::
    倾向于不在圆括号内使用空格. 关键字 ``else`` 另起一行.
    
对基本条件语句有两种可以接受的格式. 一种在圆括号和条件之间有空格, 另一种没有.

最常见的是没有空格的格式. 哪种都可以, 但 *保持一致性*. 如果你是在修改一个文件, 参考当前已有格式. 如果是写新的代码, 参考目录下或项目中其它文件. 还在徘徊的话, 就不要加空格了.
    .. code-block:: c++
        
        if (condition) {  // no spaces inside parentheses
          ...  // 2 space indent.
        } else {  // The else goes on the same line as the closing brace.
          ...
        }
        
如果你更喜欢在圆括号内部加空格:
    .. code-block:: c++
        
        if ( condition ) {  // spaces inside parentheses - rare
          ...  // 2 space indent.
        } else {  // The else goes on the same line as the closing brace.
          ...
        }
        
注意所有情况下 ``if`` 和左圆括号间都有个空格. 右圆括号和左大括号之间也要有个空格:
    .. warning::
        .. code-block:: c++
        
            if(condition)     // Bad - space missing after IF.
            if (condition){   // Bad - space missing before {.
            if(condition){    // Doubly bad.
    
    .. code-block:: c++
        
        if (condition) {  // Good - proper space after IF and before {.
        
如果能增强可读性, 简短的条件语句允许写在同一行. 只有当语句简单并且没有使用 ``else`` 子句时使用:
    .. code-block:: c++
        
        if (x == kFoo) return new Foo();
        if (x == kBar) return new Bar();
        
如果语句有 ``else`` 分支则不允许:
    .. warning::
        .. code-block:: c++
        
            // Not allowed - IF statement on one line when there is an ELSE clause
            if (x) DoThis();
            else DoThat();
        
通常, 单行语句不需要使用大括号, 如果你喜欢用也没问题; 复杂的条件或循环语句用大括号可读性会更好. 也有一些项目要求 ``if`` 必须总是使用大括号:
    .. code-block:: c++
        
        if (condition)
          DoSomething();  // 2 space indent.
        
        if (condition) {
          DoSomething();  // 2 space indent.
        }
        
但如果语句中某个 ``if-else`` 分支使用了大括号的话, 其它分支也必须使用:
    .. warning::
        
        .. code-block:: c++
        
            // Not allowed - curly on IF but not ELSE
            if (condition) {
                foo;
            } else
                bar;
            
            // Not allowed - curly on ELSE but not IF
            if (condition)
                foo;
            else {
                bar;
            }
    
    
    .. code-block:: c++
        
        // Curly braces around both IF and ELSE required because
        // one of the clauses used braces.
        if (condition) {
          foo;
        } else {
          bar;
        }


8.7. 循环和开关选择语句
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. tip::
    ``switch`` 语句可以使用大括号分段. 空循环体应使用 ``{}`` 或 ``continue``.
    
``switch`` 语句中的 ``case`` 块可以使用大括号也可以不用, 取决于你的个人喜好. 如果用的话, 要按照下文所述的方法.

如果有不满足 ``case`` 条件的枚举值, ``switch`` 应该总是包含一个 ``default`` 匹配 (如果有输入值没有 case 去处理, 编译器将报警). 如果 ``default`` 应该永远执行不到, 简单的加条 ``assert``:
    .. code-block:: c++
        
        switch (var) {
          case 0: {  // 2 space indent
            ...      // 4 space indent
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
        
空循环体应使用 ``{}`` 或 ``continue``, 而不是一个简单的分号.
    .. code-block:: c++
        
        while (condition) {
          // Repeat test until it returns false.
        }
        for (int i = 0; i < kSomeNumber; ++i) {}  // Good - empty body.
        while (condition) continue;  // Good - continue indicates no logic.
    
    .. warning::
        .. code-block:: c++
        
            while (condition);  // Bad - looks like part of do/while loop.
        
8.8. 指针和引用表达式
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. tip::
    句点或箭头前后不要有空格. 指针/地址操作符 (``*, &``) 之后不能有空格.
    
下面是指针和引用表达式的正确使用范例:
    .. code-block:: c++
        
        x = *p;
        p = &x;
        x = r.y;
        x = r->y;

注意:
    - 在访问成员时, 句点或箭头前后没有空格.
    - 指针操作符 ``*`` 或 ``&`` 后没有空格.
    
在声明指针变量或参数时, 星号与类型或变量名紧挨都可以:
    .. code-block:: c++
        
        // These are fine, space preceding.
        char *c;
        const string &str;
        
        // These are fine, space following.
        char* c;    // but remember to do "char* c, *d, *e, ...;"!
        const string& str;
    
    .. warning::
        .. code-block:: c++
        
            char * c;  // Bad - spaces on both sides of *
            const string & str;  // Bad - spaces on both sides of &
        
在单个文件内要保持风格一致, 所以, 如果是修改现有文件, 要遵照该文件的风格.

8.9. 布尔表达式
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. tip::
    如果一个布尔表达式超过 :ref:`标准行宽 <line-length>`, 断行方式要统一一下.
    
下例中, 逻辑与 (``&&``) 操作符总位于行尾:
    .. code-block:: c++
        
        if (this_one_thing > this_other_thing &&
            a_third_thing == a_fourth_thing &&
            yet_another & last_one) {
          ...
        }
        
注意, 上例的逻辑与 (``&&``) 操作符均位于行尾. 可以考虑额外插入圆括号, 合理使用的话对增强可读性是很有帮助的.


8.10. 函数返回值
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. tip::
    ``return`` 表达式中不要用圆括号包围.
    
函数返回时不要使用圆括号:
    .. code-block:: c++
        
        return x;  // not return(x);
        
8.11. 变量及数组初始化
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. tip::
    用 ``=`` 或 ``()`` 均可.
    
在二者中做出选择; 下面的方式都是正确的:
    .. code-block:: c++
        
        int x = 3;
        int x(3);
        string name("Some Name");
        string name = "Some Name";


8.12. 预处理指令
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. tip::
    预处理指令不要缩进, 从行首开始.
    
即使预处理指令位于缩进代码块中, 指令也应从行首开始.
    .. code-block:: c++
        
        // Good - directives at beginning of line
          if (lopsided_score) {
        #if DISASTER_PENDING      // Correct -- Starts at beginning of line
            DropEverything();
        #endif
            BackToNormal();
          }
          
    .. warning::
        .. code-block:: c++
            
            // Bad - indented directives
              if (lopsided_score) {
                #if DISASTER_PENDING  // Wrong!  The "#if" should be at beginning of line
                DropEverything();
                #endif                // Wrong!  Do not indent "#endif"
                BackToNormal();
              }


8.13. 类格式
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. tip::
    访问控制块的声明依次序是 ``public:``, ``protected:``, ``private:``, 每次缩进 1 个空格.
    
类声明 (对类注释不了解的话, 参考 :ref:`类注释 <class-comments>`) 的基本格式如下:
    .. code-block:: c++
        
        class MyClass : public OtherClass {
         public:      // Note the 1 space indent!
          MyClass();  // Regular 2 space indent.
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
    
8.14. 初始化列表
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. tip::
    构造函数初始化列表放在同一行或按四格缩进并排几行.
    
下面两种初始化列表方式都可以接受:
    
    .. code-block:: c++
        
        // When it all fits on one line:
        MyClass::MyClass(int var) : some_var_(var), some_other_var_(var + 1) {
        
或
    
    .. code-block:: c++
        
        // When it requires multiple lines, indent 4 spaces, putting the colon on
        // the first initializer line:
        MyClass::MyClass(int var)
            : some_var_(var),             // 4 space indent
              some_other_var_(var + 1) {  // lined up
          ...
          DoSomething();
          ...
        }
        
8.15. 名字空间格式化
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. tip::
    名字空间内容不缩进.
    
:ref:`名字空间 <namespaces>` 不要增加额外的缩进层次, 例如:
    .. code-block:: c++
        
        namespace {

        void foo() {  // Correct.  No extra indentation within namespace.
          ...
        }

        }  // namespace
        
不要缩进名字空间:
    .. warning::
        .. code-block:: c++
        
            namespace {

              // Wrong.  Indented when it should not be.
              void foo() {
                ...
              }

            }  // namespace

        
8.16. 水平留白
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. tip::
    水平留白的使用因地制宜. 永远不要在行尾添加没意义的留白.
    
常规:
    .. code-block:: c++
        
        void f(bool b) {  // Open braces should always have a space before them.
          ...
        int i = 0;  // Semicolons usually have no space before them.
        int x[] = { 0 };  // Spaces inside braces for array initialization are
        int x[] = {0};    // optional.  If you use them, put them on both sides!
        // Spaces around the colon in inheritance and initializer lists.
        class Foo : public Bar {
         public:
          // For inline function implementations, put spaces between the braces
          // and the implementation itself.
          Foo(int b) : Bar(), baz_(b) {}  // No spaces inside empty braces.
          void Reset() { baz_ = 0; }  // Spaces separating braces from implementation.
          ...
    
    添加冗余的留白会给其他人编辑时造成额外负担. 因此, 行尾不要留空格. 如果确定一行代码已经修改完毕, 将多余的空格去掉; 或者在专门清理空格时去掉（确信没有其他人在处理). (yospaly 注: 现在大部分代码编辑器稍加设置后, 都支持自动删除行首/行尾空格, 如果不支持, 考虑换一款编辑器或 IDE)


循环和条件语句:
    .. code-block:: c++
        
        if (b) {          // Space after the keyword in conditions and loops.
        } else {          // Spaces around else.
        }
        while (test) {}   // There is usually no space inside parentheses.
        switch (i) {
        for (int i = 0; i < 5; ++i) {
        switch ( i ) {    // Loops and conditions may have spaces inside
        if ( test ) {     // parentheses, but this is rare.  Be consistent.
        for ( int i = 0; i < 5; ++i ) {
        for ( ; i < 5 ; ++i) {  // For loops always have a space after the
          ...                   // semicolon, and may have a space before the
                                // semicolon.
        switch (i) {
          case 1:         // No space before colon in a switch case.
            ...
          case 2: break;  // Use a space after a colon if there's code after it.
          
操作符:
    .. code-block:: c++
        
        x = 0;              // Assignment operators always have spaces around
                            // them.
        x = -5;             // No spaces separating unary operators and their
        ++x;                // arguments.
        if (x && !y)
          ...
        v = w * x + y / z;  // Binary operators usually have spaces around them,
        v = w*x + y/z;      // but it's okay to remove spaces around factors.
        v = w * (x + z);    // Parentheses should have no spaces inside them.


模板和转换:
    .. code-block:: c++
        
        vector<string> x;           // No spaces inside the angle
        y = static_cast<char*>(x);  // brackets (< and >), before
                                    // <, or between >( in a cast.
        vector<char *> x;           // Spaces between type and pointer are
                                    // okay, but be consistent.
        set<list<string> > x;       // C++ requires a space in > >.
        set< list<string> > x;      // You may optionally make use
                                    // symmetric spacing in < <.

8.17. 垂直留白
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. tip::
    垂直留白越少越好.
    
这不仅仅是规则而是原则问题了: 不在万不得已, 不要使用空行. 尤其是: 两个函数定义之间的空行不要超过 2 行, 函数体首尾不要留空行, 函数体中也不要随意添加空行.

基本原则是: 同一屏可以显示的代码越多, 越容易理解程序的控制流. 当然, 过于密集的代码块和过于疏松的代码块同样难看, 取决于你的判断. 但通常是垂直留白越少越好.

.. warning:: 函数首尾不要有空行
    
    .. code-block:: c++
        
        void Function() {
        
          // Unnecessary blank lines before and after
        
        }

.. warning:: 代码块首尾不要有空行
    
    .. code-block:: c++
    
        while (condition) {
          // Unnecessary blank line after
        
        }
        if (condition) {
        
          // Unnecessary blank line before
        }
        
``if-else`` 块之间空一行是可以接受的:
    .. code-block:: c++
        
        if (condition) {
          // Some lines of code too small to move to another function,
          // followed by a blank line.

        } else {
          // Another block of code
        }

译者 (YuleFox) 笔记
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

0. 对于代码格式, 因人, 系统而异各有优缺点, 但同一个项目中遵循同一标准还是有必要的;
1. 行宽原则上不超过 80 列, 把 22 寸的显示屏都占完, 怎么也说不过去;
2. 尽量不使用非 ASCII 字符, 如果使用的话, 参考 UTF-8 格式 (尤其是 UNIX/Linux 下, Windows 下可以考虑宽字符), 尽量不将字符串常量耦合到代码中, 比如独立出资源文件, 这不仅仅是风格问题了;
3. UNIX/Linux 下无条件使用空格, MSVC 的话使用 Tab 也无可厚非;
4. 函数参数, 逻辑条件, 初始化列表: 要么所有参数和函数名放在同一行, 要么所有参数并排分行;
5. 除函数定义的左大括号可以置于行首外, 包括函数/类/结构体/枚举声明, 各种语句的左大括号置于行尾, 所有右大括号独立成行;
6. ``.``/``->`` 操作符前后不留空格, ``*``/``&`` 不要前后都留, 一个就可, 靠左靠右依各人喜好;
7. 预处理指令/命名空间不使用额外缩进, 类/结构体/枚举/函数/语句使用缩进;
8. 初始化用 ``=`` 还是 ``()`` 依个人喜好, 统一就好;
9. ``return`` 不要加 ``()``;
10. 水平/垂直留白不要滥用, 怎么易读怎么来.
11. 关于 UNIX/Linux 风格为什么要把左大括号置于行尾 (``.cc`` 文件的函数实现处, 左大括号位于行首), 我的理解是代码看上去比较简约, 想想行首除了函数体被一对大括号封在一起之外, 只有右大括号的代码看上去确实也舒服; Windows 风格将左大括号置于行首的优点是匹配情况一目了然.
