Python IL2CPP protocol extraction for Magia Exedra
================================================

`recovery.restore(run)` reconstructs the recognized ARM64 protected ELF without
executing loader code. `protocol.generate(library, metadata, output)` reads
IL2CPP metadata directly and emits the four Pydantic protocol model modules.
Neither API invokes commands, an emulator, .NET, or a DummyDll generator.

The metadata record layouts and compressed constant conventions in `metadata.py`
are adapted from Il2CppDumper 6.7.46 (Perfare, MIT):
https://github.com/Perfare/Il2CppDumper
See LICENSE.Il2CppDumper for the retained copyright and license.

The protocol selection/type mapping follows the user's existing
MagiaExedra/ProtocolGen source. The packet decoder and ELF recovery implement the
loader format observed in the user's 3.16.1 and 3.19.1 samples. The loader hash
check deliberately rejects changed implementations rather than guessing.

This is the subset needed for protocol generation, not a complete replacement
for Il2CppDumper's DummyDll or disassembler export features.
