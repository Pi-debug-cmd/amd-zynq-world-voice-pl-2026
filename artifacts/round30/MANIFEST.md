# Round30 FPGA Artifacts

Release tag: `round30-submission-20261101`
Source project: `Pi-debug-cmd/2026_FPGA`, deployed source revision `a8f6f8f32b159eaea277354118220c633f31fbc2`, task `PL-20261027-01`.
Implementation evidence: [Round18 integration report](../../report/world_minphase_integration_round18_20261029.md) and [Round30 persistent boot report](../../report/world_minphase_persistent_boot_round30_20261030.md).

The archive includes these files:

| File | Bytes | SHA-256 | Purpose |
| --- | ---: | --- | --- |
| `world_minphase_swap.bin.gz` | 536768 | `6a7fec9987d31c5f803b79b1bb8e115dca9fda0dfc278b8f462d60562b628d98` | Byte-swapped FPGA Manager boot payload; matches the Round30 deployed candidate hash |
| `zynq_wrapper.bit` | 4045767 | `e2131f0c4306f891e05f9a5aa9cee33077ad794b3ab2a2a53e0eac9d67b8cee3` | Vivado 2026.1 routed bitstream |
| `zynq.hwh` | 667289 | `d510e66789afa9b08fbb27474ce91e01bf231485c08dc03d68db875c3b2fa7ff` | Block-design hardware handoff metadata |
| `timing_summary.txt` | 56255 | `db35e15e23fb0d8e233a0c7ed7b0ea33775e261d65a4cd1de857144271a29471` | Routed timing report |
| `utilization.txt` | 13464 | `604f4c0671e9d8fd4915b51820807f7493a4edfcf5001ddc2ccc42d6d7cc1282` | Implemented resource report |
| `drc.txt` | 150347 | `6b65a4b0b80d45657bb7d6db9b2ac39be67310f6beb22a5901d8b0e98ba37bae` | DRC report |
| `route_status.txt` | 651 | `ea5fbbf95224e790ebffe022e5a1c082abbf847d4f04dbd106d707ea0d801403` | Route completion summary |
| `bus_skew.txt` | 75314 | `4179efc918c1699096d6f84a3cf381ded90f66d16cde1da75355ba35d14cc8c4` | Routed bus-skew report |
| `world_minphase_bit_manifest.json` | 569 | `8aa5ef115d09acb5c693bd6817a1ebe477b7894baf6ef0511c5c742a659f714e` | Machine-readable payload metadata and raw/swap hashes |

The payload, `.bit`, and report hashes are recorded in Round18/Round30 evidence. The `.hwh` and JSON manifest hashes are computed from the preserved Vivado export and packaged manifest. The release archive itself is the transfer unit.

## Verify

Download the Release archive from `https://github.com/Pi-debug-cmd/amd-zynq-world-voice-pl-2026/releases/tag/round30-submission-20261101`, extract it, then run:

```powershell
Get-FileHash -Algorithm SHA256 .\artifacts\round30\world_minphase_swap.bin.gz
Get-FileHash -Algorithm SHA256 .\artifacts\round30\zynq_wrapper.bit
Get-FileHash -Algorithm SHA256 .\artifacts\round30\zynq.hwh
```

Compare results with the table above. The `.bit` and `.hwh` are the Round18 full-system implementation used by this candidate. Round30 changed persistent deployment/startup behavior and reused the same hardware image; the deployed compressed payload hash confirms that identity.

## Limits

No `.xsa`, complete vendor audio project, PetaLinux image, Linux kernel module, or runtime executable is in this archive. It is a programming and handoff artifact set, not a clean-room rebuild package. External audio I/O delays remain incomplete in the recorded routed timing constraints. Review the checklist before treating this as final contest acceptance.
