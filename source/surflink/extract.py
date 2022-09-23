from bs4 import BeautifulSoup


# Elements attributes to get links
ATTRS = ("src", "href")

def create_soup(markup):
    # Creates beutufulsoup to parse provided markup
    return BeautifulSoup(markup, 'html.parser')

def get_element_attrs_values(element, attrs):
    # Gets attributes values from bs4 element
    return [element[attr] for attr in attrs if element.has_attr(attr)]

def get_elements_by_name(soup, name):
    # Gets elemenets by their tag names
    return soup.find_all(name)


def get_elements_with_links(soup, attrs=None):
    # Gets elements containing links in their attributes
    if attrs == None:
        attrs = ATTRS
    # Creates css pattern to match elements with provided attributes
    # Output: '[href], [src]
    css_pattern = ["[" + attr + "]" for attr in attrs]
    css_pattern = ", ".join(css_pattern)
    return soup.select(css_pattern)

def get_links_from_element(element, attrs=None):
    # Gets links from attributes of element.
    # src and href are ones likely to contain links.
    if attrs == None:
        attrs = ATTRS
    return get_element_attrs_values(element, attrs)

def get_link_from_element(element, attrs=None):
    # gets link from attributes of element
    if attrs == None:
        attrs = ATTRS
    links = get_element_attrs_values(element, attrs)
    if links:
        return links[0]

def get_links_from_elements(elements, attrs=None):
    # Gets links from collection of bs4 elements
    links = []
    for element in elements:
        links.extend(get_links_from_element(element, attrs))
    return links

def get_element_attr_value(element, attr):
    # Gets element attribute value
    if element.has_attr(attr):
        return element[attr]

def get_element_attr_by_value(element, value):
    # Gets attribute of element with provided value
    try:
        index = list(element.attrs.values()).index(value)
        return list(element.attrs.keys())[index]
    except ValueError:
        pass


if __name__ == "__main__":
    pass