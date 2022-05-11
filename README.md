EndC
-
A compiled/interpreted esoteric language with nothing to do with C
End C was designed to be hard to code in, it achieves that by trashing everything knowledge you might have from other languages.

NOTE: Not everything in here is completed! this is heavily WIP!

### Hello World in End C
```endc
DCLAR SUBROUTIN main{StRiNg() argv______} <- InTgR [
     DCLAR CONSTANT StRiNg txt_______ = *hello world!*/
     CALL printto{ STDOUT. txt_______ }/
     GIV BACK 0/
]
```

Characteristics
-
- Static typing
- Templates
- Inline assembly
- Interactive interpreter
- Configurable compiler
- Supports multiple compilation targets
- Self-hosting
- Runtime code compilation via interpreter

Language Backends
-
- [Interpreter](src/backend/interpreter)
- [LLVM](https://llvm.org)
- [WebAssembly](https://wasmer.io)
- [Python Virtual Machine](https://www.python.org)
- [Java Virtual Machine](https://adoptium.net)
- [Neko VM](https://nekovm.org)
- [HashLink](https://hashlink.haxe.org)
- JavaScript
- [.NET](https://www.mono-project.com)