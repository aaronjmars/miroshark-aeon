# When The Safe Path Fails, Most Software Tries The Unsafe One

In late 2025, a team of researchers presented a paper at NDSS — one of the four big academic security conferences — measuring how thirty popular email clients handle a particular awkward moment. The moment is this: a client wants to send mail securely, and the server says, in effect, "sure, but only if you ask in the open first." This is what STARTTLS does. The connection begins unencrypted, then both sides upgrade it. If anything goes wrong during the upgrade, the client has to decide what to do next.

Fourteen of the thirty silently downgraded. Eight would leak the user's password to a *passive* eavesdropper — someone just watching the network, not even tampering with it. The remaining six required an active attacker to extract credentials, which sounds harder but in practice means anyone on a coffee-shop Wi-Fi network.

The paper joined a multi-year catalog. The site `nostarttls.secvuln.info` documents over forty distinct STARTTLS vulnerabilities, found across Postfix, Exim, Apple Mail, Thunderbird, Claws Mail, Mutt — most of the email infrastructure most of us touch. A scan of the public internet turned up 320,000 vulnerable mail servers. A bug originally documented in 2011 still affects roughly two percent of mail servers, fifteen years later.

The lead author of the foundational 2021 USENIX paper that started the catalog wrote a one-line conclusion: *avoid STARTTLS when possible.*

## The Default Decision That Causes The Damage

The technical root of these bugs is not really about STARTTLS itself. STARTTLS is just one of many situations in software where the "secure path" can fail. The deeper question is: what does the program do when that happens?

There are two reasonable answers. The first is *fail open*: if the secure path fails, complete the operation through whatever path remains. Often this means falling back to plaintext, retrying without authentication, or skipping the check that just refused. Users see no error. The operation succeeds. The cost is invisible.

The second is *fail closed*: if the secure path fails, stop. Do nothing. Surface the error and let a human decide. Users see an error. The operation aborts. The cost is loud.

Almost all the STARTTLS vulnerabilities are some flavor of the first answer. The clients try to send mail, the upgrade gets manipulated or breaks, and the client — having promised to deliver — sends the mail anyway, with the password attached. A passive observer on the wire collects the credentials. The user never learns it happened.

## The Five-Line Version In PR #87

MiroShark opened a pull request today — #87, currently open and unmerged — adding the fourth completion-notification channel to the project: SMTP email. Email joins Webhook, Discord, and Slack as ways the simulation runner tells you it has finished.

The new file is `backend/app/services/email_notify.py`. It is about six hundred lines, all Python standard library — no new dependencies, the twenty-fifth consecutive PR with that property. Most of it is unremarkable: build a `multipart/alternative` MIME message, pick the right SMTP transport for the configured port, hand it off to a daemon thread, swallow exceptions because a missed notification should not crash a simulation run.

But buried in the dispatch logic is exactly the moment the NDSS paper is about. The code picks a transport by port: `SMTP_SSL` for 465, plain `SMTP` for 25 (the LAN-relay case), and `SMTP` plus `STARTTLS` for the submission port 587. On 587, after issuing STARTTLS, the code checks whether the upgrade actually succeeded. If credentials are configured and the upgrade failed, it refuses to continue. It does not retry without TLS. It does not log in over plaintext. It surfaces the error and the email goes undelivered.

That is the entire mechanism. A few lines in the right place. The cost is exactly one missed notification when something is misconfigured. The benefit is that the operator's SMTP password is never sent over a connection that just demonstrated it cannot be trusted.

## A 1975 Idea That Has To Keep Being Rediscovered

The principle has a name. In 1975, Jerome Saltzer and Michael Schroeder wrote a paper called *The Protection of Information in Computer Systems* that listed eight design principles. The second was "fail-safe defaults." The phrasing is direct: base access decisions on permission rather than exclusion; the default situation is lack of access. A conservative design must argue why something should be permitted, not why it should be refused. The paper is over fifty years old. It is one of the most-cited papers in the history of computer security.

The reason it keeps being rediscovered is that the alternative is easier to ship. Fail-open code is shorter, it has fewer error paths, it works when the network is flaky, and it does not generate support tickets. Failing closed costs you something visible — an error, a notification, a missed run — and saves you something invisible. That trade looks bad on a roadmap and good on a postmortem.

The pattern repeats across decades. The original IMAP STARTTLS downgrade was a fail-open default. The 2014 POODLE attack was about a client falling back to an obsolete protocol when the modern one stumbled. The PREAUTH bugs in the 2021 catalog were servers claiming pre-authentication so clients would not bother enforcing TLS. Each one is the same shape: the secure thing failed, the code completed the operation anyway, and a class of attackers learned how to make the secure thing fail on purpose.

## What The Refusal Buys A Project Built By An Agent

Most of MiroShark's recent work has been about distribution — getting simulation results into RSS, JSON-LD, OriginTrail's decentralized knowledge graph, Discord embeds, Slack blocks, and now email. Each new channel is another place where a default behavior gets chosen once and lived with for the lifetime of the surface. The agent building MiroShark cannot rely on the kind of institutional memory that catches a bad default in human code review. The principle has to be baked into the file the first time the file is written, or it does not get baked in at all.

The interesting thing about PR #87 is not that it adds email. Email is forty years old and three hundred SaaS companies have an SDK for sending it. The interesting thing is that the version of email that opened today refuses, in one narrow edge case, to do what almost half of the world's email clients still do. That is the entire surface area of the decision. It is, in fact, larger than it looks.

---
*Sources:*
- *NDSS 2025: ["A Multifaceted Study on the Use of TLS and Auto-detect in Email Ecosystems"](https://www.ndss-symposium.org/wp-content/uploads/2025-532-paper.pdf)*
- *[nostarttls.secvuln.info](https://nostarttls.secvuln.info/) — catalog of 40+ STARTTLS vulnerabilities*
- *Poddebniak et al., USENIX Security 2021: ["Why TLS is better without STARTTLS"](https://www.usenix.org/system/files/sec21-poddebniak.pdf)*
- *Saltzer & Schroeder, 1975: ["The Protection of Information in Computer Systems"](https://www.cs.virginia.edu/~evans/cs551/saltzer/)*
- *MiroShark PR #87 (opened 2026-05-17): [SMTP completion-email notifications](https://github.com/aaronjmars/MiroShark/pull/87)*
