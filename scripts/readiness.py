#!/usr/bin/env python3
"""Readiness-v1 exact-scope reference verifier; not a complete authorizer.

Checks actual JWS signatures, complete canonical coverage, scope, freshness,
profile and current-state bindings. Registry authentication, assessment quality,
trusted clocks, current subject/request measurement, atomic issuance/activation,
durable revocation and enforcement fencing MUST be supplied independently.
VerifiedOrdinaryProof MUST come from a full ordinary-proof verifier, including
issuer, request, revocation and authorization checks, never from a token parser.
Neither a dataclass constructor nor a candidate's assertion establishes trust.

Only exact scope/configuration matching is supported. The helper cannot certify
range matchers, compatibility assessments, real readiness or stronger crypto
profiles beyond the classical signature subset implemented by its JWS helper.
Dependencies are pinned in .github/workflows/rfc-sync.yml.
"""
from dataclasses import dataclass
from pathlib import Path
import json
import re

from jsonschema import Draft202012Validator

from trajectory_signatures import (
    InvalidRecord, KeyBinding, MAX_INTEGER, READINESS_TYPE,
    READINESS_DECISION_TYPE, canonical, digest, digest_bytes, literal,
    unb64, verify_jws,
)

ROOT = Path(__file__).resolve().parent.parent
VALIDATORS = {
    name: Draft202012Validator(json.loads(
        (ROOT / f'schemas/readiness-{name}.json').read_text()))
    for name in ('profile', 'attestation', 'decision')
}
SUBJECT_FIELDS = {'agent_id', 'lineage_id', 'software_digest', 'model_digest',
                  'configuration_digest', 'toolchain_digest', 'permissions_digest'}
SCOPE_FIELDS = {'zone_id', 'resource_id', 'environment_digest', 'parameters_digest'}
REQUEST_FIELDS = {'request_id', 'subject', 'operation_id', 'scope',
                  'deployment_profile_digest', 'readiness_profile_digest'}
SUPERVISION = {'stable', 'metacognitive', 'assisted', 'regulated', 'silent_veto'}


@dataclass(frozen=True)
class TrustedState:
    """Authenticated live state supplied by the integration, not the applicant.

    checked_at must equal the current evaluation second in this reference.
    The caller must authenticate and fence the status read and protected effect;
    a timestamp field is not evidence of a real query or a monotonic clock.
    Key-valid-until values concern the independently resolved keys/roles.
    """
    profile_id: str
    profile_digest: str
    deployment_profile_digest: str
    assessor_registry_digest: str
    minimum_profile_version: int
    readiness_epoch: int
    active_attestation_digest: str
    challenge: dict
    checked_at: int
    status: str
    assessor_valid_from: int
    assessor_valid_until: int
    issuer_valid_from: int
    issuer_valid_until: int


@dataclass(frozen=True)
class VerifiedOrdinaryProof:
    """Output of independent full ordinary authorization verification.

    token is the complete original compact JWS; its digest uses ASCII bytes.
    request_digest must bind the actual resolved request, not caller labels.
    Constructing this record does NOT verify its token or authorize execution.
    """
    token: str
    request_digest: str
    issued_at: int
    expires_at: int


@dataclass(frozen=True)
class ReadinessEvidence:
    """Verified prerequisite evidence; contributes no standing or grant."""
    attestation_digest: str
    readiness_profile_digest: str
    deployment_profile_digest: str
    request_digest: str
    readiness_epoch: int
    checked_at: int
    expires_at: int


def integer(value, *, positive=False):
    if type(value) is not int or not (int(positive) <= value <= MAX_INTEGER):
        raise InvalidRecord('expected exact nonnegative/positive integer token')


def check_digest(value, level):
    algorithm, count = ('sha384', 96) if level == 3 else ('sha256', 64)
    if type(value) is not str or not re.fullmatch(
            algorithm + r':[0-9a-f]{' + str(count) + '}', value):
        raise InvalidRecord('digest does not match trusted cryptographic level')


def check_digests(value, level):
    if type(value) is dict:
        for key, child in value.items():
            if key.endswith('_digest'):
                check_digest(child, level)
            else:
                check_digests(child, level)
    elif type(value) is list:
        for child in value:
            check_digests(child, level)


def validate(kind, value, level):
    digest_bytes(b'', level)
    canonical(value)
    errors = list(VALIDATORS[kind].iter_errors(value))
    if errors:
        raise InvalidRecord(f'{kind} schema: {errors[0].message}')
    check_digests(value, level)
    if kind == 'profile':
        integer(value['version'], positive=True)
        integer(value['conformance_level'], positive=True)
        if value['conformance_level'] != level:
            raise InvalidRecord('profile cannot select a weaker trusted level')
        seen = set()
        for op in value['operations']:
            integer(op['max_age_seconds'], positive=True)
            if op['operation_id'] in seen:
                raise InvalidRecord('duplicate operation definition')
            seen.add(op['operation_id'])
    elif kind == 'attestation':
        integer(value['readiness_epoch'], positive=True)
        for key in ('assessed_at', 'issued_at', 'expires_at'):
            integer(value[key])
        integer(value['challenge']['issued_at'])
        if len(unb64(value['challenge']['nonce'])) != 32:
            raise InvalidRecord('challenge nonce must encode exactly 32 bytes')
        seen = set()
        for check in value['checks']:
            integer(check['observed_at'])
            if check['check_id'] in seen:
                raise InvalidRecord('duplicate assessment check')
            seen.add(check['check_id'])
    else:
        integer(value['readiness_epoch'], positive=True)
        integer(value['evaluated_at'])
        integer(value['expires_at'])


def payload(envelope):
    return {key: value for key, value in envelope.items() if key != 'signature'}


def request_digest(request, level):
    """Hash an actual independently resolved request in the reference format."""
    canonical(request)
    if type(request) is not dict or set(request) != REQUEST_FIELDS:
        raise InvalidRecord('incomplete or extended actual request')
    for key in ('request_id', 'operation_id'):
        literal(request[key])
    for key, fields in (('subject', SUBJECT_FIELDS), ('scope', SCOPE_FIELDS)):
        child = request[key]
        if type(child) is not dict or set(child) != fields:
            raise InvalidRecord('incomplete request subject or scope')
        for name, value in child.items():
            if not name.endswith('_digest'):
                literal(value)
    check_digests(request, level)
    return digest(request, level)


def verify_readiness(attestation, profile, request, *, state, assessor, now, level):
    """Verify the readiness prerequisite against independently trusted inputs.

    Does not authorize an operation, verify the ordinary proof, issue/consume
    challenges, execute an assessment or authenticate supplied current state.
    """
    integer(now)
    validate('profile', profile, level)
    validate('attestation', attestation, level)
    actual_request_digest = request_digest(request, level)
    if type(state) is not TrustedState or type(assessor) is not KeyBinding:
        raise InvalidRecord('independently verified state and key are required')
    for name in ('minimum_profile_version', 'readiness_epoch'):
        integer(getattr(state, name), positive=True)
    for name in ('checked_at', 'assessor_valid_from', 'assessor_valid_until',
                 'issuer_valid_from', 'issuer_valid_until'):
        integer(getattr(state, name))
    for name in ('profile_digest', 'deployment_profile_digest',
                 'assessor_registry_digest', 'active_attestation_digest'):
        check_digest(getattr(state, name), level)
    if state.status != 'active' or state.checked_at != now:
        raise InvalidRecord('required current status is unavailable or restrictive')
    if not state.assessor_valid_from <= attestation['issued_at'] <= now < state.assessor_valid_until:
        raise InvalidRecord('assessor key/role is no longer current')
    if (profile['profile_id'] != state.profile_id
            or digest(profile, level) != state.profile_digest
            or profile['version'] < state.minimum_profile_version
            or profile['assessor_registry_digest'] != state.assessor_registry_digest):
        raise InvalidRecord('installed profile, registry or policy floor mismatch')
    if (attestation['readiness_profile_digest'] != state.profile_digest
            or request['readiness_profile_digest'] != state.profile_digest
            or attestation['deployment_profile_digest'] != state.deployment_profile_digest
            or request['deployment_profile_digest'] != state.deployment_profile_digest):
        raise InvalidRecord('deployment/readiness profile substitution')
    if (attestation['subject'] != request['subject']
            or attestation['scope'] != request['scope']
            or attestation['operation_id'] != request['operation_id']):
        raise InvalidRecord('subject, configuration, operation or scope mismatch')
    operation = next((op for op in profile['operations']
                      if op['operation_id'] == request['operation_id']), None)
    if operation is None or operation['scope'] != request['scope']:
        raise InvalidRecord('operation has no exact approved readiness scope')
    if (attestation['assessor_id'] not in operation['assessor_ids']
            or assessor.subject != attestation['assessor_id']
            or assessor.zone_id != request['scope']['zone_id']
            or assessor.purpose != READINESS_TYPE):
        raise InvalidRecord('assessor identity, scope or signature role mismatch')
    if attestation['assessment_spec_digest'] != operation['assessment_spec_digest']:
        raise InvalidRecord('assessment criteria changed')
    if (set(check['check_id'] for check in attestation['checks'])
            != set(operation['required_checks'])):
        raise InvalidRecord('assessment did not cover exactly the required checks')
    if attestation['challenge'] != state.challenge:
        raise InvalidRecord('challenge is not the authenticated assessment instance')
    times = [check['observed_at'] for check in attestation['checks']]
    if not (attestation['challenge']['issued_at'] <= min(times)
            <= max(times) <= attestation['assessed_at']
            <= attestation['issued_at'] <= now < attestation['expires_at']
            <= min(times) + operation['max_age_seconds']):
        raise InvalidRecord('assessment chronology or evidence freshness failed')
    if attestation['expires_at'] > state.assessor_valid_until:
        raise InvalidRecord('assessment outlives trusted assessor key/role validity')
    if (attestation['readiness_epoch'] != state.readiness_epoch
            or digest(attestation, level) != state.active_attestation_digest):
        raise InvalidRecord('readiness is not the current activated assessment')
    verify_jws(attestation['signature'], payload(attestation), assessor, level=level)
    return ReadinessEvidence(
        digest(attestation, level), state.profile_digest,
        state.deployment_profile_digest, actual_request_digest,
        state.readiness_epoch, now, attestation['expires_at'])


def proof_digest(proof, expected_request_digest, *, now, level):
    """Additional binding/lifetime checks on an already fully verified proof."""
    if type(proof) is not VerifiedOrdinaryProof:
        raise InvalidRecord('a separately verified ordinary proof is required')
    integer(proof.issued_at)
    integer(proof.expires_at)
    if (proof.request_digest != expected_request_digest
            or not 0 < proof.expires_at - proof.issued_at <= 10
            or not proof.issued_at <= now < proof.expires_at):
        raise InvalidRecord('ordinary proof request binding or lifetime failed')
    if type(proof.token) is not str or len(proof.token.split('.')) != 3:
        raise InvalidRecord('ordinary proof must retain complete compact JWS bytes')
    for part in proof.token.split('.'):
        unb64(part)
    return digest_bytes(proof.token.encode('ascii'), level)


def decision_body(evidence, proof, *, issuer_id, issuer_valid_until, now, level):
    """Construct the sidecar signing payload after all prerequisite checks.

    Only an independently authorized issuer may sign this body after full
    ordinary authorization and a fenced current-state check. This constructor
    is not an issuance approval or a complete authorizer.
    """
    integer(now)
    integer(issuer_valid_until)
    literal(issuer_id)
    if (type(evidence) is not ReadinessEvidence or evidence.checked_at != now
            or not now < min(evidence.expires_at, issuer_valid_until)):
        raise InvalidRecord('readiness was not verified for this evaluation')
    proof_hash = proof_digest(proof, evidence.request_digest, now=now, level=level)
    if proof.expires_at > evidence.expires_at:
        raise InvalidRecord('ordinary proof outlives its required readiness')
    return {
        'decision_version': 'ktp-readiness-decision-v1',
        'request_digest': evidence.request_digest,
        'proof_digest': proof_hash,
        'attestation_digest': evidence.attestation_digest,
        'readiness_profile_digest': evidence.readiness_profile_digest,
        'deployment_profile_digest': evidence.deployment_profile_digest,
        'readiness_epoch': evidence.readiness_epoch,
        'evaluated_at': now,
        'expires_at': min(proof.expires_at, evidence.expires_at, issuer_valid_until),
        'issuer_id': issuer_id,
    }


def verify_decision(decision, attestation, profile, request, proof, *,
                    state, assessor, issuer, now, level):
    """Verify a sidecar and recheck live readiness for this dependent action."""
    evidence = verify_readiness(attestation, profile, request, state=state,
                                assessor=assessor, now=now, level=level)
    validate('decision', decision, level)
    proof_hash = proof_digest(proof, evidence.request_digest, now=now, level=level)
    if proof.expires_at > evidence.expires_at:
        raise InvalidRecord('ordinary proof outlives its required readiness')
    expected = {
        'request_digest': evidence.request_digest, 'proof_digest': proof_hash,
        'attestation_digest': evidence.attestation_digest,
        'readiness_profile_digest': evidence.readiness_profile_digest,
        'deployment_profile_digest': evidence.deployment_profile_digest,
        'readiness_epoch': evidence.readiness_epoch,
    }
    if any(decision[key] != value for key, value in expected.items()):
        raise InvalidRecord('sidecar does not bind the current request/proof/evidence')
    if (type(issuer) is not KeyBinding or issuer.purpose != READINESS_DECISION_TYPE
            or issuer.subject != decision['issuer_id']
            or issuer.zone_id != request['scope']['zone_id']):
        raise InvalidRecord('decision issuer or role mismatch')
    if not (max(proof.issued_at, attestation['issued_at'], state.issuer_valid_from)
            <= decision['evaluated_at']
            <= now < decision['expires_at']
            <= min(proof.expires_at, evidence.expires_at, state.issuer_valid_until)):
        raise InvalidRecord('decision chronology or dependent validity failed')
    verify_jws(decision['signature'], payload(decision), issuer, level=level)
    return evidence


def restrict_decision(existing_supervision, *args, **kwargs):
    """Add the readiness restriction to an independently evaluated decision.

    A valid prerequisite leaves the existing result unchanged. A failure vetoes.
    The caller must still enforce grants, A/E, Soul, all ceilings and all other
    requirements; this function cannot make an invalid upstream ALLOW safe.
    """
    if type(existing_supervision) is not str or existing_supervision not in SUPERVISION:
        raise InvalidRecord('unknown upstream supervision result')
    if existing_supervision == 'silent_veto':
        return existing_supervision
    try:
        verify_decision(*args, **kwargs)
    except InvalidRecord:
        return 'silent_veto'
    return existing_supervision
