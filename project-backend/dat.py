data = {
    'users': [{'u_id': 'yp',
		       'email': '951293496@qq.com',
		       'password': '123123',
		       'name_first': 'y',
		       'name_last': 'p',
		       'handle_str': 'abcd',
		       'auth_user_id': '001',
		       'token': '001abcd',
		       'session_list': 1,
		       'permission_id': 0

		       'channel_time':''
		       'dm_time':''
		       'message_time':''

		       'channels_num':0
		       'dms_num':0
		       'messages_num':0	
		       },

		       {'u_id': 'gzx',
		       'email': '1428@qq.com',
		       'password': '123123',
		       'name_first': 'g',
		       'name_last': 'zx',
		       'handle_str': 'efgh',
		       'auth_user_id': '002',
		       'token': '002efgh',
		       'session_list': 2,
		       'permission_id': 1,

		       'channel_time':''
		       'dm_time':''
		       'message_time':''

		       'channels_num':0
		       'dms_num':0
		       'messages_num':0
		       }

    ],

    'channels': [{'channel_id': len(data['channels']) + 1,
			      'name': name,
			      'is_public': is_public,
			      'owner_members': [],
			      'all_members': [],
		          'messages': []},

		         {'channel_id': len(data['channels']) + 1,
			      'name': name,
			      'is_public': is_public,
			      'owner_members': [],
			      'all_members': [],
		          'messages': []}
        ],

    'message_id': 0,

    'dms': [
    		'dm_id' : 01,
	        'name': 'dm1',
	        'messages' : [],
	        'owner' : 'yp',
	        'members' : [
	        			 {'u_id': 'yp',
	                      'email': '951293496@qq.com',
	                      'name_first': 'y',
	                      'name_last': 'p',
	                      'handle_str': 'abcd'},

	                     {'u_id': 'gzx',
	                      'email': '1428@qq.com',
	                      'name_first': 'g',
	                      'name_last': 'zx',
	                      'handle_str': 'efgh'}
	        ]
    ],
}