{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = with pkgs; [
    black
    python313Packages.pip
    python313Packages.pylint
  ];
}