# V2 Research Roadmap

## Phase 0 — Research Setup

**Purpose:** establish the research questions, dataset gates, experiment protocol, comparison matrix, configuration conventions, and reproducibility requirements.

**Exit criteria:** documentation reviewed; empty project structure present; V1 frozen; no V2 result claimed.

## Phase 1 — Modern CNN Baseline Reproduction

**Purpose:** reproduce the task in the separated V2 environment with a clearly specified modern from-scratch baseline while retaining V1 as historical evidence.

**Planned evidence:** validated data loader, fixed split manifests, registered baseline configuration, learning curves, classification metrics, resource record, and error analysis.

**Exit criteria:** one reproducible modern baseline evaluated under the test gate, without altering V1.

## Phase 2 — Transfer Learning Comparison

**Purpose:** measure the contribution of pretrained convolutional features under frozen-feature and controlled fine-tuning conditions.

**Planned evidence:** comparable configurations, labelled-data fractions, validation-based selection, compute context, and direct comparison with the modern and historical baselines.

**Exit criteria:** transfer-learning claims supported by registered experiments rather than expected strengths.

## Phase 3 — Foundation Model Embeddings

**Purpose:** evaluate self-supervised and vision-language representations through fixed embeddings and lightweight probes before considering fine-tuning.

**Planned evidence:** embedding provenance, probe protocol, few-shot curves, cross-domain evaluation, and representation error analysis.

**Exit criteria:** data-efficiency and generalization findings documented with model-revision and split traceability.

## Phase 4 — Vision-Language Freshness Reasoning

**Purpose:** study whether multimodal systems can describe visible condition evidence, communicate uncertainty, and identify limits beyond class prediction.

**Planned evidence:** fixed prompts and model revisions, a preregistered image subset, human-review rubric, qualitative and quantitative summaries, and unsupported-explanation analysis.

**Exit criteria:** explanation claims remain bounded to observed evidence and are not confused with food-safety assessment.

## Phase 5 — Paper Preparation

**Purpose:** synthesize the cross-generation comparison into an evidence-led research paper.

**Planned work:** freeze tables and figures, reconcile experiment manifests, document exclusions and negative results, conduct claim review, and prepare reproducibility materials.

**Exit criteria:** every central claim maps to a verified artifact and every limitation is visible in the paper.

No phase beyond Phase 0 is implemented by the framework task.
