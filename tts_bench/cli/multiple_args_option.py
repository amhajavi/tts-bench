import sys
import click

class MultipleArgsOption(click.Option):
    """A Click option that consumes all positional arguments until the next flag."""
    def __init__(self, *args, **kwargs):
        # Force multiple=True so Click expects a tuple/list of values
        kwargs["multiple"] = True
        super().__init__(*args, **kwargs)

    def handle_parse_result(self, ctx, opts, args):
        # Check if our option flag is present in the unparsed arguments
        for opt_name in self.opts:
            argv = sys.argv
            if opt_name in argv:
                # Find where our option is located
                idx = argv.index(opt_name)
                values = []
                # Look ahead and consume all items that do not start with a dash
                look_ahead = idx + 1
                while look_ahead < len(argv) and not argv[look_ahead].startswith("-"):
                    values.append(argv[look_ahead])
                    
                    look_ahead += 1
                
                # Remove the consumed values from the global args list
                # so Click doesn't treat them as positional arguments
                del args[idx + 1 : look_ahead]
                
                opts[self.name] = tuple(values)
                    
        return super().handle_parse_result(ctx, opts, args)