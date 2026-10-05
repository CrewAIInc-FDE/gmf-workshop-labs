"""Starter: one agent answers a customer's policy question using the policy search tool."""
from crewai import Agent, Crew, Process, Task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.project import CrewBase, agent, crew, task

from policy_qa.common import connector, llm


@CrewBase
class PolicyQACrew:
    agents: list[BaseAgent]
    tasks: list[Task]

    @agent
    def policy_assistant(self) -> Agent:
        return Agent(
            config=self.agents_config["policy_assistant"],  # type: ignore[index]
            llm=llm(),
            mcps=[connector()],
            allow_delegation=False,
            max_iter=12,
            verbose=True,
        )

    @task
    def answer_question(self) -> Task:
        return Task(config=self.tasks_config["answer_question"])  # type: ignore[index]

    @crew
    def crew(self) -> Crew:
        return Crew(agents=self.agents, tasks=self.tasks, process=Process.sequential, verbose=True)
