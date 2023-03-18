from project import *
import pytest

def test_get_html():
    assert type(get_html('https://www.amazon.com/s?k=socks&rh=n%3A7141123011%2Cn%3A2376200011&dc&ds=v1%3ASTAAoyV4opHLhrdv52LnOQCm6cmazrb2ktXk9SlAB00&qid=1672082768&rnid=2941120011&ref=sr_nr_n_5', 1).text) == str
    assert get_html('https://www.amazon.com/s?k=socks&rh=n%3A7141123011%2Cn%3A2376200011&dc&ds=v1%3ASTAAoyV4opHLhrdv52LnOQCm6cmazrb2ktXk9SlAB00&qid=1672082768&rnid=2941120011&ref=sr_nr_n_5', 1).status_code == 200 or 401 or 503

def test_get_proxy():
    assert type(get_proxy()) == dict
    assert list(get_proxy().keys()) == ['http', 'adress'] or ['https', 'adress']


def test_file_name():
    assert type(file_name()) == str