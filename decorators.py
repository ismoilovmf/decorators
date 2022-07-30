import requests
from bs4 import BeautifulSoup
from datetime import datetime
from fake_useragent import UserAgent

def logger(path):
    def for_args(old_func):
        def new_func(*args, **kwargs):
            with open(path, 'w') as f:
                name_func = f'Имя функции:\n{old_func.__name__}\n'
                f.write(name_func+'\n')
                argss = f'Аргументы функции:\n{args}\n{kwargs}\n\n'
                f.write(argss)
                call_time = 'Дата вызова функции:\n' + datetime.now().strftime("%Y-%m-%d, %H:%M:%S")
                f.write(call_time+'\n')
                start = datetime.now()
                result = old_func(*args, **kwargs)
                run_time = '\nВремя выполнения функции:\n' + str(datetime.now() - start)
                f.write('\nРезультат функции:\n')
                [f.write(str(i)+'\n') for i in result]
                f.write(run_time)
                print(run_time)
            return result
        return new_func
    return for_args

path = r'D:\Python\Decorators\result.txt'
@logger(path)
def web_srapping(url, KEYWORDS):
    lst = []
    USER_AGENT = UserAgent().random
    resp = requests.get(url+'/ru/all/', headers = {"User-Agent": USER_AGENT})
    soup = BeautifulSoup(resp.text, features="html.parser")
    posts = soup.find_all("article")
    
    for post in posts:
        for word in KEYWORDS:
            s = " ".join([hub.text for hub in post.find_all(class_='tm-article-snippet__hubs-item')])
            if word.lower() in s.lower():
                href = post.find('h2').find('a')['href']
                date = post.find("time")["title"]
                title = post.find('h2').find('a').text
                lst.append({title: [date, url+href]})
    return lst

def main():
    url = 'https://habr.com'
    lst_keywords = ['дизайн', 'фото', 'web', 'python']
    web_srapping(url, lst_keywords)

if __name__ == "__main__":
    main()
