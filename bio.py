import re

def missing(artist_data):
    return artist_data['body'] == ''

def add(artist_data, lastfm, pth, config):
    bio = get(artist_data['name'], lastfm)
    if bio == None:
        print "failed to get bio :("
        print "Perhaps there is no bio for this artist on last.fm right now.(?)\n"
        return          # failed to get bio
    bio = to_bbcode(bio)
    edit(artist_data, bio, pth, config)

def get(artist_name, lastfm):
    try:
        bio = lastfm.get_artist(artist_name).get_bio('content')
    except:
        return None
    print "found ...",
    return bio

def to_bbcode(bio):
    bio = re.sub('<a href="', '\n\n[url=', bio)
    bio = re.sub('">Read', ']Read', bio)
    bio = re.sub('</a>.', '[/url]\n', bio)
    s = 'User-contributed text is available under the Creative Commons By-SA License; additional terms may apply.'
    bio = bio.replace(s, '[size=1]' + s + '[/size]')
    return bio

def edit(artist_data, bio, pth, config):
    data = {'action' : 'edit',
            'auth' : config.pth_auth,
            'artistid' : artist_data['id'],
            'body' : bio,
            'image' : artist_data['image'],
            'summary' : 'added artist bio from last.fm'}
    r = pth.session.post(config.artist_page, data=data)
    print "added!"
