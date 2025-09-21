# Recommended file structure for a Python video game project

project-name/
├── README.md                  # overview, run & build instructions
├── LICENSE
├── pyproject.toml / setup.cfg # build / packaging config
├── requirements.txt / Pipfile
├── .gitignore
├── docs/                      # design docs, architecture, art specs
├── assets/                    # all game assets (kept out of VCS large files)
│   ├── images/
│   ├── sprites/
│   ├── audio/
│   └── fonts/
├── src/ or game_package/      # application package (importable)
│   ├── __init__.py
│   ├── main.py                # entry point
│   ├── core/                  # engine, game loop, scene manager
│   ├── entities/              # player, enemies, NPCs
│   ├── scenes/                # levels, menus, UI screens
│   ├── systems/               # input, physics, rendering, audio
│   └── utils/                 # helpers, resource loaders
├── data/                      # runtime data, level files, saved presets
├── tests/                     # unit and integration tests
├── examples/                  # small demos or usage examples
├── tools/                     # build/deploy scripts, asset pipeline
└── build/ or dist/            # generated build artifacts

Guidelines:
- Keep code under a package (src/ or package name) so imports are consistent.
- Separate assets from code; use an assets loader to reference files by logical paths.
- Add tests covering game logic (avoid relying on rendering in unit tests).
- Use pyproject.toml/requirements.txt and a lock file for reproducible installs.
- Keep large binary assets out of Git (use LFS or an external asset store).
- Provide clear run/build steps in README and CI scripts for automated builds.