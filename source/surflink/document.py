from resid import urlmod
from resid import document

from surflink import exception
from surflink import extract


class Link():
    '''Stores link along with other metadata'''
    def __init__(self, link, tag_name, tag_attrs, base_link=None, type=None,
    make_absolute=False, strict=False):
        self._link = link
        self._tag_name = tag_name
        self._tag_attrs = tag_attrs
        self._base_link = base_link
        self._type = type
        self._make_absolute = make_absolute
        self._strict = strict


        # base_link variable refers to base url of link.
        # link referes to url here not Link instance.
        if self._make_absolute:
            if base_link != None:
                self._link = urlmod.make_url_absolute(base_link, link)
            else:
                err_msg = "Base url is required to make url absoulute"
                raise exception.BaseUrlNotExists(err_msg)

        
        # Tries to guess content type.
        # Content type from html ha spriority over guessed one.
        if type:
            self._content_type = type
        else:
            #self._content_type = resid.guess_content_type(link)
            self._content_type = document.URL(link).content_type or ""

    def _is_head_resource(self):
        # Checks if link is resource usually loaded in head tag.
        return any([self.is_script(), self.is_linked()])

    def _matches_tag_name(self, tag_name):
        # Checks if tag name matches link tag name
        return self._tag_name.lower() == tag_name.lower()

    def _matches_content_type(self, content_type):
        # Checks if provided content type matches link content type
        if self._strict:
            # Only content type from markup will be considered.
            # In this case 'type' attribute supplies content type.
            # Content type will not be guessed from url.
            if self._type != None:
                return self._type.startswith(content_type)
            else:
                # Content type cannot be retrieved from markup.
                # strict denies guessing from url.
                return False
        else:
            # Content type may have been guessed from url.
            return self._content_type.startswith(content_type)

    def _matches_content_type_tag_name(self, content_type, tag_name):
        # Checks if arguments matches content type and tag name.
        # Outcomes of this method are affected by 'self._strict'.
        if self._matches_content_type(content_type):
            return True
        else:
            return self._matches_tag_name(tag_name)

    def get_link(self):
        return self._link

    def is_valid(self, strict=True):
        link = self._link.lower()
        if strict:
            #return resid.is_url(link)
            return document.URL(link).supported
        else:
            if set("<>^`{|}\s\n").intersection(link):
                return False
            elif link.startswith("#") or link.startswith("javascript:"):
                return False
            else:
                return False

    def is_resource(self):
        return self._tag_attrs == "src"

    def is_hyperlink(self):
        return self._tag_attrs == "href"

    def is_weblink(self):
        # return resid.is_weburl(self._link)
        return document.WebURL(self._link).supported

    def is_script(self):
        return self._matches_tag_name("script")

    def is_linked(self):
        return self._matches_tag_name("link")

    def is_image(self):
        return self._matches_content_type_tag_name("image/", "img")

    def is_audio(self):
        return self._matches_content_type_tag_name("audio/", "audio")

    def is_video(self):
        return self._matches_content_type_tag_name("video/", "video")

    def is_stylesheet(self):
        if self._strict and not self.is_linked():
            return False
        return self._matches_content_type("text/css")

    def is_javascript(self):
        if self._strict and not self.is_script():
            return False
        return self._matches_content_type("application/javascript")

    def is_webpage(self):
        if not self._is_head_resource():
            # return resid.find_resource(self._link).is_webpage()
            return document.WebURL(self._link).is_webpage()
        return False

    @property
    def absolute_link(self):
        if self._base_link != None:
            return urlmod.make_url_absolute(self._base_link, self._link)
        else:
            return self._link

    def __str__(self):
        return self._link

    def __repr__(self) -> str:
        output = "surflink.document.Link(link='{}', tag_name='{}', " +\
            "tag_attrs='{}', base_link={})"
        return output.format(self._link, self._tag_name, self._tag_attrs, 
        self._base_link)


class Links():
    '''Collection of multiple Link objects'''
    def __init__(self, links) -> None:
        # links: Iterable of links in string or bytes types.
        self._links = links

    def get_links(self):
        return self._links

    def get_raw_links(self):
        return list(map(lambda link:link.get_link(), self._links))

    def get_valid_links(self, strict=True):
        return list(filter((lambda link:link.is_valid(strict), self._links)))

    def get_absoulute_links(self):
        return list(map(lambda link:link.absolute_link, self._links))

    def get_resources(self):
        return list(filter(lambda link:link.is_resource(), self._links))

    def get_hyperlinks(self):
        return list(filter(lambda link:link.is_hyperlink(), self._links))

    def get_weblinks(self):
        return list(filter(lambda link:link.is_weblink(), self._links))

    def get_scripts(self):
        return list(filter(lambda link:link.is_script(), self._links))

    def get_linked(self):
        return list(filter(lambda link:link.is_linked(), self._links))

    def get_images(self):
        return list(filter(lambda link:link.is_image(), self._links))

    def get_videos(self):
        return list(filter(lambda link:link.is_video(), self._links))

    def get_audios(self):
        return list(filter(lambda link:link.is_audio(), self._links))

    def get_stylesheets(self):
        return list(filter(lambda link:link.is_stylesheet(), self._links))

    def get_javascripts(self):
        return list(filter(lambda link:link.is_javascript(), self._links))

    def get_webpages(self):
        return list(filter(lambda link:link.is_webpage(), self._links))

    def __iter__(self):
        return iter(self._links)
    
    def __len__(self):
        return len(self._links)

    def __getitem__(self, index):
        return self._links[index]

    def __str__(self):
        return str(self.get_raw_links())


class Document(Links):
    '''Template for instances containing links from HTML/XML document'''
    def __init__(self, markup, base_url=None, attrs=None, start_tag=None,
    unique=False, make_absoulute=False, strict=False):
        # markup: html/xml with links
        # url: url markup originates
        # attr: atributes of elements in markup to extract links.
        # unique: allows only unique links if enabled.
        super().__init__(list())
        self._markup = markup # markup containg links(html, xml)
        self._attrs = attrs # attributes to get links
        self._base_url = base_url # url of markup
        self._unique = unique
        self._start_tag = start_tag
        self._make_absoulute = make_absoulute
        self._strict = strict
        
        if not isinstance(markup, (str, bytes)):
            err_msg = "markup should be 'str' or 'bytes' not '{}'"
            raise TypeError(err_msg.format(self._markup.__class__.name))
        
        #if url!=None and resid.is_url(url):
        # if url!=None and urlmod.is_url(url):
        #     raise exception.URLError("'{}' is not url")

        # Setup links
        # Not recommended to call method within initializer.
        # But promise not to extend these methods.
        # That way there wont be problems unless extended.
        self._soup = self._create_soup()
        self._links = self._extract_links()

    def _create_soup(self):
        # Creates beutufulsoup to parse provided markup
        return extract.create_soup(self._markup)

    def _extract_links(self):
        # Creates link object containing links from markup
        links = []
        if self._start_tag != None:
            start_element = self._soup.find(self._start_tag)
            if not start_element:
                err_msg = "Tag '{}' does not exists"
                raise exception.TagNotExists(err_msg.format(self._start_tag))
        else:
            start_element = self._soup
        elements = extract.get_elements_with_links(start_element, self._attrs)
        for element in elements:
            link = extract.get_link_from_element(element, self._attrs)
            if link and not (self._unique and link in links):
                # Duplicate links not allowed if self._unique is True.
                # Link here refers to url not Link instance.
                tag_name = element.name
                attr_name = extract.get_element_attr_by_value(element, link)
                tag_type = extract.get_element_attr_value(element, "type")
                # Setups base url to pass to Link instance
                if self._base_url:
                    base_url = self._base_url
                else:
                    base_link = self._get_base_link()
                    if base_link:
                        base_url = base_link.get_link()
                    else:
                        base_url = None
                link_object = Link(link, tag_name, attr_name, base_url, 
                tag_type, self._make_absoulute, self._strict)
                links.append(link_object)
        return links

    def _get_base_link(self):
        element = self._soup.find("base")
        if element:
            return Link(element, "base", None)

    def get_base_link(self):
        # Gets base link for document
        return self._get_base_link()



if __name__ == "__main__":
    html = '''<a href='https://example.com/pages'>example</a>
    <a href='https://example.com/pages/main'>example</a>
    <img src='https://example.com/images/tree.png'></img>
    <iframe src='https://example.com/file-formats.html'></iframe>
    <div> contents </div>
    '''

    doc = Document(html)
    print(doc[0])