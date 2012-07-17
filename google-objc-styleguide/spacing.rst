留白和格式
==========

空格 vs. 制表符
~~~~~~~~~~~~~~~~~

.. tip::

    只使用空格，且一次缩进两个空格。

我们使用空格缩进。不要在代码中使用制表符。你应该将编辑器设置成自动将制表符替换成空格。

行宽
~~~~~~~

.. tip::

尽量让你的代码保持在 80 列之内。

我们深知 Objective-C 是一门繁冗的语言，在某些情况下略超 80 列可能有助于提高可读性，但这也只能是特例而已，不能成为开脱。

如果阅读代码的人认为把把某行行宽保持在 80 列仍然有不失可读性，你应该按他们说的去做。

我们意识到这条规则是有争议的，但很多已经存在的代码坚持了本规则，我们觉得保证一致性更重要。

通过设置 *Xcode > Preferences > Text Editing > Show page guide*，来使越界更容易被发现。

方法声明和定义
~~~~~~~~~~~~~~

.. tip::

    - / + 和返回类型之间须使用一个空格，参数列表中只有参数之间可以有空格。

方法应该像这样：

.. code-block:: objc

    - (void)doSomethingWithString:(NSString *)theString {
      ...
    }

星号前的空格是可选的。当写新的代码时，要与先前代码保持一致。

如果一行有非常多的参数，更好的方式是将每个参数单独拆成一行。如果使用多行，将每个参数前的冒号对齐。

.. code-block:: objc

    - (void)doSomethingWith:(GTMFoo *)theFoo
                       rect:(NSRect)theRect
                   interval:(float)theInterval {
      ...
    }

当第一个关键字比其它的短时，保证下一行至少有 4 个空格的缩进。这样可以使关键字垂直对齐，而不是使用冒号对齐：

.. code-block:: objc

    - (void)short:(GTMFoo *)theFoo
        longKeyword:(NSRect)theRect
        evenLongerKeyword:(float)theInterval {
      ...
    }


方法调用
~~~~~~~~~~~~~~

.. tip::

    方法调用应尽量保持与方法声明的格式一致。当格式的风格有多种选择时，新的代码要与已有代码保持一致。

调用时所有参数应该在同一行：

.. code-block:: objc

    [myObject doFooWith:arg1 name:arg2 error:arg3];

或者每行一个参数，以冒号对齐：

.. code-block:: objc

    [myObject doFooWith:arg1
                   name:arg2
                  error:arg3];

不要使用下面的缩进风格：

.. code-block:: objc

    [myObject doFooWith:arg1 name:arg2  // some lines with >1 arg
                  error:arg3];

    [myObject doFooWith:arg1
                   name:arg2 error:arg3];

    [myObject doFooWith:arg1
              name:arg2  // aligning keywords instead of colons
              error:arg3];

方法定义与方法声明一样，当关键字的长度不足以以冒号对齐时，下一行都要以四个空格进行缩进。

.. code-block:: objc

    [myObj short:arg1
        longKeyword:arg2
        evenLongerKeyword:arg3];


``@public`` 和 ``@private``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. tip::

    ``@public`` 和 ``@private`` 访问修饰符应该以一个空格缩进。

与 C++ 中的 ``public, private`` 以及 ``protected`` 非常相似。

.. code-block:: objc

    @interface MyClass : NSObject {
     @public
      ...
     @private
      ...
    }
    @end


异常
~~~~~~~~~~

.. tip::

    每个 ``@`` 标签应该有独立的一行，在 ``@`` 与 ``{}`` 之间需要有一个空格， ``@catch`` 与被捕捉到的异常对象的声明之间也要有一个空格。

如果你决定使用 Objective-C 的异常，那么就按下面的格式。不过你最好先看看 :ref:`避免抛出异常 <avoid-throwing-exceptions>` 了解下为什么不要使用异常。

.. code-block:: objc

    @try {
      foo();
    }
    @catch (NSException *ex) {
      bar(ex);
    }
    @finally {
      baz();
    }


协议名
~~~~~~~~~~

.. tip::

    类型标识符和尖括号内的协议名之间，不能有任何空格。


这条规则适用于类声明、实例变量以及方法声明。例如：

.. code-block:: objc

    @interface MyProtocoledClass : NSObject<NSWindowDelegate> {
     @private
      id<MyFancyDelegate> delegate_;
    }
    - (void)setDelegate:(id<MyFancyDelegate>)aDelegate;
    @end


块（闭包）
~~~~~~~~~~

.. tip::

    块（block）适合用在 target/selector 模式下创建回调方法时，因为它使代码更易读。块中的代码应该缩进 4 个空格。

取决于块的长度，下列都是合理的风格准则：

* 如果一行可以写完块，则没必要换行。
* 如果不得不换行，关括号应与块声明的第一个字符对齐。
* 块内的代码须按 4 空格缩进。
* 如果块太长，比如超过 20 行，建议把它定义成一个局部变量，然后再使用该变量。
* 如果块不带参数，``^{`` 之间无须空格。如果带有参数，``^(`` 之间无须空格，但 ``) {`` 之间须有一个空格。
* 块内允许按两个空格缩进，但前提是和项目的其它代码保持一致的缩进风格。

.. code-block:: objc

    // The entire block fits on one line.
    [operation setCompletionBlock:^{ [self onOperationDone]; }];

    // The block can be put on a new line, indented four spaces, with the
    // closing brace aligned with the first character of the line on which
    // block was declared.
    [operation setCompletionBlock:^{
        [self.delegate newDataAvailable];
    }];

    // Using a block with a C API follows the same alignment and spacing
    // rules as with Objective-C.
    dispatch_async(fileIOQueue_, ^{
        NSString* path = [self sessionFilePath];
        if (path) {
          // ...
        }
    });

    // An example where the parameter wraps and the block declaration fits
    // on the same line. Note the spacing of |^(SessionWindow *window) {|
    // compared to |^{| above.
    [[SessionService sharedService]
        loadWindowWithCompletionBlock:^(SessionWindow *window) {
            if (window) {
              [self windowDidLoad:window];
            } else {
              [self errorLoadingWindow];
            }
        }];

    // An example where the parameter wraps and the block declaration does
    // not fit on the same line as the name.
    [[SessionService sharedService]
        loadWindowWithCompletionBlock:
            ^(SessionWindow *window) {
                if (window) {
                  [self windowDidLoad:window];
                } else {
                  [self errorLoadingWindow];
                }
            }];

    // Large blocks can be declared out-of-line.
    void (^largeBlock)(void) = ^{
        // ...
    };
    [operationQueue_ addOperationWithBlock:largeBlock];

