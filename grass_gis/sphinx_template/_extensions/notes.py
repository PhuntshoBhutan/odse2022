# -*- coding: utf-8 -*-

from docutils import nodes
from docutils.parsers.rst.directives.admonitions import BaseAdmonition
from docutils.parsers.rst import directives
from docutils.statemachine import ViewList

class NoteCmd(directives.admonitions.BaseAdmonition):
    required_arguments = 1
    node_class = nodes.admonition

    def run(self):
        self.options['classes'] = ['notecmd']
        self.arguments[0] = self.arguments[0] + u' from command line'
        return super(NoteCmd, self).run()

class NoteGRASS6(directives.admonitions.BaseAdmonition):
    required_arguments = 0
    node_class = nodes.admonition

    def run(self):
        self.options['classes'] = ['notegrass6']
        self.arguments.append(u'Poznámka pro GRASS GIS verze 6')
        return super(NoteGRASS6, self).run()

class NoteAdvanced(directives.admonitions.BaseAdmonition):
    required_arguments = 0
    node_class = nodes.admonition

    def run(self):
        self.options['classes'] = ['noteadvanced']
        self.arguments.append(u'Note for advanced users')
        return super(NoteAdvanced, self).run()

class NoteDataset(directives.admonitions.BaseAdmonition):
    required_arguments = 0
    node_class = nodes.admonition
    has_content = True
    
    def run(self):
        self.options['classes'] = ['note']
        self.arguments.append(u'Poznámka k datové sadě GISMentors')
        self.content.append(ViewList([u'Datová sada GISMentors je založena na datech pocházejících pouze z otevřených či veřejných zdrojů jako je `EU-DEM <http://www.eea.europa.eu/data-and-maps/data/eu-dem>`__, `RÚIAN <http://www.cuzk.cz/ruian/RUIAN.aspx>`__, `OpenStreetMap <http://wiki.openstreetmap.org/wiki/Main_Page>`__, `Dibavod <http://www.dibavod.cz/>`__,  `AOPK <http://gis-aopkcr.opendata.arcgis.com/>`__ a `IPR <http://www.geoportalpraha.cz/cs/opendata>`__.']))
        
        return super(NoteDataset, self).run()

class Task(directives.admonitions.BaseAdmonition):
    required_arguments = 0
    node_class = nodes.admonition

    def run(self):
        self.options['classes'] = ['task']
        self.arguments = [u'Task']
        return super(Task, self).run()

def setup(builder):
    directives.register_directive('notecmd', NoteCmd)
    directives.register_directive('notegrass6', NoteGRASS6)
    directives.register_directive('noteadvanced', NoteAdvanced)
    directives.register_directive('notedata', NoteDataset)
    directives.register_directive('task', Task)
