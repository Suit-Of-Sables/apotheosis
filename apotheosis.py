import pylast       # pip install pylast
import sys
import configparser
import pthapi   # local copy, taken from what I was using with pthbetter
# would prefer libpth but can't get to api.API from the version on github :/
#import libpth
# apotheosis modules
import bio              # get bio from last.fm if it's empty on PTH
import similar          # get similar artists from lastfm
import image            # get image from last.fm if it's missing on PTH

# USE: python apotheosis.py 1234
# RESULT: runs imported apotheosis modules on artist with id 1234 on PTH
def main():
    # Please see apotheosis.config for more info on config settings
    config = configparser.ConfigParser()
    config.read('apotheosis.config')

    artist_id = sys.argv[1]     # ID of artist to find similar artists for

    # last.fm connection
    lastfm = pylast.LastFMNetwork(api_key=config['last.fm']['API_KEY'],
                                  api_secret=config['last.fm']['API_KEY'])

    # pth connection
    pth = pthapi.PthAPI(config['pth']['username'], config['pth']['password'])

    # get artist name and info from id
    artist_data = pth.request("artist", id=artist_id)

    print "Finding similar artists for", artist_data['name']
    new_similar = similar.find(artist_data, lastfm, config)

    print "New similar artists to add:"
    print ", ".join(new_similar)
    similar.add(artist_data, new_similar, pth, config)

    # if no artist image, add the one on last.fm
    if image.missing(artist_data):
        print "Artist image is missing..."
        image.add(artist_data, lastfm, pth, config)

    # update artist data incase it changed
    artist_data = pth.request("artist", id=artist_id)

    # if no artist bio, add the one on last.fm
    if bio.missing(artist_data):
        print "Artist bio is missing..."
        bio.add(artist_data, lastfm, pth, config)

    pth.logout()

if __name__ == '__main__':
    main()
