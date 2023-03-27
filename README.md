# REAL ESTATE LISTINGS IN NIGERIA

## Run project to get 7 days listings data
- make request to the link that contains '7 days' in it
- all 21 listings be gotten from each page
- next link would be formed by adding one to the ending digit.

## What items would we scrape for this project?
- unique id of the property **(ref)**;
- unique link **(url)** to the listing;
- **page** number where listing was gotten from;
- price (rent/month, rent/year or full cost);
- number of **bedroom**;
- number of **bathroom**;
- number of **toilet**;
- number of cars alloted for **parking** space;
- area of land covered in square meters **(area_sqm)**;
- the date it was listed **(listdate)**;
- the type **(listtype)** of listing- flat,land,apartment,...;
- further description **(details)**;
- area, city and state where it is located **(address)**;
- name of the marketing agency **(marketer)** advertising this listing;
- **contact** of said agency.

## How do we transform each of these items?
- Any items gotten from xpath similar to `...//strong[text()=""]/...` have a common unclean substring thus, on input; items are cleaned, this substring removed and resulting text stripped of whitespaces. This is made as `default_input_processor` since it has a high occurence.

- `price`: The first non-null value is collected, and thousand delimeters are eliminated.

        > (100,000, 100,000) &rarr; 100000

- `area_sqm`: Same with `price` but in addition, units of measurement (sqm) are removed

        > 40,000 sqm &rarr; 40000

- `contact`: Contact numbers in intl. format are stripped of '+' then converted to local format.

        > +23481... &rarr; 081...

- `desc`: All matches from xpath are needed since this makes up the entire description; so a simple join on whitespace was applied to this.

- Finally, `default_output_processor` is TakeFirst() because that's just right :)


## Where does the data go next?

- Data is loaded to a PostgresDB with data types, constraints & rules for INSERT specified.
