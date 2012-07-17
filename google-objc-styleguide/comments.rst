注释
=======

虽然写起来很痛苦，但注释是保证代码可读性的关键。下面的规则给出了你应该什么时候、在哪进行注释。记住：尽管注释很重要，但最好的代码应该自成文档。与其给类型及变量起一个晦涩难懂的名字，再为它写注释，不如直接起一个有意义的名字。

当你写注释的时候，记得你是在给你的听众写，即下一个需要阅读你所写代码的贡献者。大方一点，下一个读代码的人可能就是你！

记住所有 C++ 风格指南里的规则在这里也同样适用，不同的之处后续会逐步指出。

文件注释
~~~~~~~~~~

.. tip::

    每个文件的开头以文件内容的简要描述起始，紧接着是作者，最后是版权声明和/或许可证样板。

版权信息及作者
^^^^^^^^^^^^^^^^^^

每个文件应该按顺序包括如下项：

* 文件内容的简要描述
* 代码作者
* 版权信息声明（如：``Copyright 2008 Google Inc.``）
* 必要的话，加上许可证样板。为项目选择一个合适的授权样板（例如，``Apache 2.0, BSD, LGPL, GPL``）。

如果你对其他人的原始代码作出重大的修改，请把你自己的名字添加到作者里面。当另外一个代码贡献者对文件有问题时，他需要知道怎么联系你，这十分有用。

声明部分的注释
~~~~~~~~~~~~~~~~

.. tip::

    每个接口、类别以及协议应辅以注释，以描述它的目的及与整个项目的关系。

.. code-block:: objc

    // A delegate for NSApplication to handle notifications about app
    // launch and shutdown. Owned by the main app controller.
    @interface MyAppDelegate : NSObject {
      ...
    }
    @end

如果你已经在文件头部详细描述了接口，可以直接说明 “完整的描述请参见文件头部”，但是一定要有这部分注释。

另外，公共接口的每个方法，都应该有注释来解释它的作用、参数、返回值以及其它影响。

为类的线程安全性作注释，如果有的话。如果类的实例可以被多个线程访问，记得注释多线程条件下的使用规则。

实现部分的注释
~~~~~~~~~~~~~~~~

.. tip::

    使用 ``|`` 来引用注释中的变量名及符号名而不是使用引号。

这会避免二义性，尤其是当符号是一个常用词汇，这使用语句读起来很糟糕。例如，对于符号 ``count`` ：

.. code-block:: objc

    // Sometimes we need |count| to be less than zero.

或者当引用已经包含引号的符号：

.. code-block:: objc

    // Remember to call |StringWithoutSpaces("foo bar baz")|



对象所有权
~~~~~~~~~~~~~~~~

.. tip::

    当与 Objective-C 最常规的作法不同时，尽量使指针的所有权模型尽量明确。

继承自 ``NSObject`` 的对象的实例变量指针，通常被假定是强引用关系（retained），某些情况下也可以注释为弱引用（weak）或使用 ``__weak`` 生命周期限定符。同样，声明的属性如果没有被类 ``retained``，必须指定是弱引用或赋予 ``@property`` 属性。然而，Mac 软件中标记上 ``IBOutlets`` 的实例变量，被认为是不会被类 ``retained`` 的。

当实例变量指向 ``CoreFoundation``、C++ 或者其它非 Objective-C 对象时，不论指针是否会被 ``retained``，都需要使用 ``__strong`` 和 ``__weak`` 类型修饰符明确指明。``CoreFoundation`` 和其它非 Objective-C 对象指针需要显式的内存管理，即便使用了自动引用计数或垃圾回收机制。当不允许使用 ``__weak`` 类型修饰符（比如，使用 clang 编译时的 C++ 成员变量），应使用注释替代说明。

注意：Objective-C 对象中的 C++ 对象的自动封装，缺省是不允许的，参见 `这里 <http://chanson.livejournal.com/154253.html>`_ 的说明。

强引用及弱引用声明的例子：

.. code-block:: objc

    @interface MyDelegate : NSObject {
     @private
      IBOutlet NSButton *okButton_;  // normal NSControl; implicitly weak on Mac only

      AnObjcObject* doohickey_;  // my doohickey
      __weak MyObjcParent *parent_;  // so we can send msgs back (owns me)

      // non-NSObject pointers...
      __strong CWackyCPPClass *wacky_;  // some cross-platform object
      __strong CFDictionaryRef *dict_;
    }
    @property(strong, nonatomic) NSString *doohickey;
    @property(weak, nonatomic) NSString *parent;
    @end

（译注：强引用 - 对象被类 ``retained``。弱引用 - 对象没有被类 ``retained``，如委托）
