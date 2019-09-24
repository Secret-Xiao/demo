import numpy as np
import matplotlib.pyplot as plt
import pandas as pd #导入包
from sqlalchemy import create_engine
def read_mysql(table):
    engine = create_engine('mysql+pymysql://root:root@localhost'
                           ':3306/hadooptest?charset=utf8')
    detail = pd.read_sql_table(table, con=engine)
    return detail
def top_cpu_10(data_head,head):
    phone = data_head.index  # data_head['手机型号']
    print(data_head)
    height = data_head.money  # data_head['手机价格']
    plt.figure(num=1, figsize=[8, 6], dpi=None, facecolor='gainsboro')  # 生成画布
    plt.rcParams['font.sans-serif'] = 'SimHei'  # 使中文正常显示
    # plt.rcParams['axes.unicode_minus']=False  # 正常显示负号
    x = np.arange(phone.size)
    plt.bar(x, height, color='cadetblue')
    plt.xlabel('手机型号')  # 设置x轴标签
    plt.ylabel('价格')  # 设置y轴标签
    plt.title(head)  # 设置标题
    ax = plt.gca()
    ax.set_xticklabels(phone)
    plt.ylim(height.min()-200, height.max()+200)  # 设置y轴的范围
    plt.grid(True, linestyle=':', color='b', alpha=0.6)  # alpha表示透明度
    plt.xticks(np.arange(phone.size), rotation=90)  # rotation控制倾斜角度
    plt.show()
    # plt.savefig("D:/直方图.png")
def tail_20_cpu(data_group):
    plt.figure(num=1, figsize=[8, 6], dpi=None, facecolor='gainsboro')  # 生成画布
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    sizes = data_group['phoneName'].count()
    print(sizes)
    labels = dict([y for y in data_group]).keys()
    explode = (0.1, 0.1, 0,0.1,0.1,0)
    plt.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', shadow=True, startangle=120)

    # plt.pie(sizes,  labels=labels, autopct='%1.1f%%', shadow=True, startangle=120)
    plt.title("前20价格最高各手机所占其中比例")
    plt.legend(loc='upper right')
    plt.show()
    # plt.savefig("D:/饼图.png")
def test(a,b):
    data_group=a.groupby(by='phoneCPU').agg(np.min)
    data_group['money'] = data_group['money'].astype('int')  # 将手机价格转换为整型,没转换前为object类型
    price_sort = data_group.sort_values('money')  # 按手机价格升序排序
    top_cpu_10(price_sort,b)

if __name__ == "__main__":
    # 读取某一张具体的表
    detail=read_mysql("test2")
    detail['money'] = detail['money'].astype('int')
    #
    # data_group=detail.groupby(by='CPU型号')
    # group_one=dict([x for x in data_group])['骁龙855']
    # group_one['手机价格']=group_one['手机价格'].astype('int')# 将手机价格转换为整型,没转换前为object类型
    # price_sort=group_one.sort_values('手机价格') # 按手机价格升序排序
    # data_head=price_sort.head(10) # 取出排序后的前十行
    # top_cpu_10(data_head)

    # detail['手机价格'] = detail['手机价格'].astype('int')
    # sort_price = detail.sort_values('手机价格')
    # tail_twenty = sort_price.tail(20)
    # data_group = tail_twenty.groupby(by='CPU型号')
    # print(data_group)
    #
    # tail_20_cpu(data_group)

    data_group=detail.groupby(by='phoneCPU')

    group_855=dict([x for x in data_group])['高通 骁龙855']
    # group_855['money']=group_855['money'].astype('int')# 将手机价格转换为整型,没转换前为object类型
    price_sort=group_855.sort_values('money') # 按手机价格升序排序
    data_head=price_sort.head(10) # 取出排序后的前十行
    top_cpu_10(data_head,'骁龙855cpu各手机型号与价格直方图')

    group_845 = dict([x for x in data_group])['高通 骁龙845']
    # group_845['money'] = group_845['money'].astype('int')  # 将手机价格转换为整型,没转换前为object类型
    price_sort = group_845.sort_values('money')  # 按手机价格升序排序
    data_head = price_sort.head(10)  # 取出排序后的前十行
    top_cpu_10(data_head,'骁龙845cpu各手机型号与价格直方图')
    #
    group_835 = dict([x for x in data_group])['高通 骁龙835']
    # group_835['money'] = group_835['money'].astype('int')  # 将手机价格转换为整型,没转换前为object类型
    price_sort = group_835.sort_values('money')  # 按手机价格升序排序
    data_head = price_sort.head(10)  # 取出排序后的前十行
    top_cpu_10(data_head,'骁龙835cpu各手机型号与价格直方图')

    #饼图

    sort_price = detail.sort_values('money')
    tail_twenty = sort_price.tail(20)
    data_group1 = tail_twenty.groupby(by='phoneCPU')
    tail_20_cpu(data_group1)

    #各个价位手机图
    money_3000 = detail[detail.money > 3000]
    money_2000=detail[detail.money>2000]
    money_2000=money_2000[money_2000.money<3000]
    money_1000 = detail[detail.money > 1000]
    money_1000=money_1000[money_1000.money<2000]
    test(money_1000,'1000元~2000元的手机')
    test(money_2000,'2000元~3000元的手机')
    test(money_3000,'3000千元以上的手机')

    #CPU价格最低图
    # detail['money'] = detail['money'].astype('int')
    CPUmin = data_group.agg({'money': 'min'}).sort_values('money')
    # print(CPUmin)
    top_cpu_10(CPUmin,'各个CPU最低价的价格排行')