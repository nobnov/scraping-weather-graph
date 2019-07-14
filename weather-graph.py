import datetime
import re
import urllib.request

import matplotlib.pyplot as plt
from bs4 import BeautifulSoup


def temp_generate(temps):
    temp_list = []

    for temp in temps:
        temp = temp.text

        if '最低' not in temp and '最高' not in temp:
            temp = temp.replace('\n|\t', '').replace('(', '{').replace(')', '}')
            temp = re.sub('{.*?}', '', temp)

            if '／' in temp:
                temp = None
            else:
                temp = int(temp)

            temp_list.append(temp)

    return temp_list


url = urllib.request.urlopen('https://www.jma.go.jp/jp/week/315.html')
soup = BeautifulSoup(url, 'lxml')

days = soup.find("table", {"id": "infotablefont"}).find_all("tr")[0].find_all("th")
rainy = soup.find("table", {"id": "infotablefont"}).find_all("tr")[2].find_all("td")
max_temp = soup.find("table", {"id": "infotablefont"}).find_all("tr")[4].find_all("td")
min_temp = soup.find("table", {"id": "infotablefont"}).find_all("tr")[5].find_all("td")

day_list = []
for day in days:
    day = day.text

    if '日付' not in day:
        day_list.append(day[:-1])

hour = datetime.datetime.now().hour

rainy_list = []
for rain in rainy:
    rain = rain.text

    if '降水確率' not in rain:
        if '/' in rain:
            if 0 <= hour < 6:
                rain = rain.split('/')[0]
            elif 6 <= hour < 12:
                rain = rain.split('/')[1]
            elif 12 <= hour < 18:
                rain = rain.split('/')[2]
            elif 18 <= hour < 24:
                rain = rain.split('/')[3]
        else:
            pass

        rainy_list.append(int(rain))

maxtemp_list = temp_generate(max_temp)
mintemp_list = temp_generate(min_temp)

x = day_list
plt.subplot(2, 1, 1)
plt.plot(x, maxtemp_list, label='Max', color="red", marker="o")
plt.plot(x, mintemp_list, label='Min', color="blue", marker="o")
plt.title("Weekly weather")
plt.xlabel("Day")
plt.ylabel("Temp")
plt.legend()

plt.subplot(2, 1, 2)
plt.plot(x, rainy_list, marker="o")
plt.title("Rainy percent")
plt.ylabel("Percent")

plt.show()
