# RoleInvite

This is the RoleInvite cog for Red. This is a quite different autorole cog, which works depending on the invite the member used to join!

You can set the autorole system so when a member joins with the invite x, he gets the role y. You can also set it so when someone joins with an unlinked invite, he gets another role. There's even a setting to always give a role to new members regardless of the invite used.

There is a detailed documentation, covering all commands in details, please read this if you want to know how commands works in details: https://laggron.red/roleinvite.html

The cog is built with an API, allowing you to use RoleInvite without a context on Discord, perfect for your pre-made eval commands or any scheduler. You can get more details about this on the [API reference](https://laggron.red/roleinvite-api.html).

## Installation and quick start

`[p]` is your prefix.

1.  Install the repo if it's not already done.
    ```
    [p]repo add Laggrons-Dumb-Cogs https://github.com/retke/Laggrons-Dumb-Cogs v3
    ```

2.  Install and load RoleInvite
    ```py
    [p]cog install Laggrons-Dumb-Cogs roleinvite
    # Type "I agree" if requested
    # wait for your bot to install the cog
    [p]load roleinvite
    ```

RoleInvite is now installed! You can create a link with the command `[p]roleinviteset`.

## Discord server

If you need support, have bugs to report or suggestions to bring, please join my Discord server and tell me, `El Laggron#0260`, about it!

[![Discord server](https://discordapp.com/api/guilds/363008468602454017/embed.png?style=banner3)](https://discord.gg/AVzjfpR)

## [Laggron's Dumb Cogs](https://github.com/retke/Laggrons-Dumb-Cogs)

![Artwork](https://github.com/retke/Laggrons-Dumb-Cogs/blob/master/.github/RESSOURCES/BANNERS/Base_banner.png)

This cog is part of the Laggron's Dumb Cogs repository, where utility cogs for managing your server are made!
If you like this cog, you should check the other cogs from [the repository](https://github.com/retke/Laggrons-Dumb-Cogs)!

You can also support me on Patreon and get exclusive rewards!

<img src="https://c5.patreon.com/external/logo/become_a_patron_button@2x.png" alt="Become a Patreon" width="180"/>

<!-- Replace link by cogs.red link -->

## Contribute

If you're reading this from Github and want to contribute or just understand the source code, I'm gonna stop you right there. Indeed, the cog is a bit complex so let me explain a bit how each file work before source diving.

- `__init__.py` The first file invoked when loading the cog. Nothing useful here.
- `api.py` The most important functions are there, such as creating a link, remove one or update the stored invites count. Those functions don't need a context to be invoked.
- `errors.py` The custom errors raised by `api.py` are in this file. There are only empty classes inherited from `Exception`.
- `roleinvite.py` The file of the cog. All commands are stored there.

With that said, source diving should be easier.
