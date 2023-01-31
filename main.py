from random import randint
from pathlib import Path
import sys

from environs import Env
import requests

from vk import get_wall_upload_server
from vk import post_photo_on_server
from vk import save_wall_photo
from vk import post_on_the_wall
from vk import VkErrors


TEMP_PICTURE_PATH = Path("temp_picture.png")


def main():

    env = Env()
    env.read_env()
    vk_access_token = env('VK_ACCESS_TOKEN')
    group_id = env('VK_GROUP_ID')

    try:
        text = download_random_comic()
    except requests.exceptions.ConnectionError:
        print("Connection error. Make new attempt..")
        sys.exit()
    try:
        upload_address = get_wall_upload_server(vk_access_token, group_id)
        server, photo, hash_code = post_photo_on_server(TEMP_PICTURE_PATH,
                                                        upload_address
                                                        )
        owner_id, photo_id = save_wall_photo(vk_access_token,
                                             group_id, server, photo,
                                             hash_code
                                             )
        post_on_the_wall(vk_access_token, group_id, owner_id, photo_id, text)
    except requests.exceptions.ConnectionError:
        print("Connection error. Make new attempt..")
        sys.exit()
    except VkErrors as error_text:
        print(error_text)
        sys.exit()
    finally:
        Path.unlink(TEMP_PICTURE_PATH)

    print("Опубликован новый пост.")


def download_random_comic():

    comic_number = get_random_number()

    image_metadata_url = f"https://xkcd.com/{comic_number}/info.0.json"
    metadata_response = requests.get(image_metadata_url)
    metadata_response.raise_for_status()
    metadata_response = metadata_response.json()

    text = metadata_response['alt']

    img_response = requests.get(metadata_response["img"])
    img_response.raise_for_status()

    with open("temp_picture.png", "wb") as picture:
        picture.write(img_response.content)
    return text


def get_random_number():
    last_comic_url = "https://xkcd.com/info.0.json"
    response = requests.get(last_comic_url)
    response.raise_for_status()
    return randint(1, int(response.json()['num']))


if __name__ == "__main__":
    main()
