You are setting up the "genesis-kit" AI-native development system on my machine,
then helping me start my first project with it. Work like an engineer, not a
narrator: after EVERY command, actually run it and paste the real output. Never
say "this should work." If a step fails, stop and tell me exactly what broke.

────────────────────────────────────────
STEP 1 — Check prerequisites
────────────────────────────────────────
Run and show me the versions:
    git --version
    node --version        # need v18 or newer
If node is missing or older than 18, STOP and tell me to install it first.

────────────────────────────────────────
STEP 2 — Clone the three repos into ~/Desktop
────────────────────────────────────────
(If a folder already exists, cd into it and `git pull` instead of cloning.)
    mkdir -p ~/Desktop
    git clone https://github.com/ayush488-glitch/genesis-kit       ~/Desktop/genesis-kit
    git clone https://github.com/ayush488-glitch/skills-directory  ~/Desktop/skills-directory
    git clone https://github.com/ayush488-glitch/agentic-swe-kit   ~/Desktop/agentic-swe-kit
Confirm all three folders exist with: ls -d ~/Desktop/{genesis-kit,skills-directory,agentic-swe-kit}

────────────────────────────────────────
STEP 3 — Install the kit
────────────────────────────────────────
    cd ~/Desktop/genesis-kit && ./install.sh
This installs the agentic-swe-kit, drops the `genesis` skill into my agent, and
sets GENESIS_KIT_ROOT in my shell file. Because that variable won't be live in
this session yet, export it now so the rest of the steps work:
    export GENESIS_KIT_ROOT="$HOME/Desktop/genesis-kit"
Verify the install — both must succeed:
    echo "$GENESIS_KIT_ROOT"
    ls "$GENESIS_KIT_ROOT/tools"        # must show scaffold.sh and graphizer.mjs
Confirm the genesis skill landed in my agent (show whichever exists):
    ls ~/.claude/skills/genesis 2>/dev/null || ls ~/.codex/skills/genesis 2>/dev/null || ls ~/.hermes/skills/genesis 2>/dev/null

────────────────────────────────────────
STEP 4 — Ask me about my project, then scaffold it
────────────────────────────────────────
Ask me: "What are you building, and is there a project folder yet?" WAIT for my
answer. If I have no folder, create one and make it a git repo:
    mkdir -p ~/Desktop/<my-project> && cd ~/Desktop/<my-project> && git init
Then lay the genesis spine into it:
    "$GENESIS_KIT_ROOT/tools/scaffold.sh" .
    node "$GENESIS_KIT_ROOT/tools/graphizer.mjs" . --write
Verify the spine exists: ls -la .genesis
(If .genesis already exists, do NOT overwrite it — read .genesis/checkpoints/CURRENT.md and resume instead.)

────────────────────────────────────────
STEP 5 — Run the genesis ritual (G0–G6) with me
────────────────────────────────────────
Invoke the `genesis` skill and walk me through these, filling the files as you go:
  • G0 — Ask me the 5 diagnostic questions (scope: new/extend/incident · AI
        components? · distributed? · trust boundary? · current phase). Write the
        cognitive job into .genesis/DONE.html section 1.
  • G2 — Add 2–3 invariants BY HAND to .genesis/context-graph.json — the health
        rules that define "not broken" for my project (e.g. "domain never imports
        framework", "every outbound call has a timeout").
  • G3 — Seed .genesis/wiki/index.md with pointers to the agentic-swe-kit concept
        pages my project touches.
  • G4 — Fill .genesis/DONE.html section 2: the definition of done, copied from
        the phase "Gate:" lines.
  • G5 — Slice .genesis/PLAN.md into milestones. EVERY milestone needs one exact
        demo command that proves it works. If you can't write the demo command,
        the milestone is too vague — split it.
  • G6 — Fill .genesis/KICKOFF.md, then show me the "Genesis output checklist" at
        the bottom of .genesis/genesis.md and confirm every box is true.

────────────────────────────────────────
STEP 6 — Tell me what to do next
────────────────────────────────────────
When the checklist is all-true, print a short "You're ready" summary and tell me:
  1. Pick milestone M1 and run G0 Existence Pre-Flight (is it already built?).
  2. Start the BUILD loop. Drive it with my agent's loop/goal command, e.g.
     /goal "M1 done — the M1 demo command passes and L4 VERIFY approves".
  3. Every iteration must pass the 5 gates (G1 Skill, G2 Progress, G3 Cost,
     G4 Quality, G5 Verify) — gates are computed (run the command, paste the
     result), never narrated.
  4. Run L4 VERIFY as a SEPARATE session/model — the maker never grades itself.
  5. To resume later in a cold session, paste .genesis/KICKOFF.md.

RULES THE WHOLE TIME: never overwrite an existing .genesis/. Gates are computed,
not narrated. Never mark a milestone done without a separate L4 VERIFY approval.
Never edit DONE.html or PLAN.md without asking me first.```

