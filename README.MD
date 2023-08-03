# Get MTHMC's Data

# 

## 简介

可用于绘制从小米米家电子温湿度计Pro（Mi Temperature and Humidity Monitor Clock）获取到的数据。

## 前提条件
在使用此脚本之前，请确保已安装以下内容：

- Python 3.x
- 必需的Python库：numpy，matplotlib和Bleak（用于蓝牙通信）

您可以使用pip安装所需的库：
```
pip install -r requirements.txt
```

## 使用方法

详细可以参考 [米家电子温湿度计Pro 数据读取（二） - 哔哩哔哩 (bilibili.com)](https://www.bilibili.com/read/cv23451390/) 

## 自定义
- 如果在图表中遇到任何有关中文字符的问题，您可以在代码中指定不同的中文字体。修改脚本中的"font_path"变量，将其指向您系统上的TTF字体文件。

## 注意
- 该脚本使用蓝牙通信来访问设备中的数据。确保您的设备支持蓝牙

## 许可证
此项目基于MIT许可证授权 - 有关详细信息，请参阅[LICENSE](LICENSE.md)文件。

## 致谢
- [米家电子温湿度计Pro 数据读取（二） - 哔哩哔哩 (bilibili.com)](https://www.bilibili.com/read/cv23451390/)
- [ChatGPT]（https://chat.openai.com/）
