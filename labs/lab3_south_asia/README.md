# Lab 3: Mapping IT-BPO Exports Across Indian States

## Overview

This lab maps the spatial distribution of India's IT and Business Process Outsourcing (BPO) activity at the state level, connecting Chapter 8 to concentration indices and comparative services-versus-manufacturing patterns.

## Core Method

Location Quotients, Herfindahl–Hirschman Index, and Gini coefficients for state-level IT-sector concentration.

## Primary Datasets

| Dataset | Source | Access |
|---|---|---|
| India KLEMS / IT-sector value added | KLEMS India | Public / lab extracts |
| State-level services exports | RBI / STPI | Public reports (acquisition pending) |
| Bangladesh garment comparison | BGMEA / trade extracts | Public |

## Implementation Status

- [x] `code/lab3_concentration_scaffold.py` — LQ, HHI, Gini with synthetic and real-panel modes
- [x] `code/prepare_lab3_inputs.py` — canonical panel mapping
- [x] `code/concentration_trajectory_plotter.py` — concentration path plots
- [x] `code/run_real_south_asia_specs.py` — real-spec runner
- [ ] `code/fetch_rbi_services.py` — RBI acquisition
- [ ] Smile-curve city-tier analysis promised in the chapter exercises
- [x] Smoke tests for concentration scaffold

## Evidence Labels

- `--run-smoke-test` outputs are **synthetic demonstrations**.
- Real-panel runs are **author calculations** from mapped KLEMS/IT extracts; they are not STPI zone-level export maps until RBI/STPI acquisition is complete.

## Build Checklist

1. [x] Concentration indices on a canonical state panel.
2. [~] Real KLEMS/IT mapping and specs.
3. [ ] RBI/STPI export acquisition and choropleth mapping.
4. [ ] Services smile-curve exercise.
5. [ ] India–Bangladesh comparative concentration deliverable with provenance metadata.
