from website import create_app

app = create_app()

#only if we run this main.py file are
#we going to execute the name fn

if __name__== '__main__':
    app.run(debug=True) #debug = True will rerun the
    #program if we make any changes to our code