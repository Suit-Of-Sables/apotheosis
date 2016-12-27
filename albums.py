from HTMLParser import HTMLParser
import mechanize
import image
from config import pth_auth
from cStringIO import StringIO

def get_covers(artist, lastfm, pth):
    print"ALBUM COVERS\n"
    groups = artist['torrentgroup']

    parser = HTMLParser()

    for group in groups:
        cur_image = group['wikiImage']

        if image.is_fine(cur_image):
            continue

        #Everything is not fine!!
        print parser.unescape(group['groupName'])
        if image.needs_new(cur_image):
            if image.missing(cur_image):
                print "missing ...",
            elif image.broken_link(cur_image):
                print "broken link ...",

            image_to_rehost = image.get(lastfm, artist['name'], group['groupName'])

            if image_to_rehost == None:
                print "failed to get new image :( Nothing on Last.fm?\n"
                continue
            else:
                print "found ...",

        if image.needs_rehost(cur_image) and pth_auth != None:
            print cur_image
            print "bad host ...",
            image_to_rehost = cur_image

        if pth_auth != None:
            print "rehosting ...",
            rehosted_image = image.rehost(image_to_rehost)

            if rehosted_image == None:
                print "failed to rehost image :( What could be the problem?\n"
                continue
        else:
            print "adding ...",

        # image.py uses something almost identical
        # they should be collapsed into one function
        url = "https://passtheheadphones.me/torrents.php?action=editgroup&groupid=%s" % group['groupId']
        r = pth.session.get(url, data={'auth': pth_auth})
        forms = mechanize.ParseFile(StringIO(r.text.encode('utf-8')), url)

        form = None
        # for f in iter(forms, f.find_control('image') == True)
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
        print "done!\n"
