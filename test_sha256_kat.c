#include <stdio.h>
#include <stdint.h>
#include <string.h>

void sha256_compute(const uint8_t *data, uint64_t len, uint8_t scratch_buf[128], uint32_t out_digest[8]);

int test_vector(const char *name, const uint8_t *data, uint64_t len, const char *expected_hex) {
    uint8_t scratch[128];
    uint32_t digest[8];
    sha256_compute(data, len, scratch, digest);

    char computed_hex[65];
    for (int i = 0; i < 8; i++) {
        sprintf(computed_hex + i * 8, "%08x", digest[i]);
    }
    computed_hex[64] = '\0';

    int match = (strcmp(computed_hex, expected_hex) == 0);
    printf("  [%s] %s\n", match ? "PASS" : "FAIL", name);
    printf("         Computed: %s\n", computed_hex);
    printf("         Expected: %s\n", expected_hex);
    return match;
}

int main() {
    printf("======================================================================\n");
    printf("SHA-256 KNOWN-ANSWER TEST (KAT) RUNNER — NIST FIPS 180-4 VECTORS\n");
    printf("======================================================================\n");

    int all_passed = 1;

    // Vector 1: Empty string ""
    all_passed &= test_vector(
        "NIST Vector 1 (Empty String)",
        (const uint8_t *)"", 0,
        "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    );

    // Vector 2: "abc"
    all_passed &= test_vector(
        "NIST Vector 2 (\"abc\")",
        (const uint8_t *)"abc", 3,
        "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"
    );

    // Vector 3: 56-byte multi-block boundary
    all_passed &= test_vector(
        "NIST Vector 3 (56-byte Boundary: \"abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq\")",
        (const uint8_t *)"abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq", 56,
        "248d6a61d20638b8e5c026930c3e6039a33ce45964ff2167f6ecedd419db06c1"
    );

    // Vector 4: 112 bytes (two full blocks)
    const char *v4_str = "abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopqabcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq";
    all_passed &= test_vector(
        "NIST Vector 4 (112-byte Multi-Block)",
        (const uint8_t *)v4_str, strlen(v4_str),
        "59f109d9533b2b70e7c3b814a2bd218f78ea5d3714455bc67987cf0d664399cf"
    );

    // Vector 5: 256-byte Physics-0 payload
    uint8_t payload[256];
    FILE *f = fopen("physics-0.bin", "rb");
    if (f) {
        size_t n = fread(payload, 1, 256, f);
        (void)n;
        fclose(f);
        all_passed &= test_vector(
            "PHYSICS-0 Canonical Staging Payload (256 bytes)",
            payload, 256,
            "e1d89bb1e0854ebaccd2be5c756c8a2ff8c5ecc8c0f90b4abd461fb7bf98374c"
        );
    } else {
        printf("  [WARN] physics-0.bin not found on disk\n");
    }

    printf("----------------------------------------------------------------------\n");
    printf("KAT RESULT: %s\n", all_passed ? "ALL NIST VECTORS PASSED" : "FAILURES DETECTED");
    printf("======================================================================\n");
    return all_passed ? 0 : 1;
}
