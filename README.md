# GhostToGrav

This script will convert a ghost blog export to grav blog item.md files.

## Usage:
  * -g _ghostexport.json_ **Required:** Specify the json file that contains the exported ghost blog data.
  * -o _path_ **Optional** Specify the path to export to. Defaults to `./01.blog`
  * -l _lang_ **Optional** Specify the two letter language code, eg `en`.
    This will add the language code suffix to the blog and item.md files as `blog.en.md` and `item.en.md`.
    If you omit this argument then no language code suffix will be used.
  * -f _quoted string_ **Optional** Add additional frontmatter tags to `item.md`. 
    Specify this argument as many times as desired. e.g., `-f "show_sidebar: true" -f "hero_classes: text-light"`
    These will be written one after the other so spaces should be kept, otherwise you can try to specify everything
    in a line using `\n` as a separator.
  * -s **Optional** If this argument is present, the path for `item.md` will be generated from the ghost post slug.
    Otherwise, the path is generated from the ghost post title.  

I largely wrote this to convert my own data, so I've made some assumptions.
I thought other people may find this useful, so I added some features like the lang and frontmatter options.

This script does not distinguish between pages and posts in the ghost export. 
If the post status is draft it will add the `published: false` tag to the item.md frontmatter.

The script extracts authors and applies them to their respective posts.
If there is only one user, they are set as the post author.
The script automatically adds the 'blog' category taxonomy to each item.md.
If there are any tags applied to a post, the script will extract them and apply them to the respective item.md.

This script does not convert the post text to markdown, it writes it as-is from the plaintext key.
This script also does not handle images at all.

This script should work with Python 3.9 and up.

I highly recommend using virtualenv first so that your system packages don't get clobbered: `python -m venv venv` then `./venv/bin/activate` or 
`venv\Scripts\activate.bat` for Windows.
Then do `pip install -r requirements.txt` to install python-slugify dependency. 