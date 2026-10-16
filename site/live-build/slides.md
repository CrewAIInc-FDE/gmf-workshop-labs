# Live build: a policy Q&A automation in Studio

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
- Pre-deployed fallback automation (built on the Flows path) is ready and its run form is open in a second tab: "<fallback crew name TBD>".
- Paste buffer ready (the prompt and the question, see the next slide's notes). In Studio, the dropdown next to the arrow starts on Crews: practice selecting Flows once.
- Reference screenshot (dropdown open, Flows ticked): [Studio home](../assets/live-build-01-studio-flows-dropdown.png). On 2026-10-16 the dropdown already started on Flows in our organization, so it may not need changing. Check anyway.

**Say, at 11:10**
- Okay, so let's actually build one. I am going to describe a team of agents in plain English, and Studio builds it. Not a single line of code.
- The goal: a customer service rep at Northwind asks a policy question. One agent answers from the policies and cites them. A second agent re-reads every policy the first one cited and fixes anything that does not match.
- Ask the room to watch for five things from the last section: small agents, scoped tools, a task with an expected output, a hosted run, and a trace.
- Analogy: it is a drafter and a reviewer. Same as how any real review process works.

**Likely question:** "Do I have to write prompts like that?" Short answer: no, you describe it the way you would to a colleague. The more specific you are, the less Studio guesses.
@time 11:10

@slide Describe it, run it, read the trace
@idea Plain English in. A crew on the canvas. A trace of every step.
@image assets/live-build-04-flow-canvas.png | Studio canvas showing a Trigger card connected to one step, Answer Policy Question Crew, described as 2 agents across 2 tasks with the Northwind Workshop Data app attached.
- Mode: Flows
- Describe it, press the arrow, confirm the plan
- Click Run, type a question, Execute
- Read the timeline
@notes
**Step 1 - Describe it (11:11 to 11:14)**
1. In AMP, open Crew Studio from the left menu.
2. In the "Describe your automation" box, open the dropdown next to the arrow. It starts on **Crews**. Select **Flows**. Say it out loud: "Make sure this says Flows. Crews is the older Studio and the screens will not match." (Flows is the newer Studio. A flow is the whole automation, and a crew is a small team of agents that does the work of one step. Studio builds the flow and puts the two agents in one step.)
3. Paste the prompt below, check the dropdown still says Flows, and press the arrow. (This is the finished-crew prompt from the Policy Q&A Studio lab, so the room can find it again in the lab guide.)

```text
Build a crew for Northwind Auto Finance, a fictional auto lender, with two agents and two tasks that run in order. Agent 1, a Northwind policy assistant with the Northwind Workshop Data tools search_policies and get_policy, answers a customer service agent's question about Northwind's policies: {question}. Its task: answer in plain language in at most 120 words, cite every rule by policy id like (POL-101), include any exceptions that apply, say "The policies don't cover this" instead of guessing when the policies don't answer the question, and don't paste policy text into the answer. Agent 2, a Policy compliance reviewer with the tool get_policy, gets the first answer as context. Its task: re-read every policy cited in the answer, correct any number, condition or citation that doesn't match, add any exception the customer needs to know, and return the final answer followed by a line "Review notes:" saying what you changed, or "none".
```

4. Studio Assistant shows a plan after about 6 seconds: six short steps (receive the question, draft the answer, answer rules, handle gaps, compliance review, final answer with review notes) and "Does this look correct?". Read two of the steps aloud, then click **Yes, this is correct**. If you forget, nothing happens: that is the most common stall.
- Studio then builds for about 50 seconds ("Built 1 step"). A welcome tour pop-up may appear on a first project: click Next through it or close it. Names will differ slightly from the lab screenshots, that is fine.
- Reference screenshots: [the prompt pasted in the box with Flows selected](../assets/live-build-02-prompt-in-box.png), then [the plan with the Yes, this is correct button](../assets/live-build-03-plan-confirm.png).

**What to say while it generates (about 60 to 90 seconds - do not sit in silence)**
- This is the part that used to take a developer a day. I described a team and a job. Studio is turning that into agents and tasks.
- Tie back: an agent is a role with a goal and tools. A task is what to do and what done looks like. A crew is the agents and tasks together.
- Constraining agency, already: I told it the length, the citation format, and what to say when the policies are silent. That is the "set format" part of the last slide.

**Step 2 - Read the canvas (11:14 to 11:16)**
- Expect a **Trigger** card (leave it alone: the flow starts when you click Run) and one step card, named like "Answer Policy Question Crew", that says **2 agents across 2 tasks**. Point at that: the flow is the whole automation, and the step is the crew of two.
- Click the step to open the crew: a draft task and a review task, each with its agent and **Apps: Northwind Workshop Data**. Click an agent: Task, Profile (role, goal, backstory), Model, Apps. The reviewer should list `get_policy` only. Point at that: the reviewer cannot search, it can only re-read. That is a scoped tool. (If Studio gave the reviewer more tools, say so and move on.)
- Read the step's Output out loud: "at most 120 words, cites by policy id".
- Point at `${state.question}` in the task: that is the input. One automation, any question.
- Reference screenshots: the flow canvas with the Trigger card and the "2 agents across 2 tasks" step is the picture on this slide. After you open the step, [the crew with both tasks](../assets/live-build-05-crew-two-tasks.png).
- If the canvas shows two separate steps instead of one crew step, that is fine: the first output still feeds the reviewer. If it shows only one agent, or the agent has no Apps line: do not debug live. Go to the fallback (see the last slide's notes for the exact switch).

**Likely question:** "Where does it get the policies?" Short answer: from a data connector, a standard plug called MCP. It is already set up as "Northwind Workshop Data". Agents only get the tools you hand them.
@time 11:12

@slide Run it, and watch what it does
@idea The crew runs in the cloud. Every step lands in a timeline you can inspect.
@image assets/live-build-08-output-review-notes.png | Studio Output tab for a finished run: the Answer Policy Question step with its Review Answer task opened. The answer says a customer enrolled in the Natural Disaster Hardship Program will not be charged a late fee, cites POL-115 and POL-102, and ends with a Review notes line.
- Question in: a late-fee question after a disaster
- Agent 1 searches, reads, drafts a cited answer
- Agent 2 re-reads each policy and corrects
- Answer ends with a Review notes line
@notes
**Step 3 - Run it (11:16 to 11:21)**
1. Click **Run** (top right). The Run parameters dialog opens. (If the Run button is grey, Studio Chat is still working: wait for "Built".)
2. In **question**, select all and type exactly:

```text
A customer in a declared disaster area missed a payment last week. Will they be charged a late fee?
```

3. Click **Execute**.
- Reference screenshot: [Run parameters dialog with the question filled in](../assets/live-build-06-run-parameters.png).

**What to say while it runs (about 2 to 4 minutes)**
- It is running in AMP, in the cloud. My laptop is not doing the work. If I closed it right now, the run would keep going. That is the hosted part.
- The Output tab shows the step with both tasks while it works, and finishes in about 20 to 25 seconds. Then click the **Traces** tab and open the Flow Timeline. Narrate the rows: "That is the first agent calling search_policies. Now it is calling get_policy to read the one it found. Now it is writing."
- Then the second agent: "Now the reviewer. It is re-reading each policy that the first answer cited, and checking the numbers."
- Tie it back to the RAG slide: the search step is RAG, used as one tool. The agent chose when to call it. The reviewer is the check.
- Constraining agency, third time: "Notice nobody told it which tool to use in which order. It reasoned about that. But the shape of the result, the length, the citation, the Review notes line, was fixed."
- Reference screenshot: [Traces tab, Flow Timeline with the search_policies and get_policy calls](../assets/live-build-07-traces-timeline.png). In our rehearsal runs the last get_policy row sometimes carries a red ERROR tag even though the run completes and the answer is fine. If someone asks, say the timeline shows everything, including noise, and the final answer is what counts.

**Expected output (about; confirm in rehearsal)**
- The final answer should say that a late fee is not charged once the customer is enrolled in the Natural Disaster Hardship Program, that they enroll by asking within 120 days of the declaration, and cite `(POL-115)` and likely `(POL-102)` for the late-fee rule. It stays under about 120 words.
- It ends with a line starting `Review notes:` saying what the reviewer changed, or `none`.
- Go to the **Output** tab, open the review task, and click **Raw** so the lines stay apart. The reviewer's output is the final answer. In our runs the Review notes line was `none` in some runs and a short correction in others (for example a corrected lease deferral limit). Both are right: say so.
- Reference screenshot: [Output tab with the review task open, showing the answer and the Review notes line](../assets/live-build-08-output-review-notes.png). This is the picture on this slide.
- Read the answer aloud, then ask the room: "Could you check this? Which policy is it based on?" They can: that is the point of the citation.

**Timing marks (observed in rehearsal, 2026-10-16):** plan appears in about 6 seconds, build takes about 25 to 50 seconds (23 seconds in the screenshot rehearsal), a run takes 20 to 25 seconds (19.5 to 21 seconds as reported by Studio, about 25 seconds from Execute to done, longer on a slow run). Typed and running by 11:16. If it is not done by 11:21, stop narrating a spinner and move to the fallback. One of our three rehearsal runs answered that the policy library returned nothing, and took over 90 seconds: if that happens, click Run again once rather than debugging; if that run also fails, go to the fallback.

**Fallback (if Studio is slow or builds something odd)**
- Say: "Studio is a live system, so let me show you one I built earlier." Do not apologise at length.
- Switch to the second tab: the pre-deployed automation "<fallback crew name TBD>". Open it in AMP, go to the **Run** tab (the flow is drawn as a diagram), click **Run Flow**, paste the same question under **Input Parameters**, click **Run Flow** again, and narrate the trace exactly as above. Results appear under **Executions** after about 15 to 20 seconds; open **Final Output** and read the text after `{"raw" =>`.
- If both live runs fail, show the saved screenshots of one completed run: [Output](../assets/fallback-1-output.png), [Output with both tasks open](../assets/fallback-2-output-both-tasks.png), [Traces timeline](../assets/fallback-3-traces-timeline.png), [a trace event opened](../assets/fallback-4-trace-detail.png). Narrate them the same way.
- If the fallback run also fails or hangs, do not retry: switch to the third tab, the fallback's completed execution from the day before, and narrate its **Final Output** and **Traces** the same way. The rule is one retry, then the fallback, then the saved execution.
- TODO: name of the pre-deployed fallback crew is to be decided. Fill it in here and in the first slide's notes.
- If it is only slow at the start (no plan, or nothing on the canvas after about 90 seconds): talk through the five things on the previous slide while it works, and switch if it is still empty at 11:14.

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
