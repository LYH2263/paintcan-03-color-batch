from pydantic import BaseModel
class SettingsUpdate(BaseModel):
    default_color_code: str | None = None
