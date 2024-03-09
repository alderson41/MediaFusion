import aiohttp
import asyncio
import lxml.html
import hashlib
import io
import json


forum_hashes = {}

forums = {
    "tamil_blasters": {
	"homepage": "https://www.1tamilblasters.zip",
	"catalogs": {
	  "tamil": {
		"hdrip": "7-tamil-new-movies-hdrips-bdrips-dvdrips-hdtv",
		"tcrip": "8-tamil-new-movies-tcrip-dvdscr-hdcam-predvd",
		"dubbed": "9-tamil-dubbed-movies-bdrips-hdrips-dvdscr-hdcam-in-multi-audios",
		"series": "63-tamil-new-web-series-tv-shows",
		"old": "56-tamil-old-mid-movies-bdrips-hdrips-dvdrips-hdtv"
	  },
	  "malayalam": {
		"tcrip": "75-malayalam-new-movies-tcrip-dvdscr-hdcam-predvd",
		"hdrip": "74-malayalam-new-movies-hdrips-bdrips-dvdrips-hdtv",
		"dubbed": "76-malayalam-dubbed-movies-bdrips-hdrips-dvdscr-hdcam",
		"series": "98-malayalam-new-web-series-tv-shows",
		"old": "77-malayalam-old-mid-movies-bdrips-hdrips-dvdrips"
	  },
	  "telugu": {
		"tcrip": "79-telugu-new-movies-tcrip-dvdscr-hdcam-predvd",
		"hdrip": "78-telugu-new-movies-hdrips-bdrips-dvdrips-hdtv",
		"dubbed": "80-telugu-dubbed-movies-bdrips-hdrips-dvdscr-hdcam",
		"series": "96-telugu-new-web-series-tv-shows",
		"old": "81-telugu-old-mid-movies-bdrips-hdrips-dvdrips"
	  },
	  "hindi": {
		"tcrip": "87-hindi-new-movies-tcrip-dvdscr-hdcam-predvd",
		"hdrip": "86-hindi-new-movies-hdrips-bdrips-dvdrips-hdtv",
		"dubbed": "88-hindi-dubbed-movies-bdrips-hdrips-dvdscr-hdcam",
		"series": "89-hindi-new-web-series-tv-shows",
		"old": "102-hindi-old-mid-movies-bdrips-hdrips-dvdrips"
	  },
	  "kannada": {
		"tcrip": "83-kannada-new-movies-tcrip-dvdscr-hdcam-predvd",
		"hdrip": "82-kannada-new-movies-hdrips-bdrips-dvdrips-hdtv",
		"dubbed": "84-kannada-dubbed-movies-bdrips-hdrips-dvdscr-hdcam",
		"series": "103-kannada-new-web-series-tv-shows",
		"old": "85-kannada-old-mid-movies-bdrips-hdrips-dvdrips"
	  },
	  "english": {
		"tcrip": "52-english-movies-hdcam-dvdscr-predvd",
		"hdrip": "53-english-movies-hdrips-bdrips-dvdrips",
		"series": "92-english-web-series-tv-shows"
	  }
	}
  }
}


def compute_hash(cont: str) -> str:
    md5 = hashlib.md5(cont.encode())
    return md5.hexdigest()


async def grab_updates(session: aiohttp.ClientSession, url:str) -> None:
    '''
    
    '''


async def chk_updates(session: aiohttp.ClientSession, url:str, lang:str, cat:str, site:str) -> None:
    cont = await send_req(session, url)
    if site not in forum_hashes:
        forum_hashes[site] = {}
    if lang not in forum_hashes[site]:
        forum_hashes[site][lang] = {}
    hash_val = compute_hash(cont) 

    if cat in forum_hashes[site][lang]:
        if forum_hashes[site][lang][cat] == hash_val:
            print(f'No Updates found in {site} -> {lang} -> {cat}')
        else:
            print(f'**Updates found in {site} -> {lang} -> {cat}')
            forum_hashes[site][lang][cat] = hash_val
    else:
        print(f'First run Updates found in {site} -> {lang} -> {cat}')
        forum_hashes[site][lang][cat] = hash_val


async def send_req(session: aiohttp.ClientSession, url:str) -> str:
    async with session.get(url) as resp:
        res = await resp.text()
        parser = lxml.html.parse(io.StringIO(res))
        container = parser.xpath('//ol[@class="ipsDataList ipsDataList_zebra ipsClear cForumTopicTable  cTopicList "]')
        movies = container[0].xpath('.//span[@class="ipsType_break ipsContained"]/a/@title')
        movs = ''.join(i for i in movies)
        return movs
    

async def main():
    site = 'tamil_blasters'
    base_link = 'https://www.1tamilblasters.fans/index.php?/forums/forum/{}'
    async with aiohttp.ClientSession() as session:
        generated = [
            {"url": base_link.format(cat_url), "lang": lang, "cat": cat, "site": site, "session": session}
            for lang, categories in forums[site]['catalogs'].items()
            for cat, cat_url in categories.items()
        ]

        tasks = [asyncio.create_task(chk_updates(**kwargs)) for kwargs in generated]
        await asyncio.gather(*tasks)


if __name__ == '__main__':
    
    old_hash = open('hash.json', 'r')
    forum_hashes = json.loads(old_hash.read())
    old_hash.close()
    asyncio.run(main())
    f = open('hash.json', 'w')
    json.dump(forum_hashes, f, indent=4, sort_keys=False)
