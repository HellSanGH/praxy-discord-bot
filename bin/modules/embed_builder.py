import time

def embed_default_builder(interaction, embed):
    global default_embed_thumbnail
    global default_embed_displaytime
    if default_embed_thumbnail:
        embed.set_thumbnail(url=default_embed_thumbnail)
    if default_embed_displaytime:
        embed.set_footer(text=f"Command requested by {interaction.user} at {time.ctime()}")
    return embed
