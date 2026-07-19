# YGO-x-MTG

Yu-Gi-Oh! cards adapted as Magic: The Gathering cards and saved as Magic Set Editor projects.

## Source of truth

English card data lives in `MSE_projects/*.mse-set/`; English project documentation lives in `docs/`. Frozen French snapshots live in `MSE_projects/French/`, `docs/French/`, `rule_reviews/French/`, and `mse/French/` and are not authoritative.

## First-time setup

This repository does not commit machine-specific Magic Set Editor paths. After every fresh clone:

```bash
python setup_mse.py
```

Enter the root of your Magic Set Editor installation when prompted. The setup script works with paths from any operating system and verifies:

- the MSE executable;
- the `data` directory and every game, frame, and symbol-font package referenced by the checked-in `.mse-set` projects;
- the bundled Magic fonts required by those frames;
- this repository's `MSE_projects` directory.

A successful run creates a gitignored `.env` containing `MSE_ROOT`, `MSE_EXECUTABLE`, `MSE_CLI`, `MSE_DATA_DIR`, `MSE_FONTS_DIR`, and `MSE_PROJECTS_DIR`. Run the setup again if either the repository or MSE installation is moved.

For unattended setup, pass the installation directly:

```bash
python setup_mse.py --mse-root "/path/to/Magic Set Editor"
```

After setup, run `mse_project_menu.pyw` to browse and open the projects with the configured MSE executable.

## MSE launch diagnostics

The GUI launcher writes configuration and process-launch events (`config.mse.*` and `spawn.mse.*`) to the gitignored `.mse_launcher.log` file in the repository root. Check that file when MSE does not open or exits unexpectedly.
