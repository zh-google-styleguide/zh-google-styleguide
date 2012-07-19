
Google Objective-C Style Guide 中文版
----------------------------------------

:版本:   2.36

:原作者:
    .. line-block::

         Mike Pinkerton
         Greg Miller
         Dave MacLachlan

:翻译:
    .. line-block::

        `ewangke <http://ke.indiebros.com/>`_
        `brantyoung <http://yangyubo.com>`_

:项目主页:
    - `Google Style Guide <http://google-styleguide.googlecode.com>`_
    - `Google 开源项目风格指南 - 中文版 <http://github.com/zh-google-styleguide/zh-google-styleguide>`_


译者的话
========

ewanke
^^^^^^^^^^^^

一直想翻译这个 `style guide <http://google-styleguide.googlecode.com/svn/trunk/objcguide.xml>`_ ，终于在周末花了7个小时的时间用vim敲出了HTML。很多术语的翻译很难，平时看的中文技术类书籍有限，对很多术语的中文译法不是很清楚，难免有不恰当之处，请读者指出并帮我改进：王轲 ”ewangke at gmail.com” 2011.03.27

brantyoung
^^^^^^^^^^^^

对 Objective-C 的了解有限，凭着感觉和 C/C++ 方面的理解：

* 把指南更新到 2.36 版本
* 调整了一些术语和句子


背景介绍
========

Objective-C 是 C 语言的扩展，增加了动态类型和面对对象的特性。它被设计成具有易读易用的，支持复杂的面向对象设计的编程语言。它是 Mac OS X 以及 iPhone 的主要开发语言。

Cocoa 是 Mac OS X 上主要的应用程序框架之一。它由一组 Objective-C 类组成，为快速开发出功能齐全的 Mac OS X 应用程序提供支持。

苹果公司已经有一份非常全面的 Objective-C 编码指南。Google 为 C++ 也写了一份类似的编码指南。而这份 Objective-C 指南则是苹果和 Google 常规建议的最佳结合。因此，在阅读本指南之前，请确定你已经阅读过：

* `Apple’s Cocoa Coding Guidelines <http://developer.apple.com/documentation/Cocoa/Conceptual/CodingGuidelines/index.html>`_

* `Google’s Open Source C++ Style Guide <http://codinn.com/projects/google-cpp-styleguide/>`_

.. note::

    所有在 Google 的 C++ 风格指南中所禁止的事情，如未明确说明，也同样不能在Objective-C++ 中使用。

本文档的目的在于为所有的 Mac OS X 的代码提供编码指南及实践。许多准则是在实际的项目和小组中经过长期的演化、验证的。Google 开发的开源项目遵从本指南的要求。

Google 已经发布了遵守本指南开源代码，它们属于 `Google Toolbox for Mac project <http://code.google.com/p/google-toolbox-for-mac/>`_ 项目（本文以缩写 GTM 指代）。GTM 代码库中的代码通常为了可以在不同项目中复用。

注意，本指南不是 Objective-C 教程。我们假定读者对 Objective-C 非常熟悉。如果你刚刚接触 Objective-C 或者需要温习，请阅读 `The Objective-C Programming Language <http://developer.apple.com/documentation/Cocoa/Conceptual/ObjectiveC/index.html>`_ 。

例子
========

都说一个例子顶上一千句话，我们就从一个例子开始，来感受一下编码的风格、留白以及命名等等。

一个头文件的例子，展示了在 ``@interface`` 声明中如何进行正确的注释以及留白。

.. code-block:: objc

    //  Foo.h
    //  AwesomeProject
    //
    //  Created by Greg Miller on 6/13/08.
    //  Copyright 2008 Google, Inc. All rights reserved.
    //

    #import <Foundation/Foundation.h>

    // A sample class demonstrating good Objective-C style. All interfaces,
    // categories, and protocols (read: all top-level declarations in a header)
    // MUST be commented. Comments must also be adjacent to the object they're
    // documenting.
    //
    // (no blank line between this comment and the interface)
    @interface Foo : NSObject {
     @private
      NSString *bar_;
      NSString *bam_;
    }

    // Returns an autoreleased instance of Foo. See -initWithBar: for details
    // about |bar|.
    + (id)fooWithBar:(NSString *)bar;

    // Designated initializer. |bar| is a thing that represents a thing that
    // does a thing.
    - (id)initWithBar:(NSString *)bar;

    // Gets and sets |bar_|.
    - (NSString *)bar;
    - (void)setBar:(NSString *)bar;

    // Does some work with |blah| and returns YES if the work was completed
    // successfully, and NO otherwise.
    - (BOOL)doWorkWithBlah:(NSString *)blah;

    @end

一个源文件的例子，展示了 ``@implementation`` 部分如何进行正确的注释、留白。同时也包括了基于引用实现的一些重要方法，如 ``getters`` 、 ``setters`` 、 ``init`` 以及 ``dealloc`` 。

.. code-block:: objc

    //
    //  Foo.m
    //  AwesomeProject
    //
    //  Created by Greg Miller on 6/13/08.
    //  Copyright 2008 Google, Inc. All rights reserved.
    //

    #import "Foo.h"


    @implementation Foo

    + (id)fooWithBar:(NSString *)bar {
      return [[[self alloc] initWithBar:bar] autorelease];
    }

    // Must always override super's designated initializer.
    - (id)init {
      return [self initWithBar:nil];
    }

    - (id)initWithBar:(NSString *)bar {
      if ((self = [super init])) {
        bar_ = [bar copy];
        bam_ = [[NSString alloc] initWithFormat:@"hi %d", 3];
      }
      return self;
    }

    - (void)dealloc {
      [bar_ release];
      [bam_ release];
      [super dealloc];
    }

    - (NSString *)bar {
      return bar_;
    }

    - (void)setBar:(NSString *)bar {
      [bar_ autorelease];
      bar_ = [bar copy];
    }

    - (BOOL)doWorkWithBlah:(NSString *)blah {
      // ...
      return NO;
    }

    @end


不要求在 ``@interface``、``@implementation`` 和 ``@end`` 前后空行。如果你在 ``@interface`` 声明了实例变量，则须在关括号 ``}`` 之后空一行。

除非接口和实现非常短，比如少量的私有方法或桥接类，空行方有助于可读性。
