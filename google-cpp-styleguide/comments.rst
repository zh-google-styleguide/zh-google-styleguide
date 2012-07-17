7. 注释
------------

注释虽然写起来很痛苦, 但对保证代码可读性至关重要. 下面的规则描述了如何注释以及在哪儿注释. 当然也要记住: 注释固然很重要, 但最好的代码本身应该是自文档化. 有意义的类型名和变量名, 要远胜过要用注释解释的含糊不清的名字.

你写的注释是给代码读者看的: 下一个需要理解你的代码的人. 慷慨些吧, 下一个人可能就是你!

7.1. 注释风格
~~~~~~~~~~~~~~~~~~~~

.. tip::
    使用 ``//`` 或 ``/* */``, 统一就好.

``//`` 或 ``/* */`` 都可以; 但 ``//`` *更* 常用. 要在如何注释及注释风格上确保统一.

7.2. 文件注释
~~~~~~~~~~~~~~~~~~~~

.. tip::
    在每一个文件开头加入版权公告, 然后是文件内容描述.
    
法律公告和作者信息:
    每个文件都应该包含以下项, 依次是:
    
        - 版权声明 (比如, ``Copyright 2008 Google Inc.``)
        
        - 许可证. 为项目选择合适的许可证版本 (比如, Apache 2.0, BSD, LGPL, GPL)
        
        - 作者: 标识文件的原始作者.
    
    如果你对原始作者的文件做了重大修改, 将你的信息添加到作者信息里. 这样当其他人对该文件有疑问时可以知道该联系谁.

文件内容:
    紧接着版权许可和作者信息之后, 每个文件都要用注释描述文件内容.
    
    通常, ``.h`` 文件要对所声明的类的功能和用法作简单说明. ``.cc`` 文件通常包含了更多的实现细节或算法技巧讨论,  如果你感觉这些实现细节或算法技巧讨论对于理解 ``.h`` 文件有帮助, 可以该注释挪到 ``.h``, 并在 ``.cc`` 中指出文档在 ``.h``.
    
    不要简单的在 ``.h`` 和 ``.cc`` 间复制注释. 这种偏离了注释的实际意义.

.. _class-comments:

7.3. 类注释
~~~~~~~~~~~~~~~~~~~~

.. tip::
    每个类的定义都要附带一份注释, 描述类的功能和用法.

.. code-block:: c++
    
    // Iterates over the contents of a GargantuanTable.  Sample usage:
    //    GargantuanTable_Iterator* iter = table->NewIterator();
    //    for (iter->Seek("foo"); !iter->done(); iter->Next()) {
    //      process(iter->key(), iter->value());
    //    }
    //    delete iter;
    class GargantuanTable_Iterator {
        ...
    };
    
如果你觉得已经在文件顶部详细描述了该类, 想直接简单的来上一句 "完整描述见文件顶部" 也不打紧, 但务必确保有这类注释.

如果类有任何同步前提, 文档说明之. 如果该类的实例可被多线程访问, 要特别注意文档说明多线程环境下相关的规则和常量使用.

7.4. 函数注释
~~~~~~~~~~~~~~~~~~~~

.. tip::
    函数声明处注释描述函数功能; 定义处描述函数实现.
    
函数声明:
    注释位于声明之前, 对函数功能及用法进行描述. 注释使用叙述式 ("Opens the file") 而非指令式 ("Open the file"); 注释只是为了描述函数, 而不是命令函数做什么. 通常, 注释不会描述函数如何工作. 那是函数定义部分的事情.
    
    函数声明处注释的内容:
    
        - 函数的输入输出.
        - 对类成员函数而言: 函数调用期间对象是否需要保持引用参数, 是否会释放这些参数.
        - 如果函数分配了空间, 需要由调用者释放.
        - 参数是否可以为 ``NULL``.
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
        
    但也要避免罗罗嗦嗦, 或做些显而易见的说明. 下面的注释就没有必要加上 "returns false otherwise", 因为已经暗含其中了:
    
        .. code-block:: c++
        
            // Returns true if the table cannot hold any more entries.
            bool IsTableFull();
        
    注释构造/析构函数时, 切记读代码的人知道构造/析构函数是干啥的, 所以 "destroys this object" 这样的注释是没有意义的. 注明构造函数对参数做了什么 (例如, 是否取得指针所有权) 以及析构函数清理了什么. 如果都是些无关紧要的内容, 直接省掉注释. 析构函数前没有注释是很正常的.

函数定义:
    每个函数定义时要用注释说明函数功能和实现要点. 比如说说你用的编程技巧, 实现的大致步骤, 或解释如此实现的理由, 为什么前半部分要加锁而后半部分不需要.
    
    *不要* 从 ``.h`` 文件或其他地方的函数声明处直接复制注释. 简要重述函数功能是可以的, 但注释重点要放在如何实现上.
    
7.5. 变量注释
~~~~~~~~~~~~~~~~~~~~

.. tip::
    通常变量名本身足以很好说明变量用途. 某些情况下, 也需要额外的注释说明.

类数据成员:
    每个类数据成员 (也叫实例变量或成员变量) 都应该用注释说明用途. 如果变量可以接受 ``NULL`` 或 ``-1`` 等警戒值, 须加以说明. 比如:
    
        .. code-block:: c++
            
            private:
                // Keeps track of the total number of entries in the table.
                // Used to ensure we do not go over the limit. -1 means
                // that we don't yet know how many entries the table has.
                int num_total_entries_;


全局变量:
    和数据成员一样, 所有全局变量也要注释说明含义及用途. 比如:
    
        .. code-block:: c++
            
            // The total number of tests cases that we run through in this regression test.
            const int kNumTestCases = 6;


7.6. 实现注释
~~~~~~~~~~~~~~~~~~~~

.. tip::
    对于代码中巧妙的, 晦涩的, 有趣的, 重要的地方加以注释.
    
代码前注释:
    巧妙或复杂的代码段前要加注释. 比如:
    
        .. code-block:: c++
            
            // Divide result by two, taking into account that x
            // contains the carry from the add.
            for (int i = 0; i < result->size(); i++) {
                x = (x << 8) + (*result)[i];
                (*result)[i] = x >> 1;
                x &= 1;
            }

行注释:
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
            DoSomethingElseThatIsLonger();  // Comment here so there are two spaces between
                                            // the code and the comment.
            { // One space before comment when opening a new scope is allowed,
              // thus the comment lines up with the following comments and code.
              DoSomethingElse();  // Two spaces before line comments normally.
            }

NULL, true/false, 1, 2, 3...:
    向函数传入 ``NULL``, 布尔值或整数时, 要注释说明含义, 或使用常量让代码望文知意. 例如, 对比:
        
        .. warning::
            .. code-block:: c++
            
                bool success = CalculateSomething(interesting_value,
                                                  10,
                                                  false,
                                                  NULL);  // What are these arguments??
    
    
    和:
    
        .. code-block:: c++
            
            bool success = CalculateSomething(interesting_value,
                                              10,     // Default base value.
                                              false,  // Not the first time we're calling this.
                                              NULL);  // No callback.
    
    
    或使用常量或描述性变量:
    
        .. code-block:: c++
            
            const int kDefaultBaseValue = 10;
            const bool kFirstTimeCalling = false;
            Callback *null_callback = NULL;
            bool success = CalculateSomething(interesting_value,
                                              kDefaultBaseValue,
                                              kFirstTimeCalling,
                                              null_callback);

不允许:
    注意 *永远不要* 用自然语言翻译代码作为注释. 要假设读代码的人 C++ 水平比你高, 即便他/她可能不知道你的用意:
    
    .. warning::
        .. code-block:: c++
            
            // 现在, 检查 b 数组并确保 i 是否存在,
            // 下一个元素是 i+1.
            ...        // 天哪. 令人崩溃的注释.
    
7.7. 标点, 拼写和语法
~~~~~~~~~~~~~~~~~~~~~~~~

.. tip::
    注意标点, 拼写和语法; 写的好的注释比差的要易读的多.
    
注释的通常写法是包含正确大小写和结尾句号的完整语句. 短一点的注释 (如代码行尾注释) 可以随意点, 依然要注意风格的一致性. 完整的语句可读性更好, 也可以说明该注释是完整的, 而不是一些不成熟的想法.

虽然被别人指出该用分号时却用了逗号多少有些尴尬, 但清晰易读的代码还是很重要的. 正确的标点, 拼写和语法对此会有所帮助.

7.8. TODO 注释
~~~~~~~~~~~~~~~~~~~~~~~~

.. tip::
    对那些临时的, 短期的解决方案, 或已经够好但仍不完美的代码使用 ``TODO`` 注释.
    
``TODO`` 注释要使用全大写的字符串 ``TODO``, 在随后的圆括号里写上你的大名, 邮件地址, 或其它身份标识. 冒号是可选的. 主要目的是让添加注释的人 (也是可以请求提供更多细节的人) 可根据规范的 ``TODO`` 格式进行查找. 添加 ``TODO`` 注释并不意味着你要自己来修正.
    
    .. code-block:: c++
    
        // TODO(kl@gmail.com): Use a "*" here for concatenation operator.
        // TODO(Zeke) change this to use relations.
        
如果加 ``TODO`` 是为了在 "将来某一天做某事", 可以附上一个非常明确的时间 "Fix by November 2005"), 或者一个明确的事项 ("Remove this code when all clients can handle XML responses.").

译者 (YuleFox) 笔记
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. 关于注释风格，很多 C++ 的 coders 更喜欢行注释, C coders 或许对块注释依然情有独钟, 或者在文件头大段大段的注释时使用块注释;
2. 文件注释可以炫耀你的成就, 也是为了捅了篓子别人可以找你;
3. 注释要言简意赅, 不要拖沓冗余, 复杂的东西简单化和简单的东西复杂化都是要被鄙视的;
4. 对于 Chinese coders 来说, 用英文注释还是用中文注释, it is a problem, 但不管怎样, 注释是为了让别人看懂, 难道是为了炫耀编程语言之外的你的母语或外语水平吗；
5. 注释不要太乱, 适当的缩进才会让人乐意看. 但也没有必要规定注释从第几列开始 (我自己写代码的时候总喜欢这样), UNIX/LINUX 下还可以约定是使用 tab 还是 space, 个人倾向于 space;
6. TODO 很不错, 有时候, 注释确实是为了标记一些未完成的或完成的不尽如人意的地方, 这样一搜索, 就知道还有哪些活要干, 日志都省了.
