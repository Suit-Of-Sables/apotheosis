import requests

# The hardcoded URLs should end up in a config file

def missing(image):
    return image == ''

def bad_host(image):
    # do I have to worry about http being used instead of https?:
    if image.startswith('http://ptpimg.me/') or image.startswith('https://ptpimg.me/'):
        return False
    else:
        return True

def get(artist_name, lastfm):
    try:
        image = lastfm.get_artist(artist_name).get_cover_image(size=4)
    except:
        try:
            image = lastfm.get_artist(artist_name).get_cover_image(size=3)
        except:
            try:
                image = lastfm.get_artist(artist_name).get_cover_image(size=2)
            except:
                return None
    return image

def edit(artist, artist_page, image, pth, auth):

    artist['body'] = clean_body(artist['body'])

    data = {'action' : 'edit',
            'auth' : auth,
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

def rehost(img, api_key):
    data = {'link-upload' : img,
            'api_key' : api_key}
    r = requests.post('https://ptpimg.me/upload.php', data=data)
    if r.status_code != 200:
        return None

    rjson = r.json()[0]

    rehosted_img = "https://ptpimg.me/{0}.{1}".format( rjson['code'], rjson['ext'])

    return rehosted_img
