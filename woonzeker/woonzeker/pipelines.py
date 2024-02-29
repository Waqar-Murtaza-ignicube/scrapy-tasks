"Modules are defined here"
from itemadapter import ItemAdapter


class WoonzekerPipeline:
    """pipeline class to clean the data"""
    def process_item(self, item, spider):
        """pipeline method to use an item adapter"""
        adapter = ItemAdapter(item)

        surface_item = adapter.get("surface")
        adapter["surface"] = f"{surface_item} m\u00B2"

        description = adapter["description"]
        adapter["description"] = description.replace("\n", "")

        photo_item = adapter.get("photo")
        adapter["photo"] = photo_item.split('url(')[-1].split(')')[0]

        bedroom_item = adapter.get("bedrooms")
        adapter["bedrooms"] = int(bedroom_item)

        room_item = adapter.get("rooms")
        adapter["rooms"] = int(room_item)

        furniture_item = adapter.get("furniture")
        if furniture_item == 'gestoffeerd':
            adapter["furniture"] = "upholstered"
        elif furniture_item == 'gemeubileerd':
            adapter["furniture"] = "furnished"
        elif furniture_item == 'gedeeltelijk gestoffeerd':
            adapter["furniture"] = "partially upholstered"
        elif furniture_item == 'casco':
            adapter["furniture"] = "airframe"

        price_item = adapter.get("price")
        stripped = price_item.replace("€", "").replace(".", "").replace(",",".").strip()
        adapter["price"] = float(stripped)

        longitude_item = adapter.get("longitude")
        latitude_item = adapter.get("latitude")
        if longitude_item == "cQ":
            adapter["longitude"] = None

        latitude_item = adapter.get("latitude")
        if latitude_item == "cQ":
            adapter["latitude"] = None

        return item
