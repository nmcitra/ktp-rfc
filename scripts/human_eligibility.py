#!/usr/bin/env python3
"""Narrow human-eligibility and erasure-accounting reference, not an authorizer.

All Trusted* inputs MUST be independently authenticated by the integration.
Constructing a dataclass, parsing candidate records, or copying matching digest
strings establishes no human identity, issuer authority, factual qualification,
current status, actual disposal, or complete inventory. This module does not
verify signatures, issue ordinary proofs, enforce storage/access policy, execute
erasure, or clear revocation. Returned decision/receipt bodies are unsigned.
The integration MUST authenticate the complete body, bind the actual request and
ordinary proof, enforce its <=10-second lifetime, recheck current state, and
preserve A/E, Soul, grants, ceilings, privacy flows and execution restrictions.

Only exact scopes and direct human-to-agent delegation are supported. No person
score, tenure, popularity, inferred qualification, broader scope or authority
is computed. Metadata remains linkable personal information.
Raw wire JSON must first use trajectory_signatures.strict_loads (or equivalent
strict parsing); a dictionary cannot reveal duplicate keys already discarded
by a permissive parser. Pinned criterion meaning requires independent review:
closed shapes cannot detect a forbidden person-ranking policy hidden in prose.
"""
from dataclasses import asdict, dataclass
import json
from pathlib import Path
import re

from jsonschema import Draft202012Validator
from trajectory_signatures import (
    InvalidRecord, MAX_INTEGER, canonical, digest, digest_bytes, literal,
)

ROOT = Path(__file__).resolve().parent.parent
SCHEMAS = {name: json.loads((ROOT / 'schemas' / filename).read_text())
           for name, filename in (
               ('profile', 'human-eligibility-profile.json'),
               ('decision', 'human-eligibility-decision.json'),
               ('receipt', 'privacy-erasure-receipt.json'))}
VALIDATORS = {name: Draft202012Validator(schema) for name, schema in SCHEMAS.items()}
for name in ('request', 'evidence', 'grant', 'delegation'):
    VALIDATORS[name] = Draft202012Validator({
        '$ref': '#/$defs/' + name, '$defs': SCHEMAS['profile']['$defs']})


@dataclass(frozen=True)
class TrustedContext:
    """Authenticated live human/session, actor, policy and correction state.

    Active maps contain record ID -> digest of its entire canonical record,
    including version and status. The integration authenticates issuer/scope,
    content, grants and delegation authority before activating those records.
    checked_at must equal evaluation time; a field alone proves no live read.
    """
    principal_id: str
    actor_id: str
    actor_type: str
    authentication_digest: str
    profile_id: str
    profile_digest: str
    minimum_profile_version: int
    issuer_registry_digest: str
    state_epoch: int
    checked_at: int
    status: str
    active_evidence: dict
    active_grants: dict
    active_delegations: dict


@dataclass(frozen=True)
class TrustedErasureInventory:
    """Externally authenticated inventory and verified disposal evidence.

    copy_verifications maps each copy ID to the canonical digest of its exact
    {copy_id, disposition, verification_digest} claim, so a verified erasure
    method cannot be relabeled. Key maps bind IDs to destruction evidence.
    Retention maps bind copy IDs to complete canonical exception objects.
    Inventory discovery, recipient completeness, lawful/purpose-limited
    exceptions and real deletion/key destruction remain external obligations.
    """
    request_digest: str
    subject_scope_digest: str
    inventory_digest: str
    inventory_version: int
    scope_cutoff: int
    inventory_complete: bool
    checked_at: int
    known_recipient_ids: list
    allowed_retention_purposes: list
    copy_verifications: dict
    key_destructions: dict
    recipient_acknowledgements: dict
    retention_authorizations: dict


def integer(value, positive=False):
    if type(value) is not int or not int(positive) <= value <= MAX_INTEGER:
        raise InvalidRecord('expected bounded exact integer token')


def check_digest(value, level):
    algorithm, size = ('sha384', 96) if level == 3 else ('sha256', 64)
    if type(value) is not str or not re.fullmatch(
            algorithm + r':[0-9a-f]{' + str(size) + '}', value):
        raise InvalidRecord('digest does not match trusted level')


def exact_values(value, level):
    """This contract has no numeric measurement fields: all numbers are tokens."""
    if type(value) is float:
        raise InvalidRecord('floating representations are not integer tokens')
    if type(value) is dict:
        for name, child in value.items():
            if (name.endswith('_digest') or name == 'digest') and child is not None:
                check_digest(child, level)
            else:
                exact_values(child, level)
    elif type(value) is list:
        for child in value:
            exact_values(child, level)


def validate(kind, value, level):
    digest_bytes(b'', level)
    canonical(value)
    errors = list(VALIDATORS[kind].iter_errors(value))
    if errors:
        raise InvalidRecord(f'{kind} schema: {errors[0].message}')
    exact_values(value, level)
    if kind == 'profile':
        if value['conformance_level'] != level:
            raise InvalidRecord('candidate profile cannot select trusted level')
        unique(value['operations'], 'operation_id')
        for operation in value['operations']:
            unique(operation['requirements'], 'requirement_id')


def unique(records, id_field):
    identifiers = [record[id_field] for record in records]
    if len(set(identifiers)) != len(identifiers):
        raise InvalidRecord(f'duplicate {id_field}')


def active_map(value, level):
    if type(value) is not dict:
        raise InvalidRecord('authenticated active/evidence map must be an object')
    for identifier, record_digest in value.items():
        literal(identifier)
        check_digest(record_digest, level)


def trusted_context(context, now, level):
    if type(context) is not TrustedContext:
        raise InvalidRecord('independently authenticated human context required')
    canonical(asdict(context))
    for name in ('principal_id', 'actor_id', 'profile_id'):
        literal(getattr(context, name))
    if context.actor_type not in ('human', 'agent'):
        raise InvalidRecord('authenticated actor type is unsupported')
    if context.actor_type == 'human' and context.actor_id != context.principal_id:
        raise InvalidRecord('direct actor differs from authenticated human principal')
    for name in ('authentication_digest', 'profile_digest', 'issuer_registry_digest'):
        check_digest(getattr(context, name), level)
    for name in ('minimum_profile_version', 'state_epoch'):
        integer(getattr(context, name), True)
    integer(context.checked_at)
    if context.checked_at != now:
        raise InvalidRecord('current human status must be checked for this evaluation')
    if type(context.status) is not str:
        raise InvalidRecord('invalid current status')
    for name in ('active_evidence', 'active_grants', 'active_delegations'):
        active_map(getattr(context, name), level)


def current(record, id_field, active, level):
    return (record['status'] == 'active'
            and active.get(record[id_field]) == digest(record, level))


def references(records, id_field, level):
    return [{'record_id': record[id_field], 'version': record['version'],
             'digest': digest(record, level)}
            for record in sorted(records, key=lambda item: item[id_field])]


def evidence_issues(record, requirement, request, context, now, level):
    """Minimized review grounds; candidate inclusion is not authentication."""
    issues = []
    if not current(record, 'evidence_id', context.active_evidence, level):
        issues.append('not_current')
    if record['principal_id'] != context.principal_id:
        issues.append('identity_mismatch')
    if record['issuer_id'] not in requirement['issuer_ids']:
        issues.append('issuer_mismatch')
    if (record['operation_id'] != request['operation_id']
            or record['scope'] != request['scope']):
        issues.append('scope_mismatch')
    if record['assessment_spec_digest'] != requirement['assessment_spec_digest']:
        issues.append('criteria_mismatch')
    if record['outcome'] != 'satisfied':
        issues.append(record['outcome'])
    if not record['observed_at'] <= record['issued_at'] < record['expires_at']:
        issues.append('invalid_time')
    if now < record['issued_at']:
        issues.append('not_yet_valid')
    if now >= record['expires_at'] or record['status'] == 'expired':
        issues.append('expired')
    if record['expires_at'] > record['observed_at'] + requirement['max_age_seconds']:
        issues.append('freshness_invalid')
    return sorted(set(issues))


def evaluate_eligibility(profile, request, evidence, grants, delegations, *,
                         context, now, level):
    """Return an unsigned eligible/ineligible prerequisite body; never ALLOW.

    Candidate records must match exact active trusted records. Re-evaluation
    after a correction uses the new active record/version and current epoch.
    An ineligible result cannot relax an upstream veto or grant authority.
    """
    integer(now)
    validate('profile', profile, level)
    validate('request', request, level)
    trusted_context(context, now, level)
    if (profile['profile_id'] != context.profile_id
            or digest(profile, level) != context.profile_digest
            or request['profile_digest'] != context.profile_digest
            or profile['version'] < context.minimum_profile_version
            or profile['issuer_registry_digest'] != context.issuer_registry_digest):
        raise InvalidRecord('installed profile, registry or version floor mismatch')
    if request['actor_id'] != context.actor_id:
        raise InvalidRecord('request actor is not independently authenticated actor')
    for kind, records, id_field in (
            ('evidence', evidence, 'evidence_id'), ('grant', grants, 'grant_id'),
            ('delegation', delegations, 'delegation_id')):
        if type(records) is not list:
            raise InvalidRecord('candidate records must be arrays')
        for record in records:
            validate(kind, record, level)
        unique(records, id_field)
    reasons = []
    requirement_results = []
    expirations = []
    selected_evidence, selected_grants, selected_delegations = [], [], []
    if context.status != 'active':
        reasons.append('current_status_restrictive')
    operation = next((op for op in profile['operations']
                      if op['operation_id'] == request['operation_id']
                      and op['scope'] == request['scope']), None)
    if operation is None:
        reasons.append('operation_unmapped')
    else:
        for requirement in sorted(operation['requirements'],
                                  key=lambda item: item['requirement_id']):
            considered = [record for record in evidence
                          if record['requirement_id'] == requirement['requirement_id']]
            reviews = [(record, evidence_issues(record, requirement, request,
                                               context, now, level))
                       for record in considered]
            matches = [record for record, issues in reviews if not issues]
            requirement_results.append({
                'requirement_id': requirement['requirement_id'],
                'result': 'satisfied' if matches else 'unavailable',
                'reason_codes': ([] if matches else sorted(
                    {issue for _, issues in reviews for issue in issues})
                    if considered else ['no_evidence']),
                'considered_refs': references(considered, 'evidence_id', level),
            })
            if not matches:
                reasons.append('required_evidence_unavailable')
            else:
                record = min(matches, key=lambda item: item['evidence_id'])
                selected_evidence.append(record)
                expirations.append(record['expires_at'])
        matching_grants = [record for record in grants if (
            current(record, 'grant_id', context.active_grants, level)
            and record['principal_id'] == context.principal_id
            and record['operation_id'] == request['operation_id']
            and record['scope'] == request['scope']
            and record['issuer_id'] in operation['grant_issuer_ids']
            and record['valid_from'] <= now < record['expires_at'])]
        if not matching_grants:
            reasons.append('authority_unavailable')
        elif context.actor_type == 'human':
            record = min(matching_grants, key=lambda item: item['grant_id'])
            selected_grants.append(record)
            expirations.append(record['expires_at'])
        else:
            pairs = []
            if operation['allow_delegation']:
                for grant in matching_grants:
                    if not grant['delegation_allowed']:
                        continue
                    for record in delegations:
                        if (current(record, 'delegation_id', context.active_delegations, level)
                                and record['principal_id'] == context.principal_id
                                and record['delegate_id'] == context.actor_id
                                and record['source_grant_digest'] == digest(grant, level)
                                and record['operation_id'] == grant['operation_id']
                                and record['scope'] == grant['scope']
                                and grant['valid_from'] <= record['valid_from'] <= now
                                < record['expires_at'] <= grant['expires_at']):
                            pairs.append((grant, record))
            if not pairs:
                reasons.append('delegation_unavailable')
            else:
                grant, record = min(pairs, key=lambda pair:
                                    (pair[0]['grant_id'], pair[1]['delegation_id']))
                selected_grants.append(grant)
                selected_delegations.append(record)
                expirations.extend((grant['expires_at'], record['expires_at']))
    result = {
        'decision_version': 'ktp-human-eligibility-decision-v1',
        'principal_id': context.principal_id, 'actor_id': context.actor_id,
        'actor_type': context.actor_type,
        'authentication_digest': context.authentication_digest,
        'request_digest': digest(request, level), 'profile_digest': context.profile_digest,
        'profile_version': profile['version'],
        'issuer_registry_digest': context.issuer_registry_digest,
        'state_epoch': context.state_epoch, 'state_digest': digest(asdict(context), level),
        'requirement_results': requirement_results,
        'evidence_refs': references(selected_evidence, 'evidence_id', level),
        'grant_refs': references(selected_grants, 'grant_id', level),
        'delegation_refs': references(selected_delegations, 'delegation_id', level),
        'evaluated_at': now,
        'expires_at': now if reasons else min(expirations),
        'result': 'ineligible' if reasons else 'eligible',
        'reason_codes': sorted(set(reasons)), 'review_route_id': profile['review_route_id'],
    }
    validate('decision', result, level)
    return result


def inventory_body(receipt):
    """Exact declared inventory projection, separate from disposal outcomes.

    The independently authenticated digest covers this projection. Ordering is
    by identity; neither missing copies nor different key-sharing declarations
    can be concealed by changing disposal-status fields.
    """
    return {key: receipt[key] for key in (
        'subject_scope_digest', 'inventory_version', 'scope_cutoff', 'inventory_complete')} | {
        'copies': [{key: copy[key] for key in ('copy_id', 'kind', 'recipient_id', 'key_ids')}
                   for copy in sorted(receipt['copies'], key=lambda item: item['copy_id'])],
        'keys': [{key: entry[key] for key in ('key_id', 'shared')}
                 for entry in sorted(receipt['keys'], key=lambda item: item['key_id'])],
    }


def copy_disposition_body(copy):
    """Exact disposal claim independently authenticated by the integration."""
    return {key: copy[key] for key in ('copy_id', 'disposition', 'verification_digest')}


def verify_erasure_receipt(receipt, *, inventory, now, level):
    """Check an unsigned receipt against authenticated inventory/evidence.

    Returns only its accounting status, not proof that physical erasure occurred.
    Does not mutate inventory, delete data, or touch revocation/safety state.
    """
    integer(now)
    validate('receipt', receipt, level)
    if type(inventory) is not TrustedErasureInventory:
        raise InvalidRecord('independently authenticated erasure inventory required')
    canonical(asdict(inventory))
    for name in ('request_digest', 'subject_scope_digest', 'inventory_digest'):
        check_digest(getattr(inventory, name), level)
    integer(inventory.inventory_version, True)
    integer(inventory.scope_cutoff)
    integer(inventory.checked_at)
    if type(inventory.inventory_complete) is not bool:
        raise InvalidRecord('inventory completeness must be independently established')
    if inventory.checked_at != now or not inventory.scope_cutoff <= now:
        raise InvalidRecord('erasure inventory must be current with a nonfuture cutoff')
    for name in ('known_recipient_ids', 'allowed_retention_purposes'):
        values = getattr(inventory, name)
        if type(values) is not list:
            raise InvalidRecord('trusted recipient/purpose inventory must be an array')
        for value in values:
            literal(value)
        if len(set(values)) != len(values):
            raise InvalidRecord('duplicate recipient/purpose inventory')
    for name in ('copy_verifications', 'key_destructions',
                 'recipient_acknowledgements', 'retention_authorizations'):
        active_map(getattr(inventory, name), level)
    for name in ('request_digest', 'subject_scope_digest', 'inventory_digest',
                 'inventory_version', 'scope_cutoff', 'inventory_complete'):
        if receipt[name] != getattr(inventory, name):
            raise InvalidRecord('receipt substituted its request, scope or inventory')
    if receipt['evaluated_at'] != now:
        raise InvalidRecord('receipt is not evaluated at the current checked time')
    unique(receipt['copies'], 'copy_id')
    unique(receipt['keys'], 'key_id')
    if digest(inventory_body(receipt), level) != inventory.inventory_digest:
        raise InvalidRecord('receipt omitted or changed an inventoried copy/key')
    known_keys = {entry['key_id']: entry for entry in receipt['keys']}
    referenced = {key for copy in receipt['copies'] for key in copy['key_ids']}
    if referenced != set(known_keys):
        raise InvalidRecord('copy/key inventory does not resolve exactly')
    recipients = set()
    for entry in receipt['keys']:
        if entry['disposition'] == 'destroyed':
            if (entry['destruction_digest'] is None
                    or inventory.key_destructions.get(entry['key_id']) != entry['destruction_digest']):
                raise InvalidRecord('key destruction lacks independently verified evidence')
        elif entry['destruction_digest'] is not None:
            raise InvalidRecord('active key cannot carry a destruction claim')
    erased = retained = 0
    for copy in receipt['copies']:
        identifier = copy['copy_id']
        if copy['kind'] == 'downstream':
            if copy['recipient_id'] is None:
                raise InvalidRecord('downstream copy must name its actual recipient')
            recipients.add(copy['recipient_id'])
        elif copy['recipient_id'] is not None:
            raise InvalidRecord('non-downstream copy cannot masquerade as recipient accounting')
        ack = copy['acknowledgement_digest']
        if ack is not None and (copy['kind'] != 'downstream'
                or inventory.recipient_acknowledgements.get(identifier) != ack):
            raise InvalidRecord('downstream acknowledgement is unverified or misbound')
        disposition = copy['disposition']
        if disposition in ('deleted', 'crypto_erased'):
            if (copy['verification_digest'] is None
                    or inventory.copy_verifications.get(identifier)
                    != digest(copy_disposition_body(copy), level)):
                raise InvalidRecord('copy erasure lacks independently verified evidence')
            if copy['retention'] is not None:
                raise InvalidRecord('retained copy cannot simultaneously count as erased')
            if copy['kind'] == 'downstream' and ack is None:
                raise InvalidRecord('downstream erasure requires acknowledged disposal')
            if disposition == 'crypto_erased':
                if not copy['key_ids'] or any(known_keys[key]['shared']
                        or known_keys[key]['disposition'] != 'destroyed'
                        for key in copy['key_ids']):
                    raise InvalidRecord('crypto-erasure requires all exclusive keys destroyed')
            erased += 1
        elif disposition == 'retained':
            exception = copy['retention']
            if (exception is None or copy['verification_digest'] is not None
                    or exception['purpose_id'] not in inventory.allowed_retention_purposes
                    or inventory.retention_authorizations.get(identifier) != digest(exception, level)):
                raise InvalidRecord('retention needs a complete independently approved exception')
            retained += 1
        elif copy['verification_digest'] is not None or copy['retention'] is not None:
            raise InvalidRecord('pending copy cannot assert erasure or an undeclared exception')
    if recipients != set(inventory.known_recipient_ids):
        raise InvalidRecord('known downstream recipient omitted or substituted')
    status = ('complete' if inventory.inventory_complete and erased == len(receipt['copies'])
              else 'partial' if erased or retained else 'pending')
    if receipt['status'] != status:
        raise InvalidRecord('receipt overstates or misstates verified erasure progress')
    return status
