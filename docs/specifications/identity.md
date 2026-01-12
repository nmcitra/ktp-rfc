# Identity

*Trust who, not just what: vector identity and trajectory-based authentication*

KTP Identity binds entities to their behavior over time and space, not just to static credentials. Trajectory-aware proofs, revocation rules, and attestations keep trust portable without losing accountability.

## Why it matters

- **Vector Identity**: Identity is a stateful vector (who/where/when) with constitutional constraints, not a username or API key.
- **Trajectory authentication**: Continuity of behavior is verified across time slices, stopping replayed or hijacked identities.
- **Revocation and rotation**: Credentials degrade gracefully and can be revoked with evidence, preserving auditability.
- **Attested lineage**: Provenance and sensor attestations travel with the identity so downstream agents can verify claims.

## Jump into the specs

- [KTP-Identity](../rfcs/ktp-identity.md){ .md-button .md-button--primary }
- [KTP-Identity: Vector Identity](../rfcs/ktp-identity.md){ .md-button }
- [KTP-Federation](../rfcs/ktp-federation.md){ .md-button }

## Build with it

- Shape payloads with the [JSON Schemas](../schemas/index.md)
- Test flows using the [Developer Toolkit](../implement/index.md) and [Experience Calculator](../implement/experience-calculator.md)
