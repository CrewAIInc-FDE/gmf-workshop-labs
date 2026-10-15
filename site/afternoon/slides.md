# Afternoon kickoff: build a crew and run it on AMP

Ten minutes at 12:30 CT. Then the labs are self-paced until 15:00, and show and tell runs 15:00 to 15:45.

@slide This afternoon you build a crew and run it in the cloud
@idea By 15:00 you will have a working crew on CrewAI AMP that you can show to the room.
- Start from a working starter crew for one Northwind Auto Finance task
- Make one small edit and watch the output change
- Add a second agent that checks the first one's work
- Show what you built at 15:00
@source Northwind Auto Finance is a fictional lender. All data in the labs is synthetic.
@notes
- Good afternoon. This is the build session. Ten minutes from me, then it is your time until 15:00.
- Say the outcome plainly: everyone leaves the afternoon with a crew that is deployed and running on AMP, built by them.
- Remind the room this builds on the morning: agents, tasks, crews. Nothing new to learn first - the guide teaches each piece right when you need it.
- Likely question: "Do I need to finish everything?" Answer: the core is about 60 minutes. Extras are optional. Show and tell is for whatever you have running at 15:00, finished or not.
@time 12:30

@slide Pick a lab
@idea Four labs, same shape: start from a working crew, change it, then add a second agent.
- **Policy Q&A** - answer a question from written policy, citing every rule. Suits anyone, a good first lab
- **Intake triage** - read an inbox document and route it. Suits operations folks
- **Renewal prep** - find expiring agreements, draft outreach. Suits servicing and sales
- **Bring your own** - your idea, on the sample data. Suits anyone with a problem in mind
@source Lab guides are in the lab index (link in the Zoom chat)
@notes
- One line per lab, then stop. Do not teach any of them from the front.
- Policy Q&A: a service agent asks "can we waive this late fee?" and the crew answers from the policy text with the rule cited.
- Intake triage: the mailroom problem. A letter or email comes in, someone decides which team owns it.
- Renewal prep: leases and loans ending soon, find them, draft the outreach.
- Bring your own: you choose the problem, you use the same sample data and tools. Pick this if you already know what you want to automate. It is also the lab where we will ask for a bit more at show and tell.
- Likely question: "Can I do more than one lab?" Answer: yes. Finish one core first, then start another if there is time. Each has its own guide.
- Likely question: "Which is easiest?" Answer: they are built to be about the same effort, roughly 60 minutes for the core. Pick the one closest to a problem you recognise.
- Link: the lab index is on the slide and in the Zoom chat. Drop it in the chat now.
@time 12:32

@slide Pick a track: code or Studio
@idea Same lab, same crew, same result on AMP. The track is how you build it.
- **Code** - VS Code in the dev container; edit files, deploy from the terminal. Pick it if your container is ready
- **Studio** - browser only; build and deploy in Crew Studio. Pick it if you would rather skip the terminal
- Both take about 60 minutes for the core
- Each lab has a guide for each track on the labs site
@notes
- Make the choice easy: it is not a skill test. Both tracks end with a deployed crew on AMP.
- Code needs VS Code attached to the dev container on your laptop. If that is not working in the first ten minutes, switch to Studio rather than fight it. The Studio guide is a clean restart, not a downgrade.
- Studio is browser only, so it works on any laptop. Good for business analysts who want to stay out of a terminal.
- Likely question: "Can I switch tracks halfway?" Answer: yes, but the deployment you made is separate, so you would start the other guide from the top. Better to decide now.
- Likely question: "Which one will look better at show and tell?" Answer: neither. Show the run output, that is the point.
@time 12:34

@slide How it works: edit, deploy, run from AMP
@idea Your crew runs in the cloud on CrewAI AMP, not on your laptop.
@image assets/amp-architecture.svg | Diagram of the workshop flow: your laptop and dev container send your crew to CrewAI AMP, where it runs and calls the Northwind data connector.
- Edit your crew (in the container, or in Studio)
- Deploy it to AMP
- Run it from the Run form in AMP and read the result
@notes
- Walk the diagram left to right: laptop, container, AMP, data connector. The container is just where you edit and deploy from.
- Key point to say twice: you never run the crew on your laptop. No local run, nothing to install for the run itself. The crew runs on AMP and calls the Northwind data connector from there.
- The loop for the whole afternoon is edit, deploy, run from the Run form. Every Part in every guide repeats it.
- Where to find your crew in AMP: use "Owned by me" so you do not scroll through other people's deployments.
- First-time AMP step in the guide: link the model key once in the deployment settings. It is in Part 0. Do not skip it, it is the number one reason the first run fails.
- Likely question: "Where does the data come from?" Answer: a shared sample-data connector for Northwind Auto Finance. Synthetic data only.
- Likely question: "Can I run it locally to debug?" Answer: not in this workshop. Read the run output in AMP. The guides have a troubleshooting table.
@time 12:36

@slide Self-paced: the guide is the teacher
@idea Nobody will teach the labs from the front. Follow your guide, and ask for help early.
- Each Part opens with a short "what you're about to learn" before the steps
- In the room: raise a hand, or ask your pod helper
- Remote: join the breakout room for your lab, one room per lab, each with a named helper
- Stuck for more than 10 minutes? Ask, do not wait
- The finished version of each lab is in the guide if you get really stuck
@notes
- Say it directly: I will not be teaching steps from the front. The guide does that, at your speed.
- In the room: pods of four or five. Work as a team or solo, your choice. Raise a hand, a helper will come, and CrewAI people are floating.
- Remote: you will be sent to a breakout room for your lab. Each room has a named helper from the host company, and CrewAI people float between rooms. Use the Zoom "Ask for help" button or just talk in the room.
- Which room do I join: the one that matches your lab. If you do the Code and the Studio track of the same lab, you are in the same room. The helper handles both.
- Likely question: "Do I stay in the breakout room all afternoon?" Answer: stay as long as you want help. You can leave and return to the main session any time. You will be called back near the end.
- Likely question: "What if I finish early?" Answer: do the optional extras at the end of the guide, start a second lab, or build toward your show and tell.
- Say the ten-minute rule: stuck more than ten minutes, ask.
@time 12:37

@slide Synthetic data only
@idea Use only the sample data in the labs. Never paste real customer or company data.
- Northwind Auto Finance is a fictional lender
- The data connector returns sample policies, documents, and accounts
- No real names, account numbers, or documents in prompts, files, or chat
- This session is recorded
@notes
- Say this slowly. It matters for everyone, and for the recording.
- Everything in the labs, including the sample customers like Marco Reyes and account NW-39940, is made up.
- In Bring your own, the idea can be real but the data has to be the sample data. Describe the problem in general terms. Do not type a real customer's details into the crew, a file, or the Zoom chat.
- The session is being recorded, and the Zoom chat is saved. If something real is pasted by accident, say so to a helper and we will deal with it.
- Likely question: "Can I use our own policy documents?" Answer: not today. Sample data only. Tell us the problem in the chat at the end, and we will capture it.
@time 12:39

@slide Register to show and tell in the Zoom chat
@idea Post one line in the main chat once you have something running. No forms.
- Format: `SHOW | team or your name | lab | one line on what you built`
- Bring your own: add `| PROBLEM: ... | USERS: ...`
- Post by 15:00 so we can pick; earlier is better
- Remote? Post in the main chat, or ask your room helper to post it for you
- The room: a few teams show, plus 3-4 remote volunteers who share camera and screen
@notes
- Example to read aloud: `SHOW | Team Pioneers | Intake triage | routes a hardship letter and flags it urgent`
- Bring your own example: `SHOW | Dana solo | Bring your own | drafts a late-fee waiver reply | PROBLEM: agents rewrite the same reply all day | USERS: service agents`
- Solo is fine. Unfinished is fine. If it runs once, you can show it.
- Remote: if you are in a breakout room, the room chat does not reach the main chat. Either step back to the main session to post, or ask your room helper to post it for you. We will also pull everyone back to the main room shortly before 15:00.
- Show and tell is three minutes each: show the run, say what you changed, say who it helps.
- Likely question: "Do I have to present?" Answer: no. Posting is only if you want a slot. We will pick a few in the room and 3-4 remote volunteers, and keep it moving.
- Likely question: "Where is the use case part?" Answer: at the end of show and tell, everyone posts a use case in the chat. Format on the closing slide there.
@time 12:40

@slide The afternoon timeline
@idea Self-paced from 12:40. Show and tell starts at 15:00.
- 12:30 - kickoff (this)
- 12:40 - labs open, self-paced, help in the room or your breakout room
- 14:50 - remote attendees called back to the main room; last call to post `SHOW`
- 15:00 - build session ends, registration closes
- 15:00 to 15:45 - show and tell, then post your use case in the chat
@notes
- Most people finish the core in 60 to 75 minutes. That leaves time for extras, a second lab, or polishing what you will show.
- Take a break whenever you need one. Nothing is timed against you before 15:00.
- At about 14:50 I will call everyone back to the main room. If you are mid-step, finish the step, post your SHOW line, and come back.
- Close: open the lab index (it is in the chat), pick a lab, pick a track, and go. Helpers, wave so the room can see you.
- If there are no questions, stop. Do not fill the time.
@time 12:42
