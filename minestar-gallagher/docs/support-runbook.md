# Support Runbook

## Common Issues

**Service won't start**
- Check Event Log
- Verify .env has correct keys
- Test with `python src/main.py`

**No gate access**
- Check competency on vehicle in Gallagher
- Verify MineStar shows authorised login
- Look in audit table

**High CPU**
- Check polling interval in synchronisation.py

## Useful Commands
integrationctl status
integrationctl test-minestar
integrationctl test-gallagher