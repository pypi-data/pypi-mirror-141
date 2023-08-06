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
Messkit commands
"""

import os
import stat
import sys
import subprocess

import sqlalchemy as sa
from prompt_toolkit import prompt
from prompt_toolkit.styles import Style
from rich import print as rprint
from alembic.util.messaging import obfuscate_url_pw

from rattail import commands
from rattail.files import resource_path

from messkit import __version__


def main(*args):
    """
    Main entry point for Messkit command system
    """
    args = list(args or sys.argv[1:])
    cmd = Command()
    cmd.run(*args)


class Command(commands.Command):
    """
    Main command for Messkit
    """
    name = 'messkit'
    version = __version__
    description = "Messkit (Generic Data App)"
    long_description = ''


class Install(commands.Subcommand):
    """
    Install a Messkit app
    """
    name = 'install'
    description = __doc__.strip()

    def run(self, args):

        rprint("\n\t[blue]Welcome to Messkit![/blue]")
        rprint("\n\tThis tool will install and configure a new app.")
        rprint("\n\t[italic]NB. You should already have created a new database in PostgreSQL or MySQL.[/italic]")

        # continue?
        if not self.basic_prompt("continue?", True, is_bool=True):
            rprint()
            sys.exit(0)

        # appdir must not yet exist
        appdir = os.path.join(sys.prefix, 'app')
        if os.path.exists(appdir):
            rprint("\n\t[bold red]appdir already exists:[/bold red]  {}\n".format(appdir))
            sys.exit(1)

        # get db info
        dbtype = self.basic_prompt('db type', 'postgresql')
        dbhost = self.basic_prompt('db host', 'localhost')
        dbport = self.basic_prompt('db port', '3306' if dbtype == 'mysql' else '5432')
        dbname = self.basic_prompt('db name', 'messkit')
        dbuser = self.basic_prompt('db user', 'rattail')

        # get db password
        dbpass = None
        while not dbpass:
            dbpass = self.basic_prompt('db pass', is_password=True)

        # test db connection
        rprint("\n\ttesting db connection... ", end='')
        dburl = self.make_db_url(dbtype, dbhost, dbport, dbname, dbuser, dbpass)
        error = self.test_db_connection(dburl)
        if error:
            rprint("[bold red]cannot connect![/bold red] ..error was:")
            rprint("\n{}".format(error))
            rprint("\n\t[bold yellow]aborting mission[/bold yellow]\n")
            sys.exit(1)
        rprint("[bold green]good[/bold green]")

        # make the appdir
        self.app.make_appdir(appdir)

        # shared context for generated app files
        context = {
            'envdir': sys.prefix,
            'app_package': 'messkit',
            'app_title': "Messkit",
            'appdir': appdir,
            'db_url': dburl,
            'pyramid_egg': 'Messkit',
            'beaker_key': 'messkit',
        }

        # make config files
        rattail_conf = self.app.make_config_file(
            'rattail', os.path.join(appdir, 'rattail.conf'),
            template_path=resource_path('messkit:templates/installer/rattail.conf.mako'),
            **context)
        quiet_conf = self.app.make_config_file('quiet', appdir)
        web_conf = self.app.make_config_file(
            'web-complete', os.path.join(appdir, 'web.conf'),
            **context)

        # make upgrade script
        path = os.path.join(appdir, 'upgrade.sh')
        self.app.render_mako_template(
            resource_path('messkit:templates/installer/upgrade.sh.mako'),
            context, output_path=path)
        os.chmod(path, stat.S_IRWXU
                 | stat.S_IRGRP
                 | stat.S_IXGRP
                 | stat.S_IROTH
                 | stat.S_IXOTH)

        rprint("\n\tappdir created at:  [bold green]{}[/bold green]".format(appdir))

        bindir = os.path.join(sys.prefix, 'bin')

        schema_installed = False
        if self.basic_prompt("install db schema?", True, is_bool=True):
            rprint()

            # install db schema
            alembic = os.path.join(bindir, 'alembic')
            cmd = [alembic, '-c', rattail_conf, 'upgrade', 'heads']
            subprocess.check_call(cmd)
            schema_installed = True

            rattail = os.path.join(bindir, 'rattail')

            # set falafel theme
            cmd = [rattail, '-c', quiet_conf, '--no-versioning',
                   'setting-put', 'tailbone.theme', 'falafel']
            subprocess.check_call(cmd)

            # set main image
            cmd = [rattail, '-c', quiet_conf, '--no-versioning',
                   'setting-put', 'tailbone.main_image_url', '/messkit/img/messkit.png']
            subprocess.check_call(cmd)

            # set header image
            cmd = [rattail, '-c', quiet_conf, '--no-versioning',
                   'setting-put', 'tailbone.header_image_url', '/messkit/img/messkit-small.png']
            subprocess.check_call(cmd)

            # set favicon image
            cmd = [rattail, '-c', quiet_conf, '--no-versioning',
                   'setting-put', 'tailbone.favicon_url', '/messkit/img/messkit-small.png']
            subprocess.check_call(cmd)

            rprint("\n\tdb schema installed to:  [bold green]{}[/bold green]".format(
                obfuscate_url_pw(dburl)))

            if self.basic_prompt("create admin user?", True, is_bool=True):

                # get admin credentials
                username = self.basic_prompt('admin username', 'admin')
                password = None
                while not password:
                    password = self.basic_prompt('admin password', is_password=True)
                    if password:
                        confirm = self.basic_prompt('confirm password', is_password=True)
                        if not confirm or confirm != password:
                            rprint("[bold yellow]passwords did not match[/bold yellow]")
                            password = None
                fullname = self.basic_prompt('full name')

                rprint()

                # make admin user
                rattail = os.path.join(bindir, 'rattail')
                cmd = [rattail, '-c', quiet_conf, 'make-user', '-A', username,
                       '--password', password]
                if fullname:
                    cmd.extend(['--full-name', fullname])
                subprocess.check_call(cmd)

                rprint("\n\tadmin user created:  [bold green]{}[/bold green]".format(
                    username))

        if self.basic_prompt("make poser dir?", True, is_bool=True):
            rprint()

            # make poser dir
            poser_handler = self.app.get_poser_handler()
            poserdir = poser_handler.make_poser_dir()

            rprint("\n\tposer dir created:  [bold green]{}[/bold green]".format(
                poserdir))

        rprint("\n\t[bold green]initial setup is complete![/bold green]")

        if schema_installed:
            rprint("\n\tyou can run the web app with this command:")
            pserve = os.path.join(bindir, 'pserve')
            rprint("\n\t[blue]{} file+ini:{}[/blue]".format(pserve, web_conf))

        rprint()

        # TODO: somewhere should ask about apache proxy, https etc.?

    def basic_prompt(self, info, default=None, is_password=False, is_bool=False):

        # message formatting styles
        style = Style.from_dict({
            '': '',
            'bold': 'bold',
        })

        # build prompt message
        message = [
            ('', '\n'),
            ('class:bold', info),
        ]
        if default is not None:
            if is_bool:
                message.append(('', ' [{}]: '.format('Y' if default else 'N')))
            else:
                message.append(('', ' [{}]: '.format(default)))
        else:
            message.append(('', ': '))

        # prompt user for input
        try:
            text = prompt(message, style=style, is_password=is_password)
        except (KeyboardInterrupt, EOFError):
            rprint("\n\t[bold yellow]operation canceled by user[/bold yellow]\n",
                   file=self.stderr)
            sys.exit(2)

        if is_bool:
            if text == '':
                return default
            elif text.upper() == 'Y':
                return True
            elif text.upper() == 'N':
                return False
            rprint("\n\t[bold yellow]ambiguous, please try again[/bold yellow]\n")
            return self.basic_prompt(info, default, is_bool=True)

        return text or default

    def make_db_url(self, dbtype, dbhost, dbport, dbname, dbuser, dbpass):
        try:
            # newer style
            from sqlalchemy.engine import URL
            factory = URL.create
        except ImportError:
            # older style
            from sqlalchemy.engine.url import URL
            factory = URL

        if dbtype == 'mysql':
            drivername = 'mysql+mysqlconnector'
        else:
            drivername = 'postgresql+psycopg2'

        return factory(drivername=drivername,
                       username=dbuser,
                       password=dbpass,
                       host=dbhost,
                       port=dbport,
                       database=dbname)

    def test_db_connection(self, url):
        engine = sa.create_engine(url)

        # check for random table; does not matter if it exists, we
        # just need to test interaction and this is a neutral way
        try:
            engine.has_table('whatever')
        except Exception as error:
            return str(error)
