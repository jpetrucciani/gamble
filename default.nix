{ jacobi ? import
    (fetchTarball {
      name = "jpetrucciani-2023-01-23";
      url = "https://github.com/jpetrucciani/nix/archive/017005177512bb0374f93c9ad7ede35d807f0c3b.tar.gz";
      sha256 = "0b1bp01rz748i9iq3f28ny2xa06wglh00qm1zb0m8v41c0w19ahv";
    })
    { }
}:
let
  name = "gamble";
  tools = with jacobi; {
    cli = [
      jq
      nixpkgs-fmt
    ];
    python = [
      ruff
      (python310.withPackages (p: with p; [
        # dev
        colorama
        pytest
        pytest-cov
        setuptools
        tox
      ]))
    ];
    scripts = [
      (writeShellScriptBin "test_actions" ''
        export DOCKER_HOST=$(${jacobi.docker-client}/bin/docker context inspect --format '{{.Endpoints.docker.Host}}')
        ${jacobi.act}/bin/act --container-architecture linux/amd64 -r --rm
      '')
      (writeShellScriptBin "prospector" ''
        ${prospector}/bin/prospector $@
      '')
    ];
  };

  env = let paths = jacobi._toolset tools; in
    jacobi.buildEnv {
      inherit name;
      buildInputs = paths;
      paths = paths;
    };
in
env
