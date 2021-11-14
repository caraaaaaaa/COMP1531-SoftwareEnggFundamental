# Assumptions


### auth.py
- Assumes u_id starts at 1 when the first user is registered
- Assumes that the characters entered are case sensitive




### channel.py
- Assumes that owner members and all members are stored inside each channel
- Channel_invite assumes invitee can be either log in or not, but inviter should be loged in to invite members
- channel_invite assumes inviter be a valid user
- Channel_details assumes that there can be more than one owner of a channel
- Channel_messages only allows valid indices for the start index, no negative indices and no indices equal to or large than the number of messages
- Channel_messages will always attempt to return 50 messages, if there are less than 50 messages it will return all of them and end = -1
- Channel_join assumes that the user to enter the channel is logged in and is valid
- Channel_leave assumes there is no reason someone cannot leave a channel

### channels.py
- Assumes channel_id and u_id starts at 1 after the first channel is created
- Channels_create assumes the 'is_public' parameter to either be True or False in order to be valid
- Channels_list assumes that it ignores wether a channel is private or is_public
- Channels_listall assumes that it ignores wether a channel is private or is_public
- Channels_list asssumes that only the channel id and name need to be returned 
- channels_listal asssumes that only the channel id and name need to be returned 

### data.py


### other.py


### message.py
- message_share assumes that messages are share in the following format:
    '"Original message"\nOptional message'
