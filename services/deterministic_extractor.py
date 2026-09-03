import re
from bs4 import BeautifulSoup
from typing import Dict, Any, List

class ExtractedField:
    def __init__(self, name: str, value: str, evidence: str, confidence: str):
        self.name = name
        self.value = value
        self.evidence = evidence
        self.confidence = confidence

class DeterministicExtractor:
    
    @staticmethod
    def extract_from_html(html_content: str, source_type: str) -> Dict[str, ExtractedField]:
        if source_type not in ["OFFICIAL_WEBSITE", "OFFICIAL_RTI_PAGE", "OFFICIAL_PIO_PAGE", "OFFICIAL_PORTAL"]:
            return {} # UNEXTRACTABLE
            
        soup = BeautifulSoup(html_content, "html.parser")
        fields = {}
        
        # 1. PIO Name and Designation (Simple pattern matching for tables or strong labels)
        pio_candidates = DeterministicExtractor._find_label_value(soup, ["public information officer", "pio", "nodal officer"])
        if len(pio_candidates) == 1:
            val, ev = pio_candidates[0]
            fields["pio_name"] = ExtractedField("pio_name", val, ev, "HIGH")
        elif len(pio_candidates) > 1:
            fields["pio_name"] = ExtractedField("pio_name", "MULTIPLE_CANDIDATES", "Found multiple potential PIOs", "AMBIGUOUS")
            
        # 2. Appellate Authority
        faa_candidates = DeterministicExtractor._find_label_value(soup, ["first appellate authority", "appellate authority", "faa"])
        if len(faa_candidates) == 1:
            val, ev = faa_candidates[0]
            fields["appellate_authority_designation"] = ExtractedField("appellate_authority_designation", val, ev, "HIGH")
        elif len(faa_candidates) > 1:
            fields["appellate_authority_designation"] = ExtractedField("appellate_authority_designation", "MULTIPLE_CANDIDATES", "Found multiple potential FAAs", "AMBIGUOUS")
            
        # 3. Filing Fee
        fee_candidates = DeterministicExtractor._find_label_value(soup, ["rti fee", "application fee", "filing fee"])
        for val, ev in fee_candidates:
            if "rs" in val.lower() or "rupee" in val.lower() or any(char.isdigit() for char in val):
                # Clean up value
                clean_fee = val.strip()
                fields["filing_fee"] = ExtractedField("filing_fee", clean_fee, ev, "HIGH")
                break
                
        # 4. Online Portal
        portal_links = soup.find_all('a', href=re.compile(r"http.*rtionline.*gov.*in", re.I))
        if portal_links:
            href = portal_links[0].get("href")
            ev = portal_links[0].get_text(strip=True)[:100]
            fields["online_portal"] = ExtractedField("online_portal", href, ev, "HIGH")
            
        return fields
        
    @staticmethod
    def _find_label_value(soup: BeautifulSoup, keywords: List[str]) -> List[tuple]:
        """Finds label-value pairs using tables or adjacent text."""
        candidates = []
        
        # Strategy 1: Tables (th -> td)
        for th in soup.find_all(['th', 'td']):
            text = th.get_text(separator=" ", strip=True).lower()
            if any(kw in text for kw in keywords):
                # Find the next td
                next_td = th.find_next_sibling('td')
                if next_td:
                    val = next_td.get_text(separator=" ", strip=True)
                    if val and len(val) > 2:
                        evidence = str(th.parent)[:200] # store the tr string as evidence
                        candidates.append((val, evidence))
                        
        # Strategy 2: Label -> Text (e.g., <strong>PIO:</strong> John Doe)
        if not candidates:
            for el in soup.find_all(['strong', 'b', 'span', 'div']):
                text = el.get_text(separator=" ", strip=True).lower()
                if text.endswith(":") and any(kw in text for kw in keywords):
                    # the value is usually the next sibling string
                    sibling = el.next_sibling
                    if sibling and isinstance(sibling, str) and sibling.strip():
                        val = sibling.strip()
                        evidence = el.parent.get_text(separator=" ", strip=True)[:200]
                        candidates.append((val, evidence))
                        
        return candidates
