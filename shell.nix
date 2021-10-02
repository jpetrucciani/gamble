let
  mach-nix = import
    (builtins.fetchGit {
      url = "https://github.com/DavHau/mach-nix/";
      ref = "refs/tags/3.3.0";
    })
    { python = "python3"; };
in
mach-nix.mkPythonShell {
  requirements = builtins.readFile ./requirements.dev.txt;
}
