import os
import json
import sys
# Config functions from main script
from generatemain import read_config, write_config


def get_wall_filenames(wall_items_path):
    return [
        f for f in os.listdir(wall_items_path)
        if os.path.isfile(os.path.join(wall_items_path, f)) and f.lower().endswith(".nitro")
    ]

def generate_wall_furnidata(wall_items_path, filenames, starting_id, output_folder="output"):
    os.makedirs(output_folder, exist_ok=True)
    output_file = os.path.join(output_folder, "furnidata_wall.txt")

    default_values = {
        "revision": 59005,
        "category": "wallpaper",
        "xdim": 1,
        "ydim": 1,
        "partcolors": {"color":[]},
        "adurl": "",
        "buyout": False,
        "rentofferid": -1,
        "rentbuyout": False,
        "bc": False,
        "excludeddynamic": False,
        "customparams": "",
        "specialtype": 0,
        "furniline": "",
        "environment": "",
        "rare": False,
    }

    current_id = starting_id
    with open(output_file, "a") as w:
        for filename in filenames:
            f_name = os.path.splitext(filename)[0]
            entry = {
                "id": current_id,
                "classname": f_name,
                "name": f_name,
                "description": f"{f_name} desc",
                "offerid": current_id,
                **default_values
            }
            w.write(json.dumps(entry, indent=4) + ",\n")
            current_id += 1

    print(f"Furnidata for Wall Items saved to {output_file}")
    return current_id


def generate_wall_sql(wall_items_path, filenames, starting_id, starting_cata_id, page_id,
                      output_folder="output", cost_credits=0, cost_points=50, points_type=0):
    os.makedirs(output_folder, exist_ok=True)
    items_base_file = os.path.join(output_folder, "items_base_wall_sql.txt")
    catalog_items_file = os.path.join(output_folder, "catalog_items_wall.txt")

    current_id = starting_id
    cata_id = starting_cata_id
    
    with open(items_base_file, "a") as items_file, open(catalog_items_file, "a") as catalog_file:
        for filename in filenames:
            name = os.path.splitext(filename)[0]

            items_query = (
                "INSERT INTO `items_base` "
                "(`id`, `sprite_id`, `item_name`, `public_name`, `width`, `length`, `stack_height`, "
                "`allow_stack`, `allow_sit`, `allow_lay`, `allow_walk`, `allow_gift`, `allow_trade`, "
                "`allow_recycle`, `allow_marketplace_sell`, `allow_inventory_stack`, `type`, "
                "`interaction_type`, `interaction_modes_count`, `vending_ids`, `multiheight`, "
                "`customparams`, `effect_id_male`, effect_id_female`, `clothing_on_walk`, `page_id`, `rare`) VALUES "
                f"('{current_id}', '{current_id}', '{name}', '{name}', 1, 1, 1.00, '0', '0', '0', '0', '1', '1', "
                "'0', '0', '1', 'i', 'default', 1, '', '', '', 0, 0, '', NULL, '0');"
            )

            catalog_query = (
                "INSERT INTO `catalog_items` "
                "(`id`, `item_ids`, `page_id`, `offer_id`, `song_id`, `order_number`, `catalog_name`, "
                "`cost_credits`, `cost_points`, `points_type`, `amount`, `limited_sells`, `limited_stack`, "
                "`extradata`, `badge`, `have_offer`, `club_only`, `rate`) VALUES "
                f"('{cata_id}', '{current_id}', '{page_id}', '{current_id}', 0, 99, '{name}', "
                f"{cost_credits}, {cost_points}, {points_type}, 1, 0, 0, '', NULL, '1', '0', NULL);"
            )

            items_file.write(items_query + "\n")
            catalog_file.write(catalog_query + "\n")
            current_id += 1
            cata_id += 1

    print(f" Wall Items SQL saved to {items_base_file} and {catalog_items_file}!")
    return current_id, cata_id

def main():
    config_file = "config.txt"
    output_folder = "output"

    # Read config but override floor_items_path with wall_items_path
    (starting_id, page_id, starting_cata_id,
     floor_items_path, cost_credits, cost_points, points_type) = read_config (config_file)
    
    # Read wall_items_path directly
    wall_items_path = None
    try:
        with open(config_file, "r") as f:
            for line in f:
                if line.strip().startswith("wall_items_path"):
                    _, val = line.strip().split("=", 1)
                    wall_items_path = val.strip()
                    break
    except FileNotFoundError:
        pass

    if not wall_items_path or not os.path.exists(wall_items_path):
        print(f"Error: Your wall_items_path '{wall_items_path}' is invalid or does not exist.")
        sys.exit(1)

    filenames = get_wall_filenames(wall_items_path)

    if not filenames:
        print(f"Error: There are no .nitro files found in '{wall_items_path}'.")
        sys.exit(1)

    print("Generating Wall Furnidata...")
    end_id_furnidata = generate_wall_furnidata(wall_items_path, filenames, starting_id, output_folder)

    print("Generating Wall Items SQL...")
    end_id_sql, end_cata_id_sql = generate_wall_sql(
        wall_items_path, filenames, starting_id, starting_cata_id, page_id, output_folder,
        cost_credits, cost_points, points_type
    )

    # Update new ids in config.txt
    final_starting_id = max(end_id_furnidata, end_id_sql)
    write_config(
        final_starting_id, page_id, end_cata_id_sql,
        floor_items_path=floor_items_path, # Keep floor item pat
        cost_credits=cost_credits, cost_points=cost_points, points_type=points_type,
        filename=config_file
    )

    print("Wall Item Data and SQL Generated!")

if __name__ == "__main__":
    main()