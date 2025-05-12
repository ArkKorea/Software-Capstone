import enum

class FavoriteType(str, enum.Enum):
    food = "food"
    bundle = "bundle"
    supplier = "supplier"