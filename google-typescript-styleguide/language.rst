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

关于可见性，还可参见 `导出可见性 </gsg-ts-ch03#导出可见性>`_ 一节。

构造函数
--------

调用构造函数时必须使用括号，即使不传递任何参数。

.. code-block:: typescript

   // 不要这样做！
   const x = new Foo;

   // 应当这样做！
   const x = new Foo();

根据 ES2015 标准，如果在类中并未显式地声明构造函数，则编译器会提供一个默认的构造函数。因此，没有必要为类提供一个空构造函数，或者简单地调用基类的构造函数。但是，如果构造函数中含有参数属性、访问限定符或者参数装饰器，即使函数体是空的也不能省略。

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

类成员
------

``#private`` 语法
^^^^^^^^^^^^^^^^^^^^^

禁止使用 ``#private`` 私有字段（又称私有标识符）语法声明私有成员。

.. code-block:: typescript

   // 不要这样做！
   class Clazz {
     #ident = 1;
   }

而应当使用 TypeScript 的访问修饰符。

.. code-block:: typescript

   // 应该这样做！
   class Clazz {
     private ident = 1;
   }

为什么？因为私有字段语法会导致 TypeScipt 在编译为 JavaScript 时出现体积和性能问题。同时，ES2015 之前的标准都不支持私有字段语法，因此它限制了 TypeScript 最低只能被编译至 ES2015。另外，在进行静态类型和可见性检查时，私有字段语法相比访问修饰符并无明显优势。

使用 ``readonly``
^^^^^^^^^^^^^^^^^^^^^

对于不会在构造函数以外进行赋值的属性，应使用 ``readonly`` 修饰符标记。这些属性并不需要具有深层不可变性。

参数属性
^^^^^^^^

不要在构造函数中显式地对类成员进行初始化。应当使用 TypeScript 的参数属性语法。

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

如果需要为参数属性添加文档，应使用 JSDoc 的 ``@param`` 标签，参见“第 1 章：语法规范”中 `参数属性注释 </gsg-ts-ch00#参数属性注释>`_ 一节。

字段初始化
^^^^^^^^^^

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

用于类的词法范围之外的属性
^^^^^^^^^^^^^^^^^^^^^^^^^^

如果一个属性被用于它们所在类的词法范围之外，例如用于模板（template）的 AngularJS 控制器（controller）属性，则禁止将其设为 ``private``\ ，因为显然这些属性是用于外部的。

对于这类属性，应当将其设为 ``public``\ ，如果有需要的话也可以使用 ``protected``\ 。例如，Angular 和 Polymer 的模板属性应使用 ``public``\ ，而 AngularJS 应使用 ``protected``\ 。

此外，禁止在 TypeScript 代码中使用 ``obj['foo']`` 语法绕过可见性限制进行访问。

为什么？

如果一个属性被设为 ``private``\ ，就相当于向自动化工具和读者声明对这个属性的访问局限于类的内部。例如，用于查找未使用代码的工具可能会将一个私有属性标记为未使用，即使在其它文件中有代码设法绕过了可见性限制对其进行访问。

虽然 ``obj['foo']`` 可以绕过 TypeScript 编译器对可见性的检查，但是这种访问方法可能会由于调整了构建规则而失效。此外，它也违反了后文中所提到的 `兼容性优化 <#兼容性优化>`_ 规则。

取值器与设值器（存取器）
^^^^^^^^^^^^^^^^^^^^^^^^

可以在类中使用存取器，其中取值器方法必须是纯函数（即结果必须是一致的，且函数不能有副作用）。存取器还可以用于隐藏内部复杂的实现细节。

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

原始类型与封装类
----------------

在 TypeScript 中，不要实例化原始类型的封装类，例如 ``String``\ 、\ ``Boolean``\ 、\ ``Number`` 等。封装类有许多不合直觉的行为，例如 ``new Boolean(false)`` 在布尔表达式中会被求值为 ``true``\ 。

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

数组构造函数
------------

在 TypeScript 中，禁止使用 ``Array()`` 构造函数。它有许多不合直觉又彼此矛盾的行为，例如：

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

强制类型转换
------------

在 TypeScript 中，可以使用 ``String()`` 和 ``Boolean()`` 函数（注意不能使用 ``new``\ ！）、模板字符串和 ``!!`` 运算符进行强制类型转换。

.. code-block:: typescript

   const bool = Boolean(false);
   const str = String(aNumber);
   const bool2 = !!str;
   const str2 = `result: ${bool2}`;

不建议通过字符串连接操作将类型强制转换为 ``string``\ ，这会导致加法运算符两侧的运算对象具有不同的类型。

在将其它类型转换为数字时，必须使用 ``Number()`` 函数，并且，在类型转换有可能失败的场合，必须显式地检查其返回值是否为 ``NaN``\ 。

**注意**\ ：\ ``Number('')``\ 、\ ``Number(' ')`` 和 ``Number('\t')`` 返回 ``0`` 而不是 ``NaN``\ 。\ ``Number('Infinity')`` 和 ``Number('-Infinity')`` 分别返回 ``Infinity`` 和 ``-Infinity``\ 。这些情况可能需要特殊处理。

.. code-block:: typescript

   const aNumber = Number('123');
   if (isNaN(aNumber)) throw new Error(...);  // 如果输入字符串有可能无法被解析为数字，就需要处理返回 NaN 的情况。
   assertFinite(aNumber, ...);                // 如果输入字符串已经保证合法，可以在这里添加断言。

禁止使用一元加法运算符 ``+`` 将字符串强制转换为数字。用这种方法进行解析有失败的可能，还有可能出现奇怪的边界情况。而且，这样的写法往往成为代码中的坏味道，\ ``+`` 在代码审核中非常容易被忽略掉。

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

应当使用 ``Number()`` 和 ``Math.floor`` 或者 ``Math.trunc``\ （如果支持的话）解析整数。

.. code-block:: typescript

   let f = Number(someString);
   if (isNaN(f)) handleError();
   f = Math.floor(f);

不要在 ``if``\ 、\ ``for`` 或者 ``while`` 的条件语句中显式地将类型转换为 ``boolean``\ ，因为这里原本就会执行隐式的类型转换。

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

最后，在代码中可以使用显式的比较。

.. code-block:: typescript

   // 显式地和 0 进行比较，没问题！
   if (arr.length > 0) {...}
   // 依赖隐式类型转换，也没问题！
   if (arr.length) {...}

变量
----

必须使用 ``const`` 或 ``let`` 声明变量。尽可能地使用 ``const``\ ，除非这个变量需要被重新赋值。禁止使用 ``var``\ 。

.. code-block:: typescript

   const foo = otherValue;  // 如果 foo 不可变，就使用 const。
   let bar = someValue;     // 如果 bar 在之后会被重新赋值，就使用 let。

与大多数其它编程语言相同，使用 ``const`` 和 ``let`` 声明的变量都具有块级作用域。与之相反的是，使用 ``var`` 声明的变量在 JavaScript 中具有函数作用域，这会造成许多难以理解的 bug，因此禁止在 TypeScript 中使用 ``var``\ 。

.. code-block:: typescript

   var foo = someValue;     // 不要这么做！

最后，变量必须先声明再使用。

异常
----

在实例化异常对象时，必须使用 ``new Error()`` 语法而非调用 ``Error()`` 函数。虽然这两种方法都能够创建一个异常实例，但是使用 ``new`` 能够与代码中其它的对象实例化在形式上保持更好的一致性。

.. code-block:: typescript

   // 应当这样做！
   throw new Error('Foo is not a valid bar.');

   // 不要这样做！
   throw Error('Foo is not a valid bar.');

对象迭代
--------

对对象使用 ``for (... in ...)`` 语法进行迭代很容易出错，因为它同时包括了对象从原型链中继承得来的属性。因此，禁止使用裸的 ``for (... in ...)`` 语句。

.. code-block:: typescript

   // 不要这样做！
   for (const x in someObj) {
     // x 可能包括 someObj 从原型中继承得到的属性。
   }

在对对象进行迭代时，必须使用 ``if`` 语句对对象的属性进行过滤，或者使用 ``for (... of Object.keys(...))``\ 。

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

容器迭代
--------

禁止在数组上使用 ``for (... in ...)`` 进行迭代。这是一个违反直觉的操作，它对数组的下标而非元素进行迭代，还会将其强制转换为 ``string`` 类型！

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

禁止使用 ``Array.prototype.forEach``\ 、\ ``Set.prototype.forEach`` 和 ``Map.prototype.forEach``\ 。这些方法会使代码难以调试，还会令编译器的某些检查（例如可见性检查）失效。

.. code-block:: typescript

   // 不要这样做！
   someArr.forEach((item, index) => {
     someFn(item, index);
   });

为什么？考虑下面这段代码：

.. code-block:: typescript

   let x: string|null = 'abc';
   myArray.forEach(() => { x.charAt(0); });

从读者的角度看，这段代码并没有什么问题：\ ``x`` 没有被初始化为 ``null``\ ，并且在被访问之前也没有发生过任何变化。但是对编译器而言，它并不知道传给 ``.forEach()`` 的闭包 ``() => { x.charAt(0); }`` 会被立即执行，它有可能在之后的某处代码中被调用，而到那时 ``x`` 有可能已经被设为 ``null``\ 。这里因此出现了一个编译错误。与之等价的 ``for-of`` 形式的迭代就不会有任何问题。

读者可以在 `这里 <https://www.typescriptlang.org/play?#code/DYUwLgBAHgXBDOYBOBLAdgcwD5oK7GAgF4IByAQwCMBjUgbgCgBtAXQDoAzAeyQFFzqACwAUwgJTEAfBADeDCNDZDySAIJhhABjGMAvjoYNQkAJ5xEqTDnyESFGvQbckEYdS5pEEAPoQuHCFYJOQUTJUEVdS0DXQYgA>`_ 对比这两个版本的代码。

在工程实践中，代码路径越复杂、越违背直觉，越容易在进行控制流分析时出现这类问题。

展开运算符
----------

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

禁止展开原始类型，包括 ``null`` 和 ``undefined``\ 。

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
