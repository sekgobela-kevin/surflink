# surflink
Surflink extracts links/urls from html markup with ability to choose
which urls to be extracted. Instead of extracting all urls from
html, specific urls like images can be extracted while leaving the rest.
Urls by default can only be extracted if they are within __href__ and 
__src__ attributes of tags.

Type of url is determined from the tag of url and also content type guessed
from the url. __strict__ argument can be passed to most functions which
allows to determine type of url from its tag other than guessed content type.
That would make image url to be matched only if its within 'img' tag but 
wont be matched if not within tag even if it has image extension.

Other functions operating on urls also exits such as making urls absolute
or filtering them based on their scheme or hostname. 
[resid](https://github.com/sekgobela-kevin/resid) provides more features
for operating with urls and others which surflink does not provide but
may be valuable.

### Installing
This is enough into your command-line application(python required):
```bash
pip install surflink
```

### Usage
First import surflink to use its functions.
```python
>>> import resid
```

This html sample will be used for code examples examples to follow.
```html
<html>
    <head>
        <base href="https://example.com/">
        <script src='https://example.com/startup.js' 
        type="application/javascript"></script>
        <script src='https://example.com/jquery.js'></script>
        <link rel="stylesheet" href='https://example.com/w3.css'>
    </head>
    <body>
        <iframe src='https://example.com/great_river.html'></iframe>
        <img src='https://example.com/pages/elephant.png'>
        <audio src='https://example.com/audios/hiphop_beat.mp3'></audio>
        <video src='https://example.com/audios/underground.mp4'></video>
        
        Random Links
        <a href='/pages/world'>world</a><br>
        <a href='https://example.com/pages/tree.png'>tree image</a><br>
        <a href="https://en.wikipedia.org/wiki/Food">food</a>
    </body>
</html>
```

Take it as part of code samples to follow as variable `html_sample` has been
defined before it.
```python
# This variable contains above html as string.
>>> html_sample = ...
```

Here urls for images and javascript get extracted from html. All functions
that extract urls accept the same argument but may return different urls.
```python
# Extracts urls for images no matter where they are from.
>>> surflink.extract_image_urls(html_sample)
['https://example.com/pages/elephant.png', 'https://example.com/pages/tree.png']
```
```python
# Does the same with javascript urls.
>>> surflink.extract_javascript_urls(html_sample)
['https://example.com/startup.js', 'https://example.com/jquery.js']
```

Realise that 'https://example.com/pages/tree.png' was matched as image just
because of its extension even if it was not in __img__ tags or stated that
its an image url. `strict` argument does exatly in that url type will be 
determined based on whats on html not guessed content type.
```python
# Now only image urls with 'img' tag will be extracted.
# Unless type attribute is set to something else not being image.
>>> surflink.extract_image_urls(html_sample, strict=True)
['https://example.com/pages/elephant.png']
```

Sometimes urls with html may be relative to other urls and it may happen
that their absolute version is needed. That would require making url
absolute using whatever url it is based on usually can be found within
the html but sometimes it may need to be provided explicitely.

There is url '/pages/world' which is relative but we need it to be absolute
like other urls. Its now easier as our html already contains base url which
is internally used to make url absolute.
```python
# Realise that '/pages/world' is absolute and missing scheme and domain.
>>> surflink.extract_webpage_urls(html_sample)
[..., '/pages/world', 'https://en.wikipedia.org/wiki/Food']
```
```python
# But here scheme and domain were added automatically.
>>> surflink.extract_webpage_urls(html_sample, make_absolute=True)
[..., 'https://example.com/pages/world', 'https://en.wikipedia.org/wiki/Food']
# Base url can be provided with 'base_url' argument if your html does
# not provide one or want to overide html base url.
surflink.extract_webpage_urls(html_sample, base_url="https://example.com/" 
make_absolute=True)
```

Urls can be made absolute without requiring extracting them from html.
```python
# Makes single url absolute
>>> surflink.make_url_absoulute(base_url="https://example.com/", url="/pages/world")
'https://example.com/pages/world'
```
```python
# Makes multiple urls absolute
>>> urls = ["/pages/world", "//example.com/pages/elephant.png"]
>>> surflink.make_urls_absoulute(base_url="https://example.com/pages", urls=urls)
['https://example.com/pages/world', 'https://example.com/pages/elephant.png']
```

There exists other arguments on functions that extracts urls such as `attrs` 
which specifies attributes to extract urls and `start_tag` which specifies
tag name to start extracting urls and lastly `unique` which ensures function
returns unique urls.
```python
>>> surflink.extract_javascript_urls(html_sample, attrs=("src", "href"), start_tag="html", strict=False)
['https://example.com/startup.js', 'https://example.com/jquery.js']
```

> Functions here are just few of other functions that exists in surflink.

### License
[MIT license](https://github.com/sekgobela-kevin/surflink/blob/main/LICENSE)

