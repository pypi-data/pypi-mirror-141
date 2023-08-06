import click
import requests
import pickle
from pathlib import Path

__author__ = "dynamicfire"
api_key = ""
loc_id = ""

@click.group()
def main():
    """
    CLI for querying weather
    """
    pass


@main.command()
@click.option("--key", default="!!!", help="API key for qweather")
@click.option("--id", default="!!!", help="Location ID for weather querying")
def config(key, id):
    """
    Configure weather cli
    """
    if key != "!!!":
        click.echo(click.style(f"Your key set as {key}", fg="green"))
        storeData("weather_api", key)
    if id != "!!!":
        click.echo(click.style(f"Your location ID set as {id}", fg="green"))
        storeData("weather_id", id)
    if key == "!!!" and id == "!!!":
        click.echo(click.style(f"Use --key <key> to set API key; --id <location-id> to set location id", fg="red"))


@main.command()
@click.argument('name', default="")
def query_loc(name):
    """
    Search location id by name then return a result list with ID numbers
    """
    config_key_file = Path("weather_api")
    global api_key
    if config_key_file.is_file():
        api_key = loadData("weather_api")
        #print(api_key)
        url_format = 'https://geoapi.qweather.com/v2/city/lookup?location='

        url_format += name + "&key=" + api_key

        if name == "":
            click.echo(click.style(f"weather_cli query-loc <name> for querying location id", fg="red"))
        else:
            response = requests.get(url_format).json()

            if response["code"] == "200":
                for loc in response["location"]:
                    click.echo(click.style(f"Location ID: {loc['id']}", fg="green"))
                    click.echo(
                        click.style(f"Name: {loc['name']},{loc['adm2']},{loc['adm2']},{loc['country']}", fg="blue"))
                    print("====================")
            elif response["code"] == "204":
                click.echo(click.style(f"请求成功，但你查询的地区暂时没有你需要的数据。", fg="red"))
            elif response["code"] == "400":
                click.echo(click.style(f"请求错误，可能包含错误的请求参数或缺少必选的请求参数。", fg="red"))
            elif response["code"] == "401":
                click.echo(click.style(f"认证失败，可能使用了错误的KEY、数字签名错误、KEY的类型错误（如使用SDK的KEY去访问Web API）。", fg="red"))
            elif response["code"] == "402":
                click.echo(click.style(f"超过访问次数或余额不足以支持继续访问服务，你可以充值、升级访问量或等待访问量重置。", fg="red"))
            elif response["code"] == "403":
                click.echo(click.style(f"无访问权限，可能是绑定的PackageName、BundleID、域名IP地址不一致，或者是需要额外付费的数据。", fg="red"))
            elif response["code"] == "404":
                click.echo(click.style(f"查询的数据或地区不存在。", fg="red"))
            elif response["code"] == "429":
                click.echo(click.style(f"超过限定的QPM（每分钟访问次数），请参考QPM说明。", fg="red"))
            elif response["code"] == "500":
                click.echo(click.style(f"无响应或超时，接口服务异常。", fg="red"))
    else:
        click.echo(click.style(f"You haven't configured the API key yet.", fg="red"))




@main.command()
@click.option("--forecast_range", '-r', default=3, help="Forecast range.", type=int)
@click.option("--location", '-l', default="default", help="Location ID")
def query(forecast_range, location):
    """Query weather"""
    global api_key
    global loc_id
    forecast_range_set = 3

    config_key_file = Path("weather_api")
    if config_key_file.is_file():
        api_key = loadData("weather_api")
    else:
        click.echo(click.style(f"You haven't configured the API key yet.", fg="red"))

    config_id_file = Path("weather_id")
    if config_id_file.is_file():
        loc_id = loadData("weather_id")
    else:
        click.echo(click.style(f"You haven't configured the Location ID yet.", fg="red"))
        click.echo(click.style(f"Use --location to query specfic location, or weather_cli config --id to set location id.", fg="red"))

    if api_key != "" and loc_id != "":
        if forecast_range == 3 or forecast_range == 7:
            # click.echo(click.style(f"Your forecast range set as {forecast_range}-day", fg="green"))
            forecast_range_set = forecast_range

        if location != "default":
            loc_id = location

        url_format = 'https://devapi.qweather.com/v7/weather/'

        url_format += str(forecast_range_set) + "d?location=" + loc_id + "&key=" + api_key
        response = requests.get(url_format).json()

        query_id(loc_id)

        if response["code"] == "200":
            for loc in response["daily"]:
                click.echo(click.style(f"{loc['fxDate']}", fg="green"))
                click.echo(
                    click.style(f"白天：{loc['textDay']}，夜间：{loc['textNight']}；{loc['tempMin']}°C到{loc['tempMax']}°C",
                                fg="green"))
                print("====================")
        elif response["code"] == "204":
            click.echo(click.style(f"请求成功，但你查询的地区暂时没有你需要的数据。", fg="red"))
        elif response["code"] == "400":
            click.echo(click.style(f"请求错误，可能包含错误的请求参数或缺少必选的请求参数。", fg="red"))
        elif response["code"] == "401":
            click.echo(click.style(f"认证失败，可能使用了错误的KEY、数字签名错误、KEY的类型错误（如使用SDK的KEY去访问Web API）。", fg="red"))
        elif response["code"] == "402":
            click.echo(click.style(f"超过访问次数或余额不足以支持继续访问服务，你可以充值、升级访问量或等待访问量重置。", fg="red"))
        elif response["code"] == "403":
            click.echo(click.style(f"无访问权限，可能是绑定的PackageName、BundleID、域名IP地址不一致，或者是需要额外付费的数据。", fg="red"))
        elif response["code"] == "404":
            click.echo(click.style(f"查询的数据或地区不存在。", fg="red"))
        elif response["code"] == "429":
            click.echo(click.style(f"超过限定的QPM（每分钟访问次数），请参考QPM说明。", fg="red"))
        elif response["code"] == "500":
            click.echo(click.style(f"无响应或超时，接口服务异常。", fg="red"))


def storeData(key, vaule):
    # initializing data to be stored in db
    # database
    db = vaule

    # Its important to use binary mode
    dbfile = open(key, 'wb')

    # source, destination
    pickle.dump(db, dbfile)
    dbfile.close()


def loadData(key):
    # for reading also binary mode is important
    dbfile = open(key, 'rb')
    db = pickle.load(dbfile)
    temp = db
    dbfile.close()
    return temp


def query_id(name):
    """Search location id by name then return a result list with ID numbers"""
    config_key_file = Path("weather_api")
    global api_key
    if config_key_file.is_file():
        api_key = loadData("weather_api")
        url_format = 'https://geoapi.qweather.com/v2/city/lookup?location='

        url_format += name + "&key=" + api_key
        response = requests.get(url_format).json()

        if response["code"] == "200":
            for loc in response["location"]:
                click.echo(click.style(f"{loc['name']},{loc['adm2']},{loc['adm2']},{loc['country']}", fg="blue"))
                print("====================")
        elif response["code"] == "204":
            click.echo(click.style(f"请求成功，但你查询的地区暂时没有你需要的数据。", fg="red"))
        elif response["code"] == "400":
            click.echo(click.style(f"请求错误，可能包含错误的请求参数或缺少必选的请求参数。", fg="red"))
        elif response["code"] == "401":
            click.echo(click.style(f"认证失败，可能使用了错误的KEY、数字签名错误、KEY的类型错误（如使用SDK的KEY去访问Web API）。", fg="red"))
        elif response["code"] == "402":
            click.echo(click.style(f"超过访问次数或余额不足以支持继续访问服务，你可以充值、升级访问量或等待访问量重置。", fg="red"))
        elif response["code"] == "403":
            click.echo(click.style(f"无访问权限，可能是绑定的PackageName、BundleID、域名IP地址不一致，或者是需要额外付费的数据。", fg="red"))
        elif response["code"] == "404":
            click.echo(click.style(f"查询的数据或地区不存在。", fg="red"))
        elif response["code"] == "429":
            click.echo(click.style(f"超过限定的QPM（每分钟访问次数），请参考QPM说明。", fg="red"))
        elif response["code"] == "500":
            click.echo(click.style(f"无响应或超时，接口服务异常。", fg="red"))
    else:
        click.echo(click.style(f"You haven't configured the API key yet.", fg="red"))


if __name__ == "__main__":
    main()