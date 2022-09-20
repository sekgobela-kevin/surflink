from resid import urlmod
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

    def is_resource(self):
        return self.tag_attr == "src"

    def is_hyperlink(self):
        return self.tag_attr == "href"

    def is_script(self):
        return self.tag_name.lower() == "script"

    def is_linked(self):
        return self.tag_name.lower() == "link"

    @property
    def absolute_link(self):
        if self.base_link != None:
            return urlmod.make_url_absolute(self.base_link, self.link)
        else:
            return self.link


    

class Document():
    '''Template for instances containing links from HTML/XML'''
    def __init__(self, markup, url=None, attrs=("src", "href"), unique=True):
        self._markup = markup # markup containg links(html, xml)
        self._attrs = attrs # attributes to get links
        self._url = url # url of markup
        if url!=None and resid.is_url(url):
            raise exception.URLError("'{}' is not url")
        self._unique = unique

        # Setup links
        self._soup = self._create_soup()
        self._links = self._create_links()

    def _create_soup(self):
        # Creates beutufulsoup to parse provided markup
        return extract.create_soup(self._url)

    def _create_links(self):
        # Creates link object containing links from markup
        links = []
        elements = extract.get_elements_with_links(self._soup, self._attrs)
        for element in elements:
            link = extract.get_link_from_element(element, self._attrs)
            if link and not (self._unique and link in links):
                # Duplicate links not allowed if self._unique is True.
                tag_name = link.name
                attr_name = extract.get_element_attr_by_value(element, link)
                link_object = Link(link, tag_name, attr_name, self._url)
                links.add(link_object)
        return links

    def get_resource_links(self):
        return list(filter(lambda link:link.is_resource(), self._links))

    def get_hyperlinks(self):
        return list(filter(lambda link:link.is_hyperlinks(), self._links))

    def get_script_links(self):
        return list(filter(lambda link:link.is_script(), self._links))

    def get_linked_links(self):
        return list(filter(lambda link:link.is_linked(), self._links))

    def get_absoulute_links(self):
        return list(map(lambda link:link.absolute_link, self._links))
