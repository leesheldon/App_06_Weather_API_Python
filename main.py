from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)


stations = pd.read_csv("data_small/stations.txt", skiprows=17)
stations = stations[["STAID", "STANAME                                 "]]


@app.route("/")
def home():
    return render_template("home.html", data=stations.to_html())


@app.route("/api/v1/<station>/<date>")
def about(station, date):
    filepath = "data_small/TG_STAID" + str(station).zfill(6) + ".txt"
    df = pd.read_csv(filepath, skiprows=20, parse_dates=["    DATE"])
    temperature = df.loc[df["    DATE"] == date]["   TG"].squeeze() / 10
    return {"station": station,
            "date": date,
            "temperature": temperature}


@app.route("/api/v1/<station>")
def all_dates_one_station(station):
    filepath = "data_small/TG_STAID" + str(station).zfill(6) + ".txt"
    df = pd.read_csv(filepath, skiprows=20, parse_dates=["    DATE"])
    result = df.to_dict(orient="records")
    return result


@app.route("/api/v1/yearly/<station>/<year>")
def yearly_one_station(station, year):
    filepath = "data_small/TG_STAID" + str(station).zfill(6) + ".txt"

    # This way will keep the DATE column type as DateTime type in the output
    df = pd.read_csv(filepath, skiprows=20, parse_dates=["    DATE"])
    result = df[df["    DATE"].dt.year == int(year)].to_dict(orient="records")

    # This way will keep the DATE column type as String type in the output
    # df = pd.read_csv(filepath, skiprows=20)
    # df["    DATE"] = df["    DATE"].astype(str)
    # result = df[df["    DATE"].str.startswith(str(year))].to_dict(orient="records")

    return result


if __name__ == "__main__":
    app.run(debug=True)
