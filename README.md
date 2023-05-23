# Rec Room Circuits
Maintained by Funn Punn and Joksulainen

| Task                  | Progress |
|-----------------------|----------|
| Implement Chip JSON   | ✅        |
| Create Chip Docs      | 🚧        |
| Create Circuit Guides | 🚧        |

## How to add extra info to chip files?

1. Fork the repository and preferably make a new branch.
1. Go to the `ExtraInfo` folder under the root directory.
1. Find your chip. You can search by name or UUID.
1. Edit the contained markdown. Conform to the formatting found in the file, we will correct any mistakes manually by adding commits to your pull request if allowed.
1. Commit your changes and submit a pull request. I'll do the rest.

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
...
```

You can also test the new pages by going to Website/circuits and running `npm run start -- --host 0.0.0.0`. (after you installed the `docusaurus` module, of course).
