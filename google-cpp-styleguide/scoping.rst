2. 作用域
----------------

.. _namespaces:

2.1. 命名空间
~~~~~~~~~~~~~~~~~~~~~~~~

.. tip::

    除了少数特殊情况, 应该在命名空间 (namespace) 内放置代码. 命名空间应该有独一无二的名字, 其中包含项目名称, 也可以选择性地包含文件路径. 禁止使用 using 指令 (例如 ``using namespace foo``). 禁止使用内联 (inline) 命名空间. 请参见 :ref:`内部链接 <internal-linkage>` 中关于匿名命名空间 (unamed namespace) 的内容.

**定义:**

    命名空间可以将全局作用域 (global scope) 划分为独立的、有名字的作用域, 因此可以有效防止全局作用域中的命名冲突 (name collision).

**优点:**

    命名空间可以避免大型程序中的命名冲突, 同时代码可以继续使用简短的名称.

    举例来说, 若两个项目的全局作用域中都有一个叫 ``Foo`` 的类 (class), 这两个符号 (symbol) 会在编译或运行时发生冲突. 如果每个项目在不同的命名空间中放置代码, ``project1::Foo`` 和 ``project2::Foo`` 就是截然不同的符号, 不会冲突.

    内联命名空间会自动把其中的标识符置入外层作用域, 比如：

    .. code-block:: c++

        namespace outer {
        inline namespace inner {
            void foo();
        }  // namespace inner
        }  // namespace outer

    此时表达式 ``outer::inner::foo()`` 与 ``outer::foo()`` 等效. 内联命名空间的主要用途是保持不同 ABI 版本之间的兼容性。

**缺点:**

    命名空间让人难以理解, 因为难以找到一个标识符所对应的定义.

    内联命名空间更难理解, 因为其中的标识符不仅仅出现在声明它的命名空间中. 因此内联命名空间只能作为版本控制策略的一部分.

    部分情景下, 我们必须多次使用完全限定名称 (fully-qualified name) 来引用符号. 此时多层嵌套的命名空间会让代码冗长.

**结论:**

    建议按如下方法使用命名空间:

    - 遵守 `命名空间命名 <naming.html#namespace-names>`_ 规则.

    - 像前面的例子一样, 用注释给命名空间收尾. (译者注: 注明命名空间的名字.)

    - 在导入语句、 `gflags <https://gflags.github.io/gflags/>`_ 声明/定义以及其他命名空间的类的前向声明 (forward declaration) 之后, 用命名空间包裹整个源代码文件:

        .. code-block:: c++

            // .h 文件
            namespace mynamespace {

            // 所有声明都位于命名空间中.
            // 注意没有缩进.
            class MyClass {
                public:
                ...
                void Foo();
            };

            }  // namespace mynamespace

        .. code-block:: c++

            // .cc 文件
            namespace mynamespace {

            // 函数定义位于命名空间中.
            void MyClass::Foo() {
                ...
            }

            }  // namespace mynamespace

        更复杂的 ``.cc`` 文件有更多细节, 比如旗标 (flag) 或 using 声明.

        .. code-block:: c++

            #include "a.h"

            DEFINE_FLAG(bool, someflag, false, "某个旗标");

            namespace mynamespace {

            using ::foo::Bar;

            ...命名空间内的代码...  // 代码紧贴左边框.

            }  // namespace mynamespace

    - 若要将自动生成的 proto 消息代码放入命名空间, 可以在 ``.proto`` 文件中使用 ``package`` 修饰符 (specifier). 参见 `Protocol Buffer 的包 <https://developers.google.com/protocol-buffers/docs/reference/cpp-generated#package>`_.

    - 不要在 ``std`` 命名空间内声明任何东西. 不要前向声明 (forward declare) 标准库的类. 在 ``std`` 命名空间内声明实体是未定义行为 (undefined behavior), 也就是会损害可移植性. 若要声明标准库的实体, 应该导入对应的头文件.

    - 禁止使用 *using 指令* 引入命名空间的所有符号。

        .. code-block:: c++

            // 禁止: 这会污染命名空间.
            using namespace foo;

    - 除了在明显标注为内部使用的命名空间内, 不要让头文件引入命名空间别名 (namespace alias). 这是因为头文件的命名空间中引入的任何东西都是该文件的公开 API. 正确示例:

        .. code-block:: c++

            // 在 .cc 中, 用别名缩略常用的名称.
            namespace baz = ::foo::bar::baz;

        .. code-block:: c++

            // 在 .h 中, 用别名缩略常用的命名空间.
            namespace librarian {
            namespace impl {  // 仅限内部使用, 不是 API.
            namespace sidetable = ::pipeline_diagnostics::sidetable;
            }  // namespace impl

            inline void my_inline_function() {
              // 一个函数 (f或方法) 中的局部别名.
              namespace baz = ::foo::bar::baz;
              ...
            }
            }  // namespace librarian

    - 禁止内联命名空间.

    - 如果命名空间的名称包含 "internal", 代表用户不应该使用这些 API.

        .. code-block:: c++

            // Absl 以外的代码不应该使用这一内部符号.
            using ::absl::container_internal::ImplementationDetail;

    - 我们鼓励新的代码使用单行的嵌套命名空间声明, 但不强制要求.

        译者注: 例如

        .. code-block:: c++

            namespace foo::bar {
            ...
            }  // namespace foo::bar

.. _internal-linkage:

2.2. 内部链接
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. tip::

    若其他文件不需要使用 ``.cc`` 文件中的定义, 这些定义可以放入匿名命名空间 (unnamed namespace) 或声明为 ``static``, 以实现内部链接 (internal linkage). 但是不要在 ``.h`` 文件中使用这些手段.

**定义:**

    所有放入匿名命名空间中的声明都会内部链接. 声明为 ``static`` 的函数和变量也会内部链接. 这意味着其他文件不能访问你声明的任何事物. 即使另一个文件声明了一模一样的名称, 这两个实体也都是相互独立的.

**结论:**

    建议 ``.cc`` 文件中所有不需要外部使用的代码采用内部链接. 不要在 ``.h`` 文件中使用内部链接.

    匿名命名空间的声明应与具名命名空间的格式相同. 在末尾的注释中, 不用填写命名空间名称:

    .. code-block:: c++

        namespace {
        ...
        }  // namespace

.. _nonmember-static-member-and-global-functions:

2.3. 非成员函数、静态成员函数和全局函数
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. tip::

    建议将非成员 (nonmember) 函数放入命名空间; 尽量不要使用完全全局的函数 (completely global function). 不要仅仅为了给静态成员 (static member) 分组而使用类 (class). 类的静态方法应当和类的实例或静态数据紧密相关.

**优点:**

    非成员函数和静态成员函数在某些情况下有用. 若将非成员函数放在命名空间内, 不会污染全局命名空间.

**缺点:**

    有时非成员函数和静态成员函数更适合成为一个新的类的成员, 尤其是当它们需要访问外部资源或有明显的依赖关系时.

**结论:**

    有时我们需要定义一个和类的实例无关的函数. 这样的函数可以定义为静态成员函数或非成员函数. 非成员函数不应该依赖外部变量, 且大部分情况下应该位于命名空间中. 不要仅仅为了给静态成员分组而创建一个新类; 这相当于给所有名称添加一个公共前缀, 而这样的分组通常是不必要的.

    如果你定义的非成员函数仅供本 ``.cc`` 文件使用, 请用 :ref:`内部链接 <internal-linkage>` 限制其作用域.

.. _local-variables:

2.4. 局部变量
~~~~~~~~~~~~~~~~~~~~~~

.. tip::

    应该尽可能缩小函数变量的作用域 (scope), 并在声明的同时初始化.

你可以在 C++ 函数的任何位置声明变量. 我们提倡尽可能缩小变量的作用域, 且声明离第一次使用的位置越近越好. 这样读者更容易找到声明, 了解变量的类型和初始值. 特别地, 应该直接初始化变量而非先声明再赋值, 比如:

    .. code-block:: c++

        int i;
        i = f();     // 不好: 初始化和声明分离.

    .. code-block:: c++

        int i = f(); // 良好: 声明时初始化​。

    .. code-block:: c++

        int jobs = NumJobs();
        // 更多代码...
        f(jobs);      // 不好: 初始化和使用位置分离.

    .. code-block:: c++

        int jobs = NumJobs();
        f(jobs);      // 良好: 初始化以后立即 (或很快) 使用.

    .. code-block:: c++

        vector<int> v;
        v.push_back(1);  // 用花括号初始化更好.
        v.push_back(2);

    .. code-block:: c++

        vector<int> v = {1, 2}; // 良好: 立即初始化 v.


通常应该在语句内声明用于 ``if``、``while`` 和 ``for`` 语句的变量, 这样会把作用域限制在语句内. 例如:

    .. code-block:: c++

        while (const char* p = strchr(str, '/')) str = p + 1;


需要注意的是, 如果变量是一个对象, 那么它每次进入作用域时会调用构造函数, 每次退出作用域时都会调用析构函数.

.. code-block:: c++

    // 低效的实现:
    for (int i = 0; i < 1000000; ++i) {
        Foo f;  // 调用 1000000 次构造函数和析构函数.
        f.DoSomething(i);
    }

在循环的作用域外面声明这类变量更高效:

.. code-block:: c++

    Foo f;  // 调用 1 次构造函数和析构函数.
    for (int i = 0; i < 1000000; ++i) {
        f.DoSomething(i);
    }

.. _static-and-global-variables:

2.5. 静态和全局变量
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. tip::

    禁止使用 `静态储存周期 (static storage duration) <http://zh.cppreference.com/w/cpp/language/storage_duration#.E5.AD.98.E5.82.A8.E6.9C.9F>`_ 的变量, 除非它们可以 `平凡地析构 (trivially destructible) <https://zh.cppreference.com/w/cpp/types/is_destructible>`_. 简单来说, 就是析构函数 (destructor) 不会做任何事情, 包括成员和基类 (base) 的析构函数. 正式地说, 就是这一类型 (type) 没有用户定义的析构函数或虚析构函数 (virtual destructor), 且所有成员和基类也能平凡地析构. 函数的局部静态变量可以动态地初始化 (dynamic initialization) . 除了少数情况外, 不推荐动态初始化静态类成员变量或命名空间内的变量. 详情参见下文.

作为经验之谈: 若只看全局变量的声明, 如果该语句可以作为常量表达式 (constexpr), 则满足以上要求.

**定义:**

    每个对象 (object) 都有与生命周期 (linetime) 相关的储存周期 (storage duration). 静态储存周期对象的存活时间是从程序初始化开始, 到程序结束为止. 这些对象可能是命名空间作用域内的变量 (全局变量)、类的静态数据成员或者用 ``static`` 修饰符 (specifier) 声明的函数局部变量. 对于函数局部静态变量, 初始化发生在在控制流第一次经过声明时; 所有其他对象会在程序启动时初始化. 程序退出时会销毁所有静态储存周期的对象 (这发生在未汇合 (join) 的线程终止前).

    初始化过程可以是动态 (dynamic) 的, 也就是初始化过程中有不平凡 (non-trivial) 的操作. (例如, 会分配内存的构造函数, 或者用当前进程 ID 初始化的变量.) 其他初始化都是静态 (static) 初始化. 二者并非水火不容: 静态储存周期的变量 **一定** 会静态初始化 (初始化为指定常量或给所有字节清零), 必要时会随后再次动态初始化.

**优点:**

    全局或静态变量对很多场景有帮助: 具名常量 (named constants)、编译单元 (translation unit) 内部的辅助数据结构、命令行旗标 (flag)、日志、注册机制、后台基础设施等等.

**缺点:**

    使用动态初始化或具有非平凡析构函数的全局和静态变量时, 会增加代码复杂度, 容易引发难以察觉的错误. 不同编译单元的动态初始化顺序不确定, 析构顺序也不确定 (只知道析构顺序一定是初始化顺序的逆序). 如果静态变量的初始化代码引用了另一个静态储存周期的变量, 这次访问可能发生在另一变量的生命周期开始前 (或生命周期结束后). 此外, 若有些线程没有在程序结束前汇合, 这些线程可能在静态变量析构后继续访问这些变量.

**决定:**

    **关于析构的决定**

    平凡的析构函数不受执行顺序影响 (他们实际上不算"执行"); 其他析构函数则有风险, 可能访问生命周期已结束的对象. 因此, 只有拥有平凡析构函数的对象才能采用静态储存周期. 基本类型 (例如指针和 ``int``) 可以平凡地析构, 可平凡析构的类型所构成的数组也可以平凡地析构. 注意, 用 ``constexpr`` 修饰的变量可以平凡地析构.

    .. code-block:: c++

        const int kNum = 10;  // 允许

        struct X { int n; };
        const X kX[] = {{1}, {2}, {3}};  // 允许

        void foo() {
          static const char* const kMessages[] = {"hello", "world"};  // 允许
        }

        // 允许: constexpr 可以保证析构函数是平凡的.
        constexpr std::array<int, 3> kArray = {1, 2, 3};

    .. code-block:: c++

        // 不好: 非平凡的析构.
        const std::string kFoo = "foo";

        // 和上面相同的原因, 即使 kBar 是引用 (该规则也适用于生命周期被延长的临时对象).
        const std::string& kBar = StrCat("a", "b", "c");

        void bar() {
          // 不好: 非平凡的析构.
          static std::map<int, int> kData = {{1, 0}, {2, 0}, {3, 0}};
        }

    注意, 引用不是对象, 因此它们的析构函数不受限. 但是, 它们仍需遵守动态初始化的限制. 特别地, 我们允许形如 ``static T& t = *new T;`` 的函数内局部静态引用.

    **关于初始化的决定**

    初始化是更复杂的话题, 因为我们不仅需要考虑构造函数的执行过程, 也要考虑初始化表达式 (initializer) 的求值过程.

    .. code-block:: c++

        int n = 5;    // 可以
        int m = f();  // ? (依赖 f)
        Foo x;        // ? (依赖 Foo::Foo)
        Bar y = g();  // ? (依赖 g 和 Bar::Bar)
    
    除了第一行语句以外, 其他语句都会受到不确定的初始化顺序影响.

    我们所需的概念在 C++ 标准中的正式称谓是常量初始化 (constant initialization). 这意味着初始化表达式是常量表达式 (constant expression), 并且如果要用构造函数进行初始化, 则该构造函数也必须声明为 ``constexpr``:

    .. code-block:: c++

        struct Foo { constexpr Foo(int) {} };

        int n = 5;  // 可以, 5 是常量表达式.
        Foo x(2);   // 可以, 2 是常量表达式且被选中的构造函数也是 constexpr.
        Foo a[] = { Foo(1), Foo(2), Foo(3) };  // 可以
    
    可以自由使用常量初始化. 应该用 ``constexpr`` 或 ``constinit`` 标记静态变量的常量初始化过程. 应该假设任何没有这些标记的静态变量都是动态初始化的, 并谨慎地检查这些代码.

    作为反例, 以下初始化过程有问题:

    .. code-block:: c++

        // 下文使用了这些声明.
        time_t time(time_t*);      // 不是 constexpr!
        int f();                   // 不是 constexpr!
        struct Bar { Bar() {} };

        // 有问题的初始化.
        time_t m = time(nullptr);  // 初始化表达式不是常量表达式.
        Foo y(f());                // 同上
        Bar b;                     // 被选中的构造函数 Bar::Bar() 不是 constexpr.
    
    我们不建议且通常禁止动态地初始化全局变量. 不过, 如果这一初始化过程不依赖于其他初始化过程的顺序, 则可以允许. 若满足这一要求, 则初始化的顺序变化不会产生任何区别. 例如:

    .. code-block:: c++

        int p = getpid();  // 若其他静态变量不会在初始化过程中使用 p, 则允许.
    
    允许动态地初始化静态局部变量 (这是常见的).

    **常用的语法结构**

    - 全局字符串: 如果你需要具名的 (named) 全局或静态字符串常量, 可以采用 ``constexpr`` 修饰的 ``string_view`` 变量、字符数组或指向字符串字面量 (literal) 的字符指针. 字符串字面量具有静态储存周期, 因此通常能满足需要. 参见 `第 140 号每周提示 <https://abseil.io/tips/140>`_.
    - 字典和集合等动态容器 (container): 若你需要用静态变量储存不会改变的数据 (例如用于搜索的集合或查找表), 不要使用标准库的动态容器, 因为这些容器拥有非平凡的析构函数. 可以考虑用平凡类型的数组替代, 例如 ``int`` 数组的数组 (作为把 ``int`` 映射到 ``int`` 的字典) 或者数对 (pair) 的数组 (例如一组 ``int`` 和 ``const char*`` 的数对). 对于少量数据, 线性搜索就足够了, 而且因为具有内存局部性 (memory locality) 而更加高效; 可以使用 `absl/algorithm/container.h <https://github.com/abseil/abseil-cpp/blob/master/absl/algorithm/container.h>`_ 中的工具实现常见操作. 如有需要, 可以保持数据有序并采用二分查找法 (binary search). 如果你确实需要使用标准库的动态容器, 建议使用如下文所述的函数内局部静态指针.
    - 智能指针 (smart pointer, 例如 ``std::unique_ptr`` 和 ``std::shared_ptr``) 在析构时有释放资源的操作, 因此不能作为静态变量. 请思考你的情景是否适用于本小节描述的其他模式. 简单的解决方式是, 用裸指针 (plain pointer) 指向动态分配的对象, 并且永远不删除这个对象 (参见最后一点).
    - 自定义类型的静态变量: 如果静态数据或常量数据是自定义类型, 请给这一类型设置平凡的析构函数和 ``constexpr`` 修饰的构造函数.
    - 若以上都不适用, 你可以采用函数内局部静态指针或引用, 动态分配一个对象且永不删除 (例如 ``static const auto& impl = *new T(args...);``).

2.6. thread_local 变量
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. tip::

    必须使用编译期常量 (compile-time constant) 初始化在函数外定义的 ``thread_local`` 变量, 且必须使用 `ABSL_CONST_INIT <https://github.com/abseil/abseil-cpp/blob/master/absl/base/attributes.h>`_ 属性来强制执行这一规则. 优先采用 ``thread_local``, 而非其他定义线程内局部数据的方法.

**定义:**

    我们可以用 ``thread_local`` 修饰符声明变量:

    .. code-block:: c++

        thread_local Foo foo = ...;
    
    这样的变量本质上其实是一组不同的对象. 不同线程访问该变量时, 会访问各自的对象. ``thread_local`` 变量在很多方面类似于 :ref:`静态储存周期的变量 <static-and-global-variables>`. 例如, 可以在命名空间内、函数内或类的静态成员内声明这些变量, 但不能在类的普通成员内声明它们.

    ``thread_local`` 实例与静态变量的初始化过程类似, 区别是 ``thread_local`` 实例会在每个线程启动时初始化, 而非程序启动时初始化. 这意味着函数内的 ``thread_local`` 变量是线程安全的. 若要访问其他 ``thread_local`` 变量, 则有跟静态变量一样的初始化顺序问题 (而且问题更大).

    ``thread_local`` 的变量也有微妙的析构顺序问题: 线程终止时, ``thread_local`` 的销毁顺序是初始化顺序的逆序 (正如 C++ 在其他部分的规则一样). 如果 ``thread_local`` 的变量在析构过程中访问了该线程中已销毁的其他 ``thread_local`` 变量, 就会出现难以调试的释放后使用 (use-after-free, 即野指针) 问题.

**优点:**

    - 线程的局部数据可以从根本上防止竞态条件 (race) (因为通常只有一个线程访问), 因此 ``thread_local`` 能帮助并行化.
    - 在创建线程局部数据的各种方法中, ``thread_local`` 是由语法标准支持的唯一方法.

**缺点:**

    - 在线程启动或首次使用 ``thread_local`` 变量时, 可能触发很多难以预测、运行时间不可控的其他代码.
    - ``thread_local`` 本质上是全局变量. 除了线程安全以外, 它具有全局变量的所有其他缺点.
    - 在最坏情况下, ``thread_local`` 变量占用的内存与线程数量成正比, 占用量可能十分巨大.
    - 成员数据 (data member) 必须是静态的才能声明为 ``thread_local``.
    - 若 ``thread_local`` 变量拥有复杂的析构函数, 我们可能遇到野指针. 特别地, 析构函数不能 (直接或间接地) 访问任何有可能已被销毁的其他 ``thread_local`` 变量. 我们难以检查这一规则.
    - 那些用于全局/静态变量的、预防野指针的方法不适用于 ``thread_local``. 展开来说, 我们可以跳过全局或局部变量的析构函数, 因为他们的生命周期会随着程序终止而自然结束. 因此, 操作系统很快就会回收泄露的内存和其他资源. 然而, 若跳过 ``thread_local`` 的析构函数, 那么资源泄漏量和程序运行期间创建的线程数量成正比.

**决定:**

    位于类或命名空间中的 ``thread_local`` 变量只能用真正的编译时常量来初始化  (也就是不能动态初始化). 必须用 `ABSL_CONST_INIT <https://github.com/abseil/abseil-cpp/blob/master/absl/base/attributes.h>`_ 修饰来保证这一点 (也可以用 ``constexpr`` 修饰, 但不常见). 

    .. code-block:: c++
        
        ABSL_CONST_INIT thread_local Foo foo = ...;
    
    函数中的 ``thread_local`` 变量没有初始化的顾虑, 但是在线程退出时有释放后使用的风险. 注意, 你可以用静态方法暴露函数内的 ``thread_local`` 变量, 来模拟类或命名空间中的 ``thread_local`` 变量:

    .. code-block:: c++

        Foo& MyThreadLocalFoo() {
          thread_local Foo result = ComplicatedInitialization();
          return result;
        }
    
    注意, 线程退出时会销毁 ``thread_local`` 变量. 如果析构函数使用了任何其他 (可能已经销毁的) ``thead_local`` 变量, 我们会遇到难以调试的野指针. 建议使用平凡的类型, 或析构函数中没有自定义代码的类型, 以减少访问其他 ``thread_local`` 变量的可能性.

    建议优先使用 ``thread_local`` 定义线程的局部数据, 而非其他机制.

译者 (YuleFox) 笔记
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#. ``cc`` 中的匿名命名空间可避免命名冲突, 限定作用域, 避免直接使用 ``using`` 关键字污染命名空间;
#. 嵌套类符合局部使用原则, 只是不能在其他头文件中前置声明, 尽量不要 ``public``;
#. 尽量不用全局函数和全局变量, 考虑作用域和命名空间限制, 尽量单独形成编译单元;
#. 多线程中的全局变量 (含静态成员变量) 不要使用 ``class`` 类型 (含 STL 容器), 避免不明确行为导致的 bug.
#. 作用域的使用, 除了考虑名称污染, 可读性之外, 主要是为降低耦合, 提高编译/执行效率.

译者（acgtyrant）笔记
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#. 注意「using 指示（using-directive）」和「using 声明（using-declaration）」的区别。
#. 匿名命名空间说白了就是文件作用域，就像 C static 声明的作用域一样，后者已经被 C++ 标准提倡弃用。
#. 局部变量在声明的同时进行显式值初始化，比起隐式初始化再赋值的两步过程要高效，同时也贯彻了计算机体系结构重要的概念「局部性（locality）」。
#. 注意别在循环犯大量构造和析构的低级错误。
