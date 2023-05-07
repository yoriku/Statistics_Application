from flask import Flask, render_template, request
import pandas as pd
import function as func

app = Flask(__name__, template_folder='static')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        target_name = request.form.get('target_name')
        stat_mode = request.form.get('stat_mode')
        class_weight = request.form.get('class_weight')

        # Check input items
        if not file:
            return render_template('index.html', error="Error : Enter your file")
        if not('.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in set(["csv"])):
            return render_template('index.html', error="Error : You can use only csv file")
        if target_name is None or stat_mode is None or class_weight is None:
            return render_template('index.html', error="Error : Enter your params")
        
        target_name = str(target_name)

        df = pd.read_csv(file)

        # check columns name
        if target_name not in df.columns:
            return render_template('index.html', error="Error : Not exist target row")

        # plot boxplot
        fig = func.plot(df, target_name)
        fig.update_layout(title='Box plot')

        # calc stat ind
        stat_mode = func.return_mode(int(stat_mode))
        rows = func.calc_stat(df, target_name, mode=stat_mode)
        # table = func.convart_table(stat_bm)

        # eval using Logistic Regression
        class_weight = int(class_weight)
        cm, metr, header = func.eval_model(df, target_name, class_weight)
        fig_cm = func.plot_cm(cm)

        graph = fig.to_html(full_html=False)
        graph_cm = fig_cm.to_html(full_html=False)
        return render_template('index.html', graph=graph, rows=rows, graph_cm=graph_cm, metr=zip(header, metr), show=True)
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
