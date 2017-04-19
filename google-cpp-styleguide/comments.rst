8. 注释
------------

注释虽然写起来很痛苦, 但对保证代码可读性至关重要. 下面的规则描述了如何注释以及在哪儿注释. 当然也要记住: 注释固然很重要, 但最好的代码应当本身就是文档. 有意义的类型名和变量名, 要远胜过要用注释解释的含糊不清的名字.

你写的注释是给代码读者看的, 也就是下一个需要理解你的代码的人. 所以慷慨些吧, 下一个读者可能就是你!

8.1. 注释风格
~~~~~~~~~~~~~~~~~~~~~~

**总述**

使用 ``//`` 或 ``/* */``, 统一就好.

**说明**

``//`` 或 ``/* */`` 都可以; 但 ``//`` *更* 常用. 要在如何注释及注释风格上确保统一.

8.2. 文件注释
~~~~~~~~~~~~~~~~~~~~~~

**总述**

在每一个文件开头加入版权公告.

文件注释描述了该文件的内容. 如果一个文件只声明, 或实现, 或测试了一个对象, 并且这个对象已经在它的声明处进行了详细的注释, 那么就没必要再加上文件注释. 除此之外的其他文件都需要文件注释.

**说明**

法律公告和作者信息
=============================

每个文件都应该包含许可证引用. 为项目选择合适的许可证版本.(比如, Apache 2.0, BSD, LGPL, GPL)

如果你对原始作者的文件做了重大修改, 请考虑删除原作者信息.

文件内容
=============================

如果一个 ``.h`` 文件声明了多个概念, 则文件注释应当对文件的内容做一个大致的说明, 同时说明各概念之间的联系. 一个一到两行的文件注释就足够了, 对于每个概念的详细文档应当放在各个概念中, 而不是文件注释中.

不要在 ``.h`` 和 ``.cc`` 之间复制注释, 这样的注释偏离了注释的实际意义.

.. _class-comments:

8.3. 类注释
~~~~~~~~~~~~~~~~~~

**总述**

每个类的定义都要附带一份注释, 描述类的功能和用法, 除非它的功能相当明显.

.. code-block:: c++

    // Iterates over the contents of a GargantuanTable.
    // Example:
    //    GargantuanTableIterator* iter = table->NewIterator();
    //    for (iter->Seek("foo"); !iter->done(); iter->Next()) {
    //      process(iter->key(), iter->value());
    //    }
    //    delete iter;
    class GargantuanTableIterator {
      ...
    };

**说明**

类注释应当为读者理解如何使用与何时使用类提供足够的信息, 同时应当提醒读者在正确使用此类时应当考虑的因素. 如果类有任何同步前提, 请用文档说明. 如果该类的实例可被多线程访问, 要特别注意文档说明多线程环境下相关的规则和常量使用.

如果你想用一小段代码演示这个类的基本用法或通常用法, 放在类注释里也非常合适.

如果类的声明和定义分开了(例如分别放在了 ``.h`` 和 ``.cc`` 文件中), 此时, 描述类用法的注释应当和接口定义放在一起, 描述类的操作和实现的注释应当和实现放在一起.

8.4. 函数注释
~~~~~~~~~~~~~~~~~~~~~~

**总述**

函数声明处的注释描述函数功能; 定义处的注释描述函数实现.

**说明**

函数声明
=============================

基本上每个函数声明处前都应当加上注释, 描述函数的功能和用途. 只有在函数的功能简单而明显时才能省略这些注释(例如, 简单的取值和设值函数). 注释使用叙述式 ("Opens the file") 而非指令式 ("Open the file"); 注释只是为了描述函数, 而不是命令函数做什么. 通常, 注释不会描述函数如何工作. 那是函数定义部分的事情.

函数声明处注释的内容:

- 函数的输入输出.

- 对类成员函数而言: 函数调用期间对象是否需要保持引用参数, 是否会释放这些参数.

- 函数是否分配了必须由调用者释放的空间.

- 参数是否可以为空指针.

- 是否存在函数使用上的性能隐患.

- 如果函数是可重入的, 其同步前提是什么?

举例如下:

.. code-block:: c++

    // Returns an iterator for this table.  It is the client's
    // responsibility to delete the iterator when it is done with it,
    // and it must not use the iterator once the GargantuanTable object
    // on which the iterator was created has been deleted.
    //
    // The iterator is initially positioned at the beginning of the table.
    //
    // This method is equivalent to:
    //    Iterator* iter = table->NewIterator();
    //    iter->Seek("");
    //    return iter;
    // If you are going to immediately seek to another place in the
    // returned iterator, it will be faster to use NewIterator()
    // and avoid the extra seek.
    Iterator* GetIterator() const;

但也要避免罗罗嗦嗦, 或者对显而易见的内容进行说明. 下面的注释就没有必要加上 "否则返回 false", 因为已经暗含其中了:

.. code-block:: c++

    // Returns true if the table cannot hold any more entries.
    bool IsTableFull();

注释函数重载时, 注释的重点应该是函数中被重载的部分, 而不是简单的重复被重载的函数的注释. 多数情况下, 函数重载不需要额外的文档, 因此也没有必要加上注释.

注释构造/析构函数时, 切记读代码的人知道构造/析构函数的功能, 所以 "销毁这一对象" 这样的注释是没有意义的. 你应当注明的是注明构造函数对参数做了什么 (例如, 是否取得指针所有权) 以及析构函数清理了什么. 如果都是些无关紧要的内容, 直接省掉注释. 析构函数前没有注释是很正常的.

函数定义
=============================

如果函数的实现过程中用到了很巧妙的方式, 那么在函数定义处应当加上解释性的注释. 例如, 你所使用的编程技巧, 实现的大致步骤, 或解释如此实现的理由. 举个例子, 你可以说明为什么函数的前半部分要加锁而后半部分不需要.

*不要* 从 ``.h`` 文件或其他地方的函数声明处直接复制注释. 简要重述函数功能是可以的, 但注释重点要放在如何实现上.

8.5. 变量注释
~~~~~~~~~~~~~~~~~~~~~~

**总述**

通常变量名本身足以很好说明变量用途. 某些情况下, 也需要额外的注释说明.

**说明**

类数据成员
=============================

每个类数据成员 (也叫实例变量或成员变量) 都应该用注释说明用途. 如果有非变量的参数(例如特殊值, 数据成员之间的关系, 生命周期等)不能够用类型与变量名明确表达, 则应当加上注释. 然而, 如果变量类型与变量名已经足以描述一个变量, 那么就不再需要加上注释.

特别地, 如果变量可以接受 ``NULL`` 或 ``-1`` 等警戒值, 须加以说明. 比如:

.. code-block:: c++

    private:
     // Used to bounds-check table accesses. -1 means
     // that we don't yet know how many entries the table has.
     int num_total_entries_;


全局变量
=============================

和数据成员一样, 所有全局变量也要注释说明含义及用途, 以及作为全局变量的原因. 比如:

.. code-block:: c++

    // The total number of tests cases that we run through in this regression test.
    const int kNumTestCases = 6;

8.6. 实现注释
~~~~~~~~~~~~~~~~~~~~~~

**总述**

对于代码中巧妙的, 晦涩的, 有趣的, 重要的地方加以注释.

**说明**

代码前注释
=============================

巧妙或复杂的代码段前要加注释. 比如:

.. code-block:: c++

    // Divide result by two, taking into account that x
    // contains the carry from the add.
    for (int i = 0; i < result->size(); i++) {
      x = (x << 8) + (*result)[i];
      (*result)[i] = x >> 1;
      x &= 1;
    }

行注释
=============================

比较隐晦的地方要在行尾加入注释. 在行尾空两格进行注释. 比如:

.. code-block:: c++

    // If we have enough memory, mmap the data portion too.
    mmap_budget = max<int64>(0, mmap_budget - index_->length());
    if (mmap_budget >= data_size_ && !MmapData(mmap_chunk_bytes, mlock))
      return;  // Error already logged.

注意, 这里用了两段注释分别描述这段代码的作用, 和提示函数返回时错误已经被记入日志.

如果你需要连续进行多行注释, 可以使之对齐获得更好的可读性:

.. code-block:: c++

    DoSomething();                  // Comment here so the comments line up.
    DoSomethingElseThatIsLonger();  // Two spaces between the code and the comment.
    { // One space before comment when opening a new scope is allowed,
      // thus the comment lines up with the following comments and code.
      DoSomethingElse();  // Two spaces before line comments normally.
    }
    std::vector<string> list{
                        // Comments in braced lists describe the next element...
                        "First item",
                        // .. and should be aligned appropriately.
    "Second item"};
    DoSomething(); /* For trailing block comments, one space is fine. */

函数参数注释
=============================

如果函数参数的意义不明显, 考虑用下面的方式进行弥补:

- 如果参数是一个字面常量, 并且这一常量在多处函数调用中被使用, 用以推断它们一致, 你应当用一个常量名让这一约定变得更明显, 并且保证这一约定不会被打破.

- 考虑更改函数的签名, 让某个 ``bool`` 类型的参数变为 ``enum`` 类型, 这样可以让这个参数的值表达其意义.

- 如果某个函数有多个配置选项, 你可以考虑定义一个类或结构体以保存所有的选项, 并传入类或结构体的实例. 这样的方法有许多优点, 例如这样的选项可以在调用处用变量名引用, 这样就能清晰地表明其意义. 同时也减少了函数参数的数量, 使得函数调用更易读也易写. 除此之外, 以这样的方式, 如果你使用其他的选项, 就无需对调用点进行更改.

- 用具名变量代替大段而复杂的嵌套表达式.

- 万不得已时, 才考虑在调用点用注释阐明参数的意义.

比如下面的示例的对比:

.. code-block:: c++

    // What are these arguments?
    const DecimalNumber product = CalculateProduct(values, 7, false, nullptr);

和

.. code-block:: c++

    ProductOptions options;
    options.set_precision_decimals(7);
    options.set_use_cache(ProductOptions::kDontUseCache);
    const DecimalNumber product =
        CalculateProduct(values, options, /*completion_callback=*/nullptr);

哪个更清晰一目了然.

不允许的行为
=============================

不要描述显而易见的现象, *永远不要* 用自然语言翻译代码作为注释, 除非即使对深入理解 C++ 的读者来说代码的行为都是不明显的. 要假设读代码的人 C++ 水平比你高, 即便他/她可能不知道你的用意:

你所提供的注释应当解释代码 *为什么* 要这么做和代码的目的, 或者最好是让代码自文档化.

比较这样的注释:

.. code-block:: c++

    // Find the element in the vector.  <-- 差: 这太明显了!
    auto iter = std::find(v.begin(), v.end(), element);
    if (iter != v.end()) {
      Process(element);
    }

和这样的注释:

.. code-block:: c++

    // Process "element" unless it was already processed.
    auto iter = std::find(v.begin(), v.end(), element);
    if (iter != v.end()) {
      Process(element);
    }

自文档化的代码根本就不需要注释. 上面例子中的注释对下面的代码来说就是毫无必要的:

.. code-block:: c++

    if (!IsAlreadyProcessed(element)) {
      Process(element);
    }

8.8. 标点, 拼写和语法
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**总述**

注意标点, 拼写和语法; 写的好的注释比差的要易读的多.

**说明**

注释的通常写法是包含正确大小写和结尾句号的完整叙述性语句. 大多数情况下, 完整的句子比句子片段可读性更高. 短一点的注释, 比如代码行尾注释, 可以随意点, 但依然要注意风格的一致性.

虽然被别人指出该用分号时却用了逗号多少有些尴尬, 但清晰易读的代码还是很重要的. 正确的标点, 拼写和语法对此会有很大帮助.

8.8. TODO 注释
~~~~~~~~~~~~~~~~~~~~~~~~~~

**总述**

对那些临时的, 短期的解决方案, 或已经够好但仍不完美的代码使用 ``TODO`` 注释.

``TODO`` 注释要使用全大写的字符串 ``TODO``, 在随后的圆括号里写上你的名字, 邮件地址, bug ID, 或其它身份标识和与这一 ``TODO`` 相关的 issue. 主要目的是让添加注释的人 (也是可以请求提供更多细节的人) 可根据规范的 ``TODO`` 格式进行查找. 添加 ``TODO`` 注释并不意味着你要自己来修正, 因此当你加上带有姓名的 ``TODO`` 时, 一般都是写上自己的名字.

.. code-block:: c++

    // TODO(kl@gmail.com): Use a "*" here for concatenation operator.
    // TODO(Zeke) change this to use relations.
    // TODO(bug 12345): remove the "Last visitors" feature

如果加 ``TODO`` 是为了在 "将来某一天做某事", 可以附上一个非常明确的时间 "Fix by November 2005"), 或者一个明确的事项 ("Remove this code when all clients can handle XML responses.").

8.9. 弃用注释
~~~~~~~~~~~~~~~~~~~~~~

**总述**

通过弃用注释（``DEPRECATED`` comments）以标记某接口点已弃用. 

您可以写上包含全大写的 ``DEPRECATED`` 的注释, 以标记某接口为弃用状态. 注释可以放在接口声明前, 或者同一行. 

在 ``DEPRECATED`` 一词后, 在括号中留下您的名字, 邮箱地址以及其他身份标识.

弃用注释应当包涵简短而清晰的指引, 以帮助其他人修复其调用点. 在 C++ 中, 你可以将一个弃用函数改造成一个内联函数, 这一函数将调用新的接口.

仅仅标记接口为 ``DEPRECATED`` 并不会让大家不约而同地弃用, 您还得亲自主动修正调用点（callsites）, 或是找个帮手. 

修正好的代码应该不会再涉及弃用接口点了, 着实改用新接口点. 如果您不知从何下手, 可以找标记弃用注释的当事人一起商量. 

译者 (YuleFox) 笔记
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#. 关于注释风格, 很多 C++ 的 coders 更喜欢行注释, C coders 或许对块注释依然情有独钟, 或者在文件头大段大段的注释时使用块注释;
#. 文件注释可以炫耀你的成就, 也是为了捅了篓子别人可以找你;
#. 注释要言简意赅, 不要拖沓冗余, 复杂的东西简单化和简单的东西复杂化都是要被鄙视的;
#. 对于 Chinese coders 来说, 用英文注释还是用中文注释, it is a problem, 但不管怎样, 注释是为了让别人看懂, 难道是为了炫耀编程语言之外的你的母语或外语水平吗；
#. 注释不要太乱, 适当的缩进才会让人乐意看. 但也没有必要规定注释从第几列开始 (我自己写代码的时候总喜欢这样), UNIX/LINUX 下还可以约定是使用 tab 还是 space, 个人倾向于 space;
#. TODO 很不错, 有时候, 注释确实是为了标记一些未完成的或完成的不尽如人意的地方, 这样一搜索, 就知道还有哪些活要干, 日志都省了.
