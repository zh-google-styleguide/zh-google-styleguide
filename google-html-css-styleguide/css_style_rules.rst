css样式规则
==================

CSS有效性
----------

尽可能使用有效的CSS。

使用有效的CSS代码，除非在处理css验证器bug或者是专有的语法时。

使用诸如 `W3C CSS validator <http://jigsaw.w3.org/css-validator/>`_ 等工具验证测试。

使用有效的CSS代码是一个可衡量CSS代码质量的指标，可帮你找出不起作用可被删除的CSS代码，从而确保CSS的合理使用。

id与class的命名
-----------------

使用有意义的或者通用的id和class名称

用能反映出元素目的或者通用的id、class名称，代替那些很表象的、难懂的名称。

如果名称需要是易懂的，或不容易被修改，应该首选特定的或者能反映出元素目的的名称。

通用的名称适用于非特殊元素或与兄弟元素无区别的元素。他们常被称为“辅助元素”。

使用功能性或者通用的名称，可减少不必要的文档或者模板变化。

.. code-block:: css

  /* 不推荐：无意义 */
  #yee-1901 {}
  
  
  /* 不推荐：表象 */
  .button-green {}
  .clear {}
  
  /* 推荐：具体的 */
  #gallery {}
  #login {}
  .video {}
  
  /* 推荐：通用的 */
  .aux {}
  .alt {}

id与class的命名规范
-----------------------

ID和class命名要尽可能简短，但必要的话就别怕长。

尽可能简洁地传达id或者class名称的含义。

使用简洁的id或者class名称有助于提高可读性和代码效率。

.. code-block:: css

  /* 不推荐 */
  #navigation {}
  .atr {}
  
  /* 推荐 */
  #nav {}
  .author {}

选择器的类型
--------------

应当避免在id和class前添加类型选择器。

除了必要情况下（例如辅助的类），不要将元素与id或class名称结合做为选择器。

避免不必要的祖先选择器也是出于 `性能原因 <http://www.stevesouders.com/blog/2009/06/18/simplifying-css-selectors/>`_ 的考虑。

.. code-block:: css
  
  /* 不推荐 */
  ul#example {}
  div.error {}
  
  /* 推荐 */
  #example {}
  .error {}

简写属性
------------

尽可能使用简写的属性书写方式。

CSS提供了多种属性 `简写 <http://www.w3.org/TR/CSS21/about.html#shorthand>`_ 的方式（如 ``font`` ），即使只显式设置一个值，也应该尽可能地使用。

使用简写属性有助于提高代码效率及可读性。

.. code-block:: css

  /* 不推荐 */
  border-top-style: none;
  font-family: palatino, georgia, serif;
  font-size: 100%;
  line-height: 1.6;
  padding-bottom: 2em;
  padding-left: 1em;
  padding-right: 1em;
  padding-top: 0;
  
  /* 推荐 */
  border-top: 0;
  font: 100%/1.6 palatino, georgia, serif;
  padding: 0 1em 2em;


0与单位
----------

省略“0”后的单位。

除非必需，否则0后不要加单位。

.. code-block:: css

  margin: 0;
  padding: 0;

前导0
-----------

省略前导“0”值。

在-1至1之间的值无需保留整数位的0。

.. code-block:: css

  font-size: .8em;


十六进制表示法
----------------

在可能的情况下使用3个字符的十六进制表示法。

对于可用3字符十六进制表示的颜色值，按此规则书写更短、更简洁。

.. code-block:: css

  /* 不推荐 */
  color: #eebbcc;
  
  /* 推荐 */
  color: #ebc;


前缀选择器
------------

加特定应用前缀（可选）

大型项目中以及嵌入在其它项目或外部网站上的代码需要给id和class添加前缀（命名空间）。使用短的、独特的标识符，并在其后跟一个破折号。
使用命名空间有助于防止命名冲突，可以让维护变得简单，例如在搜索和替换操作时。

.. code-block:: css

  .adw-help {} /* AdWords */
  #maia-note {} /* Maia */


id与class名称分隔符
---------------------

用连字符分隔ID和类名中的单词。

选择器中的词语和缩写中不要使用除了连字符以外的任何字符（包括空字符），以提高可理解性和可读性。

.. code-block:: css

  /* 不推荐: 单词未分开 */
  .demoimage {}
  
  /* 不推荐：使用下划线而不是连字符 */
  .error_status {}
  
  /* 推荐 */
  #video-id {}
  .ads-sample {}

Hacks
------------

请先尝试其他的方法，避免用户代理检测以及CSS的“hacks”。

进行用户代理检测或使用特殊的CSS选择器及hacks看起来是处理样式差异的捷径。但为了实现和保持高效性以及代码的可维护性，这两种方案应该放到最后考虑。换句话说，用户代理检测和使用hacks会增大项目推进的阻力，所以从项目的长远利益考虑应尽力避免。一旦允许并无顾忌地使用用户代理检测和hacks便很容易滥用，最终一发而不可收。
