{ jacobi ? import
    (fetchTarball {
      name = "jpetrucciani-2023-01-23";
      url = "https://github.com/jpetrucciani/nix/archive/4d8e4081fd11f83219ee9e7c5c0d91c0f9f6eb0c.tar.gz";
      sha256 = "12jrlj8r42p7yavhrkn0q3rnfrg313h60ck8447c3zq7fi14kf4p";
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
