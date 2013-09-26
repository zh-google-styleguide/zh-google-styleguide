整体的元数据规则
===================

编码
---------

使用UTF-8无BOM编码。

让你的编辑器使用无字节顺序标记的UTF-8编码。

在HTML模板和文档中使用 ``<meta charset=”utf-8”>`` 指定编码。不需要为样式表指定编码，它默认是UTF-8。

（想了解更多关于应该何时并如何指定编码，请查看 `Handling character encodings in HTML and CSS <http://www.w3.org/International/tutorials/tutorial-char-enc/>`_）

注释
--------

在需要时尽可能去解释你的代码。

用注释去解释你的代码，包括它的应用范围、用途、此方案的选择理由等。

（这一条是可选的，没必要为每个文件写上详细的注释，会增重HTML/CSS的代码，主要取决于项目的复杂度。）

处理内容
----------

用TODO标记待办事宜和处理内容。

只用TODO来标记待办事宜，不要使用其他格式，例如@@。

在括号里添加联系方式（姓名或邮箱），格式为TODO（联系方式）。

在冒号后面添加处理内容，格式为TODO：处理内容。

.. code-block:: html

  {# TODO(john.doe): 重新处理水平居中 #}
  <center>Test</center>
  
  <!-- TODO: 移除可选的标签 -->
  <ul>
   <li>Apples</li>
   <li>Oranges</li>
  </ul>
