## 北航成绩查询脚本

本项目基于@wzk1015（`ScoreGet_ReleasedVersion_v1.1.py`）修改。

2023-07-06 更新：在原脚本基础上接入了微信的pushplus推送，请在pushplus官网注册账号并填入token即可使用。



### 功能

每分钟刷新本学期GPA，若发生变化（即有课程出分）则一分钟内自动发送推送至微信。



### 使用方法

1. 选择用于发送成绩信息微信，关注pushplus公众号并注册账号，获得token，填入程序相应位置
2. 获取Cookie。Chrome的获取方法：在浏览器中打开[查分网址](https://app.buaa.edu.cn/buaascore/wap/default/index)，并用自己的统一认证账号登录，然后按下F12进入开发者模式，在最上面一栏中点"Application"，在左边栏点"Cookies"左边的小三角，选中"Cookies"下第一个项，将每个元素的名称和值按`'Name':'Value'`的格式填入代码中的cookies，也就是把cookies建立成由【名称到值的映射】构成的字典
3. 运行程序



注：需要保证**py程序持续运行**才能发送推送。有服务器的话可以挂到服务器后台上运行。
