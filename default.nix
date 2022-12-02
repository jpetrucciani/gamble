{ jacobi ? import
    (fetchTarball {
      name = "jacobi-2022-12-01";
      url = "https://nix.cobi.dev/x/15e5cfd7927420eddc8d822e2dc0ee32908c850b";
      sha256 = "139k9dnqb5k1n7r1i6hk7vfiy9nmmla4hdvczi14sa4lv7grg7aq";
    })
    { }
}:
let
  inherit (jacobi.hax) ifIsLinux ifIsDarwin;

  name = "gamble";
  tools = with jacobi; {
    cli = [
      jq
      nixpkgs-fmt
    ];
    python = [
      (python310.withPackages (p: with p; [
        requests

        # dev
        colorama
        pytest
        pytest-cov
        setuptools
        tox
        types-requests
      ]))
    ];
    scripts = [
      (writeShellScriptBin "test_actions" ''
        ${jacobi.act}/bin/act --artifact-server-path ./.cache/ -r --rm
      '')
      (writeShellScriptBin "prospector" ''
        ${prospector}/bin/prospector $@
      '')
    ];
  };

  env = jacobi.enviro {
    inherit name tools;
  };
in
env
