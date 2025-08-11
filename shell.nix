{ pkgs ? import <nixpkgs> {} }:

with pkgs;

mkShell {
  buildInputs =  [
    (python3.withPackages (ps: with ps; [
      pip
      pandas
      requests
      nltk
      flask
      pinecone-client
      arxiv
      grpcio
      protobuf
      googleapis-common-protos
    ]))

    protobuf
    grpc-gateway
  ];

}
