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

因此，应当使用文件作用域作为实质上的命名空间，同时使用具名的导出声明：

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

.. _ts-imports-source-organization:

导入
********************************************************************************

在 ES6 和 TypeScript 中，导入语句共有四种变体：

======================================== ======================================== ========================================
导入类型                                                    示例                                     用途
======================================== ======================================== ========================================
模块                                       ``import * as foo from '...';``           TypeScript 导入方式
解构                                       ``import {SomeThing} from '...';``        TypeScript 导入方式
默认                                       ``import SomeThing from '...';``          只用于外部代码的特殊需求
副作用                                      ``import '...';``                         只用于加载某些库的副作用（例如自定义元素）
======================================== ======================================== ========================================

.. code-block:: typescript

    // 应当这样做！从这两种变体中选择较合适的一种（见下文）。
    import * as ng from '@angular/core';
    import {Foo} from './foo';

    // 只在有需要时使用默认导入。
    import Button from 'Button';

    // 有时导入某些库是为了其代码执行时的副作用。
    import 'jasmine';
    import '@polymer/paper-button';

.. _ts-module-versus-destructuring-imports:

选择模块导入还是解构导入？
================================================================================

根据使用场景的不同，模块导入和解构导入分别有其各自的优势。

虽然模块导入语句中出现了通配符 ``*`` ，但模块导入并不能因此被视为其它语言中的通配符导入。相反地，模块导入语句为整个模块提供了一个名称，模块中的所有符号都通过这个名称进行访问，这为代码提供了更好的可读性，同时令模块中的所有符号可以进行自动补全。模块导入减少了导入语句的数量（模块中的所有符号都可以使用），降低了命名冲突的出现几率，同时还允许为被导入的模块提供一个简洁的名称。在从一个大型 API 中导入多个不同的符号时，模块导入语句尤其有用。

解构导入语句则为每一个被导入的符号提供一个局部的名称，这样在使用被导入的符号时，代码可以更简洁。对那些十分常用的符号，例如 Jasmine 的 ``describe`` 和 ``it`` 来说，这一点尤其有用。

.. code-block:: typescript

    // 不要这样做！无意义地使用命名空间中的名称使得导入语句过于冗长。
    import {TableViewItem, TableViewHeader, TableViewRow, TableViewModel,
    TableViewRenderer} from './tableview';
    let item: TableViewItem = ...;

.. code-block:: typescript

    // 应当这样做！使用模块作为命名空间。
    import * as tableview from './tableview';
    let item: tableview.Item = ...;

.. code-block:: typescript

    import * as testing from './testing';

    // 所有的测试都只会重复地使用相同的三个函数。
    // 如果只需要导入少数几个符号，而这些符号的使用频率又非常高的话，
    // 也可以考虑使用解构导入语句直接导入这几个符号（见下文）。
    testing.describe('foo', () => {
    testing.it('bar', () => {
        testing.expect(...);
        testing.expect(...);
    });
    });

.. code-block:: typescript

    // 这样做更好！为这几个常用的函数提供局部变量名。
    import {describe, it, expect} from './testing';

    describe('foo', () => {
    it('bar', () => {
        expect(...);
        expect(...);
    });
    });
    ...

.. _ts-renaming-imports:

重命名导入
================================================================================

在代码中，应当通过使用模块导入或重命名导出解决命名冲突。此外，在需要时，也可以使用重命名导入（例如 ``import {SomeThing as SomeOtherThing}`` ）。

在以下几种情况下，重命名导入可能较为有用：

1. 避免与其它导入的符号产生命名冲突。
2. 被导入符号的名称是自动生成的。
3. 被导入符号的名称不能清晰地描述其自身，需要通过重命名提高代码的可读性，如将 RxJS 的 ``from`` 函数重命名为 ``observableFrom`` 。

.. _ts-import-export-type:

``import type`` 和 ``export type``
================================================================================

不要使用 ``import type ... from`` 或者 ``export type ... from`` 。

.. tip::

    这一规则不适用于导出类型定义，如 ``export type Foo = ...;`` 。

.. code-block:: typescript

    // 不要这样做！
    import type {Foo} from './foo';
    export type {Bar} from './bar';

应当使用常规的导入语句。

.. code-block:: typescript

    // 应当这样做！
    import {Foo} from './foo';
    export {Bar} from './bar';

TypeScript 的工具链会自动区分用作类型的符号和用作值的符号。对于类型引用，工具链不会生成运行时加载的代码。这样做的原因是为了提供更好的开发体验，否则在 ``import type`` 和 ``import`` 之间反复切换会非常繁琐。同时， ``import type`` 并不提供任何保证，因为代码仍然可以通过其它的途径导入同一个依赖。

如果需要在运行时加载代码以执行其副作用，应使用 ``import '...'`` ，参见 :ref:`ts-imports-source-organization` 一节。

使用 ``export type`` 似乎可以避免将某个用作值的符号导出为 API。然而，和 ``import type`` 类似， ``export type`` 也不提供任何保证，因为外部代码仍然可以通过其它途径导入。如果需要拆分对 API 作为值的使用和作为类型的使用，并保证二者不被混用的话，应当显式地将其拆分成不同的符号，例如 ``UserService`` 和 ``AjaxUserService`` ，这样不容易造成错误，同时能更好地表达设计思路。

.. _ts-organize-by-feature:

根据特征组织代码
********************************************************************************

应当根据特征而非类型组织代码。例如，一个在线商城的代码应当按照 ``products`` ， ``checkout`` ， ``backend`` 等分类，而不是 ``views`` ， ``models`` ， ``controllers`` 。

