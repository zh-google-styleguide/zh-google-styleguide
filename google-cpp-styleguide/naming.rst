6. 命名约定
------------

最重要的一致性规则是命名管理. 命名风格快速获知名字代表是什么东东: 类型? 变量? 函数? 常量? 宏 ... ? 甚至不需要去查找类型声明. 我们大脑中的模式匹配引擎可以非常可靠的处理这些命名规则.

命名规则具有一定随意性, 但相比按个人喜好命名, 一致性更重, 所以不管你怎么想, 规则总归是规则.

6.1. 通用命名规则
~~~~~~~~~~~~~~~~~~~~

.. tip::
    函数命名, 变量命名, 文件命名应具备描述性; 不要过度缩写. 类型和变量应该是名词, 函数名可以用 "命令性" 动词.
    
如何命名:
    尽可能给出描述性的名称. 不要节约行空间, 让别人很快理解你的代码更重要. 好的命名风格:
        .. code-block:: c++
            
            int num_errors;                  // Good.
            int num_completed_connections;   // Good.
        
    糟糕的命名使用含糊的缩写或随意的字符:
        .. code-block:: c++
            
            int n;                           // Bad - meaningless.
            int nerr;                        // Bad - ambiguous abbreviation.
            int n_comp_conns;                // Bad - ambiguous abbreviation.
    
    类型和变量名一般为名词: 如 ``FileOpener``, ``num_errors``.
    
    函数名通常是指令性的 (确切的说它们应该是命令), 如 ``OpenFile()``, ``set_num_errors()``. 取值函数是个特例 (在 :ref:`函数命名 <function-names>` 处详细阐述), 函数名和它要取值的变量同名.
    
缩写:
    除非该缩写在其它地方都非常普遍, 否则不要使用. 例如:
        .. code-block:: c++
        
            // Good
            // These show proper names with no abbreviations.
            int num_dns_connections;  // 大部分人都知道 "DNS" 是啥意思.
            int price_count_reader;   // OK, price count. 有意义.
        
        .. warning::
            .. code-block:: c++
                
                // Bad!
                // Abbreviations can be confusing or ambiguous outside a small group.
                int wgc_connections;  // Only your group knows what this stands for.
                int pc_reader;        // Lots of things can be abbreviated "pc".
        
    永远不要用省略字母的缩写:
        .. code-block:: c++
            
            int error_count;  // Good.
            int error_cnt;    // Bad.
        
        
6.2. 文件命名
~~~~~~~~~~~~~~~~~~~~

.. tip::
    文件名要全部小写, 可以包含下划线 (``_``) 或连字符 (``-``). 按项目约定来.

可接受的文件命名::
    
    my_useful_class.cc
    my-useful-class.cc
    myusefulclass.cc

C++ 文件要以 ``.cc`` 结尾, 头文件以 ``.h`` 结尾.

不要使用已经存在于 ``/usr/include`` 下的文件名 (yospaly 注: 即编译器搜索系统头文件的路径), 如 ``db.h``.

通常应尽量让文件名更加明确. ``http_server_logs.h`` 就比 ``logs.h`` 要好. 定义类时文件名一般成对出现, 如 ``foo_bar.h`` 和 ``foo_bar.cc``, 对应于类 ``FooBar``.

内联函数必须放在 ``.h`` 文件中. 如果内联函数比较短, 就直接放在 ``.h`` 中. 如果代码比较长, 可以放到以 ``-inl.h`` 结尾的文件中. 对于包含大量内联代码的类, 可以使用三个文件::
    
    url_table.h      // The class declaration.
    url_table.cc     // The class definition.
    url_table-inl.h  // Inline functions that include lots of code.
    
参考 :ref:`-inl.h 文件 <inl-files>` 一节.

6.3. 类型命名
~~~~~~~~~~~~~~~~~~~~

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
~~~~~~~~~~~~~~~~~~~~

.. tip::
    变量名一律小写, 单词之间用下划线连接. 类的成员变量以下划线结尾, 如::
        
        my_exciting_local_variable
        my_exciting_member_variable_

普通变量命名:
    举例::
        
        string table_name;  // OK - uses underscore.
        string tablename;   // OK - all lowercase.
    
    .. warning::
        .. code-block:: c++
            
            string tableName;   // Bad - mixed case.
    
结构体变量:
    结构体的数据成员可以和普通变量一样, 不用像类那样接下划线:
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
~~~~~~~~~~~~~~~~~~~~

.. tip::
    在名称前加 ``k``: kDaysInAWeek.
    
所有编译时常量, 无论是局部的, 全局的还是类中的, 和其他变量稍微区别一下. ``k`` 后接大写字母开头的单词::
    const int kDaysInAWeek = 7;


.. _function-names:

6.6. 函数命名
~~~~~~~~~~~~~~~~~~~~

.. tip::
    常规函数使用大小写混合, 取值和设值函数则要求与变量名匹配: ``MyExcitingFunction()``, ``MyExcitingMethod()``, ``my_exciting_member_variable()``, ``set_my_exciting_member_variable()``.
    
常规函数:
    函数名的每个单词首字母大写, 没有下划线::
        
        AddTableEntry()
        DeleteUrl()

取值和设值函数:
    取值和设值函数要与存取的变量名匹配. 这儿摘录一个类, ``num_entries_`` 是该类的实例变量:
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
~~~~~~~~~~~~~~~~~~~~

.. tip::
    名字空间用小写字母命名, 并基于项目名称和目录结构: ``google_awesome_project``.
    
关于名字空间的讨论和如何命名, 参考 :ref:`名字空间 <namespaces>` 一节.

6.8. 枚举命名
~~~~~~~~~~~~~~~~~~~~

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
~~~~~~~~~~~~~~~~~~~~

.. tip::
    你并不打算 :ref:`使用宏 <preprocessor-macros>`, 对吧? 如果你一定要用, 像这样命名: ``MY_MACRO_THAT_SCARES_SMALL_CHILDREN``.

参考 `预处理宏 <preprocessor-macros>`; 通常 *不应该* 使用宏. 如果不得不用, 其命名像枚举命名一样全部大写, 使用下划线::
    
    #define ROUND(x) ...
    #define PI_ROUNDED 3.0

    
6.10. 命名规则的特例
~~~~~~~~~~~~~~~~~~~~~

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

