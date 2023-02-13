from argparse import ArgumentParser
from datetime import datetime
from pathlib import Path

from utils import jinja_env, nowbeijing, pximg_reverse_proxy, xsession, get_original_imgurls

POST_DIR = Path("./source/_posts/pixivinfo/")
TEMPLATE_DIR = Path("./scripts_py/templates/")
CUMSTOM_FILTERS = {
    "url_pximg": pximg_reverse_proxy
}


def get_top10_details(type_: str = "daily") -> dict:
    """"""
    pixiv = xsession.Pixiv()
    pixiv.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0"
    })

    ### DEBUG ###
    # pixiv.proxies.update({
    #     "http": "http://127.0.0.1:10809",
    #     "https": "http://127.0.0.1:10809"
    # })

    if type_ == "monthly":
        ranking_data = pixiv.get_ranking_monthly()
    elif type_ == "weekly":
        ranking_data = pixiv.get_ranking_weekly()
    else:
        ranking_data = pixiv.get_ranking_daily()

    data = {}

    tags = set()
    illusts = []
    for content in ranking_data["contents"][:10]:
        illust_id = content["illust_id"]
        illust_info = pixiv.get_illust(illust_id)
        illust_urls = pixiv._get_illust_pages(illust_id)

        # 手动生成 illust_info 里的 url
        if not illust_urls:
            illust_urls = get_original_imgurls(illust_id, content["url"], int(content["illust_page_count"]))

        # 替换掉 illust_info 里的 url
        illust_info["urls"] = illust_urls

        illusts.append(illust_info)
        tags.update(t["tag"] for t in illust_info["tags"]["tags"])

    data["rank_date"] = datetime.strptime(ranking_data["date"], "%Y%m%d")
    data["tags"] = sorted(tags)
    data["illusts"] = illusts

    return data


def gen_daily_top10():
    env = jinja_env(TEMPLATE_DIR, CUMSTOM_FILTERS)
    today = nowbeijing()

    # daily top10 blog
    render_content = {
        "today": today,
        "rank_type": "日"
    }
    ranking_data = get_top10_details("daily")
    render_content.update(ranking_data)

    tmp = env.get_template("dailytop10.jinja2")
    output = tmp.render(render_content)

    filename = f"dailytop10-{ranking_data['rank_date'].strftime('%Y%m%d')}"
    save_path = POST_DIR.joinpath(f"{ranking_data['rank_date'].strftime('%Y/%m/%d')}/{filename}.md")
    save_path.parent.mkdir(parents=True, exist_ok=True)
    save_path.write_text(output, encoding="utf8")


def gen_monthly_top10():
    env = jinja_env(TEMPLATE_DIR, CUMSTOM_FILTERS)
    today = nowbeijing()

    # monthly top10 blog
    render_content = {
        "today": today,
        "rank_type": "月"
    }
    ranking_data = get_top10_details("monthly")
    render_content.update(ranking_data)

    tmp = env.get_template("monthlytop10.jinja2")
    output = tmp.render(render_content)

    filename = f"monthlytop10-{ranking_data['rank_date'].strftime('%Y%m%d')}"
    save_path = POST_DIR.joinpath(f"{ranking_data['rank_date'].strftime('%Y/%m/%d')}/{filename}.md")
    save_path.parent.mkdir(parents=True, exist_ok=True)
    save_path.write_text(output, encoding="utf8")


if __name__ == "__main__":
    parser = ArgumentParser()

    parser.add_argument("--daily_top10", action="store_true")
    parser.add_argument("--monthly_top10", action="store_true")

    args = parser.parse_args()

    if args.daily_top10:
        gen_daily_top10()
    if args.monthly_top10:
        gen_monthly_top10()
