HTML样式规则
==============

文档类型
---------

使用HTML5。

HTML5（HTML语法）是所有HTML文档的首选： ``<!DOCTYPE html>`` 。

（推荐使用HTML，即text/html。不要使用XHTML。XHTML，即 `application/xhtml+xml <http://hixie.ch/advocacy/xhtml>`_，缺乏浏览器和基础结构的支持，并且优化的空间比HTML小。）
虽然HTML闭合标签没有问题，但是不要自闭合空标签。即写 ``<br>`` 而不是 ``<br />`` 。


HTML合法性
------------

在可能的情况下使用合法的HTML。

使用合法的HTML代码，除非由于文件大小导致的不可达到的性能目标而不能使用。

利用已用工具对合法性进行测试，例如 `W3C HTML validator <http://validator.w3.org/nu/>`_。

使用合法的HTML是一个可度量的基准质量属性，该属性有助于了解技术需求和约束，从而确保合理的HTML使用。

.. code-block:: html

  <!-- 不推荐 -->
  <title>Test</title>
  <article>This is only a test.
  
  <!-- 推荐 -->
  <!DOCTYPE html>
  <meta charset="utf-8">
  <title>Test</title>
  <article>This is only a test.</article>

语义化
--------

根据HTML的目的使用它。

根据元素（有时被错误的叫做“标签”）被创造的用途使用他们。比如，对标题使用标题元素，对段落使用 ``p`` 元素，对锚点使用 ``a`` 元素等。

语义化的使用HTML对于可访问性、复用性和代码的高效性等因素非常重要。

.. code-block:: html

  <!-- 不推荐 -->
  <div onclick="goToRecommendations();">All recommendations</div>
  
  <!-- 推荐 -->
  <a href="recommendations/">All recommendations</a>

多媒体降级
------------

为多媒体提供替代内容。

对于图片、视频、通过 ``canvas`` 实现的动画等多媒体来说，确保提供可访问的替代内容。对于图片，可提供有意义的替代文本（ ``alt`` ）；对于视频和音频，如有条件可提供对白和字幕。

提供替代内容对辅助功能很重要：没有 ``alt`` ，一位盲人用户很难知道一张图片的内容，其他用户可能不能了解视频和音频的内容。
（对于 ``alt`` 属性会引起冗余的图片和你不打算添加CSS的纯粹装饰性的图片，不用添加替代文本，写成 ``alt=""`` 即可。）

.. code-block:: html

  <!-- 不推荐 -->
  <img src="spreadsheet.png">
  
  <!-- 推荐 -->
  <img src="spreadsheet.png" alt="Spreadsheet screenshot.">

关注点分离
-----------

将结构、表现、行为分离。

严格保持结构（标识），表现（样式），行为（脚本）分离，尽量使三者之间的相互影响最小。

就是说，确保文档和模板只包含HTML，并且HTML只用来表现结构。把任何表现性的东西都移到样式表，任何行为性的东西都移到脚本中。

此外，尽可能少的从文档和模板中引用样式表和脚本来减少三者的相互影响。

结构、表现、行为分离对维护非常重要。更改HTML文档和模板总是比更新样式表和脚本成本更高。

.. code-block:: html

  <!-- 不推荐 -->
  <!DOCTYPE html>
  <title>HTML sucks</title>
  <link rel="stylesheet" href="base.css" media="screen">
  <link rel="stylesheet" href="grid.css" media="screen">
  <link rel="stylesheet" href="print.css" media="print">
  <h1 style="font-size: 1em;">HTML sucks</h1>
  <p>I’ve read about this on a few sites but now I’m sure:
    <u>HTML is stupid!!1</u>
  <center>I can’t believe there’s no way to control the styling of
    my website without doing everything all over again!</center>
   
  <!-- 推荐 -->
  <!DOCTYPE html>
  <title>My first CSS-only redesign</title>
  <link rel="stylesheet" href="default.css">
  <h1>My first CSS-only redesign</h1>
  <p>I’ve read about this on a few sites but today I’m actually
    doing it: separating concerns and avoiding anything in the HTML of
    my website that is presentational.
  <p>It’s awesome!

实体引用
-----------

不要使用实体引用。

假设文件、编辑器和团队之间使用相同的编码（UTF-8），则没有必要使用例如 ``&mdash;`` 、 ``&rdquo;`` 或 ``&#x263a;`` 这样的实体引用。

唯一的例外适用于HTML中具有特殊意义的字符（比如<和&），和控制或者隐藏的字符（比如不换行空格）。

.. code-block:: html

  <!-- 不推荐 -->
  The currency symbol for the Euro is &ldquo;&eur;&rdquo;.
  
  <!-- 推荐 -->
  The currency symbol for the Euro is "€".

可选的标签
------------

省略可选的标签（可选）。

为了优化文件大小和可扫描，考虑省略可选标签。 `HTML5规范 <http://www.whatwg.org/specs/web-apps/current-work/multipage/syntax.html#syntax-tag-omission>`_ 定义了哪些标签可以被省略。

（这种方法可能要求一段宽限期去建立一个更加广泛的准则，因为它和Web开发人员通常所了解的有着显著不同。考虑到一致性和简单性，最好省略所有可选标签。）

.. code-block:: html

  <!-- 不推荐 -->
  <!DOCTYPE html>
  <html>
   <head>
     <title>Spending money, spending bytes</title>
   </head>
   <body>
     <p>Sic.</p>
   </body>
  </html>
  
  <!-- 推荐 -->
  <!DOCTYPE html>
  <title>Saving money, saving bytes</title>
  <p>Qed.

type属性
---------

为样式表和脚本省略 ``type`` 属性。

引用样式表（除非不是使用CSS）和脚本（除非不是使用JavaScript）不要使用type属性。

HTML5将 `text/css <http://www.whatwg.org/specs/web-apps/current-work/multipage/semantics.html#attr-style-type>`_ 和 `text/javascript <http://www.whatwg.org/specs/web-apps/current-work/multipage/scripting-1.html#attr-script-type>`_ 设置为默认值，在这种情况下指定type属性并不必要。甚至同样兼容老版本的浏览器。

.. code-block:: html
  <!-- 不推荐 -->
  <link rel="stylesheet" href="//www.google.com/css/maia.css" type="text/css">
  
  <!-- 推荐 -->
  <link rel="stylesheet" href="//www.google.com/css/maia.css">
  
  <!-- 不推荐 -->
  <script src="//www.google.com/js/gweb/analytics/autotrack.js" type="text/javascript"></script>
  
  <!-- 推荐 -->
  <script src="//www.google.com/js/gweb/analytics/autotrack.js"></script>
