"""
Config Manager - Handle skill configuration
"""

import os
import json
from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict, field


@dataclass
class OutputConfig:
    base_path: str = "./output"
    subdirs: Dict[str, str] = field(default_factory=lambda: {
        "pdf": "pdf",
        "pptx": "pptx",
        "docx": "word",
        "xlsx": "excel",
        "html": "html",
    })


@dataclass
class TemplateConfig:
    path: str = "./templates"
    builtin: List[str] = field(default_factory=lambda: [
        "whitepaper",
        "catalog",
        "portfolio",
        "infographic",
        "flyer",
        "reportlab_advanced",
        "weasyprint_premium",
        "matplotlib_datareport",
        "fpdf2_modern",
        "proposal_template",
        "business_modern",
        "creative_gradient",
        "technical_dark",
        "minimalist",
        "corporate_formal",
        "advanced_business",
        "proposal",
        "manual",
        "resume",
        "excel_dashboard",
        "revealjs_presentation",
    ])


@dataclass
class FontConfig:
    primary: str = "Noto Sans JP"
    secondary: str = "Inter"
    monospace: str = "Consolas"


@dataclass
class DefaultsConfig:
    language: str = "ja"
    color_scheme: str = "business"
    font: FontConfig = field(default_factory=FontConfig)
    page_size: str = "A4"


@dataclass
class EngineConfig:
    pdf: str = "playwright"
    pptx: str = "python-pptx"
    docx: str = "python-docx"
    xlsx: str = "xlsxwriter"
    html: str = "revealjs"


@dataclass
class PreflightConfig:
    enabled: bool = True
    checks: List[str] = field(default_factory=lambda: ["fonts", "images", "colors"])


@dataclass
class SkillConfig:
    version: str = "1.0.0"
    output: OutputConfig = field(default_factory=OutputConfig)
    templates: TemplateConfig = field(default_factory=TemplateConfig)
    defaults: DefaultsConfig = field(default_factory=DefaultsConfig)
    engines: EngineConfig = field(default_factory=EngineConfig)
    preflight: PreflightConfig = field(default_factory=PreflightConfig)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SkillConfig":
        # Handle nested dataclasses
        output = OutputConfig(**data.get("output", {}))
        templates = TemplateConfig(**data.get("templates", {}))

        defaults_data = data.get("defaults", {})
        font = FontConfig(**defaults_data.get("font", {}))
        defaults = DefaultsConfig(
            language=defaults_data.get("language", "ja"),
            color_scheme=defaults_data.get("color_scheme", "business"),
            font=font,
            page_size=defaults_data.get("page_size", "A4"),
        )

        engines = EngineConfig(**data.get("engines", {}))
        preflight = PreflightConfig(**data.get("preflight", {}))

        return cls(
            version=data.get("version", "1.0.0"),
            output=output,
            templates=templates,
            defaults=defaults,
            engines=engines,
            preflight=preflight,
        )


class ConfigManager:
    """Manage skill configuration"""

    CONFIG_FILE = "doc-studio.config.json"

    def __init__(self, config_path: str = None):
        self.config_dir = Path(config_path) if config_path else self._get_config_dir()
        self.config_file = self.config_dir / self.CONFIG_FILE
        self._config: Optional[SkillConfig] = None

    def _get_config_dir(self) -> Path:
        """Get configuration directory based on platform"""
        # Check for project-local config first
        local_config = Path.cwd() / ".doc-studio"
        if local_config.exists():
            return local_config

        # Otherwise use user config
        if os.name == "nt":  # Windows
            config_dir = Path(os.environ.get("APPDATA", "~")) / "doc-studio"
        else:  # Unix/Mac
            config_dir = Path.home() / ".config" / "doc-studio"

        return config_dir

    def load(self) -> SkillConfig:
        """Load configuration from file"""
        if self._config is not None:
            return self._config

        if self.config_file.exists():
            try:
                data = json.loads(self.config_file.read_text(encoding="utf-8"))
                self._config = SkillConfig.from_dict(data)
            except (json.JSONDecodeError, KeyError) as e:
                print(f"Warning: Failed to load config: {e}")
                self._config = SkillConfig()
        else:
            self._config = SkillConfig()

        return self._config

    def save(self, config: SkillConfig = None):
        """Save configuration to file"""
        if config is None:
            config = self._config or SkillConfig()

        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.config_file.write_text(
            json.dumps(config.to_dict(), indent=2, ensure_ascii=False),
            encoding="utf-8"
        )
        self._config = config

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by key (dot notation)"""
        config = self.load()
        keys = key.split(".")
        value = config.to_dict()

        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default

        return value

    def set(self, key: str, value: Any):
        """Set configuration value by key (dot notation)"""
        config = self.load()
        config_dict = config.to_dict()

        keys = key.split(".")
        current = config_dict

        for k in keys[:-1]:
            if k not in current:
                current[k] = {}
            current = current[k]

        current[keys[-1]] = value

        # Reconstruct config
        self._config = SkillConfig.from_dict(config_dict)
        self.save()

    def reset(self):
        """Reset configuration to defaults"""
        self._config = SkillConfig()
        self.save()

    def show(self) -> str:
        """Show current configuration as formatted string"""
        config = self.load()
        return json.dumps(config.to_dict(), indent=2, ensure_ascii=False)

    def get_output_path(self, format: str) -> Path:
        """Get output path for a format"""
        config = self.load()
        base = Path(config.output.base_path)
        subdir = config.output.subdirs.get(format, format)
        return base / subdir

    def get_template_path(self) -> Path:
        """Get templates path"""
        config = self.load()
        return Path(config.templates.path)

    def get_default_engine(self, format: str) -> str:
        """Get default engine for a format"""
        config = self.load()
        return getattr(config.engines, format, "auto")

    def is_preflight_enabled(self) -> bool:
        """Check if preflight is enabled"""
        config = self.load()
        return config.preflight.enabled

    def get_preflight_checks(self) -> List[str]:
        """Get enabled preflight checks"""
        config = self.load()
        return config.preflight.checks

    def create_project_config(self, project_path: str = "."):
        """Create project-local configuration"""
        project_dir = Path(project_path) / ".doc-studio"
        project_dir.mkdir(exist_ok=True)

        config_file = project_dir / self.CONFIG_FILE
        default_config = SkillConfig()

        config_file.write_text(
            json.dumps(default_config.to_dict(), indent=2, ensure_ascii=False),
            encoding="utf-8"
        )

        return str(project_dir)

    def validate(self) -> List[str]:
        """Validate current configuration"""
        errors = []
        config = self.load()

        # Check paths exist
        output_path = Path(config.output.base_path)
        if not output_path.exists():
            errors.append(f"Output path does not exist: {output_path}")

        template_path = Path(config.templates.path)
        if not template_path.exists():
            errors.append(f"Template path does not exist: {template_path}")

        # Check language
        valid_languages = ["ja", "en", "zh", "ko"]
        if config.defaults.language not in valid_languages:
            errors.append(f"Invalid language: {config.defaults.language}")

        # Check color scheme
        valid_schemes = ["business", "creative", "dark", "minimal", "formal"]
        if config.defaults.color_scheme not in valid_schemes:
            errors.append(f"Invalid color scheme: {config.defaults.color_scheme}")

        return errors
