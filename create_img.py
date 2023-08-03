import numpy as np
import time
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties  # 导入 FontProperties 类
from datetime import datetime  # 导入 datetime 类
import os

local_path = os.getcwd()

# 指定中文字体
font_path = local_path + "/HarmonyOS_Sans_SC_Regular.ttf"
custom_font = FontProperties(fname=font_path)

# 从文件中加载数据
file1 = "resieve_data.txt"
with open(file1) as f:
    data = f.readlines()

# 解析数据
class XiaomiSensorData:
    def __init__(self, index, date, temp_max, temp_min, humid):
        self.index = int(index[6:8] + index[4:6] + index[2:4] + index[0:2], 16)
        self.temp_max = int(temp_max[2:4] + temp_max[0:2], 16) / 10
        self.temp_min = int(temp_min[2:4] + temp_min[0:2], 16) / 10
        self.humid = int(humid, 16)
        time_local = time.localtime(int(date[6:8] + date[4:6] + date[2:4] + date[0:2], 16))
        self.date = time.strftime("%Y-%m-%d %H:%M:%S", time_local)

list3 = [XiaomiSensorData(i[0:8], i[8:16], i[16:20], i[22:26], i[20:22]) for i in data]

# 将数据按日期进行分组，并记录每天的最高温度和最低温度以及湿度
daily_data = {}
for d in list3:
    date = d.date.split()[0]  # 只取日期部分，忽略具体时间
    if date not in daily_data:
        daily_data[date] = {"temp_max": d.temp_max, "temp_min": d.temp_min, "humid": d.humid}
    else:
        daily_data[date]["temp_max"] = max(daily_data[date]["temp_max"], d.temp_max)
        daily_data[date]["temp_min"] = min(daily_data[date]["temp_min"], d.temp_min)
        daily_data[date]["humid"] = d.humid  # 更新湿度数据

# 绘制温度曲线图
xs = [datetime.strptime(d.date, '%Y-%m-%d %H:%M:%S') for d in list3]
temp_max1 = np.array([d.temp_max for d in list3])
temp_min1 = np.array([d.temp_min for d in list3])

plt.figure(figsize=(12, 6))
ax1 = plt.subplot(2, 2, 1)
ax1.plot(xs, temp_max1, label='最高温度', color='r')
ax1.plot(xs, temp_min1, label='最低温度', color='g')
ax1.set_xlabel('日期', fontproperties=custom_font)
ax1.set_ylabel('温度(°C)', fontproperties=custom_font)
ax1.set_title('温度曲线图', fontproperties=custom_font)
ax1.legend(loc='best', prop=custom_font)

# 在温度曲线图旁边放置温度数据表格
ax3 = plt.subplot(2, 2, 2)
ax3.axis('off')  # 不显示坐标轴
ax3.text(0, 1.0, "日期", fontsize=12, fontproperties=custom_font, ha='center', va='bottom', fontweight='bold')  # Change va to 'bottom'
ax3.text(0.25, 1.0, "最高温度(°C)", fontsize=12, fontproperties=custom_font, ha='center', va='bottom', fontweight='bold')  # Change va to 'bottom'
ax3.text(0.55, 1.0, "最低温度(°C)", fontsize=12, fontproperties=custom_font, ha='center', va='bottom', fontweight='bold')  # Change va to 'bottom'
for i, date in enumerate(sorted(daily_data.keys())):  # 显示每天的最高温度和最低温度
    ax3.text(0, 0.95 - i * 0.1, date, fontsize=12, fontproperties=custom_font, ha='center', va='center')  # Change va to 'center'
    ax3.text(0.25, 0.95 - i * 0.1, str(daily_data[date]["temp_max"]), fontsize=12, fontproperties=custom_font, ha='center', va='center')  # Change va to 'center'
    ax3.text(0.55, 0.95 - i * 0.1, str(daily_data[date]["temp_min"]), fontsize=12, fontproperties=custom_font, ha='center', va='center')  # Change va to 'center'

    
# 绘制湿度曲线图
humid1 = [daily_data[date]["humid"] for date in sorted(daily_data.keys())]  # Extract humidity data for each date

ax2 = plt.subplot(2, 2, 3)
ax2.plot(sorted(daily_data.keys()), humid1, label='湿度', color='b')
ax2.set_xlabel('日期', fontproperties=custom_font)
ax2.set_ylabel('湿度(%)', fontproperties=custom_font)
ax2.set_title('湿度曲线图', fontproperties=custom_font)
ax2.legend(loc='best', prop=custom_font)

# 在湿度曲线图旁边放置湿度数据表格
ax4 = plt.subplot(2, 2, 4)
ax4.axis('off')  # 不显示坐标轴
ax4.text(0, 1.0, "日期", fontsize=12, fontproperties=custom_font, ha='center', va='bottom', fontweight='bold')
ax4.text(0.75, 1.0, "湿度(%)", fontsize=12, fontproperties=custom_font, ha='center', va='bottom')  # Adjust the horizontal position to 0.75
for i, date in enumerate(sorted(daily_data.keys())):  # 显示每天的最高温度、最低温度和湿度
    ax4.text(0, 0.95 - i * 0.1, date, fontsize=12, fontproperties=custom_font, ha='center', va='center')
    ax4.text(0.75, 0.95 - i * 0.1, str(daily_data[date]["humid"]), fontsize=12, fontproperties=custom_font, ha='center', va='center')  # Adjust the horizontal position to 0.75

# 添加更新时间
update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
plt.text(0.99, 0.01, f"更新时间：{update_time}", ha='right', va='bottom', fontsize=10, fontproperties=custom_font, transform=ax4.transAxes)

plt.tight_layout()
# 指定保存图片的路径
plt.savefig(local_path + '/temperature_humidity_plot.png')



# 获取最新的温度和湿度
latest_data_point = list3[-1]
latest_temperature_max = latest_data_point.temp_max
latest_temperature_min = latest_data_point.temp_min
latest_humidity = latest_data_point.humid

print(f"最新最高温度：{latest_temperature_max} °C")
print(f"最新最低温度：{latest_temperature_min} °C")
print(f"最新湿度：{latest_humidity} %")
