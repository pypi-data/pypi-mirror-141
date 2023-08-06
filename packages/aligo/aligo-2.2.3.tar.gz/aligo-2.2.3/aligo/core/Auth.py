"""认证模块"""

import base64
import json
import logging
import os
import sys
import tempfile
import time
from dataclasses import asdict
from pathlib import Path
from typing import Callable, overload, List, NoReturn, Dict

import coloredlogs
import qrcode
import qrcode_terminal
import requests

from aligo.core.Config import *
from aligo.types import *
from aligo.types.Enum import *

_aligo = Path.home().joinpath('.aligo')
_aligo.mkdir(parents=True, exist_ok=True)


def get_configurations() -> List[str]:
    """获取配置文件列表"""
    list_: List[str] = []
    file_: os.DirEntry
    for file_ in os.scandir(_aligo):
        list_.append(os.path.splitext(file_.name)[0])
    return list_


class Auth:
    """..."""

    def debug_log(self, response: requests.Response) -> NoReturn:
        """打印错误日志, 便于分析调试"""
        r = response.request
        self.log.warning(f'[method status_code] {r.method} {response.status_code}')
        self.log.warning(f'[url] {response.url}')
        self.log.warning(f'[headers] {r.headers}')
        self.log.warning(f'[request body] {r.body}')
        self.log.warning(f'[response body] {response.text[:200]}')

    def error_log_exit(self, response: requests.Response) -> NoReturn:
        """打印错误日志并退出"""
        self.debug_log(response)
        exit(-1)

    @overload
    def __init__(
            self,
            name: str = 'aligo',
            show: Callable[[str], NoReturn] = None,
            level=logging.DEBUG,
            loglog: bool = False,
            proxies: Dict = None
    ):
        """扫描二维码登录"""

    @overload
    def __init__(
            self,
            name: str = 'aligo',
            refresh_token: str = None,
            level=logging.DEBUG,
            loglog: bool = False,
            proxies: Dict = None
    ):
        """refresh_token 登录"""

    def __init__(
            self, name: str = 'aligo',
            refresh_token: str = None,
            show: Callable[[str], NoReturn] = None,
            level: int = logging.DEBUG,
            loglog: bool = False,
            proxies: Dict = None
    ):
        """登录验证

        :param name: (可选, 默认: aligo) 配置文件名称, 便于使用不同配置文件进行身份验证
        :param refresh_token:
        :param show: (可选) 显示二维码的函数
        :param level: (可选) 控制控制台输出
        :param loglog: (可选) 控制文件输出
        :param proxies: (可选) 自定义代理 [proxies={"https":"localhost:10809"}],支持 http 和 socks5（具体参考requests库的用法）
        """
        self._name = _aligo.joinpath(f'{name}.json')

        self.log = logging.getLogger(f'{__name__}:{name}')

        # if level <= logging.DEBUG:
        #     fmt = '%(asctime)s.%(msecs)03d %(levelname)5s %(message)s :%(filename)s %(lineno)s'
        # else:
        fmt = f'%(asctime)s.%(msecs)03d {name}.%(levelname)s %(message)s'

        coloredlogs.install(
            level=level,
            logger=self.log,
            milliseconds=True,
            datefmt='%X',
            fmt=fmt
        )

        if loglog:
            logfile = logging.FileHandler(filename=str(self._name)[:-5] + '.log', mode='w', encoding='utf-8')
            logfile.setLevel(logging.DEBUG)
            formatter = logging.Formatter('%(asctime)s  %(filename)s  %(funcName)s : %(levelname)s  %(message)s',
                                          datefmt='%F %X')
            logfile.setFormatter(formatter)
            self.log.addHandler(logfile)

        self.log.info(f'Config {self._name}')
        self.log.info(f'日志等级 {logging.getLevelName(level)}')

        #
        self.session = requests.session()
        self.session.trust_env = False
        self.session.proxies = proxies
        self.session.params.update(UNI_PARAMS)  # type:ignore
        self.session.headers.update(UNI_HEADERS)

        self.session.get(AUTH_HOST + V2_OAUTH_AUTHORIZE, params={
            'login_type': 'custom',
            'response_type': 'code',
            'redirect_uri': 'https://www.aliyundrive.com/sign/callback',
            'client_id': CLIENT_ID,
            'state': r'{"origin":"file://"}',
            # 'state': '{"origin":"https://www.aliyundrive.com"}',
        }, stream=True).close()

        #
        SESSIONID = self.session.cookies.get('SESSIONID')
        self.log.debug(f'SESSIONID {SESSIONID}')

        #
        self.token: Optional[Token] = None
        if show is None:
            if os.name == 'nt':
                self.log.debug('Windows 操作系统')
                show = self._show_qrcode_in_window
            elif sys.platform.startswith('darwin'):
                self.log.debug('MacOS 操作系统')
                show = self._show_qrcode_in_window
            else:
                self.log.debug('类 Unix 操作系统')
                show = self._show_console
        self._show = show

        if refresh_token:
            self.log.debug('使用 refresh_token 方式登录')
            self._refresh_token(refresh_token)
            return

        if self._name.exists():
            self.log.info(f'加载配置文件 {self._name}')
            self.token = Token(**json.load(self._name.open()))
        else:
            self.log.info('使用 扫描二维码 方式登录')
            self._login()

        #
        self.session.headers.update({
            'Authorization': f'Bearer {self.token.access_token}'
        })

    def _save(self) -> NoReturn:
        """保存配置文件"""
        self.log.info(f'保存配置文件: {self._name}')
        json.dump(asdict(self.token), self._name.open('w'))

    def _login(self):
        """登录"""
        self.log.info('开始登录 ...')
        response = self._login_by_qrcode()

        if response.status_code != 200:
            self.log.error('登录失败 ~')
            self.error_log_exit(response)

        bizExt = response.json()['content']['data']['bizExt']
        bizExt = base64.b64decode(bizExt).decode('gb18030')

        # 获取解析出来的 refreshToken, 使用这个token获取下载链接是直链, 不需要带 headers
        refresh_token = json.loads(bizExt)['pds_login_result']['refreshToken']
        self._refresh_token(refresh_token, True)

    def _login_by_qrcode(self) -> requests.Response:
        """二维码登录"""
        response = self.session.get(
            PASSPORT_HOST + NEWLOGIN_QRCODE_GENERATE_DO
        )
        data = response.json()['content']['data']
        self.log.info('等待扫描二维码 ...')
        self.log.info('扫描成功后，请手动关闭图像窗口 ...')
        png = self._show(data['codeContent'])
        if png:
            self.log.info(f'如果没有显示二维码，请直接访问二维码图片文件: {png}')
        while True:
            response = self.session.post(
                PASSPORT_HOST + NEWLOGIN_QRCODE_QUERY_DO,
                data=data
            )
            login_data = response.json()['content']['data']
            qrCodeStatus = login_data['qrCodeStatus']
            # self.log.info('等待扫描二维码 ...')
            if qrCodeStatus == 'NEW':
                # self.log.info('等待扫描二维码 ...')
                pass
            elif qrCodeStatus == 'SCANED':
                self.log.info('已扫描, 等待确认 ...')
            elif qrCodeStatus == 'CONFIRMED':
                self.log.info(f'已确认 (你可以关闭二维码图像了).')
                return response
            else:
                self.log.warning('未知错误: 可能二维码已经过期.')
                self.error_log_exit(response)
            time.sleep(2)

    def _refresh_token(self, refresh_token=None, loop_call: bool = False):
        """刷新 token"""
        if refresh_token is None:
            refresh_token = self.token.refresh_token
        self.log.info('刷新 token ...')
        response = self.session.post(
            API_HOST + V2_ACCOUNT_TOKEN,
            json={
                'refresh_token': refresh_token,
                'grant_type': 'refresh_token'
            }
        )
        if response.status_code == 200:
            self.token = Token(**response.json())
            self._save()
        elif not loop_call:
            self.log.warning('刷新 token 失败 ~')
            self.debug_log(response)
            self._login()

        self.session.headers.update({
            'Authorization': f'Bearer {self.token.access_token}'
        })
        # error_log_exit(response)

    def request(self, method: str, url: str,
                params: Dict = None, headers: Dict = None, data=None,
                files: object = None, verify: bool = None, body: Dict = None) -> requests.Response:
        """统一请求方法"""
        # 删除值为None的键
        if body is not None:
            body = {k: v for k, v in body.items() if v is not None}

        if data is not None and isinstance(data, dict):
            data = {k: v for k, v in data.items() if v is not None}

        for i in range(3):
            response = self.session.request(method=method, url=url, params=params,
                                            data=data, headers=headers, files=files,
                                            verify=verify, json=body)
            status_code = response.status_code
            self.log.info(
                f'{response.request.method} {response.url} {status_code} {response.headers.get("Content-Length", 0)}'
            )
            if status_code == 401 or (
                    # aims search 手机端apis
                    status_code == 400 and response.text.startswith('AccessToken is invalid')
            ):
                self._refresh_token()
                continue

            if status_code == 429 or status_code == 500:
                self.log.warning('被限流了，休息一下 ...')
                time.sleep(5)
                continue

            return response

        self.log.info(f'重试3次仍旧失败~')
        self.error_log_exit(response)

    def get(self, path: str, host: str = API_HOST, params: dict = None, headers: dict = None,
            verify: bool = None) -> requests.Response:
        """..."""
        return self.request(method='GET', url=host + path, params=params,
                            headers=headers, verify=verify)

    def post(self, path: str, host: str = API_HOST, params: dict = None, headers: dict = None, data: dict = None,
             files=None, verify: bool = None, body: dict = None) -> requests.Response:
        """..."""
        return self.request(method='POST', url=host + path, params=params, data=data,
                            headers=headers, files=files, verify=verify, body=body)

    @staticmethod
    def _show_console(qr_link: str) -> str:
        """
        在控制台上显示二维码
        :param qr_link: 二维码链接
        :return: NoReturn
        """
        qr_img = qrcode.make(qr_link)

        # try open image
        # 1.
        qr_img.show()

        # show qrcode on console
        # 2.
        qrcode_terminal.draw(qr_link)

        # save image to file
        # 3.
        png = tempfile.mktemp('.png')
        qr_img.save(png)
        return png

    @staticmethod
    def _show_qrcode_in_window(qr_link: str) -> NoReturn:
        """
        通过 *.png 的关联应用程序显示 qrcode
        :param qr_link: 二维码链接
        :return: NoReturn
        """
        # show qrcode in windows & macos
        qr_img = qrcode.make(qr_link)
        qr_img.show()
