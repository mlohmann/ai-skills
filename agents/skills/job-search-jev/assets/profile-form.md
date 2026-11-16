# Your JobScout profile

Answer in your own words, or ask your agent to help you a few questions at a time. You can skip optional preferences. Don't include passwords, identity documents, demographic data, or private contact details.

[Work and location](#work-and-location) · [Pay and priorities](#pay-and-priorities) · [Search setup](#search-setup) · [Instructions for the agent](#instructions-for-the-agent)

## Work and location

- Target job titles or type of work:
- Seniority or experience level:
- Country or region where you live:
- Locations where you can work:
- Remote, hybrid, or on-site preferences:
- Relocation or time zone constraints:
- Countries where you're authorized to work, and whether you need sponsorship:
- Skills and experience you can support with examples:

A résumé is optional.

## Pay and priorities

- Minimum base pay, currency, and period, or no pay filter:
- Should the published band minimum meet your minimum, or is a band maximum that reaches it enough?
- If pay is missing, should the job stay in review or be excluded?
- Other requirements, preferences, or dealbreakers:
- Employers to exclude, if any:
- What matters most in ranking: role fit, skills fit, preferences, or your own criteria?

Use year, month, week, or hour as the pay period.

## Search setup

- Sources: starter list, blank source board, or your own URLs?
- History: private records, an authorized tracker, checked and empty, or not checked?
- Maximum posting age, if needed:
- Number of results you'd like:
- Evaluation: assistant review, optional JEV with disclosed fallback, or JEV required?
- Private location for your profile and results:

Assistant review is the default. Starter sources are manual links until a permitted access method is established.

## Instructions for the agent

Create a private profile with the structure in `profile.template.json`. Do not edit the public template in place.

Put location and authorization constraints in `eligibility`. Put supported experience in `candidate_evidence`. Put other constraints in `preferences`. Copy the selected source entries into `sources`.

Confirm the settings before the first search. An unanswered field is not a confirmed unrestricted preference. Use an empty list for unrestricted preferences only after confirmation.

No pay minimum is set by default. A configured minimum requires a currency. Explain the default `lower_bound` policy: the published band minimum must meet the user's minimum. Do not invent candidate evidence.
