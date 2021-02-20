with import <nixpkgs> {};
let
  rtx-python = python3.withPackages (python-packages: with python-packages; [
    aiohttp telethon toml
  ]);
in
stdenv.mkDerivation {
    name = "rtxgobrrr-environment";
    buildInputs = [ rtx-python ];
}