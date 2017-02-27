import requests
import mechanize
from contextlib2 import suppress
from cStringIO import StringIO
from classes import Artist, Album
from config import artist_page, torrents_page, ptpimg_api_key


def missing(image):
    return image == ''


def bad_host(image):
    # are there any other white-listed hosts?:
    return image.find('ptpimg.me') == -1 and image.find('imgur.com') == -1 and image.find('lut.im') == -1


def broken_link(image):
    # should albumartexchange.com images be considered broken? Are they all watermarked?
    try:
        r = requests.head(image)
    except:
        return True
    return True if r.status_code >= 400 else False


def needs_rehost(image):
    return bad_host(image) and not broken_link(image)


def needs_new(image):
    return missing(image) or broken_link(image)


def is_fine(image):
    return not missing(image) and not bad_host(image) and not broken_link(image)


def get_new_image(target, lastfm):
    cur_image = target.image
    if missing(cur_image):
        print "missing ...",
    elif broken_link(cur_image):
        print "broken link ...",
    scraped_image = get(target, lastfm)
    return scraped_image


def get(target, lastfm):

    image_source = get_image_source(target, lastfm)

    image = None
    for i in reversed(xrange(1, 5)):
        with suppress(Exception):
            image = image_source.get_cover_image(size=i)
            break
    return image


def edit(target, pth):
    url = target.edit_url
    r = pth.session.get(url, data={'auth': pth.authkey})
    forms = mechanize.ParseFile(StringIO(r.text.encode('utf-8')), url)

    form = get_image_field(forms)

    form['image'] = target.image
    form['summary'] = 'added rehosted image from last.fm'
    _, data, headers = form.click_request_data()
    pth.session.post(url, data=data, headers=dict(headers))


def rehost(image_url):
    image_url = get_usable_url(image_url)

    data = {'link-upload': image_url,
            'api_key': ptpimg_api_key}
    r = requests.post('https://ptpimg.me/upload.php', data=data)
    if r.status_code != 200:
        return None

    rjson = r.json()[0]

    rehosted_img = "https://ptpimg.me/{0}.{1}".format(rjson['code'], rjson['ext'])

    return rehosted_img


def get_usable_url(image_url):
    if image_url.find('discogs') != -1 or image_url.find('metal-archives') != -1:
        image_url = 'http://reho.st/' + image_url
    if image_url.find('cps-static') != -1 or image_url.find('metal-archives') != -1:
        image_url = image_url[:image_url.find('?')]
    return image_url


def get_image_field(forms):
    form = None
    for f in forms:
        with suppress(Exception):
            if f.find_control('image'):
                form = f
    return form


def get_image_source(target, lastfm):
    if isinstance(target, Artist):
        image_source = lastfm.get_artist(target.name)
    elif isinstance(target, Album):
        image_source = lastfm.get_album(target.artist_name, target.name)
    return image_source


def fix(target, pth, lastfm):
        if needs_new(target.image):
            target.image = get_new_image(target, lastfm)
            if target.image is None:
                print "failed to get new image :( Nothing on Last.fm?\n"
                return
            else:
                print "found ...",
                new_image = True
        else:
            new_image = False
        if pth.authkey is not None:
            if needs_rehost(target.image):
                if not new_image:
                    print target.image
                    print "bad host ...",
                    print "rehosting ...",
                target.image = rehost(target.image)
                if target.image is None:
                    print "failed to rehost image :( What could be the problem?\n"
                    return
        print "adding ...",
        edit(target, pth)
        print "done!\n"
