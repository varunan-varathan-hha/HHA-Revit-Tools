# -*- coding: utf-8 -*-
"""List all Elements of the selected level(s)."""
from collections import defaultdict

from pyrevit import script
from pyrevit import revit, DB
from pyrevit import forms


output = script.get_output()

all_elements = DB.FilteredElementCollector(revit.doc)\
                 .WhereElementIsNotElementType()\
                 .ToElements()


levels = forms.select_levels(use_selection=True)


if not levels:
    forms.alert('At least one Level element must be selected.')
else:
    output.print_md("####LIST ALL ELEMENTS ON SELECTED LEVEL(S):")
    output.print_md('By: [{}]({})'.format('Frederic Beaupere',
                                          'https://github.com/frederic-beaupere'))


    all_count = all_elements.Count
    print('\n' + str(all_count) + ' Elements found in project.')

    for element in levels:
        element_categories = defaultdict(list)
        level = element
        counter = 0

        print('\n' + '╞═════════■ {}:'.format(level.Name))

        for elem in all_elements:
            if elem.LevelId == level.Id:
                counter += 1
                element_categories[elem.Category.Name].append(elem)

        for category in element_categories:
            print('├──────────□ {}: {}'
                  .format(category,
                          str(len(element_categories[category]))))

            for elem_cat in element_categories[category]:
                print('├ id: {}'.format(output.linkify(elem_cat.Id)))

        print('├────────── {} Categories found in {}:'
              .format(str(len(element_categories)),
                      level.Name))

        for cat in element_categories:
            print('│ {}: {}'.format(str(cat),
                                    str(len(element_categories[cat]))))

        print('└────────── {}: {} Elements found.'
              .format(level.Name,
                      str(counter)))
