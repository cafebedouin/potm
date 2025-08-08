name: benefit-signal-lint
on:
  issues:
    types: [opened, edited]
jobs:
  lint:
    if: contains(join(fromJson(toJson(github.event.issue.labels)).*.name, ','), 'benefit-signal')
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Echo hint if practice_id seems unknown (skeleton)
        env:
          ISSUE_BODY: ${{ github.event.issue.body }}
        run: |
          echo "This is a placeholder. Optional script can parse ISSUE_BODY,"
          echo "compare against core/meta/ledger.yaml ids, and comment suggestions."
