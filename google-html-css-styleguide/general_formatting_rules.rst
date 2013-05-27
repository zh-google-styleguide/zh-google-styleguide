总体排版规则
==============

缩进
---------

每次缩进使用两个空格。

不使用TAB键或者混合使用TAB键和空格进行缩进。

.. code-block:: html

  <ul>
   <li>Fantastic
   <li>Great
  </ul>
  
.. code-block:: css

  .example {
   color: blue;
  }

大小写
----------

只使用小写字母。

所有的代码都使用小写字母：适用于HTML元素、属性、属性值（除了text/CDATA）、CSS选择器、属性名以及属性值（字符串除外）。

.. code-block:: html

  <!-- 不推荐 -->
  <A HREF="/">Home</A>
  
  <!-- 推荐 -->
  <img src="google.png" alt="Google">

.. code-block:: css

  /* 不推荐 */
  color: #E5E5E5;
  
  /* 推荐 */
  color: #e5e5e5;

尾部的空格
------------

删除尾部的空格。

尾部的空格是多余的，不删除则形成无意义的文件差异。

.. code-block:: html

  <!-- 不推荐 -->
  <p>What?_
  
  <!-- 推荐 -->
  <p>Yes please.
