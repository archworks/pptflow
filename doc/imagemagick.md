
# imagemagick
## 准备
### 下载
https://imagemagick.org/script/download.php


## On MacOS
### 二进制方式安装（Mac OS X Binary Release）
the display program requires the X11 server available on your Mac OS X installation DVD：
https://www.xquartz.org/

* 字体无法显示的解决方式
需要修改`$MAGICK_HOME/etc/type.xml`
参考：https://gist.github.com/otternq/a7611d576b0aed54784b (注意替换路径)

imagick_type_gen
https://legacy.imagemagick.org/Usage/scripts/imagick_type_gen
https://github.com/ImageMagick/ImageMagick/issues/7374
https://github.com/ImageMagick/ImageMagick/issues/3110