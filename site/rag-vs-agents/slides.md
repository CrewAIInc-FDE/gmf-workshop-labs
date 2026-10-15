# RAG vs agents, and tools for business

Morning module, 10:45 to 11:10 CT. Twenty minutes on retrieval versus agents, then a five-minute framing, then the live build in the next module.

@slide Find it, or do it?
@idea Some questions need an answer found. Some need a job done.
- Find it: "What is the grace period on a late payment?"
- Do it: "Help this customer with a hardship request."
- Each needs a different tool
@source Northwind Auto Finance is a fictional lender. Sample data only.
@notes
- Welcome back from the break. You just spent an hour on how AI finds the right passage in a pile of documents. Now we ask what you do with that.
- Two kinds of question show up at a business like this. "Find it" questions, where the answer is written down somewhere. And "do it" questions, where somebody has to go get things, decide, and produce something.
- Everything this module is about is picking the right tool for each of those, and not over-building.
- Heads up on the plan: about twenty minutes here, a short bit from me on why this matters for business processes, and then we build one live in Studio.
- Analogy: a reference librarian versus a new hire. The librarian finds you the right page. The new hire gets handed a job.
- Likely question: "Is one of these better?" Short answer: no, better is whichever fits the question. Plenty of problems stop at the first one.
@time 10:45

@slide RAG: search, then answer
@idea RAG looks up the right paragraphs first, then writes an answer from only those.
@image assets/rag-pipeline.svg | Four boxes in a row joined by arrows: a question in plain words, a search of the policy library, a written answer based on what was found, and an answer that shows its source. The search box is highlighted. Below: the path is the same every time, with no other systems and no decisions along the way.
@notes
- RAG stands for retrieval-augmented generation. You just did the retrieval half. This is the whole thing put together: search, then answer.
- Northwind example: "Is there a fee if I pay off my loan early?" It searches the policies, pulls back a few paragraphs, and writes the answer from those paragraphs only.
- The thing to notice is the shape. One question in, one search, one answer out. Same path every single time.
- Analogy: it is an open-book exam. The model is not recalling, it is reading the right page and then explaining it.
- For engineers: this is a single retrieval call feeding a single generation call. Retrieval quality is almost always where the answer quality comes from, so when an answer is wrong, look at what was retrieved first.
- Likely question: "Does it make things up?" Short answer: much less, because it is told to answer from what was found. It can still misread a paragraph, which is why citations matter.
@time 10:47

@slide Where RAG does well
@idea If the answer is written down, RAG is often the whole answer.
- Policy and procedure questions
- Every claim can point to a source
- Same steps every time, so easy to test
- Fewer moving parts to secure and approve
@notes
- I want to be fair to RAG, because it gets treated like the boring option. It is a complete design, not a stepping stone.
- Policy questions, procedure questions, "what does the document say" questions. That is the sweet spot.
- Citations are the big one for a financial-services company. The answer can say which policy and which section, so a person can check it.
- Predictable also means you can test it, explain it to a reviewer, and get it through an approval.
- Example: a service rep asks "What is the late fee after the grace period?" The answer is in POL-102. Search, answer, cite. Done. You do not need an agent for that.
- Likely question: "So why would anyone use anything else?" Short answer: next slide.
@time 10:49

@slide Where RAG stops
@idea RAG reads documents. It cannot go and get things, or work through steps.
- Other systems: "What is this customer's account status?"
- More than one step: check eligibility, then pick an option, then draft
- Deciding what to do next, based on what it found
- Checking its own work
@notes
- RAG answers from the documents it was given. The moment the answer lives in another system, or needs several steps, it runs out of road.
- Northwind example: a customer writes "I lost hours at work and I cannot make my November payment." The policy library can tell you the deferral rules. It cannot tell you whether this customer qualifies, because that depends on their account.
- Analogy: the librarian can hand you the policy binder. They cannot go and look at the customer's file, decide, and write the letter.
- Likely question: "Can't we just put the account data in the library too?" Short answer: you can for static things, but account data changes by the minute and sits behind its own access rules. You want to ask the system, not copy it.
- TODO (needs the W2 capture): the file SP/build/w2/EXAMPLES.md did not exist when this slide was written. When it lands, replace the first bullet with the real example it shows (a real question RAG answered wrongly or incompletely), cite the JSON it points to in the @source line, and quote the exact output. Do not invent a result. Until then, say the Northwind scenario above out loud and keep it hypothetical.
- For engineers: the failure mode to look for is a confident answer built from the right policy with the wrong or missing account facts.
@time 10:51

@slide An agent adds tools and steps
@idea An agent is given a job and tools, and works until the job is done.
- Tools: policy search, an account lookup, a calculator
- Steps: it works through the task, not one pass
- Decisions: it picks what to do next from what it found
@notes
- So here is what we add. Give a model a role, a goal, and some tools, and let it work in steps. That is an agent.
- Tools are the key word. A tool is just something it is allowed to use. Policy search is one tool. Looking up a customer account is another. RAG becomes one tool among several.
- Analogy: RAG is the reference librarian. An agent is a new hire. They have a job title, a goal, and access to a few systems, and they figure out the steps.
- It decides what to do next based on what it has learned so far. That is where the flexibility comes from, and where the risk comes from too. Keep that in your head, because it matters in the next section.
- Likely question: "Is that the same as ChatGPT with plugins?" Short answer: similar idea, but here it runs as part of a business process, on a schedule or on demand, with a record of what it did. More on that in a few minutes.
@time 10:54

@slide The agent loop
@idea Decide, use a tool, look at the result. Repeat until the job is done.
@image assets/agent-loop.svg | A goal goes into a loop of three steps: decide the next step, use a tool, look at the result, then back to deciding. The use-a-tool step is highlighted. When the job is done the loop ends with an answer or action. Caption: the flexible part is the choice at each step, which is the point of an agent and the part you constrain.
@notes
- Walk the loop with a hardship request. Goal: help this customer. Decide: I need the deferral policy. Use a tool: policy search. Look at the result: deferral works if they are under 30 days past due. Decide again: I need their account. Use a tool: account lookup. And so on, until it has enough to answer.
- The choice at each step is the flexible part. It is the reason agents can handle messy requests. It is also the thing you have to test and limit.
- Analogy: it is how a new hire works a case. They do not follow a script. They look something up, think, look something else up.
- Point at the highlighted box: the tool call is where the agent touches the real world.
- For engineers: this is the standard reason-act-observe loop. In CrewAI the tools are things like MCP servers, and every pass through the loop shows up in the run trace, which we will look at in the live build.
- Likely question: "How does it know when to stop?" Short answer: when it judges it has what the task asked for. This is why the task has an expected output. It tells it what done looks like.
@time 10:56

@slide A crew: several agents, one job
@idea A crew splits a job across agents with narrow roles, the way a team does.
- One role each: researcher, writer, reviewer
- Each task has a clear output
- One agent's output is the next one's input
- The drafter is not the approver
@notes
- One agent doing everything is like one person writing, fact-checking, and approving their own work. Nobody would run a review process that way.
- A crew is a team. Each agent gets one narrow role and one clear task. The first one's output becomes the next one's starting point.
- That separation of duties should sound familiar. It is how you already run reviews, so reviewers and auditors will recognize it.
- Small, single-purpose agents are easier to instruct and easier to debug. When something goes wrong you can see which step did it.
- Building blocks in CrewAI: agents, tasks, tools, crews. Flows add fixed step-by-step control around them, which we will touch on this afternoon.
- Likely question: "Why not one really smart agent?" Short answer: you can, and it is a fine place to start, but one agent with a long list of instructions is harder to check than three with short ones. The reviewer catching the writer is the whole benefit.
@time 10:58

@slide Sometimes you need none of them
@idea If you can write the rules down, write them down.
- "Under 30 days past due, fewer than two deferrals, contract older than 6 months: offer a deferral."
- That is a script with three conditions. Keep it a script.
- Use the model for reading and writing, plain code for the rest
@notes
- I want to say this out loud because we are about to spend a day on agents. If you can write the rules down, you do not need an agent. Write the rules down.
- Example: the deferral eligibility rule. Three conditions. An if statement does that faster, cheaper, and the same way every time. And you can explain it to a regulator in one sentence.
- Use the model where there is language or judgment: reading the customer's message, drafting the reply. Use plain code for everything else.
- Signs you picked an agent and should not have: its only tool is search, the plan is the same every time, or nobody can say what decision it is making.
- Signs you need more than RAG: prompts full of "first do this, then if that" and people copying data in from other systems by hand.
- Likely question: "So when is it worth it?" Short answer: when the input is messy and the work is judgment plus lookups, like reading an email and working out what it needs.
@time 11:00

@slide RAG, agent, or crew?
@idea Start on the left. Move right only when you must.
@image assets/rag-agent-crew.svg | Three cards from left to right. RAG: find it and explain it, search then answer, for example what is the grace period. Agent: look things up and act, a loop with tools, for example what is my payoff and until when. Crew: split the job and add a check, roles hand off work, for example handle this hardship request. An arrow underneath points right: more moving parts, more to test. Start on the left and move right only when you must.
@notes
- This is the slide to screenshot. Ask four questions in order and stop at the first no.
- One: can the answer be found in documents, and is that all you need? Then RAG.
- Two: does it need live data or an action in another system? Then you need tools, so an agent.
- Three: do distinct roles or a built-in check matter? Then a crew.
- And before all of it: can you just write the rules down?
- Ask the room to bring this to architecture review: name which question pushed you to the next level of complexity.
- Likely question: "Which one is cheapest to run?" Short answer: left to right gets more expensive and takes more testing. That is why you start on the left.
- Engineer detail: the right-hand end is not "better", it is "more to test". Plan test cases accordingly.
@time 11:02

@slide Quick poll: which one?
@idea Show of hands. Which tool does each Northwind question need?
- A: "What is the returned payment fee?"
- B: "Is this account eligible for a deferral, and when is the next payment due?"
- C: "Read this hardship email, check policy and account, draft a reply, and have it checked."
- D: "If under 30 days past due and fewer than two deferrals, offer a deferral."
@notes
- Quick show of hands, thirty seconds each, no speeches. Read each one and ask: RAG, agent, crew, or none of them?
- A: RAG. The answer is in the policies. POL-113 has the returned payment fee. Search, answer, cite.
- B: an agent. It needs policy search and an account lookup, and the steps depend on what it finds.
- C: a crew. Several jobs with a check at the end: researcher, writer, reviewer.
- D: none of them. That is a rule. Write the code. Pause here, because this one is the one people argue about and it is a good argument to have.
- Do not grade people's answers. If the room splits, say what the deciding question is and move on.
- Likely question: "What if we are not sure?" Short answer: start on the left, build it, and test with twenty real questions. The test tells you whether you need to move right.
@time 11:04

@slide Claude is a tool for people. Crew is a tool for business.
@idea A common question: what is the difference between this and the AI I already use at work?
- Claude is a tool for people.
- Crew is a tool for business.
@notes
- This is my five-minute bit. One of the questions I get asked a lot is: okay, I use AI in my job. What is the difference between you and Claude, or you and my ChatGPT desktop app?
- The one-line answer I like to give is: Claude is a tool for people. Crew is a tool for business.
- When you are using a chat tool as a person, you see what it produces. If something does not sound right, you ask it to clarify. It is human in the loop, iterative, every single step. The beauty of Claude is that it is iterative.
- A desktop assistant also does not have a hosted environment. You turn your laptop off because you are on PTO, and it does not run for two weeks. A business process needs to run when you are not there.
- Keep it light. Do not turn this into a product comparison. The point is the difference in the job each one does.
- Likely question: "Can I not just use the chat tool for this?" Short answer: for your own work, yes, that is what it is for. This is for when the work has to happen the same way, for everyone, whether or not anyone is watching.
- These lines are cues from how I already say it. Say it your way.
@time 11:05

@slide Three emails are fine. Accounting is not.
@idea Reasoning makes inputs flexible. A business process still needs one right result.
@image assets/emails-vs-accounting.svg | Two panels. Left, an email to a customer: three different reminder emails, such as Hi Sam, due Friday, and Dear Sam, due this Friday, and Reminder: Friday. Three people, three emails, all fine. Right, posting an accounting entry: look up the account, apply the posting rule, record it in the ledger. One right way, the same every time.
@notes
- If I write an email, it generates an email. You write an email. The emails can be very different in style, but as long as they are business appropriate and convey the message you want to get across, nothing else really matters.
- Accounting does not work that way. There is one right way that the organization does accounting, and it has to be done that way every time. Same for compliance forms, same for real estate leases.
- So the agency component actually needs to be very much constrained, at least at each individual step in the flow, because we do not want it to go willy-nilly.
- Left to right, same idea: the benefit of reasoning is that inputs and outputs can be more flexible, so we get less brittleness. But we need a repeatable and reliable outcome for a given set of inputs to automate a business process.
- Ask: raise a hand if you have ever been handed three differently formatted versions of the same report. That is the left panel. Nobody would accept it in the right panel.
- Likely question: "So it is less smart?" Short answer: no, same intelligence. You are narrowing the job, not the model.
@time 11:07

@slide Constrain the agency
@idea Keep the reasoning, fix the process, and the outcome repeats.
@image assets/flexible-to-repeatable.svg | Three boxes joined by arrows. Flexible inputs: any wording, any document. Constrained steps, highlighted: small jobs and set formats. Repeatable outcome: the same shape on every run.
- Small agents with one job each
- Tools limited to what the job needs
- Tasks with an expected output
- Runs hosted in the cloud
- Every run leaves a trace
@notes
- Here is the idea. What you actually want to do is constrain it. Limit the agency. Use the ability to take flexible inputs to produce deterministic outputs.
- That is how the outcome stays reliable and repeatable regardless of the inputs.
- How does CrewAI do it? Five things, and you will see all five in the build. Small single-purpose agents: the way to do that is by being just the right amount of specific. Scoped tools: this agent can search policies, and that is all. Tasks with an expected output: the shape of the answer is written down. Hosted runs: it runs in AMP, not on someone's laptop. Traces: every run records what it did, so you can see what happened.
- Bridge: "So let's build one. I am going to describe a crew in plain English in Studio, and as it builds, watch for those five things."
- For engineers: nothing here is exotic. It is the same discipline as a well-factored service: single responsibility, least privilege, a typed contract on the output, and an audit log.
- Likely question: "Do I lose the benefit of AI if I constrain it?" Short answer: no. The reasoning is still doing the hard part, understanding the messy input. You are only fixing the shape of the result.
@time 11:08
