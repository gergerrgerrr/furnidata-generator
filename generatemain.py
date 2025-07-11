import os
import json
import sys


def read_config(filename="config.txt"):
    starting_id = 1
    page_id = 1
    starting_cata_id = 1
    floor_items_path = ""
    cost_credits = None
    cost_points = None
    points_type = None

    try:
        with open(filename, "r") as f:
            for line in f:
                line = line.strip()
                # Ignoring the comments which starts with '#'
                if not line or line.startswith("#"):
                    continue

                key_value = line.split("=", 1)
                if len(key_value) != 2:
                    continue

                key = key_value[0].strip()
                value = key_value[1].strip()

                if key == "starting_id" and value:
                    starting_id = int(value)
                elif key == "page_id" and value:
                    page_id = int(value)
                elif key == "starting_cata_id" and value:
                    starting_cata_id = int(value)
                elif key == "floor_items_path" and value:
                    floor_items_path = value
                elif key == "cost_credits":
                    if value:
                        cost_credits = int(value)
                elif key == "cost_points":
                    if value:
                        cost_points = int(value)
                elif key == "points_type":
                    if value:
                        points_type = int(value)


    except (FileNotFoundError, ValueError):
        pass

    # Alert to user that default costs have been used
    if cost_credits is None:
        cost_credits = 0
        print("[ALERT] As you did not specify 'cost_credits', default value (0) is used.")

    if cost_points is None:
        cost_points = 50
        print("[ALERT] As you did not specify 'cost_points', default value (50) is used.")

    if points_type is None:
        points_type = 0
        print("[ALERT] As you did not specify 'points_type', default value (0) is used.")

    return starting_id, page_id, starting_cata_id, floor_items_path, cost_credits, cost_points, points_type


def write_config(starting_id, page_id, starting_cata_id, floor_items_path="", cost_credits=0,
                  cost_points=50, points_type=0, filename="config.txt"):
    lines = []
    try:
        with open(filename, "r") as f:
            lines = f.readlines()
    except FileNotFoundError:
        pass

    keys_found = {
        "starting_id": False,
        "page_id": False,
        "starting_cata_id": False,
        "floor_items_path": False,
        "cost_credits": False,
        "cost_points": False,
        "points_type": False,
    }

    for i, line in enumerate(lines):
        if line.strip().startswith("starting_id"):
            lines[i] = f"starting_id = {starting_id}\n"
            keys_found["starting_id"] = True
        elif line.strip().startswith("page_id"):
            lines[i] = f"page_id = {page_id}\n"
            keys_found["page_id"] = True
        elif line.strip().startswith("starting_cata_id"):
            lines[i] = f"starting_cata_id = {starting_cata_id}\n"
            keys_found["starting_cata_id"] = True
        elif line.strip().startswith("floor_items_path"):
            lines[i] = f"floor_items_path = {floor_items_path}\n"
            keys_found["floor_items_path"] = True
        elif line.strip().startswith("cost_credits"):
            lines[i] = f"cost_credits = {cost_credits}\n"
            keys_found["cost_credits"] = True
        elif line.strip().startswith("cost_points"):
            lines[i] = f"cost_points = {cost_points}\n"
            keys_found["cost_points"] = True
        elif line.strip().startswith("points_type"):
            lines[i] = f"points_type = {points_type}\n"
            keys_found["points_type"] = True

    if not keys_found["starting_id"]:
        lines.append(f"starting_id = {starting_id}\n")
    if not keys_found["page_id"]:
        lines.append(f"page_id = {page_id}\n")
    if not keys_found["starting_cata_id"]:
        lines.append(f"starting_cata_id = {starting_cata_id}\n")
    if not keys_found["floor_items_path"] and floor_items_path:
        lines.append(f"floor_items_path = {floor_items_path}\n")
    if not keys_found["cost_credits"]:
        lines.append(f"cost_credits = {cost_credits}\n")
    if not keys_found["cost_points"]:
        lines.append(f"cost_points = {cost_points}\n")
    if not keys_found["points_type"]:
        lines.append(f"points_type = {points_type}\n")

    with open(filename, "w") as f:
        f.writelines(lines)


def get_nitro_filenames(floor_items_path):
    return [
        f for f in os.listdir(floor_items_path)
        if os.path.isfile(os.path.join(floor_items_path, f)) and f.lower().endswith(".nitro")
    ]


def generate_furnidata(floor_items_path, filenames, starting_id, output_folder="output"):
    os.makedirs(output_folder, exist_ok=True)
    output_file = os.path.join(output_folder, "furnidata.txt")

    default_values = {
        "revision": 59005,
        "category": "unknown",
        "defaultdir": 0,
        "xdim": 1,
        "ydim": 1,
        "partcolors": {"color": []},
        "adurl": "",
        "buyout": False,
        "rentofferid": -1,
        "rentbuyout": False,
        "bc": False,
        "excludeddynamic": False,
        "customparams": "",
        "specialtype": 0,
        "canstandon": False,
        "cansiton": False,
        "canlayon": False,
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

    print(f"Furnidata saved to {output_file}")
    return current_id


def generate_sql(floor_items_path, filenames, starting_id, starting_cata_id,
                 page_id, output_folder="output", cost_credits=0,
                 cost_points=50, points_type=0):
    os.makedirs(output_folder, exist_ok=True)
    items_base_file = os.path.join(output_folder, "items_base_sql.txt")
    catalog_items_file = os.path.join(output_folder, "catalog_items_sql.txt")

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
                "`customparams`, `effect_id_male`, `effect_id_female`, `clothing_on_walk`, `page_id`, `rare`) VALUES "
                f"('{current_id}', '{current_id}', '{name}', '{name}', 1, 1, 1.00, '0', '0', '0', '0', '1', '1', "
                "'0', '0', '1', 's', 'default', 1, '', '', '', 0, 0, '', NULL, '0');"
            )

            # Default cost = 50 duckets
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

    print(f"SQL saved to {items_base_file} and {catalog_items_file}")
    return current_id, cata_id


def main():
    config_file = "config.txt"
    output_folder = "output"

    (
        starting_id, page_id, starting_cata_id,
        floor_items_path, cost_credits, cost_points, points_type
    ) = read_config(config_file)
    
    # Path invalid
    if not floor_items_path or not os.path.exists(floor_items_path):
        print(f"Error: Your floor_items_path '{floor_items_path}' is invalid or does not exist.")
        sys.exit(1)
    
    filenames = get_nitro_filenames(floor_items_path)

    # Path does not contain any .nitro files
    if not filenames:
        print(f"Error: There are no .nitro files found in '{floor_items_path}'.")
        sys.exit(1)

    print("Generating furnidata...")
    end_id_furnidata = generate_furnidata(floor_items_path, filenames, starting_id, output_folder)

    print("Generating SQL...")
    end_id_sql, end_cata_id_sql = generate_sql(
        floor_items_path, filenames, starting_id, starting_cata_id, page_id, output_folder,
        cost_credits, cost_points, points_type
    )

    # Update ids
    final_starting_id = max(end_id_furnidata, end_id_sql)
    write_config(
        final_starting_id, page_id, end_cata_id_sql,
        floor_items_path, cost_credits, cost_points, points_type, config_file
    )
    
    print("Completed!")


if __name__ == "__main__":
    main()

