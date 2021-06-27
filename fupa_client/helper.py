from .fupa_remote_datasource import FupaRemoteDatasource

base_url = 'https://www.fupa.net'


def soup_of_page(url):
    datasource = FupaRemoteDatasource(url)
    soup = datasource.scrap_page()
    if not soup:
        raise Exception('false url' + url)
    return soup
