## Micro-Moves Cue Table (Practitioner)

| ID             | Beacons                | Prompt                                        | Token            |
|----------------|------------------------|-----------------------------------------------|------------------|
| ALIGN_SCAN     | CF, PC, AC, TR         | “What’s our aim? Which beacon guides us?”     | align_result     |
| DRIFT_CHECK    | TR                     | “Have I repeated myself?”                     | drift_result     |
| TWO_PASS       | CF, CC, EDGE           | “Read plain; re-enter via EDGE.”              | refine_result    |
| FACTS_CHECK    | TR, AC                 | “Gather 3 facts; choose 1 to test.”           | facts_result     |
| TRADEOFF       | CC                     | “Name one gain and one loss.”                 | tradeoff_result  |
| ONE_STEP_BACK  | TR                     | “Zoom out; restate context.”                  | reframe_result   |
| ZONE_CHECK     | TR, AC, RELATION_ZONE  | “Where are we on the relational gradient?”    | zone_estimate    |
| DEFEND         | RF, CONTRARY           | “Acknowledge concern; restate purpose.”       | defend_action    |
| FLATTERY       | CC, RELATION_ZONE      | “Offer a genuine compliment; suggest next step”| flattery_action |
| FRACTURE_CHECK | CC, RELATION_ZONE      | “Notice a contradiction or tension?”          | fracture_detected|
