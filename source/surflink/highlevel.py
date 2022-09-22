from surflink import document
from resid import urlmod


def filter_raw_valid_urls(raw_urls):
    # Filters urls directly from html based on their validity.
    # Raw urls from html may lack scheme or hostname.
    links_obj = document.Links(raw_urls)
    return links_obj.get_valid_links(False)

def filter_valid_urls(urls):
    # Fiters urls based on their validity.
    # Valid url contain atleast scheme and other parts.
    links_obj = document.Links(urls)
    return links_obj.get_valid_links(True)

def filter_urls_by_scheme(urls, scheme):
    # Filters urls by their schemes
    return list(filter(lambda url:urlmod.extract_scheme(url) == scheme))

def make_url_absoulute(base_url, url):
    # Makes url absoulute by joing with its base url
    return urlmod.make_url_absolute(base_url, url)

def make_urls_absoulute(base_url, urls):
    # Makes urls absoulute by joing them with their base url
    return [make_url_absoulute(base_url, url) for url in urls]

def create_document(html_markup, attrs=None, unique=False):
    # Creates document containing links from html
    return document.Document(html_markup, attrs,unique)

def create_link(url, tag_name, tag_attr, base_link=None):
    # Creates Link object
    return document.Link(tag_name, tag_attr, base_link)


def get_links_from_link_objects(link_objs):
    # Gets links from collection of Link objects
    return document.Links(link_objs).get_raw_links()

def extract_all_urls(html_markup):
    # Extracts all urls from html
    doc_object = create_document(html_markup)
    links = doc_object.get_raw_links()
    return get_links_from_link_objects(links)

def extract_script_urls(html_markup):
    # Extracts urls that serves scripts
    doc_object = create_document(html_markup)
    links = doc_object.get_scripts()
    return get_links_from_link_objects(links)

def extract_resource_urls(html_markup):
    # Extracts urls that serve resources
    doc_object = create_document(html_markup)
    links = doc_object.get_resources()
    return get_links_from_link_objects(links)

def extract_hyperlink_urls(html_markup):
    # Extracts urls that referrences other webpages
    doc_object = create_document(html_markup)
    links = doc_object.get_scripts()
    return get_links_from_link_objects(links)

def extract_webpage_urls(html_markup):
    # Extracts urls used in World Wide Web(http, https, ftp)
    doc_object = create_document(html_markup)
    links = doc_object.get_weblinks()
    return get_links_from_link_objects(links)

def extract_webpage_urls(html_markup):
    # Extracts urls for webpages.
    doc_object = create_document(html_markup)
    links = doc_object.get_webpages()
    return get_links_from_link_objects(links)

def extract_videos_urls(html_markup):
    # Extracts urls for videos.
    doc_object = create_document(html_markup)
    links = doc_object.get_videos()
    return get_links_from_link_objects(links)

def extract_images_urls(html_markup):
    # Extracts urls for images.
    doc_object = create_document(html_markup)
    links = doc_object.get_images()
    return get_links_from_link_objects(links)

def extract_audios_urls(html_markup):
    # Extracts urls for audios.
    doc_object = create_document(html_markup)
    links = doc_object.get_images()
    return get_links_from_link_objects(links)
