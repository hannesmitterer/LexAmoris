#!/bin/bash

# LexAmoris Living Covenant Compliance Verification Script
# Version: 1.0.0
# Purpose: Automated verification of G-CSI standards, IPFS anchoring, and Key Trust Protocol

set -e

# Configuration Constants
readonly MIN_IMMUTABLE_PRINCIPLES=3  # NSR, SOV, BIO (minimum critical protections)
readonly MIN_REPLICATION_FACTOR=3    # Minimum IPFS pinning replicas for resilience
readonly MIN_CRITICAL_ARTIFACTS=5    # living-covenant, trust-anchors, key-trust, compliance, nsr

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Counters
PASS=0
FAIL=0
WARN=0

# Output functions
print_header() {
    echo -e "\n${BLUE}================================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}================================================${NC}\n"
}

print_test() {
    echo -n "  Testing: $1 ... "
}

print_pass() {
    echo -e "${GREEN}✓ PASS${NC}"
    ((PASS++))
}

print_fail() {
    echo -e "${RED}✗ FAIL${NC}"
    echo -e "    ${RED}$1${NC}"
    ((FAIL++))
}

print_warn() {
    echo -e "${YELLOW}⚠ WARN${NC}"
    echo -e "    ${YELLOW}$1${NC}"
    ((WARN++))
}

# Check if jq is available
check_jq() {
    if ! command -v jq &> /dev/null; then
        echo -e "${YELLOW}Warning: jq is not installed. Some validations will be skipped.${NC}"
        echo -e "${YELLOW}Install with: apt-get install jq (Debian/Ubuntu) or brew install jq (macOS)${NC}\n"
        return 1
    fi
    return 0
}

HAS_JQ=0
check_jq && HAS_JQ=1

# Test functions
test_file_exists() {
    local file=$1
    local desc=$2
    print_test "$desc exists"
    if [ -f "$file" ]; then
        print_pass
        return 0
    else
        print_fail "File not found: $file"
        return 1
    fi
}

test_json_valid() {
    local file=$1
    local desc=$2
    if [ $HAS_JQ -eq 0 ]; then
        return 0
    fi
    
    print_test "$desc is valid JSON"
    if jq empty "$file" 2>/dev/null; then
        print_pass
        return 0
    else
        print_fail "Invalid JSON in $file"
        return 1
    fi
}

test_json_field() {
    local file=$1
    local query=$2
    local expected=$3
    local desc=$4
    
    if [ $HAS_JQ -eq 0 ]; then
        return 0
    fi
    
    print_test "$desc"
    local actual=$(jq -r "$query" "$file" 2>/dev/null)
    if [ "$actual" = "$expected" ]; then
        print_pass
        return 0
    else
        print_fail "Expected '$expected', got '$actual'"
        return 1
    fi
}

test_json_field_exists() {
    local file=$1
    local query=$2
    local desc=$3
    
    if [ $HAS_JQ -eq 0 ]; then
        return 0
    fi
    
    print_test "$desc"
    local result=$(jq -r "$query" "$file" 2>/dev/null)
    if [ "$result" != "null" ] && [ -n "$result" ]; then
        print_pass
        return 0
    else
        print_fail "Field not found or null: $query"
        return 1
    fi
}

# Main verification sections

verify_living_covenant() {
    print_header "Living Covenant Verification"
    
    local file="living-covenant.json"
    test_file_exists "$file" "Living Covenant" || return
    test_json_valid "$file" "Living Covenant" || return
    
    test_json_field "$file" '.covenant.name' 'Lex Amoris - Law of Love' "Covenant name"
    test_json_field "$file" '.governance.model' 'distributed-consensus' "Governance model"
    test_json_field_exists "$file" '.covenant.principles[] | select(.id == "NSR-001")' "NSR-001 principle exists"
    test_json_field_exists "$file" '.covenant.principles[] | select(.id == "SOV-001")' "SOV-001 principle exists"
    test_json_field_exists "$file" '.covenant.principles[] | select(.id == "BIO-001")' "BIO-001 principle exists"
    test_json_field_exists "$file" '.covenant.principles[] | select(.id == "IMMUT-001")' "IMMUT-001 principle exists"
    
    # Check immutability
    if [ $HAS_JQ -eq 1 ]; then
        print_test "All critical principles are immutable (>= $MIN_IMMUTABLE_PRINCIPLES)"
        local immutable_count=$(jq '[.covenant.principles[] | select(.immutable == true)] | length' "$file")
        if [ "$immutable_count" -ge "$MIN_IMMUTABLE_PRINCIPLES" ]; then
            print_pass
        else
            print_fail "Only $immutable_count immutable principles found, expected >= $MIN_IMMUTABLE_PRINCIPLES"
        fi
    fi
}

verify_ipfs_anchoring() {
    print_header "IPFS Anchoring Verification"
    
    local file="ipfs-anchoring.json"
    test_file_exists "$file" "IPFS Anchoring config" || return
    test_json_valid "$file" "IPFS Anchoring config" || return
    
    test_json_field "$file" '.ipfs.enabled' 'true' "IPFS enabled"
    test_json_field "$file" '.ipfs.pinning.enabled' 'true' "Pinning enabled"
    test_json_field "$file" '.anchoring.strategy' 'content-addressed-immutable' "Anchoring strategy"
    test_json_field "$file" '.security.killSwitchPrevention' 'true' "Kill switch prevention"
    
    # Check minimum replication
    if [ $HAS_JQ -eq 1 ]; then
        print_test "Minimum replication >= $MIN_REPLICATION_FACTOR"
        local min_rep=$(jq -r '.ipfs.pinning.minReplication' "$file")
        if [ "$min_rep" -ge "$MIN_REPLICATION_FACTOR" ]; then
            print_pass
        else
            print_fail "Minimum replication is $min_rep, should be >= $MIN_REPLICATION_FACTOR"
        fi
        
        # Check critical artifacts
        print_test "All critical artifacts configured (>= $MIN_CRITICAL_ARTIFACTS)"
        local critical_count=$(jq '[.anchoring.artifacts[] | select(.critical == true)] | length' "$file")
        if [ "$critical_count" -ge "$MIN_CRITICAL_ARTIFACTS" ]; then
            print_pass
        else
            print_fail "Only $critical_count critical artifacts found, expected >= $MIN_CRITICAL_ARTIFACTS"
        fi
    fi
}

verify_key_trust_protocol() {
    print_header "Key Trust Protocol Verification"
    
    local file="key-trust-protocol.json"
    test_file_exists "$file" "Key Trust Protocol" || return
    test_json_valid "$file" "Key Trust Protocol" || return
    
    test_json_field "$file" '.conformsTo' 'ETSI TS 119 612 V2.2.1' "ETSI conformance"
    test_json_field "$file" '.trustFramework.type' 'distributed-web-of-trust' "Trust framework type"
    test_json_field "$file" '.signatureStandards.primary' 'XAdES' "Signature standard"
    test_json_field_exists "$file" '.trustAnchors.anchors[] | select(.id == "TA-001")' "Root trust anchor exists"
    test_json_field_exists "$file" '.trustAnchors.anchors[] | select(.id == "TA-002")' "Bio-ethical validator exists"
    test_json_field_exists "$file" '.trustAnchors.anchors[] | select(.id == "TA-003")' "Sovereignty guardian exists"
}

verify_trust_anchors() {
    print_header "Trust Anchors Manifest Verification"
    
    local file="trust-anchors.json"
    test_file_exists "$file" "Trust Anchors manifest" || return
    test_json_valid "$file" "Trust Anchors manifest" || return
    
    test_json_field "$file" '.conformsTo' 'ETSI TS 119 612 V2.2.1' "ETSI conformance"
    test_json_field "$file" '.ipfsAnchoring.enabled' 'true' "IPFS anchoring enabled"
    test_json_field "$file" '.signature.signatureFormat' 'XAdES-EPES' "Signature format"
    
    # Check trust service providers
    if [ $HAS_JQ -eq 1 ]; then
        print_test "Trust service providers defined"
        local tsp_count=$(jq '[.trustServiceProviders[]] | length' "$file")
        if [ "$tsp_count" -ge 1 ]; then
            print_pass
        else
            print_fail "No trust service providers found"
        fi
    fi
}

verify_gcsi_compliance() {
    print_header "G-CSI Compliance Verification"
    
    local file="g-csi-compliance.json"
    test_file_exists "$file" "G-CSI Compliance config" || return
    test_json_valid "$file" "G-CSI Compliance config" || return
    
    test_json_field "$file" '.standard' 'G-CSI-2026' "Standard version"
    test_json_field "$file" '.governance.structure.type' 'distributed-autonomous' "Governance structure"
    test_json_field "$file" '.security.framework' 'defense-in-depth' "Security framework"
    test_json_field "$file" '.identity.model' 'self-sovereign' "Identity model"
    
    # Check controls
    if [ $HAS_JQ -eq 1 ]; then
        print_test "Governance controls implemented"
        local gov_controls=$(jq '[.governance.controls[] | select(.status == "implemented")] | length' "$file")
        if [ "$gov_controls" -ge 1 ]; then
            print_pass
        else
            print_fail "No implemented governance controls found"
        fi
        
        print_test "Security controls active"
        local sec_controls=$(jq '[.security.controls[] | select(.status == "active")] | length' "$file")
        if [ "$sec_controls" -ge 1 ]; then
            print_pass
        else
            print_fail "No active security controls found"
        fi
    fi
}

verify_nsr_enforcement() {
    print_header "NSR Enforcement Verification"
    
    local file="nsr-enforcement.json"
    test_file_exists "$file" "NSR Enforcement config" || return
    test_json_valid "$file" "NSR Enforcement config" || return
    
    test_json_field "$file" '.nsr.enforcement' 'mandatory-immediate' "NSR enforcement"
    test_json_field "$file" '.nsr.immutable' 'true' "NSR immutability"
    test_json_field "$file" '.validationEngine.type' 'real-time-multi-layer' "Validation engine type"
    test_json_field "$file" '.monitoring.continuous' 'true' "Continuous monitoring"
    
    # Check validation layers
    if [ $HAS_JQ -eq 1 ]; then
        print_test "Constitutional check is blocking"
        local const_check=$(jq -r '.validationEngine.layers[] | select(.name == "Constitutional Check") | .blocking' "$file")
        if [ "$const_check" = "true" ]; then
            print_pass
        else
            print_fail "Constitutional check is not blocking"
        fi
        
        print_test "Bio-ethical assessment is blocking"
        local bio_check=$(jq -r '.validationEngine.layers[] | select(.name == "Bio-Ethical Assessment") | .blocking' "$file")
        if [ "$bio_check" = "true" ]; then
            print_pass
        else
            print_fail "Bio-ethical assessment is not blocking"
        fi
    fi
}

verify_cross_references() {
    print_header "Cross-Reference Verification"
    
    if [ $HAS_JQ -eq 0 ]; then
        echo "  Skipping cross-reference checks (jq not available)"
        return
    fi
    
    # Check IPFS anchoring lists all critical files
    print_test "IPFS anchoring includes living-covenant"
    if jq -e '.anchoring.artifacts[] | select(.path == "/living-covenant.json")' ipfs-anchoring.json > /dev/null 2>&1; then
        print_pass
    else
        print_fail "living-covenant.json not in IPFS artifacts"
    fi
    
    print_test "IPFS anchoring includes trust-anchors"
    if jq -e '.anchoring.artifacts[] | select(.path == "/trust-anchors.json")' ipfs-anchoring.json > /dev/null 2>&1; then
        print_pass
    else
        print_fail "trust-anchors.json not in IPFS artifacts"
    fi
    
    print_test "IPFS anchoring includes key-trust-protocol"
    if jq -e '.anchoring.artifacts[] | select(.path == "/key-trust-protocol.json")' ipfs-anchoring.json > /dev/null 2>&1; then
        print_pass
    else
        print_fail "key-trust-protocol.json not in IPFS artifacts"
    fi
    
    print_test "IPFS anchoring includes nsr-enforcement"
    if jq -e '.anchoring.artifacts[] | select(.path == "/nsr-enforcement.json")' ipfs-anchoring.json > /dev/null 2>&1; then
        print_pass
    else
        print_fail "nsr-enforcement.json not in IPFS artifacts"
    fi
}

verify_metadata() {
    print_header "Metadata Verification"
    
    if [ $HAS_JQ -eq 0 ]; then
        echo "  Skipping metadata checks (jq not available)"
        return
    fi
    
    for file in living-covenant.json ipfs-anchoring.json key-trust-protocol.json trust-anchors.json g-csi-compliance.json nsr-enforcement.json; do
        print_test "$file has version"
        if jq -e '.version' "$file" > /dev/null 2>&1; then
            print_pass
        else
            print_fail "No version in $file"
        fi
    done
}

print_summary() {
    print_header "Compliance Verification Summary"
    
    echo -e "  ${GREEN}Passed:${NC}  $PASS"
    echo -e "  ${RED}Failed:${NC}  $FAIL"
    echo -e "  ${YELLOW}Warnings:${NC} $WARN"
    echo
    
    if [ $FAIL -eq 0 ]; then
        echo -e "${GREEN}✓ ALL CHECKS PASSED${NC}"
        echo -e "${GREEN}LexAmoris is COMPLIANT with Living Covenant standards${NC}"
        echo
        echo -e "📜⚖️❤️ Lex Amoris Signature: Protection of the Law of Love active."
        return 0
    else
        echo -e "${RED}✗ COMPLIANCE FAILURES DETECTED${NC}"
        echo -e "${RED}Please review and fix the failed checks above${NC}"
        return 1
    fi
}

# Main execution
main() {
    print_header "LexAmoris Living Covenant Compliance Verification"
    echo "  Version: 1.0.0"
    echo "  Date: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
    echo "  Standard: G-CSI-2026"
    echo
    
    verify_living_covenant
    verify_ipfs_anchoring
    verify_key_trust_protocol
    verify_trust_anchors
    verify_gcsi_compliance
    verify_nsr_enforcement
    verify_cross_references
    verify_metadata
    
    print_summary
}

# Run main function
main
exit_code=$?

exit $exit_code
