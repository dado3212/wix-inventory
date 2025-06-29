# wix-inventory
A Python script for uploading to Wix and syncing to Instagram.


## Initial Install
Check out this repo and run the following commands to install the necessary Python libraries:
```
python3 -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
```

From https://manage.wix.com/account/api-keys generate an API key. Then create a new file with `touch secret.py` and add three constants to it with the format
```
API_KEY = '<insert api key>'
ACCOUNT_ID = '<account id>'
SITE_ID = '<site id>'
```

The `API_KEY` is the API Key you created. The `ACCOUNT_ID` is on the right side of the aforementioned API keys page. The `SITE_ID` is the alphanumeric if you go to your site dashboard and copy the `<code>` from the URL in the format `https://manage.wix.com/dashboard/<code>/home?referralInfo=my-sites`.

You'll then need to double-click the `.command` files and unblock them in Settings > Privacy & Security. You should only have to do this once.

You also need to install [Homebrew](https://brew.sh/) and then do `brew install imagemagick` for the image resizing to work.

You then need to automatically forward product items from Wix to Instagram. You can do this by <TODO>

## Developing
https://dev.wix.com/docs/rest/ has the full REST API.

## Customizing

If you go into the Wix Editor and enable "Dev Mode" and then click the `{}` on the left and create a new backend file called `http-functions.js` when you can define your own functions, where `get_changeThis` is hit by `https://spencerbeals.com/_functions/changeThis`.

<img width="294" alt="Screenshot 2025-06-29 at 12 51 46 PM" src="https://github.com/user-attachments/assets/18360565-30c7-4c2c-9d19-0c469c574b79" />

This is the code I put in to be able to adjust the images and add in labels.

```
function convertImage(img) {
    return img.replace('wix:image://v1/', 'https://static.wixstatic.com/media/').replace(/\/file\..*$/, '');
}

function formatDescription(html) {
  const text = (html || '')
    .replace(/<p>(.*?)<\/p>/g, '$1\n')    // turn <p> into newlines
    .replace(/<[^>]+>/g, '')              // remove any other tags
    .replace(/\r?\n/g, '\n')              // normalize newlines
    .replace(/&nbsp;/g, '')               // remove this ()
    .replace(/\t/g, ' ')                  // tabs break TSV too
    .trim();

  return text.includes('\n') ? `"${text.replace(/"/g, '""')}"` : text;
}

export async function get_changeThis(_request) {
  // Once we hit 100 then we need to introduce pagination.
  const { items } = await query('Stores/Products').limit(100).find({
    appOptions: {
      // Include product variants in the query
      includeVariants: true,
    },
  });

  const headers = ['id', 'link', 'title', 'availability', 'description', 'rich_text_description', 'image_link', 'additional_image_link', 'price', 'sale_price', 'identifier_exists', 'condition', 'fb_product_category', 'size', 'item_group_id', 'quantity_to_sell_on_facebook', 'internal_label'];
  const lines = [headers];

  for (const p of items) {
    let i = 0;
    for (const v of p.variants) {
        const isPrint = (v.choices['Size'] && (v.choices['Size'].includes(' Print') || v.choices['Size'].includes(' Canvas')));
        const row = [
            p.variants.length > 1 ? `${p._id}_${i}` : p._id,
            `https://www.spencerbeals.com/product-page/${p.slug}?utm_source=facebook&utm_medium=wix_meta_feed&utm_campaign=freelistings`,
            p.name,
            p.inStock ? 'in stock' : 'out of stock',
            formatDescription(p.description || ''),
            p.description.replace(/&nbsp;/g, ''), // includes HTML
            convertImage(p.mainMedia),
            p.mediaItems.slice(1).map(m => convertImage(m.src)).join(','),
            `${v.variant.price} USD`,
            `${v.variant.price} USD`,
            'no',
            'new',
            999, // home > home goods > home decor > decorative accents > posters, prints & paintings
            p.variants.length > 1 ? v.choices['Size'] : null,
            p.variants.length > 1 ? p._id : null,
            p.inStock ? (isPrint ? 100 : 1) : 0, // Pretend we have 100 prints but only 1 original
            JSON.stringify(isPrint ? ['print'] : []),
        ];
        lines.push(row);
        i++;
    }
  }

  return ok({
    headers: {
      'Content-Type': 'text/tab-separated-values'
    },
    body: lines.map(l => l.join('\t')).join('\n'),
  });
}
```
