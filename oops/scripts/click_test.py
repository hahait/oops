#!/usr/bin/env python
import click

@click.group()
def cli():
    pass

@cli.command()
@click.option("--name", help="名称")
def setname(name):
    click.echo('我的名字: %s'%(name))

@cli.command()
@click.option("--age", type=int, help="年龄")
def setage(age):
    click.echo('我的年龄: %s' %(age))

# cli.add_command(setname)
# cli.add_command(setage)

if __name__ == '__main__':
    cli()
