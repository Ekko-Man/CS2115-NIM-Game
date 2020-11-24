import os
import json
from flask import Flask, flash, request, redirect, render_template, url_for, session, request
from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField
from wtforms.validators import DataRequired


app = Flask(__name__)
app.secret_key = os.environ.get('secret_key') or "This_is_the_secret"

# class PileForm(FlaskForm):
#     num_pile = IntegerField('pile', validators=[DataRequired()])
#     num_stone = IntegerField('stone', validators=[DataRequired()])
#     submit = SubmitField('Submit')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/rule')
def rule():
    return render_template('rule.html')

@app.route('/play', methods=['GET', 'POST'])
def play():
    if request.method == 'POST':
        num_pile = request.form.get("num_pile")
        num_stone = request.form.get("num_stone")
        num_pile = int(num_pile)

        print(f"num_pile: {num_pile}, num_stone: {num_stone}\n")
        list_num_stone = ""
        list_num_stone += f"{num_stone}"
        for i in range(num_pile):
            list_num_stone += f"-{num_stone}"
        print(f"pile= {num_pile}, list_stone= {list_num_stone}")

        return redirect(url_for('game', num_pile=num_pile, list_num_stone=list_num_stone))
    elif request.method == 'GET':
        return render_template('play.html')
    else:
        return "only accept GET and POST"

@app.route('/game/pile<num_pile>/stone<list_num_stone>')
def game(num_pile, list_num_stone):
    num_pile = int(num_pile)
    print("game pass render; ", list_num_stone)
    if "-" in list_num_stone:
        list_num_stone = list_num_stone.split("-")
    print("game pass renderzzzzz; ", list_num_stone)
    return render_template('game.html', list_num_stone=list_num_stone, num_pile=num_pile)
    # return f"pile= {num_pile}, list_stone= {list_num_stone}"


def convert_list_num_stone_to_str(list_num_stone):
    str_list = ""
    a = list_num_stone[0]
    str_list += f"{a}"

    if len(list_num_stone) >1 :
        for x in list_num_stone[1:]:
            str_list+=f"-{x}"
    print("convert_list_num_stone_to_str:" , str_list)
    return str_list

def find_min_factor(num):
    yes = None
    for i in range(1, num + 1):
        if (num % i == 0) and (num != 1) and (num != num):
            yes = i
            return yes
    return yes

def end_game(list_num_stone):
    for a in list_num_stone:
        if a != 1:
            return False
    return True

@app.route('/move', methods=['POST'])
def move():
    num_pile = int(request.form.get("num_pile"))
    left_stone = request.form.get("left_stone")
    move_pile = request.form.get("move_pile")

    left_stone = int(left_stone)
    move_pile = int(move_pile)



    # Get list of num_pile
    tmp_li = range(0, num_pile)
    list_num_stone = []
    for i in tmp_li:
        tmp_num_stone = request.form.get(f"pile_{i}")
        list_num_stone.append(int(tmp_num_stone))

    # Check vaild
    if move_pile > num_pile:    #test after left
        print("A out ")
        print(f"list_num_stone: {list_num_stone}\n")
        list_num_stone =convert_list_num_stone_to_str(list_num_stone)
        flash(f"The {(move_pile+1)} is not exist.")
        return redirect(url_for('game', list_num_stone=list_num_stone , num_pile=num_pile))
    elif left_stone > list_num_stone[move_pile-1]:
        print("B out ")
        print(f"list_num_stone: {list_num_stone}\n")
        list_num_stone =convert_list_num_stone_to_str(list_num_stone)
        flash(f"The {left_stone} is smaller than  {list_num_stone[move_pile-1]}")
        return redirect(url_for('game', list_num_stone=list_num_stone , num_pile=num_pile))
    elif list_num_stone[move_pile-1] == left_stone:
        flash(f"Please take other pile of stones")
        list_num_stone = convert_list_num_stone_to_str(list_num_stone)
        return redirect(url_for('game', list_num_stone=list_num_stone , num_pile=num_pile))


   
    # evenly divides
    ed_list = []
    ed_int = list_num_stone[move_pile-1]
    for i in range(1, ed_int + 1):
        if ed_int % i == 0:
            ed_list.append(i)
    print("ed_list: ", ed_list)
    if left_stone not in ed_list:
        print("c out")
        print(f"list_num_stone: {list_num_stone}\n")
        flash(f"The {list_num_stone[move_pile-1]} can't evenly divide by {left_stone}")
        list_num_stone =convert_list_num_stone_to_str(list_num_stone)
        return redirect(url_for('game', list_num_stone=list_num_stone , num_pile=num_pile))

    list_num_stone[move_pile-1] = left_stone

    if end_game(list_num_stone):
        list_num_stone =convert_list_num_stone_to_str(list_num_stone)
        flash(f"Player win")
        return redirect(url_for('game', list_num_stone=list_num_stone , num_pile=num_pile))

    print(f"\nmove_pile: {move_pile}, left_stone: {left_stone}")
    print(f"num_pile: {num_pile}, list_num_stone: {list_num_stone}\n")

    real_exist_pile = 0
    for ex_pi in list_num_stone:
        apple = False
        for i in range(1, ex_pi + 1):
            if ex_pi % i == 0:
                if (i != 1):
                    apple = True
                    break
        if apple:
            real_exist_pile += 1

    pc_move_pile = 0
    if real_exist_pile ==1:
        for ap in list_num_stone:
            pc_move_pile += 1
            if ap != 1:
                list_num_stone[pc_move_pile-1] = 1
                break
        flash("PC win")
        return redirect(url_for('play'))
    elif real_exist_pile % 2 != 0:
        for ap in list_num_stone:
            pc_move_pile += 1
            if ap != 1:
                list_num_stone[pc_move_pile-1] = 1
                break
        flash(f"PC take the {pc_move_pile} pile left 1")
        list_num_stone = convert_list_num_stone_to_str(list_num_stone)
        return redirect(url_for('game', list_num_stone=list_num_stone , num_pile=num_pile))
    elif (real_exist_pile % 2 == 0) and (real_exist_pile > 2):
        min_factor = None
        for ap in list_num_stone:
            pc_move_pile += 1
            if ap != 1:
                min_factor = find_min_factor(list_num_stone[pc_move_pile-1])
                if min_factor:
                    list_num_stone[pc_move_pile-1] = min_factor
                    break
        if min_factor:
            flash(f"PC take the {pc_move_pile} pile left {min_factor}")
            list_num_stone = convert_list_num_stone_to_str(list_num_stone)
            return redirect(url_for('game', list_num_stone=list_num_stone , num_pile=num_pile))
        else:
            pc_move_pile = 0
            for ap in list_num_stone:
                pc_move_pile += 1
                if ap != 1:
                    list_num_stone[pc_move_pile-1] = 1
                    break
            flash(f"PC take the {pc_move_pile} pile left 1")
            list_num_stone = convert_list_num_stone_to_str(list_num_stone)
            return redirect(url_for('game', list_num_stone=list_num_stone , num_pile=num_pile))
    elif (real_exist_pile % 2 == 0) and (real_exist_pile == 2):
        min_factor = None
        for ap in list_num_stone:
            pc_move_pile += 1
            if ap != 1:
                min_factor = find_min_factor(list_num_stone[pc_move_pile-1])
                if min_factor:
                    list_num_stone[pc_move_pile-1] = min_factor
                    break
        if min_factor:
            flash(f"PC take the {pc_move_pile} pile left {min_factor}")
            list_num_stone = convert_list_num_stone_to_str(list_num_stone)
            return redirect(url_for('game', list_num_stone=list_num_stone , num_pile=num_pile))
        else:
            pc_move_pile = 0
            for ap in list_num_stone:
                pc_move_pile += 1
                if ap != 1:
                    list_num_stone[pc_move_pile-1] = 1
                    break
            flash(f"PC take the {pc_move_pile} pile left 1")
            list_num_stone = convert_list_num_stone_to_str(list_num_stone)
            return redirect(url_for('game', list_num_stone=list_num_stone , num_pile=num_pile))
    else:
        raise "Error"



#         flash(f"PC take the {pc_move_pile} pile left 1")
#         list_num_stone = convert_list_num_stone_to_str(list_num_stone)
#         return redirect(url_for('game', list_num_stone=list_num_stone , num_pile=num_pile))


#             elif real_exist_pile > 2:
#                 if ap != 1:
#                     list_num_stone[pc_move_pile-1] = 1
#                     break
#             flash(f"PC take the {pc_move_pile} pile left 1")
#             list_num_stone = convert_list_num_stone_to_str(list_num_stone)
#             return redirect(url_for('game', list_num_stone=list_num_stone , num_pile=num_pile))
#     #pc_move_pile_real







# # -If N is even, Second player can do same operation for first players. For example,
# #      if First player move {4, 4, 4, 4} -> {2, 4, 4, 4},
# #      Second player can move {2, 4, 4, 4} -> {2, 2, 4, 4}.
# #      Finally Second player can make {1, 1, 1, ..., 1}, so Second player can win.
# # -If N is odd, First player can reduce height of first tower to 1,
# #      so you can return to "N is even" case.
# #      So, you can prove that first player wins.

#     list_num_stone =convert_list_num_stone_to_str(list_num_stone)
#     flash('Happy')
#     return redirect(url_for('game', list_num_stone=list_num_stone , num_pile=num_pile))


if __name__ == '__main__':
    app.run()
