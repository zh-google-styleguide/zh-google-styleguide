类型系统
################################################################################

.. _ts-type-inference:

类型推导
********************************************************************************

对于所有类型的表达式（包括变量、字段、返回值，等等），都可以依赖 TypeScript 编译器所实现的类型推导。 google3 编译器会拒绝所有缺少类型记号又无法推导出其类型的代码，以保证所有的代码都具有类型（即使其中可能包括显式的 ``any`` 类型）。

.. code-block:: typescript

    const x = 15;  // x 的类型可以推导得出.

当变量或参数被初始化为 ``string`` ， ``number`` ， ``boolean`` ， ``RegExp`` 正则表达式字面量或 ``new`` 表达式时，由于明显能够推导出类型，因此应当省略类型记号。

.. code-block:: typescript

    // 不要这样做！添加 boolean 记号对提高可读性没有任何帮助！
    const x: boolean = true;

.. code-block:: typescript

    // 不要这样做！Set 类型显然可以从初始化语句中推导得出。
    const x: Set<string> = new Set();

.. code-block:: typescript
    
    // 应当这样做！依赖 TypeScript 的类型推导。
    const x = new Set<string>();


对于更为复杂的表达式，类型记号有助于提高代码的可读性。此时是否使用类型记号应当由代码审查员决定。

.. _ts-return-types:

返回类型
================================================================================

代码的作者可以自由决定是否在函数和方法中使用类型记号标明返回类型。代码审查员 *可以* 要求对难以理解的复杂返回类型使用类型记号进行阐明。项目内部 *可以* 自行规定必须标明返回值，本文作为一个通用的 TypeScript 风格指南，不做硬性要求。

显式地标明函数和方法的返回值有两个优点：

* 能够生成更精确的文档，有助于读者理解代码。
* 如果未来改变了函数的返回类型的话，可以让因此导致的潜在的错误更快地暴露出来。

.. _ts-null-vs-undefined:

Null 还是 Undefined ？
********************************************************************************

TypeScript 支持 ``null`` 和 ``undefined`` 类型。可空类型可以通过联合类型实现，例如 ``string | null`` 。对于 ``undefined`` 也是类似的。对于 ``null`` 和 ``undefined`` 的联合类型，并无特殊的语法。

TypeScript 代码中可以使用 ``undefined`` 或者 ``null`` 标记缺少的值，这里并无通用的规则约定应当使用其中的某一种。许多 JavaScript API 使用 ``undefined`` （例如 ``Map.get`` ），然而 DOM 和 Google API 中则更多地使用 ``null`` （例如 ``Element.getAttribute`` ），因此，对于 ``null`` 和 ``undefined`` 的选择取决于当前的上下文。

.. _ts-nullable-undefined-type-aliases:

可空/未定义类型别名
================================================================================

*不允许* 为包括 ``|null`` 或 ``|undefined`` 的联合类型创建类型别名。这种可空的别名通常意味着空值在应用中会被层层传递，并且它掩盖了导致空值出现的源头。另外，这种别名也让类或接口中的某个值何时有可能为空变得不确定。

因此，代码 *必须* 在使用别名时才允许添加 ``|null`` 或者 ``|undefined`` 。同时，代码 *应当* 在空值出现位置的附近对其进行处理。

.. code-block:: typescript

    // 不要这样做！不要在创建别名的时候包含 undefined ！
    type CoffeeResponse = Latte|Americano|undefined;

    class CoffeeService {
        getLatte(): CoffeeResponse { ... };
    }

.. code-block:: typescript

    // 应当这样做！在使用别名的时候联合 undefined ！
    type CoffeeResponse = Latte|Americano;

    class CoffeeService {
        getLatte(): CoffeeResponse|undefined { ... };
    }


.. code-block:: typescript

    // 这样做更好！使用断言对可能的空值进行处理！
    type CoffeeResponse = Latte|Americano;

    class CoffeeService {
        getLatte(): CoffeeResponse {
            return assert(fetchResponse(), 'Coffee maker is broken, file a ticket');
        };
    }

.. _ts-optionals-vs-undefined-type:

可选参数 还是 ``undefined`` 类型？
================================================================================

TypeScript 支持使用 ``?`` 创建可选参数和可选字段，例如：

.. code-block:: typescript

    interface CoffeeOrder {
        sugarCubes: number;
        milk?: Whole|LowFat|HalfHalf;
    }

    function pourCoffee(volume?: Milliliter) { ... }


可选参数实际上隐式地向类型中联合了 ``|undefined`` 。不同之处在于，在构造类实例或调用方法时，可选参数可以被直接省略。例如， ``{sugarCubes: 1}`` 是一个合法的 ``CoffeeOrder`` ，因为 ``milk`` 字段是可选的。

应当使用可选字段（对于类或者接口）和可选参数而非联合 ``|undefined`` 类型。

对于类，应当尽可能避免使用可选字段，尽可能初始化每一个字段。

.. code-block:: typescript

    class MyClass {
        field = '';
    }

.. _ts-structural-types-vs-nominal-types:

结构类型 与 指名类型
********************************************************************************

TypeScript 的类型系统使用的是结构类型而非指名类型。具体地说，一个值，如果它拥有某个类型的所有属性，且所有属性的类型能够递归地一一匹配，则这个值与这个类型也是匹配的。

在代码中，可以在适当的场景使用结构类型。具体地说，在测试代码之外，应当使用接口而非类对结构类型进行定义。在测试代码中，由于经常要创建 Mock 对象用于测试，此时不引入额外的接口往往较为方便。

在提供基于结构类型的实现时，应当在符号的声明位置显式地包含其类型，使类型检查和错误检测能够更准确地工作。

.. code-block:: typescript

    // 应当这样做！
    const foo: Foo = {
        a: 123,
        b: 'abc',
    }

.. code-block:: typescript

    // 不要这样做！
    const badFoo = {
        a: 123,
        b: 'abc',
    }

为什么要这样做？

这是因为在上文中， ``badFoo`` 对象的类型依赖于类型推导。 ``badFoo`` 对象中可能添加额外的字段，此时类型推导的结果就有可能发生变化。

如果将 ``badFoo`` 传给接收 ``Foo`` 类型参数的函数，错误提示会出现在函数调用的位置，而非对象声明的位置。在大规模的代码仓库中修改接口时，这一点区别会很重要。

.. code-block:: typescript

    interface Animal {
        sound: string;
        name: string;
    }

    function makeSound(animal: Animal) {}

    /**
     * 'cat' 的类型会被推导为 '{sound: string}'
     */
    const cat = {
        sound: 'meow',
    };

    /**
     * 'cat' 的类型并不满足函数参数的要求，
     * 因此 TypeScript 编译器会在这里报错，
     * 而这里有可能离 'cat' 的定义相当远。
     */
    makeSound(cat);

    /**
     * Horse 具有结构类型，因此这里会提示类型错误，而函数调用点不会报错。
     * 这是因为 'horse' 不满足接口 'Animal' 的类型约定。
     */
    const horse: Animal = {
        sound: 'niegh',
    };

    const dog: Animal = {
        sound: 'bark',
        name: 'MrPickles',
    };

    makeSound(dog);
    makeSound(horse);

.. _ts-interface-vs-type-aliases:

接口 还是 类型别名？
********************************************************************************

TypeScript 支持使用 `类型别名 <https://www.typescriptlang.org/docs/handbook/advanced-types.html#type-aliases>`_ 为类型命名。这一功能可以用于基本类型、联合类型、元组以及其它类型。

然而，当需要声明用于对象的类型时，应当使用接口，而非对象字面量表达式的类型别名。

.. code-block:: typescript

    // 应当这样做！
    interface User {
        firstName: string;
        lastName: string;
    }

.. code-block:: typescript

    // 不要这样做！
    type User = {
        firstName: string,
        lastName: string,
    }

为什么？

这两种形式是几乎等价的，因此，基于从两个形式中只选择其中一种以避免项目中出现变种的原则，这里选择了更常见的接口形式。另外，这里选择接口还有一个 `有趣的技术原因 <https://ncjamieson.com/prefer-interfaces/>`_ 。这篇博文引用了 TypeScript 团队负责人的话：“老实说，我个人的意见是对于任何可以建模的对象都应当使用接口。相比之下，使用类型别名没有任何优势，尤其是类型别名有许多的显示和性能问题”。

.. _ts-array-type:

``Array<T>`` 类型
********************************************************************************

对于简单类型（名称中只包含字母、数字和点 ``.`` 的类型），应当使用数组的语法糖 ``T[]`` ，而非更长的 ``Array<T>`` 形式。

对于其它复杂的类型，则应当使用较长的 ``Array<T>`` 。

这条规则也适用于 ``readonly T[]`` 和 ``ReadonlyArray<T>`` 。

.. code-block:: typescript

    // 应当这样做！
    const a: string[];
    const b: readonly string[];
    const c: ns.MyObj[];
    const d: Array<string|number>;
    const e: ReadonlyArray<string|number>;

.. code-block:: typescript

    // 不要这样做！
    const f: Array<string>;            // 语法糖写法更短。
    const g: ReadonlyArray<string>;
    const h: {n: number, s: string}[]; // 大括号和中括号让这行代码难以阅读。
    const i: (string|number)[];
    const j: readonly (string|number)[];

.. _ts-indexable-type:

索引类型 ``{[key: string]: number}``
********************************************************************************

在 JavaScript 中，使用对象作为关联数组（又称“映射表”、“哈希表”或者“字典”）是一种常见的做法：

.. code-block:: typescript

    const fileSizes: {[fileName: string]: number} = {};
    fileSizes['readme.txt'] = 541;

在 TypeScript 中，应当为键提供一个有意义的标签名。（当然，这个标签只有在文档中有实际意义，在其它场合是无用的。）

.. code-block:: typescript

    // 不要这样做！
    const users: {[key: string]: number} = ...;

.. code-block:: typescript

    // 应当这样做！
    const users: {[userName: string]: number} = ...;

然而，相比使用上面的这种形式，在 TypeScript 中应当考虑使用 ES6 新增的 ``Map`` 与 ``Set`` 类型。因为 JavaScript 对象有一些 `令人困惑又不符合预期的行为 <http://2ality.com/2012/01/objects-as-maps.html>`_ ，而 ES6 的新增类型能够更明确地表达程序员的设计思路。此外， ``Map`` 类型的键和 ``Set`` 类型的元素都允许使用 ``string`` 以外的其他类型。

TypeScript 内建的 ``Record<Keys, ValueType>`` 允许使用已定义的一组键创建类型。它与关联数组的不同之处在于键是静态确定的。关于它的使用建议，参见 :ref:`ts-mapped-conditional-types` 一节。

.. _ts-mapped-conditional-types:

映射类型与条件类型
********************************************************************************

TypeScript 中的 `映射类型 <https://www.typescriptlang.org/docs/handbook/advanced-types.html#mapped-types>`_ 与 `条件类型 <https://www.typescriptlang.org/docs/handbook/advanced-types.html#conditional-types>`_ 让程序员能够在已有类型的基础上构建出新的类型。在 TypeScript 的标准库中有许多类型运算符都是基于这一机制（例如 ``Record`` 、 ``Partial`` 、 ``Readonly`` 等等）。

TypeScript 类型系统的这一特性让创建新类型变得简洁，还程序员在设计代码抽象时，既能实现强大的功能，同时海能保证类型安全。然而，它们也有一些缺点：

* 相较于显式地指定属性与类型间关系（例如使用接口和继承，参见下文中的例子），类型运算符需要读者在头脑中自行对后方的类型表达式进行求值。本质上说，这增加了程序的理解难度，尤其是在类型推导和类型表达式有可能横跨数个文件的情况下。
* 映射类型与条件类型的求值模型并没有明确的规范，且经常随着 TypeScript 编译器的版本更新而发生变化，因此并不总是易于理解，尤其是与类型推导一同使用时。因此，代码有可能只是碰巧能够通过编译或者给出正确的结果。在这种情况下，使用类型运算符增加了代码未来的维护成本。
* 映射类型与条件类型最为强大之处在于，它们能够从复杂且/或推导的类型中派生出新的类型。然而从另一方面看，这样做也很容易导致程序难于理解与维护。
* 有些语法工具并不能够很好地支持类型系统的这一特性。例如，一些 IDE 的“查找引用”功能（以及依赖于它的“重命名重构”）无法发现位于 ``Pick<T, Keys>`` 类型中的属性，因而在查找结果中不会将其设为高亮。

因此，推荐的代码规范如下：

* 任何使用都应当使用最简单的类型构造方式进行表达。
* 一定程度的重复或冗余，往往好过复杂的类型表达式带来的长远维护成本。
* 映射类型和条件类型必须在符合上述理念的情况下使用。

例如，TypeScript 内建的 ``Pick<T, Keys>`` 类型允许以类型 ``T`` 的子集创建新的类型。然而，使用接口和继承的方式实现往往更易于理解。

.. code-block:: typescript

    interface User {
        shoeSize: number;
        favoriteIcecream: string;
        favoriteChocolate: string;
    }

    // FoodPreferences 类型拥有 favoriteIcecream 和 favoriteChocolate，但不包括 shoeSize。
    type FoodPreferences = Pick<User, 'favoriteIcecream'|'favoriteChocolate'>;

这种写法等价于显式地写出 ``FoodPreferences`` 的属性：

.. code-block:: typescript

    interface FoodPreferences {
        favoriteIcecream: string;
        favoriteChocolate: string;
    }

为了减少重复，可以让 ``User`` 继承 ``FoodPreferences`` ，或者在 ``User`` 中嵌套一个类型为 ``FoodPrefences`` 的字段（这样做可能更好）：

.. code-block:: typescript

    interface FoodPreferences { /* 同上 */ }

    interface User extends FoodPreferences {
        shoeSize: number;
        // 这样 User 也包括了 FoodPreferences 的字段。
    }

使用接口让属性的分类变得清晰，IDE 的支持更完善，方便进一步优化，同时使得代码更易于理解。

.. _ts-any-type:

``any`` 类型
********************************************************************************

TypeScript 的 ``any`` 类型是所有其它类型的超类，又是所有其它类型的子类，同时还允许解引用一切属性。因此，使用 ``any`` 十分危险——它会掩盖严重的程序错误，并且它从根本上破坏了对应的值“具有静态属性”的原则。

尽可能 *不要* 使用 ``any`` 。如果出现了需要使用 ``any`` 的场景，可以考虑下列的解决方案：

* :ref:`ts-provide-a-more-specific-type`
* :ref:`ts-using-unknown-over-any`
* :ref:`ts-suppress-the-lint-warning`

.. _ts-provide-a-more-specific-type:

提供一个更具体的类型
================================================================================

使用接口、内联对象类型、或者类型别名：

.. code-block:: typescript

    // 声明接口类型以表示服务端发送的 JSON。
    declare interface MyUserJson {
        name: string;
        email: string;
    }

    // 对重复出现的类型使用类型别名。
    type MyType = number|string;

    // 或者对复杂的返回类型使用内联对象类型。
    function getTwoThings(): {something: number, other: string} {
        // ...
        return {something, other};
    }

    // 使用泛型，有些库在这种情况下可能会使用 any 表示
    // 这里并不考虑函数所作用于的参数类型。
    // 注意，对于这种写法，“只有泛型的返回类型”一节有更详细的规范。
    function nicestElement<T>(items: T[]): T {
        // 在 items 中查找最棒的元素。
        // 这里还可以进一步为泛型参数 T 添加限制，例如 <T extends HTMLElement>。
    }

.. _ts-using-unknown-over-any:

使用 ``unknown`` 而非 ``any``
================================================================================

``any`` 类型的值可以赋给其它任何类型，还可以对其解引用任意属性。一般来说，这个行为不是必需的，也不符合期望，此时代码试图表达的内容其实是“该类型是未知的”。在这种情况下，应当使用内建的 ``unknown`` 类型。它能够表达相同的语义，并且，因为 ``unknown`` 不能解引用任意属性，它较 ``any`` 而言更为安全。

.. code-block:: typescript

    // 应当这样做！
    // 可以将任何值（包括 null 和 undefined）赋给 val，
    // 但在缩窄类型或者类型转换之前并不能使用它。
    const val: unknown = value;

.. code-block:: typescript

    // 不要这样做！
    const danger: any = value /* 这是任意一个表达式的结果 */;
    danger.whoops();  // 完全未经检查的访问！

.. _ts-suppress-the-lint-warning:

关闭 Lint 工具对 ``any`` 的警告
================================================================================

有时使用 ``any`` 是合理的，例如用于在测试中构造 Mock 对象。在这种情况下，应当添加注释关闭 Lint 工具对此的警告，并添加文档对使用 any 的合理性进行说明。

.. code-block:: typescript

    // 这个测试只需要部分地实现 BookService，否则测试会失败。
    // 所以，这里有意地使用了一个不安全的部分实现 Mock 对象。
    // tslint:disable-next-line:no-any
    const mockBookService = ({get() { return mockBook; }} as any) as BookService;
    // 购物车在这个测试里并未使用。
    // tslint:disable-next-line:no-any
    const component = new MyComponent(mockBookService, /* unused ShoppingCart */ null as any);

.. _ts-tuple-types:

元组类型
********************************************************************************

应当使用元组类型代替常见的 ``Pair`` 类型的写法：

.. code-block:: typescript

    // 不要这样做！
    interface Pair {
        first: string;
        second: string;
    }

    function splitInHalf(input: string): Pair {
        // ...
        return {first: x, second: y};
    }

.. code-block:: typescript

    // 应当这样做！
    function splitInHalf(input: string): [string, string] {
        // ...
        return [x, y];
    }

    // 这样使用:
    const [leftHalf, rightHalf] = splitInHalf('my string');

然而通常情况下，为属性提供一个有意义的名称往往能让代码更加清晰。

如果为此声明一个接口过于繁重的话，可以使用内联对象字面量类型：

.. code-block:: typescript

    function splitHostPort(address: string): {host: string, port: number} {
        // ...
    }

    // 这样使用:
    const address = splitHostPort(userAddress);
    use(address.port);

    // 也可以使用解构进行形如元组的操作：
    const {host, port} = splitHostPort(userAddress);

.. _ts-wrapper-types:

包装类型
********************************************************************************

不要使用如下几种类型，它们是 JavaScript 中基本类型的包装类型：

* ``String`` 、 ``Boolean`` 和 ``Number`` 。它们的含义和对应的基本类型 ``string`` 、 ``boolean`` 和 ``number`` 略有不同。任何时候，都应当使用后者。
* ``Object`` 。它和 ``{}`` 与 ``object`` 类似，但包含的范围略微更大。应当使用 ``{}`` 表示“包括除 ``null`` 和 ``undefined`` 之外所有类型”的类型，使用 ``object`` 表示“所有基本类型以外”的类型（这里的“所有基本类型”包括上文中提到的基本类型， ``symbol`` 和 ``bigint`` ）。

此外，不要将包装类型用作构造函数。

.. _ts-return-type-only-generics:

只有泛型的返回类型
********************************************************************************

不要创建返回类型只有泛型的 API。如果现有的 API 中存在这种情况，使用时应当显式地标明泛型参数类型。

