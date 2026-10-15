# Live build: a policy Q&A crew in Studio

Morning module, 11:10 to 11:25 CT. One presenter drives CrewAI Studio on the big screen while the room watches. The presenter script is in the notes of each slide. The 11:25 slide hands over to the host.

@slide Let's build one
@idea A crew that answers a service rep's policy question, cites its sources, and has a second agent check the work.
- Agent 1 answers from Northwind's policies
- Agent 2 re-reads every policy it cited
- Built from plain English, in about five minutes
@source Northwind Auto Finance is a fictional lender. Sample policies only.
@notes
**Before you start (do this at the break, not live)**
- Browser signed in to app.crewai.com, in the workshop organization, with Crew Studio open. Zoom the browser to 125 percent so the back row can read it.
- Check the connection once: Studio should offer the "Northwind Workshop Data" connection with the tools `search_policies` and `get_policy`. If the tool shows without a green check, tell a facilitator now, not live.
- Pre-deployed fallback crew is ready and its run form is open in a second tab: "<fallback crew name TBD>".
- Paste buffer ready (two prompts, see the next slide's notes). Have the question ready too.
- <!-- SHOT: Studio home with "Describe your automation" box and the Crews/Flows dropdown set to Crews -->

**Say, at 11:10**
- Okay, so let's actually build one. I am going to describe a crew in plain English, and Studio builds it. Not a single line of code.
- The goal: a customer service rep at Northwind asks a policy question. One agent answers from the policies and cites them. A second agent re-reads every policy the first one cited and fixes anything that does not match.
- Ask the room to watch for five things from the last section: small agents, scoped tools, a task with an expected output, a hosted run, and a trace.
- Analogy: it is a drafter and a reviewer. Same as how any real review process works.

**Likely question:** "Do I have to write prompts like that?" Short answer: no, you describe it the way you would to a colleague. The more specific you are, the less Studio guesses.
@time 11:10

@slide Describe it, run it, read the trace
@idea Plain English in. A crew on the canvas. A trace of every step.
- Mode: Crews
- Describe the crew, press the arrow
- Click Run, type a question, Execute
- Read the timeline
@notes
**Step 1 - Describe it (11:11 to 11:14)**
1. In AMP, open Crew Studio from the left menu.
2. In the "Describe your automation" box, check the dropdown next to the arrow says **Crews**, not Flows. Say it out loud: "Make sure this says Crews. Flows is a different thing we will get to later."
3. Paste the prompt below and press the arrow. (This is the finished-crew prompt from the Policy Q&A Studio lab, so the room can find it again in the lab guide.)

```text
Build a crew for Northwind Auto Finance, a fictional auto lender, with two agents and two tasks that run in order. Agent 1, a Northwind policy assistant with the Northwind Workshop Data tools search_policies and get_policy, answers a customer service agent's question about Northwind's policies: {question}. Its task: answer in plain language in at most 120 words, cite every rule by policy id like (POL-101), include any exceptions that apply, say "The policies don't cover this" instead of guessing when the policies don't answer the question, and don't paste policy text into the answer. Agent 2, a Policy compliance reviewer with the tool get_policy, gets the first answer as context. Its task: re-read every policy cited in the answer, correct any number, condition or citation that doesn't match, add any exception the customer needs to know, and return the final answer followed by a line "Review notes:" saying what you changed, or "none".
```

- Studio Chat builds it in about a minute. Names will differ slightly from the lab screenshots, that is fine.
- <!-- SHOT: the prompt pasted in the box, Crews selected -->

**What to say while it generates (about 60 to 90 seconds - do not sit in silence)**
- This is the part that used to take a developer a day. I described a team and a job. Studio is turning that into agents and tasks.
- Tie back: an agent is a role with a goal and tools. A task is what to do and what done looks like. A crew is the agents and tasks together.
- Constraining agency, already: I told it the length, the citation format, and what to say when the policies are silent. That is the "set format" part of the last slide.

**Step 2 - Read the canvas (11:14 to 11:16)**
- Expect two agent cards and two task cards. The agent that answers has the Northwind Workshop Data tool with a green check. The reviewer has `get_policy` only. Point at that: the reviewer cannot search, it can only re-read. That is a scoped tool.
- Click the pencil on one agent and one task. Read the role, goal, and backstory. Read the task's expected output out loud: "at most 120 words, cites by policy id".
- Point at `{question}` in the task: that is the input. One crew, any question.
- <!-- SHOT: canvas with two agent cards and two task cards, tool green checks visible -->
- If the canvas shows one agent only or a Flow: do not debug live. Go to the fallback (see the last slide's notes for the exact switch).

**Likely question:** "Where does it get the policies?" Short answer: from a data connector, a standard plug called MCP. It is already set up as "Northwind Workshop Data". Agents only get the tools you hand them.
@time 11:12

@slide Run it, and watch what it does
@idea The crew runs in the cloud. Every step lands in a timeline you can inspect.
- Question in: a late-fee question after a disaster
- Agent 1 searches, reads, drafts a cited answer
- Agent 2 re-reads each policy and corrects
- Answer ends with a Review notes line
@notes
**Step 3 - Run it (11:16 to 11:21)**
1. Click **Run** (top right). The Run parameters dialog opens.
2. In **question**, select all and type exactly:

```text
A customer in a declared disaster area missed a payment last week. Will they be charged a late fee?
```

3. Click **Execute**.
- <!-- SHOT: Run parameters dialog with the question filled in -->

**What to say while it runs (about 2 to 4 minutes)**
- It is running in AMP, in the cloud. My laptop is not doing the work. If I closed it right now, the run would keep going. That is the hosted part.
- Click the Run tab and open the Timeline. Narrate each row as it appears: "That is the first agent calling search_policies. Now it is calling get_policy to read the one it found. Now it is writing."
- Then the second agent: "Now the reviewer. It is re-reading each policy that the first answer cited, and checking the numbers."
- Tie it back to the RAG slide: the search step is RAG, used as one tool. The agent chose when to call it. The reviewer is the check.
- Constraining agency, third time: "Notice nobody told it which tool to use in which order. It reasoned about that. But the shape of the result, the length, the citation, the Review notes line, was fixed."
- <!-- SHOT: run timeline mid-run showing search_policies and get_policy calls -->

**Expected output (about; confirm in rehearsal)**
- The final answer should say that a late fee is not charged once the customer is enrolled in the Natural Disaster Hardship Program, that they enroll by asking within 120 days of the declaration, and cite `(POL-115)` and likely `(POL-102)` for the late-fee rule. It stays under about 120 words.
- It ends with a line starting `Review notes:` saying what the reviewer changed, or `none`.
- Click the final **Completed** row to open Event details and read the Output. After a new run, click the new Completed row, since the panel can keep showing the previous run.
- <!-- SHOT: Completed event details with the answer and the Review notes line -->
- Read the answer aloud, then ask the room: "Could you check this? Which policy is it based on?" They can: that is the point of the citation.

**Timing marks:** typed and running by 11:16. If it is not done by 11:21, stop narrating a spinner and move to the fallback.

**Fallback (if Studio is slow or builds something odd)**
- Say: "Studio is a live system, so let me show you one I built earlier." Do not apologise at length.
- Switch to the second tab: the pre-deployed crew "<fallback crew name TBD>". Open it in AMP, go to the **Run** tab, click **Run Automation**, paste the same question under **Input Parameters**, click **Execute Automation**, and narrate the timeline exactly as above.
- TODO: name of the pre-deployed fallback crew is to be decided. Fill it in here and in the first slide's notes.
- If it is only slow at the start (nothing on the canvas after about 90 seconds): talk through the five things on the previous slide while it works, and switch if it is still empty at 11:14.

**Likely question:** "Did it really read the policies, or guess?" Short answer: open the timeline. You can see the tool calls and what they returned. That is why every run leaves a trace.
@time 11:16

@slide The same crew, in code
@idea What you built on the canvas is two small files.
@image assets/policy-qa-reviewer-yaml.svg | An excerpt of two YAML files from the policy Q and A crew. agents.yaml defines the policy reviewer with a role, a goal, and a backstory. tasks.yaml defines the review answer task with a description that includes the question input, an expected output that ends with a Review notes line, the agent that does it, and a context pointing at the first task so the reviewer starts from the draft.
@source Excerpt, shortened. The reference crew is the Policy Q&A lab.
@notes
- Same crew, other view. Everything Studio put on the canvas is a couple of YAML files. Agents in one, tasks in the other.
- Left: the reviewer agent. Role, goal, backstory. That is the new-hire job description.
- Right: its task. The description, the expected output, which agent does it, and `context`. That one line is how the first answer becomes the reviewer's starting point.
- Point at `{question}`: that is the input slot the Run parameters form filled.
- Analogy: Studio is the form. YAML is the paperwork the form fills in. You can pick whichever you prefer this afternoon, and move between them.
- For engineers: this is the same project structure the code track uses, a CrewBase class with explicit agent and task methods reading these files. You edit in the dev container, then deploy to AMP and run it from the run form. Nothing runs locally.
- Show it only if time allows. If you are behind, skip straight to the recap.
- Likely question: "Can I edit it in Studio and in code?" Short answer: yes. Start in whichever you like. This afternoon you pick a path.
@time 11:21

@slide What you just saw
@idea Small agents, scoped tools, a defined output, a hosted run, a trace. That is how a flexible tool becomes a reliable process.
- Agent, task, crew: roles, jobs, and the team
- Tools: scoped to what each agent needs
- Expected output: the answer has one shape
- Hosted run with a trace you can inspect
@notes
- Quick recap, one breath each. Agent: a role with a goal and tools. Task: what to do and what done looks like. Crew: the team and the order. Tools: only what each one needs. And you could inspect every step.
- This is what I meant a few minutes ago. We kept the flexible part, understanding any wording of a question, and constrained the part that has to be reliable: the format, the citation, the check.
- Bridge to the afternoon: after lunch you build your own. Pick a project, pick a path, Studio or code. The lab guides are self-paced, so nobody has to wait on the front of the room.
- Tell them how to start: the labs are on the labs site, linked from the workshop home page. Use only the sample data in the labs.
- Likely question: "Can we use our own documents?" Short answer: this afternoon, sample data only. How you would connect your own is a good conversation for after, and the next speaker covers what is allowed at your organization.
- Then hand over: "Which is a good moment to hear about what you can use, and what is allowed, here."
@time 11:23

@slide Your AI policy and tooling
@idea What is available to you today, what is allowed, and what is coming.
- What tools are available to you now
- What is allowed, and what is not
- What is coming next
- Who to ask
@source Placeholder slide - the host provides the content and the presenter
@notes
- TODO (host): the host organization provides the content and the presenter for this segment. This is only a placeholder so the deck has a slide here. Replace with the host's slides or switch to theirs.
- Timing: 15 to 20 minutes, from 11:25. Lunch is at 11:45.
- Hand-over line: "That is the how. Now here is what it means for you, at this organization: what you can use, what you can not, and what is coming."
- If the host runs short, offer to take questions about the live build. If they run long, the build session after lunch absorbs it.
- Likely question: "Can I use what we built today at work?" Short answer: that is exactly what the host's segment answers, so hold it for them.
@time 11:25
