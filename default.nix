{ pkgs ? import
    (fetchTarball {
      name = "jpetrucciani-2024-08-04";
      url = "https://github.com/jpetrucciani/nix/archive/5d293e2449312b4fef796dcd0836bf6bc1fad684.tar.gz";
      sha256 = "0z8dyf6d9mdka8gq3zchyy5ywzz91bj18xzdjnm0gpwify0pk312";
    })
    { }
}:
let
  name = "gamble";

  python = (pkgs.poetry2nix.mkPoetryEnv {
    projectDir = ./.;
    python = pkgs.python311;
    overrides = pkgs.poetry2nix.overrides.withDefaults (final: prev: { });
    editablePackageSources = {
      "gamble" = ./gamble;
    };
    preferWheels = true;
  });

  tools = with pkgs; {
    cli = [
      nixpkgs-fmt
    ];
    python = [
      ruff
      poetry
      python
    ];
    scripts = pkgs.lib.attrsets.attrValues scripts;
  };

  scripts =
    let
      inherit (pkgs.writers) writeBashBin;
      repo = "$(${pkgs.git}/bin/git rev-parse --show-toplevel)";
    in
    {
      test_actions = writeBashBin "test_actions" ''
        export DOCKER_HOST=$(${pkgs.docker-client}/bin/docker context inspect --format '{{.Endpoints.docker.Host}}')
        ${pkgs.act}/bin/act --container-architecture linux/amd64 -r --rm
      '';
      _test = writeBashBin "_test" ''
        export PYTEST_RUNNING=1
        ${python}/bin/pytest ./tests \
          -s \
          --cov ${name} \
          --cov-report term \
          --cov-report html \
          --cov-report xml:coverage.xml \
          --junitxml=report.xml \
          "$@"
      '';
      docs = writeBashBin "docs" ''
        cd "${repo}/docs" || exit 1
        rm -rf ./build
        ${python}/bin/sphinx-build -M html source build
      '';
    };
  paths = pkgs.lib.flatten [ (builtins.attrValues tools) ];
  env = python.env.overrideAttrs (_: {
    buildInputs = paths;
  });
in
(env.overrideAttrs (_: {
  inherit name;
  NIXUP = "0.0.6";
})) // { inherit scripts; }

