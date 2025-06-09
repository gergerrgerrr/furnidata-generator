# furnidata.json and SQL generator

This python script generates:
  - furnidata.txt (Your JSON entries for the furnitures that you are adding.)
  - SQL insert statements for `items_base` and `catalog_items` tables in catalog_items_sql.txt and items_base_sql.txt respectively.
  - The default costs for the furniture in the catalogue would be 50 duckets, you may change it to suit your needs.

I made this for people who do not have automated furniture adding in their housekeeping, as I have came across that issue in the past.

Requirements:
1. You will need Python 3.x
2. Furnitures in .nitro to put into the "/furni" folder
3. Do remember to edit the "config.txt"
   starting_id = The starting id for your items_base/furnidata id
   page_id = The page id that you want the furnitures to be under **Note that this value will not change by itself and you have to modify it whenever necessary.
   starting_cata_id = Some sprite_ids might not match your cata_ids, so this would solve the issue

To run this script:
Open command prompt at the main folder and run ```python generateall.py```
  - The script will read all .nitro files in "/furni" and use those furniture names to generate your output texts.
  - Your starting_id and starting_cata_id would have auto increment so you only have to change the page_id in the future.
  - The /output folder will be created for you the first time you run the script.
  
