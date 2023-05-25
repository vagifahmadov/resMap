from setting.config import request, Blueprint, jsonify, render_template, json
from objects.defs import *

index = Blueprint('/', __name__)


@index.route('/', methods=['GET'])
def index_func():
    # vars
    headers = ['Name', 'Catagory', 'Rate', 'Address', 'Telephone', 'Photos_Place', 'Reviews_Count']
    big_data = big_datas()
    data = jinja_data_maker(titles=headers, datas=big_data)
    # split , - to get first image
    list(map(lambda d: d.update({'Photos_Place': str(d['Photos_Place']).split(",")[0]}), data))
    # print(data)
    return render_template("index.html", datas=data)


search = Blueprint('search', __name__)


@search.route('/search', methods=['GET'])
def search_func():
    # vars
    headers = ['Name', 'Catagory', 'Rate', 'Address', 'Telephone', 'Photos_Place', 'Reviews_Count']
    big_data = big_datas()
    data = jinja_data_maker(titles=headers, datas=big_data)
    # split , - to get first image
    list(map(lambda d: d.update({'Photos_Place': str(d['Photos_Place']).split(",")[0]}), data))
    # print(data)
    return render_template("search-listing.html", datas = data)


listing = Blueprint('listing', __name__)


@listing.route('/listing', methods=['GET'])
def listing_func():
    # vars
    id_data = request.args.get('id')
    data = None
    headers = [
        'Name',
        'Catagory',
        'Rate',
        'Address',
        'Telephone',
        'Photos_Place',
        'Reviews_Count',
        'Place_link',
        'Review_Comment_1',
        'Review_Comment_2',
        'Review_Comment_3',
        'Review_Rate_1',
        'Review_Rate_2',
        'Review_Rate_3',
        'Monday',
        'Tuesday',
        'Wednesday',
        'Thursday',
        'Friday',
        'Saturday',
        'Sunday',
        'Website'
    ]

    try:
        id_data = int(id_data) if id_data != "0" else id_data
    except (TypeError, KeyError, ValueError) as err:
        print(err)
        id_data = None
    if id_data is not None:
        data = jinja_data_maker(titles=headers, datas=big_datas(), col="id", parameter_value=str(id_data))
        if data is not None:
            # split , - to get first image
            data.update({'Photos_Place': str(data['Photos_Place']).split(",")[0], 'Photos_Header': str(data['Photos_Place']).split(",")[1]})
    render_html = "listing-detail.html" if data is not None else "404.html"
    return render_template(render_html, datas=data)
