import argparse

from requests import get


access_token = ''


def get_user_id(screen_name):
    return get(f"https://api.vk.com/method/utils.resolveScreenName?screen_name={screen_name}&"
               f"access_token={access_token}&v=5.76").json()['response']['object_id']


def get_user_info(id):
    user_info = get(f"https://api.vk.com/method/users.get?user_ids={id}"
                    f"&fields=sex,city,bdate&access_token={access_token}&v=5.76").json()['response'][0]
    sex = 'female' if user_info['sex'] == 1 else 'male'
    first_name = user_info['first_name']
    last_name = user_info['last_name']
    print(f"User: {first_name} {last_name}")
    if 'bdate' in user_info:
        print(f"Birth date: {user_info['bdate']}")
    if 'sex' in user_info:
        print(f'Sex: {sex}')
    if 'city' in user_info:
        print(f"City: {user_info['city']['title']}")
    print('\n')
    get_user_friends(id, first_name, last_name)


def get_user_friends(id, first_name, last_name):
    friends_info = get(f"https://api.vk.com/method/friends.get?user_id={id}&order=name"
                    f"&fields=online&access_token={access_token}&v=5.76").json()['response']
    print(f"{first_name} {last_name} has {friends_info['count']} friends:")
    friends = friends_info['items']
    for friend in friends:
        online = 'online' if friend['online'] == 1 else 'offline'
        print(f"\t{friend['first_name']} {friend['last_name']} {online}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="A simple program that prints a short information "
                                                 "about user and their friends list")
    parser.add_argument('id', type=str, help="id or screen name of the user")
    args = parser.parse_args()
    try:
        user_id = args.id if args.id.isdigit() else get_user_id(args.id)
        get_user_info(user_id)
    except Exception as e:
        print(e)
