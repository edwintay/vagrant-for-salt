{
  sources ? import ./nix/sources.nix
}:
let
  pkgs = import sources.nixpkgs {};
in
pkgs.mkShell {
  nativeBuildInputs = [
    pkgs.bashInteractive
  ];
}
