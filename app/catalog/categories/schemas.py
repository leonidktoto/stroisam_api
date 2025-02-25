from pydantic import BaseModel


class SCategories(BaseModel):
    id: int
    parent_id: int | None
    category_name: str
    image_url: str | None

    class ConfigDict:
        from_attributes = True


class SCategoriesWithChldrn(SCategories):
    has_children: bool
