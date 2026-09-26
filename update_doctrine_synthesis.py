#!/usr/bin/env python3
import os
import re

def update_doctrine():
    base_dir = "/home/drakestapleton/workspace/aien-architecture/doctrine"
    
    # 1. Update INDEX.md
    index_file = os.path.join(base_dir, "INDEX.md")
    with open(index_file, "r") as f:
        content = f.read()
        
    synthesis_doctrine_section = """
---

## 4. The Sovereign Program-Learning Doctrine (Omega Synthesis → AIEN)

### 4.1 The Synthesis Doctrine
> **`WEIGHTS SUGGEST.`**  
> **`PROGRAMS EXPLAIN.`**  
> **`OMEGA VERIFIES.`**  
> **`PHYSICS AUTHORIZES.`**  
> **`EVIDENCE TEACHES.`**

### 4.2 The Three Speeds of Intelligence
1. **Fast Learning (AIEN Model / Search Prior):** *"What should I try next?"* Implicit, speculative intuition. Search prior over Omega's possibility space. Rapidly retrainable and disposable.
2. **Medium-Term Learning (Omega Procedure Library):** *"What reusable procedures have we discovered?"* Explicit, typed, composable, verifiable semantic subgraphs.
3. **Long-Term Knowledge (Omega Semantics + Proofs + Cortex Evidence):** *"What does this mean? What has been verified? What was observed?"* Durable epistemic ground.

### 4.3 Division of State & Durability
* **Weights** hold search intuition.
* **Programs** hold explicit procedure.
* **Omega Abstractions** hold reusable concepts.
* **Cortex** holds empirical experience.
* **Proofs** hold trusted justification.
* **Physics** holds physical machine authority.

### 4.4 Trust Decomposition Inside OMEGA
The epistemic boundary runs directly through OMEGA. Search and synthesis components are strictly UNTRUSTED; semantic contracts and verification checkers are TRUSTED:

```text
OMEGA
├── OMEGA SEMANTIC CORE          TRUSTED CONTRACT
├── OMEGA VERIFIER               TRUSTED CHECKER
├── OMEGA SYNTHESIS              UNTRUSTED SEARCH
├── OMEGA ABSTRACTION MINER      UNTRUSTED SEARCH
├── OMEGA REALIZATION SEARCH     UNTRUSTED SEARCH
└── OMEGA LIBRARY
      ├── CANDIDATE               UNTRUSTED
      └── VERIFIED/PROMOTED       TRUSTED BY EVIDENCE
```

Canonical Synthesis Pipeline:
```text
AIEN
  ↓
CANDIDATE IDEA

OMEGA SYNTHESIS / COMPOSITION
  ↓
CANDIDATE PROGRAM OR REALIZATION

OMEGA TRUSTED VERIFIER
  ↓
VERIFIED SEMANTIC CANDIDATE

PHYSICS
  ↓
AUTHORIZED PHYSICAL EFFECT
```

### 4.5 Sovereign Training Corpus Scoping
> *Omega's sovereign search traces provide the cold-start training corpus for AIEN-0, removing the need for a foreign pretrained search-guide model or foreign procedural training corpus.*
"""
    if "The Sovereign Program-Learning Doctrine" not in content:
        content = content + "\n" + synthesis_doctrine_section
        
    # Mark Milestone 1 status
    content = content.replace("Milestone 1 (`ALPHA_BOOT`): Passed", "MILESTONE 1 — ALPHA_BOOT: IMPLEMENTED / QUALIFICATION REOPENED")
    
    with open(index_file, "w") as f:
        f.write(content)
    print("Updated INDEX.md")

    # 2. Update ARCHITECTURE.md with the revised 31-milestone roadmap & trust decomposition
    arch_file = os.path.join(base_dir, "ARCHITECTURE.md")
    with open(arch_file, "r") as f:
        arch = f.read()

    revised_roadmap_text = """
## 5. The 31-Milestone Sovereign Program-Learning Roadmap

```text
MILESTONE 0  — DOCTRINE_V1                     Canonical doctrine corpus frozen and ratified. [COMPLETE]
MILESTONE 1  — ALPHA_BOOT                      Canonical alpha.bin bootstrap seed. [IMPLEMENTED / QUALIFICATION REOPENED]
MILESTONE 2  — PHYSICS_BOOT                    Minimal trusted machine authority nucleus.
MILESTONE 3  — PHYSICS_EFFECTS                 Capabilities, EFFECT_INTENT admission cycle, and EFFECT_RECEIPT accounting.
MILESTONE 4  — OMEGA_SEMANTICS                 Core semantic object model and canonical content-addressed identity.
MILESTONE 5  — OMEGA_AARCH64                   Direct bare-metal machine code generation (no LLVM).
MILESTONE 6  — OMEGA_SELF_HOST                 Self-hosting compilation of the minimal Omega realization layer.
MILESTONE 7  — OMEGA_VERIFY                    Epistemic verification kernel:
                                               - REQUIRED: V0 Structural/Type/Capability, V1 Differential, V2 Property/Invariant.
                                               - FRAMEWORK DEFINED FOR: V3 Adversarial, V4 Symbolic, V5 Proof-Carrying.
MILESTONE 8  — OMEGA_PROGRAM_CORE              Semantic procedure graph representation, SYNTHESIS_TASK, and cost models.
MILESTONE 9  — OMEGA_SYNTHESIS_V0              Deterministic typed enumeration and constraint solver solving canonical closed domains.
MILESTONE 10 — OMEGA_LIBRARY_V1                Versioned procedure library, provenance tracking, and library generation tags.
MILESTONE 11 — OMEGA_LIBRARY_DISCOVERY         One nontrivial abstraction not present in the initial library that:
                                               1. Compresses multiple verified programs;
                                               2. Preserves their semantics;
                                               3. Is reused on held-out tasks;
                                               4. Reduces search cost.
MILESTONE 12 — OMEGA_LIVING_MATVEC             Living MatVec selecting among verified realization variants and procedure reuse.
MILESTONE 13 — OMEGA_MACHINE_GRAPH             Hardware topology and transformation description reported by Physics.
MILESTONE 14 — OMEGA_REALIZATION_SYNTHESIS     Synthesis engine applied to physical code generation (G_S x G_M -> G_R).
MILESTONE 15 — PHYSICS_ACCELERATOR_LINK        Zero-copy shared memory rings and capability tables (CPU governor <-> accelerator).
MILESTONE 16 — BLACKWELL_NATIVE_PATH_KNOWN     Native GPU MMIO, queue submission, and doorbell mechanics mapped empirically.
MILESTONE 17 — OMEGA_BLACKWELL_VECTOR          First verified native Blackwell compute realization (general GPU compute).
MILESTONE 18 — OMEGA_BLACKWELL_MATMUL          High-throughput matrix multiplication on Blackwell.
MILESTONE 19 — OMEGA_ACCELERATOR_RESIDENT      Persistent OMEGA execution substrate remains resident in accelerator-accessible
                                               coherent memory and maintains device execution state without repeated host-side initialization.
MILESTONE 20 — OMEGA_TENSOR                    Native tensor algebraic foundations and numeric domains.
MILESTONE 21 — OMEGA_AUTODIFF                  Symbolic graph autodiff (G_S_fwd -> G_S_grad).
MILESTONE 22 — OMEGA_OPTIMIZER                 Omega-native semantics for SGD, Adam, and AdamW, with verified CPU reference
                                               realizations and optional accelerator-fused realizations.
MILESTONE 23 — OMEGA_SEARCH_GUIDE_TRAINING     Sovereign training runtime trains initial search-guide model on Omega trace corpus.
MILESTONE 24 — AIEN_0                          First learned synthesis guide ranking primitives, subgoals, and search branches.
MILESTONE 25 — AIEN_GUIDED_SYNTHESIS           Neural-guided synthesis beats unguided search in node count while preserving 100% soundness.
MILESTONE 26 — AIEN_ABSTRACTION_DISCOVERY      AIEN proposes candidate abstractions; Omega verifies and measures before promotion.
MILESTONE 27 — AIEN_HUMAN_INTERFACE            Bidirectional natural language adapter (Language <-> Omega Task).
MILESTONE 28 — AIEN_RESIDENT                   Persistent accelerator-resident AIEN cognitive execution.
MILESTONE 29 — OMEGA_CONTINUAL_LIBRARY_LEARNING Autonomous continuous Wake/Solve/Verify -> Sleep/Compress/Promote cycle.
MILESTONE 30 — AIEN_SUCCESSION                 Closed-loop self-improvement: AIEN-N designs AIEN-N+1 under Physics canary control.
```
"""
    if "The 31-Milestone Sovereign Program-Learning Roadmap" not in arch:
        arch = arch + "\n" + revised_roadmap_text
    with open(arch_file, "w") as f:
        f.write(arch)
    print("Updated ARCHITECTURE.md")

    # 3. Update OMEGA.md with Program Synthesis and Internal Trust Split
    omega_file = os.path.join(base_dir, "OMEGA.md")
    with open(omega_file, "r") as f:
        omega = f.read()

    synthesis_section_omega = """
---

## 11. Program Synthesis, Procedure Library & Concept Formation

### 11.1 The Internal Trust Decomposition of OMEGA
OMEGA contains both trusted verification authorities and untrusted generative/search machinery:

```text
OMEGA
├── OMEGA SEMANTIC CORE          TRUSTED CONTRACT
├── OMEGA VERIFIER               TRUSTED CHECKER (V0-V2 mandatory; V3-V5 progressive)
├── OMEGA SYNTHESIS              UNTRUSTED SEARCH (Enumeration, e-graphs, constraints)
├── OMEGA ABSTRACTION MINER      UNTRUSTED SEARCH (Subgraph mining, candidate formation)
├── OMEGA REALIZATION SEARCH     UNTRUSTED SEARCH (Instruction scheduling, tiling search)
└── OMEGA LIBRARY
      ├── CANDIDATE               UNTRUSTED (Unverified speculation)
      └── VERIFIED/PROMOTED       TRUSTED BY EVIDENCE (Formally verified & measured)
```

### 11.2 Deterministic Synthesis Engine (V0)
Synthesis begins deterministically without neural guidance:
- Typed enumeration + constraint propagation + cost bounds + dynamic programming + e-graph equivalence pruning + bidirectional search.
- Solves closed-domain synthesis tasks before any neural guide is trained.

### 11.3 Two Distinct Libraries
- **Semantic Library:** Platform-independent abstractions (`MAP`, `FOLD`, `NORMALIZE`, `ATTENTION`). Survives across hardware substrate transitions.
- **Realization Library:** Target-specific implementation blocks (`NEON_TILE_4`, `BLACKWELL_TILE_X`, `CACHE_BLOCKED_GEMM`). Ephemeral and substrate-bound.

### 11.4 Abstraction Discovery and Expandable Invariant
When repeated subgraphs are mined during sleep phases:
- A candidate abstraction must prove net positive value via Minimum Description Length (MDL) compression and search reduction on held-out tasks.
- **The Expandable Invariant:** Every promoted abstraction $\\mathcal{A}$ must retain its exact formal expansion graph $\\mathcal{G}_{\\text{exp}}$ ($\\mathcal{A} \\leftrightarrow \\mathcal{G}_{\\text{exp}}$) to permit auditing, proof checking, recompilation, and migration.
"""
    if "Program Synthesis, Procedure Library & Concept Formation" not in omega:
        omega = omega + "\n" + synthesis_section_omega
    with open(omega_file, "w") as f:
        f.write(omega)
    print("Updated OMEGA.md")

    # 4. Update AIEN.md with Search Prior role and Scoped Training Corpus
    aien_file = os.path.join(base_dir, "AIEN.md")
    with open(aien_file, "r") as f:
        aien = f.read()

    synthesis_section_aien = """
---

## 12. AIEN as Synthesis Intelligence & Search Prior

### 12.1 AIEN is Not a Weight Matrix
- **AIEN** is the sovereign synthesis intelligence that searches, synthesizes, composes, learns, and proposes.
- The model inside AIEN is one component: the **search prior over Omega's discrete possibility space**.
- **Weights hold intuition; programs hold procedure; Omega abstractions hold concepts; Cortex holds experience; proofs hold justification; Physics holds authority.**

### 12.2 Sovereign Cold-Start Dataset
> **Sovereign Training Corpus Scoping:**  
> *Omega's sovereign search traces provide the cold-start training corpus for AIEN-0, removing the need for a foreign pretrained search-guide model or foreign procedural training corpus.*

AIEN-0 learns:
1. $\\text{Task} + \\text{Library} \\to \\text{Likely Useful Primitives}$
2. $\\text{Task} + \\text{Partial Program} \\to \\text{Likely Next Operation}$
3. $\\text{Task} + \\text{Search State} \\to \\text{Likely Subgoal}$
"""
    if "AIEN as Synthesis Intelligence & Search Prior" not in aien:
        aien = aien + "\n" + synthesis_section_aien
    with open(aien_file, "w") as f:
        f.write(aien)
    print("Updated AIEN.md")

    # 5. Update TRUST.md with Staged Verification Ladder & Untrusted Search
    trust_file = os.path.join(base_dir, "TRUST.md")
    with open(trust_file, "r") as f:
        trust = f.read()

    synthesis_section_trust = """
---

## 8. Epistemic Separation in Program Synthesis & Search

### 8.1 Synthesis is Untrusted
- Candidate programs synthesized by OMEGA search or proposed by AIEN are strictly UNTRUSTED proposals.
- No program acquires physical authority until verified by the trusted verifier and admitted by Physics.

### 8.2 Staged Verification Ladder for Synthesis
For early program synthesis (Milestones 7-11):
- **Mandatory Early Tiers:**
  - $V_0$: Structural, Type, and Capability Verification (linear static scan).
  - $V_1$: Differential Verification (comparison against golden reference execution).
  - $V_2$: Property & Invariant Verification (algebraic properties, bounds, conservation).
- **Progressively Maturing Tiers:**
  - $V_3$: Adversarial Corner Fuzzing.
  - $V_4$: Symbolic Equivalence Proofs.
  - $V_5$: Proof-Carrying Realization.
"""
    if "Epistemic Separation in Program Synthesis & Search" not in trust:
        trust = trust + "\n" + synthesis_section_trust
    with open(trust_file, "w") as f:
        f.write(trust)
    print("Updated TRUST.md")

if __name__ == "__main__":
    update_doctrine()
