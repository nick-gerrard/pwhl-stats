"""
Run all ingestion modules in dependency order.

Order matters — foreign keys require parent tables to be populated first:
  seasons, teams → players → roster
  seasons, teams → games
  seasons, teams, players → skater_stats, goalie_stats
  seasons, teams → standings
"""

import asyncio

from ingestions import games, goalie_stats, playoffs, roster, seasons, skater_stats, standings, teams


async def run_all():
    print("--- Ingesting seasons ---")
    await seasons.run()

    print("--- Ingesting teams ---")
    await teams.run()

    print("--- Ingesting players ---")
    from ingestions import players
    await players.run()

    print("--- Ingesting roster ---")
    await roster.run()

    print("--- Ingesting games ---")
    await games.run()

    print("--- Ingesting skater stats ---")
    await skater_stats.run()

    print("--- Ingesting goalie stats ---")
    await goalie_stats.run()

    print("--- Ingesting standings ---")
    await standings.run()

    print("--- Ingesting playoffs ---")
    await playoffs.run()

    print("=== All ingestion complete ===")


if __name__ == "__main__":
    asyncio.run(run_all())
