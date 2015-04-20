# Copyright 2015 Curtis Sand
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
libRst
======

This module is intended to provide compilation support for rst.  The intention
is to keep the required libraries all in one place to provide a deployable,
python 2.6/2.7 compatible, rst compiler.

RST Constructs to be supported:
    - paragraph
    - heading
    - list (unordered, ordered)
    - table
"""

from functools import reduce
#import docutils.core
#import sys, os.path


#def toHtml(text):
#    """ Use Docutils to compile text into html. """
#    return docutils.core.publish_parts(source=text,
#                                       writer_name='html')['html_body']
#

def indent(text, indent):
    """ Indent some text by a number of spaces

        :param indent: (int or str) number of spaces to indent the text, or
                       the text to use as the indentation

        >>> indent('foo\\nbar', indent=3)
        '   foo\\n   bar'
        >>> indent('foo\\nbar', indent='__')
        '__foo\\n__bar'
    """
    if isinstance(indent, int):
        indent = ' ' * indent
    return '\n'.join([indent + line for line in text.split('\n')])


def wrap(line, width=80, continuationPrefix=None, splitWords=False,
             wordSplitChar='-'):
    """ Wrap text to the given width.

        :param line: (str) the line of text to wrap
        :param width: (int) the width to wrap the line to
        :param continuationPrefix: (str) the string to prefix continued lines with
        :param splitWords: (bool) whether or not to split words to fill the line
        :param wordSplitChar: (str) The string to use to indicate a word
                              continues on another line.  wordSplitChar has no
                              effect if splitWords is False.

        >>> wrap('foo bar', width=6)
        'foo \\nbar \\n'
        >>> wrap('foo bar', width=6, continuationPrefix=' ')
        'foo \\n bar \\n'
        >>> wrap('foo bar', width=6, splitWords=True)
        'foo b-\\nar \\n'
        >>> wrap('foo bar', width=6, splitWords=True, wordSplitChar='>')
        'foo b>\\nar \\n'
        >>> wrap('foo bar', width=5, splitWords=True)
        'foo \\nbar \\n'
    """
    if not continuationPrefix:
        continuationPrefix = ''
    words = line.split(' ')
    retVal = ''
    newLine = ''
    for word in words:
        if len(newLine) + len(word) <= width:
            newLine += word + ' '
            continue
        elif len(newLine) + len(word) > width and not splitWords:
            retVal += newLine + '\n'
            newLine = continuationPrefix + word + ' '
            continue
        else: #split the word
            remainingSpace = width - len(newLine)
            if remainingSpace <= 1:
                retVal += newLine + '\n'
                newLine = continuationPrefix + word + ' '
                continue
            splitIndex = remainingSpace - len(wordSplitChar)
            newLine += word[:splitIndex] + wordSplitChar
            retVal += newLine + '\n'
            newLine = continuationPrefix + word[splitIndex:] + ' '
            continue
    retVal += newLine + '\n'
    return retVal


def _separateNewlines(text):
    """ Separate newlines from beginning and end of text and return them in a tuple.

        :return: (tuple of str) the beginning newline value, stripped text,
                 ending newline value

        >>> _separateNewlines('\\nfoo\\n')
        ('\\n', 'foo', '\\n')
        >>> _separateNewlines('foo')
        ('', 'foo', '')
    """
    start = ''
    end = ''
    if text[0] == '\n':
        start = '\n'
        text = text[1:]
    if text[-1] == '\n':
        end = '\n'
        text = text[:-1]
    return start, text, end


def heading(text, level):
    """ Turn a line of text into an RST heading.  Always returns a trailing
        newline.

        :param level: (int) the level of heading to produce.  Level 0 is the
                      document title and is overlined.

        >>> heading('foo', 0)
        '===\\nfoo\\n===\\n'
        >>> heading('foo', 1)
        'foo\\n===\\n'
        >>> heading('\\nfoo\\n', 2)
        '\\nfoo\\n---\\n'
        >>> heading('foo', 11)  # doctest: +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
        ValueError: A heading cannot have a level less than 0 or ...
    """
    _chars = ['=', '-', '~', '"', "'", '*', '^', '_', '+', ':', '#']
    getUnderline = lambda charIndex: _chars[charIndex] * len(text)
    start, text, end = _separateNewlines(text)
    if level < 0 or level >= len(_chars):
        msg = ('A Heading cannot have a level less than 0 or larger ' +
               'than %s: %s' % (len(_chars), text))
        raise ValueError(msg)
    elif level == 0:
        return '%s%s\n%s\n%s\n' % (start, getUnderline(level), text,
                                   getUnderline(level))
    else:
        return '%s%s\n%s\n' % (start, text, getUnderline(level-1))


def list(elements, ordered=False, startIndex=1):
    """ Create an RST List from a collection.

        :param elements: (list) a collection of strings, each an element of
                         the list
        :param ordered: (bool) set's list type between bulleted and enumerated
        :param startIndex: (int) if start index is 1 then an auto-enumerated
                           list is used ("#. element\\\n")

        >>> list(['foo', 'bar'])
        '- foo\\n- bar\\n'
        >>> list(['foo', 'bar'], ordered=True)
        '#. foo\\n#. bar\\n'
        >>> list(['foo', 'bar'], ordered=True, startIndex=3)
        '3. foo\\n4. bar\\n'

        startIndex has no effect if not ordered
        >>> list(['foo', 'bar'], ordered=False, startIndex=3)
        '- foo\\n- bar\\n'

    """
    #TODO: make this work with multiline elements
    retVal = ''
    index = startIndex
    for element in elements:
        if ordered and startIndex==1:
            retVal += '#. %s\n' % (element)
        elif ordered and startIndex>1:
            retVal += '%s. %s\n' % (index, element)
            index = index + 1
        else:
            retVal += '- %s\n' % element
    return retVal


def table(grid):
    """ Build an RST table out of nested lists. """
    #TODO: make this work with multiline cells
    grid = _padGrid(grid)
    cell_width = 2 + max(reduce(lambda x,y: x+y,
                                [[len(str(item)) for item in row]
                                 for row in grid], []))
    num_cols = len(grid[0])
    rst = _tableDiv(num_cols, cell_width, 0)
    header_flag = 1
    for row in grid:
        rst = rst + '| ' + '| '.join([_normalizeCell(x, cell_width-1)
                                      for x in row]) + '|\n'
        rst = rst + _tableDiv(num_cols, cell_width, header_flag)
        header_flag = 0
    return rst


def _tableDiv(num_cols, col_width, header_flag):
    if header_flag == 1:
        return num_cols*('+' + (col_width)*'=') + '+\n'
    else:
        return num_cols*('+' + (col_width)*'-') + '+\n'


def _normalizeCell(string, length):
    return string + ((length - len(string)) * ' ')


def _padGrid(grid):
    padChar = ''
    maxRowLen = max([len(row) for row in grid])
    for row in grid:
        while len(row) < maxRowLen:
            row.append(padChar)
    return grid


if __name__=="__main__":
    import doctest
    doctest.testmod()
