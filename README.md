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

I largely wrote this to convert my own data, so I've made some assumptions.
I thought other people may find this useful, so I added some features like the lang and frontmatter options.

This script assumes everything is a post. If the status is draft it will add the `published: false` tag
to the frontmatter. Don't automatically assume that the output is perfect. You will need to go through exported post 
to verify that it is correct, and fix what you need to fix.

This script does not convert the post text to markdown, it writes it as-is from the plaintext key.
This script also does not handle images at all.

This script should work with Python 3.9 and up.