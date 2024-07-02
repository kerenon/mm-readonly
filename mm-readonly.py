import os
import json
import time
from mattermostdriver import Driver
from mattermostdriver.exceptions import NotEnoughPermissions

def str_to_bool(s):
    return s.lower() in ('1', 'true', 'yes', 'on')

MM_TOKEN  = os.environ.get('MM_TOKEN')
MM_URL    = os.environ.get('MM_URL', 'localhost')
MM_PORT   = int(os.environ.get('MM_PORT', 8065))
MM_SCHEME = os.environ.get('MM_SCHEME', 'http')
MM_DEBUG  = str_to_bool(os.environ.get('MM_DEBUG', 'False'))

if not MM_TOKEN:
    print('A valid mattermost bot token is required to run this bot')
    sys.exit(1)

options = {
    'url': MM_URL,
    'token': MM_TOKEN,
    'port': MM_PORT,
    'scheme': MM_SCHEME,
    'debug': MM_DEBUG
}

WHITELIST = {}

driver = Driver(options)
driver.login()

env_vars = os.environ
for key, value in env_vars.items():
    if key.startswith("WHITELIST_"):
        value = value.split(',')
        value = [item.strip() for item in value]
        print(f"Importing whitelist rule {key}: {value}")
        WHITELIST[key[10:]]=value

async def handle_message(event):
    event_json = json.loads(event)
    if 'event' in event_json.keys():
        event_type = event_json['event']
        if event_type == 'posted':
            sender = event_json['data']['sender_name']
            post_data = json.loads(event_json['data']['post'])
            message_id = post_data['id']
            channel_id = event_json['broadcast']['channel_id']
            root_id = post_data['root_id']
            user_id = post_data['user_id']
            if channel_id not in WHITELIST.keys():
                print(f'Whitelist entry for channel id "{channel_id}" not found. Ignoring.')
            elif not user_id in WHITELIST[channel_id]  and not root_id:
                print(f'Deleting message from user "{sender} ({user_id})". Read only channel!')
                driver.posts.delete_post(post_id=message_id)

driver.init_websocket(handle_message)

while True:
    time.sleep(1)
