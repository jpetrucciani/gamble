let
  nixpkgs = import
    (
      fetchTarball {
        name = "nixos-unstable-2021-12-31";
        url = "https://github.com/NixOS/nixpkgs/archive/ba4fa46ea1204a31fa57a23503182af799ec70ca.tar.gz";
        sha256 = "06x57dqlxn17r38f90gnnnmhklp2fcgm46vch2frzb1lc8aq1zz0";
      }
    )
    { };
  mach-nix = import
    (
      fetchTarball {
        name = "mach-nix-2021-12-31";
        url = "https://github.com/DavHau/mach-nix/archive/31b21203a1350bff7c541e9dfdd4e07f76d874be.tar.gz";
        sha256 = "0przsgmbbcnnqdff7n43zv5girix83ky4mjlxq7m2ksr3wyj2va2";
      }
    )
    {
      pkgs = nixpkgs;
      python = "python39";
    };
in
mach-nix.mkPythonShell {
  requirements = builtins.readFile ./requirements.dev.txt;
}
