本项目依赖这位[大佬](https://github.com/kale5195/chilloutai/)开发的RunPod Serverless api调用实现

~~我就是把大佬的python接口调用改了一下，然后输入telegram bot的token就可以用了~~

参见:

[chilloutai/serverless-zh.md at main · kale5195/chilloutai (github.com)](https://github.com/kale5195/chilloutai/blob/main/serverless-zh.md)

[chilloutai/runpod_api_test.py at main · kale5195/chilloutai (github.com)](https://github.com/kale5195/chilloutai/blob/main/runpod_api_test.py)

##   如何运行

##1.前往[@botfather](t.me/botfather)处获取telegram token

<img src="https://github.com/chunzhimoe/aidrawbot/blob/f299a5ad4ab92b045e6cb1c18338860081e2424a/image-20230406102729027.png" alt="image-20230406102729027" style="zoom:50%;" />

## 2.注册runpod 获取apikey和程序name

[点击这里查看，作者的教程](https://github.com/kale5195/chilloutai/blob/main/serverless-zh.md)

## 3.部署

随便找台linux vps     **我演示用的是debian系统,debian系列系统直接梭哈**

```
apt update && apt -y install python3-pip && apt -y install git
git clone https://github.com/chunzhimoe/aidrawbot
cd aidrawbot
pip3 install requirements.txt
python3 bot.py 
```

**(可选)守护进程--日常使用screen就行**

```
apt -y install screen && screen -S bot
python3 bot.py
```

## 4.实际使用

### 4.1 [查询tag](https://chilloutai.com/) 作者大大的网站

### 4.2 转到telegram

```
/help 查看帮助
/generate 制作图片
```



<img src="https://raw.githubusercontent.com/chunzhimoe/aidrawbot/main/image-20230406103948938.png" alt="image-20230406103948938" style="zoom:67%;" />

## 5.局限性

**没有任何安全措施！！！请不要分享使用！！！生成取决于选择的runpod机器配置，大约30-40s生成一张图**

## 7.to do

- 添加bot主人模式，允许根据chat id放入群组使用

## 8.特别感谢

[kale5195/chilloutai: AI 图片生成 (github.com)](https://github.com/kale5195/chilloutai)

bot基本上也是在大佬的python调用代码runpod代码上实现的，感谢大佬的无私付出！

其中还有不少问题，我也是个代码垃圾，只略懂一点python.还有不少问题问了chatgpt,如果有其他问题,欢迎大佬们指出！



