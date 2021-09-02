语法规范
################################################################################

.. _ts-identifiers:

标识符
********************************************************************************

.. _ts-naming:

命名规范
================================================================================

在 TypeScript 中，标识符只能使用 ASCII 码表中的字母、数字、下划线与 ``(``。因此，合法的标识符可以使用正则表达式 ``[\)\w]+`` 进行匹配。根据标识符的用途不同，使用的命名法也不同，如下表所示：

======================================== ========================================
命名法                                                      分类
======================================== ========================================
帕斯卡命名法（ ``UpperCamelCase`` ）                类、接口、类型、枚举、装饰器、类型参数
驼峰式命名法（ ``lowerCamelCase`` ）                变量、参数、函数、方法、属性、模块别名
全大写下划线命名法（ ``CONSTANT_CASE``）                     全局常量、枚举值
私有成员命名法（ ``#ident`` ）                                  不允许使用
======================================== ========================================

.. _ts-abbreviations:

缩写
--------------------------------------------------------------------------------

缩写应被视为一个词。例如，应使用 ``loadHttpUrl``，而非 ``loadHTTPURL``。平台有特殊要求的标识符例外，如 ``XMLHttpRequest``。

.. _ts-dollar-sign:

美元符号 \$
--------------------------------------------------------------------------------

一般情况下，标识符不应使用 `$`，除非为了与第三方框架的命名规范保持一致。关于 `$` 的使用，可参见 :ref:`ts-naming-style` 一节对 ``Observable`` 类型的说明。

.. _ts-type-parameters:

类型参数
--------------------------------------------------------------------------------

形如 ``Array<T>`` 的类型参数既可以使用单个大写字母（如 ``T``），也可以使用帕斯卡命名法（如 ``UpperCamelCase``）。

.. _ts-test-names:

测试用例
--------------------------------------------------------------------------------

无论是在 `Closure <https://github.com/google/closure-library>`_ 库的 ``testSuites`` 还是 `xUnit <https://xunit.net/>`_ 风格的测试框架中，都可以使用 ``_`` 作为标识符的分隔符，例如 ``testX_whenY_doesZ()``。

.. _ts-underscore-prefix-suffix:

``_`` 前缀与后缀
--------------------------------------------------------------------------------

标识符禁止使用下划线 ``_`` 作为前缀或后缀。这也意味着，禁止使用单个下划线 ``_`` 作为标识符（例如：用来表示未被使用的参数）。

如果需要从数组或元组中取出某个或某几个特定的元素的话，可以在解构语句中插入额外的逗号，忽略掉不需要的元素：

.. code-block:: typescript

    const [a, , b] = [1, 5, 10];  // a <- 1, b <- 10

.. _ts-imports:

导入模块
--------------------------------------------------------------------------------

导入模块的命名空间时使用驼峰命名法（``lowerCamelCase``），文件名则使用蛇形命名法（``snake_case``）。例如：

.. code-block:: typescript

    import * as fooBar from './foo_bar';

一些库可能会在导入命名空间时使用某种特定的前缀，这与这里规定的命名规范有所冲突。然而，由于其中的一些库已经被广泛使用，因此遵循它们的特殊规则反而能够获得更好的可读性。这些特例包括：

* `jQuery <https://jquery.com/>`_，使用 ``$`` 前缀。

* `three.js <https://threejs.org/>`_，使用 ``THREE`` 前缀。

.. _ts-constants:

常量
--------------------------------------------------------------------------------

常量命名（``CONSTANT_CASE``）表示某个值不可被修改。它还可以用于虽然技术上可以实现，但是用户不应当试图修改的值，比如并未进行深度冻结（deep frozen）的值。

.. code-block:: typescript

    const UNIT_SUFFIXES = {
        'milliseconds': 'ms',
        'seconds': 's',
    };
    // UNIT_SUFFIXES 使用了常量命名，
    // 这意味着用户不应试图修改它，
    // 即使它实际上是一个可变的值。

这里所说的常量，也包括类中的静态只读属性：

.. code-block:: typescript

    class Foo {
        private static readonly MY_SPECIAL_NUMBER = 5;

        bar() {
            return 2 * Foo.MY_SPECIAL_NUMBER;
        }
    }

.. _ts-others:

其他
--------------------------------------------------------------------------------

如果某个值在程序的整个运行生命周期中会被多次实例化或被用户以任何方式进行修改，则它必须使用驼峰式命名法。

如果某个值是作为某个接口的实现的箭头函数，则它也可以使用驼峰式命名法。

.. _ts-aliases:

别名
================================================================================

在为一个已有的标识符创建具有局部作用域的别名时，别名的命名方式应当与现有的标识符和现有的命名规范保持一致。声明别名时，应使用 ``const`` （如果它是一个变量）或 ``readonly`` （如果它是类里的一个字段）。

.. code-block:: typescript

    const {Foo} = SomeType;
    const CAPACITY = 5;

    class Teapot {
        readonly BrewStateEnum = BrewStateEnum;
        readonly CAPACITY = CAPACITY;
    }

.. _ts-naming-style:

命名风格
================================================================================

TypeScript 中的类型表达了丰富的信息，因此在起名时不应与类型中所携带的信息重复。（关于更多在起名时应避免的内容，可参见谷歌的 `Testing Blog <https://testing.googleblog.com/2017/10/code-health-identifiernamingpostforworl.html>`_。）

这里有几个具体的例子：

* 不要为私有属性或方法名添加下划线 `_` 前缀或后缀。

* 不要为可选参数添加 `opt_` 前缀。
  
  * 关于在存取器中的特例，参见后文 :ref:`name-and-order-of-includes` 。

* 除非在项目中已成惯例，否则不要显式地标记接口类型（例如不要使用 ``IMyInterface`` 或者 ``MyFooInterface`` ）。在为类添加接口时，接口名称中应包含创建这一接口的原因。（例如，在为类 ``TodoItem`` 创建一个将其转为 JSON 格式以用于存储或者序列化的接口时，可以将这一接口命名为 ``TodoItemStorage`` 。）

* 对于 ``Observable`` 类型的值，通常的惯例是使用 ``$`` 前缀将其与一般类型的值进行区分，使之不致混淆。各个团队可以在与项目内部的现有做法保持一致的前提下，自行决定是否采用这一做法。

.. _ts-descriptive-names:

描述性命名
================================================================================

命名应当具有描述性且易于读者理解。不要使用对项目以外的用户而言含糊不清或并不熟悉的缩写，不要通过删减单词中的字母来强行创造缩写。

这一规则的例外是，对不超过十行的作用域中的变量，以及内部 API 的参数，可以使用短变量名（例如 ``i`` 、 ``j`` 等只有单个字母的变量名）。

.. _ts-file-encoding:

文件编码
********************************************************************************

使用 UTF-8 文件编码。

对于非 ASCII 字符，应使用实际的 Unicode 字符（例如 ``∞`` ）。对于非输出字符，使用对应的十六进制编码或 Unicode 转义编码（如 ``\u221e`` ），并添加注释进行说明。

.. code-block:: typescript

    // 应当这样做！即使没有注释也十分易懂。
    const units = 'μs';

    // 应当这样做！对非输出字符进行转义。
    const output = '\ufeff' + content;  // 字节顺序标记（Byte Order Mark，BOM）

.. code-block:: typescript

    // 不要这样做！即使加上注释也不太好读，而且容易出错。
    const units = '\u03bcs'; // Greek letter mu, 's'

    // 不要省略注释！读者在缺少注释的情况下很难理解这个字符的含义。
    const output = '\ufeff' + content;

.. _ts-comments-documentation:

注释与文档
********************************************************************************

.. _ts-jsdoc-vs-comments:

用 JSDoc 还是 注释？
================================================================================

TypesScript 中有两种类型的注释：JSDoc ``/** ... */`` 和普通注释 ``// ... 或者 /* ... */`` 。

* 对于文档，也就是用户应当阅读的注释，使用 ``/** JSDoc */`` 。
* 对于实现说明，也就是只和代码本身的实现细节有关的注释，使用 ``// 行注释`` 。

JSDoc 注释能够为工具（例如编辑器或文档生成器）所识别，而普通注释只能供人阅读。

.. _ts-jsdoc-rules-follow-the-js-style:

JSDoc 规范
================================================================================

JSDoc 的规范大部分遵循 JavaScript 风格指南中的规定。具体地说，遵循 JavaScript 风格指南中 :ref:`js-comments` 一节的规则。本节的剩余部分只对与这些规则不一致的部分进行说明。

.. _ts-document-all-top-level-exports-of-modules:

对所有导出的顶层模块进行注释
================================================================================

使用 ``/** JSDoc */`` 注释为代码的用户提供信息。这些注释应当言之有物，切忌仅仅将属性名或参数名重抄一遍。如果代码的审核人认为某个属性或方法的作用不能从它的名字上一目了然地看出来的话，这些属性和方法同样应当使用 ``/** JSDoc */`` 注释添加说明文档，无论它们是否被导出，是公开还是私有的。

.. _ts-omit-comments-that-are-redundant-with-ts:

省略对于 TypeScript 而言多余的注释
================================================================================

例如，不要在 ``@param`` 或 ``@return`` 注释中声明类型，不要在使用了 ``implements`` 、 ``enum`` 、 ``private`` 等关键字的地方添加 ``@implements`` 、 ``@enum`` 、 ``@private`` 等注释。

.. _ts-do-not-use-override:

不要使用 ``@override``
================================================================================

不要在 TypeScript 代码中使用 ``@override`` 注释。 ``@override`` 并不会被编译器视为强制性约束，这会导致注释与实现上的不一致性。如果纯粹为了文档添加这一注释，反而令人困惑。

.. _ts-make-comments-that-actually-add-information:

注释必须言之有物
================================================================================

虽然大多数情况下文档对代码十分有益，但对于那些并不用于导出的符号，有时其函数或参数的名称与类型便足以描述自身了。

注释切忌照抄参数类型和参数名，如下面的反面示例：

.. code-block:: typescript

    // 不要这样做！这个注释没有任何有意义的内容。
    /** @param fooBarService Foo 应用的 Bar 服务 */

因此，只有当需要添加额外信息时才使用 ``@param`` 和 ``@return`` 注释，其它情况下直接省略即可。

.. code-block:: typescript

    /**
     * 发送 POST 请求，开始煮咖啡
     * @param amountLitres 煮咖啡的量，注意和煮锅的尺寸对应！
     */
    brew(amountLitres: number, logger: Logger) {
        // ...
    }

.. _ts-parameter-property-comments:

参数属性注释
================================================================================

通过为构造函数的参数添加访问限定符，参数属性同时创建了构造函数参数和类成员。例如，如下的构造函数

.. code-block:: typescript

    class Foo {
        constructor(private readonly bar: Bar) { }
    }

为 ``Foo`` 类创建了 ``Bar`` 类型的成员 ``bar`` 。

如果要为这些成员添加文档，应使用 JSDoc 的 ``@param`` 注释，这样编辑器会在调用构造函数和访问属性时显示对应的文档描述信息。

.. code-block:: typescript

    /** 这个类演示了如何为参数属性添加文档 */
    class ParamProps {
        /**
         * @param percolator 煮咖啡所用的咖啡壶。
         * @param beans 煮咖啡所用的咖啡豆。
         */
        constructor(
            private readonly percolator: Percolator,
            private readonly beans: CoffeeBean[]) {}
    }


.. code-block:: typescript

    /** 这个类演示了如何为普通成员添加文档 */
    class OrdinaryClass {
        /** 下次调用 brew() 时所用的咖啡豆。 */
        nextBean: CoffeeBean;

        constructor(initialBean: CoffeeBean) {
            this.nextBean = initialBean;
        }
    }

.. _ts-comments-when-calling-a-function:

函数调用注释
================================================================================

如果有需要，可以在函数的调用点使用行内的 ``/* 块注释 */`` 为参数添加文档，或者使用字面量对象为参数添加名称并在函数声明中进行解构。注释的格式和位置没有明确的规定。

.. code-block:: typescript

    // 使用行内块注释为难以理解的参数添加说明：
    new Percolator().brew(/* amountLitres= */ 5);

    // 或者使用字面量对象为参数命名，并在函数 brew 的声明中将参数解构：
    new Percolator().brew({amountLitres: 5});


.. code-block:: typescript

    /** 一个古老的咖啡壶 {@link CoffeeBrewer} */
    export class Percolator implements CoffeeBrewer {
        /**
         * 煮咖啡。
         * @param amountLitres 煮咖啡的量，注意必须和煮锅的尺寸对应！
         */
        brew(amountLitres: number) {
            // 这个实现煮出来的咖啡味道差极了，不管了。
            // TODO(b/12345): 优化煮咖啡的过程。
        }
    }

.. _ts-place-documentation-prior-to-decorators:

将文档置于装饰器之前
================================================================================

文档、方法或者属性如果同时具有装饰器（例如 ``@Component``）和 JSDoc 注释，应当将 JSDoc 置于装饰器之前。

禁止将 JSDoc 置于装饰器和被装饰的对象之间。

.. code-block:: typescript

    // 不要这样做！JSDoc 被放在装饰器 @Component 和类 FooComponent 中间了！
    @Component({
        selector: 'foo',
        template: 'bar',
    })
    /** 打印 "bar" 的组件。 */
    export class FooComponent {}

应当将 JSDoc 置于装饰器之前。

.. code-block:: typescript

    /** 打印 "bar" 的组件。 */
    @Component({
        selector: 'foo',
        template: 'bar',
    })
    export class FooComponent {}
