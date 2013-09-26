HTML格式规则
==============

常规格式化
------------

对每个块、列表、表格元素都另起一行，每个子元素都缩进。

每个块元素、列表元素或表格元素另起一行，而不必考虑元素的样式（因CSS可以改变元素的 ``display`` 属性）。

同样的，如果他们是块、列表或者表格元素的子元素，则将之缩进。

（如果你遇到列表项之间有空白的问题，可以把所有 ``li`` 元素放到一行。Linter鼓励抛出警告而不是错误。）

.. code-block:: html

  <blockquote>
    <p><em>Space</em>, the final frontier.</p>
  </blockquote>
  
  <ul>
    <li>Moe
    <li>Larry
    <li>Curly
  </ul>
  
  <table>
    <thead>
      <tr>
        <th scope="col">Income
        <th scope="col">Taxes
    <tbody>
      <tr>
        <td>$ 5.00
        <td>$ 4.50
  </table>

HTML引号
-----------

当引用属性值时，使用双引号。

使用双引号而不是单引号来包裹属性值。

.. code-block:: html

  <!-- 不推荐 -->
  <a class='maia-button maia-button-secondary'>Sign in</a>
  
  <!-- 推荐 -->
  <a class="maia-button maia-button-secondary">Sign in</a>
