# apotheosis
pull info from last.fm to populate an artist page on PTH

* Add similar artists
* Add missing artist bio
* Add missing artist image (a next step would be to host it to ptpimg.me first or rehost an existing image)

There are still plenty of bugs.
The main one being that if you use it as is on an artist missing an artist image but with an existing bio, the bio gets garbled with html tags.
The problem is that you can't edit _just_ the image or _just_ the bio because if you don't send a value for the other field when running the edit action via php it just deletes what wasn't given a field instead of just not changing it.

This isn't so much a problem for the image as you can grab the image from the pth api and then send that along with the edit action.
The issue is that the api will give you the bio (called 'body') in XML but if you give that back to the edit action it doesn't understand the tags. It wants BBCode.

Anyway I might have a rough fix for that coming soon, but this is something odd about the gazelle api in general me thinks.


requires pylast

<code>pip install pylast</code>

Copy and fill out the config file
<code>cp apotheosis.config.template apotheosis</code>

You'll need a last.fm api account for some of the keys

Example Usage:
<code>python ./apotheosis 1234 #run script on artist with id=1234</code>
