# LocalWeave Infrastructure Plan

LocalWeave should be designed as if home internet and power can fail.

The first machine should not be a premature tower purchase. Use the available laptop or current Mac as Node 0 until real bottlenecks are known.

## Compute Tiers

| Budget | Target | Specs to prioritize |
|---|---|---|
| 200-350 USD | Tiny 24/7 server | Used mini PC, 6-8 CPU cores, 32 GB RAM, 1 TB NVMe, 1/2.5GbE |
| 400-700 USD | Serious LocalWeave core | Ryzen 7/i7 class, 32-64 GB RAM, 2 TB NVMe, 2.5GbE, storage expansion |
| 800-1300 USD | AI-capable tower | 8+ CPU cores, 64 GB RAM, 2 TB NVMe plus expansion, NVIDIA GPU with ideally 12-16+ GB VRAM |
| 1500-2500+ USD | Local AI workstation | 64-128 GB RAM, 24+ GB VRAM, multiple NVMe slots, 2.5/10GbE |

For non-GPU tiers, prioritize RAM, storage, network reliability, low idle power, and uptime.

For AI tiers, VRAM is the key constraint. A less glamorous GPU with more usable VRAM can be more valuable than a faster GPU that cannot load the desired models.

## Tower Build Criteria

If buying parts instead of a full build, prefer:

- 4 DIMM slots if possible.
- 2+ M.2 slots.
- Several SATA connections.
- Full x16 GPU slot.
- Extra PCIe slot.
- Decent PSU with GPU headroom.
- Good airflow and dust management.
- Case space for a physically large future GPU.
- 2.5GbE minimum where practical.

## Power Redundancy

UPS is useful for graceful shutdown and short outages, but the network path matters.

Problem:

```text
Apartment router has power
  but
building ONT / switch / distribution equipment loses power
  so
main internet may still fail
```

Design implication:

- Do not assume powering only the apartment router preserves internet.
- Avoid depending on unsafe or administratively difficult building-infrastructure power changes.
- Use UPS for local compute, local router, and storage protection.
- Prefer graceful shutdown and data safety over trying to survive every long outage.

## Network Redundancy

LocalWeave should support independent fallback connectivity.

Candidates:

- One 4G/5G router as independent backup.
- Two affordable cellular routers for better room coverage or provider diversity.
- Separate cellular provider from the main building ISP where cost allows.
- Smaller private provider only if reliability risk is acceptable.

Network design should distinguish:

- Primary home/building internet.
- Backup cellular internet.
- Offline mode with no internet.

Offline mode should still support:

- Markdown vault search.
- Local notes.
- Local indexes.
- Offline knowledge library.
- Local model tasks if hardware allows.
- Drafting and queued actions.

## 24/7 Runtime Posture

Eventual services:

- Local API.
- Worker queue.
- Indexer.
- Audit log writer.
- Permission service.
- Optional UI.
- Optional voice service.

Initial runtime should stay simple. Avoid always-on services until the text MVP proves value and safety.
