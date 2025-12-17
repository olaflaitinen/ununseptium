# Graph Features

## Scope

This document describes graph statistical features for network analysis in ununseptium.

### Non-Goals

- Graph databases
- Distributed graph processing
- Deep graph neural networks (see AI docs)

## Definitions

| Term | Definition |
|------|------------|
| Node | Entity in the graph (account, person) |
| Edge | Relationship between nodes (transaction) |
| Motif | Small recurring subgraph pattern |
| Centrality | Node importance measure |

See [Glossary](../glossary.md) for additional terminology.

## Transaction Network

```mermaid
graph TD
    A[Account A] -->|$5k| B[Account B]
    A -->|$3k| C[Account C]
    B -->|$4k| D[Account D]
    C -->|$2k| D
    D -->|$6k| E[Account E]
    B -->|$1k| C

```text
Financial transactions form a directed weighted graph suitable for network analysis.

## Building Networks

```python
from ununseptium.mathstats import TransactionGraph

# Build from transactions
graph = TransactionGraph()
graph.add_transactions(transactions)

# Basic stats
print(f"Nodes: {graph.n_nodes}")
print(f"Edges: {graph.n_edges}")
print(f"Density: {graph.density:.4f}")

```text
## Node Features

### Degree

Number of connections:

| Measure | Formula | Interpretation |
|---------|---------|----------------|
| In-degree | $d_{in}(v)$ | Incoming transactions |
| Out-degree | $d_{out}(v)$ | Outgoing transactions |
| Total degree | $d(v) = d_{in}(v) + d_{out}(v)$ | Total activity |

```python
# Compute degree features
degrees = graph.node_degrees()

for node, deg in degrees.items():
    print(f"{node}: in={deg.in_degree}, out={deg.out_degree}")

```text
### Centrality Measures

| Measure | Meaning | Use Case |
|---------|---------|----------|
| Degree | Direct connections | Hub identification |
| Betweenness | Bridge nodes | Intermediaries |
| Closeness | Average distance | Access to network |
| PageRank | Recursive importance | Flow concentration |
| Eigenvector | Connected to important nodes | Systemic importance |

```python
# Compute centralities
centralities = graph.compute_centralities()

print(f"PageRank: {centralities['pagerank']}")
print(f"Betweenness: {centralities['betweenness']}")

```text
### Centrality Formulas

**PageRank:**
$$PR(v) = \frac{1-d}{N} + d \sum_{u \in N_{in}(v)} \frac{PR(u)}{d_{out}(u)}$$

Where $d \approx 0.85$ is the damping factor.

**Betweenness:**
$$BC(v) = \sum_{s \neq v \neq t} \frac{\sigma_{st}(v)}{\sigma_{st}}$$

Where $\sigma_{st}$ is number of shortest paths from $s$ to $t$.

## Edge Features

### Weight Statistics

```python
# Edge weight features
weights = graph.edge_weight_stats()

print(f"Mean weight: {weights.mean}")
print(f"Std weight: {weights.std}")
print(f"Max weight: {weights.max}")

```text
### Temporal Features

```python
# Time-based edge features
temporal = graph.temporal_features()

print(f"Edge frequency: {temporal.frequency}")
print(f"Last active: {temporal.last_active}")

```text
## Motif Analysis

### Common Motifs

| Motif | Pattern | Significance |
|-------|---------|--------------|
| Triangle | A-B-C-A | Clustering |
| Star | Hub with multiple edges | Concentration |
| Chain | A-B-C-D | Flow path |
| Cycle | Circular flow | Round-tripping |

```mermaid
graph TD
    subgraph "Triangle"
        T1[A] --> T2[B]
        T2 --> T3[C]
        T3 --> T1
    end

    subgraph "Star"
        S1[Hub] --> S2[A]
        S1 --> S3[B]
        S1 --> S4[C]
    end

    subgraph "Chain"
        C1[A] --> C2[B]
        C2 --> C3[C]
        C3 --> C4[D]
    end

```text
### Motif Counting

```python
# Count motifs
motifs = graph.count_motifs()

print(f"Triangles: {motifs['triangles']}")
print(f"Stars (3-node): {motifs['stars_3']}")
print(f"Cycles (4-node): {motifs['cycles_4']}")

```text
### Motif Significance

Compare to random graphs:

$$Z_m = \frac{N_m - \bar{N}_m^{rand}}{\sigma_m^{rand}}$$

```python
# Compute motif z-scores
z_scores = graph.motif_significance(n_random=100)

for motif, z in z_scores.items():
    if abs(z) > 2:
        print(f"Significant: {motif} (z={z:.2f})")

```text
## Community Detection

```python
# Detect communities
communities = graph.detect_communities(method="louvain")

print(f"Number of communities: {len(communities)}")

for i, community in enumerate(communities):
    print(f"Community {i}: {len(community)} nodes")

```text
### Modularity

$$Q = \frac{1}{2m}\sum_{ij}\left[A_{ij} - \frac{k_i k_j}{2m}\right]\delta(c_i, c_j)$$

Higher modularity indicates stronger community structure.

## Application: AML Network Analysis

```python
from ununseptium.aml import TransactionMonitor
from ununseptium.mathstats import TransactionGraph

# Build transaction network
graph = TransactionGraph()
graph.add_transactions(transactions)

# Extract features for each account
features = {}
for account in graph.nodes:
    features[account] = {
        "degree": graph.degree(account),
        "pagerank": graph.pagerank(account),
        "betweenness": graph.betweenness(account),
        "clustering": graph.clustering_coefficient(account),
        "triangle_count": graph.triangle_count(account),
    }

# Flag suspicious patterns
for account, feat in features.items():
    # High betweenness + many triangles = potential layering
    if feat["betweenness"] > 0.1 and feat["triangle_count"] > 5:
        print(f"Suspicious: {account}")

```text
### Suspicious Patterns

| Pattern | Graph Signal | Typology |
|---------|--------------|----------|
| High betweenness | Intermediary | Layering |
| Closed triangles | Circular flow | Round-tripping |
| Star center | Hub | Structuring |
| Isolated cliques | Dense subgraph | Collusion |

## Temporal Networks

```python
# Analyze network evolution
snapshots = graph.temporal_snapshots(window="1d")

for snapshot in snapshots:
    print(f"Date: {snapshot.date}")
    print(f"  Nodes: {snapshot.n_nodes}")
    print(f"  New edges: {snapshot.new_edges}")

```text
## Performance

| Operation | Complexity |
|-----------|------------|
| Degree | O(1) |
| PageRank | O(V + E) per iteration |
| Betweenness | O(VE) |
| Triangle count | O(E^1.5) |
| Community detection | O(V log V) |

## Related Documentation

- [MathStats Overview](mathstats-overview.md)
- [AML Overview](../aml/aml-overview.md)
- [AI Overview](../ai/ai-overview.md)

## References

- Newman, M. (2018). Networks. Oxford University Press.
- Clauset, A., Newman, M. E., & Moore, C. (2004). Finding community structure.
- Milo, R., et al. (2002). Network motifs.
- [Glossary](../glossary.md)
