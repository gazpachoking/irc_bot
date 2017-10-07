import re

from six.moves.html_parser import HTMLParser


def printable_unicode_list(unicode_list):
    return '[{}]'.format(', '.join(str(x) for x in unicode_list))


def is_channel(string):
    """
    Return True if input string is a channel
    """
    return string and string[0] in "#&+!"


def strip_irc_colors(data):
    """Strip mirc colors from string. Expects data to be decoded."""
    return re.sub('[\x02\x0F\x16\x1D\x1F]|\x03(\d{1,2}(,\d{1,2})?)?', '', data)


def strip_invisible(data):
    """Strip stupid characters that have been colored 'invisible'. Assumes data has been decoded"""
    stripped_data = ''
    i = 0
    while i < len(data):
        c = data[i]
        if c == '\x03':
            match = re.match('^(\x03(?:(\d{1,2})(?:,(\d{1,2}))(.?)?)?)', data[i:])
            # if the colors match eg. \x031,1a, then "a" has same foreground and background color -> invisible
            if match and match.group(2) == match.group(3):
                if match.group(4) and ord(match.group(4)) > 31:
                    c = match.group(0)[:-1] + ' '
                else:
                    c = match.group(0)
                i += len(c) - 1
        i += 1
        stripped_data += c
    return stripped_data


def decode_html(data):
    """Decode dumb html"""
    h = HTMLParser()
    return h.unescape(data)