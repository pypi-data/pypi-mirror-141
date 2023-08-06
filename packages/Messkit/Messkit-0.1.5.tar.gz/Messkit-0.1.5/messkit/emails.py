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
Email Settings
"""

from rattail.emails import (person_merge_request,
                            rattail_export_rattail_updates,
                            rattail_import_rattail_updates,
                            rattail_import_versions_updates,
                            rattail_problems_stale_inventory_batch,
                            upgrade_failure,
                            upgrade_success,
                            user_feedback)
