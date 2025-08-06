  { pkgs ? import <nixpkgs> {} }:

  pkgs.mkShell {
      buildInputs = with pkgs; [
        python3
        (python3.withPackages(ps: with ps; [ pandas requests nltk flask pinecone]))
      ];
  }
