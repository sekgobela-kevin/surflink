from surflink import document
from resid import urlmod


__all__ = [
    "filter_raw_valid_urls",
    "filter_valid_urls",
    "filter_urls_by_scheme",
    "filter_urls_by_hostname",

    "make_url_absoulute",
    "make_urls_absoulute",

    "create_document",
    "create_link",
    "get_urls_from_links",

    "extract_urls",
    "extract_script_urls",
    "extract_resource_urls",
    "extract_hyperlink_urls",
    "extract_weblink_urls",

    "extract_webpage_urls",
    "extract_stylesheet_urls",
    "extract_video_urls",
    "extract_image_urls",
    "extract_audio_urls",

    "extract_stylesheet_urls",
    "extract_javascript_urls",
    "extract_html_urls"
]


def get_urls_from_links(links):
    '''Gets links from collection of Link objects'''
    return document.Links(links).get_raw_links()


def filter_raw_valid_urls(raw_urls):
    '''Filters urls directly from html based on their raw validity. These 
    urls may lack scheme or hostname due to being relative'''
    links_obj = document.Links(raw_urls)
    links = links_obj.get_raw_links(False)
    return get_urls_from_links(links)

def filter_valid_urls(urls):
    '''Fiters urls based on their validity.'''
    # Valid url contain atleast scheme and another part.
    links_obj = document.Links(urls)
    links = links_obj.get_valid_links(False)
    return get_urls_from_links(links)

def filter_urls_by_scheme(urls, scheme):
    '''Filters urls by their schemes'''
    def func(url):
        return urlmod.extract_scheme(url) == scheme
    return list(filter(func, urls))

def filter_urls_by_hostname(urls, hostname):
    '''Filters urls by their hostnames'''
    def func(url):
        return urlmod.extract_hostname(url) == hostname
    return list(filter(func, urls))


def make_url_absoulute(base_url, url):
    '''Makes url absoulute by joing with its base url'''
    return urlmod.make_url_absolute(base_url, url)

def make_urls_absoulute(base_url, urls):
    '''Makes urls absoulute by joing them with their base url'''
    return [make_url_absoulute(base_url, url) for url in urls]


def create_document(html_markup, **kwargs):
    '''Creates document containing links from html'''
    return document.Document(html_markup, **kwargs)

def create_link(url, tag_name, tag_attr, **kwargs):
    '''Creates Link object'''
    return document.Link(tag_name, tag_attr, **kwargs)

def create_links(links):
    '''Creates Links object from collection of Link objects'''
    return document.Links(links)


def extract_urls(html_markup, **kwargs):
    '''Extracts all urls within markup'''
    doc_object = create_document(html_markup, **kwargs)
    return doc_object.get_raw_links()

def extract_script_urls(html_markup, **kwargs):
    '''Extracts urls that serves scripts including javascript'''
    doc_object = create_document(html_markup, **kwargs)
    links = doc_object.get_scripts()
    return get_urls_from_links(links)

def extract_resource_urls(html_markup, **kwargs):
    '''Extracts urls that serve resources including stylesheets, images'''
    doc_object = create_document(html_markup, **kwargs)
    links = doc_object.get_resources()
    return get_urls_from_links(links)

def extract_hyperlink_urls(html_markup, **kwargs):
    '''Extracts urls that references other webpages('a' tag urls)'''
    doc_object = create_document(html_markup, **kwargs)
    links = doc_object.get_scripts()
    return get_urls_from_links(links)

def extract_weblink_urls(html_markup, **kwargs):
    '''Extracts urls used in World Wide Web(http, https, ftp). This covers
    only urls with 'http', 'https' or 'ftp' schemes.'''
    doc_object = create_document(html_markup, **kwargs)
    links = doc_object.get_weblinks()
    return get_urls_from_links(links)

def extract_webpage_urls(html_markup, **kwargs):
    '''Extracts urls resembling webpages(including html urls). Html url
    within script tag wont be considered webpage even if it may be html.'''
    doc_object = create_document(html_markup, **kwargs)
    links = doc_object.get_webpages()
    return get_urls_from_links(links)

def extract_video_urls(html_markup, **kwargs):
    '''Extracts urls for videos.'''
    doc_object = create_document(html_markup, **kwargs)
    links = doc_object.get_videos()
    return get_urls_from_links(links)

def extract_image_urls(html_markup, **kwargs):
    '''Extracts urls for images.'''
    doc_object = create_document(html_markup, **kwargs)
    links = doc_object.get_images()
    return get_urls_from_links(links)

def extract_audio_urls(html_markup, **kwargs):
    '''Extracts urls for audios.'''
    doc_object = create_document(html_markup, **kwargs)
    links = doc_object.get_images()
    return get_urls_from_links(links)

def extract_stylesheet_urls(html_markup, **kwargs):
    '''Extracts urls for stylesheet(including css).'''
    doc_object = create_document(html_markup, **kwargs)
    links = doc_object.get_stylesheets()
    return get_urls_from_links(links)

def extract_javascript_urls(html_markup, **kwargs):
    '''Extracts urls for for javascript(js).'''
    doc_object = create_document(html_markup, **kwargs)
    links = doc_object.get_javascripts()
    return get_urls_from_links(links)

def extract_html_urls(html_markup, **kwargs):
    '''Extracts urls for html even if its within script or link tag'''
    doc_object = create_document(html_markup, **kwargs)
    links = doc_object.get_htmls()
    return get_urls_from_links(links)


def extract_base_url(html_markup, **kwargs):
    '''Extracts base url from html'''
    doc_object = create_document(html_markup, **kwargs)
    base_link = doc_object.get_base_link()
    if base_link:
        return base_link.get_link()
