from sys import stderr, argv


args: str = '\t- ' + ( '\n\t- '.join(argv) )


print(f'Arguments passed:\n{args}')
print('Compilation done!', file=stderr)
