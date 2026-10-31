"""
The dashboard processes player data including scores, achievements,
and activity status to generate various analytics insights.
"""
players = [
    {"name": "alice", "score": 2300, "active": True, "region": "north",
     "achievements": ["first_kill", "level_10", "boss_slayer",
                      "speed_run", "survivor"]},
    {"name": "bob", "score": 1800, "active": True, "region": "east",
     "achievements": ["first_kill", "level_10", "boss_slayer"]},
    {"name": "charlie", "score": 2150, "active": True,  "region": "central",
     "achievements": ["first_kill", "level_10", "boss_slayer", "speed_run",
                      "survivor", "legend", "untouchable"]},
    {"name": "diana", "score": 2050, "active": False, "region": "north",
     "achievements": ["first_kill", "level_10", "boss_slayer", "speedster"]}
]


def score_category(score: int) -> str:
    """
    Categorize a player's score into performance tiers.
    """
    if score >= 2200:
        return "high"
    elif score >= 1900:
        return "medium"
    return "low"


def sort_key(p: dict) -> tuple:
    """
    Generate sorting key for player ranking.
    """
    return (p["score"], len(p["achievements"]))


def main() -> None:
    """
    Execute the main analytics dashboard.
    """
    print("=== Game Analytics Dashboard ===")
    print("\n=== List Comprehension Examples ===")
    high_scorers = [p["name"] for p in players if p["score"] > 2000]
    print(f"High scorers (>2000): {high_scorers}")
    scores_doubled = [p["score"] * 2 for p in players]
    print(f"Scores doubled: {scores_doubled}")
    active_players = [p["name"] for p in players if p["active"]]
    print(f"Active players: {active_players}")

    print("\n=== Dict Comprehension Examples ===")
    player_scores = {p["name"]: p["score"] for p in players if p["active"]}
    print(f"Player scores: {player_scores}")
    categories = ["high", "medium", "low"]
    score_categories = {
        level: sum(1 for p in players if score_category(p["score"]) == level)
        for level in categories
    }
    print(f"Score categories: {score_categories}")
    achievement_counts = {p["name"]: len(p["achievements"])
                          for p in players if p["active"]}
    print(f"Achievement counts: {achievement_counts}")

    print("\n=== Set Comprehension Examples ===")
    unique_players = {p["name"] for p in players}
    print(f"Unique players: {unique_players}")
    unique_achievements = {a for p in players for a in p["achievements"]}
    print(f"Unique achievements: {unique_achievements}")
    active_regions = {p["region"] for p in players if p["active"]}
    print(f"Active regions: {active_regions}")

    print("\n=== Combined Analysis ===")
    total_players = len(unique_players)
    print(f"Total players: {total_players}")
    total_unique_achievements = len(unique_achievements)
    print(f"Total unique achievements: {total_unique_achievements}")
    all_scores = [p["score"] for p in players]
    average_score = sum(all_scores) / len(all_scores)
    print(f"Average score: {average_score}")
    top = sorted(players, key=sort_key, reverse=True)[0]
    print(f"Top performer: {top['name']} ({top['score']} points,"
          f" {len(top['achievements'])} achievements)")


if __name__ == "__main__":
    main()
