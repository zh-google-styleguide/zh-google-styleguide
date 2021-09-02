语言特性
################################################################################

.. _ts-visibility:

可见性
********************************************************************************

限制属性、方法以及类型的可见性有助于代码解耦合。因此：

* 应当尽可能限制符号的可见性。
* 可以将私有方法在同一文件中改写为独立于所有类以外的内部函数，并将私有属性移至单独的内部类中。
* 在 TypeScript 中，符号默认的可见性即为 ``public`` ，因此，除了在构造函数中声明公开（ ``public`` ）且非只读（ ``readonly`` ）的参数属性之外，不要使用 ``public`` 修饰符。

.. code-block:: typescript

    class Foo {
        public bar = new Bar();  // 不要这样做！不需要 public 修饰符！

        constructor(public readonly baz: Baz) {}  // 不要这样做！readonly 修饰符已经表明了 baz 是默认 public 的属性，因此不需要 public 修饰符！
    }

.. code-block:: typescript

    class Foo {
        bar = new Bar();  // 应当这样做！将不需要的 public 修饰符省略！

        constructor(public baz: Baz) {}  // 可以这样做！公开且非只读的参数属性允许使用 public 修饰符！
    }

关于可见性，还可参见 :ref:`ts-export-visibility` 一节。

.. _ts-constructors:

构造函数
********************************************************************************

调用构造函数时必须使用括号，即使不传递任何参数。

.. code-block:: typescript

   // 不要这样做！
   const x = new Foo;

   // 应当这样做！
   const x = new Foo();

没有必要提供一个空的或者仅仅调用父类构造函数的构造函数。在 ES2015 标准中，如果没有为类显式地提供构造函数，编译器会提供一个默认的构造函数。但是，含有参数属性、访问修饰符或参数装饰器的构造函数即使函数体为空也不能省略。

.. code-block:: typescript

    // 不要这样做！没有必要声明一个空的构造函数！
    class UnnecessaryConstructor {
        constructor() {}
    }

.. code-block:: typescript

    // 不要这样做！没有必要声明一个仅仅调用基类构造函数的构造函数！
    class UnnecessaryConstructorOverride extends Base {
        constructor(value: number) {
            super(value);
        }
    }

.. code-block:: typescript

    // 应当这样做！默认构造函数由编译器提供即可！
    class DefaultConstructor {
    }

    // 应当这样做！含有参数属性的构造函数不能省略！
    class ParameterProperties {
        constructor(private myService) {}
    }

    // 应当这样做！含有参数装饰器的构造函数不能省略！
    class ParameterDecorators {
        constructor(@SideEffectDecorator myService) {}
    }

    // 应当这样做！私有的构造函数不能省略！
    class NoInstantiation {
        private constructor() {}
    }

.. _ts-class-members:

类成员
********************************************************************************

.. _ts-no-private-fields:

``#private`` 语法
================================================================================

不要使用 ``#private`` 私有字段（又称私有标识符）语法声明私有成员。

.. code-block:: typescript

    // 不要这样做！
    class Clazz {
        #ident = 1;
    }

而应当使用 TypeScript 的访问修饰符。

.. code-block:: typescript

    // 应当这样做！
    class Clazz {
        private ident = 1;
    }

为什么？因为私有字段语法会导致 TypeScipt 在编译为 JavaScript 时出现体积和性能问题。同时，ES2015 之前的标准都不支持私有字段语法，因此它限制了 TypeScript 最低只能被编译至 ES2015。另外，在进行静态类型和可见性检查时，私有字段语法相比访问修饰符并无明显优势。

.. _ts-use-readonly:

使用 ``readonly``
================================================================================

对于不会在构造函数以外进行赋值的属性，应使用 ``readonly`` 修饰符标记。这些属性并不需要具有深层不可变性。

参数属性
================================================================================

不要在构造函数中显式地对类成员进行初始化。应当使用 TypeScript 的 `参数属性 <https://www.typescriptlang.org/docs/handbook/classes.html#parameter-properties>`_ 语法。

.. code-block:: typescript

    // 不要这样做！重复的代码太多了！
    class Foo {
        private readonly barService: BarService;

        constructor(barService: BarService) {
            this.barService = barService;
        }
    }

.. code-block:: typescript

    // 应当这样做！简洁明了！
    class Foo {
        constructor(private readonly barService: BarService) {}
    }

如果需要为参数属性添加文档，应使用 JSDoc 的 ``@param`` 标签，参见 :ref:`ts-parameter-property-comments` 一节。

字段初始化
================================================================================

如果某个成员并非参数属性，应当在声明时就对其进行初始化，这样有时可以完全省略掉构造函数。

.. code-block:: typescript

    // 不要这样做！没有必要单独把初始化语句放在构造函数里！
    class Foo {
        private readonly userList: string[];
        constructor() {
            this.userList = [];
        }
    }

.. code-block:: typescript

    // 应当这样做！省略了构造函数！
    class Foo {
        private readonly userList: string[] = [];
    }

.. _ts-properties-used-outside-of-class-lexical-scope:

用于类的词法范围之外的属性
================================================================================

如果一个属性被用于它们所在类的词法范围之外，例如用于模板（template）的 AngularJS 控制器（controller）属性，则禁止将其设为 ``private`` ，因为显然这些属性是用于外部的。

对于这类属性，应当将其设为 ``public`` ，如果有需要的话也可以使用 ``protected`` 。例如，Angular 和 Polymer 的模板属性应使用 ``public`` ，而 AngularJS 应使用 ``protected`` 。

此外，禁止在 TypeScript 代码中使用 ``obj['foo']`` 语法绕过可见性限制进行访问。

为什么？

如果一个属性被设为 ``private``\ ，就相当于向自动化工具和读者声明对这个属性的访问局限于类的内部。例如，用于查找未被使用的代码的工具可能会将一个私有属性标记为未使用，即使在其它文件中有代码设法绕过了可见性限制对其进行访问。

虽然 ``obj['foo']`` 可以绕过 TypeScript 编译器对可见性的检查，但是这种访问方法可能会由于调整了构建规则而失效。此外，它也违反了后文中所提到的 :ref:`ts-optimization-compatibility-for-property-access` 规则。

.. _ts-getters-and-setters-accessors:

取值器与设值器（存取器）
================================================================================

可以在类中使用存取器，其中取值器方法必须是纯函数（即结果必须是一致稳定的，且不能有副作用）。存取器还可以用于隐藏内部复杂的实现细节。

.. code-block:: typescript

    class Foo {
        constructor(private readonly someService: SomeService) {}

        get someMember(): string {
            return this.someService.someVariable;
        }

        set someMember(newValue: string) {
            this.someService.someVariable = newValue;
        }
    }

如果存取器被用于隐藏类内部的某个属性，则被隐藏的属性应当以诸如 ``internal`` 或 ``wrapped`` 此类的完整单词作为前缀或后缀。在使用这些私有属性时，应当尽可能地通过存取器进行访问。取值器和设值器二者至少要有一个是非平凡的，也就是说，存取器不能只用于传递属性值，更不能依赖这种存取器对属性进行隐藏。这种情况下，应当直接将属性设为 ``public``\ 。对于只有取值器没有设值器的属性，则应当考虑直接将其设为 ``readonly``\ 。

.. code-block:: typescript

    class Foo {
        private wrappedBar = '';
        get bar() {
            return this.wrappedBar || 'bar';
        }

        set bar(wrapped: string) {
            this.wrappedBar = wrapped.trim();
        }
    }

.. code-block:: typescript

    class Bar {
        private barInternal = '';
        // 不要这样做！取值器和设值器都没有任何逻辑，这种情况下应当直接将属性 bar 设为 public。
        get bar() {
            return this.barInternal;
        }

        set bar(value: string) {
            this.barInternal = value;
        }
    }

.. _ts-primitive-types-wrapper-classes:

原始类型与封装类
********************************************************************************

在 TypeScript 中，不要实例化原始类型的封装类，例如 ``String`` 、 ``Boolean`` 、 ``Number`` 等。封装类有许多不合直觉的行为，例如 ``new Boolean(false)`` 在布尔表达式中会被求值为 ``true``\ 。

.. code-block:: typescript

    // 不要这样做！
    const s = new String('hello');
    const b = new Boolean(false);
    const n = new Number(5);

.. code-block:: typescript

    // 应当这样做！
    const s = 'hello';
    const b = false;
    const n = 5;

.. _ts-array-constructor:

数组构造函数
********************************************************************************

在 TypeScript 中，禁止使用 ``Array()`` 构造函数（无论是否使用 ``new`` 关键字）。它有许多不合直觉又彼此矛盾的行为，例如：

.. code-block:: typescript

    // 不要这样做！同样的构造函数，其构造方式却却完全不同！
    const a = new Array(2); // 参数 2 被视作数组的长度，因此返回的结果是 [undefined, undefined]
    const b = new Array(2, 3); // 参数 2, 3 被视为数组中的元素，返回的结果此时变成了 [2, 3]

应当使用方括号对数组进行初始化，或者使用 ``from`` 构造一个具有确定长度的数组：

.. code-block:: typescript

    const a = [2];
    const b = [2, 3];

    // 等价于 Array(2)：
    const c = [];
    c.length = 2;

    // 生成 [0, 0, 0, 0, 0]
    Array.from<number>({length: 5}).fill(0);

.. _ts-type-coercion:

强制类型转换
********************************************************************************

在 TypeScript 中，可以使用 ``String()`` 和 ``Boolean()`` 函数（注意不能和 ``new`` 一起使用！）、模板字符串和 ``!!`` 运算符进行强制类型转换。

.. code-block:: typescript

    const bool = Boolean(false);
    const str = String(aNumber);
    const bool2 = !!str;
    const str2 = `result: ${bool2}`;

不建议通过字符串连接操作将类型强制转换为 ``string`` ，这会导致加法运算符两侧的运算对象具有不同的类型。

在将其它类型转换为数字时，必须使用 ``Number()`` 函数，并且，在类型转换有可能失败的场合，必须显式地检查其返回值是否为 ``NaN`` 。

.. tip::

    ``Number('')`` 、 ``Number(' ')`` 和 ``Number('\t')`` 返回 ``0`` 而不是 ``NaN`` 。 ``Number('Infinity')`` 和 ``Number('-Infinity')`` 分别返回 ``Infinity`` 和 ``-Infinity`` 。这些情况可能需要特殊处理。

.. code-block:: typescript

    const aNumber = Number('123');
    if (isNaN(aNumber)) throw new Error(...);  // 如果输入字符串有可能无法被解析为数字，就需要处理返回 NaN 的情况。
    assertFinite(aNumber, ...);                // 如果输入字符串已经保证合法，可以在这里添加断言。

禁止使用一元加法运算符 ``+`` 将字符串强制转换为数字。用这种方法进行解析有失败的可能，还有可能出现奇怪的边界情况。而且，这样的写法往往成为代码中的坏味道， ``+`` 在代码审核中非常容易被忽略掉。

.. code-block:: typescript

    // 不要这样做！
    const x = +y;

同样地，代码中也禁止使用 ``parseInt`` 或 ``parseFloat`` 进行转换，除非用于解析表示非十进制数字的字符串。因为这两个函数都会忽略字符串中的后缀，这有可能在无意间掩盖了一部分原本会发生错误的情形（例如将 ``12 dwarves`` 解析成 ``12``\ ）。

.. code-block:: typescript

    const n = parseInt(someString, 10);  // 无论传不传基数，
    const f = parseFloat(someString);    // 都很容易造成错误。

对于需要解析非十进制数字的情况，在调用 ``parseInt`` 进行解析之前必须检查输入是否合法。

.. code-block:: typescript

    if (!/^[a-fA-F0-9]+$/.test(someString)) throw new Error(...);
    // 需要解析 16 进制数。
    // tslint:disable-next-line:ban
    const n = parseInt(someString, 16);  // 只允许在非十进制的情况下使用 parseInt。

应当使用 ``Number()`` 和 ``Math.floor`` 或者 ``Math.trunc`` （如果支持的话）解析整数。

.. code-block:: typescript

    let f = Number(someString);
    if (isNaN(f)) handleError();
    f = Math.floor(f);

不要在 ``if`` 、 ``for`` 或者 ``while`` 的条件语句中显式地将类型转换为 ``boolean`` ，因为这里原本就会执行隐式的类型转换。

.. code-block:: typescript

    // 不要这样做！
    const foo: MyInterface|null = ...;
    if (!!foo) {...}
    while (!!foo) {...}

.. code-block:: typescript

    // 应当这样做！
    const foo: MyInterface|null = ...;
    if (foo) {...}
    while (foo) {...}

最后，在代码中使用显式和隐式的比较均可。

.. code-block:: typescript

   // 显式地和 0 进行比较，没问题！
   if (arr.length > 0) {...}

   // 依赖隐式类型转换，也没问题！
   if (arr.length) {...}

.. _ts-variables:

变量
********************************************************************************

必须使用 ``const`` 或 ``let`` 声明变量。尽可能地使用 ``const`` ，除非这个变量需要被重新赋值。禁止使用 ``var`` 。

.. code-block:: typescript

    const foo = otherValue;  // 如果 foo 不可变，就使用 const。
    let bar = someValue;     // 如果 bar 在之后会被重新赋值，就使用 let。

与大多数其它编程语言类似，使用 ``const`` 和 ``let`` 声明的变量都具有块级作用域。与之相反的是，使用 ``var`` 声明的变量在 JavaScript 中具有函数作用域，这会造成许多难以理解的 bug，因此禁止在 TypeScript 中使用 ``var`` 。

.. code-block:: typescript

    // 不要这么做！
    var foo = someValue;

最后，变量必须在使用前进行声明。

.. _ts-exceptions:

异常
********************************************************************************

在实例化异常对象时，必须使用 ``new Error()`` 语法而非调用 ``Error()`` 函数。虽然这两种方法都能够创建一个异常实例，但是使用 ``new`` 能够与代码中其它的对象实例化在形式上保持更好的一致性。

.. code-block:: typescript

    // 应当这样做！
    throw new Error('Foo is not a valid bar.');

    // 不要这样做！
    throw Error('Foo is not a valid bar.');

.. _ts-iterating-objects:

对象迭代
********************************************************************************

对对象使用 ``for (... in ...)`` 语法进行迭代很容易出错，因为它同时包括了对象从原型链中继承得来的属性。因此，禁止使用裸的 ``for (... in ...)`` 语句。

.. code-block:: typescript

    // 不要这样做！
    for (const x in someObj) {
        // x 可能包括 someObj 从原型中继承得到的属性。
    }

在对对象进行迭代时，必须使用 ``if`` 语句对对象的属性进行过滤，或者使用 ``for (... of Object.keys(...))`` 。

.. code-block:: typescript

    // 应当这样做！
    for (const x in someObj) {
        if (!someObj.hasOwnProperty(x)) continue;
        // 此时 x 必然是定义在 someObj 上的属性。
    }

.. code-block:: typescript

    // 应当这样做！
    for (const x of Object.keys(someObj)) { // 注意：这里使用的是 for _of_ 语法！
        // 此时 x 必然是定义在 someObj 上的属性。
    }

.. code-block:: typescript

    // 应当这样做！
    for (const [key, value] of Object.entries(someObj)) { // 注意：这里使用的是 for _of_ 语法！
        // 此时 key 必然是定义在 someObj 上的属性。
    }

.. _ts-iterating-containers:

容器迭代
********************************************************************************

不要在数组上使用 ``for (... in ...)`` 进行迭代。这是一个违反直觉的操作，因为它是对数组的下标而非元素进行迭代（还会将其强制转换为 ``string`` 类型）！

.. code-block:: typescript

    // 不要这样做！
    for (const x in someArray) {
        // 这里的 x 是数组的下标！(还是 string 类型的！)
    }

如果要在数组上进行迭代，应当使用 ``for (... of someArr)`` 语句或者传统的 ``for`` 循环语句。

.. code-block:: typescript

    // 应当这样做！
    for (const x of someArr) {
        // 这里的x 是数组的元素。
    }

.. code-block:: typescript

    // 应当这样做！
    for (let i = 0; i < someArr.length; i++) {
        // 如果需要使用下标，就对下标进行迭代，否则就使用 for/of 循环。
        const x = someArr[i];
        // ...
    }

.. code-block:: typescript

    // 应当这样做！
    for (const [i, x] of someArr.entries()) {
        // 上面例子的另一种形式。
    }

不要使用 ``Array.prototype.forEach`` 、 ``Set.prototype.forEach`` 和 ``Map.prototype.forEach`` 。这些方法会使代码难以调试，还会令编译器的某些检查（例如可见性检查）失效。

.. code-block:: typescript

    // 不要这样做！
    someArr.forEach((item, index) => {
        someFn(item, index);
    });

为什么？考虑下面这段代码：

.. code-block:: typescript

    let x: string|null = 'abc';
    myArray.forEach(() => { x.charAt(0); });

从读者的角度看，这段代码并没有什么问题： ``x`` 没有被初始化为 ``null`` ，并且在被访问之前也没有发生过任何变化。但是对编译器而言，它并不知道传给 ``.forEach()`` 的闭包 ``() => { x.charAt(0); }`` 会被立即执行。因此，编译器有理由认为闭包有可能在之后的某处代码中被调用，而到那时 ``x`` 已经被设为 ``null`` 。于是，这里出现了一个编译错误。与之等价的 ``for-of`` 形式的迭代就不会有任何问题。

读者可以在 `这里 <https://www.typescriptlang.org/play?#code/DYUwLgBAHgXBDOYBOBLAdgcwD5oK7GAgF4IByAQwCMBjUgbgCgBtAXQDoAzAeyQFFzqACwAUwgJTEAfBADeDCNDZDySAIJhhABjGMAvjoYNQkAJ5xEqTDnyESFGvQbckEYdS5pEEAPoQuHCFYJOQUTJUEVdS0DXQYgA>`_ 对比这两个版本的代码。

在工程实践中，代码路径越复杂、越违背直觉，越容易在进行控制流分析时出现这类问题。

.. _ts-using-the-spread-operator:

展开运算符
********************************************************************************

在复制数组或对象时，展开运算符 ``[...foo]``\ 、\ ``{...bar}`` 是一个非常方便的语法。使用展开运算符时，对于同一个键，后出现的值会取代先出现的值。

.. code-block:: typescript

    const foo = {
        num: 1,
    };

    const foo2 = {
        ...foo,
        num: 5,
    };

    const foo3 = {
        num: 5,
        ...foo,
    }

    // 对于 foo2 而言，1 先出现，5 后出现。
    foo2.num === 5;

    // 对于 foo3 而言，5 先出现，1 后出现。
    foo3.num === 1;

在使用展开运算符时，被展开的值必须与被创建的值相匹配。也就是说，在创建对象时只能展开对象，在创建数组时只能展开可迭代类型。

禁止展开原始类型，包括 ``null`` 和 ``undefined`` 。

.. code-block:: typescript

    // 不要这样做！
    const foo = {num: 7};
    const bar = {num: 5, ...(shouldUseFoo && foo)}; // 展开运算符有可能作用于 undefined。

.. code-block:: typescript

    // 不要这样做！这会创建出一个没有 length 属性的对象 {0: 'a', 1: 'b', 2: 'c'}。
    const fooStrings = ['a', 'b', 'c'];
    const ids = {...fooStrings};

.. code-block:: typescript

    // 应当这样做！在创建对象时展开对象。
    const foo = shouldUseFoo ? {num: 7} : {};
    const bar = {num: 5, ...foo};

    // 应当这样做！在创建数组时展开数组。
    const fooStrings = ['a', 'b', 'c'];
    const ids = [...fooStrings, 'd', 'e'];

.. _ts-control-flow-statements-blocks:

控制流语句 / 语句块
********************************************************************************

多行控制流语句必须使用大括号。

.. code-block:: typescript
    
    // 应当这样做！
    for (let i = 0; i < x; i++) {
        doSomethingWith(i);
        andSomeMore();
    }
    if (x) {
        doSomethingWithALongMethodName(x);
    }

.. code-block:: typescript

    // 不要这样做！
    if (x)
        x.doFoo();
    for (let i = 0; i < x; i++)
        doSomethingWithALongMethodName(i);

这条规则的例外时，能够写在同一行的 ``if`` 语句可以省略大括号。

.. code-block:: typescript
    
    // 可以这样做！
    if (x) x.doFoo();

.. _ts-switch-statements:

``switch`` 语句
********************************************************************************

所有的 ``switch`` 语句都必须包含一个 ``default`` 分支，即使这个分支里没有任何代码。

.. code-block:: typescript

    // 应当这样做！
    switch (x) {
        case Y:
            doSomethingElse();
            break;
        default:
            // 什么也不做。
    }

非空语句组（ ``case ...`` ）不允许越过分支向下执行（编译器会进行检查）：

.. code-block:: typescript

    // 不能这样做！
    switch (x) {
        case X:
            doSomething();
            // 不允许向下执行！
        case Y:
            // ...
    }

空语句组可以这样做：

.. code-block:: typescript

    // 可以这样做！
    switch (x) {
        case X:
        case Y:
            doSomething();
            break;
        default: // 什么也不做。
    }

.. _ts-equality-checks:

相等性判断
********************************************************************************

必须使用三等号（ ``===`` ）和对应的不等号（ ``!==`` ）。两等号会在比较的过程中进行类型转换，这非常容易导致难以理解的错误。并且在 JavaScript 虚拟机上，两等号的运行速度比三等号慢。参见 `JavaScript 相等表 <https://dorey.github.io/JavaScript-Equality-Table/>`_ 。

.. code-block:: typescript

    // 不要这样做！
    if (foo == 'bar' || baz != bam) {
        // 由于发生了类型转换，会导致难以理解的行为。
    }

.. code-block:: typescript

    // 应当这样做！
    if (foo === 'bar' || baz !== bam) {
        // 一切都很好！
    }

**例外**：和 ``null`` 字面量的比较可以使用 ``==`` 和 ``!=`` 运算符，这样能够同时覆盖 ``null`` 和 ``undefined`` 两种情况。

.. code-block:: typescript

    // 可以这样做！
    if (foo == null) {
        // 不管 foo 是 null 还是 undefined 都会执行到这里。
    }

.. _ts-function-declarations:

函数声明
********************************************************************************

使用 ``function foo() { ... }`` 的形式声明具名函数，包括嵌套在其它作用域中，例如其它函数内部的函数。

不要使用将函数表达式赋值给局部变量的写法（例如 ``const x = function() {...};`` ）。TypeScript 本身已不允许重新绑定函数，所以在函数声明中使用 ``const`` 来阻止重写函数是没有必要的。
    
**例外**：如果函数需要访问外层作用域的 ``this`` ，则应当使用将箭头函数赋值给变量的形式代替函数声明的形式。
    
.. code-blocK:: typescript
    
    // 应当这样做！
    function foo() { ... }

.. code-block:: typescript

    // 不要这样做！
    // 在有上一段代码中的函数声明的情况下，下面这段代码无法通过编译：
    foo = () => 3;  // 错误：赋值表达式的左侧不合法。
    
    // 因此像这样进行函数声明是没有必要的。
    const foo = function() { ... }

请注意这里所说的函数声明（ ``function foo() {}`` ）和下面要讨论的函数表达式（ ``doSomethingWith(function() {});`` ）之间的区别。

顶层箭头函数可以用于显式地声明这一函数实现了一个接口。

.. code-block:: typescript
    
    interface SearchFunction {
        (source: string, subString: string): boolean;
    }
    
    const fooSearch: SearchFunction = (source, subString) => { ... };

.. _ts-function-expressions:

函数表达式
********************************************************************************

.. _ts-use-arrow-functions-in-expressions:

在表达式中使用箭头函数
================================================================================

不要使用 ES6 之前使用 ``function`` 关键字定义函数表达式的版本。应当使用箭头函数。

.. code-block:: typescript

    // 应当这样做！
    bar(() => { this.doSomething(); })

.. code-block:: typescript

    // 不要这样做！
    bar(function() { ... })

只有当函数需要动态地重新绑定 ``this`` 时，才能使用 ``function`` 关键字声明函数表达式，但是通常情况下代码中不应当重新绑定 ``this`` 。常规函数（相对于箭头函数和方法而言）不应当访问 ``this`` 。

.. _ts-expression-bodies-vs-block-bodies:

表达式函数体 和 代码块函数体
================================================================================

使用箭头函数时，应当根据具体情况选择表达式或者代码块作为函数体。

.. code-block:: typescript

    // 使用函数声明的顶层函数。
    function someFunction() {
        // 使用代码块函数体的箭头函数，也就是使用 => { } 的函数，没问题：
        const receipts = books.map((b: Book) => {
            const receipt = payMoney(b.price);
            recordTransaction(receipt);
            return receipt;
        });

        // 如果用到了函数的返回值的话，使用表达式函数体也没问题：
        const longThings = myValues.filter(v => v.length > 1000).map(v => String(v));

        function payMoney(amount: number) {
            // 函数声明也没问题，但是不要在函数中访问 this。
        }
    }

只有在确实需要用到函数返回值的情况下才能使用表达式函数体。

.. code-block:: typescript

    // 不要这样做！如果不需要函数返回值的话，应当使用代码块函数体（{ ... }）。
    myPromise.then(v => console.log(v));

.. code-block:: typescript
    
    // 应当这样做！使用代码块函数体。
    myPromise.then(v => {
        console.log(v);
    });

    // 应当这样做！即使需要函数返回值，也可以为了可读性使用代码块函数体。
    const transformed = [1, 2, 3].map(v => {
        const intermediate = someComplicatedExpr(v);
        const more = acrossManyLines(intermediate);
        return worthWrapping(more);
    });

.. _ts-rebinding-this:

重新绑定 ``this``
================================================================================

不要在函数表达式中使用 ``this`` ，除非它们明确地被用于重新绑定 ``this`` 指针。大多数情况下，使用箭头函数或者显式指定函数参数都能够避免重新绑定 ``this`` 的需求。

.. code-block:: typescript

    // 不要这样做！
    function clickHandler() {
        // 这里的 this 到底指向什么？
        this.textContent = 'Hello';
    }

    // 不要这样做！this 指针被隐式地设为 document.body。
    document.body.onclick = clickHandler;

.. code-block:: typescript

    // 应当这样做！在箭头函数中显式地对对象进行引用。
    document.body.onclick = () => { document.body.textContent = 'hello'; };

    // 可以这样做！函数显式地接收一个参数。
    const setTextFn = (e: HTMLElement) => { e.textContent = 'hello'; };
    document.body.onclick = setTextFn.bind(null, document.body);

.. _ts-arrow-functions-as-properties:

使用箭头函数作为属性
================================================================================

通常情况下，类不应该将任何属性初始化为箭头函数。箭头函数属性需要调用函数意识到被调用函数的 ``this`` 已经被绑定了，这让 ``this`` 的指向变得令人费解，也让对应的调用和引用在形式上看着似乎是不正确的，也就是说，需要额外的信息才能确认这样的使用方式是正确的。在调用实例方法时，必须使用箭头函数的形式（例如 ``const handler = (x) => { this.listener(x); };`` ）。此外，不允许持有或传递实例方法的引用（例如不要使用 ``const handler = this.listener; handler(x);`` 的写法）。

.. tip::

    在一些特殊的情况下，例如需要将函数绑定到模板时，使用箭头函数作为属性是很有用的做法，同时还能令代码的可读性提高。因此，在这些情况下对于这条规则可视具体情况加以变通。此外， :ref:`ts-event-handlers` 一节中有相关讨论。

.. code-block:: typescript

    // 不要这样做！
    class DelayHandler {
        constructor() {
            // 这里有个问题，回调函数里的 this 指针不会被保存。
            // 因此回调函数里的 this 不再是 DelayHandler 的实例了。
            setTimeout(this.patienceTracker, 5000);
        }
        private patienceTracker() {
            this.waitedPatiently = true;
        }
    }

.. code-block:: typescript

    // 不要这样做！一般而言不应当使用箭头函数作为属性。
    class DelayHandler {
        constructor() {
            // 不要这样做！这里看起来就是像是忘记了绑定 this 指针。
            setTimeout(this.patienceTracker, 5000);
        }
        private patienceTracker = () => {
            this.waitedPatiently = true;
        }
    }

.. code-block:: typescript

    // 应当这样做！在调用时显式地处理 this 指针的指向问题。
    class DelayHandler {
        constructor() {
            // 在这种情况下，应尽可能使用匿名函数。
            setTimeout(() => {
                this.patienceTracker();
            }, 5000);
        }
        private patienceTracker() {
            this.waitedPatiently = true;
        }
    }

.. _ts-event-handlers:

事件句柄
================================================================================

对于事件句柄，如果它不需要被卸载的话，可以使用箭头函数的形式，例如事件是由类自身发送的情况。如果句柄必须被卸载，则应当使用箭头函数属性，因为箭头函数属性能够自动正确地捕获 ``this`` 指针，并且能够提供一个用于卸载的稳定引用。

.. code-block:: typescript

    // 应当这样做！事件句柄可以使用匿名函数或者箭头函数属性的形式。
    class Component {
        onAttached() {
            // 事件是由类本身发送的，因此这个句柄不需要卸载。
            this.addEventListener('click', () => {
                this.listener();
            });
            // 这里的 this.listener 是一个稳定引用，因此可以在之后被卸载。
            window.addEventListener('onbeforeunload', this.listener);
        }
        onDetached() {
            // 这个事件是由 window 发送的。如果不卸载这个句柄，this.listener 
            // 会因为绑定了 this 而保存对 this 的引用，从而导致内存泄漏。
            window.removeEventListener('onbeforeunload', this.listener);
        }
        // 使用箭头函数作为属性能够自动地正确绑定 this 指针。
        private listener = () => {
            confirm('Do you want to exit the page?');
        }
    }

不要在注册事件句柄的表达式中使用 ``bind`` ，这会创建一个无法卸载的临时引用。

.. code-block:: typescript

    // 不要这样做！对句柄使用 bind 会创建一个无法卸载的临时引用。
    class Component {
        onAttached() {
            // 这里创建了一个无法卸载的临时引用。
            window.addEventListener('onbeforeunload', this.listener.bind(this));
        }
        onDetached() {
            // 这里的 bind 创建了另一个引用，所以这一行代码实际上没有实现任何功能。
            window.removeEventListener('onbeforeunload', this.listener.bind(this));
        }
        private listener() {
            confirm('Do you want to exit the page?');
        }
    }

.. _ts-automatic-semicolon-insertion:

自动分号插入
********************************************************************************

不要依赖自动分号插入（ASI），必须显式地使用分号结束每一个语句。这能够避免由于不正确的分号插入所导致的 Bug，也能够更好地兼容对 ASI 支持有限的工具（例如 clang-format）。

.. _ts-ts-ignore:

``@ts-ignore``
********************************************************************************

不要使用 ``@ts-ignore`` 。表面上看，这是一个“解决”编译错误的简单方法，但实际上，编译错误往往是由其它更大的问题导致的，因此正确的做法是直接解决这些问题本身。

举例来说，如果使用 ``@ts-ignore`` 关闭了一个类型错误，那么便很难推断其它相关代码最终会接收到何种类型。对于许多与类型相关的错误， :ref:`ts-any-type` 一节有一些关于如何正确使用 ``any`` 的有用的建议。

.. _ts-type-and-non-nullability-assertions:

类型断言与非空断言
********************************************************************************

类型断言（ ``x as SomeType`` ）和非空断言（ ``y!`` ）是不安全的。这两种语法只能够绕过编译器，而并不添加任何运行时断言检查，因此有可能导致程序在运行时崩溃。

因此，除非有明显或确切的理由，否则 *不应* 使用类型断言和非空断言。

.. code-block:: typescript

    // 不要这样做！
    (x as Foo).foo();

    y!.bar();

如果希望对类型和非空条件进行断言，最好的做法是显式地编写运行时检查。

.. code-block:: typescript

    // 应当这样做！

    // 这里假定 Foo 是一个类。
    if (x instanceof Foo) {
        x.foo();
    }

    if (y) {
        y.bar();
    }

有时根据代码中的上下文可以确定某个断言必然是安全的。在这种情况下， *应当* 添加注释详细地解释为什么这一不安全的行为可以被接受：

.. code-block:: typescript

    // 可以这样做！

    // x 是一个 Foo 类型的示例，因为……
    (x as Foo).foo();

    // y 不可能是 null，因为……
    y!.bar();

如果使用断言的理由很明显，注释就不是必需的。例如，生成的协议代码总是可空的，但有时根据上下文可以确认其中某些特定的由后端提供的字段必然不为空。在这些情况下应当根据具体场景加以判断和变通。

.. _ts-type-assertions-syntax:

类型断言语法
================================================================================

类型断言必须使用 ``as`` 语法，不要使用尖括号语法，这样能强制保证在断言外必须使用括号。

.. code-block:: typescript

    // 不要这样做！
    const x = (<Foo>z).length;
    const y = <Foo>z.length;

.. code-block:: typescript

    // 应当这样做！
    const x = (z as Foo).length;

.. _ts-type-assertions-and-object-literals:

类型断言和对象字面量
================================================================================

使用类型标记（ ``: Foo`` ）而非类型断言（ ``as Foo`` ）标明对象字面量的类型。在日后对接口的字段类型进行修改时，前者能够帮助程序员发现 Bug。

.. code-block:: typescript

    interface Foo {
        bar: number;
        baz?: string;  // 这个字段曾经的名称是“bam”，后来改名为“baz”。
    }

    const foo = {
        bar: 123,
        bam: 'abc',  // 如果使用类型断言，改名之后这里并不会报错！
    } as Foo;

    function func() {
        return {
            bar: 123,
            bam: 'abc',  // 如果使用类型断言，改名之后这里也不会报错！
        } as Foo;
    }

.. _ts-member-property-declarations:

成员属性声明
********************************************************************************

接口和类的声明必须使用 ``;`` 分隔每个成员声明。

.. code-block:: typescript

    // 应当这样做！
    interface Foo {
        memberA: string;
        memberB: number;
    }

为了与类的写法保持一致，不要在接口中使用 ``,`` 分隔字段。

.. code-block:: typescript

    // 不要这样做！
    interface Foo {
        memberA: string,
        memberB: number,
    }

然而，内联对象类型声明必须使用 ``,`` 作为分隔符。

.. code-block:: typescript

    // 应当这样做！
    type SomeTypeAlias = {
        memberA: string,
        memberB: number,
    };

    let someProperty: {memberC: string, memberD: number};

.. _ts-optimization-compatibility-for-property-access:

优化属性访问的兼容性
================================================================================

不要混用方括号属性访问和句点属性访问两种形式。

.. code-block:: typescript

    // 不要这样做！
    // 必须从两种形式中选择其中一种，以保证整个程序的一致性。
    console.log(x['someField']);
    console.log(x.someField);

代码应当尽可能为日后的属性重命名需求进行优化，并且为所有程序外部的对象属性声明对应的字段。

.. code-block:: typescript

    // 应当这样做！声明一个对应的接口。
    declare interface ServerInfoJson {
        appVersion: string;
        user: UserJson;
    }
    const data = JSON.parse(serverResponse) as ServerInfoJson;
    console.log(data.appVersion); // 这里是类型安全的，如果需要重命名也是安全的！

.. _ts-optimization-compatibility-for-module-object-imports:

优化模块对象导入的兼容性
================================================================================

导入模块对象时应当直接访问对象上的属性，而不要传递对象本身的引用，以保证模块能够被分析和优化。也可以将导入的模块视作命名空间，参见 :ref:`ts-module-versus-destructuring-imports` 一节。

.. code-block:: typescript

    // 应当这样做！
    import {method1, method2} from 'utils';
    class A {
        readonly utils = {method1, method2};
    }

.. code-block:: typescript

    // 不要这样做！
    import * as utils from 'utils';
    class A {
        readonly utils = utils;
    }

.. _ts-optimization-exception:

例外情况
================================================================================

这里所提到的优化规则适用于所有的 Web 应用，但不需要强制应用于只运行在服务端的程序。不过，出于代码整洁性的考虑，这里仍然强烈建议声明所有的类型，并且避免混用两种属性访问的形式。

.. _ts-enums:

枚举
********************************************************************************

对于枚举类型，必须使用 ``enum`` 关键字，但不要使用 ``const enum`` 。TypeScript 的枚举类型本身就是不可变的， ``const enum`` 的写法是另一种独立的语言特性，其目的是让枚举对 JavaScript 程序员透明。

.. _ts-debugger-statements:

``debugger`` 语句
********************************************************************************

不允许在生产环境代码中添加 ``debugger`` 语句。

.. code-block:: typescript

    // 不要这样做！
    function debugMe() {
        debugger;
    }

.. _ts-decorators:

装饰器
********************************************************************************

装饰器以 ``@`` 为前缀，例如 ``@MyDecorator`` 。

不要定义新的装饰器，只使用框架中已定义的装饰器，例如：

* Angular（例如 ``@Component`` 、 ``@NgModule`` 等等）
* Polymer（例如 ``@property`` 等等）

为什么？

通常情况下，应当避免使用装饰器。这是由于装饰器是一个实验性功能，仍然处于 TC39 委员会的提案阶段，且目前存在已知的无法被修复的 Bug。

使用装饰器时，装饰器必须紧接被装饰的符号，中间不允许有空行。

.. code-block:: typescript

    /** JSDoc 注释应当位于装饰器之前 */
    @Component({...})  // 装饰器之后不能有空行。
    class MyComp {
        @Input() myField: string;  // 字段的装饰器和和字段位于同一行……

        @Input()
        myOtherField: string;  // ……或位于字段之前。
    }