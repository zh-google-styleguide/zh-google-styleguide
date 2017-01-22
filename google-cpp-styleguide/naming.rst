6. 命名约定
------------------

最重要的一致性规则是命名管理. 命名风格快速获知名字代表是什么东东: 类型? 变量? 函数? 常量? 宏 ... ? 甚至不需要去查找类型声明. 我们大脑中的模式匹配引擎可以非常可靠的处理这些命名规则.

命名规则具有一定随意性, 但相比按个人喜好命名, 一致性更重, 所以不管你怎么想, 规则总归是规则.

6.1. 通用命名规则
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. tip::

    函数命名，变量命名，文件命名要有描述性；少用缩写。

    尽可能给有描述性的命名，别心疼空间，毕竟让代码易于新读者理解很重要。不要用只有项目开发者能理解的缩写，也不要通过砍掉几个字母来缩写单词。

    .. code-block:: c++

        int price_count_reader;    // 无缩写
        int num_errors;            // “num” 本来就很常见
        int num_dns_connections;   // 人人都知道 “DNS” 是啥

    .. warning::

        .. code-block:: c++

            int n;                     // 莫名其妙。
            int nerr;                  // 怪缩写。
            int n_comp_conns;          // 怪缩写。
            int wgc_connections;       // 只有贵团队知道是啥意思。
            int pc_reader;             // "pc" 有太多可能的解释了。
            int cstmr_id;              // 有删减若干字母。

6.2. 文件命名
~~~~~~~~~~~~~~~~~~~~~~

.. tip::

    文件名要全部小写, 可以包含下划线 (``_``) 或连字符 (``-``). 按项目约定来. 如果并没有项目约定，"_" 更好。

    可接受的文件命名::

        * my_useful_class.cc
        * my-useful-class.cc
        * myusefulclass.cc
        * muusefulclass_test.cc // ``_unittest`` 和 ``_regtest`` 已弃用。

    C++ 文件要以 ``.cc`` 结尾, 头文件以 ``.h`` 结尾. 专门插入文本的文件则以 ``.inc`` 结尾，参见 :ref:`self-contained headers`。

    不要使用已经存在于 ``/usr/include`` 下的文件名 (Yang.Y 注: 即编译器搜索系统头文件的路径), 如 ``db.h``.

    通常应尽量让文件名更加明确. ``http_server_logs.h`` 就比 ``logs.h`` 要好. 定义类时文件名一般成对出现, 如 ``foo_bar.h`` 和 ``foo_bar.cc``, 对应于类 ``FooBar``.

    内联函数必须放在 ``.h`` 文件中. 如果内联函数比较短, 就直接放在 ``.h`` 中.

6.3. 类型命名
~~~~~~~~~~~~~~~~~~~~~~

.. tip::

    类型名称的每个单词首字母均大写, 不包含下划线: ``MyExcitingClass``, ``MyExcitingEnum``.

所有类型命名 —— 类, 结构体, 类型定义 (``typedef``), 枚举 —— 均使用相同约定. 例如:

    .. code-block:: c++

        // classes and structs
        class UrlTable { ...
        class UrlTableTester { ...
        struct UrlTableProperties { ...

        // typedefs
        typedef hash_map<UrlTableProperties *, string> PropertiesMap;

        // enums
        enum UrlTableErrors { ...

6.4. 变量命名
~~~~~~~~~~~~~~~~~~~~~~

.. tip::

    变量名一律小写, 单词之间用下划线连接. 类的成员变量以下划线结尾, 但结构体的就不用，如:: ``a_local_variable``, ``a_struct_data_member``, ``a_class_data_member_``.

普通变量命名:

    举例::

        string table_name;  // 可 - 用下划线。
        string tablename;   // 可 - 全小写。

    .. warning::
        .. code-block:: c++

            string tableName;   // 差 - 混合大小写。

类数据成员：

    不管是静态的还是非静态的，类数据成员都可以和普通变量一样, 但要接下划线。

        .. code-block:: c++

            class TableInfo {
              ...
             private:
              string table_name_;  // 可 - 尾后加下划线。
              string tablename_;   // 可。
              static Pool<TableInfo>* pool_;  // 可。
            };

结构体变量:

    不管是静态的还是非静态的，结构体数据成员都可以和普通变量一样, 不用像类那样接下划线:

        .. code-block:: c++

            struct UrlTableProperties {
                string name;
                int num_entries;
            }

    结构体与类的讨论参考 :ref:`结构体 vs. 类 <structs_vs_classes>` 一节.

全局变量:

    对全局变量没有特别要求, 少用就好, 但如果你要用, 可以用 ``g_`` 或其它标志作为前缀, 以便更好的区分局部变量.

.. _constant-names:

6.5. 常量命名
~~~~~~~~~~~~~~~~~~~~~~

.. tip::

    在全局或类里的常量名称前加 ``k``: kDaysInAWeek. 且除去开头的 ``k`` 之外每个单词开头字母均大写。

    所有编译时常量, 无论是局部的, 全局的还是类中的, 和其他变量稍微区别一下. ``k`` 后接大写字母开头的单词:

        .. code-block:: c++

            const int kDaysInAWeek = 7;

    这规则适用于编译时的局部作用域常量，不过要按变量规则来命名也可以。

.. _function-names:

6.6. 函数命名
~~~~~~~~~~~~~~~~~~~~~~

.. tip::

    常规函数使用大小写混合, 取值和设值函数则要求与变量名匹配: ``MyExcitingFunction()``, ``MyExcitingMethod()``, ``my_exciting_member_variable()``, ``set_my_exciting_member_variable()``.

常规函数:

    函数名的每个单词首字母大写, 没有下划线。

    如果您的某函数出错时就要直接 crash, 那么就在函数名加上 OrDie. 但这函数本身必须集成在产品代码里，且平时也可能会出错。

        .. code-block:: c++

            AddTableEntry()
            DeleteUrl()
            OpenFileOrDie()

取值和设值函数:

    取值（Accessors）和设值（Mutators）函数要与存取的变量名匹配. 这儿摘录一个类, ``num_entries_`` 是该类的实例变量:

        .. code-block:: c++

            class MyClass {
                public:
                    ...
                    int num_entries() const { return num_entries_; }
                    void set_num_entries(int num_entries) { num_entries_ = num_entries; }

                private:
                    int num_entries_;
            };

    其它非常短小的内联函数名也可以用小写字母, 例如. 如果你在循环中调用这样的函数甚至都不用缓存其返回值, 小写命名就可以接受.

6.7. 名字空间命名
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. tip::

    名字空间用小写字母命名, 并基于项目名称和目录结构: ``google_awesome_project``.

关于名字空间的讨论和如何命名, 参考 :ref:`名字空间 <namespaces>` 一节.

6.8. 枚举命名
~~~~~~~~~~~~~~~~~~~~~~

.. tip::

    枚举的命名应当和 :ref:`常量 <constant-names>` 或 :ref:`宏 <macro-names>` 一致: ``kEnumName`` 或是 ``ENUM_NAME``.

单独的枚举值应该优先采用 :ref:`常量 <constant-names>` 的命名方式. 但 :ref:`宏 <macro-names>` 方式的命名也可以接受. 枚举名 ``UrlTableErrors`` (以及 ``AlternateUrlTableErrors``) 是类型, 所以要用大小写混合的方式.
    .. code-block:: c++

        enum UrlTableErrors {
            kOK = 0,
            kErrorOutOfMemory,
            kErrorMalformedInput,
        };
        enum AlternateUrlTableErrors {
            OK = 0,
            OUT_OF_MEMORY = 1,
            MALFORMED_INPUT = 2,
        };

2009 年 1 月之前, 我们一直建议采用 :ref:`宏 <macro-names>` 的方式命名枚举值. 由于枚举值和宏之间的命名冲突, 直接导致了很多问题. 由此, 这里改为优先选择常量风格的命名方式. 新代码应该尽可能优先使用常量风格. 但是老代码没必要切换到常量风格, 除非宏风格确实会产生编译期问题.

.. _macro-names:

6.9. 宏命名
~~~~~~~~~~~~~~~~~~

.. tip::

    你并不打算 :ref:`使用宏 <preprocessor-macros>`, 对吧? 如果你一定要用, 像这样命名: ``MY_MACRO_THAT_SCARES_SMALL_CHILDREN``.

参考 :ref:`预处理宏 <preprocessor-macros>`; 通常 *不应该* 使用宏. 如果不得不用, 其命名像枚举命名一样全部大写, 使用下划线::

    #define ROUND(x) ...
    #define PI_ROUNDED 3.0

6.10. 命名规则的特例
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. tip::

    如果你命名的实体与已有 C/C++ 实体相似, 可参考现有命名策略.

``bigopen()``:

    函数名, 参照 ``open()`` 的形式

``uint``:

    ``typedef``

``bigpos``:

    ``struct`` 或 ``class``, 参照 ``pos`` 的形式

``sparse_hash_map``:

    STL 相似实体; 参照 STL 命名约定

``LONGLONG_MAX``:

    常量, 如同 ``INT_MAX``

译者（acgtyrant）笔记
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#. 感觉 Google 的命名约定很高明，比如写了简单的类 QueryResult, 接着又可以直接定义一个变量 query_result, 区分度很好；再次，类内变量以下划线结尾，那么就可以直接传入同名的形参，比如 ``TextQuery::TextQuery(std::string word) : word_(word) {}`` , 其中 ``word_`` 自然是类内私有成员。
