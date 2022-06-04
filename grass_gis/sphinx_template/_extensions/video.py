# -*- coding: utf-8 -*-
"""
    ReST directive for embedding Youtube and Vimeo videos.

    There are two directives added: ``youtube`` and ``vimeo``. The only
    argument is the video id of the video to include.

    Both directives have three optional arguments: ``height``, ``width``
    and ``align``. Default height is 281 and default width is 500.

    Example::

        .. youtube:: anwy2MPT5RE
            :height: 315
            :width: 560
            :align: left

    :copyright: (c) 2012 by Danilo Bargen
    :license: BSD 3-clause
    :url: https://gist.github.com/dbrgn/2922648

    Modified by Martin Landa
"""
from __future__ import absolute_import
from docutils import nodes
from docutils.parsers.rst import Directive, directives


def align(argument):
    """Conversion function for the "align" option."""
    return directives.choice(argument, ('left', 'center', 'right'))


class IframeVideo(Directive):
    has_content = True
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = False
    option_spec = {
        'height': directives.nonnegative_int,
        'width': directives.nonnegative_int,
        'align': align,
    }
    default_width = 700
    default_height = 360

    def run(self):
        env = self.state.document.settings.env
        builder_name = env.app.builder.name

        self.options['video_id'] = directives.uri(self.arguments[0])
        if not self.options.get('width'):
            self.options['width'] = self.default_width
        if not self.options.get('height'):
            self.options['height'] = self.default_height
        if not self.options.get('align'):
            self.options['align'] = 'center'
        if not self.options.get('caption'):
            self.options['caption'] = ''.join(self.content)
# ML
#            self.options['align'] = 'left'
        if builder_name == 'latex':
            return [nodes.raw('', self.latex % self.options, format='latex')]
        
        return [nodes.raw('', self.html % self.options, format='html')]


class Youtube(IframeVideo):
    html = '<div style="text-align: %(align)s"><iframe src="http://www.youtube.com/embed/%(video_id)s" \
    width="%(width)u" height="%(height)u" frameborder="0" \
    webkitAllowFullScreen mozallowfullscreen allowfullscreen \
    class="align-%(align)s"></iframe><div style="margin-top: 5px; margin-bottom: 5px"><i>%(caption)s</i></div></div>'
    latex = '\\vskip 0.5em \\textbf{YouTube -- %(caption)s} \\newline \\url{http://www.youtube.com/embed/%(video_id)s}\\vskip 0.5em'

class Vimeo(IframeVideo):
    html = '<iframe src="http://player.vimeo.com/video/%(video_id)s" \
    width="%(width)u" height="%(height)u" frameborder="0" \
    webkitAllowFullScreen mozallowfullscreen allowFullScreen \
    class="align-%(align)s"></iframe>'


def setup(builder):
    directives.register_directive('youtube', Youtube)
    directives.register_directive('vimeo', Vimeo)
