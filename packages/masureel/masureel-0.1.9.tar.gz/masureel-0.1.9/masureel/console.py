import os
import click

from . import __version__
from .translate import translate_file
from .data import get_products, get_json, get_tool_database, get_products_by_collection, update_product_topviews
from .topviews import get_topviews


@click.command()
@click.option("--update", "-u", is_flag=True, help='Updates the Airtable cache on disk')
@click.option("--topviews", "-t", is_flag=True, help='Updates the topviews')
@click.option("--new", "-n", is_flag=True, help='Adding a new collection to the online tool. Type the name of the collection after this flag.')
@click.argument('collection', required=False)
@click.option("--translate", "-t", is_flag=True, help='Use this flag to translate Dutch .txt orders to English.\n Type the name of the file after this flag, e.g. text_to_translate.txt')
@click.argument('filename', type=click.Path(exists=True), required=False)
@click.version_option(version=__version__)
def main(update, translate, filename, new, collection, topviews):

    if topviews:
        tvs = get_topviews()
        update_product_topviews(tvs)
    if translate:
        if filename is None:
            click.secho(
                f"Please enter the name of the file you want to translate after the --translate flag!", fg='yellow')
        else:
            click.echo(click.format_filename(filename))
            print(f'translating {filename} in {os.getcwd()}')
            translate_file(filename)

    if collection is not None and new is False and translate is False:
        click.secho(
            f'Did you mean to run the script with the --new flag for {collection}? Try again using: masureel --new {collection}', fg='yellow')
    if new:
        if collection is None:
            click.secho(
                'Specify a collection by typing the name after the --new flag, like this: masureel --new collection', fg='red')
        else:
            collection = collection.capitalize()
            collections = get_json('collections.json')
            if collection in collections:
                print(f'We found an entry for {collection}, grabbing records')
                batch = get_products_by_collection(collection)
                for code, product in batch.items():
                    print(code, product)
                    if product.data_present:
                        print(
                            f'{product} is already present in the online tool as a {product.type}')
                    if product.shader_present:
                        print(f'we already have the shader for {product}')
                    if product.topview_present:
                        print(f"we already have a topview for {product}")
            else:
                click.secho(
                    f"Hmmm, can't find {collection} in our database...", fg='red')
    if update:
        # getting airtable pds
        pds = get_products()
        # grabbing pds from database.csv
        online_products = get_tool_database()
        # grabbing shaders from .matlib
        shaders = get_json('shaders.json')
        for p in pds:
            if p.code in online_products.keys():
                print(
                    f'{p.name} is present in the online tool, values are {online_products[p.code]}')
            if p.code in shaders.keys():
                print(f'{p.name} is present in matlib, we can create render jobs!')
