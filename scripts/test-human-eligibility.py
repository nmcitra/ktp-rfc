#!/usr/bin/env python3
"""Semantic contract regressions using explicit trusted-integration fixtures.

No test authenticates a real person, validates a qualification, verifies a real
issuer, performs deletion, discovers copies, or simulates those facts with a
signature. Trusted maps stand for independently verified integration outputs.
"""
import copy
from dataclasses import asdict, replace
import importlib.util
import json
import unittest

from jsonschema import Draft202012Validator
import human_eligibility as h
from trajectory_signatures import InvalidRecord, canonical, digest, strict_loads

NOW = 1000


def fixture(level=2, delegated=False):
    d = lambda value: digest({'test_fixture': value}, level)
    scope = dict(zone_id='zone-1', resource_id='service-1',
                 parameters_digest=d('parameters'), purpose_id='service-recovery')
    requirements = [dict(requirement_id=name, assessment_spec_digest=d(name+'-criteria'),
                         issuer_ids=['qualified-issuer'], max_age_seconds=300)
                    for name in ('recovery-training', 'current-assignment')]
    profile = dict(profile_version='ktp-human-eligibility-profile-v1',
        profile_id='service-human-eligibility', version=2, conformance_level=level,
        issuer_registry_digest=d('registry'), governance_authority_id='service-governance',
        review_route_id='eligibility-review', retention_policy_id='human-evidence-retention',
        operations=[dict(operation_id='restart-service', scope=copy.deepcopy(scope),
                        requirements=requirements, grant_issuer_ids=['grant-authority'],
                        allow_delegation=True)])
    request = dict(request_id='request-1', actor_id='agent-1' if delegated else 'human-1',
                   operation_id='restart-service', scope=copy.deepcopy(scope),
                   profile_digest=digest(profile, level))
    evidence = [dict(evidence_id='evidence-'+str(index), version=2,
        principal_id='human-1', requirement_id=requirement['requirement_id'],
        operation_id='restart-service', scope=copy.deepcopy(scope),
        assessment_spec_digest=requirement['assessment_spec_digest'],
        issuer_id='qualified-issuer', observed_at=900, issued_at=905,
        expires_at=1100, status='active', outcome='satisfied',
        content_digest=d(requirement['requirement_id']))
        for index, requirement in enumerate(requirements)]
    grants = [dict(grant_id='grant-1', version=1, principal_id='human-1',
        operation_id='restart-service', scope=copy.deepcopy(scope), issuer_id='grant-authority',
        valid_from=850, expires_at=1200, status='active', delegation_allowed=True)]
    delegations = [dict(delegation_id='delegation-1', version=1, principal_id='human-1',
        delegate_id='agent-1', operation_id='restart-service', scope=copy.deepcopy(scope),
        source_grant_digest=digest(grants[0], level), valid_from=950, expires_at=1150,
        status='active')] if delegated else []
    context = h.TrustedContext('human-1', request['actor_id'], 'agent' if delegated else 'human',
        d('authenticated-session'), profile['profile_id'], digest(profile, level), 2,
        profile['issuer_registry_digest'], 4, NOW, 'active',
        {r['evidence_id']:digest(r,level) for r in evidence},
        {r['grant_id']:digest(r,level) for r in grants},
        {r['delegation_id']:digest(r,level) for r in delegations})
    return dict(level=level, profile=profile, request=request, evidence=evidence,
                grants=grants, delegations=delegations, context=context)


def evaluate(f, now=NOW):
    return h.evaluate_eligibility(f['profile'], f['request'], f['evidence'], f['grants'],
        f['delegations'], context=f['context'], now=now, level=f['level'])


def activate(f, kind):
    id_field = {'evidence':'evidence_id','grants':'grant_id','delegations':'delegation_id'}[kind]
    field = {'evidence':'active_evidence','grants':'active_grants','delegations':'active_delegations'}[kind]
    f['context'] = replace(f['context'], **{field:{r[id_field]:digest(r,f['level']) for r in f[kind]}})


def install(f):
    value = digest(f['profile'], f['level'])
    f['request']['profile_digest'] = value
    f['context'] = replace(f['context'], profile_digest=value)


def erasure_fixture(level=2):
    d = lambda value: digest({'erasure_fixture':value}, level)
    copies = [dict(copy_id=name, kind=kind, recipient_id='recipient-1' if kind=='downstream' else None,
        key_ids=['backup-key'] if kind=='backup' else [], disposition='pending',
        verification_digest=None, acknowledgement_digest=None, retention=None)
        for name, kind in [('primary-copy','primary'),('replica-copy','replica'),
                           ('backup-copy','backup'),('recipient-copy','downstream')]]
    receipt = dict(receipt_version='ktp-privacy-erasure-receipt-v1', receipt_id='receipt-1',
        purpose_id='privacy-erasure', request_digest=d('request'), subject_scope_digest=d('subject-scope'),
        inventory_digest=d('placeholder'), inventory_version=3, scope_cutoff=990,
        evaluated_at=NOW, inventory_complete=True, copies=copies,
        keys=[dict(key_id='backup-key', shared=False, disposition='active', destruction_digest=None)],
        status='pending')
    receipt['inventory_digest'] = digest(h.inventory_body(receipt), level)
    inventory = h.TrustedErasureInventory(receipt['request_digest'], receipt['subject_scope_digest'],
        receipt['inventory_digest'], 3, 990, True, NOW, ['recipient-1'], ['security-audit'], {}, {}, {}, {})
    return dict(receipt=receipt, inventory=inventory, level=level)


def erasure(f, now=NOW):
    return h.verify_erasure_receipt(f['receipt'], inventory=f['inventory'], now=now, level=f['level'])


def reindex(f):
    receipt=f['receipt']
    receipt['inventory_digest']=digest(h.inventory_body(receipt),f['level'])
    f['inventory']=replace(f['inventory'], inventory_digest=receipt['inventory_digest'],
                          inventory_complete=receipt['inventory_complete'])


def erase_copy(f, index, crypto=False):
    receipt=f['receipt']; record=receipt['copies'][index]
    record['disposition']='crypto_erased' if crypto else 'deleted'
    record['verification_digest']=digest({'verified-disposal':record['copy_id']},f['level'])
    f['inventory']=replace(f['inventory'], copy_verifications={
        **f['inventory'].copy_verifications,
        record['copy_id']:digest(h.copy_disposition_body(record),f['level'])})
    if record['kind']=='downstream':
        record['acknowledgement_digest']=digest({'verified-ack':record['copy_id']},f['level'])
        f['inventory']=replace(f['inventory'], recipient_acknowledgements={
            **f['inventory'].recipient_acknowledgements,record['copy_id']:record['acknowledgement_digest']})
    if crypto:
        for key in receipt['keys']:
            if key['key_id'] in record['key_ids']:
                key['disposition']='destroyed'
                key['destruction_digest']=digest({'verified-destruction':key['key_id']},f['level'])
                f['inventory']=replace(f['inventory'],key_destructions={
                    **f['inventory'].key_destructions,key['key_id']:key['destruction_digest']})
    receipt['status']='complete' if all(c['disposition'] in ('deleted','crypto_erased')
        for c in receipt['copies']) and receipt['inventory_complete'] else 'partial'


class HumanEligibilityTests(unittest.TestCase):
    def test_schemas_and_all_supported_levels(self):
        for schema in h.SCHEMAS.values(): Draft202012Validator.check_schema(schema)
        for level in (1,2,3):
            for delegated in (False,True):
                with self.subTest(level=level,delegated=delegated):
                    f=fixture(level,delegated); result=evaluate(f)
                    self.assertEqual('eligible',result['result'])
                    h.validate('decision',result,level)
                    self.assertEqual(1100,result['expires_at'])

    def test_result_is_unsigned_prerequisite_not_person_score_or_authority(self):
        result=evaluate(fixture())
        self.assertNotIn('allow',result); self.assertNotIn('standing',result)
        self.assertNotIn('score',result); self.assertNotIn('signature',result)
        for field in ('person_score','tenure','popularity','salary','risk_score'):
            f=fixture(); f['profile'][field]=100
            with self.subTest(field=field),self.assertRaises(InvalidRecord): evaluate(f)

    def test_request_cannot_nominate_human_or_actor_type(self):
        for field in ('principal_id','human_id','actor_type'):
            f=fixture(); f['request'][field]='human-2'
            with self.subTest(field=field),self.assertRaises(InvalidRecord): evaluate(f)
        f=fixture(); f['request']['actor_id']='human-2'
        with self.assertRaises(InvalidRecord): evaluate(f)
        f=fixture(); f['context']=replace(f['context'],actor_id='human-2')
        with self.assertRaises(InvalidRecord): evaluate(f)

    def test_agent_cannot_switch_to_direct_human_path(self):
        f=fixture(delegated=True); f['delegations']=[]
        self.assertEqual('ineligible',evaluate(f)['result'])
        f['request']['actor_id']='human-1'
        with self.assertRaises(InvalidRecord): evaluate(f)
        f=fixture(delegated=True); f['context']=replace(f['context'],actor_type='human')
        with self.assertRaises(InvalidRecord): evaluate(f)

    def test_missing_requirement_is_ineligible_and_has_review_route(self):
        f=fixture(); f['evidence'].pop()
        result=evaluate(f)
        self.assertEqual('ineligible',result['result'])
        self.assertIn('required_evidence_unavailable',result['reason_codes'])
        self.assertEqual('eligibility-review',result['review_route_id'])
        self.assertEqual(NOW,result['expires_at'])

    def test_requirement_results_identify_the_specific_expired_requirement(self):
        f=fixture(); f['evidence'][1]['expires_at']=NOW; activate(f,'evidence')
        result=evaluate(f)
        details={entry['requirement_id']:entry for entry in result['requirement_results']}
        self.assertEqual('unavailable',details['current-assignment']['result'])
        self.assertEqual(['expired'],details['current-assignment']['reason_codes'])
        self.assertEqual('satisfied',details['recovery-training']['result'])
        self.assertEqual([],details['recovery-training']['reason_codes'])
        self.assertEqual(['evidence-0'],[ref['record_id'] for ref in result['evidence_refs']])
        self.assertEqual(h.references([f['evidence'][1]],'evidence_id',2),
                         details['current-assignment']['considered_refs'])

    def test_alice_identity_misattribution_and_expiry_have_distinct_review_grounds(self):
        for field,value,reason in [('principal_id','another-human','identity_mismatch'),
                                   ('expires_at',NOW,'expired')]:
            f=fixture(); f['evidence'][0][field]=value; activate(f,'evidence')
            result=evaluate(f)
            detail=next(item for item in result['requirement_results']
                        if item['requirement_id']=='recovery-training')
            with self.subTest(field=field):
                self.assertEqual('ineligible',result['result'])
                self.assertEqual([reason],detail['reason_codes'])
                self.assertEqual('unavailable',detail['result'])
                self.assertNotIn('principal_id',detail)
                self.assertEqual({'record_id','version','digest'},
                                 set(detail['considered_refs'][0]))

    def test_untrusted_considered_references_never_become_authoritative_evidence(self):
        f=fixture(); untrusted=copy.deepcopy(f['evidence'][0])
        untrusted.update(evidence_id='unregistered-claim',version=99)
        f['evidence'].append(untrusted)
        result=evaluate(f)
        self.assertEqual('eligible',result['result'])
        detail=next(item for item in result['requirement_results']
                    if item['requirement_id']=='recovery-training')
        self.assertEqual(['evidence-0','unregistered-claim'],
                         [ref['record_id'] for ref in detail['considered_refs']])
        self.assertNotIn('unregistered-claim',[ref['record_id'] for ref in result['evidence_refs']])
        f['evidence']=[record for record in f['evidence'] if record['evidence_id']!='evidence-0']
        result=evaluate(f)
        detail=next(item for item in result['requirement_results']
                    if item['requirement_id']=='recovery-training')
        self.assertEqual('ineligible',result['result'])
        self.assertEqual(['not_current'],detail['reason_codes'])
        self.assertNotIn('unregistered-claim',[ref['record_id'] for ref in result['evidence_refs']])

    def test_current_evidence_identity_issuer_scope_and_criteria_required(self):
        for field,value in [('principal_id','human-2'),('issuer_id','self-appointed'),
                           ('operation_id','delete-service'),('requirement_id','popularity'),
                           ('assessment_spec_digest',digest({'different':'criteria'},2))]:
            f=fixture(); f['evidence'][0][field]=value; activate(f,'evidence')
            with self.subTest(field=field): self.assertEqual('ineligible',evaluate(f)['result'])
        f=fixture(); f['evidence'][0]['scope']['resource_id']='service-2'; activate(f,'evidence')
        self.assertEqual('ineligible',evaluate(f)['result'])

    def test_candidate_evidence_cannot_self_activate(self):
        f=fixture(); f['evidence'][0]['content_digest']=digest({'claim':'replaced'},2)
        self.assertEqual('ineligible',evaluate(f)['result'])
        f=fixture(); f['context']=replace(f['context'],active_evidence={})
        self.assertEqual('ineligible',evaluate(f)['result'])

    def test_correction_replaces_old_active_version_in_fresh_decision(self):
        f=fixture(); old=copy.deepcopy(f['evidence']); first=evaluate(f)
        f['evidence'][0]['version']+=1
        f['evidence'][0]['content_digest']=digest({'corrected':'evidence'},2)
        activate(f,'evidence'); f['context']=replace(f['context'],state_epoch=5)
        second=evaluate(f)
        self.assertEqual('eligible',second['result'])
        self.assertNotEqual(first['evidence_refs'],second['evidence_refs'])
        self.assertNotEqual(first['state_digest'],second['state_digest'])
        f['evidence']=old
        self.assertEqual('ineligible',evaluate(f)['result'])

    def test_restrictive_current_status_and_evidence_status_win(self):
        for status in ('revoked','suspended','unavailable','unknown'):
            f=fixture(); f['context']=replace(f['context'],status=status)
            with self.subTest(status=status): self.assertEqual('ineligible',evaluate(f)['result'])
        for status in ('revoked','suspended','corrected','expired'):
            f=fixture(); f['evidence'][0]['status']=status; activate(f,'evidence')
            with self.subTest(status=status): self.assertEqual('ineligible',evaluate(f)['result'])

    def test_active_authenticated_failed_or_undetermined_criterion_is_not_qualified(self):
        for outcome in ('unsatisfied','undetermined'):
            f=fixture(); f['evidence'][0]['outcome']=outcome
            activate(f,'evidence')
            self.assertEqual('active',f['evidence'][0]['status'])
            with self.subTest(outcome=outcome):
                self.assertEqual('ineligible',evaluate(f)['result'])
        f=fixture(); del f['evidence'][0]['outcome']
        with self.assertRaises(InvalidRecord): evaluate(f)

    def test_expiry_boundary_and_old_observation_cannot_be_refreshed_by_reissue(self):
        f=fixture(); f['context']=replace(f['context'],checked_at=1099)
        self.assertEqual('eligible',evaluate(f,1099)['result'])
        f['context']=replace(f['context'],checked_at=1100)
        self.assertEqual('ineligible',evaluate(f,1100)['result'])
        for changes in ({'issued_at':1001},{'observed_at':1001,'issued_at':1001},
                        {'observed_at':906},{'expires_at':1201},
                        {'observed_at':600,'issued_at':999,'expires_at':1100}):
            f=fixture(); f['evidence'][0].update(changes); activate(f,'evidence')
            with self.subTest(changes=changes): self.assertEqual('ineligible',evaluate(f)['result'])

    def test_eligibility_does_not_create_a_grant(self):
        f=fixture(); f['grants']=[]
        self.assertIn('authority_unavailable',evaluate(f)['reason_codes'])
        for field,value in [('principal_id','human-2'),('issuer_id','human-1'),
                           ('status','revoked'),('valid_from',1001),('expires_at',1000)]:
            f=fixture(); f['grants'][0][field]=value; activate(f,'grants')
            with self.subTest(field=field): self.assertEqual('ineligible',evaluate(f)['result'])

    def test_grant_and_delegation_are_both_required_and_active(self):
        f=fixture(delegated=True); f['context']=replace(f['context'],active_grants={})
        self.assertEqual('ineligible',evaluate(f)['result'])
        f=fixture(delegated=True); f['context']=replace(f['context'],active_delegations={})
        self.assertEqual('ineligible',evaluate(f)['result'])
        f=fixture(delegated=True); f['delegations'][0]['version']+=1
        self.assertEqual('ineligible',evaluate(f)['result'])

    def test_delegation_intersection_prevents_scope_and_expiry_expansion(self):
        for field,value in [('principal_id','human-2'),('delegate_id','agent-2'),
                           ('operation_id','delete-service'),('valid_from',849),
                           ('expires_at',1201),('status','revoked'),
                           ('source_grant_digest',digest({'different':'grant'},2))]:
            f=fixture(delegated=True); f['delegations'][0][field]=value; activate(f,'delegations')
            with self.subTest(field=field): self.assertEqual('ineligible',evaluate(f)['result'])
        f=fixture(delegated=True); f['delegations'][0]['scope']['purpose_id']='marketing'
        activate(f,'delegations'); self.assertEqual('ineligible',evaluate(f)['result'])

    def test_profile_and_grant_must_explicitly_allow_delegation(self):
        f=fixture(delegated=True); f['profile']['operations'][0]['allow_delegation']=False
        install(f); self.assertEqual('ineligible',evaluate(f)['result'])
        f=fixture(delegated=True); f['grants'][0]['delegation_allowed']=False
        activate(f,'grants'); f['delegations'][0]['source_grant_digest']=digest(f['grants'][0],2)
        activate(f,'delegations'); self.assertEqual('ineligible',evaluate(f)['result'])

    def test_corrected_source_grant_requires_fresh_matching_delegation(self):
        f=fixture(delegated=True)
        f['grants'][0]['version']+=1
        activate(f,'grants')
        self.assertEqual('ineligible',evaluate(f)['result'])
        f['delegations'][0]['version']+=1
        f['delegations'][0]['source_grant_digest']=digest(f['grants'][0],2)
        activate(f,'delegations')
        self.assertEqual('eligible',evaluate(f)['result'])

    def test_purpose_and_operation_changes_have_no_implicit_coverage(self):
        for field,value in [('operation_id','delete-service')]:
            f=fixture(); f['request'][field]=value
            result=evaluate(f)
            self.assertEqual('ineligible',result['result'])
            self.assertEqual([],result['requirement_results'])
        for field,value in [('purpose_id','marketing'),('resource_id','service-2'),
                           ('parameters_digest',digest({'broader':'parameters'},2))]:
            f=fixture(); f['request']['scope'][field]=value
            with self.subTest(field=field): self.assertEqual('ineligible',evaluate(f)['result'])

    def test_profile_registry_and_floor_cannot_be_self_selected(self):
        for field,value in [('minimum_profile_version',3),('profile_id','other-profile'),
                           ('profile_digest',digest({'other':'profile'},2)),
                           ('issuer_registry_digest',digest({'other':'registry'},2))]:
            f=fixture(); f['context']=replace(f['context'],**{field:value})
            with self.subTest(field=field),self.assertRaises(InvalidRecord): evaluate(f)
        f=fixture(); f['profile']['operations'][0]['requirements'].pop()
        with self.assertRaises(InvalidRecord): evaluate(f)

    def test_current_state_cannot_be_stale_future_or_candidate_dict(self):
        for value in (999,1001,True,1000.0,None):
            f=fixture(); f['context']=replace(f['context'],checked_at=value)
            with self.subTest(value=value),self.assertRaises(InvalidRecord): evaluate(f)
        f=fixture(); f['context']=asdict(f['context'])
        with self.assertRaises(InvalidRecord): evaluate(f)

    def test_duplicate_definitions_and_conflicting_evidence_fail(self):
        for target,id_field in [('operations','operation_id')]:
            f=fixture(); duplicate=copy.deepcopy(f['profile'][target][0])
            duplicate['scope']['resource_id']='other'; f['profile'][target].append(duplicate)
            with self.assertRaises(InvalidRecord): evaluate(f)
        f=fixture(); req=copy.deepcopy(f['profile']['operations'][0]['requirements'][0])
        req['max_age_seconds']=5; f['profile']['operations'][0]['requirements'].append(req)
        with self.assertRaises(InvalidRecord): evaluate(f)
        f=fixture(); duplicate=copy.deepcopy(f['evidence'][0]); duplicate['version']+=1
        f['evidence'].append(duplicate)
        with self.assertRaises(InvalidRecord): evaluate(f)

    def test_unknown_fields_are_closed_at_every_input_object(self):
        paths=[('profile',),('profile','operations',0),('profile','operations',0,'scope'),
               ('profile','operations',0,'requirements',0),('request',),('request','scope'),
               ('evidence',0),('evidence',0,'scope'),('grants',0),('delegations',0)]
        for path in paths:
            f=fixture(delegated=True); target=f
            for key in path: target=target[key]
            target['extra']='unapproved'
            with self.subTest(path=path),self.assertRaises(InvalidRecord): evaluate(f)

    def test_unsafe_numeric_tokens_and_wildcards_fail(self):
        for value in (True,2.0,0,-1,2**53,float('nan'),float('inf')):
            f=fixture(); f['profile']['version']=value
            with self.subTest(value=value),self.assertRaises(InvalidRecord): evaluate(f)
        for value in ('','*','training?','training\nother','{all}'):
            f=fixture(); f['profile']['operations'][0]['requirements'][0]['requirement_id']=value
            with self.subTest(value=value),self.assertRaises(InvalidRecord): evaluate(f)
        f=fixture(); f['evidence'][0]['observed_at']=900.0
        with self.assertRaises(InvalidRecord): evaluate(f)

    def test_level_three_rejects_all_new_digest_downgrades(self):
        paths=[('profile','issuer_registry_digest'),('profile','operations',0,'scope','parameters_digest'),
               ('profile','operations',0,'requirements',0,'assessment_spec_digest'),
               ('evidence',0,'content_digest'),('request','profile_digest'),
               ('delegations',0,'source_grant_digest')]
        for path in paths:
            f=fixture(3,True); target=f
            for key in path[:-1]: target=target[key]
            target[path[-1]]=digest({'weak':'digest'},2)
            with self.subTest(path=path),self.assertRaises(InvalidRecord): evaluate(f)

    def test_decision_binds_exact_request_active_versions_and_is_deterministic(self):
        f=fixture(delegated=True)
        before=canonical({k:v for k,v in f.items() if k!='context'})
        first=evaluate(f)
        self.assertEqual(digest(f['request'],2),first['request_digest'])
        self.assertEqual(digest(asdict(f['context']),2),first['state_digest'])
        self.assertEqual(sorted(item['requirement_id'] for item in first['requirement_results']),
                         [item['requirement_id'] for item in first['requirement_results']])
        for collection,id_field in [('evidence','evidence_id'),('grants','grant_id'),('delegations','delegation_id')]:
            expected=h.references(f[collection],id_field,2)
            self.assertEqual(expected,first[{'evidence':'evidence_refs','grants':'grant_refs','delegations':'delegation_refs'}[collection]])
            f[collection].reverse()
        self.assertEqual(first,evaluate(f))
        f['evidence'].reverse()
        self.assertEqual(before,canonical({k:v for k,v in f.items() if k!='context'}))
        f['request']['request_id']='request-2'
        self.assertNotEqual(first['request_digest'],evaluate(f)['request_digest'])

    def test_raw_duplicate_nonfinite_unsafe_and_invalid_unicode_fail(self):
        for raw in ('{"x":1,"x":2}','{"x":NaN}','{"x":9007199254740992}',
                    '{"x":9007199254740992.0}','{"x":"\\ud800"}'):
            with self.subTest(raw=raw),self.assertRaises(InvalidRecord): strict_loads(raw)


class HumanPolicyDeclarationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        spec=importlib.util.spec_from_file_location('human_declarations',
            h.ROOT/'scripts/check-declarations.py')
        cls.checker=importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.checker)
        cls.validator=Draft202012Validator(json.loads(
            (h.ROOT/'schemas/deployment-profile.json').read_text()))

    def profile(self):
        profile=copy.deepcopy(self.checker.EXAMPLE)
        human=fixture()['profile']
        profile['human_policy']=dict(mode='operation-eligibility-v1',
            profile_id=human['profile_id'],version=human['version'],digest=digest(human,2))
        return profile

    def test_software_only_omission_and_explicit_human_binding_are_valid_declarations(self):
        for profile in (copy.deepcopy(self.checker.EXAMPLE),self.profile()):
            self.assertEqual([],self.checker.check(profile))
            self.assertTrue(self.validator.is_valid(profile))
        profile=self.profile(); profile.pop('human_policy')
        self.assertEqual([],self.checker.check(profile))
        # Omission is only a valid software-only declaration, never eligibility.

    def test_null_wrong_mode_missing_and_extended_human_bindings_fail(self):
        for value in (None,[],{},dict(self.profile()['human_policy'],mode='general-score'),
                      dict(self.profile()['human_policy'],override=True)):
            profile=self.profile(); profile['human_policy']=value
            with self.subTest(value=value):
                self.assertTrue(self.checker.check(profile))
                self.assertFalse(self.validator.is_valid(profile))
        for key in self.profile()['human_policy']:
            profile=self.profile(); del profile['human_policy'][key]
            with self.subTest(missing=key):
                self.assertTrue(self.checker.check(profile))
                self.assertFalse(self.validator.is_valid(profile))

    def test_human_binding_ids_digests_and_integer_tokens_are_strict(self):
        cases=[('profile_id',value) for value in ('','human *','human?','[human]','human\nother')]
        cases += [('digest',value) for value in (None,'sha256:bad','sha256:'+'A'*64,
                  'sha384:'+'a'*64,'sha256:'+'a'*64+'\n')]
        cases += [('version',value) for value in (True,0,-1,2**53,2.0,float('inf'))]
        for field,value in cases:
            profile=self.profile(); profile['human_policy'][field]=value
            with self.subTest(field=field,value=value):
                self.assertTrue(self.checker.check(profile))
                if type(value) is float and value==2.0:
                    # JSON Schema treats integral floats as integers; the
                    # actual declaration checker enforces the token contract.
                    self.assertTrue(self.validator.is_valid(profile))
                else:
                    self.assertFalse(self.validator.is_valid(profile))


class ErasureReceiptTests(unittest.TestCase):
    def test_pending_partial_and_complete_are_distinct_for_all_levels(self):
        for level in (1,2,3):
            f=erasure_fixture(level); self.assertEqual('pending',erasure(f))
            erase_copy(f,0); self.assertEqual('partial',erasure(f))
            erase_copy(f,1); erase_copy(f,2,crypto=True); erase_copy(f,3)
            self.assertEqual('complete',erasure(f))

    def test_no_inventory_completeness_no_complete_receipt(self):
        f=erasure_fixture(); f['receipt']['inventory_complete']=False; reindex(f)
        for index in range(4): erase_copy(f,index)
        self.assertEqual('partial',erasure(f))
        f['receipt']['status']='complete'
        with self.assertRaises(InvalidRecord): erasure(f)

    def test_backup_replica_or_recipient_omission_cannot_hide_a_copy(self):
        for index in (1,2,3):
            f=erasure_fixture(); f['receipt']['copies'].pop(index)
            with self.subTest(index=index),self.assertRaises(InvalidRecord): erasure(f)
        f=erasure_fixture(); f['receipt']['copies'].pop(3); reindex(f)
        with self.assertRaises(InvalidRecord): erasure(f)

    def test_request_scope_cutoff_and_inventory_are_independently_bound(self):
        for field,value in [('request_digest',digest({'other':'request'},2)),
                           ('subject_scope_digest',digest({'other':'subject'},2)),
                           ('inventory_digest',digest({'other':'inventory'},2)),
                           ('inventory_version',4),('scope_cutoff',999),
                           ('evaluated_at',999),('evaluated_at',1001)]:
            f=erasure_fixture(); f['receipt'][field]=value
            with self.subTest(field=field),self.assertRaises(InvalidRecord): erasure(f)
        f=erasure_fixture(); f['inventory']=replace(f['inventory'],checked_at=999)
        with self.assertRaises(InvalidRecord): erasure(f)
        f=erasure_fixture(); f['receipt']['scope_cutoff']=1001
        reindex(f); f['inventory']=replace(f['inventory'],scope_cutoff=1001)
        with self.assertRaises(InvalidRecord): erasure(f)

    def test_disposal_claim_requires_verified_copy_evidence(self):
        f=erasure_fixture(); erase_copy(f,0)
        f['inventory']=replace(f['inventory'],copy_verifications={})
        with self.assertRaises(InvalidRecord): erasure(f)
        f=erasure_fixture(); erase_copy(f,0)
        f['receipt']['copies'][0]['verification_digest']=digest({'invented':'evidence'},2)
        with self.assertRaises(InvalidRecord): erasure(f)

    def test_downstream_acknowledgement_is_required_and_copy_bound(self):
        for mode in ('absent','unverified','wrong-copy'):
            f=erasure_fixture(); erase_copy(f,3)
            if mode=='absent': f['receipt']['copies'][3]['acknowledgement_digest']=None
            elif mode=='unverified': f['inventory']=replace(f['inventory'],recipient_acknowledgements={})
            else: f['inventory']=replace(f['inventory'],recipient_acknowledgements={
                'primary-copy':f['receipt']['copies'][3]['acknowledgement_digest']})
            with self.subTest(mode=mode),self.assertRaises(InvalidRecord): erasure(f)

    def test_verified_crypto_erasure_cannot_be_relabelled_as_physical_deletion(self):
        f=erasure_fixture(); erase_copy(f,2,crypto=True)
        f['receipt']['keys'][0].update(disposition='active',destruction_digest=None)
        f['inventory']=replace(f['inventory'],key_destructions={})
        with self.assertRaises(InvalidRecord): erasure(f)
        f['receipt']['copies'][2]['disposition']='deleted'
        # The disposal evidence is still the authenticated crypto-erasure claim.
        with self.assertRaises(InvalidRecord): erasure(f)

    def test_crypto_erasure_requires_all_exclusive_keys_and_verified_destruction(self):
        for mode in ('active','unverified','shared','no-key'):
            f=erasure_fixture(); erase_copy(f,2,crypto=True)
            if mode=='active':
                f['receipt']['keys'][0].update(disposition='active',destruction_digest=None)
            elif mode=='unverified': f['inventory']=replace(f['inventory'],key_destructions={})
            elif mode=='shared': f['receipt']['keys'][0]['shared']=True; reindex(f)
            else:
                f['receipt']['copies'][2]['key_ids']=[]; f['receipt']['keys']=[]; reindex(f)
            with self.subTest(mode=mode),self.assertRaises(InvalidRecord): erasure(f)
        f=erasure_fixture(); erase_copy(f,2,crypto=True)
        f['receipt']['keys'].append(dict(key_id='second-key',shared=False,disposition='active',destruction_digest=None))
        f['receipt']['copies'][2]['key_ids'].append('second-key'); reindex(f)
        with self.assertRaises(InvalidRecord): erasure(f)

    def test_retention_is_explicit_purpose_limited_and_never_complete(self):
        f=erasure_fixture()
        for index in (0,1,3): erase_copy(f,index)
        exception=dict(exception_id='exception-1',purpose_id='security-audit',
            access_policy_digest=digest({'restricted':'access'},2),delete_by=1100,
            authorization_digest=digest({'approved':'exception'},2))
        copy_record=f['receipt']['copies'][2]
        copy_record.update(disposition='retained',retention=exception)
        f['inventory']=replace(f['inventory'],retention_authorizations={
            copy_record['copy_id']:digest(exception,2)})
        self.assertEqual('partial',erasure(f))
        original=copy.deepcopy(exception)
        for field,value in [('purpose_id','marketing'),('delete_by',999999),
                           ('access_policy_digest',digest({'public':'access'},2))]:
            copy_record['retention']=dict(original,**{field:value})
            with self.subTest(field=field),self.assertRaises(InvalidRecord): erasure(f)
        copy_record['retention']=original; f['receipt']['status']='complete'
        with self.assertRaises(InvalidRecord): erasure(f)

    def test_expired_retention_deadline_is_visible_and_does_not_count_as_erased(self):
        f=erasure_fixture(); exception=dict(exception_id='overdue-exception',purpose_id='security-audit',
            access_policy_digest=digest({'restricted':'access'},2),delete_by=999,
            authorization_digest=digest({'historical':'exception'},2))
        f['receipt']['copies'][2].update(disposition='retained',retention=exception)
        f['receipt']['status']='partial'
        f['inventory']=replace(f['inventory'],retention_authorizations={'backup-copy':digest(exception,2)})
        self.assertEqual('partial',erasure(f))
        self.assertLess(f['receipt']['copies'][2]['retention']['delete_by'],NOW)

    def test_pending_and_retained_cannot_claim_deletion_at_the_same_time(self):
        f=erasure_fixture(); f['receipt']['copies'][0]['verification_digest']=digest({'fake':'erase'},2)
        with self.assertRaises(InvalidRecord): erasure(f)
        f=erasure_fixture(); erase_copy(f,0)
        f['receipt']['copies'][0]['retention']={}
        with self.assertRaises(InvalidRecord): erasure(f)

    def test_receipt_overstatement_and_understatement_both_fail(self):
        f=erasure_fixture(); f['receipt']['status']='complete'
        with self.assertRaises(InvalidRecord): erasure(f)
        f=erasure_fixture(); erase_copy(f,0); f['receipt']['status']='pending'
        with self.assertRaises(InvalidRecord): erasure(f)

    def test_receipt_unknown_fields_duplicates_tokens_and_digest_downgrade_fail(self):
        for path in [(),('copies',0),('keys',0)]:
            f=erasure_fixture(); target=f['receipt']
            for key in path: target=target[key]
            target['clear_revocation']=True
            with self.subTest(path=path),self.assertRaises(InvalidRecord): erasure(f)
        f=erasure_fixture(); other=copy.deepcopy(f['receipt']['copies'][0]); other['disposition']='deleted'
        f['receipt']['copies'].append(other)
        with self.assertRaises(InvalidRecord): erasure(f)
        for value in (True,3.0,0,2**53):
            f=erasure_fixture(); f['receipt']['inventory_version']=value
            with self.subTest(value=value),self.assertRaises(InvalidRecord): erasure(f)
        f=erasure_fixture(3); f['receipt']['request_digest']=digest({'weak':'digest'},2)
        with self.assertRaises(InvalidRecord): erasure(f)

    def test_receipt_processing_never_mutates_or_clears_safety_state(self):
        f=erasure_fixture(); before=canonical(f['receipt']); inventory=canonical(asdict(f['inventory']))
        human=fixture(); human['context']=replace(human['context'],status='revoked')
        for _ in range(3): self.assertEqual('pending',erasure(f))
        self.assertEqual(before,canonical(f['receipt']))
        self.assertEqual(inventory,canonical(asdict(f['inventory'])))
        self.assertEqual('ineligible',evaluate(human)['result'])


if __name__=='__main__':
    unittest.main(verbosity=2)
