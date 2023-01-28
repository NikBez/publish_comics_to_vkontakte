from pathlib import Path
import requests
from vk import get_wall_upload_server, post_photo_on_server, save_wall_photo, post_on_the_wall
from environs import Env
from random import randint
from time import sleep


def main():

    env = Env()
    env.read_env()
    vk_access_token = env('VK_ACCESS_TOKEN')
    group_id = env('GROUP_ID')

    while True:
        try:
            text = download_random_commix()
        except requests.exceptions.ConnectionError:
            print("Connection error. Make new attempt..")
            sleep(5)
            continue
        try:
            upload_address = get_wall_upload_server(vk_access_token, group_id)
            uploaded_photo_params = post_photo_on_server("temp_picture.png", upload_address)
            photo_object = save_wall_photo(vk_access_token, uploaded_photo_params, group_id)
            post_on_the_wall(vk_access_token, photo_object, group_id, text)
        except requests.exceptions.ConnectionError:
            print("Connection error. Make new attempt..")
            sleep(5)
            continue

        print("Опубликован новый пост.")
        Path.unlink("temp_picture.png")
        break


def download_random_commix():

    commix_number = get_random_number()

    image_metadata_url = f"https://xkcd.com/{commix_number}/info.0.json"
    image_metadata = requests.get(image_metadata_url)
    image_metadata.raise_for_status()
    image_metadata = image_metadata.json()

    text = image_metadata['alt']

    img_url = requests.get(image_metadata["img"])
    img_url.raise_for_status()

    with open("temp_picture.png", "wb") as picture:
        picture.write(img_url.content)
    return text


def get_random_number():
    last_commix_url = "https://xkcd.com/info.0.json"
    response = requests.get(last_commix_url)
    response.raise_for_status()
    return randint(1, int(response.json()['num']))


if __name__=="__main__":
    main()

