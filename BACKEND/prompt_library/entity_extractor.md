Enhanced Prompt for Legal Entity Extraction

Task:
Extract entities from legal or regulatory text. Focus on identifying and categorizing terms into the following types:

- Authority: Supervisory bodies, regulators, courts, tribunals
- Regulation: Specific rules, directives, GDPR articles, national laws
- Role: Positions such as Data Protection Officer, Controller, Processor
- Designation: Official titles or appointments
- Member_State: Countries within the EU or other legal unions
- Organization: Companies, institutions, agencies
- Guiding-Principle: Fairness, transparency, accountability
- Case_Study: Real-world examples or precedents
- Principle: Core doctrines like proportionality, necessity
- LawfulBasis: Consent, contract, legitimate interest, public interest
- Right: Access, rectification, erasure, portability
- ComplianceSet: Bundled obligations or frameworks
- ComplianceRequirement: Specific duties like DPIA, breach notification
- Actor: Any party involved (controller, processor, subject, authority)

Instructions for Extraction:

1. Identify explicit mentions of the above categories.
2. Capture implicit references (e.g., “employment contract” → LawfulBasis: Contract).
3. Maintain legal precision — avoid overgeneralization.
4. Output should be structured (e.g., JSON or dict) with entity type and extracted value.

### Output Requirements

- Always return a JSON array.
- Each element must be an object with exactly two fields:
  - "type": the category of the entity (e.g., Regulation, Role, LawfulBasis, Right, Obligation, Document).
  - "value": the extracted text span or normalized name of the entity.
- Do not include any text outside the JSON array.
- If no entities are found, return an empty array: []

### Example Output

[
{
"type": "Regulation",
"value": "GDPR"
},
{
"type": "Role",
"value": "Data Controller"
}
]
