# -*- coding: utf-8 -*-
"""
Script to expand legal_terms.json, common_clauses.json, and government_forms.json
with authentic, comprehensive, real-world legal definitions and bilingual metadata.
"""

import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KB_DIR = os.path.join(BASE_DIR, "knowledge_base")

# -------------------------------------------------------------
# 1. EXPAND LEGAL TERMS
# -------------------------------------------------------------
NEW_LEGAL_TERMS = [
    {
        "term": "Liquidated Damages",
        "category": "Remedies & Damages",
        "definition": "A predetermined, fixed sum agreed upon in the contract that one party will pay as compensation to the other upon a specific breach.",
        "simple_english": "A pre-agreed financial penalty or compensation amount if a specific promise or deadline is broken.",
        "simple_urdu": "پہلے سے طے شدہ ہرجانے کی رقم جو معاہدے کی خلاف ورزی کی صورت میں فریقِ ثانی کو ادا کی جائے گی۔",
        "important_note": "Courts will only enforce liquidated damages if they represent a genuine pre-estimate of loss, not an arbitrary punitive penalty.",
        "aliases": ["Agreed Damages", "Pre-estimated Damages", "Stipulated Damages"]
    },
    {
        "term": "Specific Performance",
        "category": "Remedies & Damages",
        "definition": "An equitable court order compelling a defaulting party to carry out the exact contractual obligations they promised, rather than merely paying money damages.",
        "simple_english": "A court ruling forcing someone to actually fulfill their promise (e.g. deliver unique real estate or rare goods).",
        "simple_urdu": "عدالتی حکم جس کے تحت کسی فریق کو معاہدے کے عین مطابق اپنے وعدے کو عملی طور پر پورا کرنے کا پابند کیا جاتا ہے۔",
        "important_note": "Granted primarily when monetary damages are inadequate to compensate for the breach (e.g. sale of unique land).",
        "aliases": ["Equitable Enforcement", "Court Order for Performance"]
    },
    {
        "term": "Promissory Estoppel",
        "category": "Foundations",
        "definition": "A legal doctrine that prevents a party from going back on a promise when the other party reasonably relied upon that promise to their financial or practical detriment.",
        "simple_english": "A rule stopping someone from breaking their word if the other person took action and suffered a loss based on that promise.",
        "simple_urdu": "قانونی اصول جو کسی فریق کو اپنے وعدے سے مکرنے سے روکتا ہے اگر دوسرے فریق نے اس پر بھروسہ کر کے نقصان اٹھایا ہو۔",
        "important_note": "Can enforce a promise even in the absence of a formal consideration exchange under equitable justice.",
        "aliases": ["Estoppel", "Detrimental Reliance"]
    },
    {
        "term": "Injunction",
        "category": "Remedies & Damages",
        "definition": "A judicial order commanding a party to refrain from doing a specified act (prohibitory injunction) or to perform a mandatory corrective act (mandatory injunction).",
        "simple_english": "A court stay order forcing a party to halt an action immediately or do a mandatory fix.",
        "simple_urdu": "عدالتی حکمِ امتناعی (اسٹے آرڈر) جو کسی مخصوص کام کو روکنے یا فوری نافذ کرنے کے لیے دیا جاتا ہے۔",
        "important_note": "Frequently sought in IP infringement, trade secret disclosure, or breach of non-disclosure agreements.",
        "aliases": ["Restraining Order", "Stay Order", "Interlocutory Injunction"]
    },
    {
        "term": "Caveat Emptor",
        "category": "Commercial Principles",
        "definition": "A common law commercial maxim meaning 'let the buyer beware,' placing the duty of inspection on the purchaser before finalizing a deal.",
        "simple_english": "The buyer assumes the risk and responsibility to examine the goods or property before buying.",
        "simple_urdu": "خریدار کی ہوشیاری کا اصول، یعنی خریداری سے قبل چیز کا خود جائزہ لینا خریدار کی ذمہ داری ہے۔",
        "important_note": "Modern consumer protection statutes have introduced significant statutory warranties that mitigate this traditional doctrine.",
        "aliases": ["Buyer Beware", "Purchaser Due Diligence"]
    },
    {
        "term": "Subrogation",
        "category": "Risk Allocation & Insurance",
        "definition": "The legal substitution of one person or insurer in place of another with respect to a lawful claim, demand, or right against a third party.",
        "simple_english": "When an insurer pays your claim and inherits your right to sue the person who caused the damage.",
        "simple_urdu": "ایک فریق (جیسے انشورنس کمپنی) کا دوسرے فریق کی جگہ قانونی حقوق حاصل کرنا تاکہ نقصان پہنچانے والے سے ریکوری کی جا سکے۔",
        "important_note": "Commercial leases frequently include a 'waiver of subrogation' to prevent insurers from suing tenants after settling property damage.",
        "aliases": ["Right of Subrogation", "Legal Substitution"]
    },
    {
        "term": "Novation",
        "category": "Contract Lifecycle",
        "definition": "The legal substitution of a new contract or party in place of an existing one, completely releasing the original obligor from liability with the consent of all parties.",
        "simple_english": "Replacing an old contract or partner with a new one, completely freeing the original party from duties.",
        "simple_urdu": "پرانے معاہدے یا فریق کی جگہ نئے معاہدے یا فریق کا قانونی نعم البدل جس سے پرانا فریق بری الذمہ ہو جاتا ہے۔",
        "important_note": "Requires the explicit mutual consent of all contracting parties, unlike a unilateral assignment of rights.",
        "aliases": ["Contract Substitution", "Replacement Agreement"]
    },
    {
        "term": "Privity of Contract",
        "category": "Foundations",
        "definition": "The legal doctrine establishing that a contract cannot confer rights or impose obligations on any person who is not an actual party to it.",
        "simple_english": "Only people or companies that actually signed the contract can sue or be sued on its terms.",
        "simple_urdu": "معاہداتی استحقاق کا اصول، جس کے مطابق صرف معاہدے کے فریقین ہی ایک دوسرے کے خلاف دعویٰ دائر کر سکتے ہیں۔",
        "important_note": "Third-party beneficiary clauses explicitly carve out exceptions to this strict traditional rule.",
        "aliases": ["Privity Doctrine", "Contractual Relationship"]
    },
    {
        "term": "Ultra Vires",
        "category": "Corporate & Authority",
        "definition": "A Latin phrase meaning 'beyond the powers,' describing actions taken by a corporation or official that exceed the scope of their legal or constitutional authority.",
        "simple_english": "Acts done without legal authority or exceeding the allowed powers granted by corporate charter or statute.",
        "simple_urdu": "اختیار سے تجاوز، یعنی ایسا اقدام جو کمپنی کے میمورنڈم یا قانونی دائرہ اختیار سے باہر ہو۔",
        "important_note": "Contracts entered ultra vires may be void or unenforceable against the corporate entity.",
        "aliases": ["Beyond Legal Power", "Lack of Authority"]
    },
    {
        "term": "Quantum Meruit",
        "category": "Remedies & Damages",
        "definition": "A legal principle meaning 'as much as he has deserved,' awarding reasonable compensation for work or services rendered where no fixed price was finalized or contract was terminated early.",
        "simple_english": "Receiving fair market payment for the actual value of work completed, even without a finished contract.",
        "simple_urdu": "انجام دیے گئے کام کی مناسب اور منصفانہ اجرت کا استحقاق۔",
        "important_note": "Frequently invoked in construction and professional consultancy when contracts are aborted mid-stream.",
        "aliases": ["Reasonable Value of Services", "Unjust Enrichment Remedy"]
    },
    {
        "term": "Covenant",
        "category": "Duties & Performance",
        "definition": "A formal, solemn, and legally binding promise or commitment in a contract to do (affirmative covenant) or refrain from doing (negative covenant) a specified act.",
        "simple_english": "A strict contractual promise to take action or avoid doing something.",
        "simple_urdu": "باقاعدہ اور سنجیدہ قانونی عہد یا وعدہ جس کی پابندی لازمی ہو۔",
        "important_note": "Breach of covenant can trigger termination rights and direct indemnity obligations.",
        "aliases": ["Binding Promise", "Contractual Undertaking"]
    },
    {
        "term": "Lien",
        "category": "Security & Debt",
        "definition": "A legal right or claim that a creditor holds against another's property as security for a debt or performance of an obligation until satisfied.",
        "simple_english": "A legal hold on property or assets until an outstanding debt or service charge is fully paid.",
        "simple_urdu": "حقِ حبس، یعنی بقایا رقم کی وصولی تک کسی کے مال یا جائیداد کو اپنے قبضے میں رکھنے کا قانونی حق۔",
        "important_note": "Mechanics' liens or commercial possessory liens can block the sale or transfer of real property until discharged.",
        "aliases": ["Security Interest", "Encumbrance", "Possessory Lien"]
    },
    {
        "term": "Joint and Several Liability",
        "category": "Risk Allocation & Insurance",
        "definition": "A liability structure where two or more parties are collectively and individually responsible for the entire obligation or damage, allowing the claimant to recover 100% from any single party.",
        "simple_english": "When multiple co-signers are each fully responsible for the entire debt, so the creditor can sue one person for all the money.",
        "simple_urdu": "مشترکہ اور انفرادی ذمہ داری، جس کے تحت مدعی پوری رقم کسی ایک یا تمام فریقین سے وصول کر سکتا ہے۔",
        "important_note": "Signatories should seek 'several (proportional) liability' instead to prevent carrying the full burden of co-parties' defaults.",
        "aliases": ["Joint Liability", "Solidary Obligation"]
    },
    {
        "term": "Fiduciary Duty",
        "category": "Corporate & Authority",
        "definition": "The highest ethical and legal standard of care and utmost loyalty owed by one party (fiduciary) to another (beneficiary), such as directors to shareholders or agents to principals.",
        "simple_english": "A duty to act completely honestly and in the sole best financial and legal interest of the other party.",
        "simple_urdu": "امانت داری اور دیانت کا اعلیٰ ترین قانونی فرض جس میں فریقِ مخالف کے مفادات کو ترجیح دی جاتی ہے۔",
        "important_note": "Breaching fiduciary duty exposes individuals to personal liability and disgorgement of all illicit profits.",
        "aliases": ["Duty of Loyalty", "Duty of Care", "Trust Obligation"]
    },
    {
        "term": "Parol Evidence Rule",
        "category": "Contract Interpretation",
        "definition": "A common law rule preventing parties from introducing prior oral or written agreements to contradict, alter, or add to the terms of a finalized, integrated written contract.",
        "simple_english": "Oral promises made before signing don't count if they aren't written into the final signed agreement.",
        "simple_urdu": "زبانی شہادت کی ممانعت کا اصول، یعنی تحریری معاہدے کے خلاف پہلے کی زبانی باتوں کی سنوائی نہیں ہوتی۔",
        "important_note": "Reinforced by 'Entire Agreement' / 'Merger' clauses to prevent disputes over preliminary negotiations.",
        "aliases": ["Extrinsic Evidence Rule", "Four Corners Doctrine"]
    },
    {
        "term": "Bona Fide",
        "category": "Foundations",
        "definition": "A Latin term meaning 'in good faith'; acting honestly, openly, and without fraud, deceit, or malicious intention to gain an unfair advantage.",
        "simple_english": "Acting honestly and in genuine good faith without hidden deceit.",
        "simple_urdu": "نیک نیتی کے ساتھ، بغیر کسی فریب یا دھوکہ دہی کے عمل کرنا۔",
        "important_note": "Courts imply an underlying covenant of good faith and fair dealing in most contractual interactions.",
        "aliases": ["Good Faith", "Genuine", "Honest Dealing"]
    },
    {
        "term": "Mala Fide",
        "category": "Foundations",
        "definition": "A Latin term meaning 'in bad faith'; actions undertaken with fraudulent, dishonest, or malicious intent to deceive or harm another party.",
        "simple_english": "Acting dishonestly, deceitfully, or with deliberate bad intent.",
        "simple_urdu": "بدنیتی کے ساتھ، ارادتاً نقصان پہنچانے یا دھوکہ دینے کی نیت۔",
        "important_note": "Actions taken mala fide invalidate discretionary contractual approvals and expose parties to punitive damages.",
        "aliases": ["Bad Faith", "Deceitful Conduct", "Fraudulent Intent"]
    },
    {
        "term": "Inter Alia",
        "category": "Contract Interpretation",
        "definition": "A Latin phrase meaning 'among other things,' used in legal drafting to cite examples without creating an exhaustive or restrictive list.",
        "simple_english": "'Among other things' - indicating that the items mentioned are only examples, not the complete list.",
        "simple_urdu": "دیگر باتوں کے علاوہ؛ یہ ظاہر کرنے کے لیے کہ دی گئی مثالیں صرف نمونہ ہیں، مکمل فہرست نہیں۔",
        "important_note": "Prevents the restrictive application of the ejusdem generis rule by leaving provisions open-ended.",
        "aliases": ["Among Others", "Including Without Limitation"]
    },
    {
        "term": "Pro Rata",
        "category": "Financial",
        "definition": "A Latin term meaning 'in proportion'; calculating a financial share, expense, or distribution according to each party's respective mathematical percentage or fraction.",
        "simple_english": "Divided proportionally based on each person's exact share or portion.",
        "simple_urdu": "تناسب کے لحاظ سے، یعنی ہر فریق کے مخصوص فیصد کے مطابق تقسیم۔",
        "important_note": "Often seen in rent adjustments, insurance refunds, dividend distributions, and tax apportionments.",
        "aliases": ["Proportionately", "Prorated", "Fractional Share"]
    },
    {
        "term": "Ipso Facto",
        "category": "Contract Lifecycle",
        "definition": "A Latin phrase meaning 'by that very fact or act'; an effect that occurs automatically as a direct consequence of an event without requiring additional steps.",
        "simple_english": "Happening automatically by the very nature of the event itself.",
        "simple_urdu": "از خود، یعنی کسی واقعے کے رونما ہوتے ہی بغیر کسی دوسرے عمل کے خود بخود لاگو ہونا۔",
        "important_note": "Ipso facto bankruptcy termination clauses are often restricted or stayed by statutory insolvency laws.",
        "aliases": ["Automatically", "By the Fact Itself"]
    },
    {
        "term": "De Minimis",
        "category": "Contract Interpretation",
        "definition": "Derived from 'de minimis non curat lex' (the law does not concern itself with trifles); referring to matters too minor, trivial, or insignificant to warrant legal remedy.",
        "simple_english": "Too small, minor, or trivial to be worth taking to court.",
        "simple_urdu": "معمولی یا جزوی نوعیت کی چیز جس پر قانون عام طور پر توجہ نہیں دیتا۔",
        "important_note": "Contracts often set a minimum financial basket (e.g. $5,000) before indemnification claims can be launched.",
        "aliases": ["Trivial Matter", "Insignificant Variation"]
    },
    {
        "term": "Mutatis Mutandis",
        "category": "Contract Interpretation",
        "definition": "A Latin drafting term meaning 'with the necessary changes having been made,' applying existing rules or clauses to a new context with relevant factual adaptations.",
        "simple_english": "Applying the same rules with the necessary minor details changed to fit the new situation.",
        "simple_urdu": "ضروری ترامیم کے ساتھ، یعنی پرانے اصولوں کو نئی صورتحال پر ضروری ردوبدل کر کے لاگو کرنا۔",
        "important_note": "Saves repetitive drafting when extending schedules, appendices, or subsequent work orders.",
        "aliases": ["With Necessary Adaptations", "Correspondingly"]
    },
    {
        "term": "Sine Qua Non",
        "category": "Foundations",
        "definition": "An indispensable and essential condition, element, or prerequisite without which a contract, transaction, or outcome cannot exist.",
        "simple_english": "An absolute must-have condition without which the entire deal cannot move forward.",
        "simple_urdu": "لازمی اور ناگزیر شرط جس کے بغیر کوئی معاملہ یا معاہدہ قائم نہیں ہو سکتا۔",
        "important_note": "In breach and negligence, the 'but-for' test determines if an action was the sine qua non of the loss.",
        "aliases": ["Indispensable Condition", "Absolute Prerequisite"]
    },
    {
        "term": "Clean Hands Doctrine",
        "category": "Foundations",
        "definition": "An equitable legal maxim stating that a party who seeks equitable relief or remedies from the court must not have acted unethically, deceitfully, or unlawfully in the same matter.",
        "simple_english": "You cannot ask the court for fairness if you behaved unfairly or dishonestly in the transaction.",
        "simple_urdu": "صاف ہاتھوں کا اصول، یعنی عدالتی ریلیف مانگنے والے کو خود بے داغ اور دیانت دار ہونا چاہیے۔",
        "important_note": "A defendant can defeat an injunction claim by proving the claimant also acted unfairly.",
        "aliases": ["Doctrine of Clean Hands", "Equitable Integrity"]
    },
    {
        "term": "Indemnitor & Indemnitee",
        "category": "Risk Allocation & Insurance",
        "definition": "The 'Indemnitor' is the party who promises to protect, defend, and pay damages; the 'Indemnitee' is the party receiving this protection against third-party claims.",
        "simple_english": "Indemnitor = the payer/shield; Indemnitee = the protected party receiving reimbursement.",
        "simple_urdu": "ضامن (نقصان کا ازالہ کرنے والا) اور مضموم لہ (جس کے نقصان کا تحفظ کیا جا رہا ہو)۔",
        "important_note": "Check which party carries the indemnitor role and whether defense costs (attorneys' fees) are included.",
        "aliases": ["Shielding Party & Protected Party", "Indemnifying Party"]
    },
    {
        "term": "Power of Attorney",
        "category": "Corporate & Authority",
        "definition": "A formal written legal deed by which a person (principal) appoints another (agent or attorney-in-fact) to manage their property, finances, or legal affairs.",
        "simple_english": "A legal document giving someone the formal power to sign documents and make decisions on your behalf.",
        "simple_urdu": "مختار نامہ، یعنی قانونی دستاویز جس کے ذریعے کوئی شخص اپنے معاملات کسی دوسرے کے سپرد کرتا ہے۔",
        "important_note": "A General Power of Attorney grants broad discretion; a Special Power of Attorney strictly limits acts to specific property or courts.",
        "aliases": ["Mukhtar Nama", "Letter of Attorney", "Mandate"]
    },
    {
        "term": "Equitable Relief",
        "category": "Remedies & Damages",
        "definition": "Non-monetary court remedies (such as injunctions, specific performance, or rescission) awarded when financial compensation is insufficient to right the wrong.",
        "simple_english": "Court remedies that order someone to do or stop something, rather than just handing over cash.",
        "simple_urdu": "منصفانہ عدالتی ریلیف، جو محض مالی معاوضے کے بجائے کسی عمل کو روکنے یا نافذ کرنے پر مبنی ہو۔",
        "important_note": "Confidentiality agreements routinely state that breach causes irreparable harm entitling the owner to equitable relief.",
        "aliases": ["Equitable Remedy", "Non-monetary Relief"]
    }
]

# -------------------------------------------------------------
# 2. EXPAND COMMON CLAUSES
# -------------------------------------------------------------
NEW_COMMON_CLAUSES = [
    {
        "clause": "Audit and Inspection Rights",
        "category": "Compliance & Operational",
        "meaning": "Grants one party (e.g. client, licensor, or regulator) the legal right to inspect financial books, operational records, and facilities of the other party to ensure compliance.",
        "simple_english": "Allows the other party to check your books, invoices, or premises to make sure you are following the rules.",
        "simple_urdu": "حسابات اور دفاتر کی تفتیش و آڈٹ کا حق تاکہ معاہدے کی پاسداری کی جانچ کی جا سکے۔",
        "what_to_look_for": "Check frequency limits (e.g. once per year during normal business hours), advance notice requirements, and who pays the audit costs if no discrepancies are discovered."
    },
    {
        "clause": "Non-Disparagement",
        "category": "Restrictive Covenants",
        "meaning": "Prohibits parties from making negative, derogatory, or defamatory statements (verbally, in print, or online) about the other party, its management, or its products.",
        "simple_english": "A mutual promise not to badmouth, criticize, or post damaging public comments about each other.",
        "simple_urdu": "ایک دوسرے کی ساکھ کو نقصان نہ پہنچانے یا عوامی سطح پر برائی نہ کرنے کا پابند معاہدہ۔",
        "what_to_look_for": "Ensure the clause is strictly mutual (protecting both sides) and explicitly excludes truthful disclosures mandated by legal subpoenas or court testimony."
    },
    {
        "clause": "Equitable Relief and Injunctions",
        "category": "Remedies",
        "meaning": "Stipulates that monetary damages would be inadequate to remedy a breach of confidentiality, IP, or restrictive covenants, granting immediate access to emergency court injunctions.",
        "simple_english": "Agrees in advance that if secrets or IP are stolen, money isn't enough and a court can order an immediate halt.",
        "simple_urdu": "اس امر کا اقرار کہ خلاف ورزی کی صورت میں مالی معاوضہ کافی نہیں ہوگا بلکہ فوری حکمِ امتناعی حاصل کیا جا سکتا ہے۔",
        "what_to_look_for": "Look out for clauses that waive the requirement to post an injunction bond or waive your right to contest the emergency order."
    },
    {
        "clause": "Cumulative Remedies",
        "category": "Remedies",
        "meaning": "Provides that rights and legal remedies specified in the contract are additive and do not preclude or replace any other remedies available under general law or equity.",
        "simple_english": "Means using one legal remedy does not stop the party from pursuing all other legal options available.",
        "simple_urdu": "مجموعی قانونی چارہ جوئی کا حق، یعنی ایک حق استعمال کرنے سے دیگر قانونی راستے بند نہیں ہوتے۔",
        "what_to_look_for": "Check whether this conflicts with explicit exclusive remedy clauses (e.g., where liquidated damages or warranty repairs are agreed to be the sole remedy)."
    },
    {
        "clause": "Counterparts and Electronic Signatures",
        "category": "Execution",
        "meaning": "Allows the agreement to be signed in multiple identical copies, by separate parties at different times and locations, and affirms legal validity of digital/electronic signatures.",
        "simple_english": "Both sides don't need to be in the same room or use the same physical sheet; DocuSign or scanned copies are 100% legally binding.",
        "simple_urdu": "الگ الگ کاپیوں پر اور الیکٹرانک / ڈیجیٹل دستخطوں کی قانونی حیثیت کی باضابطہ منظوری۔",
        "what_to_look_for": "Ensure digital signature platforms comply with applicable Electronic Transactions Acts or local registry requirements."
    },
    {
        "clause": "Successors and Assigns",
        "category": "Lifecycle & Parties",
        "meaning": "Extends the binding obligations and benefits of the agreement to future heirs, corporate acquirers, executors, and permitted legal assignees of each party.",
        "simple_english": "The contract remains valid and binding on whoever takes over the company or inherits the assets in the future.",
        "simple_urdu": "معاہدے کی پابندی مستقبل میں آنے والے قانونی وارثوں، جانشینوں اور خریداروں پر بھی لاگو ہوگی۔",
        "what_to_look_for": "Verify that this clause does not inadvertently permit unapproved transfers without adhering to the explicit Assignment clause."
    },
    {
        "clause": "Liquidated Damages",
        "category": "Remedies",
        "meaning": "Fixes a predetermined monetary sum payable as compensation upon a specific contractual breach (such as daily penalties for delayed delivery).",
        "simple_english": "A predetermined penalty amount to be paid for every day or event of delay or default.",
        "simple_urdu": "معاہدے میں پہلے سے مقرر کردہ ہرجانہ جو تاخیر یا خلاف ورزی کی صورت میں ادا کرنا لازم ہوگا۔",
        "what_to_look_for": "Ensure there is a reasonable overall cap on liquidated damages (e.g. max 10% of total contract value) to avoid crippling financial exposure."
    },
    {
        "clause": "Time of the Essence",
        "category": "Performance",
        "meaning": "Declares that strict adherence to stated performance dates and deadlines is a fundamental condition, making any minor delay an immediate material breach.",
        "simple_english": "Deadlines are non-negotiable; missing a date by even one day is treated as a major contract breach.",
        "simple_urdu": "وقت کی پابندی انتہائی بنیادی شرط ہے؛ معمولی تاخیر بھی سنگین خلاف ورزی تصور ہوگی۔",
        "what_to_look_for": "If you are the service provider, avoid this clause or ensure reasonable cure periods and force majeure exclusions apply."
    },
    {
        "clause": "Further Assurances",
        "category": "Cooperation",
        "meaning": "Obligates both parties to sign any additional legal documents, certificates, or execute further steps reasonably necessary to give full effect to the agreement.",
        "simple_english": "Both parties agree to cooperate and sign any extra paperwork needed to finalize the deal later.",
        "simple_urdu": "معاہدے کے مقاصد کو پورا کرنے کے لیے مستقبل میں مزید ضروری دستاویزات پر دستخط کرنے کی یقین دہانی۔",
        "what_to_look_for": "Specify that such further acts must be at the requesting party's reasonable expense."
    },
    {
        "clause": "Anti-Bribery and Anti-Corruption",
        "category": "Compliance & Operational",
        "meaning": "Requires strict compliance with anti-graft laws (such as the UK Bribery Act, US FCPA, or local anti-corruption statutes), forbidding illicit kickbacks or bribes.",
        "simple_english": "A strict prohibition against paying bribes, kickbacks, or gifts to public officials or corporate decision-makers.",
        "simple_urdu": "رشوت ستانی اور غیر قانونی کمیشن کے خلاف سخت پابندی کا بین الاقوامی قانونی تقاضا۔",
        "what_to_look_for": "Look out for immediate termination rights triggered upon mere investigation or unproven allegation."
    },
    {
        "clause": "Change of Control",
        "category": "Lifecycle & Parties",
        "meaning": "Dictates what happens if a contracting party is acquired, merged, sold, or undergoes a majority ownership change, often granting the other party an exit right.",
        "simple_english": "Explains what happens if your company is sold or taken over by a new owner or competitor.",
        "simple_urdu": "کمپنی کی ملکیت یا انتظام تبدیل ہونے کی صورت میں معاہدے پر اثرات اور فریق ثانی کا حقِ تنسیخ۔",
        "what_to_look_for": "Check if a corporate restructuring or venture funding round unintentionally triggers a right for clients to walk away."
    },
    {
        "clause": "Set-Off Rights",
        "category": "Commercial",
        "meaning": "Allows a party to deduct any monies, damages, or claims owed to them from the amounts they owe to the other party under the contract.",
        "simple_english": "The right to deduct money you are owed from the bills you have to pay the other party.",
        "simple_urdu": "رقم کا باہمی کٹاؤ، یعنی اپنے واجب الادا بلوں میں سے مطلوبہ ہرجانہ یا قرض کاٹ کر بقایا ادا کرنا۔",
        "what_to_look_for": "Service providers should insist on 'no set-off' clauses to prevent clients from withholding fees over disputed collateral claims."
    },
    {
        "clause": "No Third-Party Beneficiaries",
        "category": "Foundations",
        "meaning": "Confirms that the contract is solely for the benefit of the signing parties and no outside third party acquires any rights to enforce any provision.",
        "simple_english": "Only the actual people or companies signing have legal rights; outside strangers cannot enforce this agreement.",
        "simple_urdu": "تیسرے فریق کا حق نہ ہونا؛ معاہدے کے حقوق صرف اصل دستخط کنندگان تک محدود ہیں۔",
        "what_to_look_for": "Ensure affiliates, officers, or indemnitees are explicitly carved out if they need direct protection."
    },
    {
        "clause": "Export Control and Sanctions Compliance",
        "category": "Compliance & Operational",
        "meaning": "Prohibits the export, re-export, transfer, or provision of services/software to sanctioned countries, prohibited entities, or individuals on governmental embargo lists.",
        "simple_english": "Rules forbidding the transfer of goods, tech, or funds to sanctioned nations or banned organizations.",
        "simple_urdu": "بین الاقوامی تجارتی پابندیوں اور برآمدی ضوابط کی مکمل پابندی کا عہد۔",
        "what_to_look_for": "Ensure compliance representations are limited to applicable laws of relevant jurisdictions."
    },
    {
        "clause": "Relationship of the Parties (Independent Contractor)",
        "category": "Foundations",
        "meaning": "Affirms that the parties are independent contractors and nothing creates a legal partnership, joint venture, agency, or employment relationship.",
        "simple_english": "Clarifies that you are an independent contractor, not an employee, business partner, or legal agent.",
        "simple_urdu": "فریقین کی خودمختار حیثیت کی توثیق کہ کوئی ملازمتی یا باہمی شراکت داری کا رشتہ وجود میں نہیں آیا۔",
        "what_to_look_for": "Critical to shield against vicarious tort liability and statutory employment benefit claims."
    },
    {
        "clause": "Severability and Judicial Reformation",
        "category": "Interpretation & Boilerplate",
        "meaning": "Provides that if any clause is found invalid or unlawful, the court is authorized to modify ('blue-pencil') it to the minimum extent necessary to make it lawful and preserve the remainder.",
        "simple_english": "If a judge invalidates one sentence, the rest of the contract stays alive, and the judge may rewrite that part to make it legal.",
        "simple_urdu": "ناجائز شق کا اخراج اور عدالتی ترمیم تاکہ باقی تمام معاہدہ مکمل طور پر نافذ العمل رہے۔",
        "what_to_look_for": "Verify whether an essential clause (like payment or IP) being voided entitles either party to terminate."
    },
    {
        "clause": "Force Majeure Mitigation and Notice",
        "category": "Risk Allocation & Exceptions",
        "meaning": "Sets explicit deadlines (e.g. within 5 business days) for notifying the other party of an uncontrollable event and mandates continuous good-faith efforts to mitigate delays.",
        "simple_english": "If an act of God halts work, you must notify the client quickly in writing and take all reasonable steps to resume soon.",
        "simple_urdu": "ناگہانی آفات کی فوری تحریری اطلاع اور نقصان کو کم سے کم کرنے کے عملی اقدامات کی شرط۔",
        "what_to_look_for": "Check how many days of continuous force majeure (e.g. 60 or 90 days) permits either party to cancel without penalty."
    }
]

# -------------------------------------------------------------
# 3. EXPAND GOVERNMENT & LEGAL FORMS
# -------------------------------------------------------------
NEW_GOVERNMENT_FORMS = [
    {
        "form_type": "Residential / Commercial Tenancy Agreement (Lease / Kirayanama)",
        "purpose": "A legal contract granting occupancy of real property by a landlord to a tenant for a specified duration in exchange for periodic rent payments.",
        "common_fields": [
            {
                "field_name": "Lessor / Landlord Details",
                "description": "Full legal name, CNIC/Passport, and ownership proof of the property owner.",
                "simple_urdu": "مالک مکان یا جائیداد کے مالک کا مکمل نام اور شناختی کوائف۔"
            },
            {
                "field_name": "Lessee / Tenant Details",
                "description": "Full legal name, national identity number, and permanent address of the tenant.",
                "simple_urdu": "کرایہ دار کا مکمل قانونی نام اور مستقل پتہ۔"
            },
            {
                "field_name": "Premises Schedule & Description",
                "description": "Complete physical address, plot number, covered area, and fixtures included in the tenancy.",
                "simple_urdu": "کرائے پر دی جانے والی جائیداد کا مکمل پتہ اور حدودِ اربعہ۔"
            },
            {
                "field_name": "Monthly Rent & Escalation Rate",
                "description": "Agreed monthly rental amount, due date (e.g. 5th of each month), and annual percentage increase (typically 10%).",
                "simple_urdu": "ماہانہ کرایہ، تاریخِ ادائیگی اور سالانہ اضافے کی شرح (جیسے دس فیصد)۔"
            },
            {
                "field_name": "Security Deposit / Advance Rent",
                "description": "Refundable security deposit amount held against damage or unpaid utility bills.",
                "simple_urdu": "زرِ ضمانت (سیکیورٹی ڈپازٹ) جو معاہدے کے خاتمے پر قابلِ واپسی ہوگی۔"
            },
            {
                "field_name": "Maintenance & Utility Responsibilities",
                "description": "Allocation of structural repairs to landlord vs day-to-day minor repairs and utilities to tenant.",
                "simple_urdu": "بجلی، گیس، پانی کے بلوں اور عمارت کی مرمت کی ذمہ داریوں کی تقسیم۔"
            }
        ],
        "typical_supporting_docs": [
            "Original or Certified Copy of Title Deed / Registry / Allotment Letter",
            "Valid CNIC copies of Landlord, Tenant, and two respectable witnesses",
            "Police Station Tenant Verification Form / Clearance Certificate",
            "Prescribed Stamp Paper of appropriate value according to the Stamp Act"
        ],
        "important_notes": "Under Tenancy Acts, registration of the tenancy agreement with the local Rent Tribunal or Rent Registrar is legally mandatory for enforcement of summary eviction procedures."
    },
    {
        "form_type": "SECP Form 29 (Particulars of Directors, Officers & Auditors)",
        "purpose": "Statutory corporate return filed with the Securities and Exchange Commission notifying appointments, resignations, or changes of corporate directors and officers.",
        "common_fields": [
            {
                "field_name": "Corporate Universal Identification Number (CUIN)",
                "description": "Official company registration number assigned by the corporate registry.",
                "simple_urdu": "کمپنی کا کارپوریٹ رجسٹریشن نمبر۔"
            },
            {
                "field_name": "Full Legal Name of the Company",
                "description": "Exact name of the registered corporate entity as stated on the Certificate of Incorporation.",
                "simple_urdu": "کمپنی کا باضابطہ رجسٹرڈ نام۔"
            },
            {
                "field_name": "Name & CNIC/Passport of Appointee/Outgoing Officer",
                "description": "Identity and nationality details of the incoming or resigning director/CEO.",
                "simple_urdu": "عہدے پر فائز ہونے والے یا مستعفی ڈائریکٹر یا چیف ایگزیکٹو کا نام اور شناختی نمبر۔"
            },
            {
                "field_name": "Date of Appointment / Cessation",
                "description": "Exact calendar date when the appointment took effect or resignation was accepted.",
                "simple_urdu": "تقرری یا استعفے کی حتمی تاریخ۔"
            },
            {
                "field_name": "Mode of Change / Board Resolution Reference",
                "description": "Reference to Board of Directors resolution or AGM election approving the change.",
                "simple_urdu": "بورڈ کی قرارداد یا اجلاس کا حوالہ جس میں یہ فیصلہ منظور ہوا۔"
            }
        ],
        "typical_supporting_docs": [
            "Certified Copy of Board Resolution or AGM Minutes",
            "Consent to Act as Director (Form 28)",
            "CNIC/Passport copy of the new Director",
            "Official payment receipt of SECP filing fees"
        ],
        "important_notes": "Statutory corporate laws mandate filing Form 29 within 14 to 15 days of any change in the board of directors; late filings attract statutory penal surcharges."
    },
    {
        "form_type": "Deed of Sale of Immovable Property (Sale Deed / Bayanama)",
        "purpose": "A registered deed effecting the absolute and irrevocable legal transfer of ownership of real estate from seller to buyer for valuable consideration.",
        "common_fields": [
            {
                "field_name": "Vendor / Seller Details",
                "description": "Full name, parentage, CNIC, and current residential address of the lawful titleholder.",
                "simple_urdu": "فروخت کنندہ (بائع) کا مکمل نام، ولدیت اور شناختی کارڈ نمبر۔"
            },
            {
                "field_name": "Vendee / Purchaser Details",
                "description": "Full name, parentage, CNIC, and permanent address of the incoming buyer.",
                "simple_urdu": "خریدار (مشتری) کا مکمل نام، ولدیت اور قومی شناختی نمبر۔"
            },
            {
                "field_name": "Property Schedule & Four Boundaries",
                "description": "Exact demarcations: North, South, East, West boundaries, Khasra/Plot number, and registry records.",
                "simple_urdu": "جائیداد کے حدودِ اربعہ، خسرہ یا پلاٹ نمبر اور رقبے کی تفصیل۔"
            },
            {
                "field_name": "Total Sale Consideration & Payment Receipt",
                "description": "The exact monetary price paid, pay-order/bank cheque numbers, and full acknowledgment of receipt.",
                "simple_urdu": "فروخت کی کل رقم، پے آرڈر یا بینک چیک کی تفصیل اور وصولی کی تصدیق۔"
            },
            {
                "field_name": "Clear Title & Indemnity Warranty",
                "description": "Seller's sworn covenant that the property is free from all mortgages, liens, disputes, or tax claims.",
                "simple_urdu": "مالک کی طرف سے ضمانت کہ جائیداد ہر قسم کے تنازعے اور قرض سے پاک ہے۔"
            }
        ],
        "typical_supporting_docs": [
            "Fard Malkiat / Ownership Mutation Certificate from Revenue Office",
            "No Objection Certificate (NOC) from Housing Authority or Municipal Council",
            "E-Stamp Paper of requisite value based on DC valuation table",
            "Tax payment receipts (Section 236K / 236C withholding tax)",
            "Two adult male witnesses with original CNICs"
        ],
        "important_notes": "A Sale Deed of immovable property worth over Rs. 100 must be compulsorily registered before the Sub-Registrar under the Registration Act to convey legal title."
    },
    {
        "form_type": "Partnership Deed (Form A / Form B Registration)",
        "purpose": "A founding constitutional deed between two or more partners establishing rights, profit-sharing ratios, capital contributions, and operational rules of a partnership firm.",
        "common_fields": [
            {
                "field_name": "Firm Legal Name & Principal Office",
                "description": "The trade name under which business is conducted and the headquarters address.",
                "simple_urdu": "شراکت داری فرم کا تجارتی نام اور مرکزی دفتر کا پتہ۔"
            },
            {
                "field_name": "Nature and Scope of Business",
                "description": "Specific commercial activities and services authorized under the partnership.",
                "simple_urdu": "کاروبار اور تجارتی سرگرمیوں کی نوعیت۔"
            },
            {
                "field_name": "Capital Contribution Ratio",
                "description": "Amount of money, property, or equipment invested by each individual partner.",
                "simple_urdu": "ہر شریک کا لگایا گیا سرمایہ اور اس کی مالی شرح۔"
            },
            {
                "field_name": "Profit and Loss Sharing Percentage",
                "description": "The exact contractual percentage for distribution of net profits and absorption of financial losses.",
                "simple_urdu": "نفع اور نقصان کی باہمی تقسیم کا تناسب۔"
            },
            {
                "field_name": "Bank Operations & Signatory Authority",
                "description": "Specification whether bank accounts require joint signatures or sole partner operations.",
                "simple_urdu": "بینک اکاؤنٹس چلانے اور دستخط کرنے کا اختیار۔"
            },
            {
                "field_name": "Dissolution & Retirement Procedures",
                "description": "Rules for goodwill valuation, accounts settlement, and dissolution notices.",
                "simple_urdu": "فرم کے خاتمے یا کسی شریک کی علیحدگی کی صورت میں حساب کتاب کا طریقہ کار۔"
            }
        ],
        "typical_supporting_docs": [
            "Non-judicial stamp paper of prescribed state stamp duty value",
            "Attested CNIC copies of all partners and witnesses",
            "Rent agreement or ownership proof of principal commercial premises",
            "Form I registration application submitted to the Registrar of Firms"
        ],
        "important_notes": "Unregistered partnership firms are legally barred under the Partnership Act from filing lawsuits in court to enforce contractual claims against third parties."
    },
    {
        "form_type": "Employment Agreement / Letter of Appointment",
        "purpose": "A legally binding contract between an employer and employee defining job duties, compensation, benefits, termination rules, and confidentiality.",
        "common_fields": [
            {
                "field_name": "Job Title & Reporting Line",
                "description": "Official designation and direct managerial reporting line.",
                "simple_urdu": "ملازمت کا عہدہ اور ڈائریکٹ رپورٹنگ مینیجر۔"
            },
            {
                "field_name": "Gross Salary & Allowances",
                "description": "Detailed compensation breakdown: basic salary, house rent, medical allowance, and bonuses.",
                "simple_urdu": "تنخواہ، الاؤنسز اور دیگر مالی مراعات کی تفصیل۔"
            },
            {
                "field_name": "Probationary Period",
                "description": "Initial evaluation duration (typically 3 to 6 months) during which termination requires shorter notice.",
                "simple_urdu": "آزمائشی مدت (پروبیشن پیریڈ) جس میں کارکردگی کا جائزہ لیا جاتا ہے۔"
            },
            {
                "field_name": "Termination Notice & Severance",
                "description": "Required written notice period (e.g. 30 days) or payment of salary in lieu of notice.",
                "simple_urdu": "ملازمت ختم کرنے کا تحریری نوٹس پیریڈ یا اس کے بدلے تنخواہ کی ادائیگی۔"
            },
            {
                "field_name": "Intellectual Property Assignment",
                "description": "Clause vesting full ownership of all patents, software, designs, and code created on the job into the employer.",
                "simple_urdu": "دورانِ ملازمت تخلیق کردہ تمام سافٹ ویئر اور ایجادات کے حقوق کمپنی کو سونپنا۔"
            }
        ],
        "typical_supporting_docs": [
            "Educational degrees and professional qualification certificates",
            "Previous employer relieving certificate / experience letters",
            "CNIC copy and criminal background verification"
        ],
        "important_notes": "Statutory labor and employment laws supersede contractual terms that fall below minimum wage, maximum working hours, or statutory leave entitlements."
    }
]

def expand_file(filename, new_items, key_name):
    filepath = os.path.join(KB_DIR, filename)
    with open(filepath, "r", encoding="utf-8") as f:
        existing = json.load(f)
    
    existing_keys = {item[key_name].strip().lower() for item in existing}
    added_count = 0
    
    for item in new_items:
        val = item[key_name].strip().lower()
        if val not in existing_keys:
            existing.append(item)
            existing_keys.add(val)
            added_count += 1
            
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(existing, f, ensure_ascii=False, indent=2)
        
    print(f"{filename}: Added {added_count} items. Total now: {len(existing)}")

if __name__ == "__main__":
    expand_file("legal_terms.json", NEW_LEGAL_TERMS, "term")
    expand_file("common_clauses.json", NEW_COMMON_CLAUSES, "clause")
    expand_file("government_forms.json", NEW_GOVERNMENT_FORMS, "form_type")
