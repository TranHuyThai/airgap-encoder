# airgap-encoder
Tool to transfer small files by custom 2D diagram encoder and decoder
┌─────────┬─────────────┬────────────────────┬──────────┐
│  Magic  │   Size      │       Data         │   CRC    │
│  4 bytes│  4 bytes    │      5 bytes       │  4 bytes │
├─────────┼─────────────┼────────────────────┼──────────┤
│  B2D1   │ 00 00 00 05 │ 48 65 6C 6C 6F     │ CRC value│
└─────────┴─────────────┴────────────────────┴──────────┘