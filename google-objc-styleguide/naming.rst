命名
=========


对于易维护的代码而言，命名规则非常重要。Objective-C 的方法名往往十分长，但代码块读起来就像散文一样，不需要太多的代码注释。

当编写纯粹的 Objective-C 代码时，我们基本遵守标准的 `Objective-C naming rules <http://developer.apple.com/documentation/Cocoa/Conceptual/CodingGuidelines/CodingGuidelines.html>`_，这些命名规则可能与 C++ 风格指南中的大相径庭。例如，Google 的 C++ 风格指南中推荐使用下划线分隔的单词作为变量名，而(苹果的)风格指南则使用驼峰命名法，这在 Objective-C 社区中非常普遍。

任何的类、类别、方法以及变量的名字中都使用全大写的 `首字母缩写 <http://en.wikipedia.org/wiki/Initialism>`_。这遵守了苹果的标准命名方式，如 URL、TIFF 以及 EXIF。

当编写 Objective-C++ 代码时，事情就不这么简单了。许多项目需要实现跨平台的 C++ API，并混合一些 Objective-C、Cocoa 代码，或者直接以 C++ 为后端，前端用本地 Cocoa 代码。这就导致了两种命名方式直接不统一。

我们的解决方案是：编码风格取决于方法/函数以哪种语言实现。如果在一个 ``@implementation`` 语句中，就使用 Objective-C 的风格。如果实现一个 C++ 的类，就使用 C++ 的风格。这样避免了一个函数里面实例变量和局部变量命名规则混乱，严重影响可读性。

文件名
~~~~~~~~

.. tip::

    文件名须反映出其实现了什么类 -- 包括大小写。遵循你所参与项目的约定。

文件的扩展名应该如下：

=======  ==========================
``.h``   C/C++/Objective-C 的头文件
``.m``   Ojbective-C 实现文件
``.mm``  Ojbective-C++ 的实现文件
``.cc``  纯 C++ 的实现文件
``.c``   纯 C 的实现文件
=======  ==========================

类别的文件名应该包含被扩展的类名，如：``GTMNSString+Utils.h`` 或``GTMNSTextView+Autocomplete.h``。


Objective-C++
~~~~~~~~~~~~~~~~

.. tip::

    源代码文件内，Ojbective-C++ 代码遵循你正在实现的函数/方法的风格。

为了最小化 Cocoa/Objective-C 与 C++ 之间命名风格的冲突，根据待实现的函数/方法选择编码风格。实现 ``@implementation`` 语句块时，使用 Objective-C 的命名规则；如果实现一个 C++ 的类，就使用 C++ 命名规则。

.. code-block:: objc

    // file: cross_platform_header.h

    class CrossPlatformAPI {
     public:
      ...
      int DoSomethingPlatformSpecific();  // impl on each platform
     private:
      int an_instance_var_;
    };

    // file: mac_implementation.mm
    #include "cross_platform_header.h"

    // A typical Objective-C class, using Objective-C naming.
    @interface MyDelegate : NSObject {
     @private
      int instanceVar_;
      CrossPlatformAPI* backEndObject_;
    }
    - (void)respondToSomething:(id)something;
    @end
    @implementation MyDelegate
    - (void)respondToSomething:(id)something {
      // bridge from Cocoa through our C++ backend
      instanceVar_ = backEndObject->DoSomethingPlatformSpecific();
      NSString* tempString = [NSString stringWithInt:instanceVar_];
      NSLog(@"%@", tempString);
    }
    @end

    // The platform-specific implementation of the C++ class, using
    // C++ naming.
    int CrossPlatformAPI::DoSomethingPlatformSpecific() {
      NSString* temp_string = [NSString stringWithInt:an_instance_var_];
      NSLog(@"%@", temp_string);
      return [temp_string intValue];
    }


类名
~~~~~

.. tip::

    类名（以及类别、协议名）应首字母大写，并以驼峰格式分割单词。

*应用层* 的代码，应该尽量避免不必要的前缀。为每个类都添加相同的前缀无助于可读性。当编写的代码期望在不同应用程序间复用时，应使用前缀（如：``GTMSendMessage``）。


类别名
~~~~~~

.. tip::

    类别名应该有两三个字母的前缀以表示类别是项目的一部分或者该类别是通用的。类别名应该包含它所扩展的类的名字。

比如我们要基于 ``NSString`` 创建一个用于解析的类别，我们将把类别放在一个名为 ``GTMNSString+Parsing.h`` 的文件中。类别本身命名为 ``GTMStringParsingAdditions`` （是的，我们知道类别名和文件名不一样，但是这个文件中可能存在多个不同的与解析有关类别）。类别中的方法应该以 ``gtm_myCategoryMethodOnAString:`` 为前缀以避免命名冲突，因为 Objective-C 只有一个名字空间。如果代码不会分享出去，也不会运行在不同的地址空间中，方法名字就不那么重要了。

类名与包含类别名的括号之间，应该以一个空格分隔。


Objective-C 方法名
~~~~~~~~~~~~~~~~~~~~~~~~

.. tip::

    方法名应该以小写字母开头，并混合驼峰格式。每个具名参数也应该以小写字母开头。

方法名应尽量读起来就像句子，这表示你应该选择与方法名连在一起读起来通顺的参数名。（例如，``convertPoint:fromRect:`` 或 ``replaceCharactersInRange:withString:``）。详情参见 `Apple’s Guide to Naming Methods <http://developer.apple.com/documentation/Cocoa/Conceptual/CodingGuidelines/Articles/NamingMethods.html>`_。

访问器方法应该与他们 ``要获取的`` 成员变量的名字一样，但不应该以get作为前缀。例如：

.. code-block:: objc

    - (id)getDelegate;  // AVOID
    - (id)delegate;     // GOOD

这仅限于 Objective-C 的方法名。C++ 的方法与函数的命名规则应该遵从 C++ 风格指南中的规则。


变量名
~~~~~~~~~~

.. tip::

    变量名应该以小写字母开头，并使用驼峰格式。类的成员变量应该以下划线作为后缀。例如：``myLocalVariable``、``myInstanceVariable_``。如果不能使用 Objective-C 2.0 的 ``@property``，使用 KVO/KVC 绑定的成员变量可以以一个下划线作为前缀。


普通变量名
^^^^^^^^^^^^

对于静态的属性（``int`` 或指针），不要使用匈牙利命名法。尽量为变量起一个描述性的名字。不要担心浪费列宽，因为让新的代码阅读者立即理解你的代码更重要。例如：

* 错误的命名：

    .. code-block:: objc

        int w;
        int nerr;
        int nCompConns;
        tix = [[NSMutableArray alloc] init];
        obj = [someObject object];
        p = [network port];

* 正确的命名：

    .. code-block:: objc

        int numErrors;
        int numCompletedConnections;
        tickets = [[NSMutableArray alloc] init];
        userInfo = [someObject object];
        port = [network port];

实例变量
^^^^^^^^^^^^

实例变量应该混合大小写，并以下划线作为后缀，如 ``usernameTextField_``。然而，如果不能使用 Objective-C 2.0（操作系统版本的限制），并且使用了 KVO/KVC 绑定成员变量时，我们允许例外（译者注： ``KVO=Key Value Observing，KVC=Key Value Coding``）。这种情况下，可以以一个下划线作为成员变量名字的前缀，这是苹果所接受的键/值命名惯例。如果可以使用 Objective-C 2.0，``@property`` 以及 ``@synthesize`` 提供了遵从这一命名规则的解决方案。


常量
^^^^^^^^^^^^

常量名（如宏定义、枚举、静态局部变量等）应该以小写字母 ``k`` 开头，使用驼峰格式分隔单词，如：``kInvalidHandle，kWritePerm``。


