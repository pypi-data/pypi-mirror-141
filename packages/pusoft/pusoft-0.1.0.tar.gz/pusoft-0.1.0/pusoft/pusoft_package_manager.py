import time,socket,urllib,urllib.request,os,pusoft
from colorama import init, Fore, Back, Style

init()
init(autoreset=True)
socket.setdefaulttimeout(20)

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "X-Requested-With": "XMLHttpRequest",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
    "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
}

self_path = os.path.dirname(pusoft.__file__) + "\\"

f = open(self_path + "package_list.txt","a")
f.close()

def cmd():
    global name,data
    while 1:
        print(Fore.RED + Back.YELLOW + "*PUSOFT>>>欢迎使用 PUSOFT包管理器！\n[1]安装新软件包\n[2]启动软件包命令行模式\n[3]查看已安装软件包\n[4]卸载软件包\n[5]退出\n请输入命令对应数字",end=":")
        methed = input()
        print()
        if methed == "1":
            print(Fore.WHITE + Back.MAGENTA + "\n*Pumpkin_1001>>>建立起吾与这三千世界的连结吧！")
            print(Fore.MAGENTA + Back.CYAN + "*PUSOFT>>>正在尝试连接至 GitHub 镜像仓库...\n(说明：因为中国无法连接GitHub的raw模式域名，所以我们将使用jsdelivr.net，在此感谢jsdelivr提供的cdn服务！)")
            print(Fore.WHITE + Back.MAGENTA + "\n*Pumpkin_1001>>>這絕對不是Pumpkin_1001的問題！絕對不是！")
            try:
                url = "https://cdn.jsdelivr.net/gh/Pumpkin1001/pusoft@main/list.txt"
                req = urllib.request.Request(url,headers=headers)
                response = urllib.request.urlopen(req)
                data = response.read().decode('utf-8')
                response.close()
                print(Fore.MAGENTA + Back.CYAN + "*PUSOFT>>>连接至 GitHub 镜像仓库成功！\n以下为可用的软件包：\n" + data)
                print(Fore.WHITE + Back.MAGENTA + "*Pumpkin_1001>>>很好。")
                print(Fore.WHITE + Back.MAGENTA + "*Pumpkin_1001>>>来吧，迷惘的人啊，告诉吾你所寻找的『Package』吧",end=":")
                f = open(self_path + "package_list.txt","r")
                package_list = f.read().split("\n")
                data = data.split("\n")
                while 1:
                    name = input()
                    if name in package_list:
                        print(Fore.MAGENTA + Back.CYAN + "*PUSOFT>>>您已安装 " + name + " ,若要升级，请先卸载！")
                        print(Fore.WHITE + Back.MAGENTA + "*Pumpkin_1001>>>再给你一次机会，告诉吾辈你的所求吧",end=":")
                    else:
                        if name not in data or name == "":
                            print(Fore.WHITE + Back.MAGENTA + "*Pumpkin_1001>>>未曾听闻的『Package』呢，再予君一次机会，告诉吾辈你的所求吧",end=":")
                        else:
                            break
                url = "https://cdn.jsdelivr.net/gh/Pumpkin1001/pusoft@main/" + name + ".txt"
                req = urllib.request.Request(url,headers=headers)
                response = urllib.request.urlopen(req)
                data = response.read().decode('utf-8')
                response.close()
                #data.encode('latin-1').decode('gbk').encode('utf-8')
                #data = data.split("#pupm#")
                #data = data[1].replace("#line#","\n")
                #data = data.replace("&quot;",'"')
                #data = data.replace("&#39;","'")
                #data = data.replace("&lt;","<")
                #data = data.replace("&gt;",">")
            except:
                print(Fore.MAGENTA + Back.CYAN + "*PUSOFT>>>中途连接至 GitHub 镜像仓库失败，请重试！\n")
                print(Fore.WHITE + Back.MAGENTA + "*Pumpkin_1001>>>唔，这世界也容不下本吾辈吗？\n")
            
            f = open(self_path + name + ".py","w",encoding="utf-8")
            f.write(data)
            f.close()
            print(Fore.MAGENTA + Back.CYAN + "*PUSOFT>>>文件已保存完成，正在执行安装函数...\n以下为软件包的输出内容\n----------------")
            exec("from pusoft import " + name + " as installing\ninstalling.install()")
            f = open(self_path + "package_list.txt","a")
            f.write(name)
            f.close()
            print(Fore.MAGENTA + Back.CYAN + "----------------\n*PUSOFT>>>安装成功！\n")
        elif methed == "2":
            f = open(self_path + "package_list.txt","r")
            package_list = f.read()
            f.close()
            package_list = package_list.split("\n")
            print(Fore.MAGENTA + Back.CYAN + "*PUSOFT>>>请输入软件包名称",end=":")
            while 1:
                name = input()
                if name == "" or name not in package_list:
                    print(Fore.MAGENTA + Back.CYAN + "*PUSOFT>>>您还未安装 " + name + " ,请先安装！")
                    print(Fore.WHITE + Back.MAGENTA + "*Pumpkin_1001>>>你是在愚弄吾辈吗？再给你一次机会，告诉吾辈『Package』之名吧",end=":")
                else:
                    break
            print(Fore.MAGENTA + Back.CYAN + "*PUSOFT>>>已转交控制台的控制权\n以下为软件包的输出内容\n----------------")
            exec("from pusoft import " + name + " as run\nrun.cmd()")
            print(Fore.MAGENTA + Back.CYAN + "----------------\n*PUSOFT>>>已收回控制台的控制权\n")
        elif methed == "3":
            f = open(self_path + "package_list.txt","r")
            package_list = f.read()
            f.close()
            print(Fore.MAGENTA + Back.CYAN + "*PUSOFT>>>您已安装以下软件包(若要升级，请先卸载)：\n" + package_list + "\n")
        elif methed == "4":
            f = open(self_path + "package_list.txt","r")
            package_list = f.read()
            f.close()
            package_list = package_list.split("\n")
            print(Fore.WHITE + Back.MAGENTA + "*Pumpkin_1001>>>来吧，残忍的人啊，告诉吾将为君所抛弃的『Package』吧",end=":")
            while 1:
                name = input()
                if name == "" or name not in package_list:
                    print(Fore.MAGENTA + Back.CYAN + "*PUSOFT>>>您还未安装 " + name + " ,请先安装！")
                    print(Fore.WHITE + Back.MAGENTA + "*Pumpkin_1001>>>你是在愚弄吾辈吗？再给你一次机会，告诉吾辈将为君所抛弃的『Package』吧",end=":")
                else:
                    break
            print(Fore.MAGENTA + Back.CYAN + "*PUSOFT>>>正在执行卸载函数...\n以下为软件包的输出内容\n----------------")
            exec("from pusoft import " + name + " as uninstalling\nuninstalling.uninstall()")
            package_list.remove(name)
            package_list = "\n".join(package_list)
            f = open(self_path + "package_list.txt","w")
            f.write(package_list)
            f.close()
            print(Fore.MAGENTA + Back.CYAN + "----------------\n*PUSOFT>>>卸载成功！\n")
        elif methed == "5":
            break