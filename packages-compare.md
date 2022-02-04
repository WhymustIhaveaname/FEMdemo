# Compare Python FEM packages

## Mesh packages

* [meshio](https://github.com/nschloe/meshio) __recommanded__
    * used in reading and exporting meshes
    * well functioned, no bug so far
    * need more documents
    * cannot export in ascii (maybe it can, but there is no docs)

* [meshpy](https://github.com/inducer/meshpy) __not recommanded__
    * have to compile and install manually
    * the only example does not work
    * almost no documents, no figures
    * cannot be cleanly uninstalled

* [gmsh](https://gmsh.info/) __not recommanded__
    * easy to install (`apt install gmsh`)
    * poorly-written docs
        * no explaination of its own `.geo` grammar.
        (I know there are some examples [here](https://gmsh.info/doc/texinfo/gmsh.pdf).
        However, there are only examples but no explanation of grammar.
        Let alone these examples are incomprehensible.
        Examples are used to supplement grammars, not replace grammars!)
        * no explanation of its command line parameters.
    * buggy GUI
    * no one is using it, so there is no instruction except for the shabby document.
    * it wasted me at least 8 hours. Please keep away from `gmsh`.

* [pygmsh](https://github.com/nschloe/pygmsh) __not recommanded__
    * easy to install
    * some examples and figures
    * it is a wrap of `gmsh` but `gmsh` itself is not recommended
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
