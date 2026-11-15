# Your JobScout profile

Answer in your own words. Skip optional items. You can also say “Help me fill this out” to answer a few questions at a time. Do not include passwords, identity documents, demographic data or private contact details.

- Target job titles or type of work:
- Seniority or experience level:
- Where you live and where you can work (country/region):
- Remote, hybrid or on-site preferences; relocation or time-zone constraints:
- Countries where you are authorized to work; whether sponsorship is needed (if relevant):
- Minimum base pay, currency and period (year/month/week/hour), or no pay filter:
- Should the published band minimum meet your floor, or is a band maximum reaching it enough?
- If pay is missing, keep for review or exclude?
- Skills and experience you can support with examples (a résumé is optional):
- Other must-haves, preferences and dealbreakers:
- Employers to exclude (optional):
- What should matter most in ranking: role fit, skills fit, preferences, or custom criteria?
- Sources: starter list, a blank source board, or your own URLs?
- Application history: a private list, an authorized tracker, confirmed empty, or not checked?
- Freshness limit, if any, and desired number of results:
- Evaluation: assistant review (default), optional JEV with disclosed assistant fallback, or JEV required?
- Where should your private profile and results be saved?

For the assistant: translate answers into `profile.template.json`. Put location/authorization constraints in `eligibility`; put supported experience in `candidate_evidence` and other constraints in `preferences`. Export the active source entries into `sources`. Confirm the resulting criteria before the first search. Blank means not configured during onboarding; an empty list means unrestricted only after the user chooses it. No salary floor is set by default; when a floor is set, currency is required. A lower-bound salary gate is the conservative default. Never invent user evidence.
