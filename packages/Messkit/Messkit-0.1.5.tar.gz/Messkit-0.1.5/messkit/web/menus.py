# -*- coding: utf-8; -*-
######################################################################
#
#  Messkit -- Generic-ish Data Utility App
#  Copyright © 2022 Lance Edgar
#
#  This file is part of Messkit.
#
#  Messkit is free software: you can redistribute it and/or modify it
#  under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Messkit is distributed in the hope that it will be useful, but
#  WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with Messkit.  If not, see <http://www.gnu.org/licenses/>.
#
######################################################################
"""
Web Menus
"""


def simple_menus(request):

    people_menu = {
        'title': "People",
        'type': 'menu',
        'items': [
            {
                'title': "All People",
                'route': 'people',
                'perm': 'people.list',
            },
        ],
    }

    reports_menu = {
        'title': "Reports",
        'type': 'menu',
        'items': [
            {
                'title': "New Report",
                'route': 'report_output.create',
                'perm': 'report_output.create',
            },
            {
                'title': "Generated Reports",
                'route': 'report_output',
                'perm': 'report_output.list',
            },
            {
                'title': "Problem Reports",
                'route': 'problem_reports',
                'perm': 'problem_reports.list',
            },
            {'type': 'sep'},
            {
                'title': "Poser Reports",
                'route': 'poser_reports',
                'perm': 'poser_reports.list',
            },
        ],
    }

    admin_menu = {
        'title': "Admin",
        'type': 'menu',
        'items': [
            {
                'title': "Users",
                'route': 'users',
                'perm': 'users.list',
            },
            {
                'title': "Roles",
                'route': 'roles',
                'perm': 'roles.list',
            },
            {'type': 'sep'},
            {
                'title': "App Settings",
                'route': 'appsettings',
                'perm': 'settings.list',
            },
            {
                'title': "Email Settings",
                'route': 'emailprofiles',
                'perm': 'emailprofiles.list',
            },
            {
                'title': "Raw Settings",
                'route': 'settings',
                'perm': 'settings.list',
            },
            {'type': 'sep'},
            {
                'title': "Tables",
                'route': 'tables',
                'perm': 'tables.list',
            },
            {
                'title': "Messkit Upgrades",
                'route': 'upgrades',
                'perm': 'upgrades.list',
            },
        ],
    }

    menus = [
        people_menu,
        reports_menu,
        admin_menu,
    ]

    return menus
