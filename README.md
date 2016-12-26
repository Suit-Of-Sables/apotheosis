# apotheosis
pull info from last.fm to populate an artist page on PTH

* Add similar artists
* Add missing artist bio
* Add missing artist image
* Add missing cover art for all albums in artist's discography (!)
* All images, new or existing, are rehosted on ptpimg if on a bad host

There are still bugs to be found.

#### Note: the following bug seems to have been resolved with a quick fix using clean_body() in image.py
#### but keep an eye on the bio sections just in case
One thig I've noticed is that if you use it as is on an artist missing an artist image but with an existing bio, the bio gets garbled with xml tags.
The problem is that you can't edit _just_ the image or _just_ the bio because if you don't send a value for the other field when running the edit action via php it just deletes what wasn't given a field instead of just not changing it.

This isn't so much a problem for the image as you can grab the image from the pth api and then send that along with the edit action.
The issue is that the api will give you the bio (called 'body') in XML but if you give that back to the edit action it doesn't understand the tags. It wants BBCode.

1. clone the [github repo](https://github.com/Suit-Of-Sables/apotheosis)

2. install pylast <code>$ pip install --user pylast</code>

3. make a [last.fm API account](https://www.last.fm/api) (you'll need the auth keys for the config)

4. If you are a PTP member you can make a [ptpimg account](https://ptpimg.me) to take advantage of the rehosting feature.

5. copy and fill out the config file (remember to quote all strings!) <code>$ cp config.py.template config.py</code>

Example Usage: <code>$ ./apotheosis 1234 </code>
Runs script on artist with id=1234

### Copy Apotheosis Command Link

Here's a [browser script](https://greasyfork.org/en/scripts/25992-pth-apotheosis-link-creator) that will add an 'Apotheosis' link at the top of the artist's page.
![Apotheosis Command Link](https://ptpimg.me/wann7v.png)

Clicking the link will copy the command to run the script on that artist just like in the above usage example.
