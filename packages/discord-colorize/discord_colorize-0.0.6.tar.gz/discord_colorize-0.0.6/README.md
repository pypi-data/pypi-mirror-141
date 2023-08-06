Colored Codeblocks - Discord
---------------------------
Colored Codeblocks for Discord Bots using ANSI Escape Sequences.

You can do `help(discord_colorize.Colors)` to see all the available colors along with a detailed docstring on how to use the package.
  
Usage -
```python
    import discord_colorize
    colors = discord_colorize.Colors()
    data = f"""
    ```ansi
    {colors.colorize('Hello World!', fg='green', bg='indigo', bold=True, underline=True)}
    ```
    """
    help(discord_colorize.Colors)
```

[Extra Information](https://gist.github.com/kkrypt0nn/a02506f3712ff2d1c8ca7c9e0aed7c06)

Created by TheOnlyWayUp#1231 - https://github.com/TheOnlyWayUp/
