import asyncio
import requests
import json
import base64
import discord
import interactions
import time

default_color = 0x30b521

def retrieve_mc_skin(username):
    api_url = f"https://api.mojang.com/users/profiles/minecraft/{username}"
    response = requests.get(api_url)
    if response.status_code == 200:
        profile = response.json()
        uuid = profile['id']
        api_url2 = f"https://sessionserver.mojang.com/session/minecraft/profile/{uuid}"
        response = requests.get(api_url2)
        profile_data = response.json()
        uuid = profile_data['id']
        name = profile_data['name']
        skin_url = f"https://mc-heads.net/body/{uuid}/right"
        decoded_bytes = base64.b64decode(profile_data['properties'][0]['value'])
        decoded = json.loads(decoded_bytes.decode('utf-8'))
        download_url = decoded['textures']['SKIN']['url']
        try:
            model = decoded['textures']['SKIN']['metadata']['model']
        except:
            model = ""
        try:
            cape = decoded['textures']['CAPE']['url']
            if cape == "http://textures.minecraft.net/texture/2340c0e03dd24a11b15a8b33c2a7e9e32abb2051b2481d0ba7defd635ca7a933":
                cape = "Migrator Cape <:capeMigrator:1204004538567233536>"
            if cape == "http://textures.minecraft.net/texture/9e507afc56359978a3eb3e32367042b853cddd0995d17d0da995662913fb00f7":
                cape = "Mojang Studios Cape <:capeMojangStudios:1204004559115259934>"
            if cape == "http://textures.minecraft.net/texture/f9a76537647989f9a0b6d001e320dac591c359e9e61a31f4ce11c88f207f0ad4":
                cape = "Vanilla Cape <:capeVanilla:1204004578316521483>"
            if cape == "http://textures.minecraft.net/texture/17912790ff164b93196f08ba71d0e62129304776d0f347334f8a6eae509f8a56":
                cape = "Realm Mapmaker Cape <:capeRealmsmapmaker:1204004564240572476>"
            if cape == "http://textures.minecraft.net/texture/953cac8b779fe41383e675ee2b86071a71658f2180f56fbce8aa315ea70e2ed6":
                cape = "Minecon 2011 Cape <:capeMinecon2011:1204004542916599818>"
            if cape == "http://textures.minecraft.net/texture/a2e8d97ec79100e90a75d369d1b3ba81273c4f82bc1b737e934eed4a854be1b6":
                cape = "Minecon 2012 Cape <:capeMinecon2012:1204004545987092501>"
            if cape == "http://textures.minecraft.net/texture/153b1a0dfcbae953cdeb6f2c2bf6bf79943239b1372780da44bcbb29273131da":
                cape = "Minecon 2013 Cape <:capeMinecon2013:1204004547870068756>"
            if cape == "http://textures.minecraft.net/texture/b0cc08840700447322d953a02b965f1d65a13a603bf64b17c803c21446fe1635":
                cape = "Minecon 2015 Cape <:capeMinecon2015:1204004550386655242>"
            if cape == "http://textures.minecraft.net/texture/e7dfea16dc83c97df01a12fabbd1216359c0cd0ea42f9999b6e97c584963e980":
                cape = "Minecon 2016 Cape <:capeMinecon2016:1204004552370814976>"
            if cape == "http://textures.minecraft.net/texture/8f120319222a9f4a104e2f5cb97b2cda93199a2ee9e1585cb8d09d6f687cb761":
                cape = "Mojang Classic Cape <:capeMojangclassic:1204004556959387668>"
            if cape == "http://textures.minecraft.net/texture/5786fe99be377dfb6858859f926c4dbc995751e91cee373468c5fbf4865e7151":
                cape = "Mojang Cape <:capeMojang:1204004555361222676>"
            if cape == "http://textures.minecraft.net/texture/ae677f7d98ac70a533713518416df4452fe5700365c09cf45d0d156ea9396551":
                cape = "Mojira Moderator Cape <:capeMojiramoderator:1204004747120738364>"
            if cape == "http://textures.minecraft.net/texture/1bf91499701404e21bd46b0191d63239a4ef76ebde88d27e4d430ac211df681e":
                cape = "Translator Cape <:capeTranslator:1204004573551796235>"
            if cape == "http://textures.minecraft.net/texture/ca35c56efe71ed290385f4ab5346a1826b546a54d519e6a3ff01efa01acce81":
                cape = "Cobalt Cape <:capeCobalt:1204004534121406515>"
            if cape == "http://textures.minecraft.net/texture/3efadf6510961830f9fcc077f19b4daf286d502b5f5aafbd807c7bbffcaca245":
                cape = "Scrolls Champion Cape <:capeScrolls:1204007001445634048>"
            if cape == "http://textures.minecraft.net/texture/2262fb1d24912209490586ecae98aca8500df3eff91f2a07da37ee524e7e3cb6":
                cape = "Chinese Translator Cape <:capeTranslator:1204004573551796235>"
            if cape == "http://textures.minecraft.net/texture/ca29f5dd9e94fb1748203b92e36b66fda80750c87ebc18d6eafdb0e28cc1d05f":
                cape = "Cheapsh0t's Cape <:capeTranslator:1204004573551796235>"
            if cape == "http://textures.minecraft.net/texture/5048ea61566353397247d2b7d946034de926b997d5e66c86483dfb1e031aee95":
                cape = "Turtle Cape <:capeTurtle:1204004575552479242>"
            if cape == "http://textures.minecraft.net/texture/2056f2eebd759cce93460907186ef44e9192954ae12b227d817eb4b55627a7fc":
                cape = "Birthday Cape <:capeBirthday:1204004529364795412>"
            if cape == "http://textures.minecraft.net/texture/d8f8d13a1adf9636a16c31d47f3ecc9bb8d8533108aa5ad2a01b13b1a0c55eac":
                cape = "Prismarine Cape <:capePrismarine:1204004561828843570>"
            if cape == "http://textures.minecraft.net/texture/70efffaf86fe5bc089608d3cb297d3e276b9eb7a8f9f2fe6659c23a2d8b18edf":
                cape = "Millionth Customer Cape <:capeMillionth:1204004540890746921>"
            if cape == "http://textures.minecraft.net/texture/bcfbe84c6542a4a5c213c1cacf8979b5e913dcb4ad783a8b80e3c4a7d5c8bdac":
                cape = "dannyBstyle's Cape <:capeDB:1204004536717545492>"
            if cape == "http://textures.minecraft.net/texture/23ec737f18bfe4b547c95935fc297dd767bb84ee55bfd855144d279ac9bfd9fe":
                cape = "JulianClark's Cape <:capeSnowman:1204004715596226601>"
            if cape == "http://textures.minecraft.net/texture/2e002d5e1758e79ba51d08d92a0f3a95119f2f435ae7704916507b6c565a7da8":
                cape = "MrMessiah's Cape <:capeSpade:1204004570896928869>"
            if cape == "http://textures.minecraft.net/texture/afd553b39358a24edfe3b8a9a939fa5fa4faa4d9a9c3d6af8eafb377fa05c2bb":
                cape = "Cherry Blossom Cape <:capeCherryBlossom:1204004532271714354>"
        except :
            cape = ""

        return [skin_url, uuid, name, download_url, cape, model]
    elif response.status_code == 404:
        print(f"[PNH Logs] Username '{username}' was not found.")
    else:
        # Handle other response codes
        print(f"[PNH Logs] Request error: {response.status_code}")
        
        
        
def embed_builder_mc(retrieved_info, interaction_user):
        skin_url = retrieved_info[0]
        uuid = retrieved_info[1]
        name = retrieved_info[2]
        download_url = retrieved_info[3]
        cape = retrieved_info[4]
        model = retrieved_info[5]
        
        cape_url = f"http://s.optifine.net/capes/{name}.png"
        response_of = requests.head(cape_url)
        if response_of.status_code == 200:
            cape_of = cape_url
        else :
            cape_of = ""
        
        if model != "":
            skin_format = "Slim"
        else:
            skin_format = "Wide"
        embed = discord.Embed(
            title=f"{name}'s Minecraft Profile",
            description="",
            color=default_color
        )
        embed.add_field(name="", value=f"**UUID**: {uuid}", inline=False)
        embed.add_field(name="", value=f"**Skin Format**: {skin_format}", inline=False)
        if cape != "":
            embed.add_field(name="**Currently Worn Cape**", value=f"{cape}", inline=False)

        if cape_of != "":
            is_capeof = True
            embed.add_field(name="Optifine Cape", value="")
            embed.set_image(url=cape_url)
        else:
            is_capeof = False
        embed.set_thumbnail(url="https://media.discordapp.net/attachments/1178067146908123267/1178373863843823746/HC.png?ex=65b682ae&is=65a40dae&hm=ad9b8f9a149e201c4302720cf864084dccabdb54214f6ff98a5cae42c7c30721&=&format=webp&quality=lossless&width=603&height=603")
        embed.set_footer(text=f"Command requested by {interaction_user} at {time.ctime()}")   
        embed.set_thumbnail(url=skin_url)
        return embed, is_capeof