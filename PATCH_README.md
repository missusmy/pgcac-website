# Feb2026 Patch

## New Template

```text
project-root/
└── templates/
    └── base-fullwidth.html
```

The new template removes the left and right sidebars and allows addition of full-width sections.

### Basic Page Blocks

```html
{% extends "base-fullwidth.html" %}

{% block title %}Page Title{% endblock %}

{% block meta_description %}Page metadata description{% endblock %}       <!-- if missing, it will default to description found on the homepage -->
{% block og_slug %}[image filename]{% endblock %}                         <!-- if missing, it will default to the og:image from the homepage -->

{% block notification %}
  {% include "partials/_default_notification.html" %}                     <!-- adds default notification under top nav -->

  &#10084;&#65039; <a href="/">Hello</a> &#10084;&#65039; Postgres fans!  <!-- or add custom notification -->
{% endblock %}

{% block maincontent %}
  <!-- add page content here -->
{% endblock %}
```

Pages will need to add sections with Bootstrap containers in order to center the content on the page.

```html
<div id="section-name" class="py-4 py-md-5">
  <div class="container">
    <div class="row">
      <div class="col-12 col-md-10">
        <h1>Page Title</h1>
        <p class="lead">Lorem ipsum dolor sit amet consectetur adipisicing elit. Deleniti unde repellendus quis quo doloremque officiis id maiores quia modi, exercitationem aliquam, assumenda sit accusamus, suscipit quaerat aliquid facere nisi ipsum magnam nulla? Provident possimus, molestiae sunt rem, eius neque quaerat voluptas asperiores aliquam esse nisi error itaque similique perspiciatis architecto.</p>
      </div>
    </div>
  </div>
</div>
```

### Partials

Sections that are repeated on the site are added to `templates/partials` in order to be re-used on the site.

```text
project-root/
└── templates/partials
    ├── _community_support.html       # looking for support section on FAQ & contact pages
    ├── _default_notification.html    # default notification message
    └── _thank_you.html               # thank you section on donate, news, sponsors, & about pages
```

How to use on the page:

```html
{% include "partials/_community_support.html" %}
```

## Changes to Info Architecture

### News

News article addition now touches 2 pages: Home & News.

On the Homepage, place the news item date and title under `#latest-news > .container > .news-cards > .row`. Example:

```html
<div class="col-12 col-md-6 col-lg-4 mb-4">
  <div class="card h-100">
    <div class="card-body d-flex flex-column">
      <a class="link-anchor" id="2026-03-03" name="2026-03-03"></a> <!-- date as both 'id' and 'name' -->
      <h5 class="mt-0 mb-2">3 March 2026</h5>
      <h3 class="mt-0 mb-4 text-emphasis">Updates to PGCA Sponsorship Levels & Website</h3>
      <p class="mt-auto"><a href="/news#2026-03-03">Read item</a></p> <!-- link to news item on the news page -->
    </div>
  </div>
</div>
```

On the News page, each news item is a `.card` under `#news > .news-cards`. Example:

```html
<div class="card">
  <div class="container margin">
    <a class="link-anchor" id="2026-03-03" name="2026-03-03"></a>
    <h3><span class="bd-content-title text-emphasis">[news item title]<a class="anchorjs-link" aria-label="Anchor" href="#2026-03-03"></a></span></h3><!-- anchor link appears on hover -->
    <h5 class="mt-0 mb-4">3 March 2026</h5>
    [news item content]
  </div>
</div>
```

**Note:** the date (YYYY-MM-DD) needs to be added to `id` and `name` on `.link-anchor` and also to the href on `.anchorjs-link`.

### Metadata

All pages now have HTML metadata descriptions and unique og:images.

A **metadata description** is added as a block after the title block. If it's missing, the page will default to the description found on the homepage.

```html
{% block meta_description %}Page metadata description{% endblock %}
```

The **og:image** is the image that shows up when a webpage is shared on a social platform. They should be 1200x630 to be compatible with the broadest number of social platforms. Place the og:images in the `static/img/og` folder. They should be saved as PNGs.

```text
project-root/
└── static/
    └── img/
        └── og/
            └── img-name.png
```

Add the og:image information to the page as a block after the metadata description block. Only the filename, without the extension, is needed for this block. This block currently only supports PNGs. This can be changed to allow other filetypes, if needed, but it will require updating the block on every page.

```html
{% block og_slug %}[image filename]{% endblock %}
```

### Website Images

This site refresh includes a lot more graphics, mostly as background images. The images are located in the existing `static/img` folder:

```text
project-root/
└── static/
    └── img/
```

**Graphic file formats:** For website optimization (page load), it's best to use file formats that are smallest in size, such as WEBP (for raster images) or SVG (for vector images). All of the new banner elephants are transparent images, so there is a PNG and a WEBP version of each. WEBP will generally give you the smallest file size while still retaining image quality for images that have many colors and gradients, especially compared to JPGs and PNGs. WEBPs can be transparent, so they can be used in cases where PNGs (and previously GIFs) were traditionally used.

**Graphic file sizes:** It's best for the images to be under 100KB. 100-200KB is okay, but they should almost never be more than 1MB.

**Backup file formats:** Because NOT all browsers support WEBP, in order to support older browsers, you have to additionally upload a fallback graphic for the WEBP. The only time it's best to still use a PNG without a fallback is when the image only has a few flat colors, transparent or not, like a flat-color logo. Instructions for setting up a fallback are below:

To use an image as a background image with a fallback, list the larger, more widely-supported file format first and then list the WEBP (smaller file). Example:

```css
.class {
  background-image: url(/static/img/img-name.jpg);  /* fallback image for older browsers */
  background-image: url(/static/img/img-name.webp);
}
```

The order of the fallback is opposite when included as an image on the page. Here's an example of how an image with a fallback is added in the HTML:

```html
<picture>
  <source srcset="/static/img/img-name.webp" type="image/webp">
  <img src="/static/img/img-name.jpg" loading="lazy" alt="img alt" /> <!-- use lazy loading when the image is further down the page so it will only load when scrolling to it -->
</picture>
```

The above is only a basic example of the picture/source tags. It can be customized for screen resolution, screen width, etc., and can get much more complex.

Note: the iconography in the new design are using Fontawesome icons, which was existing on the site.

### Notification Bars

Notification bars are a new addition to the template and are seen below the top navigation on each page. The content for the default notification bar is a partial (see above). Add a notification bar to a page by adding a notification block before the maincontent block.

Default notification block:

```html
{% block notification %}
  {% include "partials/_default_notification.html" %}
{% endblock %}
```

Custom notification sample:

```html
{% block notification %}
  &#10084;&#65039; <a href="/">Hello</a> &#10084;&#65039; Postgres fans!
{% endblock %}
```

The notification bar will only show up if either a default notification block or a custom notification block is added to the page.

### Donation Metrics

Below the "Two Ways to Donate" section on the Donate page is a section with 3 donation metrics that should be updated every couple months:

- annual donations
- \# of individuals who donated
- \# of corporations that donated
- date the metrics was updated

### Sponsorship Prospectus

The currently prospectus is in the same existing location as the previous versions:

```text
project-root/
└── static/
    └── pdf/
        └── filename.pdf
```

We've added month and year (MMMYYYY) to the filename so visitors can tell which version they've downloaded.

A link to the sponsorship prospectus PDF is in 3 places: once on the Donate page and twice on the Sponsors page. All 3 places need to be updated if the prospectus is changed.

- Donate page:
  - "Two Ways to Donate" > "Donate via other means" > <u>See Sponsorship prospectus</u>
- Sponsors page:
  - top section > "See Sponsorship Prospectus" button
  - quote section above "Thank you" at the bottom > review the <u>PGCA sponsorship prospectus</u>

### Copyright Date

The copyright year will need to be manually updated every year. It only needs to be updated in the footer section on the template(s).

## Sponsors

Information/items needed from each sponsor to be added to the sponsors page:

- company logo
- company name
- company URL
- company description - up to 305 characters, including spaces (not needed for Friend level)

### Company Logo

The template requires the company logos to be transparent. It's best to use SVGs. If an SVG is not available, transparent PNG is also acceptable but not desired because they may be very large in file size.

The default behavior for logos is the logo displayed as-is on light theme. On dark theme, a filter turns the logo to an all-white logo. There are 2 options if the logos shouldn't be all white on dark theme: (1) "always color" using `.always-color` class will keep the logo in it's original state on dark theme (keep in mind that dark parts of the logo will not have a lot of contrast on the dark background); and, (2) "grayscale" using `.grayscale` class will convert the color logo to grayscale on dark theme.

### Four Levels of Sponsors

The sponsors are separated into levels, and each level has slightly different HTML for the sponsors.

### Benefactor Level

```html
<div class="col-12 col-lg-6 sponsor-item">
  <div class="card h-100 shadow-sm">
    <div class="card-body">
      <a href="https://aws.amazon.com" target="_blank" rel="noopener" title="AWS" class="logo-wrap">
        <img class="organisation-logo" src="/static/img/sponsors/[image filename]" alt="[company name]" />  <!-- Add class "always-color" if the logo should also be the same color version on dark theme; add class "grayscale" if it should be a grayscale (not fully white) version on dark theme. -->
      </a>
      <div class="company-name text-primary">[company name]</div>
      <div class="company-url"><i class="globe-icon" aria-hidden="true"></i><a href="[company url]" target="_blank" rel="noopener">[company url]</a></div>
      <div class="company-desc">[company description]</div> <!-- Not included in Friend level -->
      <div class="donation-date">Donated in <nobr>[mmm yyyy]</nobr></div>
    </div>
  </div>
</div>
```

### Patron and Supporter Levels

The difference in the HTML for the other levels are other the classes on `.sponsor-item`. For Patron and Supporter levels, the classes are as follows:

```html
<div class="col-12 col-md-6 col-lg-4 sponsor-item">
```

### Friend Level

The classes for `.sponsor-item` for Friend level are as follows:

```html
<div class="col-6 col-md-4 col-lg-3 sponsor-item">
```

Friend level does not include company description (`.company-desc`).

## Completed QA Checklist

Mobile:

- Safari on iOS
- Chrome on Android

Desktop:

- Chrome
- Safari
- Edge
- Firefox

Accessibility:

- supports up to 400% zoom (standard for accessibility)
- passes Accessibility Insights FastPass
