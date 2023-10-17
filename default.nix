{ pkgs ? import
    (fetchTarball {
      name = "jpetrucciani-2023-10-17";
      url = "https://github.com/jpetrucciani/nix/archive/d944b2ed0e17f5e8e12332d21d226038ccb77ccb.tar.gz";
      sha256 = "0dzcqs7614pd0z0n17d3y6n6w1snk0x54pj8m740w4657i538g7s";
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
