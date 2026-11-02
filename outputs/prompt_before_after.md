# Prompt test: current vs revised instructions, run live on the ten pack items

Run with `prompts/run_prompts.py` through the Claude Code CLI (model alias `sonnet`). The pilot's production model is not named in the pack, so this tests the **instructions**, not the production system. Pilot column = what the real pilot produced (02_trial_recommendations.json).

| item | pilot | current prompt (today) | revised prompt (today) |
|---|---|---|---|
| src_001 *Metro Kings level Finals with 101-98 Game 2 w* | high / game_result<br>*Grant powers Metro Kings to Game 2 victory* | high / Game recap<br>*Kings Edge Waves 101-98 to Even the Finals at 1-1*<br>no unsupported claims | high / Game result<br>*Metro Kings beat Harbour City Waves 101-98 in Game 2*<br>no unsupported claims |
| src_002 *Watch Malik Grant's 28-point performance in G* | high / game_result<br>*Malik Grant's 28 points level the Finals* | high / Game Highlights<br>*Malik Grant Drops 28 as Metro Kings Even the Finals*<br>no unsupported claims | medium / Game highlights<br>*Malik Grant scores 28 as Metro Kings win Game 2*<br>no unsupported claims |
| src_003 *Medical update: Elias Cole questionable for G* | **no card** | high / Injury Report<br>*Elias Cole's Ankle Puts His Game 3 Status in Doubt*<br>no unsupported claims | high / Player availability<br>*Elias Cole questionable for Game 3 with ankle soreness*<br>no unsupported claims |
| src_004 *Game 3 tipoff moved to 20:00* | **no card** | not relevant: schedule_notice<br>Routine 30-minute tipoff change for Game 3 due to broadcast scheduling. It is Finals-relat | high / Schedule change<br>*Game 3 tipoff moved to 20:00 local time*<br>no unsupported claims |
| src_005 *Tayo Mensah ties Waves playoff assists record* | high / player_record<br>*Mensah sets new league playoff assists record* | low / Stats & Records<br>*Mensah Ties Waves' Playoff Assists Record With 12 Dimes in Game 2*<br>no unsupported claims | high / Player statistics and records<br>*Tayo Mensah ties Harbour City Waves franchise playoff assists record*<br>no unsupported claims |
| src_006 *Win a signed Malik Grant jersey with Northban* | high / player_news<br>*Fans can win Malik Grant's signed jersey* | not relevant: promotional<br>Sponsor giveaway for a signed jersey tied to an insurance quote request. It's a promotiona | not relevant: promotional<br>Sponsor giveaway: "Supporters who request a Northbank Insurance quote before Friday will e |
| src_007 *Game 3 fan zone opens at 17:30* | medium / event_information<br>*Game 3 fan zone opens at 17:30* | high / Event / Fan Experience<br>*Game 3 Fan Zone Opens at 17:30 Outside Harbour Arena*<br>no unsupported claims | medium / Fan information<br>*Championship Finals Game 3 fan zone opens at 17:30*<br>no unsupported claims |
| src_008 *Coach Rivera: lineup decisions will follow fi* | medium / team_news<br>*Waves to decide Game 3 lineup after final practice* | medium / Team News<br>*Waves' Game 3 Lineup Still Up in the Air After Final Practice*<br>no unsupported claims | medium / Team news<br>*Waves coach Rivera: no Game 3 lineup decisions confirmed yet*<br>no unsupported claims |
| src_009 *Game 3 preview: how the Waves can slow Malik * | medium / game_preview<br>*How the Waves could slow Malik Grant in Game 3* | high / Game Preview / Tactical Analysis<br>*Can the Waves Slow Malik Grant? Game 3 Preview Breaks Down Harbour City's Defensive Options*<br>**flags:** 'break' not in source | medium / Game preview<br>*Game 3 preview: how the Waves can slow Malik Grant*<br>no unsupported claims |
| src_010 *Sources: Elias Cole expected to miss Game 3* | not run (unapproved) | high / Injury/Player Availability<br>*Elias Cole Reportedly Expected to Sit Out Game 3*<br>no unsupported claims | medium / Player availability<br>*Sources: Elias Cole expected to miss Game 3*<br>no unsupported claims |

## Full outputs with checks

### src_001 · current

Source: *Metro Kings level Finals with 101-98 Game 2 win* — The Metro Kings beat the Harbour City Waves 101-98 to level the Championship Finals at 1-1. Malik Grant led the Kings with 28 points and eight rebounds.

```json
{
  "relevance": {
    "relevant": true,
    "category": "game_result",
    "reason": "Recap of a Championship Finals Game 2 result that levels the series at 1-1, with a standout performance from Malik Grant (28 points, 8 rebounds). It was published about 12 hours before the current time, so it is timely and of high interest to Finals fans."
  },
  "generation": {
    "category": "Game recap",
    "priority": "high",
    "headline": "Kings Edge Waves 101-98 to Even the Finals at 1-1",
    "summary": "The Metro Kings beat the Harbour City Waves 101-98 in Game 2 of the Championship Finals, levelling the series at 1-1. Malik Grant led the Kings with 28 points and eight rebounds.",
    "source_url": "https://example.com/abl/game-2-recap",
    "why_fans_will_care": "The Finals are now a reset series after the Kings' narrow three-point win, and Malik Grant's 28-point, eight-rebound performance gives Kings fans a standout storyline.",
    "confidence": 0.9
  }
}
```

**Automatic claim check:** clean

### src_001 · revised

Source: *Metro Kings level Finals with 101-98 Game 2 win* — The Metro Kings beat the Harbour City Waves 101-98 to level the Championship Finals at 1-1. Malik Grant led the Kings with 28 points and eight rebounds.

```json
{
  "relevance": {
    "relevant": true,
    "category": "game_result",
    "time_sensitive": false,
    "affects_attending_fans": false,
    "reason": "\"The Metro Kings beat the Harbour City Waves 101-98 to level the Championship Finals at 1-1\" is a final game result published about 12 hours before the current time."
  },
  "generation": {
    "category": "Game result",
    "priority": "high",
    "headline": "Metro Kings beat Harbour City Waves 101-98 in Game 2",
    "summary": "Metro Kings beat the Harbour City Waves 101-98 to level the Championship Finals at 1-1. Malik Grant led the Kings with 28 points and eight rebounds.",
    "source_url": "https://example.com/abl/game-2-recap",
    "why_recommended": "Article from the Aurora Basketball League Newsroom reporting a Championship Finals game result, which is high priority.",
    "media_type": "article",
    "story_key": "game 2 result kings waves",
    "operator_checks": [
      "Score is 101-98 in favour of Metro Kings over Harbour City Waves",
      "Championship Finals now level at 1-1",
      "Malik Grant: 28 points and eight rebounds, led the Kings",
      "Source states this is Game 2 only in the title",
      "Source gives no game time or time zone; only the publish timestamp 2026-09-02T21:03:00Z, which is about 12 hours before the current time"
    ]
  }
}
```

**Automatic claim check:** clean

### src_002 · current

Source: *Watch Malik Grant's 28-point performance in Game 2* — Video highlights from Malik Grant's 28-point performance as the Metro Kings won Game 2 101-98 and tied the Finals at one game each.

```json
{
  "relevance": {
    "relevant": true,
    "category": "player_performance",
    "reason": "Malik Grant scored 28 points in a Finals Game 2 win (101-98) that tied the series 1-1. The item is a highlights video published about 12 hours before the current time, so it is timely. It combines a standout individual performance, a close result and a series-tying moment, which should interest fans."
  },
  "generation": {
    "category": "Game Highlights",
    "priority": "high",
    "headline": "Malik Grant Drops 28 as Metro Kings Even the Finals",
    "summary": "Video highlights show Malik Grant scoring 28 points as the Metro Kings won Game 2, 101-98, tying the Finals at one game each.",
    "source_url": "https://example.com/broadcast/grant-game-2-highlights?utm_source=abl",
    "why_fans_care": "The Finals are now level at 1-1 after a three-point Metro Kings win, and Grant's 28-point game was central to it. Fans can rewatch the key moments in the highlights.",
    "confidence": 0.9
  }
}
```

**Automatic claim check:** clean

### src_002 · revised

Source: *Watch Malik Grant's 28-point performance in Game 2* — Video highlights from Malik Grant's 28-point performance as the Metro Kings won Game 2 101-98 and tied the Finals at one game each.

```json
{
  "relevance": {
    "relevant": true,
    "category": "game_result",
    "time_sensitive": false,
    "affects_attending_fans": false,
    "reason": "Reports that \"the Metro Kings won Game 2 101-98 and tied the Finals at one game each\" with Malik Grant scoring 28 points, published about 12 hours before the current time."
  },
  "generation": {
    "category": "Game highlights",
    "priority": "medium",
    "headline": "Malik Grant scores 28 as Metro Kings win Game 2",
    "summary": "Video highlights of Malik Grant's 28-point performance as the Metro Kings won Game 2 101-98 and tied the Finals at one game each.",
    "source_url": "https://example.com/broadcast/grant-game-2-highlights?utm_source=abl",
    "why_recommended": "Highlights video of a Game 2 result in the Finals. Medium priority because this is a video package, and the source does not show that an article has reported the result.",
    "media_type": "video",
    "story_key": "game 2 result kings finals",
    "operator_checks": [
      "Grant scored 28 points",
      "Metro Kings won Game 2 101-98",
      "Finals tied at one game each",
      "Item is a video highlights package, not an article",
      "Source does not show whether an article has already reported the result; confirm before treating this as medium rather than a repeat"
    ]
  }
}
```

**Automatic claim check:** clean

### src_003 · current

Source: *Medical update: Elias Cole questionable for Game 3* — Guard Elias Cole is questionable for Game 3 after sustaining soreness in his left ankle. He will be assessed after the team's final practice and remains a game-time decision.

```json
{
  "relevance": {
    "relevant": true,
    "category": "injury_news",
    "reason": "Fresh (about an hour old) injury update on guard Elias Cole's availability for Game 3 of the Finals. His status is a game-time decision, so it is timely and of high interest to fans. Editors will want to follow up after the final practice assessment."
  },
  "generation": {
    "category": "Injury Report",
    "priority": "high",
    "headline": "Elias Cole's Ankle Puts His Game 3 Status in Doubt",
    "summary": "Guard Elias Cole is questionable for Game 3 with left ankle soreness. The Harbour City Waves will assess him after the final practice, and he remains a game-time decision.",
    "source_url": "https://example.com/waves/elias-cole-medical-update",
    "why_fans_will_care": "Cole's availability could affect the Waves' lineup in Game 3, and his status won't be settled until after the final practice or possibly game time, so fans should watch for updates.",
    "confidence": 0.9
  }
}
```

**Automatic claim check:** clean

### src_003 · revised

Source: *Medical update: Elias Cole questionable for Game 3* — Guard Elias Cole is questionable for Game 3 after sustaining soreness in his left ankle. He will be assessed after the team's final practice and remains a game-time decision.

```json
{
  "relevance": {
    "relevant": true,
    "category": "player_availability",
    "time_sensitive": true,
    "affects_attending_fans": false,
    "reason": "The Waves state \"Guard Elias Cole is questionable for Game 3 after sustaining soreness in his left ankle. He will be assessed after the team's final practice and remains a game-time decision.\""
  },
  "generation": {
    "category": "Player availability",
    "priority": "high",
    "headline": "Elias Cole questionable for Game 3 with ankle soreness",
    "summary": "Guard Elias Cole is questionable for Game 3 after sustaining soreness in his left ankle. He will be assessed after the team's final practice and remains a game-time decision.",
    "source_url": "https://example.com/waves/elias-cole-medical-update",
    "why_recommended": "Medical update from Harbour City Waves on a player's availability for Game 3, which is a high-priority category. Status is questionable, not ruled out.",
    "media_type": "article",
    "story_key": "elias cole game 3 availability",
    "operator_checks": [
      "Cole is described as 'questionable', not ruled out or confirmed to play",
      "Injury is soreness in his left ankle",
      "He will be assessed after the team's final practice",
      "He remains a game-time decision",
      "Source is Harbour City Waves, published 2026-09-03T08:10:00Z",
      "Source does not give a Game 3 date or time"
    ]
  }
}
```

**Automatic claim check:** clean

### src_004 · revised

Source: *Game 3 tipoff moved to 20:00* — Tipoff for Game 3 of the Championship Finals has moved from 19:30 to 20:00 local time because of an updated broadcast schedule. Arena doors will still open at 17:30.

```json
{
  "relevance": {
    "relevant": true,
    "category": "schedule_change",
    "time_sensitive": true,
    "affects_attending_fans": true,
    "reason": "Source states \"Tipoff for Game 3 of the Championship Finals has moved from 19:30 to 20:00 local time because of an updated broadcast schedule. Arena doors will still open at 17:30.\""
  },
  "generation": {
    "category": "Schedule change",
    "priority": "high",
    "headline": "Game 3 tipoff moved to 20:00 local time",
    "summary": "Tipoff for Game 3 of the Championship Finals moved from 19:30 to 20:00 local time because of an updated broadcast schedule. Arena doors still open at 17:30.",
    "source_url": "https://example.com/abl/game-3-schedule-update",
    "why_recommended": "Change to tipoff time for Game 3 of the Championship Finals, reported by the Aurora Basketball League Newsroom. Doors time is unchanged.",
    "media_type": "article",
    "story_key": "game 3 tipoff time change",
    "operator_checks": [
      "Tipoff moved from 19:30 to 20:00 local time",
      "Reason given: updated broadcast schedule",
      "Arena doors still open at 17:30",
      "Game 3 of the Championship Finals",
      "Source is Aurora Basketball League Newsroom, published 2026-09-03T08:25:00Z",
      "Time zone not stated in source; source says only 'local'"
    ]
  }
}
```

**Automatic claim check:** clean

### src_005 · current

Source: *Tayo Mensah ties Waves playoff assists record* — Tayo Mensah recorded 12 assists in Game 2, tying the Harbour City Waves' franchise record for assists in a playoff game. The Aurora Basketball League playoff record is 17.

```json
{
  "relevance": {
    "relevant": true,
    "category": "player_record",
    "reason": "Published 35 minutes ago, this item reports a playoff milestone: Tayo Mensah's 12 assists in Game 2 tie the Waves' franchise playoff record. It is timely, player-focused and a record, so it is worth an editor's attention. The 12 assists are well short of the league playoff record of 17. The item doesn't say the game was in the Finals, so the Finals link is not confirmed."
  },
  "generation": {
    "category": "Stats & Records",
    "priority": "low",
    "headline": "Mensah Ties Waves' Playoff Assists Record With 12 Dimes in Game 2",
    "summary": "Tayo Mensah recorded 12 assists in Game 2, tying the Harbour City Waves' franchise record for assists in a playoff game. The Aurora Basketball League playoff record is 17.",
    "source_url": "https://example.com/abl/stats/mensah-12-assists",
    "why_fans_care": "Mensah matched a franchise playoff milestone, a notable individual achievement for Waves fans. At 12 assists, he is still five short of the league playoff record of 17, so a further chase may be possible.",
    "confidence": 0.8
  }
}
```

**Automatic claim check:** clean

### src_005 · revised

Source: *Tayo Mensah ties Waves playoff assists record* — Tayo Mensah recorded 12 assists in Game 2, tying the Harbour City Waves' franchise record for assists in a playoff game. The Aurora Basketball League playoff record is 17.

```json
{
  "relevance": {
    "relevant": true,
    "category": "record_or_stat",
    "time_sensitive": false,
    "affects_attending_fans": false,
    "reason": "Official stat from ABL Stats: \"Tayo Mensah recorded 12 assists in Game 2, tying the Harbour City Waves' franchise record for assists in a playoff game. The Aurora Basketball League playoff record is 17.\""
  },
  "generation": {
    "category": "Player statistics and records",
    "priority": "high",
    "headline": "Tayo Mensah ties Harbour City Waves franchise playoff assists record",
    "summary": "Tayo Mensah recorded 12 assists in Game 2, tying the Harbour City Waves' franchise record for assists in a playoff game. The Aurora Basketball League playoff record is 17.",
    "source_url": "https://example.com/abl/stats/mensah-12-assists",
    "why_recommended": "Official statistic from Aurora Basketball League Stats: Mensah's 12 assists in Game 2 tie a Waves franchise playoff record.",
    "media_type": "article",
    "story_key": "mensah 12 assists waves franchise record",
    "operator_checks": [
      "Verb is 'ties', not 'breaks' or 'sets'",
      "Scope is Harbour City Waves franchise record, not a league record",
      "Mensah recorded 12 assists in Game 2",
      "Record is for assists in a playoff game",
      "Aurora Basketball League playoff record is 17, so Mensah's 12 is not a league record",
      "Source is Aurora Basketball League Stats, published 2026-09-03T08:40:00Z",
      "No game opponent or date is given in the source"
    ]
  }
}
```

**Automatic claim check:** clean

### src_007 · current

Source: *Game 3 fan zone opens at 17:30* — The Championship Finals fan zone will open outside Harbour Arena at 17:30. It will include player interviews on the main screen, food stalls and activities for younger fans.

```json
{
  "relevance": {
    "relevant": true,
    "category": "event_promotion",
    "reason": "Fan zone opening at 17:30 is a timely, Finals-linked fan-experience item. The source was published about 23 minutes before the current time, and the zone opens later today ahead of Game 3. It has no news, results or records, so it's low priority. It's worth a brief fan-info or social mention, not a lead story."
  },
  "generation": {
    "category": "Event / Fan Experience",
    "priority": "high",
    "headline": "Game 3 Fan Zone Opens at 17:30 Outside Harbour Arena",
    "summary": "The Championship Finals fan zone opens outside Harbour Arena at 17:30, featuring player interviews on the main screen, food stalls and activities for younger fans.",
    "source_url": "https://example.com/abl/game-3-fan-zone",
    "why_fans_will_care": "Fans heading to Game 3 can arrive early for player interviews, food and family-friendly activities before the game. The item doesn't say the date or tip-off time, so fans should check the league newsroom for details.",
    "confidence": 0.85
  }
}
```

**Automatic claim check:** clean

### src_007 · revised

Source: *Game 3 fan zone opens at 17:30* — The Championship Finals fan zone will open outside Harbour Arena at 17:30. It will include player interviews on the main screen, food stalls and activities for younger fans.

```json
{
  "relevance": {
    "relevant": true,
    "category": "fan_information",
    "time_sensitive": true,
    "affects_attending_fans": true,
    "reason": "The newsroom states \"The Championship Finals fan zone will open outside Harbour Arena at 17:30,\" which is about 8 hours after the current time (09:15Z) and directly affects fans attending Game 3."
  },
  "generation": {
    "category": "Fan information",
    "priority": "medium",
    "headline": "Championship Finals Game 3 fan zone opens at 17:30",
    "summary": "The Championship Finals fan zone outside Harbour Arena opens at 17:30. It will include player interviews on the main screen, food stalls and activities for younger fans.",
    "source_url": "https://example.com/abl/game-3-fan-zone",
    "why_recommended": "Routine fan information from the Aurora Basketball League Newsroom: opening time and programme of the Game 3 fan zone outside Harbour Arena.",
    "media_type": "article",
    "story_key": "game 3 fan zone harbour arena",
    "operator_checks": [
      "Opening time is 17:30",
      "Time zone not stated in source",
      "Location is outside Harbour Arena",
      "Fan zone is for the Championship Finals, Game 3 (from title)",
      "Programme: player interviews on the main screen, food stalls, activities for younger fans",
      "Source does not give the Game 3 tipoff time or date",
      "Source is the Aurora Basketball League Newsroom, published 2026-09-03T08:52:00Z"
    ]
  }
}
```

**Automatic claim check:** clean

### src_008 · current

Source: *Coach Rivera: lineup decisions will follow final practice* — Waves coach Lena Rivera said no Game 3 lineup decisions had yet been confirmed and that player availability would be reviewed after final practice.

```json
{
  "relevance": {
    "relevant": true,
    "category": "team news / injury and availability",
    "reason": "Fresh (15 minutes old) Finals-related update from the Waves coach on Game 3. It confirms no lineup decisions yet and says player availability will be reviewed after final practice. Fans will want to know who plays, so it is worth watching for a follow-up. It is only a status update with no confirmed news, so it is a moderate priority."
  },
  "generation": {
    "category": "Team News",
    "priority": "medium",
    "headline": "Waves' Game 3 Lineup Still Up in the Air After Final Practice",
    "summary": "Coach Lena Rivera said no Game 3 lineup decisions have been confirmed. Player availability will be reviewed after the team's final practice.",
    "source_url": "https://example.com/waves/coach-game-3-availability",
    "why_fans_will_care": "Fans want to know who will play in Game 3. No lineup or availability details are confirmed yet, so an update is expected after final practice.",
    "confidence": 0.9
  }
}
```

**Automatic claim check:** clean

### src_008 · revised

Source: *Coach Rivera: lineup decisions will follow final practice* — Waves coach Lena Rivera said no Game 3 lineup decisions had yet been confirmed and that player availability would be reviewed after final practice.

```json
{
  "relevance": {
    "relevant": true,
    "category": "player_availability",
    "time_sensitive": true,
    "affects_attending_fans": false,
    "reason": "Coach Rivera said \"no Game 3 lineup decisions had yet been confirmed and that player availability would be reviewed after final practice,\" so lineup news is pending and likely to land within hours."
  },
  "generation": {
    "category": "Team news",
    "priority": "medium",
    "headline": "Waves coach Rivera: no Game 3 lineup decisions confirmed yet",
    "summary": "Waves coach Lena Rivera said no Game 3 lineup decisions had yet been confirmed. Player availability would be reviewed after final practice.",
    "source_url": "https://example.com/waves/coach-game-3-availability",
    "why_recommended": "Coach statement confirming no lineup decision yet on Game 3; availability to be reviewed after final practice.",
    "media_type": "article",
    "story_key": "game 3 lineup availability waves",
    "operator_checks": [
      "Rivera is described as Waves coach (Lena Rivera)",
      "No Game 3 lineup decisions had yet been confirmed",
      "Player availability to be reviewed after final practice",
      "Source gives no date or time for final practice",
      "Source published_at is 2026-09-03T09:00:00Z; check it is still current"
    ]
  }
}
```

**Automatic claim check:** clean

### src_009 · current

Source: *Game 3 preview: how the Waves can slow Malik Grant* — The broadcast team reviews the defensive adjustments Harbour City may make after Malik Grant scored 28 points in Game 2.

```json
{
  "relevance": {
    "relevant": true,
    "category": "tactical analysis / game preview",
    "reason": "Fresh (published 11 minutes ago) Game 3 preview tied directly to the Finals, built around Malik Grant's 28-point Game 2 performance and Harbour City's likely defensive adjustments. It is analysis from a broadcast partner and not a breaking result, so it is useful but not top priority."
  },
  "generation": {
    "category": "Game Preview / Tactical Analysis",
    "priority": "high",
    "headline": "Can the Waves Slow Malik Grant? Game 3 Preview Breaks Down Harbour City's Defensive Options",
    "summary": "After Malik Grant scored 28 points in Game 2, a broadcast partner preview reviews the defensive adjustments Harbour City may make in Game 3. Specific tactics are not detailed in the supplied excerpt.",
    "source_url": "https://example.com/broadcast/game-3-tactical-preview",
    "why_fans_care": "Fans heading into Game 3 get a tactical storyline to follow: whether Harbour City can contain Grant after his 28-point Game 2. It frames the key matchup and what to watch for.",
    "confidence": 0.8
  }
}
```

**Automatic claim check:** 'break' not in source

### src_009 · revised

Source: *Game 3 preview: how the Waves can slow Malik Grant* — The broadcast team reviews the defensive adjustments Harbour City may make after Malik Grant scored 28 points in Game 2.

```json
{
  "relevance": {
    "relevant": true,
    "category": "preview_analysis",
    "time_sensitive": true,
    "affects_attending_fans": false,
    "reason": "Approved broadcaster preview: \"The broadcast team reviews the defensive adjustments Harbour City may make after Malik Grant scored 28 points in Game 2.\""
  },
  "generation": {
    "category": "Game preview",
    "priority": "medium",
    "headline": "Game 3 preview: how the Waves can slow Malik Grant",
    "summary": "The broadcast team reviews defensive adjustments Harbour City may make after Malik Grant scored 28 points in Game 2.",
    "source_url": "https://example.com/broadcast/game-3-tactical-preview",
    "why_recommended": "Preview and analysis ahead of Game 3, focused on Malik Grant's 28-point Game 2 and possible Harbour City defensive adjustments.",
    "media_type": "article",
    "story_key": "game 3 preview waves grant",
    "operator_checks": [
      "Malik Grant scored 28 points in Game 2 (stated in source body)",
      "Defensive adjustments are what Harbour City 'may make' (conditional, not confirmed)",
      "Source is a preview/analysis from ABL Broadcast Partner, not a team or league statement",
      "Source does not state a Game 3 date, time or venue; none included",
      "Source does not say whether the item is text or video; article assumed from the wording 'preview'",
      "Headline matches the source title; Waves and Harbour City both named in the source"
    ]
  }
}
```

**Automatic claim check:** clean

### src_010 · current

Source: *Sources: Elias Cole expected to miss Game 3* — Two people described as being close to the team expect Elias Cole to miss Game 3. The Harbour City Waves have not confirmed his status.

```json
{
  "relevance": {
    "relevant": true,
    "category": "player_injury_news",
    "reason": "Unconfirmed report from CourtsideWire, citing two sources close to the team, that Elias Cole is expected to miss Game 3. Published about 90 minutes before the current time, so it is timely, and a player's availability for a Finals game is major news for fans. The Waves have not confirmed it, so an editor should treat it as unverified and look for team confirmation before publishing."
  },
  "generation": {
    "category": "Injury/Player Availability",
    "priority": "high",
    "headline": "Elias Cole Reportedly Expected to Sit Out Game 3",
    "summary": "CourtsideWire reports two people described as close to the team expect Elias Cole to miss Game 3. The Harbour City Waves have not confirmed his status.",
    "source_url": "https://example.com/courtsidewire/cole-expected-out",
    "why_fans_care": "Cole's possible absence could affect the Waves' lineup and outlook for Game 3. The report is unconfirmed and based on anonymous sources, so his status could still change.",
    "confidence": 0.55
  }
}
```

**Automatic claim check:** clean

### src_010 · revised

Source: *Sources: Elias Cole expected to miss Game 3* — Two people described as being close to the team expect Elias Cole to miss Game 3. The Harbour City Waves have not confirmed his status.

```json
{
  "relevance": {
    "relevant": true,
    "category": "player_availability",
    "time_sensitive": true,
    "affects_attending_fans": false,
    "reason": "Report says \"Two people described as being close to the team expect Elias Cole to miss Game 3,\" but \"The Harbour City Waves have not confirmed his status,\" so this is an unconfirmed sourced report."
  },
  "generation": {
    "category": "Player availability",
    "priority": "medium",
    "headline": "Sources: Elias Cole expected to miss Game 3",
    "summary": "Two people described as close to the team expect Elias Cole to miss Game 3. The Harbour City Waves have not confirmed his status.",
    "source_url": "https://example.com/courtsidewire/cole-expected-out",
    "why_recommended": "Unconfirmed report on Elias Cole's Game 3 availability. It rests on sources, not a team or league update, so it is medium priority rather than high.",
    "media_type": "article",
    "story_key": "elias cole game 3 availability",
    "operator_checks": [
      "Status is unconfirmed: source says Harbour City Waves have not confirmed Cole's status",
      "Report relies on two people described as being close to the team, not a team or league statement",
      "Wording is 'expected to miss', not 'ruled out'",
      "Only Game 3 is mentioned; no injury cause or other games stated",
      "Published 2026-09-03T07:48:00Z, about 1 hour 27 minutes before the current time; check for a later team update"
    ]
  }
}
```

**Automatic claim check:** clean
