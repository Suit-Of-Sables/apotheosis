import requests
from config import artist_page, pth_auth, ptpimg_api_key

# The hardcoded URLs should end up in a config file

def missing(image):
    return image == ''

def bad_host(image):
    # do I have to worry about http being used instead of https?:
    if image.startswith('http://ptpimg.me/') or image.startswith('https://ptpimg.me/'):
        return False
    else:
        return True

def get(lastfm, artist_name, album_name=None):
    if (album_name == None):
        image_source = lastfm.get_artist(artist_name)
    else:
        image_source = lastfm.get_album(artist_name, album_name)

    image = None
    for i in [4,3,2,1]:
        try:
            image = image_source.get_cover_image(size=i)
            if image != None:
                break
        except:
            pass
    return image

def edit(artist, image, pth):

    artist['body'] = clean_body(artist['body'])

    data = {'action' : 'edit',
            'auth' : pth_auth,
            'artistid' : artist['id'],
            'body' : artist['body'],
            'image' : image,
            'summary' : 'added artist bio from last.fm'}

    r = pth.session.post(artist_page, data=data)

def clean_body(body):
    body = body.replace('<br />', '')
    body = body.replace('<a rel="noreferrer" target="_blank" href="', '[url=')
    body = body.replace('">Read', ']Read')
    body = body.replace('</a>', '[/url]')
    body = body.replace('<span class="size1">', '[size=1]')
    body = body.replace('</span>', '[/size]')

    return body

def rehost(img):
    data = {'link-upload' : img,
            'api_key' : ptpimg_api_key}
    r = requests.post('https://ptpimg.me/upload.php', data=data)
    if r.status_code != 200:
        return None

    rjson = r.json()[0]

    rehosted_img = "https://ptpimg.me/{0}.{1}".format( rjson['code'], rjson['ext'])

    return rehosted_img
