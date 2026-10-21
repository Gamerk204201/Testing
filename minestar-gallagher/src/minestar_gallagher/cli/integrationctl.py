"""
Simple command-line tool for manual testing of the MineStar-Gallagher integration.

Examples:
    python -m minestar_gallagher.cli.integrationctl set-auth 12345 --enable
    python -m minestar_gallagher.cli.integrationctl set-auth 12345 --enable --dry-run
    python -m minestar_gallagher.cli.integrationctl set-auth 12345 --disable
    python -m minestar_gallagher.cli.integrationctl show-cardholder 12345
    python -m minestar_gallagher.cli.integrationctl list-competencies
"""

from __future__ import annotations

import argparse
import asyncio
import logging
import sys

from clients.gallagher import GallagherClient, GallagherError

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(message)s",
)
logger = logging.getLogger("integrationctl")


async def cmd_set_auth(
    cardholder_id: str,
    enable: bool,
    expiry_minutes: int,
    dry_run: bool = False,
) -> None:
    client = GallagherClient(dry_run=dry_run)
    try:
        success = await client.set_vehicle_authorisation(
            gallagher_cardholder_id=cardholder_id,
            authorised=enable,
            expiry_minutes=expiry_minutes,
            reason="Manual CLI test",
        )
        if success:
            state = "ENABLED" if enable else "DISABLED"
            print(f"OK – competency {state} on cardholder {cardholder_id}")
        else:
            print("FAILED")
            sys.exit(1)
    except GallagherError as e:
        print(f"ERROR: {e}")
        sys.exit(1)
    finally:
        await client.close()


async def cmd_show_cardholder(cardholder_id: str) -> None:
    client = GallagherClient()
    try:
        data = await client.get_cardholder(cardholder_id)

        print(f"\nCardholder ID : {cardholder_id}")
        print(f"Name          : {data.get('firstName', '')} {data.get('lastName', '')}".strip())
        print(f"Description   : {data.get('description', '')}")
        print(f"Authorised    : {data.get('authorised', '')}")

        competencies = data.get("competencies", {})
        results = competencies.get("results") or competencies.get("items") or []

        print("\nCompetencies:")
        if not results:
            print("  (none)")
        for link in results:
            comp = link.get("competency") or {}
            name = comp.get("name") or link.get("name") or "Unknown"
            enabled = link.get("enabled", "?")
            expiry = link.get("expiry") or link.get("expiryDate") or "-"
            print(f"  - {name}  | enabled={enabled}  | expiry={expiry}")
        print()
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)
    finally:
        await client.close()


async def cmd_list_competencies() -> None:
    client = GallagherClient()
    try:
        data = await client._get("/api/competencies")
        results = data.get("results", [])

        print("\nAvailable Competencies in Gallagher:")
        if not results:
            print("  (none found)")
        for item in results:
            print(f"  - {item.get('name')}  (id={item.get('id')})")
        print()
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)
    finally:
        await client.close()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="MineStar-Gallagher integration control tool"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # set-auth
    p_set = sub.add_parser("set-auth", help="Enable or disable AOZ_MINESTAR_AUTHORISED")
    p_set.add_argument("cardholder_id", help="Gallagher vehicle cardholder ID")
    group = p_set.add_mutually_exclusive_group(required=True)
    group.add_argument("--enable", action="store_true", help="Enable the competency")
    group.add_argument("--disable", action="store_true", help="Disable the competency")
    p_set.add_argument(
        "--expiry",
        type=int,
        default=15,
        help="Expiry in minutes when enabling (default: 15)",
    )
    p_set.add_argument(
        "--dry-run",
        action="store_true",
        help="Log the action only – do not call Gallagher",
    )

    # show-cardholder
    p_show = sub.add_parser("show-cardholder", help="Show cardholder details + competencies")
    p_show.add_argument("cardholder_id", help="Gallagher cardholder ID")

    # list-competencies
    sub.add_parser("list-competencies", help="List all competencies in Gallagher")

    args = parser.parse_args()

    if args.command == "set-auth":
        asyncio.run(
            cmd_set_auth(
                cardholder_id=args.cardholder_id,
                enable=args.enable,
                expiry_minutes=args.expiry,
                dry_run=args.dry_run,
            )
        )
    elif args.command == "show-cardholder":
        asyncio.run(cmd_show_cardholder(args.cardholder_id))
    elif args.command == "list-competencies":
        asyncio.run(cmd_list_competencies())


if __name__ == "__main__":
    main()