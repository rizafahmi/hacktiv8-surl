import string
import shortuuid
import opengraph

from math import floor

BASE = string.digits + string.lowercase + string.uppercase
SHORT_SITE = 'http://localhost:5000'

def toBase62(num, b = 62):
    if b <= 0 or b > 62:
        return 0
    base = BASE
    r = num % b
    res = base[r]
    q = floor(num/b)
    while q:
        r = q % b
        q = floor(q/b)
        res = base[int(r)] + res
    return res

def toBase10(num, b = 62):
    base = BASE
    limit = len(num)
    res = 0
    for i in xrange(limit):
        res = b * res + base.find(num[i])
    return res

def generate_surl(url):
    return SHORT_SITE + '/r/' + shortuuid.uuid(name=url)

def get_metadata(url):
    from opengraph import OpenGraph
    site = OpenGraph(url="http://"+url)
    return site
