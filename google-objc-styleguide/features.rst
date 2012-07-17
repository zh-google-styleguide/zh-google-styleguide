Cocoa 和 Objective-C 特性
==============================


成员变量应该是 ``@private``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. tip::

    成员变量应该声明为 ``@private``

.. code-block:: objc

    @interface MyClass : NSObject {
     @private
      id myInstanceVariable_;
    }
    // public accessors, setter takes ownership
    - (id)myInstanceVariable;
    - (void)setMyInstanceVariable:(id)theVar;
    @end



明确指定构造函数
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. tip::

    注释并且明确指定你的类的构造函数。

对于需要继承你的类的人来说，明确指定构造函数十分重要。这样他们就可以只重写一个构造函数（可能是几个）来保证他们的子类的构造函数会被调用。这也有助于将来别人调试你的类时，理解初始化代码的工作流程。


重载指定构造函数
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. tip::

    当你写子类的时候，如果需要 ``init…`` 方法，记得重载父类的指定构造函数。

如果你没有重载父类的指定构造函数，你的构造函数有时可能不会被调用，这会导致非常隐秘而且难以解决的 bug。


重载 ``NSObject`` 的方法
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. tip::

    如果重载了 ``NSObject`` 类的方法，强烈建议把它们放在 ``@implementation`` 内的起始处，这也是常见的操作方法。

通常适用（但不局限）于 ``init...``，``copyWithZone:``，以及 ``dealloc`` 方法。所有 ``init...`` 方法应该放在一起，``copyWithZone:`` 紧随其后，最后才是 ``dealloc`` 方法。

初始化
~~~~~~~~~~~

.. tip::

    不要在 init 方法中，将成员变量初始化为 ``0`` 或者 ``nil``；毫无必要。

刚分配的对象，默认值都是 0，除了 ``isa`` 指针（译者注：``NSObject`` 的 ``isa`` 指针，用于标识对象的类型）。所以不要在初始化器里面写一堆将成员初始化为 ``0`` 或者 ``nil`` 的代码。


避免 ``+new``
~~~~~~~~~~~~~~~

.. tip::

    不要调用 ``NSObject`` 类方法 ``new``，也不要在子类中重载它。使用 ``alloc`` 和 ``init`` 方法创建并初始化对象。


现代的 Ojbective-C 代码通过调用 ``alloc`` 和 ``init`` 方法来创建并 retain 一个对象。由于类方法 ``new`` 很少使用，这使得有关内存分配的代码审查更困难。

保持公共 API 简单
~~~~~~~~~~~~~~~~~~~~~~~

.. tip::

    保持类简单；避免 “厨房水槽（kitchen-sink）” 式的 API。如果一个函数压根没必要公开，就不要这么做。用私有类别保证公共头文件整洁。

与 C++ 不同，Objective-C 没有方法来区分公共的方法和私有的方法 -- 所有的方法都是公共的（译者注：这取决于 Objective-C 运行时的方法调用的消息机制）。因此，除非客户端的代码期望使用某个方法，不要把这个方法放进公共 API 中。尽可能的避免了你你不希望被调用的方法却被调用到。这包括重载父类的方法。对于内部实现所需要的方法，在实现的文件中定义一个类别，而不是把它们放进公有的头文件中。

.. code-block:: objc

    // GTMFoo.m
    #import "GTMFoo.h"

    @interface GTMFoo (PrivateDelegateHandling)
    - (NSString *)doSomethingWithDelegate;  // Declare private method
    @end

    @implementation GTMFoo(PrivateDelegateHandling)
    ...
    - (NSString *)doSomethingWithDelegate {
      // Implement this method
    }
    ...
    @end

Objective-C 2.0 以前，如果你在私有的 ``@interface`` 中声明了某个方法，但在 ``@implementation`` 中忘记定义这个方法，编译器不会抱怨（这是因为你没有在其它的类别中实现这个私有的方法）。解决文案是将方法放进指定类别的 ``@implemenation`` 中。

如果你在使用 Objective-C 2.0，相反你应该使用 `类扩展 <http://developer.apple.com/documentation/Cocoa/Conceptual/ObjectiveC/Articles/chapter_4_section_5.html>`_ 来声明你的私有类别，例如：

.. code-block:: objc

    @interface GMFoo () { ... }

这么做确保如果声明的方法没有在 ``@implementation`` 中实现，会触发一个编译器告警。

再次说明，“私有的” 方法其实不是私有的。你有时可能不小心重载了父类的私有方法，因而制造出很难查找的 Bug。通常，私有的方法应该有一个相当特殊的名字以防止子类无意地重载它们。

Ojbective-C 的类别可以用来将一个大的 ``@implementation`` 拆分成更容易理解的小块，同时，类别可以为最适合的类添加新的、特定应用程序的功能。例如，当添加一个 “middle truncation” 方法时，创建一个 ``NSString`` 的新类别并把方法放在里面，要比创建任意的一个新类把方法放进里面好得多。

``#import`` and ``#include``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. tip::

    ``#import`` Ojbective-C/Objective-C++ 头文件，``#include`` C/C++ 头文件。

基于你所包括的头文件的编程语言，选择使用 ``#import`` 或是 ``#include``：

* 当包含一个使用 Objective-C、Objective-C++ 的头文件时，使用 ``#import`` 。
* 当包含一个使用标准 C、C++ 头文件时，使用 ``#include``。头文件应该使用 `#define 保护 <http://google-styleguide.googlecode.com/svn/trunk/cppguide.xml?showone=The__define_Guard#The__define_Guard>`_。

一些 Ojbective-C 的头文件缺少 ``#define`` 保护，需要使用 ``#import`` 的方式包含。由于 Objective-C 的头文件只会被 Objective-C 的源文件及头文件包含，广泛地使用 ``#import`` 是可以的。

文件中没有 Objective-C 代码的标准 C、C++ 头文件，很可能会被普通的 C、C++ 包含。由于标准 C、C++ 里面没有 ``#import`` 的用法，这些文件将被 ``#include``。在 Objective-C 源文件中使用 ``#include`` 包含这些头文件，意味着这些头文件永远会在相同的语义下包含。

这条规则帮助跨平台的项目避免低级错误。某个 Mac 开发者写了一个新的 C 或 C++ 头文件，如果忘记使用 ``#define`` 保护，在 Mac 下使用 ``#import`` 这个头文件不回引起问题，但是在其它平台下使用 ``#include`` 将可能编译失败。在所有的平台上统一使用 ``#include``，意味着构造更可能全都成功或者失败，防止这些文件只能在某些平台下能够工作。

.. code-block:: objc

    #import <Cocoa/Cocoa.h>
    #include <CoreFoundation/CoreFoundation.h>
    #import "GTMFoo.h"
    #include "base/basictypes.h"


使用根框架
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. tip::

    ``#import`` 根框架而不是单独的零散文件

当你试图从框架（如 Cocoa 或者 Foundation）中包含若干零散的系统头文件时，实际上包含顶层根框架的话，编译器要做的工作更少。根框架通常已经经过预编译，加载更快。另外记得使用 ``#import`` 而不是 ``#include`` 来包含 Objective-C 的框架。

.. code-block:: objc

    #import <Foundation/Foundation.h>     // good

    #import <Foundation/NSArray.h>        // avoid
    #import <Foundation/NSString.h>
    ...


构建时即设定 ``autorelease``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. tip::

    当创建临时对象时，在同一行使用 ``autolease``，而不是在同一个方法的后面语句中使用一个单独的 ``release``。

尽管运行效率会差一点，但避免了意外删除 ``release`` 或者插入 ``return`` 语句而导致内存泄露的可能。例如：

.. code-block:: objc

    // AVOID (unless you have a compelling performance reason)
    MyController* controller = [[MyController alloc] init];
    // ... code here that might return ...
    [controller release];

    // BETTER
    MyController* controller = [[[MyController alloc] init] autorelease];


``autorelease`` 优先 ``retain`` 其次
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. tip::

    给对象赋值时遵守 ``autorelease``之后 ``retain`` 的模式。

当给一个变量赋值新的对象时，必须先释放掉旧的对象以避免内存泄露。有很多 “正确的” 方法可以处理这种情况。我们则选择 “``autorelease`` 之后 ``retain``” 的方法，因为事实证明它不容易出错。注意大的循环会填满 ``autorelease`` 池，并且可能效率上会差一点，但权衡之下我们认为是可以接受的。

.. code-block:: objc

    - (void)setFoo:(GMFoo *)aFoo {
      [foo_ autorelease];  // Won't dealloc if |foo_| == |aFoo|
      foo_ = [aFoo retain];
    }


``init`` 和 ``dealloc`` 内避免使用访问器
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. tip::

    在 ``init`` 和 ``dealloc`` 方法执行的过程中，子类可能会处在一个不一致的状态，所以这些方法中的代码应避免调用访问器。

子类尚未初始化，或在 ``init`` 和 ``dealloc`` 方法执行时已经被销毁，会使访问器方法很可能不可靠。实际上，应在这些方法中直接对 ivals 进行赋值或释放操作。

正确：

.. code-block:: objc

    - (id)init {
      self = [super init];
      if (self) {
        bar_ = [[NSMutableString alloc] init];  // good
      }
      return self;
    }

    - (void)dealloc {
      [bar_ release];                           // good
      [super dealloc];
    }

错误：

.. code-block:: objc

    - (id)init {
      self = [super init];
      if (self) {
        self.bar = [NSMutableString string];  // avoid
      }
      return self;
    }

    - (void)dealloc {
      self.bar = nil;                         // avoid
      [super dealloc];
    }


按声明顺序销毁实例变量
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. tip::

    ``dealloc`` 中实例变量被释放的顺序应该与它们在 ``@interface`` 中声明的顺序一致，这有助于代码审查。

代码审查者在评审新的或者修改过的 ``dealloc`` 实现时，需要保证每个 ``retained`` 的实例变量都得到了释放。

为了简化 ``dealloc`` 的审查，``retained`` 实例变量被释放的顺序应该与他们在 ``@interface`` 中声明的顺序一致。如果 ``dealloc`` 调用了其它方法释放成员变量，添加注释解释这些方法释放了哪些实例变量。

``setter`` 应复制 NSStrings
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. tip::

    接受 ``NSString`` 作为参数的 ``setter``，应该总是 ``copy`` 传入的字符串。

永远不要仅仅 ``retain`` 一个字符串。因为调用者很可能在你不知情的情况下修改了字符串。不要假定别人不会修改，你接受的对象是一个 ``NSString`` 对象而不是 ``NSMutableString`` 对象。

.. code-block:: objc

    - (void)setFoo:(NSString *)aFoo {
      [foo_ autorelease];
      foo_ = [aFoo copy];
    }



.. _avoid-throwing-exceptions:

避免抛异常
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. tip::

    不要 ``@throw`` Objective-C 异常，同时也要时刻准备捕获从第三方或 OS 代码中抛出的异常。

我们的确允许 ``-fobjc-exceptions`` 编译开关（主要因为我们要用到 ``@synchronized`` ），但我们不使用 ``@throw``。为了合理使用第三方的代码，``@try``、``@catch`` 和 ``@finally`` 是允许的。如果你确实使用了异常，请明确注释你期望什么方法抛出异常。

不要使用 ``NS_DURING``、``NS_HANDLER``、``NS_ENDHANDLER``、``NS_VALUERETURN`` 和 ``NS_VOIDRETURN`` 宏，除非你写的代码需要在 Mac OS X 10.2 或之前的操作系统中运行。

注意：如果抛出 Objective-C 异常，Objective-C++ 代码中基于栈的对象不会被销毁。比如：

.. code-block:: objc

    class exceptiontest {
     public:
      exceptiontest() { NSLog(@"Created"); }
      ~exceptiontest() { NSLog(@"Destroyed"); }
    };

    void foo() {
      exceptiontest a;
      NSException *exception = [NSException exceptionWithName:@"foo"
                                                       reason:@"bar"
                                                     userInfo:nil];
      @throw exception;
    }

    int main(int argc, char *argv[]) {
      GMAutoreleasePool pool;
      @try {
        foo();
      }
      @catch(NSException *ex) {
        NSLog(@"exception raised");
      }
      return 0;
    }

会输出：

.. ：：

    2006-09-28 12:34:29.244 exceptiontest[23661] Created
    2006-09-28 12:34:29.244 exceptiontest[23661] exception raised


注意：这里析构函数从未被调用。这主要会影响基于栈的 ``smartptr``，比如 ``shared_ptr``、``linked_ptr``，以及所有你可能用到的 STL 对象。因此我们不得不痛苦的说，如果必须在 Objective-C++ 中使用异常，就只用 C++ 的异常机制。永远不应该重新抛出 Objective-C 异常，也不应该在 ``@try``、``@catch`` 或 ``@finally`` 语句块中使用基于栈的 C++ 对象。

nil 检查
~~~~~~~~~~~~~~

.. tip::

    ``nil`` 检查只用在逻辑流程中。



使用 ``nil`` 的检查来检查应用程序的逻辑流程，而不是避免崩溃。Objective-C 运行时会处理向 ``nil`` 对象发送消息的情况。如果方法没有返回值，就没关系。如果有返回值，可能由于运行时架构、返回值类型以及 OS X 版本的不同而不同，参见 `Apple’s documentation <http://developer.apple.com/documentation/Cocoa/Conceptual/ObjectiveC/Articles/chapter_2_section_3.html>`_ 。

注意，这和 C/C++ 中检查指针是否为 ‵‵NULL`` 很不一样，C/C++ 运行时不做任何检查，从而导致应用程序崩溃。因此你仍然需要保证你不会对一个 C/C++ 的空指针解引用。

BOOL 若干陷阱
~~~~~~~~~~~~~~~~~~~~~

.. tip::

    将普通整形转换成 ``BOOL`` 时要小心。不要直接将 ``BOOL`` 值与 ``YES`` 进行比较。

Ojbective-C 中把 ``BOOL`` 定义成无符号字符型，这意味着 ``BOOL`` 类型的值远不止 ``YES``(1)或 ``NO``(0)。不要直接把整形转换成 ``BOOL``。常见的错误包括将数组的大小、指针值及位运算的结果直接转换成 ``BOOL`` ，取决于整型结果的最后一个字节，很可能会产生一个 ``NO`` 值。当转换整形至 ``BOOL`` 时，使用三目操作符来返回 ``YES`` 或者 ``NO``。（译者注：读者可以试一下任意的 256 的整数的转换结果，如 256、512 …）

你可以安全在 ``BOOL``、``_Bool`` 以及 ``bool`` 之间转换（参见 C++ Std 4.7.4, 4.12 以及 C99 Std 6.3.1.2）。你不能安全在 ``BOOL`` 以及 ``Boolean`` 之间转换，因此请把 ``Boolean`` 当作一个普通整形，就像之前讨论的那样。但 Objective-C 的方法标识符中，只使用 ``BOOL``。

对 ``BOOL`` 使用逻辑运算符（``&&``，``||`` 和 ``!``）是合法的，返回值也可以安全地转换成 ``BOOL``，不需要使用三目操作符。

错误的用法：

.. code-block:: objc

    - (BOOL)isBold {
      return [self fontTraits] & NSFontBoldTrait;
    }
    - (BOOL)isValid {
      return [self stringValue];
    }


正确的用法：

    .. code-block:: objc

    - (BOOL)isBold {
      return ([self fontTraits] & NSFontBoldTrait) ? YES : NO;
    }
    - (BOOL)isValid {
      return [self stringValue] != nil;
    }
    - (BOOL)isEnabled {
      return [self isValid] && [self isBold];
    }


同样，不要直接比较 ``YES/NO`` 和 ``BOOL`` 变量。不仅仅因为影响可读性，更重要的是结果可能与你想的不同。

错误的用法：

.. code-block:: objc

    BOOL great = [foo isGreat];
    if (great == YES)
      // ...be great!

正确的用法：

.. code-block:: objc

    BOOL great = [foo isGreat];
    if (great)
      // ...be great!

属性（Property）
~~~~~~~~~~~~~~~~~~~~~

.. tip::

    属性（Property）通常允许使用，但需要清楚的了解：属性（Property）是 Objective-C 2.0 的特性，会限制你的代码只能跑在 iPhone 和 Mac OS X 10.5 (Leopard) 及更高版本上。点引用只允许访问声明过的 ``@property``。

命名
^^^^^^

属性所关联的实例变量的命名必须遵守以下划线作为后缀的规则。属性的名字应该与成员变量去掉下划线后缀的名字一模一样。

使用 ``@synthesize`` 指示符来正确地重命名属性。

.. code-block:: objc

    @interface MyClass : NSObject {
     @private
      NSString *name_;
    }
    @property(copy, nonatomic) NSString *name;
    @end

    @implementation MyClass
    @synthesize name = name_;
    @end


位置
^^^^^^

属性的声明必须紧靠着类接口中的实例变量语句块。属性的定义必须在 ``@implementation`` 的类定义的最上方。他们的缩进与包含他们的 ``@interface`` 以及 ``@implementation`` 语句一样。

.. code-block:: objc

    @interface MyClass : NSObject {
     @private
      NSString *name_;
    }
    @property(copy, nonatomic) NSString *name;
    @end

    @implementation MyClass
    @synthesize name = name_;
    - (id)init {
    ...
    }
    @end


字符串应使用 ``copy`` 属性（Attribute）
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

应总是用 ``copy`` 属性（attribute）声明 ``NSString`` 属性（property）。

从逻辑上，确保遵守 ``NSString`` 的 ``setter`` 必须使用 ``copy`` 而不是 ``retain`` 的原则。


原子性
^^^^^^^^^^

一定要注意属性（property）的开销。缺省情况下，所有 ``synthesize`` 的 ``setter`` 和 ``getter`` 都是原子的。这会给每个 ``get`` 或者 ``set`` 带来一定的同步开销。将属性（property）声明为 ``nonatomic``，除非你需要原子性。


点引用
^^^^^^^^^^

点引用是地道的 Objective-C 2.0 风格。它被使用于简单的属性 ``set``、``get`` 操作，但不应该用它来调用对象的其它操作。

正确的做法：

.. code-block:: objc

    NSString *oldName = myObject.name;
    myObject.name = @"Alice";

错误的做法：

.. code-block:: objc

    NSArray *array = [[NSArray arrayWithObject:@"hello"] retain];

    NSUInteger numberOfItems = array.count;  // not a property
    array.release;                           // not a property


没有实例变量的接口
~~~~~~~~~~~~~~~~~~~~~

.. tip::

    没有声明任何实例变量的接口，应省略空花括号。

正确的做法：

    @interface MyClass : NSObject
    // Does a lot of stuff
    - (void)fooBarBam;
    @end

错误的做法：

    @interface MyClass : NSObject {
    }
    // Does a lot of stuff
    - (void)fooBarBam;
    @end



自动 ``synthesize`` 实例变量
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. tip::

    只运行在 iOS 下的代码，优先考虑使用自动 ``synthesize`` 实例变量。

``synthesize`` 实例变量时，使用 ``@synthesize var = var_;`` 防止原本想调用 ``self.var = blah;`` 却不慎写成了 ``var = blah;``。


不要synthesize CFType的属性 CFType应该永远使用@dynamic实现指示符。 尽管CFType不能使用retain属性特性，开发者必须自己处理retain和release。很少有情况你需要仅仅对它进行赋值，因此最好显示地实现getter和setter，并作出注释说明。 列出所有的实现指示符 尽管@dynamic是默认的，显示列出它以及其它的实现指示符会提高可读性，代码阅读者可以一眼就知道类的每个属性是如何实现的。

.. code-block:: objc

    // Header file
    @interface Foo : NSObject
    // A guy walks into a bar.
    @property(nonatomic, copy) NSString *bar;
    @end

    // Implementation file
    @interface Foo ()
    @property(nonatomic, retain) NSArray *baz;
    @end

    @implementation Foo
    @synthesize bar = bar_;
    @synthesize baz = baz_;
    @end

