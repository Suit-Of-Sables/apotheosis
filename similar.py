def find(artist_data, lastfm, config):
    # non-string config vars seem to be annoying...
    max_to_add = int(config.max_to_add)
    min_score = float(config.min_score)

    # get list of current similar artists on PTH
    cur_similar = [a['name'] for a in artist_data["similarArtists"]]

    # get list of at most max_to_add similar artist from last.fm
    new_similar = lastfm.get_artist(artist_data['name']).get_similar()
    new_similar = new_similar[:max_to_add]

    # find all artists that meet min_score
    new_similar = [a[0].name for a in new_similar if a[1] >= min_score]

    # but don't don't try to add one if already there
    new_similar = [a for a in new_similar if a not in cur_similar]

    return new_similar

def add(artist_data, new_similar, pth, config):

    data = {'action' : 'add_similar',
            'auth' : config.pth_auth,
            'artistid' : artist_data['id'],
            'artistname': ''}

    for artist in new_similar:
        data['artistname'] = artist
        r = pth.session.post(config.artist_page, data=data)
