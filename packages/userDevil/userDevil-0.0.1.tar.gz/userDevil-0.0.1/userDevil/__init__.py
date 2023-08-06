import requests

header = {'user-agent': 'Mozilla/5.0 (Linux; Android 10; SM-G981B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Mobile Safari/537.36'}


def check(url, type, proxy='', method='GET' ,content=None):
    if not proxy:
        if method == 'GET':
            if type == 'stats_code': return 'Taken' if requests.get(str(url), headers=header).ok else 'Valid'
            elif type == 'from_content': return 'Valid' if (str(requests.get(url, headers=header).text)).find(content) > 0 else 'Taken'
            else: return 'Wrong type!'

        elif method == 'POST':
            if type == 'stats_code': return 'Taken' if requests.post(str(url), headers=header).ok else 'Valid'
            elif type == 'from_content': return 'Valid' if (str(requests.post(url, headers=header).text)).find(content) > 0 else 'Taken'
            else: return 'Wrong type!'

        else: return 'Wrong method!'

    elif proxy:
        try:
            if method == 'GET':
                if type == 'stats_code': return 'Taken' if requests.get(str(url), headers=header, timeout=15, proxies={'http':f'http://{proxy}', 'https':f'http://{proxy}'}).ok else 'Valid'
                elif type == 'from_content': return 'Valid' if (str(requests.get(url, headers=header, timeout=15, proxies={'http':f'http://{proxy}', 'https':f'http://{proxy}'}).text)).find(content) > 0 else 'Taken'
                else: return 'Wrong type!'

            elif method == 'POST':
                if type == 'stats_code': return 'Taken' if requests.post(str(url), headers=header, timeout=15, proxies={'http':f'http://{proxy}', 'https':f'http://{proxy}'}).ok else 'Valid'
                elif type == 'from_content': return 'Valid' if (str(requests.post(url, headers=header, timeout=15, proxies={'http':f'http://{proxy}', 'https':f'http://{proxy}'}).text)).find(content) > 0 else 'Taken'
                else: return 'Wrong type!'

            else: return 'Wrong method!'

        except requests.exceptions.ProxyError: return 'Bad proxy!'
        except requests.exceptions.ConnectTimeout: return 'Timeout!'
        except requests.exceptions.SSLError: return 'SSL Error!'
        except requests.exceptions.ConnectionError: return 'Bad proxy!'