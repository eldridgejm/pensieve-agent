with import <nixpkgs> {};

mkShell {
  venvDir = "venv";
  buildInputs = with python38Packages; [
    venvShellHook
  ];
  postShellHook = ''
    pip install -e .
    pip install behave ipython black
    '';
}
