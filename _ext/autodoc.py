import shutil
import os
import json
import html

fName = os.path.realpath(__file__)

CONTRIB_INFO = ['affiliation', 'location', 'email', 'url', 'ORCID']
CASEHISTORY_INFO = ['citations', 'contributors', 'tags']

ORCID_URL = 'http://orcid.org/'

THIS_IS_AUTOGENERATED = (
    ".. --------------------------------- ..\n"
    "..                                   ..\n"
    "..    THIS FILE IS AUTO GENEREATED   ..\n"
    "..                                   ..\n"
    "..    autodoc.py                     ..\n"
    "..                                   ..\n"
    ".. --------------------------------- ..\n"
)


def make_formula_sheet():

    # Create the examples dir in the docs folder.

    EquationSheetDir = os.path.sep.join(fName.split(os.path.sep)[:-2] +
                                        ['content', 'equation_bank'])
    files = os.listdir(EquationSheetDir)

    rst = os.path.sep.join((fName.split(os.path.sep)[:-2] +
                           ['content', 'equation_bank' + '.rst']))

    out = """.. _equation_bank:

{}


Equation Bank
=============

""".format(THIS_IS_AUTOGENERATED)

    print('\nCreating: equation_bank.rst')
    f = open(rst, 'w')
    f.write(out)

    for name in files:
        out = """

 - {}

    .. include:: equation_bank/{}

        """.format(name.rstrip('.rst'), name)
        f.write(out)

    f.close()

    print('Done writing equation_bank.rst\n')


def make_contributorslist(fpath='contributors.json',
                          fout='contributors.rst',
                          contrib_info=CONTRIB_INFO):

    fpath = os.path.sep.join(fName.split(os.path.sep)[:-2] + [fpath])
    fout = os.path.sep.join(fName.split(os.path.sep)[:-2] + [fout])

    fpath = open(fpath)  # file to write to
    contribs = json.load(fpath)  # contributors json
    keys = contribs.keys()

    # sort by last name
    last_names = []
    for key, val in contribs.iteritems():
        if 'name' not in val:
            raise Exception('{} has no name!?'.format(keys))
        last_names.append(val['name'].split(' ')[-1])

    # # get relavent info
    # contrib_info = list(
    #     set([item for entries in contribs.itervalues() for item in entries]
    #         ).difference(set(['avatar']))
    #     )

    last_names = zip(last_names, contribs.keys())
    sorted_names = sorted(last_names)

    out = """
{}

.. _contibutors:

Contributors
============

""".format(THIS_IS_AUTOGENERATED)

    print('\nCreating: contributors.rst')
    f = open(fout, 'w')
    f.write(out)

    for _, key in sorted_names:

        contrib = contribs[key]

        html_block = []
        for info_key in contrib_info:
            if info_key in contrib:
                # if info_key == 'ORCID':
                #     html = """
                #         <strong>ORCID:</strong><a class="reference external" href="http://orcid.org/{val}">{val}</a><br>
                #     """.format(val=contrib[info_key])
                # val = contrib[info_key]
                # if info_key == 'ORCID':
                #     val = "`{val} <{url}>`_".format(val=val, url=ORCID_URL+val)
                val = contrib[info_key]
                if info_key == 'ORCID':
                    htmlval = """
    <a class="reference external" href="{url}">{orcid}</a>
                    """.format(url=html.escape(ORCID_URL + val), orcid=val)
                # a website
                elif 'http' in val or 'www' in val:
                    if 'www' in val and 'http' not in val:
                        val = 'http://' + val
                    htmlval = """
    <a class="reference external" href="{url}">{url}</a>
                    """.format(url=html.escape(val))
                # an email
                elif '@' in val:
                    htmlval = """
    <a class="reference external" href="mailto:{email}">{email}</a>
                    """.format(email=html.escape(val))
                # otherwise assume it is text
                else:
                    htmlval = html.escape(val)

                htmlval = """
    <strong>{key}:</strong> {htmlval}
                          """.format(key=info_key, htmlval=htmlval)

                html_block.append(htmlval)

        # join the block
        html_block = '<br>'.join(html_block)

        if 'avatar' in contrib:
            avatar = """
    <a class="reference internal image-reference" href="{avatar}"><img alt="{avatar}" class="align-left" src="{avatar}" style="width: 120px; border-radius: 10px; vertical-align: text-middle padding-left="20px" /></a>
            """.format(avatar=contrib['avatar'])

        else:
            avatar = ""

        out = """

.. _{id}:

{name}
{underline}

.. raw:: html

    <div class="row" style="min-height: 160px">
    <div class="col-md-4">
        {avatar}
    </div>
    <div class="col-md-6" style="line-height: 1.5">
        {html_block}
    </div>
    <br>
    </div>


        """.format(id=key,
                   name=contrib['name'],
                   underline='-'*len(contrib['name']),
                   namepermalink=key,
                   par=html.escape('&para;'),
                   avatar=avatar,
                   html_block=html_block
                   )

        f.write(out)

    f.close()

    print('Done writing contributors.rst\n')



def make_case_histories(fpath='content/case_histories/case_histories.json',
                        fout='content/case_histories/case_histories.rst',
                        casehistory_info=CASEHISTORY_INFO):

    fpath = os.path.sep.join(fName.split(os.path.sep)[:-2] + fpath.split('/'))
    fout = os.path.sep.join(fName.split(os.path.sep)[:-2] + fout.split('/'))

    fpath = open(fpath)  # file to write to
    casehistories = json.load(fpath)  # casehistories json

    out = """

{}


""".format(THIS_IS_AUTOGENERATED)

    print('Creating: case_histories.html')
    f = open(fout, 'w')
    f.write(out)

    for key in casehistories.keys():
        casehistory = casehistories[key]

        if 'citation' in casehistory:
            reference_block="- {citations}".format(
                citations=[':cite:`citation`' for citation in casehistory['citations']])
        else:
            reference_block=""

        if 'contributors' in casehistory:
            contrib_dict = {
                'authors': [],
                'editors': [],
                'reviewers': []}

            for contrib in casehistory['contributors']:
                contrib_style = contrib['as']

                contributor = ':ref:`{}`'.format(
                        contrib['uid'].split(':')[1]
                        )
                if contrib_style in contrib_dict:
                    contrib_dict[contrib_style] += ', ' + contributor
                else:
                    contrib_dict[contrib_style] = contributor

            contributions = ['    - {contrib_style}: {contribs}'.format(
                contrib_style=contrib_style, contribs=val
                ) for contrib_style, val in contrib_dict.iteritems() if val]

            contributions = '\n'.join(contributions)

            contributors_block="""
- Contributors
{contributions}
""".format(contributions=contributions)

        if 'tags' in casehistory:
            tags_dict = {}
            for tags in casehistory['tags']:
                tags_style = tags['as'].replace('_', ' ')

                if tags_style in tags_dict:
                    tags_dict[tags_style] += ', '+tags['uid'].replace('_', ' ')
                else:
                    tags_dict[tags_style] = tags['uid'].replace('_', ' ')

            tags_list = ['    - {tags_style}: {tag}'.format(
                tags_style=tag_style, tag=val
                ) for tag_style, val in tags_dict.iteritems()]

            tags_list = '\n'.join(tags_list)

            tags_block="""
- Tags
{tags_list}
""".format(tags_list=tags_list)

        out="""

{title}
{underline}

.. image:: {thumbnail}
    :alt: {uid}
    :width: 260
    :align: right

- :ref:`{title} Case History <{uid}_index>`
{references_block}
{contributors_block}
{tags_block}
|
|
|



        """.format(
            uid=key,
            title=casehistory['title'],
            underline='^'*len(casehistory['title']),
            source=casehistory['source'],
            thumbnail=casehistory['thumbnail'],
            references_block=reference_block,
            contributors_block=contributors_block,
            tags_block=tags_block
            )

        f.write(out)

    f.close()

    print('Done writing case_histories.rst')


# .. raw:: html

#     <span id="{uid}"></span><h3><a class="referance internal" href="{source}/index.html" title="Go to the case history">{title}</a></h3>
#     <div class="row">
#     <div class="col-md-6">
#     <a class="reference internal image-reference" href="../../_images/{thumbnail}"><img alt="../../_images/{thumbnail}" class="align-left" src="../../_images/{thumbnail}" style="width: 250px;" /></a>
#     </div>
#     <div class="col-md-6">
#     <ul>
#     {info_block}
#     </ul>
#     </div>
#     <br>
#     <br>
#     </div>


if __name__ == '__main__':
    """
        Run the following to create the formula sheet.
    """

    make_formula_sheet()
    make_contributorslist()
    make_case_histories()