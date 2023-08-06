import discord, requests, json, os

def most_item(data):
    return max(data, key=data.count)

class Disrider:
    def __init__(self, api_key):
        self.api_key = api_key

    def character(self, nickname):
        api_key = self.api_key

        url = f"https://api.nexon.co.kr/kart/v1.0/users/nickname/{nickname}"
        user_res = requests.get(url, headers={'Authorization': api_key})
        if user_res.status_code == 200:
            user_id = json.loads(user_res.text)["accessId"]

            url = f"https://api.nexon.co.kr/kart/v1.0/users/{user_id}/matches?start_date=&end_date= &offset=0&limit=1&match_types="
            match_res = requests.get(url, headers={'Authorization': api_key})

            if match_res.status_code == 200:
                with open("metadata/character.json", "r", encoding="utf8") as char:
                    character_json = json.load(char)

                match_data = json.loads(match_res.text)["matches"][0]["matches"]
                for match in match_data:
                    for char in character_json:
                        if char['id'] == match['character']:
                            img_list = os.listdir("metadata/character")
                            for img in img_list:
                                if img == f"{char['id']}.png":
                                    file = discord.File(f"metadata/character/{char['id']}.png", filename=f"{char['id']}.png")

                                    return {
                                            "characterName": char['name'],
                                            "locateID": f"{char['id']}.png",
                                            "file": file
                                            }

            else:
                raise Exception("Exception: 유저 데이터를 불러오는데에 실패했습니다.")

        else:
            raise Exception("NotFoundUser: 존재하지 않는 카트라이더 라이더명입니다.")

    def level(self, nickname):
        api_key = self.api_key

        url = f"https://api.nexon.co.kr/kart/v1.0/users/nickname/{nickname}"
        user_res = requests.get(url, headers={'Authorization': api_key})
        if user_res.status_code == 200:
            return json.loads(user_res.text)["level"]

        else:
            raise Exception("NotFoundUser: 존재하지 않는 카트라이더 라이더명입니다.")

    async def default_info(self, ctx, nickname, embed_color):
        api_key = self.api_key

        with open("metadata/character.json", "r", encoding="utf8") as char:
            character_json = json.load(char)

        with open("metadata/track.json", "r", encoding="utf8") as track:
            track_json = json.load(track)

        url = f"https://api.nexon.co.kr/kart/v1.0/users/nickname/{nickname}"
        user_res = requests.get(url, headers={'Authorization': api_key})
        if user_res.status_code == 200:
            user_id, name, level = json.loads(user_res.text)["accessId"], json.loads(user_res.text)["name"], json.loads(user_res.text)["level"]

            url = f"https://api.nexon.co.kr/kart/v1.0/users/{user_id}/matches?start_date=&end_date= &offset=0&limit=200&match_types="
            match_res = requests.get(url, headers={'Authorization': api_key})

            if match_res.status_code == 200:
                embed = discord.Embed(title=f"[ {name} ] 님의 카트라이더 유저 정보", description=f"**{level} LEVEL**", color=embed_color)

                match_data = json.loads(match_res.text)["matches"][0]["matches"]

                character = []
                track = []

                win = 0
                lose = 0

                for match in match_data:
                    character.append(match["character"])
                    track.append(match["trackId"])

                    if match["matchResult"] == '1':
                        win += 1

                    else:
                        lose += 1

                for char in character_json:
                    if char["id"] == most_item(character):
                        embed.add_field(name="CHARACTER", value=f"{char['name']}", inline=True)

                        img_list = os.listdir("metadata/character")
                        for img in img_list:
                            if img == f"{char['id']}.png":
                                file1 = discord.File(f"metadata/character/{char['id']}.png", filename=f"{char['id']}.png")
                                embed.set_thumbnail(url=f"attachment://{char['id']}.png")

                        break

                for track_temp in track_json:
                    if track_temp["id"] == most_item(track):
                        embed.add_field(name="MOST TRACK", value=f"{track_temp['name']}", inline=True)

                        img_list = os.listdir("metadata/track")
                        for img in img_list:
                            if img == f"{track_temp['id']}.png":
                                file2 = discord.File(f"metadata/track/{track_temp['id']}.png", filename=f"{track_temp['id']}.png")
                                embed.set_image(url=f"attachment://{track_temp['id']}.png")

                        break

                return await ctx.send(embed=embed, files=[file1, file2])

            else:
                raise Exception("Exception: 유저 매치 데이터를 불러오는데에 실패했습니다.")

        else:
            raise Exception("NotFoundUser: 존재하지 않는 카트라이더 라이더명입니다.")