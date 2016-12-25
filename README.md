# apotheosis
pull info from last.fm to populate an artist page on PTH

* Add similar artists
* Add missing artist bio
* Add missing artist image (a next step would be to host it to ptpimg.me first or rehost an existing image)

There are still bugs to be found.

#### Note: the following bug seems to have been resolved with a quick fix using clean_body() in image.py
#### but keep an eye on the bio sections just in case
One thig I've noticed is that if you use it as is on an artist missing an artist image but with an existing bio, the bio gets garbled with xml tags.
The problem is that you can't edit _just_ the image or _just_ the bio because if you don't send a value for the other field when running the edit action via php it just deletes what wasn't given a field instead of just not changing it.

This isn't so much a problem for the image as you can grab the image from the pth api and then send that along with the edit action.
The issue is that the api will give you the bio (called 'body') in XML but if you give that back to the edit action it doesn't understand the tags. It wants BBCode.

1. clone the [github repo](https://github.com/Suit-Of-Sables/apotheosis)

2. install pylast <code>$ pip install --user pylast</code>

3. make a [last.fm API account](http://www.last.fm/api) (you'll need the auth keys for the config)

4. copy and fill out the config file<code>$ cp config.py.template config.py</code>

Example Usage: <code>$ ./apotheosis 1234 </code>
Runs script on artist with id=1234
