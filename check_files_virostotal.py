import hashlib
import os
import requests


APIKEI = ''


def upload_url1(file1):
    import requests

    url = 'https://www.virustotal.com/vtapi/v2/file/scan/upload_url'

    params = {'apikey': APIKEI}

    response = requests.get(url, params=params)
    upload_url_json = response.json()
    upload_url = upload_url_json['upload_url']

    with open(file1, 'rb') as file2:
        files = {'file': file2}
        response = requests.post(upload_url, files=files)
    answer = response.json()
    return answer


def get_digest(file_path):
    h = hashlib.sha256()

    with open(file_path, 'rb') as file:
        while True:
            chunk = file.read(h.block_size)
            if not chunk:
                break
            h.update(chunk)

    return h.hexdigest()


def file_scan(file1):
    with open(file1, 'rb') as file2:
        url = 'https://www.virustotal.com/vtapi/v2/file/scan'

        files = {'file': file2}

        params = {'apikey': APIKEI}

        response = requests.post(url, files=files, params=params)
        answer = response.json()
    return answer


def hash2(file2):
    url = 'https://www.virustotal.com/vtapi/v2/file/report'
    params = {'apikey': APIKEI,
              'resource': get_digest(file2),
              'allinfo': False}
    response = requests.get(url, params=params)
    answer = response.json()
    if answer['response_code'] == 1:
        os.remove(file2)
        return answer, False
    elif os.path.getsize(file2) < 33000000:
        return file_scan(file2), True
    if os.path.getsize(file2) < 200000000:
        return upload_url1(file2), True


def hash3(hash_n, m=False):
    url = 'https://www.virustotal.com/vtapi/v2/file/report'
    params = {'apikey': APIKEI,
              'resource': hash_n,
              'allinfo': m}
    response = requests.get(url, params=params)
    answer = response.json()
    return answer
