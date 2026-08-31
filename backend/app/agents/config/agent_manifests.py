"""Multi-Agent DAG Manifests and Topology Configs.
Configures autonomous coordination patterns, tool bindings, and state transition schemas.
"""

AGENT_TOPOLOGY_CONFIG = {
    "version": "1.1.0",
    "coordinator": "SupervisorWorkerCoordinator",
    "consensus_threshold": 0.75,
    "max_execution_steps": 25,
    "state_persistence": "postgresql_pgvector",
    "supported_archetypes": [
        "PlannerAgent",
        "ResearcherAgent",
        "CodeSynthesizerAgent",
        "QualityGateJudge",
    ],
}
