import requests
import mechanize
from cStringIO import StringIO
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

def edit(artist, new_image, pth):

    url = artist_page + '?action=edit&artistid=%s' % artist['id']
    print url
    r = pth.session.get(url, data={'auth': pth_auth})
    forms = mechanize.ParseFile(StringIO(r.text.encode('utf-8')), url)

    form = None
    for f in forms:
        try:
            if f.find_control('image'):
                form = f
                break
        except:
            pass

    form['image'] = new_image
    form['summary'] = 'added rehosted image from last.fm'
    _, data, headers = form.click_request_data()
    pth.session.post(url, data=data, headers=dict(headers))

def rehost(image_url):
    if image_url.find('discogs') != -1:
        image_url = 'http://reho.st/' + image_url

    data = {'link-upload' : image_url,
            'api_key' : ptpimg_api_key}
    r = requests.post('https://ptpimg.me/upload.php', data=data)
    if r.status_code != 200:
        return None

    rjson = r.json()[0]

    rehosted_img = "https://ptpimg.me/{0}.{1}".format( rjson['code'], rjson['ext'])

    return rehosted_img
