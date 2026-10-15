# Foundations: what AI is, how it finds things, and why search choices matter

Morning module, 9:30 to 10:30 CT. One hour of plain-language foundations: what generative AI is and is not, embeddings by analogy, vector search, top-k, keyword versus semantic versus hybrid, and a simple vector store. Every search result on these slides is a real output from the workshop's Northwind data connector, captured 2026-10-15.

@slide Foundations: five ideas in one hour
@idea No jargon without a picture. Ask the moment a word goes by that you do not know.
- What generative AI is, and is not
- Embeddings: a map of meaning
- Vector search and top-k
- Keyword, semantic, and hybrid search
- A simple vector store
@source Every example uses Northwind Auto Finance, a fictional lender, with synthetic data
@notes
- Hand-over from the host's remarks: "Thank you. Today is mostly hands-on, so here is the morning, and then we start with the basics."
- The hour has five ideas, in this order. They stack, so each one makes the next one easy.
- I'm doing this in plain language on purpose. The host told me a lot of people in this room don't have clarity on this stuff yet, and honestly that's normal. If a word goes by that you don't know, put your hand up. Somebody else is wondering too.
- Every example uses Northwind Auto Finance, a fictional lender. The search results you'll see are real output from the same demo data service you'll use in the labs this afternoon, so nothing here is mocked up.
- For engineers: I'll flag the deeper stuff as "for engineers" in passing, one sentence, and then we move on. The labs are where you get to poke at it.
- Analogy: this hour is learning how the library works, before we hire the librarian. After the break we hire the librarian.
- Likely question: "Do we build any of this today?" Short answer: yes, this afternoon. This hour is the mental model that makes the build make sense.
@time 9:30

@slide Generative AI: words in, words out
@idea You give it words. It writes the most likely useful continuation.
@image assets/words-in-words-out.svg | Three boxes joined by arrows. Left: your words, such as a question or a document. Middle: the model, which has read a huge amount of text. Right: words out, the likely useful continuation. Below: it writes one small piece at a time, and nothing is looked up.
@notes
- A generative AI model has read an enormous amount of text and learned what tends to come next. That's the whole trick.
- Words in can be a question, an instruction, a pasted document. It's all the same to the model: text in, text out.
- The thing to hold onto: it writes. It doesn't look anything up. That one fact explains most of what goes right and wrong today.
- Quick show of hands: who has used a chat assistant this week? Keep your hand up if you pasted something in and asked it to rewrite or summarize it. That's exactly the use this slide describes.
- Analogy: autocomplete on your phone, if autocomplete had read most of the internet and could keep going for a few pages.
- For engineers: the small pieces are tokens. The host asked us to keep tokens and chunking out of the main track, so I'm parking that. Catch me at the break.
- Likely question: "Is it actually thinking?" Short answer: people argue about that. For our purposes it doesn't matter. What matters is it produces fluent text, and fluent isn't the same as checked.
@time 9:31

@slide What it is good at
@idea Anything where the job is working with language.
- Summarizing a long document
- Rewriting in a different tone
- Sorting things into categories
- Pulling fields out of free text
- Explaining a dense policy in plain words
@notes
- These are the jobs where a fluent reader helps. Summarize, rewrite, classify, extract, explain.
- At a lender, think of a long customer email that needs sorting, a policy paragraph a rep needs in plain words, or a stack of notes that need three fields pulled out.
- Notice what's on the list: all of it is working with text somebody already gave it. That matters in two slides.
- Analogy: a very well-read new hire on day one. Fluent and fast, writes a clean email, but has never seen your policy manual.
- Likely question: "Can it do all of these reliably?" Short answer: well enough to be useful, not well enough to skip checking. Reliable and repeatable is a design job, and it's what Part 2 of the labs is about.
@time 9:34

@slide What it is not
@idea It recalls patterns. It does not look facts up.
- Not a database: recall can be wrong
- Not current: it knows what it was trained on
- Not a calculator: it can give a confident, wrong number
- Not the decision-maker of record: a person stays accountable
@notes
- Four things it isn't. Not a database: it doesn't look things up, it recalls patterns, and recall can be wrong.
- Not current: it knows what it read during training. It has no idea what changed in your late-fee policy last month.
- Not a calculator: ask for a payoff quote and you can get a confident, wrong number. Numbers that matter get computed by a system that computes.
- Not the decision-maker of record. It drafts and recommends. The accountability stays with a person and a process, and I'd say that's especially true in financial services.
- Analogy: the new hire again. Great at drafting the reply, but you wouldn't let them sign off a payoff quote from memory on day one.
- Likely question: "So can we trust it at all?" Short answer: trust it for the language work, check it for the facts, and the rest of the hour is how you give it the right facts to work from.
@time 9:36

@slide Confident is not the same as correct
@idea Without the policy you get a fluent, generic answer. With the policy it can be specific.
- Without the policy: a plausible answer from general patterns, maybe right for some other lender
- With it: "A grace period of 10 calendar days applies before a late fee is assessed."
- And: "The late fee is 5 percent of the scheduled payment amount, capped at 25 dollars, unless state law sets a lower limit."
- The model did not get smarter. It was handed the right paragraph.
@source Policy POL-102 text as returned by the connector: a4_control_grace_all_agree.json
@notes
- This is the one slide to remember if you forget the rest. A customer asks about a late fee. With no documents, the model answers from general patterns, and you get something that sounds right and could be right for some other lender.
- With the Northwind policy in front of it, it can say 10 calendar days, 5 percent, capped at 25 dollars, unless state law sets a lower limit. That's the real text of our sample policy POL-102, straight from the connector.
- Same model both times. It didn't get smarter. It was handed the right paragraph.
- I'm not putting a made-up "wrong answer" on the screen, because I don't want to show you a fake output. Try it yourself at the break: ask any chat assistant about late fees at an auto lender and read how confident it sounds.
- Analogy: open-book versus closed-book exam. Same student, very different answers.
- Likely question: "Why not just train the model on our policies?" Short answer: you can, but it's slow, it goes stale the day a policy changes, and it can't point at its source. Handing it the paragraph at question time is cheaper and checkable.
@time 9:39

@slide The real question: which paragraphs?
@idea You cannot paste the whole policy library into every question.
- A real library is hundreds of pages
- A few paragraphs matter for this question
- Search picks them. The model answers from them.
- The rest of this hour is how search decides
@source The demo library has 15 policies: e_list_policies.json
@notes
- The model can only look at so much text at once, and the more you hand it, the harder it is to check. So we don't paste the whole library in.
- The question becomes: out of everything we have, which few paragraphs does the model see for this question? That's what search is for.
- Our demo library is small, 15 policies, so you can hold it in your head. A real one is thousands of pages. The ideas are the same, the stakes are bigger.
- Analogy: you ask a colleague a question about a policy. They don't read the whole manual out loud. They go to the right page, then explain it.
- Likely question: "Why not just make the model remember everything?" Short answer: its memory has a limit and it goes stale. Handing it the right pages at question time stays current and shows its source.
- For engineers: this is the retrieval half of retrieval-augmented generation. The model sees only what retrieval returns, so retrieval quality caps answer quality.
@time 9:42

@slide An embedding is a pin on a map of meaning
@idea Every piece of text gets a location. Similar meanings sit close together.
- Pin one sentence on the map
- Pin another that means the same thing, in different words
- They tend to land in the same neighbourhood
- A sentence about something else lands across town
@source Illustrative description, not captured output
@notes
- Here's the picture I want you to keep. Imagine a huge map. Every sentence, every policy paragraph, gets a pin, and the pin's position is its meaning.
- Sentences that mean similar things end up near each other, even when they share no words. "Can I skip a payment this month?" and "Is a payment extension available?" should land in the same neighbourhood. "How do I get my title released?" lands somewhere else.
- No math today. An embedding model is what drops the pins. It's a different model from the one that writes answers.
- Analogy: a city map where neighbourhoods are topics. Hardship stuff is one part of town, fees another, paying off the loan another.
- For engineers: the "location" is a long list of numbers, a vector. In the demo store it's 384 of them per policy, and I'll show you real ones in a few slides. "Close" means the distance between two of those lists is small.
- Likely question: "Who draws the map?" Short answer: an embedding model, ahead of time for the library, and again for each question when it arrives.
@time 9:44

@slide Similar meanings sit together
@idea Real policy titles, placed by topic. Positions are illustrative.
@image assets/map-of-meaning.svg | A hand-drawn illustration of a map of meaning with four neighbourhoods of policy titles. Payment relief: Payment Deferral, Natural Disaster Hardship, Loan Modification. Fees and payments: Late Fee and Grace, Electronic Payments. Ending the loan: Early Payoff, Title and Lien Release. Rules and risk: Servicemember Protections, Repossession. Positions are illustrative only.
@source Titles from the Northwind policy library: e_list_policies.json. Positions drawn by hand, not computed.
@notes
- Same idea, now with our actual policy titles. Payment Deferral, Natural Disaster Hardship, and Loan Modification are all about helping somebody who can't pay, so they sit together. Late fees and electronic payments are about money moving. Early payoff and title release are about ending the loan.
- Be clear with the room: I drew these positions by hand to show the idea. They are illustrative, and the real map has hundreds of dimensions, not two. I'm not claiming this is what the model computed.
- One thing worth noticing: neighbourhoods are fuzzy. A hardship policy and a fee policy can sit near each other, because a hardship plan suspends late fees. Real maps are messy.
- Analogy: a library's shelving. Books on the same subject are on the same shelf, and the shelves for related subjects are near each other.
- For engineers: you embed every policy once, ahead of time, and embed each question when it arrives. In the demo the text embedded is the title plus the full policy text, as one piece.
- Likely question: "Does the map know our business?" Short answer: it knows general language. It doesn't know your products or your internal jargon unless that language shows up in the text you embed.
@time 9:47

@slide Vector search: drop a pin, look nearby
@idea The question gets a pin of its own. The closest pins come back, closest first.
@image assets/vector-search.svg | A map with grey pins for policies and one coral pin for the question. The three pins nearest the question are circled and numbered 1, 2, and 3. A list on the right says: drop a pin for the question, look nearby at the closest pins, and return them closest first.
@source Illustrative drawing
@notes
- This is vector search. "Vector" is just the list of numbers that gives a pin its position. Search is three steps: drop a pin for the question, look at the closest pins, give them back in order.
- The thing that surprises people: the question and the policy don't need to share a word. They need to be near each other on the map.
- Each result comes back with a score. Bigger means closer. A score only means something compared to the other scores from the same search, which I'll come back to, because it bites people.
- Analogy: you walk into a shop with a half-described problem and the assistant walks you to the nearest shelf that looks relevant. They didn't match your words, they matched your need.
- Likely question: "Is it slow?" Short answer: no. In the demo, each call came back in well under half a second. The captured calls ranged from 0.03 to 0.40 seconds.
@time 9:51

@slide Vector search on a real question
@idea "My house was flooded in the hurricane, can I get help with my car payment?"
@image assets/hurricane-semantic.svg | Semantic search, top three results. First, highlighted: Natural Disaster, POL-115, score 0.682. Second: Payment Deferral, POL-101, 0.648. Third: Electronic Payments, POL-113, 0.616. A note says the right policy is first: the question says flooded and hurricane, the policy says disaster, different words and the same meaning.
@source a5_hurricane_synonym.json - semantic mode, top_k 3. The policy text says "disaster" and never says "hurricane" or "flood".
@notes
- Here's the real thing. A customer writes about a flooded house and a hurricane. Our policy for that is called Natural Disaster Hardship Program. The word "hurricane" isn't in it, the word "flood" isn't in it. It says "disaster".
- Semantic search put it first, at 0.682. A pure word-match has very little to go on here: keyword search did return it, but third, on common words like "payment". This is what a map of meaning buys you.
- Be honest about the scores, though. Look at them: 0.682, 0.648, 0.616. They're close. It's the order that matters, not any one number. Don't read 0.68 as "68 percent sure".
- Also look at what came second: Payment Deferral, which is a sensible neighbour for somebody who can't pay. That's the map working the way I described.
- Analogy: you asked for "something to help with water damage" and the clerk pointed to the flood-insurance shelf without you saying the word.
- Likely question: "What does the score mean?" Short answer: how close the pins are, on a scale that belongs to this one search mode. Compare results inside one search, not across searches or across modes.
- For engineers: semantic mode here is cosine similarity on BAAI/bge-small-en-v1.5 vectors, computed locally in the connector.
@time 9:54

@slide Halfway: where we are
@idea Text in, meaning out, nearest neighbours back.
- Generative AI is fluent, not automatically correct
- The fix is handing it the right paragraphs
- An embedding is a pin on a map of meaning
- Vector search returns the nearest pins
- Questions? This is the best time to ask.
@notes
- Halfway through, and this is the point to stop. Quick recap in four lines: the model writes, it doesn't look up. So we give it the right paragraphs. Embeddings give every paragraph a place on a map. Vector search finds the nearest ones.
- Take questions here. Honestly, if one thing from the first half is fuzzy, the second half is going to be fuzzy too, so I'd rather spend three minutes now.
- Likely question: "Where does the answer-writing model come in?" Short answer: after all this. Search picks the paragraphs, then the writing model reads them and answers. That whole shape has a name, retrieval-augmented generation, and we'll name it after the break.
- If nobody has a question, ask one back: "In your own work, where do you have a pile of documents and a person who knows which page to open?" Take one answer. It's the use case for everything in this hour.
- Timing check: if we're past 10:02 here, trim the k slides, not the three-ways slides. The search modes are the part people use the most.
@time 9:58

@slide Top-k: how many results you hand over
@idea The model can only use what it is shown.
- k = 1: only the single closest result
- k = 3: the three closest
- k = 8: the eight closest
- In this demo each result is a whole policy
@notes
- Top-k is just "how many of the closest results do we pass to the model". The k is a number you pick.
- It sounds like a tuning detail. It's one of the most consequential choices in the whole setup, because the model can only use what it's shown.
- Small note on our demo: each result is a whole policy, not a snippet of one. In a bigger system you'd often get back pieces of documents. The idea is the same.
- Analogy: you ask a colleague to pull the relevant policies for a case. "Just the best one" or "the top three" or "everything that looks vaguely related" gets you three very different piles of paper.
- Likely question: "Who picks k?" Short answer: whoever builds the search. Often it's a setting in the tool, and you'll set it yourself in the lab.
@time 10:00

@slide Top-k: how much of the ranking you read
@image assets/top-k-funnel.svg | A funnel narrowing from left to right. The wide end is the whole library, ranked closest first. The narrow end is the top k, for example 3, the few results handed to the model. An arrow leads to the model. Below: too few misses a condition, too many buries the answer.
@source Illustrative drawing. The demo library has 15 policies: e_list_policies.json
@notes
- Search ranks the entire library, every time, closest first. Top-k is where you draw the line on how much of that ranking the model gets to read.
- Too small: the model never sees a condition that matters, and it answers confidently without it. Too large: the one policy that matters is buried in a pile of loosely related ones, and the answer gets slower and harder to check.
- Quick framing for the business folks: this is a dial between "might miss something" and "might drown in noise". There's no perfect setting, just a sensible default you test.
- Analogy: a hiring panel. You rank 15 resumes and shortlist three to interview. Shortlist one and you might miss the best fit. Interview all fifteen and nobody gets proper attention.
- Likely question: "Doesn't the model just ignore the junk?" Short answer: sometimes. But junk takes room and can pull the answer off course. Less, and more relevant, is usually easier to check.
@time 10:02

@slide One question at k = 1, 3, and 8
@idea "How many times can I defer a payment, and do I qualify?"
@image assets/top-k-list.svg | A ranked list of eight policies with scores, and brackets for k = 1, 3, and 8. Rank 1 is Natural Disaster 0.865. Rank 2, highlighted, is Payment Deferral 0.761. Rank 3 is Late Fee and Grace 0.65. Then Electronic Payments 0.615, Refinancing 0.59, Lease-End 0.434, Repossession 0.408, and Servicemember 0.369.
@source b_topk_1_3_8.json - hybrid mode. The ranking is the same at every k; only how far down you read changes.
@notes
- Same question, same ranking, three different cut-offs. Notice the ranking never changes. Only how far down we read.
- At k = 1 the single best hit is Natural Disaster Hardship, 0.865. The question says nothing about a disaster, so the model would answer confidently from the wrong policy. The standard deferral policy, POL-101, is second.
- At k = 3 we get POL-101 in, and the answer can cover the normal rules. That's the sweet spot here.
- At k = 8 the five extras, ranks 4 to 8, are mostly noise: electronic payments, refinancing, lease-end, repossession, servicemember. And with only 15 policies in the library, 8 is more than half of everything. Real libraries are bigger, so noise shows up more slowly but it still shows up.
- Rule of thumb: start around 3 to 5, then test with 20 realistic questions that have known right answers. Look at what was retrieved, not only the final answer. Most wrong answers are retrieval problems.
- Analogy: the hiring shortlist again. Notice the best resume at k = 1 wasn't the right fit. That's why you don't interview one.
- Likely question: "So k = 3 is always right?" Short answer: no, it's right for this library and this question. That's why you test.
- For engineers: this is hybrid mode, so scores are 0.5 times semantic plus 0.5 times keyword scaled to the best keyword score. Don't compare them to the other modes' scores.
@time 10:05

@slide Three ways to search
@idea Same library, three ways to rank it.
- Keyword: matches the exact words
- Semantic: matches meaning, using the map
- Hybrid: runs both and blends the rankings
- The mode decides which policies the model ever sees
@notes
- Everything so far was semantic search, the map of meaning. There are two other ways to rank, and the choice changes what the model sees.
- Keyword search matches the words you typed. Great for exact things: a figure, a name, a code. Useless if the customer used different words than the policy did.
- Semantic search matches meaning. Great for how customers actually talk. Weak on exact figures, because a number is just another blob to the map.
- Hybrid runs both and blends the two rankings.
- Analogy: Ctrl+F versus asking a person. Ctrl+F finds the exact string and nothing else. The person understands what you mean but might not nail the exact clause.
- For engineers: in this connector keyword is TF-IDF cosine, semantic is bge-small cosine, and hybrid is half of each, with the keyword half scaled to the best keyword score. Only title and body text are indexed, not the policy ID.
- Likely question: "Which is best?" Short answer: next four slides, with real results. Short version: it depends on the question, which is the whole point.
@time 10:08

@slide Keyword misses the synonym. Semantic finds it.
@idea "I'm being deployed overseas with the Army, what happens to my loan?"
@image assets/a1-results.svg | Three columns of top-three results. Keyword: Refinancing 0.113, Late Fee and Grace 0.049, Payment Deferral 0.0 no match. Semantic: Servicemember 0.681 highlighted, Refinancing 0.653, Payment Deferral 0.646. Hybrid: Refinancing 0.827, Late Fee and Grace 0.527, Servicemember 0.34 highlighted. Highlighted means it is the policy that answers the question.
@source a1_deployed_synonym.json - top_k 3. Scores are only comparable inside one column. A score of 0.0 means no evidence, not "third best".
@notes
- The right policy here is Servicemember Protections, POL-110. The customer says "deployed" and "Army". The policy says "active duty" and "military". They share almost no words.
- Keyword never returns it. Its top three are refinancing, late fee, and a deferral policy that scored 0.0. A zero doesn't mean third best, it means no evidence at all. It's just filling the list.
- Semantic puts Servicemember first, at 0.681. Be fair, though: the margin is narrow, 0.681 against 0.653 and 0.646. It got the right answer, but not with a lot of daylight.
- Look at hybrid too. The right policy is in there, but at third place. I'll come back to this on the scoreboard slide, because it's the thing that stops me saying "just use hybrid".
- Analogy: you ask a clerk for "anything about the Army" and they only check for that word. Another clerk understands you mean military, and walks you to the right shelf.
- Likely question: "Why didn't keyword catch 'military'?" Short answer: the customer never typed it. Keyword can only match words that are actually in the question.
@time 10:09

@slide Keyword nails the exact figure
@idea Search for "84 months", a figure inside the deferral policy.
@image assets/a2-results.svg | Three columns of top-three results. Keyword: Payment Deferral 0.09 highlighted, Lease-End 0.055, Electronic Payments 0.043. Semantic: Refinancing 0.551, Lease-End 0.546, Natural Disaster 0.546, with Payment Deferral not returned. Hybrid: Payment Deferral 0.76 highlighted, Lease-End 0.576, Electronic Payments 0.498.
@source a2_84months_keyword_wins.json - top_k 3. The policy says "a total term of 84 months" (d_get_policy_POL-101.json).
@notes
- Flip it around. Somebody searches for "84 months", the maximum total term in the deferral policy. This time keyword wins. Payment Deferral comes back first.
- Semantic doesn't return it at all. Look at its scores: 0.551, 0.546, 0.546. They're nearly tied, which tells you there's no real winner. A number is just not something the map is good at.
- Keyword's own score is low in absolute terms, 0.09. Don't judge it by the size. Look at the lead over the runner-up.
- Hybrid gets it back, first at 0.76.
- Analogy: Ctrl+F finds "84" in a contract instantly. Asking a person "something about eighty-something" gets you a shrug.
- Likely question: "Can I search by policy number, like POL-115?" Short answer: not in this demo. The ID isn't indexed for search. In the capture, "What does POL-115 say?" put POL-115 third in keyword and second in semantic. An ID is a lookup, so you ask for it directly with get_policy. That's what the second tool is for.
@time 10:12

@slide Same library, different answers
@idea The search mode decides which policies the model ever sees.
@image assets/modes-side-by-side.svg | Two questions, three modes. Deployed with the Army: keyword's top is Refinancing and the right policy is missing; semantic's top is Servicemember, which is right; hybrid's top is Refinancing, with the right policy third. 84 months: keyword's top is Payment Deferral, which is right; semantic's right policy is missing; hybrid's top is Payment Deferral, which is right.
@source a1_deployed_synonym.json and a2_84months_keyword_wins.json - top_k 3. Each box: the top result, then where the policy that answers the question landed. Highlighted means it was first.
@notes
- Put the last two slides next to each other. The Army question: semantic wins, keyword misses. The 84 months question: keyword wins, semantic misses. Neither one is just better. They're good at different kinds of questions.
- That's the practical takeaway for the business side: words that people type fall into two kinds. Their own everyday words, where meaning matters. And exact things like figures, names, and codes, where the exact string matters.
- Highlighted cell means the top result is the one that answers the question. Look at hybrid on the Army row: right policy is in the pile, but not on top.
- Analogy: two kinds of colleague. One has a great memory for exact wording. The other has a great feel for what you mean. Which do you ask? Depends on the question.
- Likely question: "Can't the system just pick for us?" Short answer: that's roughly what hybrid does, and next slide shows it working. After that, I'll show you where it doesn't.
@time 10:14

@slide Hybrid earns its keep
@idea "I lost my job and can't make my payment"
@image assets/a3-results.svg | Three columns of top-three results. Keyword: Payment Deferral 0.108 highlighted, Late Fee and Grace 0.075, Electronic Payments 0.066. Semantic: Electronic Payments 0.618, Natural Disaster 0.617, Late Fee and Grace 0.596, with Payment Deferral not returned. Hybrid: Payment Deferral 0.793 highlighted, Late Fee and Grace 0.644, Electronic Payments 0.615.
@source a3_lost_job_mixed.json - top_k 3. The deferral policy lists "job loss" among its hardships.
@notes
- This is the most common hardship question a lender gets, in plain words. The right policy is the standard deferral, POL-101.
- Semantic alone never returns it. Its top three are electronic payments, natural disaster, and late fee. You'd expect semantic to nail this one. It doesn't.
- Keyword catches it, because the policy literally says "job loss". Hybrid blends the two signals and puts the deferral policy first at 0.793.
- So here's where hybrid earns its keep: the question used everyday words, and the policy used a specific phrase. You want both signals.
- Analogy: two people looking for the same file. One searches by the exact phrase, the other by what it's about. Between them they find it.
- Likely question: "Why would semantic miss something so obvious?" Short answer: it's a small model on a small library, and "can't make my payment" sits near several payment policies on the map. It's a real limit, not a bug in the demo. A bigger or different embedding model changes the picture, and you'd test for that.
- For engineers: the embedding model here is bge-small, run locally in the connector with no API key.
@time 10:16

@slide Hybrid is a good default, not a guarantee
@idea Right policy in the top three: hybrid 5 of 6.
@image assets/where-it-landed.svg | A table of six questions across keyword, semantic, and hybrid showing the rank of the right policy in the top three. Late by a few days: 1, 1, 1. Deployed with the Army: not found, 1, 3. 84 months: 1, not found, 1. Lost my job: 1, not found, 1. Flooded in the hurricane: 3, 1, 3. Take my car: not found in any mode.
@source a4, a1, a2, a3, a5, a6 JSON files in the capture - top_k 3. Right policy per question as labelled in the capture. Six questions is a handful, not a benchmark.
@notes
- Here's the honest scoreboard. Six real questions, rank of the right policy in each mode's top three.
- Hybrid had it in the top three five times out of six, and first on three. Keyword four, semantic three. So hybrid is a good place to start.
- But look at the Army row. Semantic had it first. Hybrid pushed it to third. And the hurricane row: hybrid is no better than keyword. Blending two rankings can dilute the one that was right.
- So the claim I'll make is "usually a good default, always check what came back". I won't say "safest". Six questions isn't a benchmark, and I'd be wary of anyone who quotes you a number off a handful.
- The first row is the control: when the question uses the policy's own words, all three agree, and the mode barely matters. Differences show up on everything else.
- Analogy: a panel of two judges who sometimes disagree. Averaging their scores usually works. Sometimes the one who was right gets outvoted.
- Likely question: "So how do we choose?" Short answer: build a small set of real questions with known right answers, run all three modes, and look. That's twenty questions, not two thousand.
@time 10:19

@slide Sometimes nothing finds it
@idea "Can you take my car if I fall behind?"
@image assets/a6-results.svg | Three columns of top-three results. Keyword: Payment Deferral, Late Fee and Grace, and Early Payoff, all scoring 0.0 with no match. Semantic: Insurance 0.61, Payment Deferral 0.607, Natural Disaster 0.597. Hybrid: Insurance 0.305, Payment Deferral 0.303, Natural Disaster 0.299. A banner says Repossession, POL-107, is in none of them.
@source a6_take_my_car_all_miss.json - top_k 3. Keyword scores are all 0.0, so the order is just file order. Hybrid scores are not on the same scale as the others.
@notes
- The honest failure. A customer asks, in plain words, whether we can take their car. The policy is Repossession and Right-to-Cure, POL-107. No mode returns it in the top three.
- Keyword: every score is 0.0. The customer said "take" and "fall behind". The policy says "repossession" and "past due". The three it shows are just the first three policies in the file. Zero means no evidence.
- Semantic puts insurance first. Plausible neighbours, wrong answer. And hybrid's scores around 0.3 look small only because the keyword half had nothing to add. Don't compare scores across modes.
- The lesson: when an answer is wrong, look at what was retrieved before blaming the writing model. Most wrong answers are retrieval problems. If POL-107 never arrives, no amount of clever writing gets it back.
- What do you do about it? Reword the question, ask for more results, add the customer's likely phrases to the policy text, or use a different embedding model. We'll cover some of those in the labs.
- Analogy: the librarian handed you three books and none were the right one. You can't blame the person who reads the books out loud.
- Likely question: "Would a bigger k fix it?" Short answer: maybe, but I haven't tested it here, so I won't promise. The capture only has top 3 for this one.
@time 10:22

@slide A simple vector store: text, numbers, labels
@idea One real record: the whole policy, 384 numbers, a few labels.
@image assets/real-record.svg | A card showing the real record for POL-101. Five fields: id POL-101, title Payment Deferral and Extension Policy, category Hardship and Collections, effective date 2025-01-01, and the start of the policy text. Below, in coral: the embedding, 384 numbers made by BAAI/bge-small-en-v1.5, starting minus 0.0377, minus 0.0155, 0.0031, 0.0185, 0.0072.
@source d_get_policy_POL-101.json and _embedding_pol101.json. The vector was computed locally with the same call the server uses. The connector never shows vectors.
@notes
- A vector store is a table. Each row is one piece of text, its position on the map, and a few labels. That's it.
- This is the real record for POL-101 in our demo store. Five fields: an ID, a title, a category, an effective date, and the text. The text is the whole policy, about 280 words, as one piece.
- Under it, the embedding. 384 numbers, made by a small model called BAAI bge-small. I'm showing you the first five. The real thing is 384 of them, and no human ever reads them. They're just the pin's coordinates.
- Be clear on what you can't see: the connector never hands those numbers out. I computed them locally with the same call the server uses, so I could show you. It builds them when it starts up and holds them in memory.
- Search then works on exactly this: your question gets its own 384 numbers, and the store returns the rows whose numbers are nearest.
- Analogy: a card catalogue. Each card has the title, the shelf location, and a summary. The numbers are the shelf location.
- Likely question: "Does the ID work in search?" Short answer: no. The ID is a label on the row, not part of the text that gets searched. To fetch POL-115 you ask for it by ID, it isn't a search.
- For engineers: the text embedded is title, then a period, then the full policy. One embedding per policy, no splitting.
@time 10:24

@slide What you would add in a real system
@idea This demo store has none of these filters. A real one would.
- Status: only policies that are current
- Audience: customer-facing or internal
- Product: lease, or retail installment
- Effective date: nothing approved but not yet in force
- Source and section: so an answer can cite its source
@source Design ideas, not features of the demo connector. Its search takes only a query, top_k, and a mode.
@notes
- Be straight with the room: the demo has none of this. The real record you just saw has an ID, title, category, and effective date. Search takes a query, a number of results, and a mode. No filters.
- So this slide is about what you'd add when you build one for real. Labels on each record let you narrow the map before you search, so only eligible policies can come back.
- Status is the big one for a lender: never answer from a superseded policy. Audience keeps internal collections guidance out of customer replies. Product keeps a lease question from getting an installment answer.
- Labels are also how you get a citation. If the source and section travel with the record, the answer can point at them, and a person can check.
- My view, personally: good labels often beat a fancier embedding model. I haven't benchmarked that here, so treat it as my read from similar builds, not a measured result.
- Analogy: the card catalogue again. The labels are the "current edition only" and "adult section" stickers.
- Likely question: "Do we need filters from day one?" Short answer: you need to know which ones you'll need before you decide what a record is. Status and effective date are the usual first two for policy.
@time 10:27

@slide Foundations in one slide
@idea Five ideas to take to the next hour.
- Generative AI is fluent, not automatically correct. Give it the right text.
- An embedding is a pin on a map of meaning
- Vector search returns the nearest pins. Top-k is how many you hand over.
- Keyword, semantic, and hybrid return different results. Check what came back.
- A vector store is text, numbers, and labels
@notes
- One slide, five lines, and it's the whole hour. I'll read them out loud and stop.
- Fluent, not correct, so give it the right text. A pin on a map of meaning. Nearest pins come back, and k is how many you read. Three search modes, none of them magic. A store is text, numbers, and labels.
- If you remember one thing, make it this: look at what was retrieved. Not just the answer.
- Likely question: "Where do I see this in the labs?" Short answer: the policy Q&A lab uses this same demo connector. You'll call its search tool from a crew this afternoon.
@time 10:28

@slide Next: when finding the policy is not enough
@idea "A customer on account NW-45512 lost their job and wants to defer their payments. Can we approve a deferral?"
- Search finds the rule: POL-101 first, 0.863
- The rule says: "no more than 30 days past due"
- The account says: 33 days past due
- A fluent answer from the policy alone would be wrong
- Checking the account is a job for an agent: after the break
@source c_agent_case.json - hybrid, top_k 3, then get_client_account. Synthetic account, no real customer.
@notes
- Teaser for the next module, one minute. Same kind of question as before, but about a specific customer.
- Hybrid search gets the right policy first, 0.863. It says the account must be no more than 30 days past due, and a documented job loss can allow a third deferral. A plain search-then-answer system would say "yes, send a separation letter".
- But search can't see this customer's account. When the agent in the capture looked it up, that account was 33 days past due, delinquent, with two missed payments. So the standard deferral isn't available, and the confident answer would have been wrong.
- Finding the policy was never the hard part. Checking the account and then choosing what to search for next is. That's several steps with decisions between them, and it's what we do after the break.
- Analogy: the librarian handed you the policy binder. Somebody still has to go and look at the customer's file.
- Likely question: "Can't we just put the account data into the library?" Short answer: you could for static things, but accounts change by the minute and sit behind their own access rules. You want to ask the system, not copy it. Next module.
@time 10:29

@slide Break
@idea Back at 10:45 for retrieval versus agents, and a live build.
- Stretch, water, ask me anything about the last hour
@notes
- Break until 10:45. Stay on time: the next module starts at 10:45 with the "find it or do it" question.
- If anybody wants to see the real search results up close, the connector is the same one the labs use, and I'm around.
- Likely question: "Will these slides be shared?" Short answer: yes, they're on the workshop site, and the labs are on the labs site linked from the home page.
@time 10:30
