import click
import asyncio
from minestar_gallagher.clients.minestar import get_current_qualifications
from minestar_gallagher.clients.gallagher import update_vehicle_authorisation
from minestar_gallagher.services.synchronisation import daily_full_sync

@click.group()
def cli():
    """MineStar-Gallagher Integration CLI"""
    pass

@cli.command()
def status():
    """Show service status"""
    click.echo("Service is running (check Windows Services)")

@cli.command()
async def test_minestar():
    """Test MineStar connection"""
    try:
        data = await get_current_qualifications()
        click.echo(f"Success! Found {len(data)} current assignments")
        for v, info in list(data.items())[:5]:
            click.echo(f"  Vehicle {v}: authorised={info['is_authorised']}")
    except Exception as e:
        click.echo(f"Failed: {e}")

@cli.command()
@click.argument("vehicle_id")
async def test_gallagher(vehicle_id):
    """Test Gallagher update for a vehicle"""
    try:
        await update_vehicle_authorisation(vehicle_id, True, reason="CLI test")
        click.echo(f"Competency enabled on {vehicle_id}")
    except Exception as e:
        click.echo(f"Failed: {e}")

@cli.command()
async def reconcile():
    """Run full sync now"""
    click.echo("Running full sync...")
    await daily_full_sync()
    click.echo("Done.")

if __name__ == '__main__':
    cli()