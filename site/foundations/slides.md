# Foundations: agents, tasks, and crews

Placeholder slides that prove the build pipeline. The real content replaces these before the workshop.

@slide An agent is a role with a goal
@idea Think of a new hire: a job title, a clear goal, and a bit of background.
- Role: who the agent is
- Goal: what it is trying to get done
- Backstory: how it should approach the work
@source Northwind Auto Finance sample data, not real customer information
@notes
- Open with the new-hire analogy, then point at role, goal, and backstory one at a time.
- Ask the room: who has onboarded someone this year? Take one answer, no more.
- Do not explain models or tokens here. Business analysts are in the room.
@time 9:42

@slide A task turns a goal into a deliverable
@idea A task says exactly what to do and what a finished answer looks like.
- Description: what to do
- Expected output: what done looks like
@notes
- Contrast a vague ask ("look into this policy") with a task that names the output ("a two-sentence answer and the policy ID").
- Say it twice: the expected output is what makes results repeatable.
@time 9:50

@slide A crew runs agents in order
@idea Each agent does one small job and hands its result to the next.
@image assets/sequential-crew.svg | Three boxes in a row: an intake agent, a policy agent, and a reply agent, joined by arrows. The policy agent is highlighted and uses a policy search tool.
@notes
- Walk the arrows left to right. The output of one task becomes the context for the next.
- Small single-purpose agents are easier to check than one agent doing everything.
- Pause on the highlighted box: this is where the tool gets used.
@time 9:58

@slide Your crew runs in the cloud, not on your laptop
@idea You edit in a dev container, then deploy to CrewAI AMP, where the crew runs.
- Edit the YAML in the container
- Push to AMP
- Run it from the AMP run form
@notes
- Set expectations for the labs: nobody runs the crew locally.
- Say where to find your deployment: "Owned by me".
- If someone is stuck on setup, point them to Part 0 of the lab guide and keep moving.
@time 10:05
