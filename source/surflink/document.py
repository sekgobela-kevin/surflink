from resid import urlmod
from resid import document

from surflink import exception
from surflink import extract


# Map containing tag names and possible content types.
TAG_NAMES_CONTENT_TYPES = {
    "img": "image/x",
    "video": "video/x",
    "audio": "audio/x",
    "iframe": "text/html",
    "script": "application/javascript"
}

class Link():
    '''Stores link along with other metadata'''
    def __init__(self, link, tag_name, tag_attr, base_link=None, type=None,
    rel_attr=None, make_absolute=False, strict=False):
        self._link = link
        self._tag_name = tag_name
        self._tag_attr = tag_attr
        self._base_link = base_link
        self._type = type
        self._rel_attr = rel_attr
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

        
        # Tries to find/guess content type.
        # Content type from html has priority over guessed one.
        tag_name_lower = self._tag_name.lower()
        if type:
            self._content_type = type
        elif self._rel_attr and self._rel_attr == "stylesheet":
            # Since type not provided then its considered css.
            self._content_type = "text/css"
        elif tag_name_lower in TAG_NAMES_CONTENT_TYPES:
            # Guessed content type is preffered when it follows 
            # content type from tag name.
            guessed_content_type = document.URL(link).content_type
            tag_content_type = TAG_NAMES_CONTENT_TYPES[tag_name_lower]
            if guessed_content_type:
                if tag_content_type.endswith("/x"):
                    # Checks if first parts of contents are same.
                    # This helps decide if guessed content type be used.
                    guessed_start = guessed_content_type.split("/")[0]
                    tag_start = tag_content_type.split("/")[0]
                    if guessed_start == tag_start:
                        self._content_type = guessed_content_type
            # Checks if content type is defined and if not define one.
            # Tag content type is used since guessed did not pass.
            if not hasattr(self, "_content_type"):
                self._content_type = tag_content_type
        elif not self._strict:
            # Content type is now guessed from url since its not strict.
            if self._is_valid(False):
                # Link without extension will be considered html.
                # Its important to know if link is valid.
                #self._content_type = resid.guess_content_type(link)
                self._content_type = document.WebURL(link).content_type or ""
            else:
                self._content_type = ""
        else:
            self._content_type = ""


    def _is_head_resource(self):
        # Checks if link is resource usually loaded in head tag.
        return self._tag_name.lower() in ["link", "script"]

    def _matches_tag_name(self, tag_name):
        # Checks if tag name matches link tag name
        return self._tag_name.lower() == tag_name.lower()

    def _matches_tag_attr(self, tag_attr):
        # Checks if tag name matches link tag name
        return self._tag_attr.lower() == tag_attr.lower()

    def _matches_content_type(self, content_type):
        # Checks if provided content type matches link content type
        if self._content_type:
            # Content type may be from different places like tag name,
            # tag attributes or guessed from url extension.
            return self._content_type.startswith(content_type)
        else:
            # Content type is not available(strict may have been enabled)
            return False

    def _matches_content_type_tag_name(self, content_type, tag_name):
        # Checks if arguments matches content type and tag name.
        # Outcomes of this method are affected by 'self._strict'.
        if self._matches_content_type(content_type):
            return True
        else:
            return self._matches_tag_name(tag_name)

    def _is_valid(self, strict=True):
        # Checks if link is valid.
        link = self._link.lower()
        if strict:
            #return resid.is_url(link)
            return document.URL(link).supported
        else:
            if set("<>^`{|} \n").intersection(link):
                return False
            elif link.startswith("#") or link.startswith("javascript:"):
                return False
            else:
                return True

    def get_link(self):
        return self._link

    def get_absolute_link():
        # Returns absolute version of link(url).
        if self._base_link != None:
            return urlmod.make_url_absolute(self._base_link, self._link)
        else:
            err_msg = "Base url is required to make url absoulute"
            raise exception.BaseUrlNotExists(err_msg)
    
    def is_valid(self, strict=True):
        return self._is_valid(strict)

    def is_resource(self):
        return self._matches_tag_attr("src") or self._is_head_resource()

    def is_hyperlink(self):
        return self._matches_tag_name("a")

    def is_weblink(self):
        # Checks if link is world Wide Web link.
        # Only if link contains http, https or ftp schemes.
        try:
            absolute_link = self.get_absolute_link()
        except exception.BaseUrlNotExists:
            absolute_link = self._link
        finally:
            # return resid.is_weburl(self._link)
            return document.WebURL(absolute_link).supported

    def is_script(self):
        if self._matches_tag_name("script"):
            return True
        elif not self._strict:
            # Javascript url is also script url no matter if its within
            # 'script' tag.
            return self._matches_content_type("application/javascript")
        else:
            return False

    def is_linked(self):
        return self._matches_tag_name("link")

    def is_image(self):
        return self._matches_content_type("image/")

    def is_audio(self):
        return self._matches_content_type("audio/")

    def is_video(self):
        return self._matches_content_type("video/")

    def is_stylesheet(self):
        if self._strict and not self.is_linked():
            return False
        elif self.self._rel_attr:
            return self.self._rel_attr.lower() == "stylesheet"
        else:
            return self._matches_content_type("text/css")

    def is_javascript(self):
        if self._strict and not self.is_script():
            return False
        else:
            # If type for script not provided then its javascript.
            if self._type == None and self.is_script():
                return True
            return self._matches_content_type("application/javascript")

    def is_html(self):
        # Checks if link is refers to html file.
        matches_content_type = self._matches_content_type("text/html")
        # matches_content_type will be True even if url lacks extension.
        if matches_content_type and self._is_head_resource():
            # Avoid matching head resources as html when extension is 
            # missing. This only applies when strict is not enabled.
            weburl_type = document.URL(self._link).content_type
            # weburl_type will be html even if it lacks extension.
            if weburl_type == self._content_type:
                # Content type may have been guessed from url.
                # Url may have been made html even if it lacks extension.
                url_type = document.WebURL(self._link).content_type
                # url_type wont be html if it lacks extension.
                return url_type == "text/html"
        return matches_content_type

    def is_webpage(self):
        if self._is_head_resource():
            # Webpage will never be head resource unlike html.
            # Even if its type is html, its just not webpage.
            return False
        else:
            return self.is_html()

    @property
    def link(self):
        return self._link

    @property
    def absolute_link(self):
        return self.get_absolute_link()

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

    def get_htmls(self):
        return list(filter(lambda link:link.is_html(), self._links))

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
    unique=False, make_absolute=False, strict=False):
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
        self._make_absolute = make_absolute
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
        # Setups base url to pass to Link instance
        base_link = self._get_base_link()
        if base_link:
            base_url = base_link.get_link()
        else:
            base_url = None
        # Setups start element to use to get urls from markup
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
                tag_rel = extract.get_element_attr_value(element, "rel")
                # Creates Link object from collected data.
                link_object = Link(link, tag_name, attr_name, base_url, 
                tag_type, tag_rel, self._make_absolute, self._strict)
                if link_object.is_valid(False):
                    links.append(link_object)
        return links

    def _get_base_link(self):
        # Gets base link for markup.
        if self._base_url:
            return Link(self._base_url, "", None)
        else:
            element = self._soup.find("base")
            if element:
                base_url = extract.get_element_attr_value(element, "href")
                if base_url:
                    return Link(base_url, "base", None)

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