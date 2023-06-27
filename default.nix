{ pkgs ? import
    (fetchTarball {
      name = "jpetrucciani-2023-06-26";
      url = "https://github.com/jpetrucciani/nix/archive/cfbb79b2245dcc3d06f6bd80892d346363a8b9e5.tar.gz";
      sha256 = "15wa55yhmv3hfsx29zabg6q5sqy9y3xrxy7w0dlrzfpkpy6xk56n";
    })
    { }
}:
let
  name = "gamble";

  tools = with pkgs; {
    cli = [
      nixpkgs-fmt
    ];
    python = [
      ruff
      (python311.withPackages (p: with p; [
        colorama
        pytest
        pytest-cov
        setuptools
        tox
      ]))
    ];
    scripts = [
      (writeShellScriptBin "test_actions" ''
        export DOCKER_HOST=$(${pkgs.docker-client}/bin/docker context inspect --format '{{.Endpoints.docker.Host}}')
        ${pkgs.act}/bin/act --container-architecture linux/amd64 -r --rm
      '')
    ];
  };

  paths = pkgs.lib.flatten [ (builtins.attrValues tools) ];
in
pkgs.buildEnv {
  inherit name paths;
  buildInputs = paths;
}
