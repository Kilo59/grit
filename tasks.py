import invoke


@invoke.task
def sort(ctx, path=".", check=False):
    """Sort module imports."""
    print("  sorting imports ...")
    args = ["isort", path, "--profile", "black"]
    if check:
        args.append("--check-only")
    ctx.run(" ".join(args))


@invoke.task
def fmt(ctx, path=".", sort_=True, check=False):
    """Run code formatter."""
    print("  formatting ...")

    args = ["black", path]
    if check:
        args.append("--check")
    ctx.run(" ".join(args))
    if sort_:
        sort(ctx, path, check)


@invoke.task
def lint(ctx, path="grit"):
    ctx.run(f"pylint {path}")


@invoke.task
def types(ctx, path="."):
    ctx.run(f"mypy {path}")
