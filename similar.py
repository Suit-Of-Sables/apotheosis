def find(artist_data, lastfm, config):
    # get list of current similar artists on PTH
    cur_similar = [a['name'] for a in artist_data["similarArtists"]]

    # get list of at most max_to_add similar artist from last.fm
    similar = lastfm.get_artist(artist_data['name']).get_similar()
    similar = similar[:int(config['DEFAULT']['max_to_add'])]

    # find all artists that meed min_score
    new_similar = []
    for artist in similar:
        if artist[1] >= float(config['DEFAULT']['min_score']):
            new_similar.append(artist[0].name)

    # but don't don't try to add one if already there
    new_similar = [a for a in new_similar if a not in cur_similar]

    return new_similar

def add(artist_data, new_similar, pth, config):

    data = {'action' : 'add_similar',
            'auth' : config['pth']['auth'],
            'artistid' : artist_data['id'],
            'artistname': ''}

    for artist in new_similar:
        data['artistname'] = artist
        r = pth.session.post(config['pth']['artist_page'], data=data)
