"""
config_manager.py: Quản lý nạp, lưu trữ và thiết lập giá trị mặc định cho cấu hình ứng dụng.
"""

import json
import os
from typing import Any, Dict

DEFAULT_CONFIG: Dict[str, Any] = {
    "app_settings": {
        "window_size": "960x700",
        "max_commits": 50,
        "temp_dir_prefix": "gitdiff_",
        "default_target_dir": "",
        "export_mode": "changed_only",  # "changed_only" hoặc "full_snapshot"
        "generate_patch": True,
        "generate_summary": True,
    },
    "git_settings": {
        "custom_git_path": "",
        "clone_timeout": 300,
        "fetch_all_branches": True,
        "ignore_patterns": [
            ".git",
            "__pycache__",
            "*.pyc",
            ".DS_Store",
            "Thumbs.db",
            "node_modules",
            ".venv",
        ],
    },
    "ui_settings": {
        "theme": "clean_light",
        "font_family": "Segoe UI",
        "font_size": 10,
        "auto_cleanup": True,
        "external_diff_tool": "code",
    },
}


class ConfigManager:
    """Quản lý cấu hình JSON có kèm dự phòng (fallback) an toàn"""

    def __init__(self, config_path: str = "config.json"):
        self.config_path = os.path.abspath(config_path)
        self.config: Dict[str, Any] = self.load_config()

    def load_config(self) -> Dict[str, Any]:
        """Tải cấu hình từ file, kết hợp với các giá trị mặc định nếu thiếu"""
        config = json.loads(json.dumps(DEFAULT_CONFIG))
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    user_cfg = json.load(f)
                    if isinstance(user_cfg, dict):
                        for section, values in user_cfg.items():
                            if section in config and isinstance(values, dict):
                                config[section].update(values)
                            else:
                                config[section] = values
            except Exception as err:
                print(f"Cảnh báo: Không thể nạp {self.config_path} ({err}), sử dụng cấu hình mặc định.")
        else:
            self.save_config(config)
        return config

    def save_config(self, new_config: Dict[str, Any] | None = None) -> bool:
        """Lưu cấu hình ra file JSON"""
        if new_config is not None:
            self.config = new_config
        try:
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump(self.config, f, indent=4, ensure_ascii=False)
            return True
        except Exception as err:
            print(f"Lỗi khi lưu cấu hình: {err}")
            return False

    def get(self, section: str, key: str, fallback: Any = None) -> Any:
        """Lấy giá trị cấu hình một cách an toàn"""
        sec = self.config.get(section, {})
        if isinstance(sec, dict):
            return sec.get(key, fallback)
        return fallback

    def set(self, section: str, key: str, value: Any) -> None:
        """Đặt giá trị cấu hình và tự động lưu"""
        if section not in self.config or not isinstance(self.config[section], dict):
            self.config[section] = {}
        self.config[section][key] = value
        self.save_config()


# Instance singleton dùng chung
_global_config_manager: ConfigManager | None = None


def get_config_manager() -> ConfigManager:
    """Lấy thể hiện ConfigManager duy nhất"""
    global _global_config_manager
    if _global_config_manager is None:
        _global_config_manager = ConfigManager()
    return _global_config_manager
