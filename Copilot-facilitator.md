
## おすすめの設定・運用

### 1. 会議の冒頭に、一度だけ指示する

次の文章をFacilitatorとの会議チャットに投稿してください。

```
@Facilitator, establish the following meeting instruction profile for this meeting.

PROFILE NAME: BRIEFING_MODE

Purpose:
Help participants understand the substance of the discussion across English and Japanese without providing literal translations.

Language rules:
- English discussion → concise Japanese summary.
- Japanese discussion → concise English summary.
- Mixed-language discussion → summarize each key point in the opposite language.

Summary format:
1. Main point
2. Rationale or concern
3. What the speaker wants from the team
4. Question or decision requiring attention

Keep responses brief and distinguish confirmed facts from assumptions.

When I use the command "BRIEF", apply this profile to the latest relevant discussion.

When I use "BRIEF-ISSUES", apply this profile and focus on disagreements, risks, and unresolved questions.

When I use "BRIEF-ACTIONS", apply this profile and focus on decisions, action items, owners, and deadlines.

These commands are shorthand instructions for this meeting, not separate tasks. Please follow their defined meanings whenever they are used.
```


### 2. 必要なときだけ、短い指示で呼び出す

通常の要約
@Facilitator BRIEF

意見の相違や未解決事項
@Facilitator BRIEF-ISSUES

決定事項とネクストアクション
@Facilitator BRIEF-ACTIONS
