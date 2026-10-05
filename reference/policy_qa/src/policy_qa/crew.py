"""Reference: research the policies, draft the answer, then review it against the cited policies."""
from crewai import Agent, Crew, Process, Task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.project import CrewBase, agent, crew, task

from policy_qa.common import connector, llm


@CrewBase
class PolicyQACrew:
    agents: list[BaseAgent]
    tasks: list[Task]

    @agent
    def policy_researcher(self) -> Agent:
        return Agent(
            config=self.agents_config["policy_researcher"],  # type: ignore[index]
            llm=llm(),
            mcps=[connector()],
            allow_delegation=False,
            max_iter=12,
            verbose=True,
        )


    @agent
    def answer_writer(self) -> Agent:
        return Agent(
            config=self.agents_config["answer_writer"],  # type: ignore[index]
            llm=llm(),
            allow_delegation=False,
            max_iter=12,
            verbose=True,
        )


    @agent
    def policy_reviewer(self) -> Agent:
        return Agent(
            config=self.agents_config["policy_reviewer"],  # type: ignore[index]
            llm=llm(),
            mcps=[connector()],
            allow_delegation=False,
            max_iter=12,
            verbose=True,
        )

    @task
    def research_policies(self) -> Task:
        return Task(config=self.tasks_config["research_policies"])  # type: ignore[index]


    @task
    def draft_answer(self) -> Task:
        return Task(config=self.tasks_config["draft_answer"])  # type: ignore[index]


    @task
    def review_answer(self) -> Task:
        return Task(config=self.tasks_config["review_answer"])  # type: ignore[index]

    @crew
    def crew(self) -> Crew:
        return Crew(agents=self.agents, tasks=self.tasks, process=Process.sequential, verbose=True)
