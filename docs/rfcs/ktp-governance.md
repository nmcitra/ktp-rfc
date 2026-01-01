Kinetic Trust Protocol                                      C. Perkins
Specification Draft                                           NMCITRA
Version: 0.1                                             November 2025


        Kinetic Trust Protocol (KTP) - Governance Specification

Abstract

   This document specifies the governance model for the Kinetic Trust
   Protocol (KTP) specification itself. It defines how the protocol
   evolves, who makes decisions, how disputes are resolved, and how
   the specification remains open and accessible.

   Governance Recursion applies: the governance of KTP is itself
   subject to principles of transparency, accountability, and
   distributed authority.

Status of This Memo

   This document is a draft specification developed by the New Mexico
   Cyber Intelligence & Threat Response Alliance (NMCITRA).

Copyright Notice

   Copyright (c) 2025 Chris Perkins / NMCITRA.
   Licensed under Apache License, Version 2.0.

Table of Contents

   1.  Introduction  . . . . . . . . . . . . . . . . . . . . . . . .  2
   2.  Governance Principles . . . . . . . . . . . . . . . . . . . .  3
   3.  Organizational Structure  . . . . . . . . . . . . . . . . . .  5
       3.1.  Stewardship Council . . . . . . . . . . . . . . . . . .  5
       3.2.  Technical Committee . . . . . . . . . . . . . . . . . .  7
       3.3.  Working Groups  . . . . . . . . . . . . . . . . . . . .  8
       3.4.  Community . . . . . . . . . . . . . . . . . . . . . . .  9
   4.  Decision Making . . . . . . . . . . . . . . . . . . . . . . . 10
       4.1.  Consensus Process . . . . . . . . . . . . . . . . . . . 10
       4.2.  Voting Procedures . . . . . . . . . . . . . . . . . . . 11
       4.3.  Appeals . . . . . . . . . . . . . . . . . . . . . . . . 12
   5.  Specification Process . . . . . . . . . . . . . . . . . . . . 13
       5.1.  RFC Lifecycle . . . . . . . . . . . . . . . . . . . . . 13
       5.2.  Change Proposals  . . . . . . . . . . . . . . . . . . . 15
       5.3.  Review Process  . . . . . . . . . . . . . . . . . . . . 16
       5.4.  Versioning  . . . . . . . . . . . . . . . . . . . . . . 17
   6.  Intellectual Property . . . . . . . . . . . . . . . . . . . . 19
       6.1.  Licensing . . . . . . . . . . . . . . . . . . . . . . . 19
       6.2.  Patent Policy . . . . . . . . . . . . . . . . . . . . . 20
       6.3.  Trademark Policy  . . . . . . . . . . . . . . . . . . . 21
   7.  Standards Body Alignment  . . . . . . . . . . . . . . . . . . 22
       7.1.  Target Organizations  . . . . . . . . . . . . . . . . . 22
       7.2.  Submission Strategy . . . . . . . . . . . . . . . . . . 23
   8.  Anti-Capture Provisions . . . . . . . . . . . . . . . . . . . 24
       8.1.  Vendor Independence . . . . . . . . . . . . . . . . . . 24
       8.2.  Geographic Diversity  . . . . . . . . . . . . . . . . . 25
       8.3.  Fork Rights . . . . . . . . . . . . . . . . . . . . . . 26
   9.  Funding Model . . . . . . . . . . . . . . . . . . . . . . . . 27
   10. Amendment Process . . . . . . . . . . . . . . . . . . . . . . 28
   11. References  . . . . . . . . . . . . . . . . . . . . . . . . . 29
   Appendix A.  Initial Stewardship Council  . . . . . . . . . . . . 30
   Authors' Addresses  . . . . . . . . . . . . . . . . . . . . . . . 31


1.  Introduction

   A specification without governance eventually dies or becomes
   captured. HTTP thrives because of W3C stewardship. OpenSSL
   struggled without clear governance until OpenSSL Foundation
   formed. KTP requires explicit governance to survive and serve
   its purpose.

   This document answers:

   - Who decides what goes into KTP?
   - How are disputes resolved?
   - How does the specification evolve?
   - Who owns the intellectual property?
   - How do we prevent corporate capture?
   - How is governance itself governed?

   The last question is critical. Governance Recursion means the
   governance structure is itself subject to the principles it
   enforces: transparency, accountability, distributed authority.


2.  Governance Principles

   PRINCIPLE 1: OPENNESS
   KTP is an open specification. Anyone can:
   - Read the specifications (free, no registration)
   - Propose changes (public process)
   - Implement the protocol (royalty-free)
   - Fork if governance fails (Apache 2.0)

   PRINCIPLE 2: TRANSPARENCY
   All governance decisions are:
   - Made in public (or promptly published if emergency)
   - Documented with rationale
   - Archived indefinitely
   - Searchable and accessible

   PRINCIPLE 3: DISTRIBUTED AUTHORITY
   No single entity controls KTP:
   - Stewardship Council has multiple constituencies
   - Technical Committee has diverse membership
   - Major decisions require supermajority
   - Veto power is limited and documented

   PRINCIPLE 4: MERITOCRACY
   Influence is earned through contribution:
   - Code contributions
   - Specification writing
   - Implementation experience
   - Community support
   - Security research

   PRINCIPLE 5: CONSENSUS-SEEKING
   Decisions prefer consensus over voting:
   - Discussion before decision
   - Address concerns substantively
   - Voting as last resort
   - Documented dissent is legitimate

   PRINCIPLE 6: ACCOUNTABILITY
   Decision-makers are accountable:
   - Term limits for leadership positions
   - Recall procedures for misconduct
   - Financial transparency
   - Conflict of interest disclosure

   PRINCIPLE 7: MISSION ALIGNMENT
   Governance serves the mission:
   - Trust infrastructure for human-AI systems
   - Privacy as a fundamental right
   - Security without surveillance
   - Individuals before institutions

   When principles conflict, they are prioritized as listed.
   Openness trumps efficiency. Privacy trumps convenience.


3.  Organizational Structure

3.1.  Stewardship Council

   The Stewardship Council is the highest governance body.

3.1.1.  Composition

   Seven (7) members representing:

   - 2 seats: Academic/Research institutions
   - 2 seats: Implementing organizations
   - 1 seat: Privacy/Civil liberties advocacy
   - 1 seat: International/Non-US constituency
   - 1 seat: Individual contributor (not affiliated with large org)

   No single organization may hold more than one seat.
   Organizations with >$1B annual revenue: Maximum 2 seats total.

3.1.2.  Responsibilities

   The Stewardship Council:

   - Sets strategic direction
   - Approves major specification versions
   - Resolves disputes escalated from Technical Committee
   - Manages intellectual property
   - Oversees financial matters
   - Appoints Technical Committee chair
   - Amends governance documents

3.1.3.  Terms

   - Term length: 3 years
   - Term limit: 2 consecutive terms (may return after 1 term gap)
   - Staggered terms: Approximately 2-3 seats up each year
   - Vacancies: Filled by Council appointment until next election

3.1.4.  Selection

   - Academic seats: Elected by participating academic institutions
   - Implementer seats: Elected by certified implementers
   - Advocacy seat: Appointed by recognized civil liberties org
   - International seat: Elected by non-US participating orgs
   - Individual seat: Elected by individual contributors

   Elections use ranked-choice voting. Quorum: 60% of eligible voters.

3.1.5.  Meetings

   - Quarterly meetings (public, recorded)
   - Annual in-person meeting (location rotates internationally)
   - Emergency meetings as needed (24-hour notice minimum)
   - Minutes published within 7 days

3.2.  Technical Committee

   The Technical Committee manages specification development.

3.2.1.  Composition

   Nine (9) members:

   - Chair (appointed by Stewardship Council)
   - 8 elected members (by active contributors)

   Members must have demonstrated technical contribution.

3.2.2.  Responsibilities

   The Technical Committee:

   - Reviews and approves RFC changes
   - Maintains specification quality
   - Resolves technical disputes
   - Coordinates working groups
   - Recommends major versions to Stewardship Council
   - Manages security vulnerability process

3.2.3.  Terms

   - Term length: 2 years
   - Term limit: 3 consecutive terms
   - Elections: Annual, staggered

3.2.4.  Meetings

   - Monthly meetings (public, recorded)
   - Weekly office hours (open to community)
   - Asynchronous discussion on public mailing list

3.3.  Working Groups

   Working Groups focus on specific areas.

3.3.1.  Standing Working Groups

   - CORE WG: KTP-CORE, KTP-IDENTITY, KTP-ENFORCE
   - SECURITY WG: KTP-CRYPTO, KTP-THREAT-MODEL, security issues
   - OPERATIONS WG: KTP-TRANSPORT, KTP-RECOVERY, KTP-CONFORMANCE
   - PRIVACY WG: KTP-PRIVACY, privacy impact assessments
   - FEDERATION WG: KTP-FEDERATION, KTP-ZONES, KTP-CELESTIAL
   - HUMAN WG: KTP-HUMAN, ethics, governance recursion

3.3.2.  Ad-hoc Working Groups

   Technical Committee may charter ad-hoc WGs for specific issues.
   Ad-hoc WGs have defined scope and sunset date.

3.3.3.  Working Group Chairs

   - Appointed by Technical Committee
   - 2-year terms, renewable
   - Must be active contributor to WG area

3.4.  Community

   Anyone may participate in KTP governance.

3.4.1.  Participation Rights

   All community members may:
   - Participate in mailing lists
   - Submit change proposals
   - Comment on proposals
   - Attend public meetings
   - Access all public documents

3.4.2.  Contributor Status

   Contributors who have:
   - Submitted accepted specification text, OR
   - Submitted accepted code to reference implementation, OR
   - Provided significant review feedback

   Gain voting rights in Technical Committee elections.

3.4.3.  Certified Implementer Status

   Organizations that:
   - Pass Level 1+ conformance testing
   - Maintain active implementation
   - Participate in interoperability testing

   Gain voting rights in Implementer seat elections.


4.  Decision Making

4.1.  Consensus Process

   KTP prefers consensus over voting.

4.1.1.  Consensus Definition

   Consensus means:
   - All major concerns addressed
   - No blocking objections
   - General support (not unanimity)
   - Documented dissent acceptable

4.1.2.  Consensus Process

   1. PROPOSAL: Written proposal with rationale
   2. DISCUSSION: Minimum 2 weeks for non-urgent
   3. RESPONSE: Proposer addresses concerns
   4. CALL FOR CONSENSUS: Chair calls for objections
   5. RESOLUTION: No blocking objections = consensus

   Blocking objection must:
   - Be technical (not preference)
   - Include specific concern
   - Suggest alternative (if possible)

4.1.3.  Timeframes

   - Editorial changes: 1 week discussion
   - Minor changes: 2 weeks discussion
   - Major changes: 4 weeks discussion
   - Breaking changes: 8 weeks discussion

4.2.  Voting Procedures

   When consensus fails, voting decides.

4.2.1.  Technical Committee Votes

   - Quorum: 5 of 9 members
   - Simple majority: Editorial, minor changes
   - 2/3 majority: Major changes
   - 3/4 majority: Breaking changes, process changes

4.2.2.  Stewardship Council Votes

   - Quorum: 5 of 7 members
   - Simple majority: Routine matters
   - 2/3 majority: Strategic decisions
   - Unanimous: Governance amendments

4.2.3.  Vote Recording

   All votes recorded with:
   - Vote tallies (for/against/abstain)
   - Individual votes (named)
   - Rationale for dissenting votes

4.3.  Appeals

   Decisions may be appealed.

4.3.1.  Appeal Process

   1. Working Group decision → Technical Committee
   2. Technical Committee decision → Stewardship Council
   3. Stewardship Council decision → Community vote

   Community vote requires:
   - Petition by 10% of active contributors
   - 2/3 majority to overturn
   - Quorum of 50% of contributors

4.3.2.  Appeal Timeframe

   Appeals must be filed within 30 days of decision.
   Appeal does not stay decision unless harm is irreversible.


5.  Specification Process

5.1.  RFC Lifecycle

   KTP RFCs progress through stages:

   DRAFT
   - Initial proposal
   - Open for major changes
   - Not for production use
   - Format: ktp-name-draft.txt

   CANDIDATE
   - Feature complete
   - Implementation experience required
   - Open for refinement
   - Format: ktp-name-candidate.txt

   STANDARD
   - Stable specification
   - Multiple interoperable implementations
   - Backward compatibility required
   - Format: ktp-name.txt (version in header)

   DEPRECATED
   - Superseded by newer specification
   - Implementations should migrate
   - May be removed after transition period

   HISTORIC
   - No longer recommended
   - Preserved for reference
   - Not removed (archives are permanent)

5.1.1.  Stage Transitions

   DRAFT → CANDIDATE:
   - Technical Committee approval
   - At least one implementation (any level)
   - Public review period (4 weeks minimum)

   CANDIDATE → STANDARD:
   - Stewardship Council approval
   - At least two independent implementations
   - Interoperability demonstrated
   - Security review completed
   - Public review period (8 weeks minimum)

   STANDARD → DEPRECATED:
   - Replacement specification at STANDARD
   - Migration guide published
   - 18-month transition period announced
   - Technical Committee approval

   DEPRECATED → HISTORIC:
   - Transition period complete
   - Technical Committee approval

5.2.  Change Proposals

5.2.1.  Proposal Format

   All change proposals include:

   - Title
   - Author(s)
   - Status (proposed, accepted, rejected, withdrawn)
   - Target RFC(s)
   - Abstract (1 paragraph)
   - Motivation (why is this change needed?)
   - Specification (precise changes)
   - Security Considerations
   - Privacy Considerations (REQUIRED)
   - Backward Compatibility impact
   - References

5.2.2.  Proposal Submission

   1. Submit to mailing list (ktp-proposals@)
   2. Discuss informally
   3. Refine based on feedback
   4. Submit formal proposal (GitHub PR or equivalent)
   5. Enter review process

5.3.  Review Process

5.3.1.  Technical Review

   All proposals require:
   - Working Group review
   - Security WG review (if security-relevant)
   - Privacy WG review (always)
   - At least 2 Technical Committee member reviews

5.3.2.  Public Review

   All proposals have public review period:
   - Editorial: 1 week
   - Minor: 2 weeks
   - Major: 4 weeks
   - Breaking: 8 weeks

   Public comments addressed before acceptance.

5.3.3.  Implementation Review

   For CANDIDATE and STANDARD stages:
   - Implementation experience required
   - Interoperability testing results
   - Performance impact assessment

5.4.  Versioning

5.4.1.  Version Number Format

   KTP uses semantic versioning: MAJOR.MINOR.PATCH

   - MAJOR: Breaking changes (backward incompatible)
   - MINOR: New features (backward compatible)
   - PATCH: Bug fixes, clarifications

5.4.2.  Version Compatibility

   PATCH versions: Fully compatible
   - Implementations should accept any PATCH

   MINOR versions: Forward compatible
   - New features may be ignored by older implementations
   - Older features must still work

   MAJOR versions: Not guaranteed compatible
   - Migration guide required
   - Transition period required
   - Old MAJOR supported for 24 months minimum

5.4.3.  Version Negotiation

   Implementations advertise supported versions.
   Highest mutually-supported version used.
   If no mutual version, connection fails.


6.  Intellectual Property

6.1.  Licensing

6.1.1.  Specification License

   All KTP specifications are licensed under:
   Creative Commons Attribution 4.0 International (CC BY 4.0)

   This allows:
   - Commercial use
   - Derivative works
   - Distribution
   - With attribution

6.1.2.  Reference Implementation License

   Reference implementations are licensed under:
   Apache License, Version 2.0

   This allows:
   - Commercial use
   - Modification
   - Distribution
   - Patent rights
   - With attribution and license notice

6.1.3.  Contributor License Agreement

   Contributors grant:
   - License to use contribution under project license
   - Patent license for necessary claims
   - Representation of authority to contribute

   CLA is kept minimal to encourage contribution.

6.2.  Patent Policy

6.2.1.  Royalty-Free Commitment

   All participants commit to:
   - Royalty-free licensing of necessary claims
   - No patent litigation against implementers
   - Defensive termination only

6.2.2.  Patent Disclosure

   Participants must disclose:
   - Known patents potentially reading on specification
   - Within 60 days of becoming aware
   - Publicly, to mailing list

6.2.3.  Defensive Patent Pool

   Consider joining Open Invention Network or similar pool.
   Mutual non-aggression among KTP implementers.

6.3.  Trademark Policy

6.3.1.  Trademark Ownership

   "Kinetic Trust Protocol" and "KTP" trademarks held by:
   [TBD - neutral foundation or standards body]

   Trademarks protect:
   - Against confusing non-compliant implementations
   - Brand integrity
   - Community trust

6.3.2.  Trademark Usage

   Permitted:
   - Accurate reference to protocol
   - Certification mark for conformant implementations
   - "Compatible with KTP" for tested interoperability

   Not permitted:
   - Implying endorsement without certification
   - Use in product names without license
   - Confusingly similar marks


7.  Standards Body Alignment

7.1.  Target Organizations

7.1.1.  Primary Targets

   IETF (Internet Engineering Task Force)
   - Natural home for protocol specifications
   - Strong process and community
   - Path: Individual draft → WG draft → RFC

   NIST (National Institute of Standards and Technology)
   - Government adoption path
   - Cybersecurity framework alignment
   - Path: Special Publication or standard

7.1.2.  Secondary Targets

   ISO/IEC (International Organization for Standardization)
   - International recognition
   - Formal standardization
   - Path: Via national body (ANSI for US)

   IEEE (Institute of Electrical and Electronics Engineers)
   - Technical standards
   - Industry adoption
   - Path: Standards Association process

   OASIS (Organization for the Advancement of Structured Information Standards)
   - Enterprise/XML focus
   - Open process
   - Path: Technical Committee → OASIS Standard

7.2.  Submission Strategy

7.2.1.  Phased Approach

   Phase 1 (2025-2026): Community development
   - Stabilize core specifications
   - Build implementation base
   - Gather deployment experience

   Phase 2 (2026-2027): IETF engagement
   - Form IETF BOF (Birds of a Feather)
   - Propose Working Group charter
   - Submit Internet-Drafts

   Phase 3 (2027-2028): Formal standardization
   - Progress through IETF process
   - Parallel NIST engagement
   - ISO consideration

7.2.2.  Standards Body Relations

   Maintain liaison relationships with:
   - W3C (Web standards)
   - FIDO Alliance (authentication)
   - OpenID Foundation (identity)
   - Confidential Computing Consortium


8.  Anti-Capture Provisions

8.1.  Vendor Independence

8.1.1.  Specification Independence

   KTP specifications must not:
   - Require specific vendor products
   - Include vendor-specific extensions in core
   - Be encumbered by vendor patents
   - Prefer vendor implementations

8.1.2.  Governance Independence

   Vendor influence is limited by:
   - Seat caps in Stewardship Council
   - Funding caps (no single source >25%)
   - Conflict of interest disclosure
   - Public decision-making

8.1.3.  Capture Warning Signs

   Community should monitor for:
   - Single vendor dominating contributions
   - Technical decisions favoring one implementation
   - Governance nominations from single source
   - Specification changes requiring proprietary features

   If warning signs appear, Stewardship Council must investigate.

8.2.  Geographic Diversity

8.2.1.  International Representation

   Governance must include:
   - Non-US representation on Stewardship Council (mandatory)
   - Working Group chairs from multiple regions
   - Meetings accessible to multiple time zones
   - Documents available in translation (best effort)

8.2.2.  Jurisdictional Neutrality

   KTP specifications must not:
   - Assume specific legal jurisdiction
   - Require compliance with specific nation's laws
   - Exclude participants based on nationality
   - Embed surveillance capabilities

8.3.  Fork Rights

8.3.1.  Right to Fork

   The community always retains the right to fork KTP if:
   - Governance becomes captured
   - Mission alignment lost
   - Openness violated
   - Any other irreconcilable issue

   Apache 2.0 licensing ensures fork rights cannot be revoked.

8.3.2.  Fork Procedure

   If fork deemed necessary:
   1. Public statement of concerns
   2. Good-faith attempt at resolution (30 days)
   3. Community vote on fork (majority of active contributors)
   4. If approved: new governance, new name, continued work

   Fork is last resort, not threat. Governance should make
   fork unnecessary by remaining responsive.


9.  Funding Model

9.1.  Funding Sources

   Acceptable funding sources:
   - Implementation certification fees
   - Conference/event fees
   - Sponsorship (with limits)
   - Grants from foundations
   - Government research grants

   Unacceptable funding:
   - Single-source majority funding
   - Funding with specification control strings
   - Funding from entities under sanctions

9.2.  Financial Transparency

   Annual financial report includes:
   - All funding sources (>$1000)
   - All expenditures (>$1000)
   - Reserves
   - Budget for next year

   Published publicly within 90 days of fiscal year end.

9.3.  Funding Limits

   - No single source >25% of annual budget
   - No vendor category >40% of annual budget
   - Minimum 6-month reserve maintained


10.  Amendment Process

10.1.  Governance Amendment Procedure

   This governance document may be amended:

   1. PROPOSAL: Any Stewardship Council member may propose
   2. DISCUSSION: Minimum 30-day public discussion
   3. COUNCIL VOTE: Unanimous Stewardship Council approval
   4. COMMUNITY REVIEW: 30-day community comment period
   5. RATIFICATION: No blocking objections from community

   If community blocking objection:
   - Council must address concerns
   - May proceed with 6/7 Council vote + community vote
   - Community vote requires 2/3 majority of contributors

10.2.  Protected Provisions

   Some provisions require higher threshold to amend:

   - Open licensing (cannot become proprietary)
   - Patent policy (cannot add royalties)
   - Fork rights (cannot be restricted)
   - Privacy principles (cannot weaken)

   These require:
   - Unanimous Council
   - 3/4 community vote
   - 90-day implementation delay


11.  References

   [IETF-PROCESS]
              Bradner, S., "The Internet Standards Process",
              RFC 2026, October 1996.

   [W3C-PROCESS]
              World Wide Web Consortium, "W3C Process Document",
              https://www.w3.org/Consortium/Process/

   [APACHE-GOVERNANCE]
              Apache Software Foundation, "How the ASF Works",
              https://apache.org/foundation/how-it-works.html

   [OPENSSF]  Open Source Security Foundation, "Governance",
              https://openssf.org/about/governance/


Appendix A.  Initial Stewardship Council

   Until formal elections can be held, the initial Stewardship
   Council consists of:

   [TBD - Initial council to be appointed by founding organization
   with commitment to hold elections within 18 months]

   Initial council responsibilities:
   - Establish election procedures
   - Ratify initial specifications
   - Charter initial Working Groups
   - Conduct first elections
   - Transition to elected council


Authors' Addresses

   Chris Perkins
   New Mexico Cyber Intelligence & Threat Response Alliance (NMCITRA)

   Email: cperkins@nmcitra.org
