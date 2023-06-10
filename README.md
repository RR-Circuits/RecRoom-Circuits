# Rec Room Circuits
Maintained by Funn Punn and joksulainen

| Task                  | Progress |
|-----------------------|----------|
| Implement Chip JSON   | ✅        |
| Create Chip Docs      | ✅\*      |
| Create Circuit Guides | 🚧        |

\* automated creation finished, still need community efforts

## Before contributing

I cannot express the importance of making a new branch to make your changes in instead of directly committing to the main branch in the forked repository enough.
It will save you so many headaches caused by merge conflicts from changes to the main branch.
For the sake of all of our sanity, please make your changes in a branch that isn't the main branch and use that to make a pull request instead.

\- joksulainen

## How to add extra info to chip files?

1. Fork the repository if you haven't already.
1. Go to the `ExtraInfo` folder under the root directory.
1. Find your chip. You can search by name or UUID.
1. Edit the contained markdown. Conform to the formatting found in the file, we will correct any mistakes manually by adding commits to your pull request if allowed.
1. Commit your changes and submit a pull request, we'll do the rest.

## How to make guides?

This process is almost identical to the ExtraInfo one.

1. Fork the repository if you haven't already.
1. Go to the `Guides` folder under the root directory.
1. Make a new `.mdx` file. Add your markdown content there. Please use a format similar to the other guides if any.
1. Commit your changes and submit a pull request. we'll do the rest.

## Tips:

Docusaurus works with markdown files, but it also has a few plugins.
This means that you can create note, tip, info, danger and caution boxes to display meaningful notes.

```md
:::note

Some **content** with _Markdown_ `syntax`. Check [this `api`](#).

:::

:::danger

Some **content** with _Markdown_ `syntax`. Check [this `api`](#).

:::

:::tip

Some **content** with _Markdown_ `syntax`. Check [this `api`](#).

:::
```

You can also test the new pages by going to `Circuits` and running `npm run start -- --host 0.0.0.0`. (after installing the `docusaurus` module, of course).


### Credits

- joksulainen - went through 7 stages of life in one day, just to make the most important stuff work
- Funn Punn - did a thing, I guess
- CV2 community - used this (actually I'm not sure)
