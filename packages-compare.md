# Compare Python FEM packages

## Mesh packages

* [meshpy](https://github.com/inducer/meshpy) __not recommanded__
    * have to compile and install manually
    * the only example does not work
    * almost no documents, no figures
    * cannot be cleanly uninstalled

* [pygmsh](https://github.com/nschloe/pygmsh) __seems good__
    * easy to install
    * some examples and figures
    * too few function: no quadrilateral mesh

## FEM packages

* Votes from https://www.researchgate.net/post/What-is-the-best-finite-element-library-for-Python-programming-language

    Package|Votes
    -------|-----
    SfePy  |+++
    PolyFem|+-+
    SciPy  |+
    FElupe |+

* [SfePy](https://sfepy.org/doc-devel/index.html) __very recommanded__
    * well documented, lots of examples and figures
    * not easy to install, but it works and works very well
    * author replies issues very fast
