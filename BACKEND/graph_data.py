###############################################


nodes = [
    {
        "id": "Gdpr",
        "type": "Regulation",
        "properties": {
            "name": "General Data Protection Regulation",
            "date_enforced": "2018-05-25",
            "impact": "Defines how personal data is collected, processed, kept safe, compliance guaranteed, liability, and rights of citizens.",
        },
    },
    {
        "id": "Data Controller",
        "type": "Role",
        "properties": {
            "name": "Data Controller",
            "description": """In general terms, the data controller is the natural or legal person (could be a company
            or a non-profit organisation), public authority, agency or other body which, alone or
            jointly with others, determines the purposes, conditions and means of processing personal data.
        """,
            "responsibility": "Owns the data, sets rules for collection and processing, and keeps records of all processing activities.",
        },
    },
    {
        "id": "UK Supervisory Authority",
        "type": "Authority",
        "properties": {
            "name": "UK Data Protection Authority",
            "country": "United Kingdom",
            "position": """States that employees of a data controller cannot be considered processors.
            However, if the same processing activities would be outsourced (e.g. to an external consultant),
            this external party would be considered a data processor.
        """,
        },
    },
    {
        "id": "Data Processor",
        "type": "Role",
        "properties": {
            "name": "Data Processor",
            "description": "Entity designated by the controller to collect and process data on its behalf.",
        },
    },
    {
        "id": "Data Protection Officer",
        "type": "Role",
        "properties": {
            "name": "Data Protection Officer",
            "description": """
Ensures compliance with GDPR rules and advises the organization.
It has to be designated on the basis of professional qualities
and knowledge of data protection law and practices.
""",
            "responsibility": """
· inform and advise the employees of the data controller or processor
on their obligations arising from the GDPR and any other national data protection rules;
· monitor compliance with the data protection legislation;
· check if the responsibilities of the controller and processor have correctly been assigned,
and if awareness-raising and sufficient training for staff have taken place;
· provide advice on the data protection impact assessment and monitor its performance;
· cooperate with the supervisory authority, and to act as a contact person for them;
· be available for inquiries from data subjects (individuals whose data the controller possesses),
for issues of data processing or where individuals want to make use of one of their rights.
""",
            "accessibility": """
Data protection officers can work for several organisations as long as they remain easily accessible.
""",
            "status_and_rights": """
Furthermore, they can be a member of the staff or fulfil their tasks on the basis of a service contract.
DPOs also enjoy specific rights such as to have sufficient resources to fulfil the tasks assigned to them.
They also have the right of access to the entities’ data processing personnel and operations and to training
in order to maintain their expert knowledge. Moreover, data protection officers should have significant
independence in carrying out their tasks and reporting to the highest management level. They can also fulfil
other tasks as long as there is no conflict of interest with their role as DPO. Many of the tasks that are
assigned to the data controller (e.g. documenting processing activities etc.) can hence also be assumed by
the DPO. Lastly, DPOs enjoy a high level of job security. They cannot be fired, nor can penalties be imposed
on the ground of performing their responsibilities as a DPO. There is no length of tenure for this position.
""",
        },
    },
    {
        "id": "Germany",
        "type": "MemberState",
        "properties": {
            "name": "Germany",
            "rule": "Requires appointment of a DPO if more than 10 people are constantly involved in automatic processing of data.",
        },
    },
    {
        "id": "Public Authority",
        "type": "Organization",
        "properties": {
            "name": "Public Authority",
            "description": "Entity whose processing activities require appointment of a DPO.",
            "implication": "Faces financial and staff implications when appointing a DPO.",
        },
    },
    {
        "id": "Guiding Principles",
        "type": "PrincipleSet",
        "properties": {
            "name": "GDPR Guiding Principles",
            "description": "Seven principles that govern how personal data can be collected and processed under GDPR.",
            "principles": """
                "Lawfulness, fairness and transparency",
                "Purpose limitation",
                "Data minimisation",
                "Accuracy",
                "Storage limitation",
                "Integrity and confidentiality",
                "Accountability",
            """
        },
    },
    {
        "id": "Barbulescu v Romania",
        "type": "CaseLaw",
        "properties": {
            "name": "Bărbulescu v. Romania",
            "description": "Case demonstrating employees can rely on GDPR principles when privacy is violated.",
        },
    },
    {
        "id": "Lawfulness, Fairness and Transparency",
        "type": "Principle",
        "properties": {
            "name": "Lawfulness, Fairness and Transparency",
            "details": """
Data collection must be based on a legal basis (consent, public interest, legitimate interests).
Fairness requires handling data in a way people expect to be reasonable, without deception.
Transparency requires clear communication about what data is collected, for what purpose,
for whom, and for how long, in plain and understandable language.
"""
        },
    },
    {
        "id": "Purpose Limitation",
        "type": "Principle",
        "properties": {
            "name": "Purpose Limitation",
"details": """
Personal data must be collected for specified, explicit, and legitimate purposes
and cannot be processed in ways incompatible with those purposes.
In employment, the controller must specify the purpose for collecting employee data.
Data may be reused for compatible purposes (e.g., archiving in the public interest,
scientific or historical research, statistical purposes) if the data subject consents
or if a new legal provision requires or allows it.
"""        },
    },
    {
        "id": "Data Minimisation",
        "type": "Principle",
        "properties": {
            "name": "Data Minimisation",
"details": """
Personal data must be adequate, relevant, and limited to what is necessary.
The minimum amount of data required for processing should be identified before collection.
Data must have a clear link to the purpose and only be collected to fulfil that purpose.
Example: collecting blood type for employees in hazardous work may be justified for health and safety,
but collecting it for non-hazardous employees would breach this principle.
"""
        },
    },
    {
        "id": "Accuracy",
        "type": "Principle",
        "properties": {
            "name": "Accuracy",
 "details": """
Personal data must be accurate and kept up to date.
The data controller has an obligation to proactively ensure accuracy
and rectify or delete inaccurate, incorrect, or misleading data without delay.
Controllers may rely on data subject requests (e.g., updating an address)
or must update records when circumstances change (e.g., payroll records after a pay rise).
"""
        },
    },
    {
        "id": "Storage Limitation",
        "type": "Principle",
        "properties": {
            "name": "Storage Limitation",
            "details": """
Personal data must be kept only for a determined period and no longer than necessary.
When the purpose for retaining data is no longer relevant or the data becomes outdated,
it should be deleted or anonymised.
This principle prevents data from becoming irrelevant, excessive, inaccurate, or outdated,
and encourages controllers to set clear retention policies.
"""
        },
    },
    {
        "id": "Integrity and Confidentiality",
        "type": "Principle",
        "properties": {
            "name": "Integrity and Confidentiality",
"details": """
Personal data must be kept secure.
Appropriate measures must be taken to protect against unauthorised or unlawful processing,
and against accidental loss, destruction, or damage.
This principle requires controllers to implement strong data security safeguards.
"""
        },
    },
    {
        "id": "Accountability",
        "type": "Principle",
        "properties": {
            "name": "Accountability",
            "details": """
The data controller is responsible and accountable for compliance with GDPR.
Controllers must put in place all necessary measures, such as implementing a privacy management framework, to demonstrate and ensure compliance.
"""
        },
    },
    {
        "id": "Lawful Basis and Limits to Processing",
        "type": "PrincipleSet",
        "properties": {
            "name": "Lawful Basis and Limits to Processing Personal Data",
            "details": """
Processing of personal data must be based on one of the lawful grounds defined by GDPR. 
These include: Consent of the data subject, Performance of a contract, Compliance with a legal obligation, Protection of vital interests, Legitimate interests, Processing of special categories of data, Processing of data on criminal offences, and Processing in the context of employment.
"""
        },
    },
    {
        "id": "Consent of the Data Subject",
        "type": "LawfulBasis",
        "properties": {
            "name": "Consent of the Data Subject",
            "details": """
Consent allows a controller to process personal data for one or more specific purposes. 
It must be easy to give and withdraw, clearly distinguishable from other matters, and presented in plain language. 
Active consent (e.g., ticking a box) is valid, but pre-ticked boxes are not. Consent forms must specify if third parties may process the data and highlight the right to withdraw at any time. 
Evidence of consent must be kept. Consent must be freely given—making it a precondition for services is coercion and a breach. In employment or public service contexts, consent is discouraged due to power imbalances. 
Explicit consent is required for processing special categories of data, data transfers without safeguards, and automated decision-making or profiling.
"""
        },
    },
    {
        "id": "Performance of a Contract",
        "type": "LawfulBasis",
        "properties": {
            "name": "Performance of a Contract",
    "details": """
Processing is lawful if necessary to fulfil the purposes of a contract
or to take preliminary steps requested by the data subject before entering into a contract.
For example, providing a quote requires processing data without needing consent.
The contractual basis does not need to be in written form.
"""        },
    },
    {
        "id": "Compliance with a Legal Obligation",
        "type": "LawfulBasis",
        "properties": {
            "name": "Compliance with a Legal Obligation",
            "details": "Processing is lawful if necessary to comply with a legal obligation under national or EU law, and consent is not required. For example, an employer may be obliged to collect employee data for the national tax authority. In such cases, the controller must document the legal basis, and referring to an official government site explaining the obligation is considered sufficient proof.",
        },
    },
    {
        "id": "Protection of Vital Interests",
        "type": "LawfulBasis",
        "properties": {
            "name": "Protection of Vital Interests",
            "details": "Processing is lawful when necessary to protect the life of a person. This applies particularly to emergency services, where medical records may be needed to safeguard vital interests. However, if the person is able to provide consent, vital interests cannot be used as the legal basis for processing.",
        },
    },
    {
        "id": "Legitimate Interest",
        "type": "LawfulBasis",
        "properties": {
            "name": "Legitimate Interest",
            "details": "Processing is lawful if the controller or a third party has a legitimate interest, provided there is no less intrusive way to achieve the same result and the interests do not override the fundamental rights or freedoms of the data subject. Three steps must be considered: (1) identify the legitimate interests, their importance, and beneficiaries; (2) assess whether a less intrusive method exists; (3) balance the interests, considering expectations of data subjects, transparency, and potential objections. Results of these tests should be documented to demonstrate compliance. Guidance is available from authorities such as the UK Information Commissioner’s Office and the Data Protection Network. GDPR specifically mentions employee or client data as contexts where legitimate interests may apply.",
        },
    },
    {
        "id": "Processing Special Categories of Data",
        "type": "LawfulBasis",
        "properties": {
            "name": "Processing Special Categories of Data",
            "details": """
Processing of special categories of data (racial or ethnic origin, political opinions, religious or philosophical beliefs, trade union membership, genetic data, biometric data, health data, sex life or sexual orientation) is prohibited unless specific grounds apply.

Exceptions include:
- Explicit consent where not prohibited by law.
- Employment or social security law with safeguards under national or EU law or collective agreements.
- Protection of vital interests when consent cannot be given.
- Legitimate activities of not-for-profit bodies with political, philosophical, religious, or trade union aims, limited to members or regular contacts, and not disclosed outside without consent.
- Data made public by the subject.
- Necessity for the establishment or exercise of legal claims.
- Preventive or occupational medicine, health or social care, or management of health/social care systems, subject to professional secrecy.
- Processing necessary for substantial public interest.

Some Member States impose additional restrictions beyond GDPR for these categories of data.
""",
        },
    },
    {
        "id": "Processing Data on Criminal Offences",
        "type": "LawfulBasis",
        "properties": {
            "name": "Processing Data on Criminal Offences",
            "details": """
Processing of data concerning criminal convictions or offences is only lawful if it has a valid legal basis and meets one of the following conditions:
- The processing takes place under official authority.
- The processing is authorised by Union or Member State law, provided appropriate safeguards for the rights and freedoms of data subjects are in place.

Private entities are prohibited from maintaining registers of criminal convictions or offences.
""",
        },
    },
    {
        "id": "Processing in the Context of Employment",
        "type": "LawfulBasis",
        "properties": {
            "name": "Processing in the Context of Employment",
            "details": """
Employment is a specific situation for processing personal data. National law or collective agreements may establish rules to protect employees’ rights and freedoms in this context. 

Examples of purposes include:
- Recruitment.
- Performance of the employment contract, including obligations under law or collective agreements.
- Management, planning, and organisation of work.
- Equality and diversity in the workplace.
- Health and safety at work.
- Protection of employer’s or customer’s property.
- Exercise and enjoyment of rights and benefits related to employment.
- Termination of the employment relationship. (Art. 88)

Key aspects:
- Safeguarding human dignity, legitimate interests, and fundamental rights.
- Ensuring transparency of processing.
- Rules on transfer of personal data within groups of undertakings or enterprises engaged in joint economic activity.
- Monitoring systems at the workplace (e.g., surveillance, geo-tracking).

If Member States adopt measures in this context, they must notify the European Commission to ensure compliance with GDPR. So far, Belgium, Germany, Latvia, Slovakia, and Hungary have used this opening clause. Trade unions may also adopt additional measures by collective agreement at company level.

In general, if monitoring provisions exist, employers must inform employees and prove that such measures are appropriate and balanced with employees’ fundamental rights and freedoms.
""",
        },
    },
    {
        "id": "Individual Rights of Data Subjects",
        "type": "RightsSet",
        "properties": {
            "name": "Individual Rights of Data Subjects",
            "details": """
The GDPR grants data subjects a set of individual rights to ensure transparency, control, and protection over their personal data.

These rights include:
- Right to be informed.
- Right to access.
- Right to rectification.
- Right to erasure.
- Right to restrict processing.
- Right to data portability.
- Right to object.
- Rights related to automated decision-making, including profiling.
""",
        },
    },
    {
        "id": "Right to be Informed",
        "type": "Right",
        "properties": {
            "name": "Right to be Informed",
            "details": """
Data subjects have the right to be informed in a transparent manner about what personal data are being collected and processed. 

The data controller must:
- Provide information on which data are retained and for what purpose at the moment the data are obtained (e.g., when someone registers through a form).
- Ensure the information is precise, transparent, easily accessible, and written in plain language.
- Respond to requests for additional information within one month, including details on purpose, storage duration, and who will have access (including third parties).
- Inform the data subject of their rights: access, rectification, erasure, restriction of processing, objection, and data portability.

If the purpose of processing changes, the data controller must inform the data subject before any new processing takes place.
""",
        },
    },
    {
        "id": "Right to Access",
        "type": "Right",
        "properties": {
            "name": "Right to Access",
            "details": """
Data subjects have the right to obtain a copy of their personal data and supplementary information related to it. Requests can be filed at reasonable intervals of time, and replies must be provided free of charge.

The reply should include:
- The purpose of the processing and the categories of personal data concerned.
- The recipients or categories of recipients to whom the personal data have been or will be disclosed, including recipients in third countries or international organisations.
- Where possible, the envisaged period for which the personal data will be stored, or, if not possible, the criteria used to determine that period.
- The existence of the right to request rectification, erasure, restriction of processing, or to object to processing.
- The right to lodge a complaint with a supervisory authority.
- Where the personal data are not collected directly from the data subject, any available information about their source.
- The existence of automated decision-making, including profiling, and meaningful information about the logic involved, as well as the significance and envisaged consequences of such processing for the data subject.
""",
        },
    },
    {
        "id": "Right to Access",
        "type": "Right",
        "properties": {
            "name": "Right to Access",
            "details": """
Data subjects have the right to obtain a copy of their personal data and supplementary information related to it. Requests can be filed at reasonable intervals of time, and replies must be provided free of charge.

The reply should include:
- The purpose of the processing and the categories of personal data concerned.
- The recipients or categories of recipients to whom the personal data have been or will be disclosed, including recipients in third countries or international organisations.
- Where possible, the envisaged period for which the personal data will be stored, or, if not possible, the criteria used to determine that period.
- The existence of the right to request rectification, erasure, restriction of processing, or to object to processing.
- The right to lodge a complaint with a supervisory authority.
- Where the personal data are not collected directly from the data subject, any available information about their source.
- The existence of automated decision-making, including profiling, and meaningful information about the logic involved, as well as the significance and envisaged consequences of such processing for the data subject.
""",
        },
    },
    {
        "id": "Right to Rectification",
        "type": "Right",
        "properties": {
            "name": "Right to Rectification",
            "details": """
Data subjects have the right to request the rectification of their personal data or to have incomplete data completed. 

The data controller must:
- Respond without undue delay and within one month of receiving the request.
- Extend the response period by up to two months if the request is complex, but must inform the data subject of the extension and reasons.
- Provide the rectified or completed data to the data subject free of charge.
""",
        },
    },
    {
        "id": "Right to Erasure",
        "type": "Right",
        "properties": {
            "name": "Right to Erasure",
            "details": """
Data subjects have the right, under specific circumstances, to have their personal data erased — also known as the 'right to be forgotten'.

This applies when:
- Data are no longer necessary for the purpose for which they were collected or processed.
- The data subject withdraws consent (if consent was the legal ground for processing).
- The data was unlawfully processed.
- The data subject objects to processing and the controller cannot demonstrate compelling legitimate grounds that override the data subject’s interests, rights, and freedoms.
- The data was collected when the data subject was a child (generally under 16 years old, depending on national legislation).

Controller obligations:
- Act upon request without undue delay.
- Respond within one month, or extend up to three months if the request is complex.

Limitations — the right to erasure does not apply if processing:
- Is necessary for freedom of expression or information.
- Is required to comply with other legal obligations.
- Is in the public interest.
- Relates to public health.
- Is necessary for the establishment or defense of legal claims.
- Is carried out for archiving purposes in the public interest.

The right to erasure is conditional. For example, requests may be declined if the controller demonstrates overriding legitimate grounds, such as maintaining information for public interest reasons.
""",
        },
    },
    {
        "id": "Right to Restrict Processing",
        "type": "Right",
        "properties": {
            "name": "Right to Restrict Processing",
            "details": """
Data subjects have the right to request the restriction or suppression of their personal data. This right limits the way the controller can use the data.

This applies when:
- The accuracy of the data is contested, and restriction is requested while the controller verifies its accuracy.
- The data was unlawfully processed, and the data subject prefers restriction instead of erasure.
- It is unclear whether the controller’s legitimate grounds override the interests of the data subject (if legitimate interests were the legal basis), in which case data should be restricted during verification.

Controller obligations:
- Implement measures to restrict data, such as moving it temporarily to another system, making it unavailable to users, or suspending access.
- Comply with the restriction request within one month of receipt.

Notes:
- This right is distinct from the rights to rectification and objection, though there are linkages.
""",
        },
    },
    {
        "id": "Right to Data Portability",
        "type": "Right",
        "properties": {
            "name": "Right to Data Portability",
            "details": """
Data subjects have the right to move their personal data easily from one controller’s IT system to another. 

This means:
- They can receive their personal data in a structured, commonly used, and machine-readable format.
- They can transmit their data to another controller without hindrance from the original controller.

Conditions:
- Applies only if the lawful basis for processing was consent or performance of a contract.
- Applies only when processing is carried out by automated means.
- Requires technical feasibility — IT systems must be able to export and receive the data.

Controller obligations:
- Comply with portability requests within one month of receipt.

Examples:
- Switching between telecom providers or applications (e.g., iTunes, Spotify) while retaining data and history.
- Platform workers (e.g., Uber drivers) transferring their data to another service platform, if technically feasible.
- Digital reputation data (such as reviews) may also be transferred if conditions are met.
""",
        },
    },
    {
        "id": "Right to Object",
        "type": "Right",
        "properties": {
            "name": "Right to Object",
            "details": """
Data subjects have the right, under certain circumstances, to object to and stop the processing of their personal data.

Key aspects:
- Individuals can object at any time to processing for direct marketing purposes. In such cases, the controller must stop processing immediately.
- This right is not absolute. If the controller relies on public interest or legitimate interests as the lawful basis, it may continue processing only if it demonstrates compelling legitimate grounds that override the interests, rights, and freedoms of the data subject.
- When an objection is received, the controller must stop using and processing the personal data, but this does not necessarily mean the data must be erased.
- The controller has one month from receipt of the objection to comply with the request.
""",
        },
    },
    {
        "id": "Rights related to Automated Decision-Making and Profiling",
        "type": "Right",
        "properties": {
            "name": "Rights related to Automated Decision-Making and Profiling",
            "details": """
Data subjects have the right not to be subject to decisions made solely by automated means, including profiling, when such decisions have legal or similarly significant effects.

Key aspects:
- Individuals must receive sufficient information about automated decisions taken without human involvement that impact them (e.g., refusal of an online loan application, recruitment aptitude tests, or employee monitoring systems).
- Profiling is defined as automated processing of personal data to evaluate personal aspects, such as work performance, economic situation, health, preferences, reliability, behaviour, location, or movement.

Controller obligations:
- Conduct a Data Protection Impact Assessment (DPIA) before implementing automated decision-making processes, due to the high risks involved.
- Use automated decision-making only if:
  - The data subject has explicitly consented.
  - It is necessary for entering into or performing a contract.
  - It is authorised by law (e.g., to combat tax fraud).
- If special categories of data are involved, automated decision-making is permitted only with explicit consent or for reasons of substantial public interest.

Safeguards:
- Data subjects must receive meaningful information about the logic involved, the significance, and the envisaged consequences of automated decisions.
- Controllers should take measures to prevent bias, discrimination, and errors.
- Concerns remain about readability, intelligibility, and clarity of algorithmic explanations, which require further investigation.
""",
        },
    },
    {
        "id": "Data Security",
        "type": "ComplianceSet",
        "properties": {
            "name": "Data Security",
            "description": """
Data privacy and security are interlinked, and security must be systematically built into and implemented across the organisation.

This includes:
- Physical security (premises, workstations, video-surveillance cameras).
- System security (internal networks, mobile equipment, servers, websites).
- Organisational measures to ensure compliance with GDPR and related regulations.
""",
            "details": """
                "Data protection by design and by default",
                "Contracts",
                "Documentation",
                "Data protection impact assessment (DPIA)",
                "Data breach",
                "Ensuring compliance",
                "Codes of conduct",
                "Binding corporate rules",
                "Certification",
                "Independent supervisory authority",
           """,
        },
    },
    {
        "id": "Data Protection by Design and by Default",
        "type": "Requirement",
        "properties": {
            "name": "Data Protection by Design and by Default",
            "details": """
These are two principles in the GDPR, both the responsibility of the data controller.

Data protection by design:
- Requires controllers to apply technical and organisational measures, including ethical considerations, to ensure privacy.
- Any processing of personal data supported by IT systems should be the outcome of a design project.
- Measures include anonymisation, encryption, and delete functionalities to guarantee restricted access and permanent protection.

Data protection by default:
- Requires controllers to collect and process only personal data necessary for each specific purpose.
- Processing must comply with the law and be transparently communicated to data subjects.
- Data subjects should not need to make extra efforts to protect their privacy.

Organisational obligations:
- Controllers must proactively safeguard data and train employees on risks and GDPR rules.
- The seven data-protection principles should guide which data can be collected.
- Controllers must ensure ongoing confidentiality, integrity, availability, and resilience of processing systems.
- They must restore access to personal data in a timely manner in case of incidents.
- Regular testing, assessing, and evaluating of technical and organisational measures must be in place.

Implementation considerations:
- Controllers and processors should assess scope, context, purpose, and costs before implementing new security measures.
""",
        },
    },
    {
        "id": "Contracts",
        "type": "Requirement",
        "properties": {
            "name": "Contracts",
            "details": """
The GDPR requires that data protection by design and by default provisions also apply to any third-party processor. 

Key obligations:
- The data controller must establish a contract with any processor.
- The contract must clearly state the responsibilities and liabilities of both parties.
- It must specify the legal basis for the data processing.
- It must provide guidance on which data can be processed and for which purpose.

This ensures accountability and transparency between controllers and processors, and guarantees that processors adhere to GDPR principles when handling personal data.
""",
        },
    },
    {
        "id": "Documentation",
        "type": "Requirement",
        "properties": {
            "name": "Documentation",
            "details": """
Under the GDPR, organisations must document their processing activities in certain circumstances:

Conditions:
- If the organisation employs more than 250 persons.
- If processing is likely to result in a risk to the rights and freedoms of data subjects.
- If processing is not occasional.
- If processing includes special categories of data or data related to criminal convictions or offences.

Controller obligations:
- Document processing activities under their responsibility.
- Maintain safeguard mechanisms, records of consent, and information about the location of data.
- While best practice is to document all processing activities, GDPR provides specific obligations in Article 30.

Benefits:
- Documentation provides transparency and accountability.
- It allows employees and data subjects to better understand what data is processed and for what reasons.
- It supports the exercise of data subject rights under the regulation.
""",
        },
    },
    {
        "id": "Data Protection Impact Assessment (DPIA)",
        "type": "Requirement",
        "properties": {
            "name": "Data Protection Impact Assessment (DPIA)",
            "details": """
A Data Protection Impact Assessment (DPIA) is required when processing is likely to result in a high risk to the rights and freedoms of individuals, including risks of significant social or economic disadvantage.

Controller obligations:
- Conduct an assessment before any processing operation to evaluate its impact on personal data protection.
- Carry out a DPIA when:
  - Systematic and extensive profiling is used.
  - Special categories of data are processed on a large scale.
  - Publicly accessible places are systematically monitored.
- Consult the national data protection authority’s list of processing operations that require a DPIA.
- Seek the views of data subjects or their representatives (e.g., works councils) on intended processing.

Risk management:
- The Data Protection Officer (DPO) should advise on reducing risks.
- If high risks cannot be mitigated, the controller must consult the national data protection authority before proceeding.

Examples:
- Introducing geo-tracking technology for employees.
- Collecting data on employees’ trade union membership.
- Deploying new technologies or software that process employees’ personal data.

Guidance:
- The Article 29 Working Party and the Data Protection Working Party provide guidelines on when and how to conduct a DPIA.
- Controllers should assess scope, context, purpose, and costs before implementing new measures.
""",
        },
    },
    {
        "id": "Data Breach",
        "type": "Requirement",
        "properties": {
            "name": "Data Breach",
            "details": """
A data breach is any unlawful destruction, loss, alteration, unauthorised disclosure of, or access to personal data. 

Forms of breaches:
- Loss of data (e.g., theft of a computer or mobile phone).
- Hacking of servers or systems.
- Any incident that compromises confidentiality, integrity, or availability of personal data.

Controller and processor obligations:
- Every breach that implies risks to personal rights and freedoms must be reported to the supervisory authority as soon as it is detected, regardless of when it occurred.
- Develop and implement a security breach response plan and policy.
- Employees, data subjects, processors, and the Data Protection Officer must immediately (within 72 hours) inform the controller upon detecting a breach.
- The controller must assess severity and, if necessary, notify the supervisory authority and affected data subjects.
- If direct notification to data subjects is impractical, a public announcement may be used.
- If authorities are not notified within 72 hours, the controller must provide a reasonable justification for the delay.

Notification requirements:
- Specify which data were accessed.
- Indicate how many people were affected.
- Provide the name of the Data Protection Officer.
- Outline possible consequences of the breach.
- Describe measures taken to mitigate the breach.
""",
        },
    },
    {
        "id": "Ensuring Compliance",
        "type": "Requirement",
        "properties": {
            "name": "Ensuring Compliance",
            "details": """
Ensuring compliance under the GDPR involves adopting additional safeguards and mechanisms that demonstrate accountability and adherence to the regulation. This umbrella covers sectoral codes of conduct, binding corporate rules, certification schemes, and oversight by independent supervisory authorities.
""",
        },
    },
    {
        "id": "Codes of Conduct",
        "type": "Requirement",
        "properties": {
            "name": "Codes of Conduct",
            "details": """
Associations or bodies representing categories of controllers or processors can establish sectoral codes of conduct. 
- Can apply nationally or across the EU.
- Organisations outside the EU may adhere contractually.
- Must cover GDPR rules and may add restrictions for high-risk sectors.
- Draft codes require supervisory authority approval; if cross-border, the European Data Protection Board (EDPB) reviews them.
""",
        },
    },
    {
        "id": "Binding Corporate Rules",
        "type": "Requirement",
        "properties": {
            "name": "Binding Corporate Rules",
            "details": """
Companies can adopt internal binding corporate rules (BCRs) that apply to all entities within the organisation.
- Drafted by the employer and approved by the supervisory authority.
- Once approved, BCRs allow lawful data transfers across company entities.
""",
        },
    },
    {
        "id": "Certification",
        "type": "Requirement",
        "properties": {
            "name": "Certification",
            "details": """
The EDPB and national supervisory authorities can accredit certification bodies.
- Organisations can demonstrate GDPR compliance by obtaining accredited certificates.
- Certification provides external validation of compliance practices.
""",
        },
    },
    {
        "id": "Independent Supervisory Authority",
        "type": "Requirement",
        "properties": {
            "name": "Independent Supervisory Authority",
            "details": """
National data protection authorities have expanded powers under GDPR.
- Can ban certain types of processing or impose fines.
- Cooperate across Member States to monitor and enforce compliance.
- Their primary role is to oversee, enforce, and safeguard data protection rights.
""",
        },
    },
    {
        "id": "Liability",
        "type": "ComplianceSet",
        "properties": {
            "name": "Liability",
            "details": """
                "Fines",
                "Data Controller",
                "Data Processor",
                "Joint and Several Liability",
                "Data Protection Officer",
                "Employee",
            """,
        },
    },
    {
        "id": "Fines",
        "type": "Requirement",
        "properties": {
            "name": "Fines",
            "details": """
GDPR allows supervisory authorities to impose administrative fines for non-compliance. 
- Fines can be significant, up to 20 million EUR or 4% of global annual turnover, whichever is higher.
- The severity depends on the nature, gravity, and duration of the infringement.
""",
        },
    },
    {
        "id": "Data Controller",
        "type": "Actor",
        "properties": {
            "name": "Data Controller",
            "details": """
The data controller determines the purposes and means of processing personal data. 
- Holds primary responsibility for compliance.
- Must ensure contracts, safeguards, and lawful bases are in place.
""",
        },
    },
    {
        "id": "Data Processor",
        "type": "Actor",
        "properties": {
            "name": "Data Processor",
            "details": """
The data processor acts on behalf of the controller. 
- Must follow controller instructions.
- Can be held liable if acting outside instructions or failing to implement safeguards.
""",
        },
    },
    {
        "id": "Joint and Several Liability",
        "type": "Requirement",
        "properties": {
            "name": "Joint and Several Liability",
            "details": """
When multiple parties (controllers or processors) are involved in processing, they may be jointly and severally liable. 
- This ensures data subjects can claim compensation from any responsible party.
- Liability can later be apportioned internally between parties.
""",
        },
    },
    {
        "id": "Data Protection Officer",
        "type": "Actor",
        "properties": {
            "name": "Data Protection Officer",
            "details": """
The Data Protection Officer (DPO) advises on compliance and monitors data protection practices. 
- Not personally liable for fines but plays a critical role in ensuring organisational compliance.
- Acts as a point of contact with supervisory authorities.
""",
        },
    },
    {
        "id": "Employee",
        "type": "Actor",
        "properties": {
            "name": "Employee",
            "details": """
Employees handling personal data must follow organisational policies and GDPR rules. 
- Breaches caused by negligence or misconduct can expose the organisation to liability.
- Training and awareness are essential safeguards.
""",
        },
    },
    {
        "id": "Fines",
        "type": "Requirement",
        "properties": {
            "name": "Fines",
            "details": """
The GDPR allows supervisory authorities to impose administrative fines for non-compliance.

Key aspects:
- Fines can reach up to 20 million EUR or 4% of the company’s annual global turnover, whichever is higher.
- Such maximum fines are typically reserved for repeated or severe violations, especially when organisations benefit from breaking data protection law.
- The imposition of fines depends on factors such as:
  - Severity and duration of the breach.
  - Cooperation with supervisory authorities.
  - Measures taken to mitigate the breach.
  - Number of people affected.

Graduated enforcement:
- For minor breaches, authorities may prefer issuing warnings or corrective orders rather than imposing fines.

Compensation rights:
- Data subjects have the right to demand compensation from controllers or processors for material or non-material damage resulting from infringements.
""",
        },
    },
    {
        "id": "Data Controller",
        "type": "Actor",
        "properties": {
            "name": "Data Controller",
            "details": """
The data controller is generally liable for any non-compliance under the GDPR.

Key aspects:
- The controller determines the purposes and means of processing personal data.
- Liability usually cannot be transferred to the Data Protection Officer, who serves only in an advisory role. This limitation is sometimes controversial.
- In certain cases, liability can be transferred to the data processor, or both controller and processor may be jointly liable.
- Controllers and processors can avoid liability if they can prove they were not responsible for the damage.

Case law:
- In 2017, the UK supermarket chain Morrisons was held liable for a deliberate data breach caused by an employee. This case illustrates that employers can be liable even when the breach is intentional misconduct by staff.
""",
        },
    },
    {
        "id": "Data Processor",
        "type": "Actor",
        "properties": {
            "name": "Data Processor",
            "details": """
The data processor is the natural person or organisation that processes personal data on behalf of the controller.

Liability rules:
- The processor is liable only if they fail to comply with GDPR requirements on processing or act outside the controller’s instructions.
- Liability arises when processors:
  - Use sub-contractors without authorisation from the controller.
  - Fail to cooperate with supervisory authorities.
  - Do not implement required safety and security measures.
  - Fail to maintain records of processing activities.

Relationship with controller:
- The processor must strictly follow the controller’s instructions.
- Contracts between controller and processor must clearly define responsibilities, safeguards, and compliance obligations.
""",
        },
    },
    {
        "id": "Joint and Several Liability",
        "type": "Requirement",
        "properties": {
            "name": "Joint and Several Liability",
            "details": """
Joint and several liability applies when both the controller and processor, or multiple controllers/processors, contribute to a data breach.

Key aspects:
- Each party involved is liable for the entire damage caused by the breach.
- This ensures that data subjects can claim full compensation from any responsible party without needing to prove which one caused the harm.
- After compensation is paid, the liable party can seek reimbursement from the other controllers or processors based on their share of responsibility.
- This mechanism strengthens accountability and guarantees that data subjects are not left uncompensated due to disputes between controllers and processors.
""",
        },
    },
    {
        "id": "Data Protection Officer",
        "type": "Actor",
        "properties": {
            "name": "Data Protection Officer",
            "details": """
The GDPR does not explicitly state that the Data Protection Officer (DPO) can be held liable for their actions. However, legal opinion is divided on this issue.

Key aspects:
- The DPO’s role is primarily advisory, monitoring compliance and acting as a point of contact with supervisory authorities.
- Under GDPR, liability generally rests with the controller or processor, not the DPO.

Legal perspectives:
- The International Association of Privacy Professionals (IAPP) argues that national laws imposing criminal liability on DPOs are compatible with GDPR.
- In Ireland, DPOs can be criminally liable if they consent to violations.
- In the UK, DPOs may be liable if they knowingly provide false advice.

Academic opinion:
- Thiébaut Devergranne, professor of IT law, suggests courts could establish civil liability for DPOs even without explicit legal grounds.
- Examples include cases where a DPO had knowledge of a problem but failed to report it, or demonstrated incompetence amounting to grave misconduct.

Uncertainty:
- Further court rulings are needed to clarify the extent of DPO liability.
- Current consensus is that liability protections apply unless misconduct or complicity is proven.
""",
        },
    },
    {
        "id": "Employee",
        "type": "Actor",
        "properties": {
            "name": "Employee",
            "details": """
Employees handling personal data are generally not personally accountable under GDPR, since liability usually rests with the data controller.

Key aspects:
- The controller is in general liable for damages caused by data breaches.
- Employees are usually shielded from personal liability unless misconduct is intentional.

Exceptions:
- In cases of deliberate breaches, employees may face criminal conviction and dismissal (e.g., the Morrisons case in the UK).
- Criminal offences committed by employees may fall outside GDPR but still carry consequences under national law.

Uncertainty:
- The GDPR does not clearly define the extent of employee liability for unintentional breaches.
- Open questions remain, such as:
  - Whether employees of controllers have higher liability than employees of processors.
  - On what legal grounds employees could be held liable for data breaches.

Conclusion:
- Employee liability under GDPR is limited and unsettled, with intentional misconduct being the main scenario where personal accountability applies.
""",
        },
    },
    {
        "id": "The GDPR and the Public Sector",
        "type": "ComplianceSet",
        "properties": {
            "name": "The GDPR and the Public Sector",
            "details": """
                "Public Sector",
                "Public authorities or bodies",
                "Independent supervisory authority",
            """,
        },
    },
    {
        "id": "Public Interest",
        "type": "Requirement",
        "properties": {
            "name": "Public Interest",
            "details": """
The notion of public interest is not explicitly defined in the GDPR and depends on context and national practice. However, the regulation provides leeway for processing by both public and private actors when the purpose serves the public interest.

Key aspects:
- **Purpose limitation exception**: Data may be processed for archiving, scientific or historical research, or statistical purposes in the public interest. In such cases:
  - Data can be stored for longer periods if data minimisation is respected.
  - Data subject rights may not apply if they render the purpose impossible or seriously impair its achievement.
- **Special categories of data**: Processing is permitted if there is a legal basis in EU or Member State law, and the public interest is substantial.
- **Legal basis**: Article 6(1)(e) allows processing if necessary for the performance of a task carried out in the public interest or in the exercise of official authority vested in the controller.
- **Public health**: Special categories of data may be processed for reasons of public interest in public health, provided sufficient safeguards exist in EU or Member State law.
- **Consultation requirement**: Member States may require controllers to consult with the data protection authority before relying on public interest as a lawful basis.
- **Data transfers**: Important reasons of public interest can justify transferring data to a third country without prior European Commission adequacy assessment, but only if recognised by EU or Member State law.
- **Complaints mechanism**: The “one-stop-shop” mechanism does not apply to public authorities or private bodies acting in the public interest. Only the authority where the body is established is competent in such cases.
""",
        },
    },
    {
        "id": "Public Authorities or Bodies",
        "type": "Actor",
        "properties": {
            "name": "Public Authorities or Bodies",
            "details": """
Public authorities and bodies are subject to specific derogations and obligations under the GDPR.

Derogations (GDPR does not apply):
- EU institutions and agencies are regulated by Regulation (EC) No 45/2001.
- Public administrations collecting data for investigations under legal obligations (e.g., tax/customs authorities, financial investigation units, securities market regulators).
- Processing in the context of the EU Common Foreign and Security Policy.
- Data collected for prevention, investigation, detection, or prosecution of criminal offences, or execution of criminal penalties. In these cases, EU Directive 2016/680 applies.

Special provisions:
- Public authorities may process data without consent if necessary for tasks carried out in the public interest or in the exercise of official authority vested in the controller.
- They must demonstrate that processing is in the public interest and within their legal competences. This differs from the “legitimate interest” clause for private entities.
- Courts acting in their judicial capacity may process special categories of data.
- Only public authorities may maintain a comprehensive register of criminal convictions.

Administrative fines:
- Member States can decide whether and to what extent public authorities are subject to administrative fines.

Data Protection Officer (DPO):
- Public authorities must appoint a DPO to advise on compliance.
- Several institutions may share a DPO to reduce costs, depending on organisational structure and size.
- Courts acting in their judicial capacity are exempt from appointing a DPO.
""",
        },
    },
    {
        "id": "Independent Supervisory Authority",
        "type": "Actor",
        "properties": {
            "name": "Independent Supervisory Authority",
            "details": """
Member States must establish one or more independent data protection supervisory authorities under the GDPR.

Independence and resources:
- Authorities must be independent; members cannot hold occupations incompatible with their role.
- Member States must provide sufficient human, financial, and technical resources.
- Members enjoy strong job security, ending only upon expiry of term, resignation, compulsory retirement, or serious misconduct.
- Members are bound by professional secrecy rules.

Tasks and powers:
- Monitor and enforce GDPR compliance.
- Handle complaints from data subjects.
- Conduct investigations, provide advice on processing, and raise public awareness.
- Article 57 lists supervisory authority tasks.
- Article 58 grants powers to:
  - Request information from controllers/processors.
  - Issue warnings or reprimands.
  - Ban unlawful processing.
  - Accredit certification bodies.
  - Impose fines.

Cooperation and one-stop-shop mechanism:
- A lead authority must be designated to represent the Member State in the European Data Protection Board (EDPB).
- The one-stop-shop mechanism allows data subjects to lodge complaints in the Member State of a private entity’s main establishment.
- The lead authority coordinates with other authorities where the company operates.
- If consensus cannot be reached, the EDPB issues a binding decision.
- Cooperation is strengthened by deadlines (one month for replies) and rules for joint operations.
""",
        },
    },
    {
        "id": "Guidelines on Compliance for Trade Unions",
        "type": "ComplianceSet",
        "properties": {
            "name": "Guidelines on Compliance for Trade Unions",
            "details": """
                "On Data Collection and Mapping",
                "On data security",
                "On technical measures",
                "On policies and procedures",
            """,
        },
    },
    {
        "id": "On Data Collection and Mapping",
        "type": "Requirement",
        "properties": {
            "name": "On Data Collection and Mapping",
            "details": """
Trade unions must adopt structured practices for collecting and mapping personal data to ensure GDPR compliance.

Key steps:
1. **Information sessions**: Organize GDPR awareness sessions for union staff and individuals directly involved in data processing.
2. **Data Protection Officer (DPO)**: Identify the DPO and involve them in mapping crucial trade union issues within the organisation or workplace.
3. **Explicit consent**: When new data is collected, unions must obtain explicit consent for specified purposes.
4. **Existing data**: No need to re-ask for consent if it was already given at the time of collection (e.g., membership forms, mailing list sign-ups). Legitimate interests (e.g., newsletters) may serve as a legal basis, but if no legal basis exists, the data should be deleted.
5. **Special categories of data**: Prohibited from collecting sensitive categories (e.g., racial ethnicity, health). Aggregated, non-identifiable information may be shared (e.g., “Among 10 participants, 3 are vegetarians”).
6. **Children’s data**: Verify national rules on the age threshold (13–16 years depending on Member State). Active parental consent is required when processing children’s data.
7. **Data inventory**: Maintain a clear inventory of personal data held on members, affiliates, and supporters, including details of data sharing practices.
""",
        },
    },
    {
        "id": "On Data Security",
        "type": "Requirement",
        "properties": {
            "name": "On Data Security",
            "details": """
Trade unions must implement strong data security measures to safeguard member information and comply with GDPR.

Key steps:
8. **Risk identification and mitigation**: Assess risks specific to the organisation, minimise them, and educate employees on prevention strategies.
9. **Privacy and security programme**: Develop a comprehensive programme ensuring confidentiality and protection against unauthorised access.
10. **Secure database management**: Create password-protected or encrypted databases, limit access to authorised personnel, and store data on protected servers. Pay special attention to special categories of data, which should only be collected if aligned with union aims.
11. **Phishing awareness**: Raise staff awareness about phishing and spam, communicating risks regularly.
12. **Breach response plan**: Draft a clear plan to follow when data breaches occur, including notification procedures and mitigation steps.
13. **Provider evaluation**: Assess external providers and partners in terms of their security standards and compliance with GDPR.
""",
        },
    },
    {
        "id": "On Technical Measures",
        "type": "Requirement",
        "properties": {
            "name": "On Technical Measures",
            "details": """
Trade unions must adopt appropriate technical and organisational measures to ensure GDPR compliance.

Key step:
1. **Implement and evaluate measures**: Put in place relevant technical and organisational safeguards such as auditing, testing, encryption, and secure access controls. Be aware of measures that cannot be implemented and document the justification for their absence.
""",
        },
    },
    {
        "id": "On Policies and Procedures",
        "type": "Requirement",
        "properties": {
            "name": "On Policies and Procedures",
            "details": """
Trade unions must establish clear policies and procedures to ensure GDPR compliance and accountability.

Key steps:
2. **Identify applicable laws**: Review European and national regulations, opinions from authorities, and established data protection practices.
3. **Privacy notices**: Ensure notices shown at data collection (e.g., registration forms) state retention periods, specific purposes, and data subject rights. Inform members of any changes in privacy terms.
4. **Internal procedure**: Draft a procedure explaining how, why, and for how long personal data is stored and processed. Cover all individual rights, request-handling processes, breach response, and designate responsible roles (controller, processor, DPO).
5. **Privacy policy**: Review and publish a privacy policy on the union’s website. It should follow lawful processing principles and include:
   a. What data are collected  
   b. For which purpose  
   c. For how long  
   d. How they are collected  
   e. How they are processed  
   f. How the process is carried out  
   g. Potential future processing scenarios  
   h. How data subjects can exercise their rights  
   i. With whom data is shared  
   j. Safeguards in place  
   - Apply data minimisation: reduce third-party processors. Avoid social media plugins that collect visitor data.
6. **Data Protection Impact Assessment (DPIA)**: Conduct when necessary, especially for new technologies or high-risk processing.
7. **Avoid risky practices**: List practices to avoid, such as sharing data and passwords.
8. **Employee data**: As employers, trade unions must respect GDPR when processing employee data.
""",
        },
    },
    {
        "id": "Practical Recommendations on Data Protection",
        "type": "Requirement",
        "properties": {
            "name": "Practical Recommendations on Data Protection",
            "details": """
Keeping data safe is the utmost priority. Trade unions and organisations should adopt practical measures to protect data subjects and avoid breaches.

Key recommendations:
1. **Employee training**: Ensure staff have constant and sufficient information and training on data protection.
2. **Policies in place**: Establish data protection policies covering security measures and employment/staffing data.
3. **Password protection**: Secure all devices with strong passwords, change them regularly, and lock devices overnight.
4. **Paper records**: Store physical records in locked cabinets, out of view of visitors.
5. **Software updates**: Regularly update software and anti-virus programmes to reduce vulnerabilities.
6. **Encryption**: Encrypt databases and documents, especially those containing special categories of data (e.g., union membership).
7. **Email practices**: Use good practices such as sending emails via mailing lists or placing recipients in the blind copy (BCC) field.
8. **Website security**: Secure websites and collect consent if cookies are required.
9. **Anonymisation**: Adopt anonymous approaches by unlinking or deleting files as soon as possible. Case files may rely on legitimate union activities or legal claims as a basis, but must be erased or anonymised once closed.
10. **Employer responsibilities**: Ensure employers are aware of their responsibilities as controllers under GDPR.
11. **Supervisory Authority contact**: Know when to contact the Supervisory Authority for guidance or reporting.
""",
        },
    },
]


relationships = [
    {
        "source": {"id": "Data Controller", "type": "Role"},
        "target": {"id": "Data Protection Officer", "type": "Role"},
        "type": "OBLIGATION_TO_APPOINT",
        "properties": {
            "in_case_of": "If the processing is carried out by a public authority or body, or if the core activities of the controller or the processor consist of processing operations which, by virtue of their nature, their scope and/or their purposes, require regular and systematic monitoring of data subjects on a large scale, or if the core activities consist of processing on a large scale of special categories of data."
        },
    },
    {
        "source": {"id": "Data Protection Officer", "type": "Role"},
        "target": {"id": "Data Controller", "type": "Role"},
        "type": "ADVISE",
        "properties": {"comply": "how to comply with the regulation"},
    },
    {
        "source": {"id": "Germany", "type": "MemberState"},
        "target": {"id": "Data Protection Officer", "type": "Role"},
        "type": "APPOINTMENT_RULE",
        "properties": {
            "law": """

               If more than 10 people are constantly involved in automatic processing of data, a DPO must be appointed.
               If the DPO is to be a member of staff, then the works council has a right of co-determi-
nation. In general, it is strongly advised to appoint a DPO even if it is not an obligation.
            """
        },
    },
    {
        "source": {"id": "Data Controller", "type": "Role"},
        "target": {"id": "Data Processor", "type": "Role"},
        "type": "DESIGNATES",
        "properties": {
            "context": "Controller appoints processor to collect and process data"
        },
    },
    {
        "source": {"id": "Employee", "type": "Role"},
        "target": {"id": "Data Controller", "type": "Role"},
        "type": "CONSIDERED_AS",
        "properties": {"jurisdiction": "UK authority view"},
    },
 
    {
        "source": {"id": "Data Controller", "type": "Role"},
        "target": {"id": "Data Processor", "type": "Role"},
        "type": "RESPONSIBLE_FOR",
        "properties": {"implication": "Liability and responsibility issues under GDPR"},
    },
    {
        "source": {"id": "Public Authority", "type": "Organization"},
        "target": {"id": "Data Protection Officer", "type": "Role"},
        "type": "FINANCIAL_AND_STAFF_IMPLICATIONS",
        "properties": {
            "context": """Required to appoint DPO when processing large amounts of data which may be reduced by 
                                            appointing one DPO for several organisations.
        
        """
        },
    },
    {
        "source": {"id": "Barbulescu v Romania", "type": "CaseLaw"},
        "target": {"id": "Guiding Principles", "type": "PrincipleSet"},
        "type": "ILLUSTRATES",
        "properties": {
            "context": "Case shows employees can rely on principles if privacy is violated"
        },
    },
    {
        "source": {"id": "Guiding Principles", "type": "PrincipleSet"},
        "target": {"id": "Lawfulness, Fairness and Transparency", "type": "Principle"},
        "type": "COMPRISES",
    },
    {
        "source": {"id": "Guiding Principles", "type": "PrincipleSet"},
        "target": {"id": "Purpose Limitation", "type": "Principle"},
        "type": "COMPRISES",
    },
    {
        "source": {"id": "Guiding Principles", "type": "PrincipleSet"},
        "target": {"id": "Data Minimisation", "type": "Principle"},
        "type": "COMPRISES",
    },
    {
        "source": {"id": "Guiding Principles", "type": "PrincipleSet"},
        "target": {"id": "Accuracy", "type": "Principle"},
        "type": "COMPRISES",
    },
    {
        "source": {"id": "Guiding Principles", "type": "PrincipleSet"},
        "target": {"id": "Storage Limitation", "type": "Principle"},
        "type": "COMPRISES",
    },
    {
        "source": {"id": "Guiding Principles", "type": "PrincipleSet"},
        "target": {"id": "Integrity and Confidentiality", "type": "Principle"},
        "type": "COMPRISES",
    },
    {
        "source": {"id": "Guiding Principles", "type": "PrincipleSet"},
        "target": {"id": "Accountability", "type": "Principle"},
        "type": "COMPRISES",
    },
    {
        "source": {
            "id": "Lawful Basis and Limits to Processing",
            "type": "PrincipleSet",
        },
        "target": {"id": "Consent of the Data Subject", "type": "LawfulBasis"},
        "type": "COMPRISES",
    },
    {
        "source": {
            "id": "Lawful Basis and Limits to Processing",
            "type": "PrincipleSet",
        },
        "target": {"id": "Performance of a Contract", "type": "LawfulBasis"},
        "type": "COMPRISES",
    },
    {
        "source": {
            "id": "Lawful Basis and Limits to Processing",
            "type": "PrincipleSet",
        },
        "target": {"id": "Compliance with a Legal Obligation", "type": "LawfulBasis"},
        "type": "COMPRISES",
    },
    {
        "source": {
            "id": "Lawful Basis and Limits to Processing",
            "type": "PrincipleSet",
        },
        "target": {"id": "Protection of Vital Interests", "type": "LawfulBasis"},
        "type": "COMPRISES",
    },
    {
        "source": {
            "id": "Lawful Basis and Limits to Processing",
            "type": "PrincipleSet",
        },
        "target": {"id": "Legitimate Interest", "type": "LawfulBasis"},
        "type": "COMPRISES",
    },
    {
        "source": {
            "id": "Lawful Basis and Limits to Processing",
            "type": "PrincipleSet",
        },
        "target": {
            "id": "Processing Special Categories of Data",
            "type": "LawfulBasis",
        },
        "type": "COMPRISES",
    },
    {
        "source": {
            "id": "Lawful Basis and Limits to Processing",
            "type": "PrincipleSet",
        },
        "target": {"id": "Processing Data on Criminal Offences", "type": "LawfulBasis"},
        "type": "COMPRISES",
    },
    {
        "source": {
            "id": "Lawful Basis and Limits to Processing",
            "type": "PrincipleSet",
        },
        "target": {
            "id": "Processing in the Context of Employment",
            "type": "LawfulBasis",
        },
        "type": "COMPRISES",
    },
    {
        "source": {
            "id": "Lawful Basis and Limits to Processing",
            "type": "PrincipleSet",
        },
        "target": {"id": "Consent of the Data Subject", "type": "LawfulBasis"},
        "type": "COMPRISES",
    },
    {
        "source": {
            "id": "Lawful Basis and Limits to Processing",
            "type": "PrincipleSet",
        },
        "target": {"id": "Performance of a Contract", "type": "LawfulBasis"},
        "type": "COMPRISES",
    },
    {
        "source": {
            "id": "Lawful Basis and Limits to Processing",
            "type": "PrincipleSet",
        },
        "target": {"id": "Compliance with a Legal Obligation", "type": "LawfulBasis"},
        "type": "COMPRISES",
    },
    {
        "source": {
            "id": "Lawful Basis and Limits to Processing",
            "type": "PrincipleSet",
        },
        "target": {"id": "Protection of Vital Interests", "type": "LawfulBasis"},
        "type": "COMPRISES",
    },
    {
        "source": {
            "id": "Lawful Basis and Limits to Processing",
            "type": "PrincipleSet",
        },
        "target": {"id": "Legitimate Interest", "type": "LawfulBasis"},
        "type": "COMPRISES",
    },
    {
        "source": {
            "id": "Lawful Basis and Limits to Processing",
            "type": "PrincipleSet",
        },
        "target": {
            "id": "Processing Special Categories of Data",
            "type": "LawfulBasis",
        },
        "type": "COMPRISES",
    },
    {
        "source": {
            "id": "Lawful Basis and Limits to Processing",
            "type": "PrincipleSet",
        },
        "target": {"id": "Processing Data on Criminal Offences", "type": "LawfulBasis"},
        "type": "COMPRISES",
    },
    {
        "source": {
            "id": "Lawful Basis and Limits to Processing",
            "type": "PrincipleSet",
        },
        "target": {
            "id": "Processing in the Context of Employment",
            "type": "LawfulBasis",
        },
        "type": "COMPRISES",
    },
    {
        "source": {"id": "Individual Rights of Data Subjects", "type": "RightsSet"},
        "target": {"id": "Right to be Informed", "type": "Right"},
        "type": "COMPRISES",
    },
    {
        "source": {"id": "Individual Rights of Data Subjects", "type": "RightsSet"},
        "target": {"id": "Right to Access", "type": "Right"},
        "type": "COMPRISES",
    },
    {
        "source": {"id": "Individual Rights of Data Subjects", "type": "RightsSet"},
        "target": {"id": "Right to Rectification", "type": "Right"},
        "type": "COMPRISES",
    },
    {
        "source": {"id": "Individual Rights of Data Subjects", "type": "RightsSet"},
        "target": {"id": "Right to Erasure", "type": "Right"},
        "type": "COMPRISES",
    },
    {
        "source": {"id": "Individual Rights of Data Subjects", "type": "RightsSet"},
        "target": {"id": "Right to Restrict Processing", "type": "Right"},
        "type": "COMPRISES",
    },
    {
        "source": {"id": "Individual Rights of Data Subjects", "type": "RightsSet"},
        "target": {"id": "Right to Data Portability", "type": "Right"},
        "type": "COMPRISES",
    },
    {
        "source": {"id": "Individual Rights of Data Subjects", "type": "RightsSet"},
        "target": {"id": "Right to Object", "type": "Right"},
        "type": "COMPRISES",
    },
    {
        "source": {"id": "Individual Rights of Data Subjects", "type": "RightsSet"},
        "target": {
            "id": "Rights related to Automated Decision-Making and Profiling",
            "type": "Right",
        },
        "type": "COMPRISES",
    },
    {
        "source": {"id": "Data Security", "type": "ComplianceSet"},
        "target": {
            "id": "Data Protection by Design and by Default",
            "type": "Requirement",
        },
        "type": "COMPRISES",
    },
    {
        "source": {"id": "Data Security", "type": "ComplianceSet"},
        "target": {"id": "Contracts", "type": "Requirement"},
        "type": "COMPRISES",
    },
    {
        "source": {"id": "Data Security", "type": "ComplianceSet"},
        "target": {"id": "Documentation", "type": "Requirement"},
        "type": "COMPRISES",
    },
    {
        "source": {"id": "Data Security", "type": "ComplianceSet"},
        "target": {
            "id": "Data Protection Impact Assessment (DPIA)",
            "type": "Requirement",
        },
        "type": "COMPRISES",
    },
    {
        "source": {"id": "Data Security", "type": "ComplianceSet"},
        "target": {"id": "Data Breach", "type": "Requirement"},
        "type": "COMPRISES",
    },
    {
        "source": {"id": "Data Security", "type": "ComplianceSet"},
        "target": {"id": "Ensuring Compliance", "type": "Requirement"},
        "type": "COMPRISES",
    },
    {
        "source": {"id": "Data Security", "type": "ComplianceSet"},
        "target": {"id": "Codes of conduct", "type": "Requirement"},
        "type": "COMPRISES",
    },
    {
        "source": {"id": "Data Security", "type": "ComplianceSet"},
        "target": {"id": "Binding corporate rules", "type": "Requirement"},
        "type": "COMPRISES",
    },
    {
        "source": {"id": "Data Security", "type": "ComplianceSet"},
        "target": {"id": "Certification", "type": "Requirement"},
        "type": "COMPRISES",
    },
    {
        "source": {"id": "Data Security", "type": "ComplianceSet"},
        "target": {"id": "Independent supervisory authority", "type": "Requirement"},
        "type": "COMPRISES",
    },
    {
        "source": {"id": "Liability", "type": "ComplianceSet"},
        "target": {"id": "Fines", "type": "Requirement"},
        "type": "COMPRISES",
    },
    {
        "source": {"id": "Liability", "type": "ComplianceSet"},
        "target": {"id": "Data Controller", "type": "Actor"},
        "type": "COMPRISES",
    },
    {
        "source": {"id": "Liability", "type": "ComplianceSet"},
        "target": {"id": "Data Processor", "type": "Actor"},
        "type": "COMPRISES",
    },
    {
        "source": {"id": "Liability", "type": "ComplianceSet"},
        "target": {"id": "Joint and Several Liability", "type": "Requirement"},
        "type": "COMPRISES",
    },
    {
        "source": {"id": "Liability", "type": "ComplianceSet"},
        "target": {"id": "Data Protection Officer", "type": "Actor"},
        "type": "COMPRISES",
    },
    {
        "source": {"id": "Liability", "type": "ComplianceSet"},
        "target": {"id": "Employee", "type": "Actor"},
        "type": "COMPRISES",
    },
    {
        "source": {"id": "The GDPR and the Public Sector", "type": "ComplianceSet"},
        "target": {"id": "Public Interest", "type": "Requirement"},
        "type": "COMPRISES",
    },
    {
        "source": {"id": "The GDPR and the Public Sector", "type": "ComplianceSet"},
        "target": {"id": "Public Authorities or Bodies", "type": "Actor"},
        "type": "COMPRISES",
    },
    {
        "source": {"id": "The GDPR and the Public Sector", "type": "ComplianceSet"},
        "target": {"id": "Independent Supervisory Authority", "type": "Actor"},
        "type": "COMPRISES",
    },
    {
        "source": {
            "id": "Guidelines on Compliance for Trade Unions",
            "type": "ComplianceSet",
        },
        "target": {"id": "On Data Collection and Mapping", "type": "Requirement"},
        "type": "COMPRISES",
    },
    {
        "source": {
            "id": "Guidelines on Compliance for Trade Unions",
            "type": "ComplianceSet",
        },
        "target": {"id": "On Data Security", "type": "Requirement"},
        "type": "COMPRISES",
    },
    {
        "source": {
            "id": "Guidelines on Compliance for Trade Unions",
            "type": "ComplianceSet",
        },
        "target": {"id": "On Technical Measures", "type": "Requirement"},
        "type": "COMPRISES",
    },
    {
        "source": {
            "id": "Guidelines on Compliance for Trade Unions",
            "type": "ComplianceSet",
        },
        "target": {"id": "On Policies and Procedures", "type": "Requirement"},
        "type": "COMPRISES",
    },
]
