"""
Document Generator - Core engine for all document formats
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from enum import Enum


class DocumentFormat(Enum):
    PDF = "pdf"
    PPTX = "pptx"
    DOCX = "docx"
    XLSX = "xlsx"
    HTML = "html"


class EngineType(Enum):
    PLAYWRIGHT = "playwright"
    REPORTLAB = "reportlab"
    WEASYPRINT = "weasyprint"
    FPDF2 = "fpdf2"
    MATPLOTLIB = "matplotlib"
    PYTHON_PPTX = "python-pptx"
    PYTHON_DOCX = "python-docx"
    DOCXTPL = "docxtpl"
    XLSXWRITER = "xlsxwriter"
    REVEALJS = "revealjs"


@dataclass
class GenerationConfig:
    """Configuration for document generation"""
    format: DocumentFormat
    template: str
    output_path: str
    data: Dict[str, Any]
    engine: Optional[EngineType] = None
    language: str = "ja"
    color_scheme: str = "business"
    page_size: str = "A4"


class DocumentGenerator:
    """Main document generator class"""

    # Canonical template mapping (format -> template -> script filename in templates/)
    # NOTE: Keep this list aligned with references/templates.md
    TEMPLATE_SCRIPTS: Dict[DocumentFormat, Dict[str, str]] = {
        DocumentFormat.PDF: {
            "whitepaper": "pdf_whitepaper.py",
            "catalog": "pdf_catalog.py",
            "portfolio": "pdf_portfolio.py",
            "infographic": "pdf_infographic.py",
            "flyer": "pdf_flyer.py",
            "reportlab_advanced": "advanced_reportlab.py",
            "weasyprint_premium": "advanced_weasyprint.py",
            "matplotlib_datareport": "advanced_matplotlib.py",
            "fpdf2_modern": "advanced_fpdf2.py",
            "proposal_template": "advanced_docxtpl.py",
        },
        DocumentFormat.PPTX: {
            "business_modern": "pptx_business_modern.py",
            "creative_gradient": "pptx_creative_gradient.py",
            "technical_dark": "pptx_technical_dark.py",
            "minimalist": "pptx_minimalist.py",
            "corporate_formal": "pptx_corporate_formal.py",
            "advanced_business": "pptx_advanced_business.py",
        },
        DocumentFormat.DOCX: {
            "proposal": "docx_proposal.py",
            "manual": "docx_manual.py",
            "resume": "docx_resume.py",
        },
        DocumentFormat.XLSX: {
            "excel_dashboard": "advanced_xlsxwriter.py",
        },
        DocumentFormat.HTML: {
            "revealjs_presentation": "html_revealjs_presentation.py",
        },
    }

    def __init__(self, skill_root: str | None = None):
        # templates/ はスキルに同梱される前提。cwdではなく“スキルの場所”を基準に探す。
        default_skill_root = Path(__file__).resolve().parents[1]
        self.skill_root = Path(skill_root).resolve() if skill_root else default_skill_root
        self.templates_path = self.skill_root / "templates"

    def generate(self, config: GenerationConfig) -> str:
        """
        Generate document based on configuration

        Args:
            config: GenerationConfig instance

        Returns:
            Path to generated file
        """
        # Validate inputs
        self._validate_config(config)

        # Prepare data file
        data_file = self._prepare_data_file(config)

        # Execute generation script
        output_file = self._execute_generation(config, data_file)

        # Cleanup
        if data_file.exists():
            data_file.unlink()

        return str(output_file)

    def _validate_config(self, config: GenerationConfig):
        """Validate generation configuration"""
        if config.format not in DocumentFormat:
            raise ValueError(f"Unsupported format: {config.format}")

        if not config.output_path:
            raise ValueError("Output path is required")

        # Validate template exists (resolved to a file under templates/)
        template_path = self._resolve_template_path(config)
        if not template_path.exists():
            raise ValueError(f"Template not found: {config.template} ({template_path})")

    def _prepare_data_file(self, config: GenerationConfig) -> Path:
        """Prepare temporary data file for generation"""
        import tempfile

        data_file = Path(tempfile.gettempdir()) / f"doc_studio_data_{os.getpid()}.json"
        data_file.write_text(json.dumps(config.data, ensure_ascii=False, indent=2), encoding="utf-8")
        return data_file

    def _resolve_template_path(self, config: GenerationConfig) -> Path:
        """Resolve template file path under templates/."""
        # 1) Allow passing a concrete filename (with or without extension)
        candidate_names: list[str] = []
        raw = config.template.strip()

        # Path-like: treat as relative to templates/ unless absolute.
        if any(sep in raw for sep in ("/", "\\", os.sep)):
            p = Path(raw)
            return p if p.is_absolute() else (self.templates_path / p)

        if raw.endswith(".py") or raw.endswith(".html"):
            candidate_names.append(raw)
        else:
            candidate_names.append(f"{raw}.py")
            candidate_names.append(f"{raw}.html")

        for name in candidate_names:
            p = self.templates_path / name
            if p.exists():
                return p

        # 2) Canonical mapping (format + short template name)
        mapping = self.TEMPLATE_SCRIPTS.get(config.format, {})
        if raw in mapping:
            return self.templates_path / mapping[raw]

        # 3) Convenience: accept "pdf_whitepaper" style
        prefixed_py = self.templates_path / f"{config.format.value}_{raw}.py"
        if prefixed_py.exists():
            return prefixed_py

        return self.templates_path / f"{raw}.py"

    def _execute_generation(self, config: GenerationConfig, data_file: Path) -> Path:
        """Execute template script and return output file path."""
        script_path = self._resolve_template_path(config)
        if not script_path.exists():
            raise ValueError(f"Template script not found: {script_path}")

        output_file = Path(config.output_path)
        if not output_file.suffix:
            suffix_map = {
                DocumentFormat.PDF: ".pdf",
                DocumentFormat.PPTX: ".pptx",
                DocumentFormat.DOCX: ".docx",
                DocumentFormat.XLSX: ".xlsx",
                DocumentFormat.HTML: ".html",
            }
            output_file = output_file.with_suffix(suffix_map.get(config.format, ""))

        output_file.parent.mkdir(parents=True, exist_ok=True)

        # Build command (all templates accept these common args)
        cmd = [
            sys.executable,
            str(script_path),
            "--output", str(output_file),
            "--data-file", str(data_file),
        ]

        # Execute
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True,
                encoding="utf-8",
                cwd=str(Path.cwd()),
            )
        except subprocess.CalledProcessError as e:
            stderr = (e.stderr or "").strip()
            stdout = (e.stdout or "").strip()
            msg = "Generation failed"
            if stderr:
                msg += f": {stderr}"
            elif stdout:
                msg += f": {stdout}"
            raise RuntimeError(msg) from e

        if not output_file.exists():
            debug = (result.stdout or "").strip() or "(no stdout)"
            raise RuntimeError(f"Template ran but output not found: {output_file}\n{debug}")

        return output_file

    def get_supported_formats(self) -> List[str]:
        """Get list of supported formats"""
        return [fmt.value for fmt in DocumentFormat]

    def get_supported_engines(self, format: DocumentFormat) -> List[str]:
        """Get list of supported engines for a format"""
        engines = self.ENGINE_PRIORITY.get(format, [])
        return [eng.value for eng in engines]

    def quick_generate(
        self,
        format: str,
        template: str,
        output: str,
        data: Dict[str, Any] = None,
        engine: str = None
    ) -> str:
        """Quick generation with simplified interface"""
        config = GenerationConfig(
            format=DocumentFormat(format),
            template=template,
            output_path=output,
            data=data or {},
            engine=EngineType(engine) if engine else None,
        )
        return self.generate(config)


class BatchGenerator:
    """Batch document generation"""

    def __init__(self, generator: DocumentGenerator):
        self.generator = generator

    def generate_multiple(
        self,
        configs: List[GenerationConfig],
        parallel: bool = False
    ) -> List[str]:
        """Generate multiple documents"""
        if parallel:
            return self._generate_parallel(configs)
        else:
            return self._generate_sequential(configs)

    def _generate_sequential(self, configs: List[GenerationConfig]) -> List[str]:
        """Generate documents sequentially"""
        results = []
        for config in configs:
            try:
                path = self.generator.generate(config)
                results.append(path)
            except Exception as e:
                results.append(f"ERROR: {e}")
        return results

    def _generate_parallel(self, configs: List[GenerationConfig]) -> List[str]:
        """Generate documents in parallel"""
        from concurrent.futures import ThreadPoolExecutor, as_completed

        results = [None] * len(configs)

        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = {
                executor.submit(self.generator.generate, config): i
                for i, config in enumerate(configs)
            }

            for future in as_completed(futures):
                idx = futures[future]
                try:
                    results[idx] = future.result()
                except Exception as e:
                    results[idx] = f"ERROR: {e}"

        return results
