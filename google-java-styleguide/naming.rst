5. 命名
----------------

5.1. 所有标识符通用的规则
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

标识符只使用ASCII字母、数字以及在下面提到的极少数情况中才会使用的下划线。因此，每个有效的标识符名称都应与正则表达式 ``\w+`` 匹配。

在Google风格中， **不** 使用特殊的前缀或后缀。例如，以下都不是Google风格的命名： ``name_`` ， ``mName`` ， ``s_name`` 和 ``kName`` 。

5.2. 不同类型标识符的规则
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

5.2.1. 包名
""""""""""""""""""""""""""""""""""""""""""""""""""

包名只使用小写字母和数字（不使用下划线）。连续的单词直接连接在一起。例如 ``com.example.deepspace`` ，而不是 ``com.example.deepSpace`` 或 ``com.example.deep_space`` 。

.. _class-names:

5.2.2. 类名
""""""""""""""""""""""""""""""""""""""""""""""""""

类名使用 :ref:`大驼峰命名法（UpperCamelCase） <camel-case>` 。

类名通常是名词或名词短语。例如 ``Character`` 、 ``ImmutableList`` 。接口名称也可能是名词或名词短语（例如 ``List`` ），但有时可能是形容词或形容词短语（例如 ``Readable`` ）。

对于注解的命名，至今还没有具体的规则，甚至也没有任何不成文的规定。

测试类的名称以 ``Test`` 结尾，例如， ``HashIntegrationTest`` 。如果它覆盖一个单一的类，其名称是该类的名称后加上 ``Test``，例如 ``HashImplTest`` 。

5.2.3. 方法名
""""""""""""""""""""""""""""""""""""""""""""""""""

方法名使用 :ref:`小驼峰命名法（lowerCamelCase） <camel-case>` 。

方法名通常是动词或动词短语。例如 ``sendMessage`` 、 ``stop`` 。

在JUnit测试方法名中，可以使用下划线来分隔名称的逻辑组件，每个组件都使用 :ref:`小驼峰命名法 <camel-case>` 编写，例如 ``transferMoney_deductsFromSource`` 。命名测试方法没有唯一正确的方式。

5.2.4. 常量字段名
""""""""""""""""""""""""""""""""""""""""""""""""""

常量名使用 ``UPPER_SNAKE_CASE`` （大蛇式）：全部为大写字母，每个单词之间用单个下划线分隔。但是，什么才算是一个常量呢？

常量是指那些由 ``static final`` 修饰的字段，其内容是深度不可变（译者注：指该对象以及其内部所有可能的引用或对象都是不可变的，与“浅层不可变”相对）的，且其方法不会产生可检测到的副作用。例子包括基本数据类型、字符串、不可变的值类和设置为 ``null`` 的任何东西。如果实例的任何可观察状态可以被改变，那它就不是一个常量。仅有不改变对象的意图是不够的。例如：

.. code-block:: java

    // Constants
    static final int NUMBER = 5;
    static final ImmutableList<String> NAMES = ImmutableList.of("Ed", "Ann");
    static final Map<String, Integer> AGES = ImmutableMap.of("Ed", 35, "Ann", 32);
    static final Joiner COMMA_JOINER = Joiner.on(','); // because Joiner is immutable
    static final SomeMutableType[] EMPTY_ARRAY = {};

    // Not constants
    static String nonFinal = "non-final";
    final String nonStatic = "non-static";
    static final Set<String> mutableCollection = new HashSet<String>();
    static final ImmutableSet<SomeMutableType> mutableElements = ImmutableSet.of(mutable);
    static final ImmutableMap<String, SomeMutableType> mutableValues =
        ImmutableMap.of("Ed", mutableInstance, "Ann", mutableInstance2);
    static final Logger logger = Logger.getLogger(MyClass.getName());
    static final String[] nonEmptyArray = {"these", "can", "change"};

常量名通常是名词或名词短语。

5.2.5. 非常量字段名
""""""""""""""""""""""""""""""""""""""""""""""""""

非常量字段名，无论其是否为静态的，都使用 :ref:`小驼峰命名法 <camel-case>` 格式编写。

非常量字段名通常是名词或名词短语。例如， ``computedValues`` 或 ``index`` 。

5.2.6. 参数名
""""""""""""""""""""""""""""""""""""""""""""""""""

参数名使用 :ref:`小驼峰命名法 <camel-case>` 格式编写。

公共（ ``public``）方法中应避免使用单字符参数名。

5.2.7. 局部变量名
""""""""""""""""""""""""""""""""""""""""""""""""""

局部变量名使用 :ref:`小驼峰命名法 <camel-case>` 格式编写。

即使是 final 且不可变的，局部变量也不被视为常量，因此不应按常量的风格命名。

5.2.8. 类型变量名
""""""""""""""""""""""""""""""""""""""""""""""""""

每个类型变量的命名方式有两种：

- 单个大写字母，后面可选择性地跟一个数字（如 ``E`` , ``T`` , ``X`` , ``T2`` ）

- 按照类的命名方式命名（参见第5.2.2节，:ref:`类名 <class-names>`），然后跟一个大写字母 ``T`` （例如： ``RequestT`` , ``FooBarT`` ）。

.. _camel-case:

5.3. 驼峰命名法：明确规定
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

有时将英文短语转换为驼峰命名有多种合理的方式，例如当存在缩略词或如"IPv6"或"iOS"这样不寻常的结构时。为了提高可预测性，Google风格指定了以下的（几乎）明确的规定。

从名称的口头表达开始：

- 1. 将短语转换为纯ASCII并去除所有的撇号。例如，“Müller's algorithm”可能变为“Muellers algorithm”。

- 2. 将这个结果分割为单词，以空格和任何剩余的标点符号（通常是连字符）为分隔。

    - 推荐：如果任何单词在常见用法中已经有一个传统的驼峰命名形式，那么将其分割成其组成部分（例如，"AdWords"变为"ad words"）。注意，像"iOS"这样的单词并不真的是驼峰命名，实际上它违反了任何惯例，所以这个建议不再适用。

- 3. 现在将所有内容（包括缩略词）全部转为小写，然后只将：

    - ... 每个单词的第一个字母大写，得到大驼峰命名，或

    - ... 除第一个单词外的每个单词的第一个字母大写，得到小驼峰命名

- 4. 最后，将所有的单词连接成一个标识符。

注意，原始单词的大小写几乎完全被忽略。示例：

============================================================ ============================================================ ============================================================
 口头表达                                                      正确形式                                                       错误形式                   
============================================================ ============================================================ ============================================================
 "XML HTTP request"                                            ``XmlHttpRequest``                                            ``XMLHTTPRequest``
 "new customer ID"                                             ``newCustomerId``                                             ``newCustomerID``
 "inner stopwatch"                                             ``innerStopwatch``                                            ``innerStopWatch``
 "supports IPv6 on iOS?"                                       ``supportsIpv6OnIos``                                         ``supportsIPv6OnIOS``
 "YouTube importer"                                            ``YouTubeImporter`` 、 ``YoutubeImporter`` *
============================================================ ============================================================ ============================================================

\*可以接受，但不推荐。

.. tip::

    **注意：** 在英文中，有些单词的连字符使用是模糊的：例如，“nonempty”和“non-empty”都是正确的，因此方法名 ``checkNonempty`` 和 ``checkNonEmpty`` 同样都是正确的。

