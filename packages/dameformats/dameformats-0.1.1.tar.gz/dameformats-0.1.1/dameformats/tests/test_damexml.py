#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (C) 2019  David Arroyo Menéndez

# Author: David Arroyo Menéndez <davidam@gnu.org>
# Maintainer: David Arroyo Menéndez <davidam@gnu.org>

# This file is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.

# This file is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with dameformats; see the file LICENSE.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
# Boston, MA 02110-1301 USA,

import unittest
from xml.dom import minidom
import xml.etree.ElementTree as ET

class TestDameXml(unittest.TestCase):

    # XML
    def test_damexml_getelementsbytagname(self):
        # using read and loads to open
        xmldoc = minidom.parse('files/items.xml')
        itemlist = xmldoc.getElementsByTagName('item')
        self.assertEqual(len(itemlist), 4)
        l1 = []
        for s in itemlist:
            l1.append(s.attributes['name'].value)
        self.assertEqual(l1, ['item1', 'item2', 'item3', 'item4'])

    def test_damexml_rss_titles(self):
        tree = ET.parse('files/rss.xml')
        l1 = []
        for elem in tree.iter():
            # using elem.tag
            if (elem.tag == "title"):
                l1.append(elem.text)
        self.assertEqual(l1[0:2], ["Richard Stallman's Political Notes",
                                   'Economic growth and fossil fuels'])
    def test_damexml_root(self):
        tree = ET.parse('files/rss.xml')
        root = tree.getroot()
        self.assertEqual(root.tag, 'rss')
        self.assertEqual(root.attrib, {'version': '2.0'})
        l2 = []
        for elem in root.iter():
            if (elem.tag == "title"):
                l2.append(elem.text)
        self.assertEqual(l2[0:2], ["Richard Stallman's Political Notes",
                                   'Economic growth and fossil fuels'])

    def test_damexml_fromstring(self):
        root = ET.fromstring('<a><b /><c><d /></c></a>')
        self.assertEqual(root.tag, 'a')
        self.assertEqual(root[0].tag, 'b')
        self.assertEqual(root[1].tag, 'c')
        self.assertEqual(root[1][0].tag, 'd')

    def test_damexml_parser(self):
        parser = ET.XMLPullParser(['start', 'end'])
        parser.feed('<p>')
        parser.feed('</p>')
        l0 = []
        l1 = []
        for event, elem in parser.read_events():
            l0.append(event)
            l1.append(elem)
        self.assertEqual(len(l0), 2)
        self.assertEqual(len(l1), 2)        
        parser2 = ET.XMLPullParser(['start', 'end'])
        parser2.feed('<a>')
        parser2.feed('</a>')
        l2 = []
        l3 = []
        for event2, elem2 in parser2.read_events():
            l2.append(event2)
            l3.append(elem2)
        self.assertEqual(len(l2), 2)
        self.assertEqual(len(l3), 2)
        
    def test_damexml_xpath(self):
        tree = ET.parse("files/html.html")
        p = tree.find("body/p")
        links = list(p.iter("a"))
        self.assertEqual(len(links), 2)

    def test_damexml_xpath2(self):
        tree = ET.parse("files/html.html")
        p = tree.find("body/p[@class='xyz']")
        links = list(p.iter("a"))
        self.assertEqual(len(links), 0)
        texts = list(p.itertext())
        self.assertEqual(len(texts), 1)
        self.assertEqual(texts[0], "Moved to example.org or example.com.")        
        
    def test_damexml_xpath3(self):
        tree = ET.parse('files/countries.xml')
        root = tree.getroot()
        self.assertEqual(root.tag, 'data')
        self.assertEqual(root.attrib, {})
        root.findall('.')
        years = root.findall('./country/year')
        self.assertEqual(len(years), 2)
        self.assertEqual(years[0].text, '2008')
        self.assertEqual(years[1].text, '2011')        
        ranking = root.findall('./country/rank')
        self.assertEqual(len(ranking), 2)
        self.assertEqual(ranking[0].attrib, {'updated': 'yes'})
        neighborhood = root.findall('./country/neighbor')        
        self.assertEqual(neighborhood[0].attrib, {'name': 'Austria', 'direction': 'E'})
        
if __name__ == '__main__':
    unittest.main()
