import secrets


def start():
    text = ['I would like to have ',
            'Please find ',
            'The interface should have ',
            'The interface is ',
            'My interface would be ',
            'I want a screen with ',
            'In this page, I would like to have ']
    return secrets.choice(text)


def connector():
    text = ['then ',
            'then there would be ',
            'then there should be ',
            'under which there\'s also ',
            'under that there\'s also ',
            'followed by ',
            'then I would also like to have ',
            'and under that, add as well ']
    return secrets.choice(text)


def new_sentence():
    text = ['. Under that, I would also like to have ',
            '. This would be followed by ',
            '. Please, also add ',
            '. The interface should also contain ',
            '. The page would also include ',
            '. The screen also has ',
            '. Another thing to add would be ',
            '. Below this, include as well ']
    return secrets.choice(text)


def final_connector():
    text = ['and finally, add ',
            'and at the end of the page, include ',
            'and to finish, there should be ',
            'and the last thing is to add ']
    return secrets.choice(text)


def position():
    text = ['part ',
            'section ',
            'portion ',
            'zone ']
    return secrets.choice(text)


def interface():
    text = ['interface ',
            'page ',
            'screen ',
            'user interface ']
    return secrets.choice(text)


def containing():
    text = ['with ',
            'containing ',
            'including ',
            'that has ']
    return secrets.choice(text)


def contain():
    text = ['contain ',
            'include ',
            'have ']
    return secrets.choice(text)

