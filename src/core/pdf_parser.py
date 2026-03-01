"""PDF Parser for academic papers."""
import re
from dataclasses import dataclass
from typing import List, Optional, Tuple, Dict, Any
from pathlib import Path


@dataclass
class PDFElement:
    """Represents a parsed PDF element."""
    page_num: int
    element_type: str  # text, heading, figure, table, caption
    content: str
    original_content: str = ""  # For translated content
    translated_content: str = ""
    bbox: Optional[Tuple[float, float, float, float]] = None
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}
        if not self.original_content:
            self.original_content = self.content


class PDFParser:
    """Parser for academic PDF papers."""
    
    # Patterns for academic paper elements
    FIGURE_PATTERN = re.compile(r'^(?:Figure|Fig\.?)\s*(\d+[a-zA-Z]?)', re.IGNORECASE)
    TABLE_PATTERN = re.compile(r'^(?:Table)\s*(\d+[a-zA-Z]?)', re.IGNORECASE)
    REFERENCES_HEADING = re.compile(r'^(?:References|Bibliography|Works Cited)', re.IGNORECASE)
    ACKNOWLEDGMENTS = re.compile(r'^(?:Acknowledgments|Acknowledgements)', re.IGNORECASE)
    
    def __init__(self, pdf_path: str, config: Any = None):
        self.pdf_path = Path(pdf_path)
        self.config = config
        self.elements: List[PDFElement] = []
        self._page_count = 0
        self._metadata = {}
        
    def parse(self) -> List[PDFElement]:
        """Parse PDF and extract all elements."""
        import fitz  # PyMuPDF
        
        doc = fitz.open(str(self.pdf_path))
        self._page_count = len(doc)
        self._metadata = doc.metadata
        
        skip_references = self._should_skip_references()
        in_references = False
        
        for page_num, page in enumerate(doc, start=1):
            blocks = page.get_text("blocks")
            
            for block in blocks:
                # block format: [x0, y0, x1, y1, text, block_no, block_type]
                x0, y0, x1, y1, text, block_no, block_type = block
                text = text.strip()
                
                if not text:
                    continue
                
                # Check if entering references section
                if skip_references and self.REFERENCES_HEADING.search(text):
                    in_references = True
                    continue
                
                if in_references:
                    continue
                
                # Classify the element
                element_type = self._classify_element(text, page_num)
                
                if element_type:
                    element = PDFElement(
                        page_num=page_num,
                        element_type=element_type,
                        content=text,
                        bbox=(x0, y0, x1, y1)
                    )
                    self.elements.append(element)
            
            # Extract images with captions
            image_list = page.get_images()
            for img_index, img in enumerate(image_list):
                # Get image position
                pix = page.get_pixmap(matrix=fitz.Matrix(1, 1), xref=img[0])
                # Find caption near image (simplified)
                element = PDFElement(
                    page_num=page_num,
                    element_type="figure_image",
                    content=f"[Image on page {page_num}]",
                    bbox=None
                )
                self.elements.append(element)
        
        doc.close()
        return self.elements
    
    def _should_skip_references(self) -> bool:
        """Check if references should be skipped."""
        if self.config:
            return self.config.get('pdf.skip_references', True)
        return True
    
    def _classify_element(self, text: str, page_num: int) -> Optional[str]:
        """Classify a text block."""
        # Skip very short text
        if len(text) < 3:
            return None
        
        # Check for figure caption
        if self.FIGURE_PATTERN.match(text):
            return "figure_caption"
        
        # Check for table caption
        if self.TABLE_PATTERN.match(text):
            return "table_caption"
        
        # Check for section heading (all caps or short + colon)
        if len(text) < 100 and (text.isupper() or text.endswith(':')):
            return "heading"
        
        # Check for bullet points (common in paper sections)
        if text.strip().startswith(('•', '-', '·', '1.', '2.', '3.')):
            return "list_item"
        
        # Default to paragraph
        return "paragraph"
    
    def get_text_elements(self) -> List[PDFElement]:
        """Get only text elements (excluding images)."""
        return [e for e in self.elements if e.element_type != "figure_image"]
    
    def get_elements_by_page(self, page_num: int) -> List[PDFElement]:
        """Get all elements from a specific page."""
        return [e for e in self.elements if e.page_num == page_num]
    
    @property
    def page_count(self) -> int:
        return self._page_count
    
    @property
    def title(self) -> str:
        return self._metadata.get('title', self.pdf_path.stem)
    
    @property
    def author(self) -> str:
        return self._metadata.get('author', 'Unknown')


# For backwards compatibility
from .config_loader import config