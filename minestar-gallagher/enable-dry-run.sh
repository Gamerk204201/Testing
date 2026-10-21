#!/bin/bash
sed -i 's/dry_run: bool = False/dry_run: bool = True/' src/minestar_gallagher/configuration.py
echo "Dry-run ENABLED"
