import re
import random
import string
import urllib

import bs4
import click
import requests
from simple_loggers import SimpleLogger


class Soopat(object):
    base_url = 'http://www.soopat.com'

    def __init__(self, logger=None):
        self.logger = SimpleLogger('Soopat')
        self.session = requests.session()

    def login(self, username=None, password=None):

        url = 'http://t.soopat.com/index.php?mod=login&code=dologin'

        payload = {
            'username': username or click.prompt('>>> username'),
            'password': password or click.prompt('>>> password'),
        }
        self.session.post(url, data=payload)

        if not self.session.cookies.get('auth'):
            self.logger.error('Login Failed')
            return False

        self.logger.info(f'login successful! [username: {username}]')
        return True

    def register(self, email=None, nickname=None, password=None, auto=True):
        url = 'http://t.soopat.com/index.php?mod=member'

        resp = self.session.get(url)
        soup = bs4.BeautifulSoup(resp.text, 'html.parser')

        qtr = soup.select_one('input[name="qtr"]').attrs['value']
        qt = soup.select_one('#qt').findPrevious().findPrevious().text.strip('=')
        qt = sum(map(int, qt.split('+')))

        random_name = ''.join(random.sample(string.ascii_letters, 11))

        if auto:
            nickname = password = random_name
            email = f'{random_name}@qq.com'
        else:
            email = email or click.prompt('>>> email', default=f'{random_name}@qq.com')
            nickname = nickname or click.prompt('>>> nickname', default=random_name)
            password = password or click.prompt('>>> nickname', default=random_name)

        payload = {
            'email': email,
            'nickname': nickname,
            'password': password,
            'password2': password,
            'copyrightInput': '1',
            'qtr': qtr,
            'qt': qt,
        }

        res = self.session.post(f'{url}&code=doregister', data=payload, allow_redirects=False)
        soup = bs4.BeautifulSoup(res.text, 'html.parser')
        if '您已经注册成功' in res.text:
            self.logger.info(f'您已经注册成功!\n用户名: {email}, 密码: {password}')
            return email, password
        else:
            error_msg = soup.select_one('.main_2').text.strip()
            self.logger.error(f'注册失败!\n{error_msg}')

    def get_pdf_url(self, raw_url, server=''):
        """get the url of pdf

        :param raw_url: raw url or ID, eg. 'http://www.soopat.com/Patent/202111607937' or '202111607937'
        :param server: server to download, '' or 'ct', defaults to ''
        """
        ID = raw_url.split('/')[-1]

        url = f'{self.base_url}/Home/DownloadChoice/{ID}'

        resp = self.session.get(url)
        res = re.findall(rf'"(/Home/DownloadRemote/.+?\.pdf\?Server={server})"', resp.text)
        if not res:
            self.logger.error(f'pdf not exists for ID: {ID}')
            exit(1)

        pdf_url = self.base_url + res[0]
        return pdf_url

    def download(self, pdf_url, outfile=None):
        if 'DownloadRemote' not in pdf_url:
            pdf_url = self.get_pdf_url(pdf_url)

        r = self.session.get(pdf_url, stream=True)
        if r.headers.get('Content-Type') != 'application/pdf':
            if '当日额度已满' in r.text:
                self.logger.warning(f'当日额度已满，无法下载！')
                exit(1)

        if not outfile:
            disposition = r.headers.get('Content-Disposition')
            outfile = urllib.parse.unquote(disposition).split('filename=', 1)[1]

        self.savefile(r, outfile)

    def savefile(self, stream, outfile):
        with open(outfile, 'wb') as out:
            for chunk in stream.iter_content(chunk_size=1024):
                out.write(chunk)
        self.logger.info(f'>>> saved file to: {outfile}')


if __name__ == "__main__":
    sp = Soopat()
    sp.login('tdIhFyuqbZa@qq.com', 'tdIhFyuqbZa')
    # sp.register()
    sp.download('202010463344')