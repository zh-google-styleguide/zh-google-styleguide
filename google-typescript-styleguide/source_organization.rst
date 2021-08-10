代码管理
################################################################################

.. _ts-modules:

模块
********************************************************************************

.. _import-paths:

导入路径
================================================================================

TypeScript 代码必须使用路径进行导入。这里的路径既可以是相对路径，以 ``.`` 或 ``..`` 开头，也可以是从项目根目录开始的绝对路径，如 ``root/path/to/file`` 。

在引用逻辑上属于同一项目的文件时，应使用相对路径 ``./foo`` ，不要使用绝对路径 ``path/to/foo`` 。 

应尽可能地限制父层级的数量（避免出现诸如 ``../../../`` 的路径），过多的层级会导致模块和路径结构难以理解。

.. code-block:: typescript

    import {Symbol1} from 'google3/path/from/root';
    import {Symbol2} from '../parent/file';
    import {Symbol3} from './sibling';

.. _namespaces-vs-modules:

用 命名空间 还是 模块？
================================================================================

在 TypeScript 有两种组织代码的方式：命名空间（namespace）和模块（module）。

不允许使用命名空间，在 TypeScript 中必须使用模块（即 `ES6 模块 <http://exploringjs.com/es6/ch_modules.html>`_ ）。也就是说，在引用其它文件中的代码时必须以 ``import {foo} from 'bar'`` 的形式进行导入和导出。

不允许使用 ``namespace Foo { ... }`` 的形式组织代码。命名空间只能在所用的外部第三方库有要求时才能使用。如果需要在语义上对代码划分命名空间，应当通过分成不同文件的方式实现。

不允许在导入时使用 ``require`` 关键字（形如 ``import x = require('...');`` ）。应当使用 ES6 的模块语法。

.. code-block:: typescript

    // 不要这样做！不要使用命名空间！
    namespace Rocket {
        function launch() { ... }
    }

    // 不要这样做！不要使用 <reference> ！
    /// <reference path="..."/>

    // 不要这样做！不要使用 require() ！
    import x = require('mydep');

.. tip::

    TypeScript 的命名空间早期也被称为内部模块并使用 ``module`` 关键字，形如 ``module Foo { ... }`` 。不要使用这种用法。任何时候都应当使用 ES6 的导入语法。

.. _ts-exports:

导出
********************************************************************************

代码中必须使用具名的导出声明。

.. code-block:: typescript

    // Use named exports:
    export class Foo { ... }

不要使用默认导出，这样能保证所有的导入语句都遵循统一的范式：

.. code-block:: typescript

    // 不要这样做！不要使用默认导出！
    export default class Foo { ... }

为什么？因为默认导出并不为被导出的符号提供一个标准的名称，这增加了维护的难度和降低可读性的风险，同时并未带来明显的益处。如下面的例子所示：

.. code-block:: typescript

    // 默认导出会造成如下的弊端
    import Foo from './bar';  // 这个语句是合法的。
    import Bar from './bar';  // 这个语句也是合法的。

具名导出的一个优势是，当代码中试图导入一个并未被导出的符号时，这段代码会报错。例如，假设在 ``foo.ts`` 中有如下的导出声明：

.. code-block:: typescript

    // 不要这样做！
    const foo = 'blah';
    export default foo;

如果在 ``bar.ts`` 中有如下的导入语句：

.. code-block:: typescript

    // 编译错误！
    import {fizz} from './foo';

会导致编译错误： ``error TS2614: Module '"./foo"' has no exported member 'fizz'`` 。反之，如果在 ``bar.ts`` 中的导入语句为：

.. code-block:: typescript

    // 不要这样做！这定义了一个多余的变量 fizz！
    import fizz from './foo';

结果是 ``fizz === foo`` ，这往往不符合预期，且难以调试。

此外，默认导出会鼓励程序员将所有内容全部置于一个巨大的对象当中，这个对象实际上充当了命名空间的角色：

.. code-block:: typescript

    // 不要这样做！
    export default class Foo {
        static SOME_CONSTANT = ...
        static someHelpfulFunction() { ... }
        ...
    }

显然，这个文件中具有文件作用域，它可以被用做命名空间。但是，这里创建了第二个作用域——类 ``Foo`` ，这个类在其它文件中具有歧义：它既可以被视为类型，又可以被视为值。

因此，我们应当使用文件作用域作为实质上的命名空间，同时使用具名的导出声明：

.. code-block:: typescript

    // 应当这样做！
    export const SOME_CONSTANT = ...
    export function someHelpfulFunction()
    export class Foo {
        // 只有类 Foo 中的内容
    }

.. _ts-export-visibility:

导出可见性
================================================================================

TypeScript 不支持限制导出符号的可见性。因此，不要导出不用于模块以外的符号。一般来说，应当尽量减小模块的外部 API 的规模。

.. _ts-mutable-exports:

可变导出
================================================================================

虽然技术上可以实现，但是可变导出会造成难以理解和调试的代码，尤其是对于在多个模块中经过了多次重新导出的符号。这条规则的一个例子是，不允许使用 ``export let`` 。

.. code-block:: typescript

    // 不要这样做！
    export let foo = 3;
    // 在纯 ES6 环境中，变量 foo 是一个可变值，导入了 foo 的代码会观察到它的值在一秒钟之后发生了改变。
    // 在 TypeScript 中，如果 foo 被另一个文件重新导出了，导入该文件的代码则不会观察到变化。
    window.setTimeout(() => {
        foo = 4;
    }, 1000 /* ms */);

如果确实需要允许外部代码对可变值进行访问，应当提供一个显式的取值器。

.. code-block:: typescript

    // 应当这样做！
    let foo = 3;
    window.setTimeout(() => {
        foo = 4;
    }, 1000 /* ms */);
    // 使用显式的取值器对可变导出进行访问。
    export function getFoo() { return foo; };

有一种常见的编程情景是，要根据某种特定的条件从两个值中选取其中一个进行导出：先检查条件，然后导出。这种情况下，应当保证模块中的代码执行完毕后，导出的结果就是确定的。

.. code-block:: typescript

    function pickApi() {
        if (useOtherApi()) return OtherApi;
        return RegularApi;
    }
    export const SomeApi = pickApi();


.. _ts-container-classes:

容器类
================================================================================

不要为了实现命名空间创建含有静态方法或属性的容器类。
    
.. code-block:: typescript
    
    // 不要这样做！
    export class Container {
        static FOO = 1;
        static bar() { return 1; }
    }

应当将这些方法和属性设为单独导出的常数和函数。

.. code-block:: typescript
    
    // 应当这样做！
    export const FOO = 1;
    export function bar() { return 1; }
