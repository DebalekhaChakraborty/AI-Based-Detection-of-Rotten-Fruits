# V2 Dataset Strategy

## Principles

Dataset selection is part of the research design, not a preliminary download step. Every candidate must pass provenance, availability, license, integrity, class-mapping, privacy, and leakage review before use. Public access does not imply redistribution permission.

No V2 dataset has been downloaded at framework-creation time.

## V1 Historical Dataset

| Field | Strategy |
| --- | --- |
| Dataset | Kalluri, *Fruits fresh and rotten for classification* |
| Purpose | Preserve the historical six-class comparison baseline |
| Availability | Historical Kaggle version documented in `DATASET_PROVENANCE.md`; access must be rechecked before a V2 run |
| License considerations | Existing metadata reports an unknown license; images must not be redistributed |
| Expected challenge | Source-provided transformed families, limited acquisition diversity, background artifacts, and class imbalance |

V2 comparisons using this dataset must reuse or explicitly supersede the documented leakage-safe split policy. They must not silently use the published train/test folders as independent samples.

## Candidate Expansion Sources

| Candidate | Purpose | Availability gate | License considerations | Expected challenge |
| --- | --- | --- | --- | --- |
| Fruits-360 | Fruit identity pretraining, auxiliary representation analysis, or controlled domain-shift study | Verify the authoritative source, version, and continued access before acquisition | Confirm the exact version's license and whether derived splits or embeddings may be redistributed | Mostly controlled imagery; taxonomy focuses on identity rather than freshness |
| Agricultural freshness or defect datasets | Extend condition labels and test transfer across crop types | Conduct a literature and repository provenance review; prefer primary publishers | Review each dataset separately because “academic use” and redistribution terms vary | Inconsistent freshness definitions, annotation quality, capture protocols, and class ontologies |
| Real-world shelf images | Measure robustness under clutter, occlusion, packaging, mixed lighting, and multiple objects | Requires a documented collection or licensed source plan before capture or download | Address photographer rights, store permission, personal information, brands, and redistribution consent | Domain shift, ambiguous labels, multiple fruit instances, and uncertain ground truth |

Candidate inclusion does not imply approval. A dataset enters an experiment only after its gate record is complete.

## Dataset Roles

- **Primary benchmark:** supports direct model-generation comparisons under one fixed ontology and test policy.
- **Label-efficiency subsets:** deterministic fractions of the primary training partition; validation and test remain unchanged.
- **Cross-domain evaluation:** an independently sourced dataset used only for generalization analysis.
- **Explanation study set:** a fixed, documented subset chosen before reviewing model outputs and stratified across classes and failure conditions.

Results from different roles must remain distinguishable in tables and claims.

## Acquisition Gate

Before any download, record:

1. Dataset title, owner, authoritative URL, publication or version date, and retrieval date.
2. License text or terms-of-use evidence; unresolved terms block redistribution and may block use.
3. Expected files, size, checksum source if available, and storage location outside Git.
4. Intended research role and class mapping.
5. Planned integrity, corruption, duplicate, transformation-family, and leakage checks.
6. Whether people, private locations, labels, or other sensitive information may appear.

## Split and Lineage Records

Processed data must be reproducible from a source checksum plus a preparation record. Split manifests should contain stable relative identifiers and class labels, never embedded image bytes. Raw data, processed images, and downloaded archives remain outside version control. Only lawful, non-sensitive metadata and original analysis artifacts may be considered for Git.
