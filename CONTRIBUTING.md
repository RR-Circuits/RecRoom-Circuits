# Before contributing

I cannot express the importance of making a new branch to make your changes in instead of directly committing to the `main` branch in the forked repository enough.
It will save you so many headaches caused by merge conflicts from changes to the `main` branch.
For the sake of all of our sanity, please make your changes in a branch that isn't the `main` branch and use that to make a pull request instead.

\- joksulainen

## How to add extra info to chips?

1. Fork the repository and make a new branch if you haven't already.
1. Go to the `ExtraInfo` directory under the root directory.
1. Find your chip. You can search by name or UUID.
1. Edit the contained markdown. Conform to the formatting found in the file, we will correct any mistakes manually.
1. Commit your changes and submit a pull request, we'll do the rest.

## How to make guides?

1. Fork the repository and make a new branch if you haven't already.
1. Go to the `Guides` directory under the root directory.
1. Make a new directory that contains a `doc.mdx` file and `assets` directory. You can look at other guides to get a handle on the structure of the directory.
1. Make your guide in the `doc.mdx` file and put any images and other assets in the `assets` directory. These assets can be embedded into the guide with the `<GuideMedia fileName="" type="image|audio|video" />` tag.    
    - Read the [introduction page for guides](https://circuits.pages.dev/guides/) for more details about available tags.
1. Commit your changes and submit a pull request, we'll do the rest.
