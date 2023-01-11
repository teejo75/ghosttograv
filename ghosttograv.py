import argparse
import json
from types import SimpleNamespace
from pathlib import Path
from slugify import slugify

# blog.md frontmatter based on the Grav blog skeleton
blog_frontmatter = '''---
title: Home
sitemap:
    changefreq: monthly
body_classes: 'header-dark header-transparent'
hero_classes: 'text-light title-h1h2 overlay-dark-gradient hero-large parallax'
blog_url: /blog
show_sidebar: true
show_breadcrumbs: true
show_pagination: true
content:
    items:
        - '@self.children'
    limit: 5
    order:
        by: date
        dir: desc
    pagination: true
    url_taxonomy_filters: true
pagination: true
---
'''


def fix_apostrophe(text):
    return text.replace("'", "''")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog="ghosttograv", description="Convert ghost export json to grav blog items")
    parser.add_argument("-g", "--ghost", action="store", dest="ghostexportfile", help="Ghost Export JSON File",
                        required=True)
    parser.add_argument("-o", "--out", action="store", dest="outpath",
                        help="Folder to use for output, defaults to ./01.blog")
    parser.add_argument("-l", "--lang", action="store", dest="lang",
                        help="Language code to use as file suffix, eg 'item.en.md'. Omit to not have tag")
    parser.add_argument("-f", "--frontmatter", action="append", dest="frontmatter",
                        help="Add additional frontmatter string tags to item.md. Use as many times as required.")
    parser.add_argument("-s", "--slug", action="store_true", dest="slug",
                        help="If this argument is present, the post slug will be used as the item.md path. Otherwise, "
                             "the path will be generated from the post title.")
    args = parser.parse_args()
    if args.outpath is not None:
        outpath = args.outpath
    else:
        outpath = "./01.blog"

    print(f"Attempting to load {args.ghostexportfile}...")
    f = open(args.ghostexportfile, encoding="utf8")
    ghostdata = json.load(f, object_hook=lambda d: SimpleNamespace(**d))
    settings = ghostdata.db[0].data.settings
    tags = ghostdata.db[0].data.tags
    print(f"Found {len(tags)} tags")
    posts_tags = ghostdata.db[0].data.posts_tags
    posts = ghostdata.db[0].data.posts
    print(f"Found {len(posts)} posts")

    users = ghostdata.db[0].data.users
    print(f"Found {len(users)} users")
    posts_authors = ghostdata.db[0].data.posts_authors

    # Extract site title and description for blog.md
    print("Extracting site title and description from settings for blog.md")
    site_title = ""
    site_description = ""
    for setting in settings:
        if setting.key == "title":
            site_title = setting.value
        if setting.key == "description":
            site_description = setting.value
    print(f"Checking and creating {outpath} if necessary...")
    poutpath = Path(outpath)
    if not poutpath.exists():
        poutpath.mkdir(parents=True)
    print(f"Creating blog.md in {outpath} (File will be overwritten if it exists)")
    if args.lang is not None:
        blogmd = Path.joinpath(poutpath, f"blog.{args.lang}.md")
    else:
        blogmd = Path.joinpath(poutpath, "blog.md")
    with blogmd.open('w', encoding="utf8") as blogfile:
        blogfile.writelines(blog_frontmatter)
        blogfile.write(f"# {site_title}\n")
        blogfile.write(f"## {site_description}\n")

    print(f"Extracting posts in to {outpath}")
    postcount = 1
    postmax = len(posts)
    for post in posts:
        print(f"Processing post {postcount} of {postmax}", end="\r", flush=True)

        # Extract tags
        post_tagids = []
        post_tags = []
        for pt in posts_tags:
            if pt.post_id == post.id:
                post_tagids.append(pt.tag_id)

        for tagid in post_tagids:
            for tag in tags:
                if tagid == tag.id:
                    post_tags.append(tag.slug)

        author = ""
        authorid = ""
        if len(users) > 1:
            # Extract authors
            for pa in posts_authors:
                if pa.post_id == post.id:
                    authorid = pa.author_id
            for u in users:
                if authorid == u.id:
                    author = u.name
        else:
            author = users[0].name
        # If -s or --slug is present use post.slug as item.md folder name
        if args.slug is True:
            itempath = Path.joinpath(poutpath, Path(post.slug))
        else:
            # Default use post title as item.md folder name
            itempath = Path.joinpath(poutpath, Path(slugify(post.title)))

        if not itempath.exists():
            itempath.mkdir()

        if args.lang is not None:
            itemmd = Path.joinpath(itempath, f"item.{args.lang}.md")
        else:
            itemmd = Path.joinpath(itempath, 'item.md')
        with itemmd.open('w', encoding="utf8") as itemfile:
            itemfile.write("---\n")
            itemfile.write(f"title: '{fix_apostrophe(post.title)}'\n")
            itemfile.write(f"author: {author}\n")
            itemfile.write("taxonomy:\n")
            itemfile.write("    category:\n")
            itemfile.write("        - blog\n")
            if len(post_tags) > 0:
                itemfile.write(f"    tag: [{','.join(post_tags)}]\n")

            if args.frontmatter is not None:
                for fm in args.frontmatter:
                    itemfile.write(f"{fm}\n")

            # My ghostfile post date format matches more or less what I use in Grav so I don't need to change it much.
            itemfile.write(f"date: '{post.created_at[:-3]}'\n")  # Should remove the seconds from the timestamp
            if post.status == "draft":
                itemfile.write("published: false\n")

            itemfile.write("---\n")
            itemfile.writelines(post.plaintext, )

    print("Finished processing json")
