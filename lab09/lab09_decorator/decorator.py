import sys

MESSAGE_LIST = []

def authorise(function):
    """
    You need a function here authorise which contains another function called wrapper.
    This function authenticates the token against CrocodileLikesStrawberries and if valid calls the function given as input,
    authorise then needs to return wrapper.
    """
    def wrapper(*args, **kwargs):
        if len(args) == 2:
            token, input_token = args
            if token == "CrocodileLikesStrawberries":
                result = function(input_token)
                return result

        if len(args) == 1:
            token, = args
            if token == "CrocodileLikesStrawberries":
                result =  function()
    return wrapper

@authorise
def get_messages():
    return MESSAGE_LIST

@authorise
def add_messages(msg):
    global MESSAGE_LIST
    MESSAGE_LIST.append(msg)
    return ''

if __name__ == '__main__':
    auth_token = ""
    if len(sys.argv) == 2:
        auth_token = sys.argv[1]

    add_messages(auth_token, "Hello")
    add_messages(auth_token, "How")
    add_messages(auth_token, "Are")
    add_messages(auth_token, "You?")
    res = get_messages(auth_token)
    if res:
        print(res)
