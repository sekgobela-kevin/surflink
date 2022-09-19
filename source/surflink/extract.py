from bs4 import BeautifulSoup


def create_soup(markup):
    # Creates beutufulsoup to parse provided markup
    return BeautifulSoup(markup, 'html.parser')

def get_element_attrs_values(element, attrs):
    # Gets attributes values from bs4 element
    return [element[attr] for attr in attrs if element.has_attr(attr)]

def get_elements_by_name(soup, name):
    # Gets elemenets by their tag names
    return soup.find_all(name)


def get_links_from_element(element, attrs=None):
    # Gets links from attributes of element.
    # src and href are ones likely to contain links.
    if attrs == None:
        attrs = ["src", "href"]
    return get_element_attrs_values(element, attrs)

def get_links_from_elements(elements, attrs=None):
    # Gets links from collection of bs4 elements
    links = []
    for element in elements:
        links.extend(get_links_from_element(element, attrs))
    return links


if __name__ == "__main__":
    pass