import requests
from vk import get_wall_upload_server, post_photo_on_server, save_wall_photo, post_on_the_wall
from environs import Env

env = Env()
env.read_env()
vk_access_token = env('VK_ACCESS_TOKEN')
group_id = env('GROUP_ID')

url = "https://xkcd.com/353/info.0.json"
response = requests.get(url)
response.raise_for_status()
image_url = response.json()['img']
alt_text = response.json()['alt']

img = requests.get(image_url)
response.raise_for_status()

with open("picture.png", "wb") as picture:
    picture.write(img.content)

upload_address = get_wall_upload_server(vk_access_token, group_id)
uploaded_photo_params = post_photo_on_server("picture.png", upload_address)
photo_object = save_wall_photo(vk_access_token, uploaded_photo_params, group_id)
post_id = post_on_the_wall(vk_access_token, photo_object, group_id, alt_text)

print(post_id)



