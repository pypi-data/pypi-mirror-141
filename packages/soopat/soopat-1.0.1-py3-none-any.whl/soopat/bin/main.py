from pathlib import Path

import click
from passconfig import PassConfig

from soopat.core import Soopat
from soopat import version_info


epilog = '''
Contact: {author} <{author_email}>
'''.format(**version_info)


@click.group(epilog=epilog)
@click.version_option(version=version_info['version'])
@click.option('-c', '--configfile',
              help='the configration file to store username or password',
              default=Path('~').expanduser().joinpath('.soopat.ini'),
              show_default=True)
@click.option('-s', '--section', help='the section name of config', default='common', show_default=True)
@click.pass_context
def cli(ctx, **kwargs):
    """Soopat Client"""
    ctx.ensure_object(dict)
    ctx.obj['sp'] = Soopat()
    ctx.obj['pc'] = PassConfig(configfile=kwargs['configfile'], section=kwargs['section'])


@click.command()
@click.pass_context
@click.option('-a', '--auto', help='register automaticly', is_flag=True)
def register(ctx, **kwargs):
    """register an account"""
    sp = ctx.obj['sp']
    pc = ctx.obj['pc']
    res = sp.register(auto=kwargs['auto'])
    if res:
        pc.username = res[0]
        pc.password = res[1]
        pc.save()


download_epilog = '''
\b
Examples:
    soopat download -i 202010463344
    soopat download -i http://www.soopat.com/Patent/202111607937
    soopat download -i 202010463344 -u your_username -p your_password -o out.pdf
'''


@click.command(no_args_is_help=True, epilog=download_epilog)
@click.pass_context
@click.option('-i', '--url', help='the url or ID to download', required=True)
@click.option('-u', '--username', help='the username to login')
@click.option('-p', '--password', help='the password to login')
@click.option('-o', '--outfile', help='the output filename')
def download(ctx, **kwargs):
    """download the pdf"""
    sp = ctx.obj['sp']
    pc = ctx.obj['pc']

    username = kwargs['username']
    password = kwargs['password']

    if not all([username, password]):
        username, password = pc.get()

    if sp.login(username, password):
        sp.download(kwargs['url'], outfile=kwargs['outfile'])
        pc.save()


def main():
    cli.add_command(register)
    cli.add_command(download)
    cli()


if __name__ == "__main__":
    main()
