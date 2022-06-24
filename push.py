from pushnotifier import PushNotifier as pn


def sendNotification(x="somthing went wrong", username = 'ZennPy', password ='&Push1900', app = 'com.test1234.app', token='575B52VB52VB6C3V63CV696V575B63CVBFBFBKFKFF'):
    #global pn
    message = pn.PushNotifier(username, password, app, token)
    message.send_text(x,devices=['JqA2'], silent=False)



if __name__ == '__main__':

    message = pn.PushNotifier('ZennPy', '&Push1900',  'com.test1234.app', '575B52VB52VB6C3V63CV696V575B63CVBFBFBKFKFF')
    message.send_text('just for sean',devices=['JqA2'], silent=False)
    #pn.send_text('just for nic',devices=['KZBR'], silent=False)

    #pn.send_text('hello world', silent=False, devices=['abcd', 'efgh'])
    #pn.send_url('https://www.example.com', silent=False, devices=['abcd', 'efgh'])
    #pn.send_notification('hello world', 'https://www.example.com', silent=False, devices=['abcd', 'efgh'])

    # Note on send_image: currently you can't send images to android/ios devices
    #pn.send_image('path/to/image.png', silent=False, devices=['abcd', 'efgh'])
