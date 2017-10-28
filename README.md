这是一个模仿hacknews/reddit做的学习项目，使用了django、mysql、bootstrap和jquery。
***
值得注意的有两点：
一是根目录下应该还有两个文件EMAIL_HOST_PASSWORD.txt和SECRET_KEY.txt，
setting.py会从这两个文件读取内容来设置EMAIL_HOST_PASSWORD和SECRET_KEY，
为了保持私密，就没有把这两个文件添加到public分支了。

二是local.cnf上存储有本地数据库的相关设置，服务器连接的数据库设置文件online.cnf也没有
放到这个public分支里面。
