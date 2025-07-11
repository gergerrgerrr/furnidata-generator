# furnidata.json and SQL generator

This python script generates:
  - **furnidata.txt** (Your JSON entries for the FLOOR furnitures that you are adding.)
  - **furnidata_wall.txt** (Your JSON entries for the WALL furnitures that you are adding.)
  - **SQL insert statements** for `items_base` and `catalog_items` tables.
  - Floor Items: catalog_items_sql.txt, items_base_sql.txt
  - Wall Items: catalog_items_wall.txt, items_base_wall_sql.txt

  - You can modify the costs of `catalog_items` by configuring the values in **config.txt**.

I made this for people who do not have automated furniture adding in their housekeeping, as I have came across that issue in the past.

Things that you should know:
1. You will need **Python 3.x**
2. Furnitures in **.nitro** to put into the "**/furni**" folder;
   - **/furni/floor_items** for Floor Items.
   - **/furni/wall_items** for Wall Items.
3. Do remember to edit the "**config.txt**"

**config.txt** configuration details:
- **floor_items_path** = Path to the **/furni/floor_items** folder.
- **wall_items_path** = Path to the **/furni/wall_items** folder.
- **page_id** = The page id that you want the furnitures to be under. **Note that this value will not change by itself and you have to modify it whenever necessary.**
- **starting_id** = The starting id for your items_base/furnidata id.
- **starting_cata_id** = Some sprite_ids might not match your cata_ids, so this would solve the issue.

Please note that if you leave these parameters empty, the default values for them would be (cost_credits=0, cost_points=50, points_type=0)
- **cost_credits** = Credit cost of your furniture in `catalog_items`
- **cost_points** = Point cost for furniture in `catalog_items`
- **points_type** = Points type for furniture in `catalog_items` (0 = duckets, 5 = diamonds OR your own currency point value if applicable.)

To run this script:
Open command prompt at the main folder and run ```python generatemain.py``` for Floor Items and ```python generatewall.py``` for Wall Items.
  - The script will read all **.nitro** files in "**/furni/{floor/wall}_items**" and use those furniture names to generate your output texts.
  - Your **starting_id** and **starting_cata_id** would have auto increment so you only have to change the **page_id** in the future.
  - The **/output** folder will be created for you the first time you run the script.

**IMPORTANT NOTE**: Always remember to backup your database files before you run any generated script!
  
