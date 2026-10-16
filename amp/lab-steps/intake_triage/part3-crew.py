"""Intake triage crew. The agents and tasks are described in config/agents.yaml and config/tasks.yaml."""
from crewai import Agent, Crew, Process, Task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.project import CrewBase, agent, crew, task

from intake_triage.common import connector, llm


@CrewBase
class IntakeTriageCrew:
    agents: list[BaseAgent]
    tasks: list[Task]

    @agent
    def intake_clerk(self) -> Agent:
        return Agent(
            config=self.agents_config["intake_clerk"],  # type: ignore[index]
            llm=llm(),
            mcps=[connector("get_inbox_document", "list_routing_queues")],
            max_iter=12,
            verbose=True,
        )

    @agent
    def queue_router(self) -> Agent:
        return Agent(
            config=self.agents_config["queue_router"],  # type: ignore[index]
            llm=llm(),
            mcps=[connector("get_inbox_document", "list_routing_queues", "route_document")],
            max_iter=12,
            verbose=True,
        )

    @task
    def triage_document(self) -> Task:
        return Task(config=self.tasks_config["triage_document"])  # type: ignore[index]

    @task
    def route_to_queue(self) -> Task:
        return Task(config=self.tasks_config["route_to_queue"])  # type: ignore[index]

    @crew
    def crew(self) -> Crew:
        return Crew(agents=self.agents, tasks=self.tasks, process=Process.sequential, verbose=True)
