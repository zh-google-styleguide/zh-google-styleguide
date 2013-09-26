CSS格式化规则
===============

声明顺序
---------

按字母顺序排列声明。

css文件书写按字母顺序排列的方式，容易记忆和维护，以达到一致的代码。

在排序时忽略浏览器特定的前缀。但是，特定CSS属性的多个浏览器前缀应按字母顺序排列（如-moz书写在-webkit前面）。

.. code-block:: css

  background: fuchsia;
  border: 1px solid;
  -moz-border-radius: 4px;
  -webkit-border-radius: 4px;
  border-radius: 4px;
  color: black;
  text-align: center;
  text-indent: 2em;

块内容的缩进
--------------

缩进块内容。

将包括嵌套及声明的 `块内容 <http://www.w3.org/TR/CSS21/syndata.html#block>`_ 进行缩进，以体现层次并提高可读性。

.. code-block:: css

  @media screen, projection {
  
    html {
      background: #fff;
      color: #444;
    }
  
  }

声明结束
----------   
   
每个属性后使用分号结束。

以分号结束每个属性，提高一致性和可扩展性。

.. code-block:: css

  /* 不推荐 */
  .test {
    display: block;
    height: 100px
  }
  
  /* 推荐 */
  .test {
    display: block;
    height: 100px;
  }

CSS属性名结束
---------------   
   
属性名称的冒号后有一个空格。

为保证一致性，在属性名与属性值之间添加一个空格（但是属性名和冒号间没有空格）。

.. code-block:: css

  /* 不推荐 */
  h3 {
    font-weight:bold;
  }
  
  /* 推荐 */
  h3 {
    font-weight: bold;
  }

声明块间隔
--------------
   
在选择器和后面的声明块之间使用一个空格。

最后一个选择器与表示 `声名块 <http://www.w3.org/TR/CSS21/syndata.html#rule-sets>`_ 开始的左大花括号在同行，中间有一个字符空格。
   
表示开始的左大花括号和选择器在同行。

.. code-block:: css

  /* 不推荐：缺少空间 */
  #video{
    margin-top: 1em;
  }
  
  
  /* 不推荐：不必要的换行符 */
  #video
  {
    margin-top: 1em;
  }
  
  /* 推荐 */
  #video {
    margin-top: 1em;
  }


选择器及声明分离
-------------------   
   
每个选择器和声明独立成行。

总是让每个选择器和声明单独成行。

.. code-block:: css

  /* 不推荐 */
  a:focus, a:active {
    position: relative; top: 1px;
  }
  
  /* 推荐 */
  h1,
  h2,
  h3 {
    font-weight: normal;
    line-height: 1.2;
  }


CSS代码块分离
-----------------   
   
使用新空行分离规则。

始终把一个空行（两个换行符）放在代码块规则之间。

.. code-block:: css

  html {
    background: #fff;
  }
  
  
  body {
    margin: auto;
    width: 50%;
  }

CSS引号
----------   

属性选择器和属性值中使用单引号。
   
在属性选择器及属性值中使用单引号（''）而不是双引号（""）。在 ``url（）`` 中不要使用引号。

特例：如果你确实需要定义 ``@charset`` ，由于 `不允许使用单引号 <http://www.w3.org/TR/CSS21/syndata.html#charset>`_ ，故请使用双引号。

.. code-block:: css

  /* 不推荐 */
  @import url("//www.google.com/css/maia.css");
  
  html {
    font-family: "open sans", arial, sans-serif;
  }
  
  /* 推荐 */
  @import url(//www.google.com/css/maia.css);
  
  html {
    font-family: 'open sans', arial, sans-serif;
  }
