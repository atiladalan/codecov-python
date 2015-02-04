import re


IGNORE = re.compile(r'^((vendor/)|(\$\{))')


def from_xml(xml):
    coverage = {}
    for f in getattr(xml, "iter", "findall")('file'):
        path = f.attrib['name']
        if IGNORE.match(path):
            continue
        elif f.find('line') is None:
            continue

        lines = [None]*(max([int(line.attrib['num']) for line in getattr(f, 'iter', 'findall')('line')] or [0])+1)
        if len(lines) > 1:
            for line in getattr(f, 'iter', 'findall')('line'):
                lines[int(line.attrib['num'])] = int(line.attrib['count'] or 0)
        lines[0] = None
        # skip last line
        lines.pop(-1)
        coverage[path] = lines

    return dict(coverage=coverage)
