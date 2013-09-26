整体样式规则
================

协议
---------------

嵌入式资源省略协议头。

省略图片、媒体文件、样式表以及脚本的URL协议头部分（http:、https:），不使用这两个协议的文件则不省略。
省略协议头，即让URL变成相对地址，可以避免协议混合及小文件重复下载。

.. code-block:: html

  <!-- 不推荐 -->
  <script src="http://www.google.com/js/gweb/analytics/autotrack.js"></script>
  
  <!-- 推荐 -->
  <script src="//www.google.com/js/gweb/analytics/autotrack.js"></script>
  
.. code-block:: css

  /* 不推荐 */
  .example {
   background: url(http://www.google.com/images/example);
  }
  
  /* 推荐 */
  .example {
    background: url(//www.google.com/images/example);
  }

