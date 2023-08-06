import random
import re

from .constants import ipv4_regex, ipv6_regex

def lighter(line):
    # https://en.wikipedia.org/wiki/ANSI_escape_code#SGR_(Select_Graphic_Rendition)_parameters

    # make style bold
    style = 1

    # just make text black
    textcolor = 30


    bg = random.randint(40,47)
    if bg == 40:
        #background is black so change textcolor to white
        textcolor = 97

    # add bright colors 50% chance
    if random.randint(0, 1):
        bg += 60

    format = ';'.join([str(style), str(textcolor), str(bg)])

    return '\x1b[%sm%s\x1b[0m' % (format, line)

def highlighter_ipv4(results):
    pattern = re.compile(ipv4_regex)
    ipv4s = pattern.findall(results)
    for ip in set(ipv4s):
        results = results.replace(ip, lighter(ip))
    print(results)

def highlighter_ipv6(results):
    ipv6_address = re.compile(ipv6_regex)

    ipv6s = ipv6_address.findall(results)
    for ip in set(ipv6s):
        results = results.replace(ip, lighter(ip))
    print(results)

def highlight_both(results):
    ipv6_address = re.compile(ipv6_regex)

    ipv6s = ipv6_address.findall(results)
    for ip in set(ipv6s):
        results = results.replace(ip, lighter(ip))

    pattern = re.compile(ipv4_regex)
    ipv4s = pattern.findall(results)
    for ip in set(ipv4s):
        results = results.replace(ip, lighter(ip))
    print(results)