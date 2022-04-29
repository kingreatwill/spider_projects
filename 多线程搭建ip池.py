# -*- coding: gbk -*-    # ��ֹ��������ȸ�ʽ����
# ip������վ��http://www.66ip.cn/areaindex_19/1.html

import requests
from fake_useragent import UserAgent
import pandas as pd
from lxml import etree # xpath
import threading    # ���߳�

# ---------�Ȼ�ȡurl�б�----------
def get_url():
    url_list = []
    url = 'http://www.66ip.cn/index.html'
    data_html = requests.get(url)
    data_html.encoding = 'gbk'
    data_html = data_html.text
    html = etree.HTML(data_html)
    page = html.xpath('//*[@id="PageList"]/a[12]/text()')      # ��ȡȫ������ҳ��
    for i in range(int(page[0])):
        country_url = 'http://www.66ip.cn/{}.html'.format(i+1)
        url_list.append(country_url)
    for i in range(1,35):       # ��Ϊ�Ǹ���վֻ��35������
        city_url = 'http://www.66ip.cn/areaindex_{}/1.html'.format(i)
        url_list.append(city_url)
    return url_list

# ---------------��ȡ����վ����ip----------------
def get_all_ip(url_list):
    headers = {
        'User-Agent': UserAgent().random,
    }
    test_ip = []    # ���ڴ����ȡ������ip
    for url in url_list:
        try:        # ��ֹ��ʱ�����쳣�׳�����
            data_html = requests.get(url=url, headers=headers)
            data_html.encoding = 'gbk'
            data_html = data_html.text
            html = etree.HTML(data_html)
            etree.tostring(html)
            response = html.xpath('//div[@align="center"]/table/tr/td/text()')      # ��ȡhtml����ip��Ϣ����һ������
            test_ip += dispose_list_ip(response)       # ��������Ĵ�������������Ҫ������ɸ��
        except:
            continue
    print("���λ�ȡip��Ϣ��������",len(test_ip))
    return test_ip

# --------------����ȡ��list_ip�ؼ���Ϣ������ȡ�������������----------------
def dispose_list_ip(list_ip):
    num = int((int(len(list_ip)) / 5) - 1)  # 5��һ�У������м��У����е�һ���Ǳ���ֱ��ȥ��
    test_list = []

    for i in range(num):
        a = i * 5
        ip_index = 5 + a  # ʡȥǰ��ı��⣬��5������ip������ÿ��5�������Ӧip
        location_index = 6 + a
        place_index = 7 + a

        items = []
        items.append(list_ip[ip_index])
        items.append(list_ip[location_index])
        items.append((list_ip[place_index]))
        test_list.append(items)
    return test_list

# -----------���б�Ĵ�����������csv-------------
def save_list_ip(list,file_path):
    columns_name=["ip","port","place"]
    test=pd.DataFrame(columns=columns_name,data=list)         # ȥ������ֵ��������ظ�
    test.to_csv(file_path,mode='a',encoding='utf-8')
    print("����ɹ�")

# ------------��ȡ�ļ�����df��ʽ����--------------
def read_ip(file_path):
    file = open(file_path,encoding='utf-8')
    df = pd.read_csv(file,usecols=[1,2,3])      # ֻ��ȡ2,3,4,�У��ѵ�һ�е�����ȥ����
    df = pd.DataFrame(df)
    return df

# -----------��ȡ��ȡ��ip����֤�Ƿ�ϸ�-----------
def verify_ip(ip_list):
    verify_ip = []

    for ip in ip_list:
        ip_port = str(ip[0]) + ":" + str(ip[1])  # ��������ip���˿ں�
        headers = {
            "User-Agent": UserAgent().random
        }
        proxies = {
            'http': 'http://' + ip_port,
            'https': 'https://'+ip_port
        }
        '''http://icanhazip.com���ʳɹ��ͻ᷵�ص�ǰ��IP��ַ'''
        try:
            p = requests.get('http://icanhazip.com', headers=headers, proxies=proxies, timeout=3)
            item = []  # ������ipд��csv�з����ȡ
            item.append(ip[0])
            item.append(ip[1])
            item.append(ip[2])
            verify_ip.append(item)
            print(ip_port + "��֤�ɹ���")
        except Exception as e:
            print(ip_port,"��֤ʧ��")
            continue
    return verify_ip

# ----------------���߳���д----------------------
class MyThread(threading.Thread):
    def __init__(self,func,args):
        """
        :param func: run�����еĺ�����
        :param args: func��������Ĳ���
        """
        threading.Thread.__init__(self)
        self.func = func
        self.args = args

    def run(self):
        print('��ǰ���߳�:{}����'.format(threading.current_thread().name))
        self.result = self.func(self.args)
        return self.func
    def get_result(self):       # ��ȡ����ֵ
        try:
            return self.result  # ������̲߳�ʹ��join�������˴����ܻᱨû��self.result�Ĵ���
        except:
            return None

# -----���������������ƽ���ָ�Ϊ�߳����������߳�ִ��----
def split_list(list,thread_num):
    list_total = []
    num = thread_num  # �߳�����
    x = len(list) // num  # ���������з�����5�������㴫��
    count = 1  # �������ǵڼ����б�
    for i in range(0, len(list), x):
        if count < num:
            list_total.append(list[i:i + x])
            count += 1
        else:
            list_total.append(list[i:])
            break
    return list_total

# -----------���̷߳�����ַ��ȡip��Ϣ---------------
def create_thread_get_ip_list(list,thread_num):
    list_total = split_list(list,thread_num)    # ��������ķ�����������ƽ��������߳�
    thread_list =[]     # �̳߳�
    for url in list_total:      # ����߳�
        t = MyThread(func=get_all_ip,args=url)
        thread_list.append(t)
        # thread1 = MyThread(func=get_all_ip,args=list_total[0])
        # thread2 = MyThread(func=get_all_ip,args=list_total[1])
    for t in thread_list:       # ���������߳�
        t.start()
    for t in thread_list:       # ���̵߳ȴ����߳�
        t.join()
    ip=[]                       # �����ȡ��ip
    for t in thread_list:       # �����ݴ���ip��
        ip += t.get_result()
    print("�ܹ��̻߳�ȡip����Ϊ��",len(ip))
    print(ip)
    return ip

# ------------�����߳���֤ip----------------------
def create_thread_verify_ip(list,thread_num):
    list_total = split_list(list, thread_num)
    thread_list = []    # ����̳߳�
    ip = []             # �����֤�ɹ���ip
    for list in list_total:
        t = MyThread(func=verify_ip,args=list)
        thread_list.append(t)
    for t in thread_list:
        t.start()
    for t in thread_list:
        t.join()
    for t in thread_list:
        ip += t.get_result()
    return ip

if __name__ == '__main__':
    # ----------# ��ȡ����ȡ��ȫ��url---------
    url_list = get_url()
    print(url_list)
    # ----------# �������߳���ȡ--------------
    thread_num1 = 100     # ��һ���߳�����
    test_ip = create_thread_get_ip_list(url_list,thread_num1)
    # ----------��������-------------------
    test_path = 'test.csv'
    save_list_ip(test_ip,test_path)

    # -----���ｨ�����������棬����������������---------
    # ----------# ��ȡ��������������--------------
    df = read_ip(test_path)
    print("ȥ��ǰ�����У�",len(df))
    df = df.drop_duplicates()       # ȥ���ظ�����
    print("ȥ�غ������У�",len(df))
    ip_list = df.values.tolist()    # dfת�б�����Ȼ���̵߳�ʱ���������
    print(ip_list)

    # ----------# �������߳���֤ip--------------
    thread_num2 = 100  # �ڶ����̵߳�����
    ip = create_thread_verify_ip(list=ip_list,thread_num=thread_num2)
    print("��֤ʧ��ip������",len(ip_list)-len(ip))
    print("����ip������",len(ip))

    # ����
    save_path = "verify_ip.csv"
    save_list_ip(ip,save_path)

'''
    # ----�ڶ�����֤��������԰��Լ�����дһ��forѭ��������֤���Σ����ip�ص�������----
    verify_path = 'verify_ip.csv'
    df = read_ip(verify_path)
    print("ȥ��ǰ�����У�",len(df))
    df = df.drop_duplicates()       # ȥ���ظ�����
    print("ȥ�غ������У�",len(df))
    ip_list = df.values.tolist()    # dfת�б�����Ȼ���̵߳�ʱ���������
    print(ip_list)

    # ----------# �������߳���֤ip--------------
    thread_num3 = 20  # �������̵߳�����
    ip = create_thread_verify_ip(list=ip_list,thread_num=thread_num3)
    print("��֤ʧ��ip������",len(ip_list)-len(ip))
    print("����ip������",len(ip))

    # ����
    save_path = "����ip.csv"
    save_list_ip(ip,save_path)
'''
