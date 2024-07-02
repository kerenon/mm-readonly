# mm-readonly
## About
The free version of Mattermost does not allow you to create read only channels. To solve this problem, I created this very minimalistic bot. After adding to channels, the bot listens to message post events and checks if the posting user is on the channels whitelist. If not, the message gets deleted almost instantly. Replies to existing posts (threads) are allowed.

## Configuration
Configuration is done entirely using environment variables:
* `MM_URL`: Mattermost server URL without http(s) (`10.100.0.100` or `mattermost.example.com`)
* `MM_PORT`: Mattermost server port (`8065`)
* `MM_TOKEN`: Mattermost bot token (`cdieh7um3kd1ta778u4rcxeqto`)
* `MM_SCHEME`: Mattermost server access schema (`http` or `https`)
* `MM_DEBUG`: Debug websocket connection (`True` or `False`)

Whitelist rules are also added using environment variables:

The format is: WHITELIST_channel_id=user_id1,user_id2,user_id3...

`WHITELIST_x9haj1kz3dr43x5eqshcet3kiw=f3dtetan3i85pytf51zg4a1msy`
