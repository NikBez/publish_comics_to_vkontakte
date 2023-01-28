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

    return {"album_id": response["response"]["album_id"],
            "upload_url": response["response"]["upload_url"],
            "user_id": response["response"]["user_id"]
            }


def post_photo_on_server(photo_path, upload_params):

    with open(photo_path, 'rb') as photo:
        url = upload_params["upload_url"]
        files = {
            'photo': photo,
        }
        response = requests.post(url, files=files)
        response.raise_for_status()
        return {
            "server": response.json()["server"],
            "photo": response.json()["photo"],
            "hash": response.json()["hash"],
        }


def save_wall_photo(vk_access_token, uploaded_photo_params, group_id):

    base_url = "https://api.vk.com/method/photos.saveWallPhoto"
    header = {"Authorization": f"Bearer {vk_access_token}"}

    params = {
        "v": 5.131,
        "group_id": group_id,
        "photo": uploaded_photo_params["photo"],
        "server": uploaded_photo_params["server"],
        "hash": uploaded_photo_params["hash"],
    }
    response = requests.post(base_url, headers=header, data=params)
    response.raise_for_status()
    response = response.json()
    return {
        "owner_id": response['response'][0]['owner_id'],
        "photo_id": response['response'][0]['id']
    }


def post_on_the_wall(vk_access_token, photo_object, group_id, text=""):

    base_url = "https://api.vk.com/method/wall.post"
    header = {"Authorization": f"Bearer {vk_access_token}"}
    params = {
        "v": 5.131,
        "owner_id": f'-{group_id}',
        "from_group": 1,
        "attachments": f"photo{photo_object['owner_id']}_{photo_object['photo_id']}",
        'message': text,
    }
    response = requests.get(base_url, headers=header, params=params)
    response.raise_for_status()
    response = response.json()
    return response


def get_groups(vk_access_token, user_id):
    base_url = "https://api.vk.com/method/groups.get"
    header = {"Authorization": f"Bearer {vk_access_token}"}
    params = {
        "v": 5.131,
        "user_id": user_id,
        # "filter": "admin",
    }
    response = requests.get(base_url, headers=header, params=params)
    response.raise_for_status()
    response = response.json()
    return response
