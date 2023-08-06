"""

A command line tool to generate html tables with embedded images, videos and audio

- Separate columns with `,` or pass all files and group by parent using `--groupy_nthparent 1`
- The easiest way to use it is to put each column in a folder and then pass it using a wildcard `*`


Examples:

    htmltable col1/*.* , col2/*.* , col3/*.* --title "my table" --controls controls preload autoplay loop muted --base64 --index > output.html
    htmltable col*/* --groupy_nthparent 1    --title "my table" --controls controls preload autoplay loop muted --base64 --index > output.html

"""

import itertools
import argparse
from functools import partial
import base64
import sys
import os
import filetype

from pathlib import Path
from tqdm import tqdm


__all__ = ['data_to_html']

real_print = print
print = print if sys.stdout.isatty() else lambda *a, **k: None


def get_nth_parentdir(path, n):
    assert n >= 1
    path = Path(path)
    for i in range(n):
        path = path.parent
    return path.name

def create_html(rowwise, titlestr='', rowindex=False, colindex=False):
    html = '<html>'
    html += """<head>
    <style>

        table { width: 100%; }

        table, th, td {
            border: 1px solid black;
            border-collapse: collapse;
        }

        tr:nth-child(even) { background-color: #eee; }
        tr:nth-child(odd) {  background-color: #fff; }

        """ + ",".join(list(filter(None, [("tr:nth-child(1) > th" if colindex else ""),  (" tr > td:nth-child(1), tr:nth-child(1) > th:nth-child(1)" if rowindex else "")]))) + """ {
            background-color: black;
            color: white;
            text-align: center;
            text-align: center;
            font-weight: bold;
        }

        th, td {
            padding: 15px;
            text-align: left;
        }

        body > table > tbody > tr > * > * {
            max-width: 600px;
            max-height: 600px;
        }
    </style>
</head>""" + f"""
<body>
<h1 style="text-align: center;">{titlestr}</h1>
<table>
    <tr>""" + ''.join([f'<th>{c}</th>\n' for c in rowwise[0]]) + """</tr>"""

    for row in rowwise[1:]:
        html += f'<tr>'
        for cell in row:
            html += f'<td> {cell} </td>'
        html += '</tr>'

    html += ''' </table></body></html>'''

    return html

def get_img(fpath, mimetype, ret_html=True, b64=True, **kwargs):
    if b64:
        with open(fpath, "rb") as f:
            fpath = f"data:{mimetype};base64," + base64.b64encode(f.read()).decode()

    if not ret_html:
        return fpath
    else:
        return f'<img src="{fpath}">'

def get_audio(fpath, mimetype, ret_html=True, b64=True, controls=[], **kwargs):
    return get_video(fpath, mimetype, ret_html=ret_html, b64=b64, controls=controls, **kwargs)

def get_video(fpath, mimetype, ret_html=True, b64=True, controls=[], **kwargs):
    if b64:
        with open(fpath, "rb") as f:
            fpath = f"data:{mimetype};base64," + base64.b64encode(f.read()).decode()

    mtype = mimetype.split("/")[0]
    if not ret_html:
        return fpath
    else:
        return f'<{mtype} {" ".join(controls)}><source src="{fpath}" type="{mimetype}"></{mtype}>'

def convert_mediapath(fpath, controls=[], b64=False):
    if fpath is None:
        return ""

    try:
        mimetype = str(filetype.guess(str(fpath)).mime)
    except:
        mimetype = None
    if mimetype is None:
        return fpath

    if mimetype.split('/')[0] in ['image']:
        return get_img(fpath, mimetype, ret_html=True, b64=b64)
    elif mimetype.split('/')[0] in ['audio']:
        return get_audio(fpath, mimetype, ret_html=True, controls=controls, b64=b64)
    elif mimetype.split('/')[0] in ['video']:
        return get_video(fpath, mimetype, ret_html=True, controls=controls, b64=b64)
    else:
        return fpath

def get_parentname_fpaths(fpaths):
    parentnames = [Path(fpath).parent.name for fpath in fpaths]
    assert all(x == parentnames[0] for x in parentnames), (
        f'Inconsistent parent folder names: {parentnames}, unable to infer column names.'
        'For nonhomogeneous file paths (different parent folders), please specify the column names manually using -c/--colnames')
    return parentnames[0]

def transpose_fn(l, clamp=False):
    # https://stackoverflow.com/a/6473724
    if clamp:
        # short circuits at shortest nested list if table is jagged:
        return list(map(list, zip(*l)))
    else:
        # discards no data if jagged and fills short nested lists with None
        return list(map(list, itertools.zip_longest(*list(l), fillvalue="")))

def hstack(a1, a2):
    # mutates a1
    for i in range(len(a1)):
        a1[i] = [a2[i]] + a1[i]



def data_to_html(data, title='', colnames=[], base64=False, index=False, filename_index=False,
         controls=['controls'], transpose=False, clamp=False, **kwargs):
    transpose_function = partial(transpose_fn, clamp=clamp)
    colwise = data
    # append column headers
    if colnames:
        assert len(colnames) == len(colwise), f'--colnames length must match number of columns. Expected: {len(colwise)}, got: {len(colnames)} {colnames}'
        colwise = [[c] + l for (c, l) in zip(colnames, colwise)]
    else:
        colwise = [[get_parentname_fpaths(l)] + l for l in colwise]


    # padding
    maxlen = max(list(map(len, colwise)))
    for i in range(len(colwise)):
        colwise[i] += [''] * (maxlen - len(colwise[i]) )

    if clamp:
        minlen = min(list(map(lambda l: len(list(filter(lambda x: not not x, l))), colwise)))
        colwise = [l[:minlen] for l in colwise]

    rowwise = transpose_function(colwise)

    if filename_index:
        rowwise = [rowwise[0]] + [sorted(l, key=os.path.basename) for l in rowwise[1:]]
        rownames_raw = transpose_function(rowwise[1:])
        ## assert all columns have the same filenames
        cols = [list(map(os.path.basename, l)) for l in (rownames_raw)]
        for col in cols:
            assert col == cols[0], (
                f'Inconsistent filenames. --filename_index expects columns to have matching filenames.'
                f'\nExpected: {cols[0]}'
                f'\nGot:      {col}.'
                )

    rowwise = [list(map(partial(convert_mediapath, b64=base64, controls=controls), l))
               for l in tqdm(rowwise, 'encoding media', file=sys.stderr)]

    if filename_index:
        hstack(rowwise, ['#'] + cols[0])
    elif index:
        hstack(rowwise,  ['#'] + list(range(1, len(rowwise), 1)))

    if transpose:
        rowwise = transpose_function(rowwise)

    html = create_html(rowwise, title,
                       rowindex=index or transpose,
                       colindex=not (not index and transpose),
                       )
    real_print(html)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument('data', type=str, nargs='+',
                        help='input table data. Format: col1_item1 col1_item2 col1_item3 , col2_item1 col2_item2 col2_item3 ...')
    parser.add_argument('--title', default='', help='title heading for the table')
    parser.add_argument('-g', '--groupy_nthparent', type=int, default=0, help='choose columns based on the nth parent, instead of separating using "," delimiter to determine columns.'
                        'This allows to dynamically specify folders instead of passing folders explicitly with "," in between. Set to -g 1 for the direct parent of the files')
    parser.add_argument('-c', '--colnames', nargs='+', help='Provide a list of column names (instead of automatically inferring column names from filepaths).')
    parser.add_argument('-b', '--base64', action='store_true', help='Encode all the media to a base64 URL, meaning that the html file is now portable and doesn\'t depend on the location of the images/audios/videos')
    index_grp = parser.add_mutually_exclusive_group()
    index_grp.add_argument('-x', '--index', action='store_true', help='add numerical index column')
    index_grp.add_argument('-fx', '--filename_index', action='store_true', help='Infer index (rowname) based on row filenames, instead of numerical index. All columns must have identical filenames otherwise an error is raised')
    parser.add_argument('--controls', nargs='*', choices=["controls", "preload", "autoplay", "loop", "muted"], default=['controls'], help='HTML video and audio controls')
    parser.add_argument('-t', '--transpose', action='store_true', help='swap columns and rows')
    parser.add_argument('--clamp', action='store_true', help='clamp number of rows to the shortest row, ensures the table is symmetric.')
    args = parser.parse_args()
    
    # colwise: list of lists, iterates columns wise
    if args.groupy_nthparent:
        args.data = [list(y) for x, y in itertools.groupby(args.data, lambda z: get_nth_parentdir(z, 1)) ]
    else:
        args.data = [list(y) for x, y in itertools.groupby(args.data, lambda z: z == ',') if not x]
        
    
    data_to_html(**vars(args))

