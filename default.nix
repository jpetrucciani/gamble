{ pkgs ? import
    (fetchTarball {
      name = "jpetrucciani-2024-11-23";
      url = "https://github.com/jpetrucciani/nix/archive/9615d18512c3cadce8ae2ce4a92c5215296adaa9.tar.gz";
      sha256 = "1ibk7xkzwa8ljdm8360rg6nxnwzl06gbxlx93zzz0imv6nsf96kq";
    })
    { }
}:
let
  name = "gamble";

  python = pkgs.poetry-helpers.mkEnv {
    projectDir = ./.;
    python = pkgs.python312;
    editablePackageSources."gamble" = ./gamble;
  };

  tools = with pkgs; {
    cli = [
      nixpkgs-fmt
    ];
    python = [
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
  NIXUP = "0.0.8";
})) // { inherit scripts; }

