from flask import Flask, render_template
import webpage
app = Flask(__name__)

@app.route("/")
def template_test():
    list_of_prs = webpage.week_old_comments()
    return render_template('week-old.html', my_list=list_of_prs)

@app.route("/no_discussion")
def no_discussion():
	list_of_prs = webpage.no_discussion()
	return render_template('no-discussion.html', my_list=list_of_prs)
	
def main():
    port = 3000
    app.run(port = port)