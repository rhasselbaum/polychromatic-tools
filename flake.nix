{
  # Nix Flake for this package
  description = "polychromatic-restore package Flake";

  inputs = {
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils, ... }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { inherit system; };
        pname = "polychromatic-restore";
      in
      {
        packages = {
          polychromatic-restore = pkgs.stdenv.mkDerivation {
            inherit pname;
            version = "git";

            src = ./.;
            buildInputs = with pkgs; [
              (python3.withPackages (p: with p; [ dbus-python pygobject3 ]))
              makeWrapper
              wrapGAppsNoGuiHook
              polychromatic
            ];

            installPhase = ''
              mkdir -p $out/bin $out/effects
              cp $src/polychromatic-restore.py $out/bin
              cp $src/default-effect.json $out/effects
              chmod +x $out/bin/polychromatic-restore.py
              makeWrapper $out/bin/polychromatic-restore.py $out/bin/polychromatic-restore --add-flags $out/effects/default-effect.json \
                --set PATH ${pkgs.polychromatic}/bin
            '';
          };
        };

        defaultPackage = self.packages.${system}.polychromatic-restore;
      }
    );
  }