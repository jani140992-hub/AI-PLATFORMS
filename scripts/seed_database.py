"""Seed Database with Default Enterprise Tenants, Workflows, and Agents."""

import asyncio
from app.core.database import AsyncSessionLocal
from app.db.models.tenant import Tenant, Workspace
from app.db.models.agent import AgentDefinition
from app.db.models.workflow import WorkflowDefinition
from app.db.models.governance import PromptTemplate, PromptVersion


async def seed():
    print("Seeding OmniFlow AI database with demo enterprise entities...")
    async with AsyncSessionLocal() as session:
        # Create Default Tenant
        tenant = Tenant(
            id="default-tenant",
            name="Acme Global Corporation",
            slug="acme-global",
            plan_tier="enterprise",
            monthly_token_quota=100_000_000,
        )
        session.add(tenant)

        # Create Default Workspace
        ws = Workspace(
            id="default-workspace",
            tenant_id="default-tenant",
            name="AI R&D Center",
            slug="ai-rd-center",
            description="Central workspace for agent evaluation and RAG pipelines",
            is_default=True,
        )
        session.add(ws)

        # Create Autonomous Agents
        researcher = AgentDefinition(
            workspace_id="default-workspace",
            name="Senior Market Researcher",
            slug="senior-market-researcher",
            system_prompt="You are a senior equity research analyst specializing in technology markets.",
            model_provider="openai",
            model_name="gpt-4o",
            temperature=0.4,
            memory_type="vector",
            tools_config={"enabled_tools": ["web_search", "calculator"]},
        )
        session.add(researcher)

        await session.commit()
        print("Database seed complete.")


if __name__ == "__main__":
    asyncio.run(seed())
