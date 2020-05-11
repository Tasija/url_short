"""Flask Url Shortener service."""

from flask import Flask, jsonify, render_template, request, redirect

import shortener

app = Flask(__name__)


@app.route("/", methods=["GET"])
def shorten_url_form():
    return render_template("url_form.html")


@app.route("/shorten", methods=["POST"])
def shorten_original_url():
    if request.json:
        original_url = request.json["url"]
    else:
        original_url = request.form.get("url", "")
    short_url = shortener.get_short_url(original_url)

    return jsonify(short_url), 200


@app.route("/<url_key>", methods=["GET"])
def go_to_original_url(url_key=None):
    if len(url_key) > 2:
        return jsonify("Invalid short Url"), 400

    original_url = shortener.get_original_url(url_key)
    if original_url and not "http" in original_url:
        original_url = "http://" + original_url
    if original_url:
        return redirect(original_url)
    else:
        return jsonify("Not yet short url there"), 404


@app.route("/admin", methods=["GET"])
def show_admin_urls():
    # sort by call count
    all_urls = sorted(
        shortener.id_url_map.values(), key=lambda x: x[3], reverse=True)

    return render_template("admin.html", all_urls=all_urls)
