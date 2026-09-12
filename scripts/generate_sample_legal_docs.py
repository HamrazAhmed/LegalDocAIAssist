# -*- coding: utf-8 -*-
"""
Generates authentic sample legal contract PDFs and text documents in sample_documents/
These documents can be loaded directly in LegalDocAiAssist for live demonstrations and tests.
"""

import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAMPLES_DIR = os.path.join(ROOT_DIR, "sample_documents")
os.makedirs(SAMPLES_DIR, exist_ok=True)

COMMERCIAL_SERVICES_AGREEMENT = """MASTER SERVICES AGREEMENT

This Master Services Agreement ("Agreement") is made and entered into as of January 15, 2025 ("Effective Date"), by and between:
VERTEX CLOUD TECHNOLOGIES (PVT) LIMITED, a company incorporated under the laws of Pakistan, having its registered office at 42-B, Commercial Zone, Gulberg III, Lahore ("Service Provider"), and
MERIDIAN GLOBAL LOGISTICS INC., a corporation organized under applicable laws, having its principal office at Suite 800, Financial District, Karachi ("Client").

Service Provider and Client are collectively referred to as the "Parties" and individually as a "Party."

RECITALS
WHEREAS, Client desires to retain Service Provider to perform enterprise software development and cloud integration services; and
WHEREAS, Service Provider possesses the technical expertise, personnel, and resources required to perform such services;
NOW, THEREFORE, in consideration of the mutual covenants and promises herein contained, the Parties agree as follows:

1. SCOPE OF SERVICES AND DELIVERABLES
1.1 Statements of Work. Service Provider shall provide the professional cloud architecture, backend development, and cybersecurity integration services described in one or more Statements of Work ("SOW") executed by both Parties.
1.2 Standard of Performance. Service Provider covenants that all deliverables and services shall be performed in a timely, professional, and workmanlike manner in conformity with industry standards.
1.3 Change Orders. Any material modification or expansion to the agreed scope of work must be documented in a written Change Order signed by authorized representatives of both Parties.

2. FEES, INVOICING, AND PAYMENT TERMS
2.1 Compensation. Client shall pay Service Provider the milestone fees and time-and-materials rates set forth in each applicable SOW.
2.2 Invoicing Schedule. Service Provider shall invoice Client on the first business day of each calendar month for services rendered during the preceding month.
2.3 Payment Terms. Client shall pay all undisputed invoice amounts within thirty (30) calendar days from receipt of invoice ("Net 30").
2.4 Late Payment Interest. Any undisputed amount not paid when due shall accrue late interest at the rate of 1.5% per month, or the maximum rate permitted by law, calculated daily from the due date until paid in full.
2.5 Disputed Invoices. Client shall notify Service Provider in writing within ten (10) business days of invoice receipt if Client disputes any charge in good faith. Undisputed portions must be paid on schedule.

3. TERM AND TERMINATION
3.1 Term. This Agreement shall commence on the Effective Date and remain in full force for an initial term of two (2) years, unless terminated earlier pursuant to this Section 3.
3.2 Termination for Convenience. Client or Service Provider may terminate this Agreement or any SOW for any reason or no reason upon providing sixty (60) days advance written notice to the other Party.
3.3 Termination for Material Breach. Either Party may terminate this Agreement immediately upon written notice if the other Party commits a material breach of any obligation and fails to cure such breach within thirty (30) calendar days of receiving written notice thereof.
3.4 Immediate Termination. Either Party may terminate this Agreement immediately without cure period if the other Party: (a) breaches Section 5 (Confidentiality); (b) becomes insolvent or files for bankruptcy; or (c) engages in gross negligence or willful misconduct.
3.5 Effect of Termination. Upon termination, Client shall pay Service Provider for all completed work and non-cancelable commitments incurred up to the effective termination date. All proprietary files and confidential records must be returned or destroyed within fourteen (14) days.

4. INTELLECTUAL PROPERTY RIGHTS
4.1 Client Ownership. All custom deliverables, source code, designs, and work products developed specifically for Client under an SOW shall be the exclusive property of Client upon full payment of all applicable fees ("Work for Hire").
4.2 Pre-existing IP. Service Provider retains sole and exclusive ownership of all pre-existing software, libraries, algorithms, and tools owned or licensed by Service Provider prior to the Effective Date ("Background IP").
4.3 License to Background IP. Service Provider grants Client a perpetual, worldwide, non-exclusive, royalty-free license to use Background IP solely as incorporated into the Deliverables.

5. CONFIDENTIALITY AND NON-DISCLOSURE
5.1 Definition. "Confidential Information" means all non-public technical, business, customer, or financial data disclosed by one Party to the other, marked as confidential or reasonably understood to be confidential.
5.2 Obligations. The receiving Party agrees: (a) to hold Confidential Information in strict confidence; (b) not to disclose it to third parties without prior written consent; and (c) to use it solely for executing this Agreement.
5.3 Exclusions. Confidentiality obligations do not apply to information that: (a) is or becomes public knowledge without breach; (b) was already known to the recipient prior to disclosure; or (c) is required to be disclosed by valid court subpoena.
5.4 Survival. Confidentiality obligations shall survive termination of this Agreement for a period of five (5) years.

6. INDEMNIFICATION AND HOLD HARMLESS
6.1 Vendor Indemnity. Service Provider shall defend, indemnify, and hold harmless Client, its directors, officers, and employees against any third-party claims, liabilities, losses, or legal costs arising out of any allegation that the Deliverables infringe any valid patent, copyright, or trade secret.
6.2 Client Indemnity. Client shall defend, indemnify, and hold harmless Service Provider against third-party claims arising from: (a) Client's breach of applicable laws; or (b) data, content, or materials provided by Client to Service Provider.
6.3 Indemnification Procedure. The indemnified Party must give prompt written notice of the claim, grant the indemnifying Party sole control of defense and settlement, and provide reasonable assistance at the indemnifying Party's expense.

7. LIMITATION OF LIABILITY
7.1 Consequential Damages Waiver. Under no circumstances shall either Party be liable to the other for indirect, incidental, special, exemplary, or consequential damages, or loss of profits, data, or business opportunities.
7.2 Aggregate Liability Cap. The total aggregate liability of either Party arising out of or related to this Agreement, whether in contract, tort, or otherwise, shall be strictly capped at the total amount paid or payable by Client to Service Provider under this Agreement during the twelve (12) months preceding the event giving rise to liability.
7.3 Carveouts. The liability limitations in Sections 7.1 and 7.2 shall NOT apply to: (a) breach of Section 5 (Confidentiality); (b) indemnification obligations under Section 6; or (c) damages caused by gross negligence or intentional fraud.

8. GOVERNING LAW AND DISPUTE RESOLUTION
8.1 Governing Law. This Agreement shall be construed and governed in accordance with the substantive laws of Pakistan, without regard to its conflict of laws principles.
8.2 Good Faith Negotiation. In the event of any controversy or claim arising out of this Agreement, the Parties shall first attempt in good faith to resolve the dispute through executive negotiations for at least twenty-one (21) days.
8.3 Arbitration. Any dispute not resolved through negotiation shall be submitted to final and binding arbitration under the Arbitration Act, 1940. The arbitration shall take place in Lahore, Pakistan, conducted in the English language before a sole arbitrator mutually agreed by the Parties.

9. GENERAL BOILERPLATE PROVISIONS
9.1 Force Majeure. Neither Party shall be liable for delays or non-performance resulting from acts of God, flood, war, pandemic, government restriction, or civil unrest beyond reasonable control.
9.2 Severability. If any provision of this Agreement is held invalid or unenforceable, the remaining provisions shall remain in full force and effect.
9.3 Entire Agreement. This Agreement constitutes the entire agreement between the Parties and supersedes all prior negotiations, representations, or oral agreements.
9.4 Counterparts. This Agreement may be executed in counterparts, each of which shall be deemed an original, and electronic signatures shall be legally binding.

IN WITNESS WHEREOF, the Parties have caused this Master Services Agreement to be executed by their duly authorized representatives.

VERTEX CLOUD TECHNOLOGIES (PVT) LTD         MERIDIAN GLOBAL LOGISTICS INC.
By: __________________________________         By: __________________________________
Name: Tariq Mansoor                            Name: Sarah J. Jenkins
Title: Chief Executive Officer                 Title: VP of Global Operations
Date: January 15, 2025                         Date: January 15, 2025
"""

MUTUAL_NDA_AGREEMENT = """MUTUAL NON-DISCLOSURE AND CONFIDENTIALITY AGREEMENT

This Mutual Non-Disclosure Agreement ("Agreement") is entered into as of March 1, 2025 ("Effective Date"), by and between:
ALPHA FINTECH INNOVATIONS LIMITED, having its principal office at 14 Blue Area, Islamabad ("Party A"), and
DELTA CAPITAL VENTURES LLP, having its principal office at 78 Clifton Block 4, Karachi ("Party B").

Each of Party A and Party B may be referred to individually as a "Party" and collectively as the "Parties," and as a "Disclosing Party" or "Receiving Party" respectively.

1. PURPOSE
The Parties wish to explore potential business collaboration and investment opportunities in digital payment infrastructure ("Purpose"). In connection with this Purpose, each Party may disclose proprietary commercial and technical information.

2. DEFINITION OF CONFIDENTIAL INFORMATION
"Confidential Information" means all non-public information disclosed directly or indirectly by Disclosing Party to Receiving Party, whether orally, visually, or in writing, including but not limited to business plans, financial models, customer data, source code, patent applications, algorithmic architectures, and trade secrets.

3. EXCLUSIONS FROM CONFIDENTIALITY
Confidential Information does not include information that:
(a) is or becomes generally available to the public without breach of this Agreement;
(b) was already rightfully in Receiving Party's possession prior to disclosure without confidentiality restrictions;
(c) is lawfully received from a third party without breach of any confidentiality obligation; or
(d) is independently developed by Receiving Party without access to or reliance upon Disclosing Party's Confidential Information.

4. OBLIGATIONS OF RECEIVING PARTY
4.1 Standard of Care. Receiving Party shall protect Disclosing Party's Confidential Information with the same degree of care it uses for its own confidential information of like nature, but in no event less than reasonable care.
4.2 Permitted Disclosures. Receiving Party may disclose Confidential Information only to its employees, directors, legal counsel, and financial advisors who need to know for the Purpose and who are bound by confidentiality obligations at least as restrictive as this Agreement.
4.3 Non-Use. Receiving Party shall not use Confidential Information for any purpose other than evaluating and pursuing the Purpose.

5. COMPELLED DISCLOSURE
If Receiving Party is requested or required by law, court subpoena, or governmental authority to disclose any Confidential Information, Receiving Party shall provide prompt written notice to Disclosing Party to enable Disclosing Party to seek a protective order or contest the disclosure.

6. RETURN OR DESTRUCTION OF MATERIALS
Upon written request of Disclosing Party or termination of this Agreement, Receiving Party shall promptly return or destroy all documents, notes, and electronic copies containing Confidential Information, and certify compliance in writing within ten (10) business days.

7. EQUITABLE RELIEF
Receiving Party acknowledges that any unauthorized disclosure or use of Confidential Information will cause irreparable injury for which monetary damages alone would be inadequate. Accordingly, Disclosing Party shall be entitled to seek injunctive relief and specific performance in court without proving actual damages or posting bond.

8. TERM AND SURVIVAL
This Agreement shall govern disclosures made for one (1) year from the Effective Date. Receiving Party's confidentiality obligations shall survive for three (3) years following disclosure. Trade secrets shall be maintained in confidence perpetually.

9. GOVERNING LAW
This Agreement shall be governed by and construed in accordance with the laws of Pakistan, and the courts of Islamabad shall have exclusive jurisdiction over any disputes.

IN WITNESS WHEREOF, the Parties have executed this Mutual Non-Disclosure Agreement.

ALPHA FINTECH INNOVATIONS LTD                 DELTA CAPITAL VENTURES LLP
By: ______________________________             By: ______________________________
Name: Asim Zubair                              Name: Hamza Khalid
Title: Managing Director                       Title: General Partner
"""

RESIDENTIAL_TENANCY_AGREEMENT = """RESIDENTIAL TENANCY LEASE AGREEMENT (KIRAYANAMA)

This Tenancy Agreement is executed at Lahore on this 1st day of February, 2025, by and between:
MR. MUHAMMAD FAROOQ, CNIC No. 35202-1234567-1, resident of House No. 12, Street 4, Sector Y, DHA Phase 3, Lahore (hereinafter called the "LANDLORD", which term includes his legal heirs, executors, and assigns) of the FIRST PART;
AND
MR. BILAL AHMED KHAN, CNIC No. 35201-9876543-3, resident of Flat 4, Model Town, Lahore (hereinafter called the "TENANT", which term includes his legal heirs, executors, and permitted occupants) of the SECOND PART.

WHEREAS Landlord is the absolute and lawful owner of residential property situated at House No. 85, Sector Z, DHA Phase 5, Lahore, comprising 1 Kanal house with 4 bedrooms, drawing room, kitchen, and lawn ("Rented Premises"); and
WHEREAS Tenant has agreed to take the Rented Premises on rent on the following terms and conditions:

1. TENANCY PERIOD AND RENEWAL
1.1 Duration. The tenancy shall be for an initial period of eleven (11) months, commencing from February 1, 2025 and expiring on December 31, 2025.
1.2 Renewal. The tenancy may be renewed by mutual consent of both parties through a fresh written agreement signed at least one (1) month prior to expiry.
1.3 Escalation. If renewed, the monthly rent shall increase by 10% (ten percent) annually.

2. MONTHLY RENT AND SECURITY DEPOSIT
2.1 Monthly Rent. The agreed monthly rent is PKR 150,000/- (Rupees One Hundred Fifty Thousand only).
2.2 Payment Due Date. Tenant shall pay the monthly rent in advance on or before the 5th calendar day of each month via direct bank transfer to Landlord's designated bank account.
2.3 Security Deposit. Tenant has deposited PKR 300,000/- (Rupees Three Hundred Thousand only, equivalent to two months rent) as refundable security deposit with Landlord. This deposit shall be refunded upon peaceful handover of possession after deducting unpaid utility bills or repair costs for tenant-caused damages.

3. UTILITIES AND TAXES
3.1 Utility Bills. Tenant shall promptly pay all utility charges for electricity (LESCO), gas (SNGPL), water, sanitation, and DHA maintenance charges according to actual consumption bills.
3.2 Property Tax. Government property taxes and capital value levies shall be the sole responsibility of Landlord.

4. TENANT'S COVENANTS AND RESTRICTIONS
4.1 Residential Use Only. The premises shall be used exclusively for peaceful residential family living. Commercial activities, guest house operations, or illegal uses are strictly prohibited.
4.2 No Subletting. Tenant shall not sublet, assign, or share possession of the premises or any part thereof with any third party.
4.3 Structural Alterations. Tenant shall make no structural changes, alterations, or demolitions without Landlord's prior written permission.
4.4 Cleanliness and Maintenance. Tenant shall maintain the property in clean and good sanitary condition, responsible for minor day-to-day repairs (plumbing washers, bulbs, switchboards).

5. INSPECTION AND REPAIRS
5.1 Landlord Inspection. Landlord or his authorized agent shall have the right to inspect the premises during reasonable daytime hours upon giving twenty-four (24) hours advance notice.
5.2 Major Repairs. Structural defects, roof leakage, or major seepage shall be rectified by Landlord at his own expense within reasonable time.

6. TERMINATION AND VACATION
6.1 Notice Period. Either party may terminate this tenancy before expiry by serving one (1) month advance written notice or paying one month rent in lieu of notice.
6.2 Default Eviction. If Tenant fails to pay rent for two consecutive months or breaches any fundamental clause, Landlord may issue a 15-day notice to vacate pursuant to the Punjab Rented Premises Act, 2009.
6.3 Handover. Upon vacation, Tenant shall deliver peaceful vacant possession in the same condition as received, normal wear and tear excepted.

7. REGISTRATION AND DISPUTE RESOLUTION
This agreement shall be registered with the local Police Station and Rent Tribunal pursuant to the Punjab Rented Premises Act. Disputes shall be subject to the exclusive jurisdiction of the Rent Tribunal, Lahore.

IN WITNESS WHEREOF, Landlord and Tenant have set their hands in the presence of witnesses.

LANDLORD: ______________________             TENANT: ______________________
Muhammad Farooq                               Bilal Ahmed Khan
CNIC: 35202-1234567-1                         CNIC: 35201-9876543-3

WITNESS 1: _____________________             WITNESS 2: _____________________
Name: Tariq Javed                             Name: Usman Riaz
CNIC: 35202-1111222-3                         CNIC: 35201-4444555-7
"""


def build_pdf_from_text(title: str, text: str, output_path: str):
    """
    Creates a valid, clean PDF 1.4 document using standard Adobe Type 1 fonts
    without requiring external C-libraries or compilers.
    """
    lines = text.strip().split("\n")
    
    # Page dimensions (Letter: 612 x 792 points)
    page_width = 612
    page_height = 792
    margin_x = 54
    margin_y = 54
    line_height = 13
    usable_height = page_height - (margin_y * 2)
    lines_per_page = int(usable_height // line_height)
    
    # Break lines into pages
    pages_lines = []
    curr_page = []
    
    for line in lines:
        # Wrap long lines (> 85 chars)
        if len(line) > 85:
            words = line.split(" ")
            wrapped = ""
            for w in words:
                if len(wrapped) + len(w) + 1 > 85:
                    curr_page.append(wrapped)
                    if len(curr_page) >= lines_per_page:
                        pages_lines.append(curr_page)
                        curr_page = []
                    wrapped = w
                else:
                    wrapped = f"{wrapped} {w}".strip()
            if wrapped:
                curr_page.append(wrapped)
                if len(curr_page) >= lines_per_page:
                    pages_lines.append(curr_page)
                    curr_page = []
        else:
            curr_page.append(line)
            if len(curr_page) >= lines_per_page:
                pages_lines.append(curr_page)
                curr_page = []
                
    if curr_page:
        pages_lines.append(curr_page)

    # Build PDF Objects
    # Object 1: Catalog
    # Object 2: Pages
    # Object 3, 4: Fonts (Helvetica, Helvetica-Bold)
    # Then for each page: Page object and Contents stream object
    num_pages = len(pages_lines)
    
    objects = {}
    next_obj_id = 1
    
    catalog_id = 1
    pages_root_id = 2
    font_norm_id = 3
    font_bold_id = 4
    next_obj_id = 5
    
    page_obj_ids = []
    content_obj_ids = []
    
    for _ in range(num_pages):
        page_obj_ids.append(next_obj_id)
        next_obj_id += 1
        content_obj_ids.append(next_obj_id)
        next_obj_id += 1
        
    objects[catalog_id] = f"<< /Type /Catalog /Pages {pages_root_id} 0 R >>"
    kids_str = " ".join([f"{pid} 0 R" for pid in page_obj_ids])
    objects[pages_root_id] = f"<< /Type /Pages /Kids [{kids_str}] /Count {num_pages} >>"
    objects[font_norm_id] = "<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>"
    objects[font_bold_id] = "<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >>"
    
    for i, (p_lines, pid, cid) in enumerate(zip(pages_lines, page_obj_ids, content_obj_ids)):
        page_num = i + 1
        objects[pid] = (
            f"<< /Type /Page /Parent {pages_root_id} 0 R "
            f"/MediaBox [0 0 {page_width} {page_height}] "
            f"/Resources << /Font << /F1 {font_norm_id} 0 R /F2 {font_bold_id} 0 R >> >> "
            f"/Contents {cid} 0 R >>"
        )
        
        # Build stream content
        stream_cmds = []
        # Header / Page number
        stream_cmds.append("BT")
        stream_cmds.append("/F2 9 Tf")
        stream_cmds.append(f"1 0 0 1 {margin_x} {page_height - 35} Tm")
        safe_title = title.replace("(", "\\(").replace(")", "\\)")
        stream_cmds.append(f"({safe_title}) Tj")
        stream_cmds.append(f"1 0 0 1 {page_width - margin_x - 60} {page_height - 35} Tm")
        stream_cmds.append(f"(Page {page_num} of {num_pages}) Tj")
        stream_cmds.append("ET")
        
        # Thin divider line below header
        stream_cmds.append(f"0.7 0.7 0.7 RG 0.5 w {margin_x} {page_height - 42} m {page_width - margin_x} {page_height - 42} l S")
        
        # Text block
        start_y = page_height - margin_y - 15
        stream_cmds.append("BT")
        stream_cmds.append(f"1 0 0 1 {margin_x} {start_y} Tm")
        stream_cmds.append(f"{line_height} TL")
        
        for l in p_lines:
            escaped = l.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
            # Check if title or section header
            if l.isupper() and len(l) > 3:
                stream_cmds.append("/F2 10 Tf")
            elif l.startswith(("1.", "2.", "3.", "4.", "5.", "6.", "7.", "8.", "9.", "10.")):
                stream_cmds.append("/F2 9.5 Tf")
            else:
                stream_cmds.append("/F1 8.5 Tf")
                
            stream_cmds.append(f"({escaped}) '")
            
        stream_cmds.append("ET")
        
        stream_data = "\n".join(stream_cmds).encode("latin1", errors="replace")
        stream_len = len(stream_data)
        
        content_header = f"<< /Length {stream_len} >>\nstream\n"
        content_footer = "\nendstream"
        objects[cid] = (content_header, stream_data, content_footer)

    # Serialize PDF with xref
    pdf_bytes = bytearray()
    pdf_bytes.extend(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    
    xref_offsets = {}
    
    for obj_id in sorted(objects.keys()):
        xref_offsets[obj_id] = len(pdf_bytes)
        val = objects[obj_id]
        if isinstance(val, tuple):
            header, stream, footer = val
            pdf_bytes.extend(f"{obj_id} 0 obj\n{header}".encode("latin1"))
            pdf_bytes.extend(stream)
            pdf_bytes.extend(f"{footer}\nendobj\n".encode("latin1"))
        else:
            pdf_bytes.extend(f"{obj_id} 0 obj\n{val}\nendobj\n".encode("latin1"))
            
    xref_start = len(pdf_bytes)
    total_objs = max(objects.keys()) + 1
    pdf_bytes.extend(f"xref\n0 {total_objs}\n0000000000 65535 f \n".encode("latin1"))
    
    for obj_id in range(1, total_objs):
        offset = xref_offsets.get(obj_id, 0)
        pdf_bytes.extend(f"{offset:010d} 00000 n \n".encode("latin1"))
        
    trailer = (
        f"trailer\n<< /Size {total_objs} /Root {catalog_id} 0 R >>\n"
        f"startxref\n{xref_start}\n%%EOF\n"
    )
    pdf_bytes.extend(trailer.encode("latin1"))
    
    with open(output_path, "wb") as f:
        f.write(pdf_bytes)
    print(f"Generated PDF: {output_path} ({len(pdf_bytes)} bytes, {num_pages} pages)")


def main():
    docs = [
        ("Commercial Services Agreement", COMMERCIAL_SERVICES_AGREEMENT, "commercial_services_agreement"),
        ("Mutual Non-Disclosure Agreement", MUTUAL_NDA_AGREEMENT, "mutual_non_disclosure_agreement"),
        ("Residential Tenancy Agreement", RESIDENTIAL_TENANCY_AGREEMENT, "residential_tenancy_agreement"),
    ]
    
    for title, content, base_name in docs:
        txt_path = os.path.join(SAMPLES_DIR, f"{base_name}.txt")
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Saved Text: {txt_path}")
        
        pdf_path = os.path.join(SAMPLES_DIR, f"{base_name}.pdf")
        build_pdf_from_text(title, content, pdf_path)

if __name__ == "__main__":
    main()
