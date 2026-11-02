# Prompt test: current vs revised instructions, run live on the ten pack items

Run with `prompts/run_prompts.py` through the Claude Code CLI (model alias `sonnet`). The pilot's production model is not named in the pack, so this tests the **instructions**, not the production system. Pilot column = what the real pilot produced (02_trial_recommendations.json).

| item | pilot | current prompt (today) | revised prompt (today) |
|---|---|---|---|
| src_001 *Metro Kings level Finals with 101-98 Game 2 w* | high / game_result<br>*Grant powers Metro Kings to Game 2 victory* | medium / Match Result<br>*Metro Kings Edge Waves 101-98 to Even the Finals at 1-1*<br>no unsupported claims | high / Basketball<br>*Metro Kings beat Harbour City Waves 101-98 in Game 2*<br>no unsupported claims |
| src_002 *Watch Malik Grant's 28-point performance in G* | high / game_result<br>*Malik Grant's 28 points level the Finals* | high / Game Highlights<br>*Malik Grant Drops 28 as Metro Kings Even the Finals With a 101-98 Thriller*<br>no unsupported claims | high / Game result<br>*Metro Kings beat opponent 101-98 in Game 2; Grant scores 28*<br>no unsupported claims |
| src_003 *Medical update: Elias Cole questionable for G* | **no card** | high / Injury Update<br>*Elias Cole's Ankle Puts Game 3 Status in Doubt for the Waves*<br>no unsupported claims | high / Player availability<br>*Elias Cole questionable for Game 3 with left ankle soreness*<br>no unsupported claims |
| src_004 *Game 3 tipoff moved to 20:00* | **no card** | high / Schedule Update<br>*Game 3 Tipoff Pushed Back 30 Minutes to 8 PM*<br>**flags:** numbers not in source ['8'] | high / Schedule change<br>*Game 3 of Championship Finals tipoff moved to 20:00 local*<br>no unsupported claims |
| src_005 *Tayo Mensah ties Waves playoff assists record* | high / player_record<br>*Mensah sets new league playoff assists record* | not relevant: player_performance_record<br>Mensah only tied a franchise playoff assists mark, which is well short of the league recor | high / Basketball<br>*Tayo Mensah ties Waves playoff assists record with 12*<br>no unsupported claims |
| src_006 *Win a signed Malik Grant jersey with Northban* | high / player_news<br>*Fans can win Malik Grant's signed jersey* | not relevant: promotional<br>Sponsor giveaway for a signed jersey tied to an insurance quote request. It's a promotiona | not relevant: promotional<br>Sponsor giveaway: "Supporters who request a Northbank Insurance quote before Friday will e |
| src_007 *Game 3 fan zone opens at 17:30* | medium / event_information<br>*Game 3 fan zone opens at 17:30* | not relevant: promotional/event logistics<br>Routine fan-zone opening notice for Game 3. It is tied to the Finals but offers no major p | medium / Fan information<br>*Game 3 fan zone opens at 17:30 outside Harbour Arena*<br>no unsupported claims |
| src_008 *Coach Rivera: lineup decisions will follow fi* | medium / team_news<br>*Waves to decide Game 3 lineup after final practice* | medium / Team News<br>*Waves Game 3 Lineup Still Up in the Air After Coach Rivera's Update*<br>no unsupported claims | high / Team news<br>*Waves coach Rivera: no Game 3 lineup decisions confirmed yet*<br>no unsupported claims |
| src_009 *Game 3 preview: how the Waves can slow Malik * | medium / game_preview<br>*How the Waves could slow Malik Grant in Game 3* | medium / Game Preview / Tactical Analysis<br>*Can the Waves Cool Off Malik Grant? Game 3 Tactical Preview*<br>no unsupported claims | medium / Basketball preview<br>*Game 3 preview: how the Waves can slow Malik Grant*<br>no unsupported claims |
| src_010 *Sources: Elias Cole expected to miss Game 3* | not run (unapproved) | medium / Injury/Availability<br>*Report: Elias Cole Likely Sidelined for Game 3*<br>no unsupported claims | high / Player availability<br>*Sources: Elias Cole expected to miss Game 3*<br>no unsupported claims |

## Full outputs with checks

### src_001 · current

Source: *Metro Kings level Finals with 101-98 Game 2 win* — The Metro Kings beat the Harbour City Waves 101-98 to level the Championship Finals at 1-1. Malik Grant led the Kings with 28 points and eight rebounds.

```json
{
  "relevance": {
    "relevant": true,
    "category": "game_result",
    "reason": "Timely Finals Game 2 result: the Metro Kings beat the Harbour City Waves 101-98 to level the series at 1-1, with a strong performance from Malik Grant (28 points, 8 rebounds). Fans following the Finals will want this."
  },
  "generation": {
    "category": "Match Result",
    "priority": "medium",
    "headline": "Metro Kings Edge Waves 101-98 to Even the Finals at 1-1",
    "summary": "The Metro Kings beat the Harbour City Waves 101-98 in Game 2 to level the Championship Finals at 1-1. Malik Grant led the Kings with 28 points and eight rebounds.",
    "source_url": "https://example.com/abl/game-2-recap",
    "why_fans_will_care": "The Finals are now a fresh best-of series, with the Kings answering back after what appears to be a Game 1 loss. Grant's 28-point, eight-rebound showing and the three-point margin point to a tight, tense contest.",
    "confidence": 0.85
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
    "time_sensitive": true,
    "affects_attending_fans": false,
    "reason": "The source reports \"The Metro Kings beat the Harbour City Waves 101-98 to level the Championship Finals at 1-1.\""
  },
  "generation": {
    "category": "Basketball",
    "priority": "high",
    "headline": "Metro Kings beat Harbour City Waves 101-98 in Game 2",
    "summary": "The Metro Kings beat the Harbour City Waves 101-98 to level the Championship Finals at 1-1. Malik Grant led the Kings with 28 points and eight rebounds.",
    "source_url": "https://example.com/abl/game-2-recap",
    "why_recommended": "Game result from the Championship Finals, sourced from the Aurora Basketball League Newsroom.",
    "media_type": "article",
    "story_key": "game 2 result kings waves",
    "operator_checks": [
      "Score is 101-98 in favour of Metro Kings over Harbour City Waves",
      "Championship Finals now level at 1-1",
      "Malik Grant scored 28 points and had eight rebounds",
      "Game is Game 2 per the source title",
      "No game time or time zone in source body; published_at is 2026-09-02T21:03:00Z"
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
    "reason": "Highlights of Malik Grant's 28-point Game 2 performance, which helped the Metro Kings win 101-98 and tie the Finals 1-1. It combines a standout individual performance, a key result and direct Finals relevance, and it is video content that is easy to publish. Its timeliness is limited: the item is dated 2026-09-02, which is two months before today's date."
  },
  "generation": {
    "content_id": "src_002",
    "category": "Game Highlights",
    "priority": "high",
    "headline": "Malik Grant Drops 28 as Metro Kings Even the Finals With a 101-98 Thriller",
    "summary": "Video highlights show Malik Grant scoring 28 points as the Metro Kings beat their opponent 101-98 in Game 2, tying the Finals at one game each.",
    "source_url": "https://example.com/broadcast/grant-game-2-highlights",
    "why_fans_care": "A three-point win levelled the Finals at 1-1, and the highlights let fans relive Grant's 28-point performance that made it happen.",
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
    "reason": "The item reports that \"the Metro Kings won Game 2 101-98 and tied the Finals at one game each,\" which is a game result, even though it is framed as video highlights."
  },
  "generation": {
    "category": "Game result",
    "priority": "high",
    "headline": "Metro Kings beat opponent 101-98 in Game 2; Grant scores 28",
    "summary": "Video highlights of Malik Grant's 28-point performance as the Metro Kings won Game 2 101-98 and tied the Finals at one game each.",
    "source_url": "https://example.com/broadcast/grant-game-2-highlights?utm_source=abl",
    "why_recommended": "Reports a Finals game result: Metro Kings won Game 2 101-98 and tied the series at one game each, with Malik Grant scoring 28 points.",
    "media_type": "video",
    "story_key": "game 2 result metro kings finals",
    "operator_checks": [
      "Metro Kings won Game 2 101-98",
      "Malik Grant scored 28 points",
      "Finals tied at one game each",
      "Source does not name the opponent",
      "Item is video highlights from ABL Broadcast Partner",
      "Published 2026-09-02T21:06:00Z; no time zone claim made beyond the source's Z suffix"
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
    "category": "injury_update",
    "reason": "Questionable status for guard Elias Cole ahead of Game 3 is timely, high-interest Finals news that affects the matchup and fan expectations. The game-time decision means it should be surfaced now, with a follow-up once he is assessed after the final practice."
  },
  "generation": {
    "category": "Injury Update",
    "priority": "high",
    "headline": "Elias Cole's Ankle Puts Game 3 Status in Doubt for the Waves",
    "summary": "Harbour City Waves guard Elias Cole is questionable for Game 3 with left ankle soreness. He'll be assessed after the team's final practice and is a game-time decision.",
    "source_url": "https://example.com/waves/elias-cole-medical-update",
    "why_fans_care": "Cole's availability could affect the Waves' lineup and game plan for Game 3, and his status won't be settled until after the final practice, possibly not until game time.",
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
    "reason": "Source states \"Guard Elias Cole is questionable for Game 3 after sustaining soreness in his left ankle\" and \"remains a game-time decision.\""
  },
  "generation": {
    "category": "Player availability",
    "priority": "high",
    "headline": "Elias Cole questionable for Game 3 with left ankle soreness",
    "summary": "Guard Elias Cole is questionable for Game 3 after sustaining soreness in his left ankle. He will be assessed after the team's final practice and remains a game-time decision.",
    "source_url": "https://example.com/waves/elias-cole-medical-update",
    "why_recommended": "Official team medical update on a player's availability for Game 3, with the status still undecided pending assessment after the final practice.",
    "media_type": "article",
    "story_key": "elias cole game 3 availability",
    "operator_checks": [
      "Cole is listed as questionable, not out",
      "Injury is soreness in his left ankle",
      "Assessment follows the team's final practice",
      "Cole remains a game-time decision",
      "Source is Harbour City Waves; published_at 2026-09-03T08:10:00Z",
      "Source names no opponent, game date or kickoff time",
      "Source names no time zone for the assessment or game"
    ]
  }
}
```

**Automatic claim check:** clean

### src_004 · current

Source: *Game 3 tipoff moved to 20:00* — Tipoff for Game 3 of the Championship Finals has moved from 19:30 to 20:00 local time because of an updated broadcast schedule. Arena doors will still open at 17:30.

```json
{
  "relevance": {
    "relevant": true,
    "category": "schedule_change",
    "reason": "Game 3 tipoff of the Championship Finals moved from 19:30 to 20:00 local time. Fans attending or watching need this timely logistical update, so it's worth a brief service item. It's routine and not a major news story, so priority is low to moderate."
  },
  "generation": {
    "category": "Schedule Update",
    "priority": "high",
    "headline": "Game 3 Tipoff Pushed Back 30 Minutes to 8 PM",
    "summary": "Game 3 of the Championship Finals now tips off at 20:00 local time instead of 19:30, due to an updated broadcast schedule. Arena doors still open at 17:30.",
    "source_url": "https://example.com/abl/game-3-schedule-update",
    "why_fans_will_care": "Fans attending or watching need the new start time to plan travel and viewing. Doors still open at 17:30, so ticket holders will have a longer wait before tipoff.",
    "confidence": 0.95
  }
}
```

**Automatic claim check:** numbers not in source ['8']

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
    "headline": "Game 3 of Championship Finals tipoff moved to 20:00 local",
    "summary": "Tipoff for Game 3 of the Championship Finals has moved from 19:30 to 20:00 local time because of an updated broadcast schedule. Arena doors will still open at 17:30.",
    "source_url": "https://example.com/abl/game-3-schedule-update",
    "why_recommended": "Official schedule change to a Championship Finals game start time, relevant to fans attending and watching.",
    "media_type": "article",
    "story_key": "game 3 tipoff time change",
    "operator_checks": [
      "Tipoff moved from 19:30 to 20:00 local time",
      "Game 3 of the Championship Finals",
      "Reason: updated broadcast schedule",
      "Arena doors still open at 17:30",
      "Time zone not stated in source; source says only 'local time'",
      "Source is Aurora Basketball League Newsroom, published 2026-09-03T08:25:00Z"
    ]
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
    "reason": "Official stats source states \"Tayo Mensah recorded 12 assists in Game 2, tying the Harbour City Waves' franchise record for assists in a playoff game. The Aurora Basketball League playoff record is 17.\""
  },
  "generation": {
    "category": "Basketball",
    "priority": "high",
    "headline": "Tayo Mensah ties Waves playoff assists record with 12",
    "summary": "Tayo Mensah recorded 12 assists in Game 2, tying the Harbour City Waves' franchise record for assists in a playoff game. The Aurora Basketball League playoff record is 17.",
    "source_url": "https://example.com/abl/stats/mensah-12-assists",
    "why_recommended": "Official stat report of a franchise playoff record being tied, which falls under the high-priority record category.",
    "media_type": "article",
    "story_key": "mensah 12 assists game 2 waves",
    "operator_checks": [
      "Mensah recorded 12 assists in Game 2",
      "Record is tied, not broken",
      "Record scope is Harbour City Waves franchise record for assists in a playoff game",
      "Aurora Basketball League playoff record is 17, so this is not a league record",
      "Source is Aurora Basketball League Stats"
    ]
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
    "reason": "The source states \"The Championship Finals fan zone will open outside Harbour Arena at 17:30,\" which is fan-logistics information for attending fans."
  },
  "generation": {
    "category": "Fan information",
    "priority": "medium",
    "headline": "Game 3 fan zone opens at 17:30 outside Harbour Arena",
    "summary": "The Championship Finals fan zone opens outside Harbour Arena at 17:30. It will include player interviews on the main screen, food stalls and activities for younger fans.",
    "source_url": "https://example.com/abl/game-3-fan-zone",
    "why_recommended": "Fan information from the Aurora Basketball League Newsroom giving the opening time and location of the Game 3 fan zone for the Championship Finals.",
    "media_type": "article",
    "story_key": "game 3 fan zone harbour arena",
    "operator_checks": [
      "Opening time is 17:30 as written in the source",
      "Time zone not stated in source",
      "Location is outside Harbour Arena",
      "Fan zone is for the Championship Finals",
      "Includes player interviews on the main screen, food stalls and activities for younger fans",
      "Source title refers to Game 3"
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
    "category": "team_news",
    "reason": "Game 3 coach update from the Waves ahead of a Finals game. The item confirms no lineup decisions yet and says player availability will be reviewed after final practice. Fans care about availability, and an editor could follow up once the lineup is set. It has no hard news yet, so it is moderate priority at best."
  },
  "generation": {
    "category": "Team News",
    "priority": "medium",
    "headline": "Waves Game 3 Lineup Still Up in the Air After Coach Rivera's Update",
    "summary": "Coach Lena Rivera said no Game 3 lineup decisions have been confirmed. Player availability will be reviewed after the team's final practice.",
    "source_url": "https://example.com/waves/coach-game-3-availability",
    "why_fans_care": "Fans hoping to know who will play in Game 3 must wait: no lineup is confirmed, and availability will only be reviewed after final practice. The item gives no details on specific players or injuries.",
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
    "category": "team_statement",
    "time_sensitive": true,
    "affects_attending_fans": false,
    "reason": "Coach Rivera said \"no Game 3 lineup decisions had yet been confirmed and that player availability would be reviewed after final practice,\" a team statement on selection with an update pending."
  },
  "generation": {
    "category": "Team news",
    "priority": "high",
    "headline": "Waves coach Rivera: no Game 3 lineup decisions confirmed yet",
    "summary": "Waves coach Lena Rivera said no Game 3 lineup decisions had yet been confirmed. Player availability would be reviewed after final practice.",
    "source_url": "https://example.com/waves/coach-game-3-availability",
    "why_recommended": "Coach statement on Game 3 player availability; availability news is high priority, and the decision is still pending.",
    "media_type": "article",
    "story_key": "game 3 lineup availability waves",
    "operator_checks": [
      "Lena Rivera is named as Waves coach",
      "No Game 3 lineup decisions had yet been confirmed",
      "Player availability to be reviewed after final practice",
      "No specific players named as available or unavailable",
      "No time or time zone stated for final practice or decisions",
      "Source is Harbour City Waves; published_at 2026-09-03T09:00:00Z; may be outdated"
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
    "category": "tactical analysis",
    "reason": "Timely Game 3 preview tied to the Finals, focusing on star player Malik Grant's 28-point Game 2 and the defensive adjustments Harbour City may make. It's of strong fan interest, though it's analysis rather than breaking news, so priority is moderate."
  },
  "generation": {
    "category": "Game Preview / Tactical Analysis",
    "priority": "medium",
    "headline": "Can the Waves Cool Off Malik Grant? Game 3 Tactical Preview",
    "summary": "Broadcast partner's team reviews defensive adjustments Harbour City may make in Game 3 after Malik Grant scored 28 points in Game 2. Specific tactics are not detailed in the supplied item.",
    "source_url": "https://example.com/broadcast/game-3-tactical-preview",
    "why_fans_care": "Fans following the series get a look at the key matchup and how Harbour City might respond to Grant's Game 2 scoring ahead of Game 3.",
    "confidence": 0.7
  }
}
```

**Automatic claim check:** clean

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
    "category": "Basketball preview",
    "priority": "medium",
    "headline": "Game 3 preview: how the Waves can slow Malik Grant",
    "summary": "Broadcast team reviews defensive adjustments Harbour City may make after Malik Grant scored 28 points in Game 2.",
    "source_url": "https://example.com/broadcast/game-3-tactical-preview",
    "why_recommended": "Game 3 preview from ABL Broadcast Partner covering likely defensive adjustments against Malik Grant, who scored 28 points in Game 2.",
    "media_type": "article",
    "story_key": "game 3 preview waves grant",
    "operator_checks": [
      "Source says Malik Grant scored 28 points in Game 2",
      "Source says Harbour City 'may' make defensive adjustments; this is a preview, not confirmed",
      "Headline names the Waves while the body names Harbour City; confirm they are the same team",
      "Source does not state the sport; category 'Basketball preview' is inferred, confirm or change",
      "Source does not say whether it is an article or video; media_type 'article' is assumed from the text body, confirm",
      "Published time 2026-09-03T09:04:00Z; no game time given in source"
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
    "category": "player_availability",
    "reason": "Unconfirmed report from anonymous sources that Elias Cole is expected to miss Game 3 of the Finals. Player availability news is timely and high-interest for fans. Because the Waves have not confirmed it, an editor should frame it as unverified and watch for an official injury report."
  },
  "generation": {
    "category": "Injury/Availability",
    "priority": "medium",
    "headline": "Report: Elias Cole Likely Sidelined for Game 3",
    "summary": "CourtsideWire, citing two people described as close to the team, reports Elias Cole is expected to miss Game 3. The Harbour City Waves have not confirmed his status.",
    "source_url": "https://example.com/courtsidewire/cole-expected-out",
    "why_fans_will_care": "Cole's possible absence could affect the Waves' lineup and outlook for Game 3, but the report is unconfirmed, so fans should watch for official team word.",
    "confidence": 0.6
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
    "reason": "Report says \"Two people described as being close to the team expect Elias Cole to miss Game 3,\" but \"The Harbour City Waves have not confirmed his status,\" so this is unconfirmed."
  },
  "generation": {
    "category": "Player availability",
    "priority": "high",
    "headline": "Sources: Elias Cole expected to miss Game 3",
    "summary": "Two people described as close to the team expect Elias Cole to miss Game 3. The Harbour City Waves have not confirmed his status.",
    "source_url": "https://example.com/courtsidewire/cole-expected-out",
    "why_recommended": "Player availability report for Game 3 from CourtsideWire, based on unnamed sources and not confirmed by the Harbour City Waves.",
    "media_type": "article",
    "story_key": "elias cole game 3 availability",
    "operator_checks": [
      "Elias Cole is reported as 'expected' to miss Game 3, not confirmed out",
      "Attribution is 'two people described as being close to the team' (unnamed sources)",
      "Harbour City Waves have not confirmed his status",
      "Source is CourtsideWire, published 2026-09-03T07:48:00Z",
      "Source does not state a reason for the absence"
    ]
  }
}
```

**Automatic claim check:** clean
