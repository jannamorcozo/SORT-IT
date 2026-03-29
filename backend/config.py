from functools import lru_cache

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "SORT-IT Backend"

    gcp_project_id: str
    gcs_model_bucket: str

    model_stage1_path: str
    model_stage2_path: str

    model_stage3_plastic_path: str
    model_stage3_glass_path: str
    model_stage3_metal_path: str
    model_stage3_paper_path: str
    model_stage3_residual_path: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    """
    Cached settings so env is only read once per process.
    """
    return Settings()