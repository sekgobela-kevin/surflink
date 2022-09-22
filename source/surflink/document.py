from resid import urlmod
from resid import document
import resid

from surflink import exception
from surflink import extract


class Link():
    '''Stores link along with other metadata'''
    def __init__(self, link, tag_name, tag_attr, base_link=None):
        self.link = link
        self.tag_name = tag_name
        self.tag_attr = tag_attr
        self.base_link = base_link
        #self.content_type = resid.guess_content_type(link)
        self.content_type = document.URL(link).content_type or ""

    def is_valid(self, strict=True):
        link = self.link.lower()
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
        return self.tag_attr == "src"

    def is_hyperlink(self):
        return self.tag_attr == "href"

    def is_weblink(self):
        # return resid.is_weburl(self.link)
        return document.WebURL(self.link).supported

    def is_script(self):
        return self.tag_name.lower() == "script"

    def is_linked(self):
        return self.tag_name.lower() == "link"

    def is_image(self):
        return "image/" in self.content_type

    def is_audio(self):
        return "image/" in self.content_type

    def is_video(self):
        return "video/" in self.content_type

    def is_text(self):
        return "text/" in self.content_type

    def is_webpage(self):
        if not (self.is_script() or self.is_linked()):
            # return resid.find_resource(self.link).is_webpage()
            return document.WebURL(self.link).is_webpage()
        return False

    @property
    def absolute_link(self):
        if self.base_link != None:
            return urlmod.make_url_absolute(self.base_link, self.link)
        else:
            return self.link

    def __str__(self):
        return self.link

    def __repr__(self) -> str:
        output = "surflink.document.Link(link='{}', tag_name='{}', " +\
            "tag_attr='{}', base_link={})"
        return output.format(self.link, self.tag_name, self.tag_attr, 
        self.base_link)


class Links():
    '''Collection of multiple Link objects'''
    def __init__(self, links) -> None:
        # links: Iterable of links in string or bytes types.
        self._links = links

    def get_links(self):
        return self._links

    def get_raw_links(self):
        return list(map(lambda link:link.link, self._links))

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

    def get_texts(self):
        return list(filter(lambda link:link.is_text(), self._links))

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
    def __init__(self, markup, url=None, attrs=("src", "href"), unique=False):
        # markup: html/xml with links
        # url: url markup originates
        # attr: atributes of elements in markup to extract links.
        # unique: allows only unique links if enabled.
        super().__init__(list())
        self._markup = markup # markup containg links(html, xml)
        self._attrs = attrs # attributes to get links
        self._url = url # url of markup
        if url!=None and resid.is_url(url):
            raise exception.URLError("'{}' is not url")
        self._unique = unique

        # Setup links
        # Not recommended to call method within initializer.
        self._soup = self._create_soup()
        self._links = self._extract_links()

    def _create_soup(self):
        # Creates beutufulsoup to parse provided markup
        return extract.create_soup(self._markup)

    def _extract_links(self):
        # Creates link object containing links from markup
        links = []
        elements = extract.get_elements_with_links(self._soup, self._attrs)
        for element in elements:
            link = extract.get_link_from_element(element, self._attrs)
            if link and not (self._unique and link in links):
                # Duplicate links not allowed if self._unique is True.
                tag_name = element.name
                attr_name = extract.get_element_attr_by_value(element, link)
                link_object = Link(link, tag_name, attr_name, self._url)
                links.append(link_object)
        return links


if __name__ == "__main__":
    html = '''<a href='https://example.com/pages'>example</a>
    <a href='https://example.com/pages/main'>example</a>
    <img src='https://example.com/images/tree.png'></img>
    <iframe src='https://example.com/file-formats.html'></iframe>
    <div> contents </div>
    '''

    doc = Document(html)
    print(doc[0])