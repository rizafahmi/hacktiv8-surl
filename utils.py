import string
import shortuuid
import opengraph

from math import floor

SHORT_SITE = 'http://localhost:5000'

def generate_surl(url):
    return SHORT_SITE + '/r/' + shortuuid.uuid(name=url)

def get_metadata(url):
    from opengraph import OpenGraph
    site = OpenGraph(url=url)
    return site
