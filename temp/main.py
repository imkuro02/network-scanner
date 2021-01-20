import eel
import time

eel.init('web')

@eel.expose
def reload():
    return 'test'

eel.start('index.html')

