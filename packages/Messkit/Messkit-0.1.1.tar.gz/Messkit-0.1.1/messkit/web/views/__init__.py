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
Messkit web views
"""


def includeme(config):

    # core
    config.include('messkit.web.views.common')
    config.include('tailbone.views.auth')
    config.include('tailbone.views.menus')
    # config.include('tailbone.views.importing')
    config.include('tailbone.views.poser')
    config.include('tailbone.views.progress')

    # config.include('tailbone.views.features')

    config.include('tailbone.views.reports')

    # main tables
    config.include('tailbone.views.email')
    config.include('tailbone.views.people')
    config.include('tailbone.views.roles')
    config.include('tailbone.views.settings')
    config.include('tailbone.views.tables')
    config.include('tailbone.views.upgrades')
    config.include('tailbone.views.users')
