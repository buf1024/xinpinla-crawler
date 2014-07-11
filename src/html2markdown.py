#!/usr/bin/env python
#coding: utf-8

from HTMLParser import HTMLParser

import re
import os
import sys
import string

class Html2MarkdownParser(HTMLParser):
    def __init__(self):
        self._markdown = ''
        self._tag_stack = []
        self._tag_attr_data = {}
        self._handled_tag_body_data = ''
        self._convertible_tags = ['a',
                                  'img',
                                  'b', 'blockquote',
                                  'em',
                                  'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'hr',
                                  'ol',
                                  'p', 'pre',
                                  'strong',
                                  'ul']
        # FIXME: special characters
        HTMLParser.__init__(self)

    def _append_to_markdown(self, new_markdown):
        if len(self._markdown) > 1:
            if re.match('\s', self._markdown[-1:]):
                self._markdown += new_markdown
            else:
                self._markdown += ' ' + new_markdown
        else:
            self._markdown += new_markdown

    # <img />
    def handle_start_img(self, attrs):
        self._tag_attr_data = dict(attrs)

    def handle_end_img(self):
        a_tag = ''
        a_tag += '![' + self._tag_attr_data.get('alt') + ']'
        a_tag += '(' + self._tag_attr_data.get('src')

        title = self._tag_attr_data.get('title')
        if title:
            a_tag += ' "' + title + '") '
        else:
            a_tag += ') '
        self._append_to_markdown(a_tag)
        
    # <a />
    def handle_start_a(self, attrs):
        self._tag_attr_data = dict(attrs)

    def handle_end_a(self):
        # 如果有嵌套的a则会挂掉
        a_tag = ''
        a_tag += '[' + self._handled_tag_body_data + ']'
        a_tag += '(' + self._tag_attr_data.get('href')
        title = self._tag_attr_data.get('title')
        if title:
            a_tag += ' "' + title + '") '
        else:
            a_tag += ') '
        self._append_to_markdown(a_tag)

    # <b />
    def handle_end_b(self):
        self._handled_tag_body_data = self._handled_tag_body_data.replace('\n', ' ')
        self._append_to_markdown('*' + self._handled_tag_body_data + '*')

    # <blockquote />
    def handle_end_blockquote(self):
        blockquote_body = self._handled_tag_body_data.split('\n')

        for blockquote_line in blockquote_body:
            blockquote_line = blockquote_line.strip()
            self._append_to_markdown('> ' + blockquote_line + '\n')

    # <em />
    def handle_end_em(self):
        self._handled_tag_body_data = self._handled_tag_body_data.replace('\n', ' ')
        self._append_to_markdown('*' + self._handled_tag_body_data + '*')

    # <h1 />
    def handle_end_h1(self):
        self._handled_tag_body_data = self._handled_tag_body_data.replace('\n', ' ')
        self._append_to_markdown('# ' + self._handled_tag_body_data + ' #' + '\n')

    # <h2 />
    def handle_end_h2(self):
        self._handled_tag_body_data = self._handled_tag_body_data.replace('\n', ' ')
        self._append_to_markdown('## ' + self._handled_tag_body_data + ' ##' + '\n')

    # <h3 />
    def handle_end_h3(self):
        self._handled_tag_body_data = self._handled_tag_body_data.replace('\n', ' ')
        self._append_to_markdown('### ' + self._handled_tag_body_data + ' ###' + '\n')

    # <h4 />
    def handle_end_h4(self):
        self._handled_tag_body_data = self._handled_tag_body_data.replace('\n', ' ')
        self._append_to_markdown('#### ' + self._handled_tag_body_data + ' ####' + '\n')

    # <h5 />
    def handle_end_h5(self):
        self._handled_tag_body_data = self._handled_tag_body_data.replace('\n', ' ')
        self._append_to_markdown('##### ' + self._handled_tag_body_data + ' #####' + '\n')

    # <h6 />
    def handle_end_h6(self):
        self._handled_tag_body_data = self._handled_tag_body_data.replace('\n', ' ')
        self._append_to_markdown('###### ' + self._handled_tag_body_data + ' ######' + '\n')

    # <hr />
    def handle_start_hr(self, attrs):
        self._append_to_markdown('* * *' + '\n')

    # <li />
    def handle_end_li(self):
        if len(self._tag_stack):
            if self._tag_stack[-1] == 'ol':
                self._append_to_markdown('1.    ' + self._handled_tag_body_data + '\n')
            elif self._tag_stack[-1] == 'ul':
                self._append_to_markdown('*    ' + self._handled_tag_body_data + '\n')

    # <p />
    def handle_start_p(self, attrs):
        self._markdown.rstrip()
        
    def handle_end_p(self):
        #self._markdown += '%s%s' % ('\n', '\n')
        self._markdown = self._markdown.rstrip() + '\n\n'

    # <pre />
    def handle_end_pre(self):
        code_lines = self._handled_tag_body_data.split('\n')
        for code_line in code_lines:
            code_line = code_line.strip()
            self._append_to_markdown('    ' + code_line + '\n')

    # <strong />
    def handle_end_strong(self):
        self._handled_tag_body_data = self._handled_tag_body_data.replace('\n', ' ')
        self._append_to_markdown('**' + self._handled_tag_body_data + '**')

    ## ###
    def handle_starttag(self, tag, attrs):        
        try:
            self._tag_stack.append(tag)
            eval('self.handle_start_' + tag + '(attrs)')
        except AttributeError, e:
            pass

    def handle_endtag(self, tag):
        try:
            self._tag_stack.pop()
            eval('self.handle_end_' + tag + '()')
            # Collapse three successive CRs into two before moving on
            while len(self._markdown) > 2 and \
                    self._markdown[-3:] == '%s%s%s' % ('\n', '\n', '\n'):
                self._markdown = self._markdown[:-3] + '%s%s' % ('\n', '\n')
        except AttributeError, e:
            pass
        except Exception, e:
            pass

        self._tag_attr_data = {}
        self._handled_tag_body_data = ''

    def handle_data(self, data):
        data = '\n'.join(map(string.strip, data.strip().split('\n')))
        if len(self._tag_stack) and self._tag_stack[-1] not in ['p']:
            self._handled_tag_body_data += data
        else:
            self._append_to_markdown(data)

    def get_markdown(self):
        return self._markdown.strip() + '\n'

def main():
    p = Html2MarkdownParser()
    buf = sys.stdin.read()
    p.feed(buf.strip())
    p.close()
    print p.get_markdown()

if __name__ == "__main__":
    sys.exit(main())