from app import app
from flask import render_template, request, session
from datetime import datetime
# import sqlite3
from models.index_model import get_teachers, get_students, get_timetable, get_timetable_date, get_lessons, get_lessons_ultra, get_price, get_lessons_pro_for_teachers
from utils import get_db_connection
# from models.index_model import get_reader, get_book_reader, get_new_reader, return_book,borrow_book


@app.route('/', methods=['GET', 'POST'])
def index():
    conn = get_db_connection()

    current_date = datetime.now().date().strftime("%Y-%m-%d")

    start_date = current_date
    count_days = 5


    # if request.method == 'POST':
    type = request.values.get("selected_type")
    print(type)
    if type:
        # if type == "day":
        #     df_lessons = get_lessons_report(conn, start_date, count_days, session['level_name'])
        # elif type == "teacher":
        #     df_lessons = get_lessons_report_by_teacher(conn, start_date, count_days, session['level_name'])
        current_type = type

    elif request.values.get("show_with_date"):
        start_date_str = request.values.get("start_date")
        # start_date = datetime.strptime(start_date_str, "%Y-%m-%d").strftime('%d-%m-%Y')
        start_date = start_date_str
        count_days = int(request.values.get("count_days"))
        current_date = start_date
        level_id = request.values.get("selected_level")
        session['level_name'] = level_id
        current_type = request.values.get("current_type")

    else:
        # df_lessons = get_lessons_report_by_teacher(conn, start_date, count_days, session['level_name'])
        current_type = "day"
        session['level_name'] = "1"

    if current_type == "day":
        # df_lessons = get_lessons_ultra(conn, start_date, count_days, "A")
        # print(start_date, count_days, session['level_name'])
        df_lessons = get_lessons_ultra(conn, start_date, count_days, session['level_name'])
    elif current_type == "teacher":
        df_lessons = get_lessons_pro_for_teachers(conn, start_date, count_days, session['level_name'])
    else:
        df_lessons = None
        print("ошибка")

    # print(current_date)

    # date_obj = datetime.strptime(current_date, "%d-%m-%Y")
    # converted_date_str = date_obj.strftime("%Y-%m-%d")
    # print(get_price(conn))
    # print(session['level_name'])
    print(df_lessons)
    html = render_template(
        'index.html',
        lessons=df_lessons,
        cur_date=current_date,
        cnt_days=count_days,
        lvl_name=int(session['level_name']),
        combo_box=get_price(conn),
        cur_type=current_type,
        len=len
    )
    return html


if __name__ == '__main__':
    app.run(debug=True)