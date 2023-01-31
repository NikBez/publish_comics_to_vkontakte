import sys

import requests


def get_wall_upload_server(vk_access_token, group_id):

    base_url = "https://api.vk.com/method/photos.getWallUploadServer"
    header = {"Authorization": f"Bearer {vk_access_token}"}
    params = {
        "v": 5.131,
        "group_id": group_id
    }
    response = requests.get(base_url, headers=header, params=params)
    response.raise_for_status()
    response = response.json()
    check_response_errors(response)

    return response["response"]["upload_url"]


def post_photo_on_server(photo_path, upload_url):

    with open(photo_path, 'rb') as photo:
        files = {
            'photo': photo,
        }
        response = requests.post(upload_url, files=files)
    response.raise_for_status()
    response = response.json()
    check_response_errors(response)

    return response["server"], response["photo"], response["hash"]


def save_wall_photo(vk_access_token, group_id, server, photo, hash_code):

    base_url = "https://api.vk.com/method/photos.saveWallPhoto"
    header = {"Authorization": f"Bearer {vk_access_token}"}

    params = {
        "v": 5.131,
        "group_id": group_id,
        "photo": photo,
        "server": server,
        "hash": hash_code,
    }
    response = requests.post(base_url, headers=header, data=params)
    response.raise_for_status()
    response = response.json()
    check_response_errors(response)
    return response['response'][0]['owner_id'], response['response'][0]['id']


def post_on_the_wall(vk_access_token, group_id, owner_id, photo_id, text=""):

    base_url = "https://api.vk.com/method/wall.post"
    header = {"Authorization": f"Bearer {vk_access_token}"}
    params = {
        "v": 5.131,
        "owner_id": f'-{group_id}',
        "from_group": 1,
        "attachments": f"photo{owner_id}_{photo_id}",
        'message': text,
    }
    response = requests.get(base_url, headers=header, params=params)
    response.raise_for_status()
    response = response.json()
    check_response_errors(response)
    return response


def check_response_errors(response):
    if 'error' in response:
        raise VkErrors(response['error']['error_code'], response['error']['error_msg'])


class VkErrors(Exception):
    def __init__(self, error_code, error_description):
        self.error_code = error_code
        self.error_description = error_description
    def __str__(self):
        return f"ERROR CODE: {self.error_code} - {self.error_description}"
