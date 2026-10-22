"""
Proof-of-concept: load MineStar scenarios from JSON and show Gallagher dry-run actions.
"""

import asyncio
import json
from pathlib import Path

from clients.gallagher import GallagherClient

def load_scenarios(path: str = "test_scenarios.json"):
    with open(path, "r") as f:
        return json.load(f)

async def main():
    scenarios = load_scenarios()
    client = GallagherClient(dry_run=True)

    print("\n=== MineStar → Gallagher Dry-Run Proof of Concept ===\n")

    for s in scenarios:
        print(f"MineStar event:")
        print(f"  Vehicle   : {s['vehicle']}")
        print(f"  Operator  : {s['operator']}")
        print(f"  Competent : {s['competent']}")
        print(f"  Reason    : {s['reason']}")
        print()

        await client.set_vehicle_authorisation(
            gallagher_cardholder_id=s["vehicle"],
            authorised=s["competent"],
            reason=s["reason"],
        )
        print("-" * 60)

    await client.close()
    print("\n=== End of proof-of-concept ===\n")

if __name__ == "__main__":
    asyncio.run(main())