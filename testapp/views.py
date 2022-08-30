import numbers
import csv
import datetime
import os
# from pickle import TRUE
from flask import render_template, request, redirect, url_for
from testapp import app
from testapp import db
from testapp.models.member import Member

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('testapp/index.html')
    if request.method == 'POST':
        form_number = request.form.get("number")
        members = Member.query.all()
        for member in members:
            if member.number == form_number:
                dt_now = datetime.datetime.now()
                file_name = str(datetime.date.today()) + '.csv'
                if os.path.exists(file_name) == False:
                    with open(file_name, "w", newline="", encoding="utf-8-sig") as f:
                        writer = csv.writer(f)
                        writer.writerow([member.number, member.name, dt_now])

                    return render_template('testapp/register.html', member=member)
                else:
                    with open(file_name, "r", encoding = 'utf_8_sig')as check:
                        reader = csv.reader(check)
                        for row in reader:
                            if row[0] == member.number:
                                return render_template('testapp/registered.html')
                    with open(file_name, 'a', newline="", encoding = 'utf_8_sig') as f:
                        writer = csv.writer(f)  
                        writer.writerow([member.number, member.name, dt_now])

                    return render_template('testapp/register.html', member=member)
            
        return render_template('testapp/unregistered.html')

@app.route('/add_member', methods=['GET', 'POST'])
def add_member():
    if request.method == 'GET':
        return render_template('testapp/add_member.html')
    if request.method == 'POST':
        form_number = request.form.get("number")  # str
        form_name = request.form.get("name")  # str
        member = Member(
            number=form_number,
            name=form_name
        )
        db.session.add(member)
        db.session.commit()
        return render_template('testapp/add_member.html')
        # return redirect(url_for('index'))

@app.route('/members')
def member_list():
    members = Member.query.all()
    return render_template('testapp/member_list.html', members=members)

@app.route('/members/<int:id>/edit', methods=['GET'])
def member_edit(id):
    # 編集ページ表示用
    member = Member.query.get(id)
    return render_template('testapp/member_edit.html', member=member)

@app.route('/members/<int:id>/update', methods=['POST'])
def member_update(id):
    member = Member.query.get(id)  # 更新するデータをDBから取得
    member.number = request.form.get('number')
    member.name = request.form.get('name')
    
    db.session.merge(member)
    db.session.commit()
    return redirect(url_for('member_list'))

@app.route('/members/<int:id>/delete', methods=['POST'])  
def member_delete(id):  
    member = Member.query.get(id)   
    db.session.delete(member)  
    db.session.commit()
    return redirect(url_for('member_list'))