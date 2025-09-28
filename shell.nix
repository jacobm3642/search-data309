{ pkgs ? import <nixpkgs> {} }:

with pkgs;

mkShell {
  buildInputs =  [
    (python311.withPackages (ps: with ps; [
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
      pytorch
      sentence-transformers
    ]))

    protobuf
    grpc-gateway
  ];

}
