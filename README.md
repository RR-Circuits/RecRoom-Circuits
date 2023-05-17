# Rec Room Circuits
Maintained by Funn Punn

| Task                  | Progress |
|-----------------------|----------|
| Implement Chip JSON   | ✅        |
| Create Chip Docs      | 🚧        |
| Create Circuit Guides | 🚧        |

## How to add extra info to chip files?

### 1) Go to the ExtraInfo folder under the root directory.
### 2) Find your chip file. You can both search by name or UUID.
### 3) Edit the chip file. It uses a template, but it's not neccesary to follow it.
### 4) Save the file and submit a pull request. I'll do the rest.

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
