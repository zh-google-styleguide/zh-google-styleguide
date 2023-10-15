6. 编程习惯
----------------

6.1  ``@Override`` ：始终使用
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

只要合法，方法就应使用 ``@Override`` 注解进行标记。这包括一个类方法覆盖一个超类方法，一个类方法实现一个接口方法，以及一个接口方法重新指定一个超接口方法的情况。

**例外：** 当父方法被 ``@Deprecated`` 标记时，可以省略 ``@Override`` 。

6.2. 捕获的异常：不应忽略
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

除了以下特别提到的情况，响应捕获的异常时什么也不做是非常少见的做法。（典型的响应是记录它，或者如果认为它是"不可能的"则将其重新抛出为 ``AssertionError`` 。）

当在 ``catch`` 块中确实合适地不采取任何行动时，应在注释中解释这样做的原因。

.. code-block:: java

    try {
        int i = Integer.parseInt(response);
        return handleNumericResponse(i);
    } catch (NumberFormatException ok) {
        // it's not numeric; that's fine, just continue
    }
    return handleTextResponse(response);

**例外：** 在测试中，如果捕获的异常的名称是或以 ``expected`` 开头的，则可以在不进行注释的情况下忽略它。以下是一个确保测试中的代码抛出预期类型的异常的非常常见的习语，所以这里不需要注释。

.. code-block:: java

    try {
        emptyStack.pop();
        fail();
    } catch (NoSuchElementException expected) {
    }

6.3. 静态成员：使用类名进行限定
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

当必须对静态类成员进行限定时，应使用该类的名称进行限定，而不是使用该类的类型引用或表达式进行限定。

.. code-block:: java

    Foo aFoo = ...;
    Foo.aStaticMethod(); // 好
    aFoo.aStaticMethod(); // 差
    somethingThatYieldsAFoo().aStaticMethod(); // 非常差

6.4. 析构方法：不使用
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
重写 ``Object.finalize`` 方法是 **极其罕见** 的。

.. tip::

    **提示：** 不要这样做。如果你确实必须这样做，首先仔细阅读并理解 `《Effective Java》第8条 <https://www.google.com/search?hl=zh-CN&tbo=p&tbm=bks&q=isbn:0134686047>`_ ："避免使用析构方法和清理器"，然后还是不要这样做。