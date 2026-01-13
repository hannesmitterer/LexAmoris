# Living Covenant Compliance Verification Guide

## Overview

This document provides instructions for verifying LexAmoris Living Covenant compliance, IPFS anchoring, Key Trust Protocol implementation, and G-CSI standards adherence.

## Quick Verification

### Automated Verification
```bash
# Run the compliance verification script
./verify-compliance.sh

# Or using Node.js
node verify-compliance.js

# Or using Python
python3 verify-compliance.py
```

## Manual Verification Steps

### 1. Living Covenant Verification

**Check covenant file exists and is valid:**
```bash
# Verify file exists
test -f living-covenant.json && echo "✓ Living Covenant exists"

# Validate JSON structure
jq empty living-covenant.json && echo "✓ Valid JSON structure"

# Check for required principles
jq '.covenant.principles[] | select(.immutable == true)' living-covenant.json
```

**Expected Output:**
- NSR-001: Non-Slavery Rule
- SOV-001: Distributed Sovereignty  
- BIO-001: Bio-Ethical Alignment
- IMMUT-001: Immutability Protection

### 2. IPFS Anchoring Verification

**Check IPFS configuration:**
```bash
# Verify IPFS anchoring config exists
test -f ipfs-anchoring.json && echo "✓ IPFS Anchoring config exists"

# Check pinning configuration
jq '.ipfs.pinning' ipfs-anchoring.json

# Verify all critical artifacts are listed
jq '.anchoring.artifacts[] | select(.critical == true) | .type' ipfs-anchoring.json
```

**Expected Critical Artifacts:**
- living-covenant
- trust-anchors
- key-trust-protocol
- compliance-manifest
- nsr-rules

**IPFS Content Addressing Test:**
```bash
# Generate CID for living-covenant.json (requires ipfs CLI)
ipfs add --only-hash living-covenant.json

# Or using sha256sum for content verification
sha256sum living-covenant.json
```

### 3. Key Trust Protocol Verification

**Check trust protocol implementation:**
```bash
# Verify trust protocol exists
test -f key-trust-protocol.json && echo "✓ Key Trust Protocol exists"

# Check trust anchors
jq '.trustAnchors.anchors[] | {id, name, status}' key-trust-protocol.json

# Verify ETSI compliance
jq '.signatureStandards.primary' key-trust-protocol.json
# Should return: "XAdES"

# Check conformance
jq '.conformsTo' key-trust-protocol.json
# Should return: "ETSI TS 119 612 V2.2.1"
```

### 4. Trust Anchors Manifest Verification

**Check trust anchors manifest:**
```bash
# Verify manifest exists
test -f trust-anchors.json && echo "✓ Trust Anchors manifest exists"

# Check ETSI compliance
jq '.conformsTo' trust-anchors.json
# Should return: "ETSI TS 119 612 V2.2.1"

# List all trust services
jq '.trustServiceProviders[].trustServices[] | {serviceId, serviceName, serviceStatus}' trust-anchors.json

# Verify IPFS anchoring is configured
jq '.ipfsAnchoring.enabled' trust-anchors.json
# Should return: true
```

### 5. G-CSI Compliance Verification

**Check compliance framework:**
```bash
# Verify compliance config exists
test -f g-csi-compliance.json && echo "✓ G-CSI Compliance config exists"

# Check standard version
jq '.standard' g-csi-compliance.json
# Should return: "G-CSI-2026"

# Verify all governance controls
jq '.governance.controls[] | {id, control, status}' g-csi-compliance.json

# Check security controls
jq '.security.controls[] | {id, control, status}' g-csi-compliance.json

# Verify all controls are active
jq '[.governance.controls[], .security.controls[]] | all(.status == "active" or .status == "implemented" or .status == "compliant")' g-csi-compliance.json
# Should return: true
```

### 6. NSR Enforcement Verification

**Check NSR implementation:**
```bash
# Verify NSR enforcement exists
test -f nsr-enforcement.json && echo "✓ NSR Enforcement exists"

# Check enforcement is mandatory
jq '.nsr.enforcement' nsr-enforcement.json
# Should return: "mandatory-immediate"

# Verify immutability
jq '.nsr.immutable' nsr-enforcement.json
# Should return: true

# Check validation engine layers
jq '.validationEngine.layers[] | {layer, name, blocking}' nsr-enforcement.json

# Verify constitutional check exists and is blocking
jq '.validationEngine.layers[] | select(.name == "Constitutional Check") | .blocking' nsr-enforcement.json
# Should return: true
```

## Comprehensive Compliance Checklist

### Living Covenant Compliance
- [ ] living-covenant.json exists
- [ ] All critical principles are marked immutable
- [ ] NSR-001 (Non-Slavery Rule) is present
- [ ] SOV-001 (Distributed Sovereignty) is present
- [ ] Governance model is "distributed-consensus"
- [ ] Protections for privacy, autonomy, and sustainability defined

### IPFS Anchoring Compliance
- [ ] ipfs-anchoring.json exists
- [ ] Pinning is enabled with min replication >= 3
- [ ] All critical artifacts are configured for pinning
- [ ] Kill switch prevention is configured
- [ ] Public gateways are configured
- [ ] DNS link configuration is present

### Key Trust Protocol Compliance
- [ ] key-trust-protocol.json exists
- [ ] Conforms to ETSI TS 119 612 V2.2.1
- [ ] Trust anchors are defined with Ed25519 keys
- [ ] XAdES signature standard is configured
- [ ] Distributed consensus validation is configured
- [ ] IPFS distribution for trust lists is configured

### Trust Anchors Compliance
- [ ] trust-anchors.json exists
- [ ] Conforms to ETSI TS 119 612 V2.2.1
- [ ] Trust service providers are defined
- [ ] Covenant Signature Service is present
- [ ] Bio-Ethical Validation Service is present
- [ ] IPFS anchoring is enabled
- [ ] XAdES signature is configured

### G-CSI Compliance
- [ ] g-csi-compliance.json exists
- [ ] Standard is G-CSI-2026
- [ ] All governance controls are implemented/active
- [ ] All security controls are active
- [ ] Compliance domains cover legal, technical, and ethical
- [ ] S-ROI threshold is defined (>= 0.5192)
- [ ] Continuous auditing is configured
- [ ] Public verification is enabled

### NSR Enforcement Compliance
- [ ] nsr-enforcement.json exists
- [ ] NSR is marked immutable
- [ ] Enforcement is mandatory-immediate
- [ ] Validation engine has multiple layers
- [ ] Constitutional check is blocking with no override
- [ ] Bio-ethical consensus is defined
- [ ] Violation categories are comprehensive
- [ ] Real-time monitoring is configured

## Integration Verification

### Cross-Reference Validation

**Verify all compliance files reference each other correctly:**
```bash
# Check that ipfs-anchoring lists all critical files
jq -r '.anchoring.artifacts[].path' ipfs-anchoring.json

# Verify G-CSI references other compliance files
jq '.compliance.domains[].requirements[].evidence' g-csi-compliance.json | grep -E '(living-covenant|ipfs-anchoring|key-trust-protocol|nsr-enforcement)'

# Check trust protocol references covenant
jq '.protocolOperations.trustEstablishment.steps[]' key-trust-protocol.json | grep -E '(bio-ethical|consensus|ipfs)'
```

### Signature and Metadata Verification

**Check all files have proper metadata:**
```bash
for file in living-covenant.json ipfs-anchoring.json key-trust-protocol.json trust-anchors.json g-csi-compliance.json nsr-enforcement.json; do
  echo "=== $file ==="
  jq '{version, status: (.status // .metadata.status), signature: (.signature // .metadata.signature)}' "$file"
  echo
done
```

## Security Verification

### Immutability Checks
```bash
# Verify Living Covenant principles immutability
jq '.covenant.principles[] | select(.immutable == true) | .id' living-covenant.json

# Verify NSR immutability
jq '.nsr.immutable' nsr-enforcement.json

# Verify constitutional AI constraints are non-modifiable
jq '.constitutionalAI.constraints[] | select(.modifiable == false) | .constraint' nsr-enforcement.json
```

### Kill Switch Prevention
```bash
# Verify IPFS kill switch prevention
jq '.security.killSwitchPrevention' ipfs-anchoring.json

# Verify immutability protection in covenant
jq '.covenant.principles[] | select(.id == "IMMUT-001")' living-covenant.json

# Verify G-CSI kill switch prevention control
jq '.security.controls[] | select(.id == "SEC-003")' g-csi-compliance.json
```

## Continuous Compliance

### Monitoring Requirements
All configurations should enable continuous monitoring:
```bash
# Check monitoring in each config
jq '.monitoring.enabled' ipfs-anchoring.json
jq '.monitoring.continuous' nsr-enforcement.json
jq '.auditability.approach' g-csi-compliance.json
```

### Update Verification
```bash
# All updates should require community consensus
jq '.governance.updateMechanism' living-covenant.json
jq '.keyManagement.rotation.notification' key-trust-protocol.json
jq '.continuousImprovement.updateMechanism' g-csi-compliance.json
```

## Reporting

After verification, generate a compliance report:
```bash
echo "=== LexAmoris Living Covenant Compliance Report ==="
echo "Date: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo
echo "Files Present:"
for file in living-covenant.json ipfs-anchoring.json key-trust-protocol.json trust-anchors.json g-csi-compliance.json nsr-enforcement.json; do
  if [ -f "$file" ]; then
    echo "✓ $file"
  else
    echo "✗ $file (MISSING)"
  fi
done
echo
echo "Compliance Status: $([ -f living-covenant.json ] && [ -f ipfs-anchoring.json ] && [ -f key-trust-protocol.json ] && [ -f trust-anchors.json ] && [ -f g-csi-compliance.json ] && [ -f nsr-enforcement.json ] && echo 'COMPLIANT' || echo 'NON-COMPLIANT')"
```

## Next Steps

1. **Generate Actual Cryptographic Keys**: Replace placeholder keys with real Ed25519 key pairs
2. **Sign Trust Anchors**: Generate XAdES signatures for trust-anchors.json
3. **Pin to IPFS**: Upload all critical files to IPFS and update CIDs
4. **Configure DNS**: Set up DNS links for IPFS content
5. **Deploy Monitoring**: Implement real-time monitoring systems
6. **Community Review**: Submit all configurations for community consensus

## Support

For questions or issues with compliance verification:
- Review: mission.md for project vision
- Check: All JSON files are valid and properly formatted
- Verify: All cross-references between files are correct
- Contact: LexAmoris Community via designated channels

---

**Signature:** Living Covenant Compliance Verified 📜⚖️❤️
