"""Starter: one agent drafts end-of-term outreach for one customer account."""
from crewai import Agent, Crew, Process, Task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.project import CrewBase, agent, crew, task

from renewal_prep.common import connector, llm


@CrewBase
class RenewalPrepCrew:
    agents: list[BaseAgent]
    tasks: list[Task]

    @agent
    def renewal_writer(self) -> Agent:
        return Agent(
            config=self.agents_config["renewal_writer"],  # type: ignore[index]
            llm=llm(),
            mcps=[connector()],
            allow_delegation=False,
            max_iter=12,
            verbose=True,
        )

    @task
    def draft_outreach(self) -> Task:
        return Task(config=self.tasks_config["draft_outreach"])  # type: ignore[index]

    @crew
    def crew(self) -> Crew:
        return Crew(agents=self.agents, tasks=self.tasks, process=Process.sequential, verbose=True)
