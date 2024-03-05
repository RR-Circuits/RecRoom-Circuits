---
slug: /
sidebar_position: 0
---
# Welcome!

# Creating a guide

Docs and guides are parsed using MDX. This means that you can use markdown, as well as JSX! (please don't define your own components here though)
""":::caution JSX is not HTML

They might look very similar, but the JSX syntax is different from HTML. This means that you can't just pop a `<p>` tag in a guide without generating errors.
Tags still have to be closed with a `/`, though!

:::"""

## Components
There are currently 2 custom components/tags you can use:
- `IChip`
- `GuideMedia`

### IChip
The `IChip` component will return the image of a chip from a given `uuid`.
If you add the `redirect` attribute, the image will hold a link that brings you to the doc page of the chip.

```jsx title="Guides/YourGuide/doc.mdx"
<IChip uuid="98b99011-9be8-43b3-89cc-1e9d55bd8b51" /> // this will become an image of the "Absolute Value" chip.
<IChip uuid="98b99011-9be8-43b3-89cc-1e9d55bd8b51" redirect /> // same as the above, except this one is clickable
```

### GuideMedia
The `GuideMedia` component has 2 required attributes: `fileName` and `fileType`.
`fileName` will be the file name of a file in `Guides/YourGuide/assets`.
`fileType` is the type of media that the site needs to use.
Available options are:
- `image`
- `video`
- `audio`

We recommend the ussage of the `height` and `width` attributes for videos and images, as some files may be too large for the page to look nice.
Use `"#%"` if you want it to use a relative size. (# is a number)

There is also the `useURL` attribute, but we do not recommend it.
If you do use it, `fileName` will have to be a direct link to a file on the internet.

Examples:
```jsx title="Guides/YourGuide/doc.mdx"
<GuideMedia fileName="Tutor1.png" fileType="image" /> // an image without a specified size
<GuideMedia fileName="FullTutorial.mp4" fileType="video" width="50%" height="50%"/> // a video, displayed at half its regular size
<GuideMedia fileName="https://foo.bar/Sample.mp3" fileType="audio" useURL/> // an online audio file, referenced by a URL
```
