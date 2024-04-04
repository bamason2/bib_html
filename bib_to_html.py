# create list of publications for insertion into bootstrap webpage using a template
# ref_template.html.

from pybtex.database import parse_file
import re

TEMPLATE='files/ref_template.html'

def create_html(input_bib_file, output_html_file):
    bib_data = parse_file(input_bib_file)
    entries = bib_data.entries
    pub_dict = {}

    # get details for html creation and put in dict
    for entry in entries:
        try:
            title = bib_data.entries[entry].fields['title']
            doi = bib_data.entries[entry].fields['doi']
            year = bib_data.entries[entry].fields['year']
            pub_dict[entry] = {'year':year,'doi':doi,'title':title }
        except:
            print('missing details')

    # sort the dictionary by year
    sorted_pub = sorted(pub_dict.items(), key=lambda item: item[1]['year'], reverse=True)

    # read in the template and replace keywords #title#, #doi# and #year# will actual values
    with open(TEMPLATE) as f:
        template_string = f.read()

    for item in sorted_pub:
        template_string_modified = re.sub(r'#title#', item[1]['title'], template_string)
        template_string_modified = re.sub(r'#doi#', item[1]['doi'], template_string_modified)
        template_string_modified = re.sub(r'#year#', item[1]['year'], template_string_modified)

        # write output to file at each iteration for debugging purposes
        with open(output_html_file, 'a') as f:
            f.write(template_string_modified)


create_html(input_bib_file='files/export_modified.bib', output_html_file='files/output_file.html')