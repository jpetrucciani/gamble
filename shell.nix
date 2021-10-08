let
  nixpkgs = import
    (
      fetchTarball {
        name = "nixos-unstable-2021-08-31";
        url = "https://github.com/NixOS/nixpkgs/archive/cb021898fab2a19e75d4e10c10c1da69c4e9f331.tar.gz";
        sha256 = "1hxpp44bg1gwfzcd570wqfvd6am4vk52938zqcwy7mxwjmk6wbrh";
      }
    )
    { };
  mach-nix = import
    (builtins.fetchGit {
      url = "https://github.com/DavHau/mach-nix/";
      ref = "refs/tags/3.3.0";
    })
    {
      pkgs = nixpkgs;
      python = "python39";
    };
in
mach-nix.mkPythonShell {
  requirements = builtins.readFile ./requirements.dev.txt;
}
