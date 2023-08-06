#!/usr/bin/env python3
# coding = utf8
"""
@ Author : ZeroSeeker
@ e-mail : zeroseeker@foxmail.com
@ GitHub : https://github.com/ZeroSeeker
@ Gitee : https://gitee.com/ZeroSeeker
"""
import requests
import json


def get_menu_response(
        cookie: str,
        time_out: int = 5
):
    """
    包含账号信息及子账号列表的菜单信息
    """
    url = 'https://open.yuewen.com/api/account/getMenu'
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Cookie": cookie,
        "Host": "open.yuewen.com",
        "Referer": "https://open.yuewen.com/new/dashboard",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"
    }
    response = requests.request(
        method='GET',
        url=url,
        headers=headers,
        timeout=time_out
    )
    return response.json()


def get_menu(
        cookie: str,
        key_name: bool = False,  # 将app名称作为key返回结果
        key_app_id: bool = False,  # 将app_id名称作为key返回结果
        make_list: bool = False,  # 将结果按照list形式返回
        time_out: int = 5
):
    """
    增加对快应用获取的兼容
    """
    res = dict()
    menu_response = get_menu_response(
        cookie=cookie,
        time_out=time_out
    )
    if menu_response.get('status') is True:
        data = menu_response.get('data')

        coop_id = data.get('coopid')  # 合作方式代码
        res['coop_id'] = coop_id
        res['email'] = data.get('email')
        res['is_authoriztion'] = data.get('is_authoriztion')
        top = data.get('top')

        coop_info = top.get(str(coop_id))
        res['coop_name'] = coop_info.get('name')  # 合作方式名称
        coop_apps = coop_info.get('children')  # 合作产品字典
        if make_list is False:
            if key_name is False and key_app_id is False:
                res['status'] = True
                res['code'] = 0
                res['msg'] = 'ok'
                res['data'] = coop_apps
            elif key_name is False and key_app_id is True:
                res['status'] = True
                res['code'] = 0
                res['msg'] = 'ok'
                res['data'] = coop_apps
            elif key_name is True and key_app_id is False:
                data_children2 = dict()
                for key, value in coop_apps.items():
                    value_0 = value.split('|')[0]
                    data_children2[value_0] = key
                res['status'] = True
                res['code'] = 0
                res['msg'] = 'ok'
                res['data'] = data_children2
        else:
            res['status'] = True
            res['code'] = 0
            res['msg'] = 'ok'
            temp_list = list()
            for key, value in coop_apps.items():
                value_0 = value.split('|')[0]
                temp_list.append({'app_id': key, 'app_name': value_0})
            res['data'] = temp_list
    else:
        res.update(menu_response)
    return res


def switch_app(
        cookie: str,
        app_id: str = None,  # 按照app_id切换（优先）
        app_name: str = None,  # 按照app_name切换
        time_out: int = 5
):
    """
    切换app
    """
    res = dict()
    if app_id is not None:
        menu_res = get_menu(cookie=cookie, key_app_id=True)
        if menu_res['code'] == 0:
            pass
        else:
            return menu_res
    elif app_name is not None:
        menu_res = get_menu(cookie=cookie, key_name=True)
        if menu_res['code'] == 0:
            menu_data = menu_res.get('data')
            app_id = menu_data.get(app_name)
        else:
            return menu_res
    else:
        res['status'] = True
        res['code'] = 0
        res['msg'] = 'ok，未做任何操作'
        return res

    coop_id = menu_res.get('coopid')
    url = 'https://open.yuewen.com/api/account/switchApp'
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Content-Type": "application/json;charset=UTF-8",
        "Cookie": cookie,
        "Host": "open.yuewen.com",
        "Origin": "https://open.yuewen.com",
        "Referer": "https://open.yuewen.com/new/dashboard",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"
    }
    data = {
        "coopid": coop_id,
        "appid": str(app_id)
    }
    response = requests.request(
        method='POST',
        url=url,
        headers=headers,
        data=json.dumps(data),
        timeout=time_out
    )
    res.update(response.json())
    return res


def adreport_ocean(
        cookie: str,
        app_id: str = None,  # 按照app_id切换（优先）
        app_name: str = None,  # 按照app_name切换
        time_out: int = 5
):
    """
    [广告回传]-[巨量引擎]（页面数据，包含app_flag、触点链接地址）
    """
    switch_res = switch_app(
        cookie=cookie,
        app_id=app_id,
        app_name=app_name,
        time_out=time_out
    )
    if switch_res['status'] is False:
        return switch_res
    else:
        pass

    url = ' https://open.yuewen.com/api/adreport/ocean?site=2'
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Cookie": cookie,
        "Host": "open.yuewen.com",
        "Referer": "https://open.yuewen.com/new/putMonitor/bytedanceBack",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36",
    }
    response = requests.request(
        method='GET',
        url=url,
        headers=headers,
        timeout=time_out
    )
    response_json = response.json()
    return response_json


def wechat_info(
        cookie: str,
        app_id: str = None,  # 按照app_id切换（优先）
        app_name: str = None,  # 按照app_name切换
        time_out: int = 5
):
    """
    [公众号-快应用设置]-[授权管理]
    """
    switch_res = switch_app(
        cookie=cookie,
        app_id=app_id,
        app_name=app_name,
        time_out=time_out
    )
    if switch_res['status'] is False:
        return switch_res
    else:
        pass

    url = 'https://open.yuewen.com/api/wechat/wechatInfo'
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Cookie": cookie,
        "Host": "open.yuewen.com",
        "Referer": "https://open.yuewen.com/new/wechat/authorization",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
    }
    response = requests.request(
        method='GET',
        url=url,
        headers=headers,
        timeout=time_out
    )
    response_json = response.json()
    return response_json
