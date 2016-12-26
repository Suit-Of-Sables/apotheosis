import mechanize
import image
from config import pth_auth
from cStringIO import StringIO

def get_covers(artist, lastfm, pth):
    print"ALBUM COVERS\n"
    groups = artist['torrentgroup']
    for group in groups:
        cur_image = group['wikiImage']

        if not image.missing(cur_image) and not image.bad_host(cur_image):
            continue

        elif image.missing(cur_image):
            print group['groupName']
            print "missing...",
            image_to_rehost = image.get(lastfm, artist['name'], group['groupName'])

            if image_to_rehost == None:
                print "failed to get new image :( Is unicode causing a problem?\n"
                continue
            print "found...",
        else:
            print group['groupName']
            print cur_image
            print "bad host...",
            image_to_rehost = cur_image

        print "rehosting...",
        rehosted_image = image.rehost(image_to_rehost)

        if rehosted_image == None:
            print "failed to rehost image :( Some discog URLs seem to be a problem...\n"
            continue
        print "rehosted!\n"


        url = "https://passtheheadphones.me/torrents.php?action=editgroup&groupid=%s" % group['groupId']
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
        form['image'] = rehosted_image
        form['summary'] = 'added rehosted image from last.fm'
        _, data, headers = form.click_request_data()
        pth.session.post(url, data=data, headers=dict(headers))
