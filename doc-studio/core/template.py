"""
Template Manager - Handle document templates
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict

from core.generator import DocumentGenerator, DocumentFormat


@dataclass
class TemplateInfo:
    """Template metadata"""
    name: str
    display_name: str
    description: str
    formats: List[str]
    engines: List[str]
    color_schemes: List[str]
    preview_image: Optional[str] = None
    tags: List[str] = None
    author: str = "Doc Studio"
    version: str = "1.0.0"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class TemplateManager:
    """Manage document templates"""

    def __init__(self, templates_path: str = None):
        default_templates_path = Path(__file__).resolve().parents[1] / "templates"
        self.templates_path = Path(templates_path).resolve() if templates_path else default_templates_path
        self.builtin_templates: Dict[str, TemplateInfo] = self._load_builtin_templates()
        self.custom_templates: Dict[str, TemplateInfo] = {}
        self._load_custom_templates()

    def _read_docstring_summary(self, file_path: Path) -> tuple[str, str]:
        """Extract (display_name, description) from the top docstring if present."""
        try:
            import ast

            text = file_path.read_text(encoding="utf-8", errors="ignore")
            module = ast.parse(text)
            doc = ast.get_docstring(module) or ""
        except Exception:
            return (file_path.stem, "")

        lines = [ln.strip() for ln in doc.splitlines() if ln.strip()]
        if not lines:
            return (file_path.stem, "")

        display_name = lines[0]
        description = "\n".join(lines[1:]).strip()
        return (display_name, description)

    def _load_builtin_templates(self) -> Dict[str, TemplateInfo]:
        """Load built-in templates shipped with the skill."""
        templates: Dict[str, TemplateInfo] = {}

        # Use canonical mapping so CLI names stay stable.
        for fmt, mapping in DocumentGenerator.TEMPLATE_SCRIPTS.items():
            for template_name, script_name in mapping.items():
                script_path = self.templates_path / script_name
                display_name, description = self._read_docstring_summary(script_path)
                templates[template_name] = TemplateInfo(
                    name=template_name,
                    display_name=display_name or template_name,
                    description=description or "",
                    formats=[fmt.value],
                    engines=[],
                    color_schemes=[],
                    tags=["builtin"],
                )

        return templates

    def _load_custom_templates(self):
        """Load custom templates from templates directory"""
        if not self.templates_path.exists():
            return

        for template_dir in self.templates_path.iterdir():
            if template_dir.is_dir():
                manifest = template_dir / "manifest.json"
                if manifest.exists():
                    try:
                        data = json.loads(manifest.read_text(encoding="utf-8"))
                        info = TemplateInfo(**data)
                        self.custom_templates[info.name] = info
                    except Exception:
                        pass

    def list_templates(
        self,
        format_filter: Optional[str] = None,
        tag_filter: Optional[str] = None
    ) -> List[TemplateInfo]:
        """
        List available templates

        Args:
            format_filter: Filter by format
            tag_filter: Filter by tag

        Returns:
            List of template info
        """
        all_templates = {**self.builtin_templates, **self.custom_templates}
        results = list(all_templates.values())

        if format_filter:
            results = [t for t in results if format_filter in t.formats]

        if tag_filter:
            results = [t for t in results if tag_filter in (t.tags or [])]

        return results

    def get_template(self, name: str) -> Optional[TemplateInfo]:
        """Get template by name"""
        if name in self.builtin_templates:
            return self.builtin_templates[name]
        return self.custom_templates.get(name)

    def get_template_path(self, name: str, format: str) -> Optional[Path]:
        """Get template file path"""
        template_dir = self.templates_path / name
        if not template_dir.exists():
            return None

        # Look for template file
        extensions = {
            "pdf": ".html",
            "pptx": ".py",
            "docx": ".py",
            "xlsx": ".py",
            "html": ".html",
        }

        ext = extensions.get(format, ".py")
        template_file = template_dir / f"template{ext}"

        if template_file.exists():
            return template_file

        # Try alternative names
        alternatives = [
            template_dir / f"{name}{ext}",
            template_dir / f"generate{ext}",
        ]

        for alt in alternatives:
            if alt.exists():
                return alt

        return None

    def create_template(
        self,
        name: str,
        display_name: str,
        description: str,
        base_template: Optional[str] = None
    ) -> Path:
        """
        Create a new custom template

        Args:
            name: Template identifier
            display_name: Human-readable name
            description: Template description
            base_template: Optional base template to copy

        Returns:
            Path to created template directory
        """
        template_dir = self.templates_path / name
        template_dir.mkdir(parents=True, exist_ok=True)

        # Create manifest
        manifest = {
            "name": name,
            "display_name": display_name,
            "description": description,
            "formats": ["pdf", "pptx", "docx"],
            "engines": ["playwright", "python-pptx", "python-docx"],
            "color_schemes": ["default"],
            "tags": ["custom"],
            "author": "User",
            "version": "1.0.0",
        }

        manifest_file = template_dir / "manifest.json"
        manifest_file.write_text(
            json.dumps(manifest, indent=2, ensure_ascii=False),
            encoding="utf-8"
        )

        # Copy from base template if specified
        if base_template and base_template in self.BUILTIN_TEMPLATES:
            self._copy_base_template(base_template, template_dir)

        return template_dir

    def _copy_base_template(self, base_name: str, target_dir: Path):
        """Copy base template files"""
        base_dir = self.templates_path / base_name
        if base_dir.exists():
            import shutil
            for item in base_dir.iterdir():
                if item.is_file():
                    shutil.copy2(item, target_dir / item.name)

    def delete_template(self, name: str) -> bool:
        """Delete a custom template"""
        if name in self.builtin_templates:
            raise ValueError(f"Cannot delete built-in template: {name}")

        if name in self.custom_templates:
            import shutil
            template_dir = self.templates_path / name
            if template_dir.exists():
                shutil.rmtree(template_dir)
            del self.custom_templates[name]
            return True

        return False

    def get_template_data_schema(self, name: str) -> Dict[str, Any]:
        """Get expected data schema for template"""
        template = self.get_template(name)
        if not template:
            return {}

        # Default schema based on template type
        schemas = {
            "business": {
                "title": "string",
                "subtitle": "string",
                "company": "string",
                "date": "string",
                "sections": "array",
                "metrics": "array",
            },
            "creative": {
                "title": "string",
                "tagline": "string",
                "slides": "array",
            },
            "technical": {
                "title": "string",
                "architecture": "object",
                "components": "array",
                "code_snippets": "array",
            },
            "data-report": {
                "title": "string",
                "charts": "array",
                "tables": "array",
                "kpis": "array",
            },
        }

        return schemas.get(name, {"title": "string", "content": "string"})

    def export_template(self, name: str, output_path: str) -> str:
        """Export template as zip"""
        import zipfile

        template_dir = self.templates_path / name
        if not template_dir.exists():
            raise ValueError(f"Template not found: {name}")

        output_file = Path(output_path) / f"{name}-template.zip"

        with zipfile.ZipFile(output_file, "w", zipfile.ZIP_DEFLATED) as zf:
            for file in template_dir.rglob("*"):
                if file.is_file():
                    zf.write(file, file.relative_to(template_dir))

        return str(output_file)

    def import_template(self, zip_path: str) -> str:
        """Import template from zip"""
        import zipfile

        zip_file = Path(zip_path)
        if not zip_file.exists():
            raise ValueError(f"Zip file not found: {zip_path}")

        # Extract
        extract_dir = self.templates_path / zip_file.stem
        with zipfile.ZipFile(zip_file, "r") as zf:
            zf.extractall(extract_dir)

        # Reload custom templates
        self._load_custom_templates()

        return str(extract_dir)
